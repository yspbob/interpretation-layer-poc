"""Subscription schedule and stops with artificial material, no model calls."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from harness import digest, wire
from qualification_batch import load_bank
from subscription_batch import (SubscriptionBatch, account_observation, approval_template,
                                configuration, exchange_observation, sha, validate_approval)
from test_qualification_batch import synthetic_bank, synthetic_answer


class SubscriptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        frozen = synthetic_bank(self.root / "bank")
        self.bank = load_bank(self.root / "bank", "freeze.json", frozen)
        self.exe = self.root / "client"; self.exe.write_text("artificial executable, never launched")
        self.catalog = self.root / "catalog"; self.catalog.write_text("{}")
        self.addCleanup(patch.stopall)
        patch("subscription_batch.CLIENT_HASH", sha(self.exe)).start()
        patch("subprocess.Popen", side_effect=AssertionError("Process forbidden in batch unit tests")).start()
        patch("socket.socket.connect", side_effect=AssertionError("Network forbidden")).start()
        self.config = configuration(self.bank, self.root / "out", self.exe, self.catalog, "artificial-account")
        self.calls = []

    def observation(self, row):
        raw = {"ordinaryUsageAllowed": True, "accountId": "artificial-account", "rateLimits": {
            "limitId": "codex", "primary": {"usedPercent": 20}, "secondary": {"usedPercent": 30},
            "credits": {"hasCredits": False, "balance": "0"}}}
        return account_observation(raw, row["id"])

    def collector(self, path, expected, folder, exe, catalog, **kwargs):
        kwargs["dispatch_guard"]()
        self.assertEqual(sha(path), expected)
        self.assertIsNone(kwargs["auth_path"])
        packet = json.loads(path.read_text())
        self.calls.append(packet)
        folder.mkdir()
        answer = synthetic_answer(packet)
        (folder / "first-answer.txt").write_bytes(wire(answer))
        return {"status": "structurally_valid", "role": packet["role"], "answer_hash": digest(answer),
                "thread_id": f"artificial-{len(self.calls)}", "usage": {"input_tokens": 100, "output_tokens": 20}}

    def batch(self, collector=None):
        return SubscriptionBatch(self.bank, self.root / "out", self.config,
                                 simulation_collector=collector or self.collector)

    def test_full_144_schedule_and_commitment(self):
        b = self.batch(); result = b.run(self.observation)
        self.assertEqual(result["counts"], {"structurally_valid": 144})
        self.assertEqual(result["model_calls"], 0)
        self.assertFalse(result["qualified"])
        self.assertEqual(result["known_input_tokens"], 14400)
        self.assertEqual([r["id"] for r in result["outcomes"]], [r["id"] for r in self.bank.schedule])
        frozen = json.loads((b.folder / "collection-freeze.json").read_text())
        self.assertTrue(all(sha(b.folder / p) == h for p, h in frozen["files"].items()))
        for packet in self.calls:
            self.assertEqual("reference" in packet, packet["role"] != "verifier")
        with self.assertRaises(ValueError): b.run(self.observation)
        with self.assertRaises(FileExistsError): self.batch()

    def test_failed_attempt_stops_and_is_not_replaced(self):
        def fail(*a, **kw):
            self.collector(*a, **kw)
            raise ValueError("Artificial failure")
        r = self.batch(fail).run(self.observation)
        self.assertEqual(r["counts"], {"failed": 1, "not_run": 143})
        self.assertEqual(r["collector_attempts"], 1)

    def test_stale_or_paid_allowance_stops_before_reservation(self):
        for field, value in (("observed_at", 0), ("has_credits", True), ("remaining_percent", 10),
                             ("account_id", "wrong"), ("scheduled_id", "wrong")):
            with self.subTest(field=field):
                target = self.root / field
                config = configuration(self.bank, target, self.exe, self.catalog, "artificial-account")
                b = SubscriptionBatch(self.bank, target, config, simulation_collector=self.collector)
                r = b.run(lambda row: {**self.observation(row), field: value})
                self.assertEqual(r["counts"], {"not_run": 144})
                self.assertEqual(r["collector_attempts"], 0)

    def test_session_reuse_stops(self):
        def same(*a, **kw):
            return {**self.collector(*a, **kw), "thread_id": "same"}
        r = self.batch(same).run(self.observation)
        self.assertEqual(r["counts"], {"structurally_valid": 1, "failed": 1, "not_run": 142})

    def test_wrong_response_identity_stops(self):
        def wrong(*a, **kw):
            return {**self.collector(*a, **kw), "answer_hash": "0" * 64}
        r = self.batch(wrong).run(self.observation)
        self.assertEqual(r["counts"], {"failed": 1, "not_run": 143})

    def test_config_drift_after_account_check_prevents_dispatch(self):
        def alter(row):
            self.catalog.write_text("changed")
            return self.observation(row)
        r = self.batch().run(alter)
        self.assertEqual(r["collector_attempts"], 0)

    def test_operator_stop_during_collection_invalidates_answer(self):
        def stop(*a, **kw):
            result = self.collector(*a, **kw)
            (self.root / "out/STOP").write_text("stop")
            return result
        r = self.batch(stop).run(self.observation)
        self.assertEqual(r["counts"], {"failed": 1, "not_run": 143})

    def test_approval_defaults_are_closed_and_bound(self):
        a = approval_template(self.config)
        with self.assertRaises(ValueError): validate_approval(a, self.config)
        a.update(run_authorised=True, protocol_accepted=True, approval_reference="artificial consent", expires_at="2099-01-01T00:00:00+00:00")
        validate_approval(a, self.config)
        with self.assertRaises(ValueError): validate_approval(a, {**self.config, "effort": "low"})
        a["expires_at"] = "2000-01-01T00:00:00+00:00"
        with self.assertRaises(ValueError): validate_approval(a, self.config)

    def test_all_core_windows_considered(self):
        r = self.observation({"id": "artificial"})
        self.assertEqual(r["remaining_percent"], 70)
        with self.assertRaises(ValueError): account_observation({}, "artificial")

    def test_revocation_in_live_control_path_stops_fake_transport(self):
        approval = approval_template(self.config)
        approval.update(run_authorised=True, protocol_accepted=True, approval_reference="TEST ONLY",
                        expires_at="2099-01-01T00:00:00+00:00")
        path = self.root / "approval.json"; path.write_bytes(wire(approval))
        def revoked(*a, **kw):
            path.write_text("{}")
            kw["dispatch_guard"]()
            self.fail("Revocation must stop dispatch")
        with patch("subscription_batch.run_packet", side_effect=revoked):
            b = SubscriptionBatch(self.bank, self.root / "out", self.config, approval_path=path, auth_path="FAKE_NOT_READ")
            result = b.run(self.observation)
        self.assertEqual(result["counts"], {"failed": 1, "not_run": 143})

    def test_account_exchange_rejects_old_receipt(self):
        folder = self.root / "observations"; folder.mkdir()
        (folder / "S.response.json").write_bytes(wire({"scheduled_id": "S", "observed_at": 0, "raw": {}}))
        with self.assertRaises(ValueError): exchange_observation(folder, {"id": "S"}, lambda: None)

    def test_collector_rejects_wrong_qualification_permit_before_launch(self):
        from codex_subscription import run_packet
        from test_codex_subscription import public_packet
        packet = self.root / "single.json"; packet.write_bytes(wire(public_packet("verifier")))
        permit = {"packet_hash": "0" * 64, "output_path": str(self.root / "attempt"),
                  "allocation_hash": "artificial", "approval_reference": "TEST ONLY"}
        with patch("codex_subscription.CLIENT_HASH", sha(self.exe)), self.assertRaises(ValueError):
            run_packet(packet, sha(packet), self.root / "attempt", self.exe, self.catalog,
                       auth_path="FAKE_NOT_READ", account_observation=self.observation({"id": "S"}),
                       qualification_permit=permit, dispatch_guard=lambda: None)
        self.assertFalse((self.root / "attempt").exists())


if __name__ == "__main__":
    unittest.main()
