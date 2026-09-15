"""Live controller path with fictional credentials and local HTTP responses only."""
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import hashlib
import tempfile
import unittest
from unittest.mock import patch

from harness import digest, wire
from live_qualification import (GATES, LiveQualificationBatch, approval_template,
                                configuration, fingerprint, preflight, commit_collection)
from provider import Settings, httpx, strict_json
from qualification_batch import load_bank
from test_provider import response_record
from test_qualification_batch import synthetic_answer, synthetic_bank


class LiveBatchTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        frozen = synthetic_bank(self.root / "bank")
        self.bank = load_bank(self.root / "bank", "freeze.json", frozen)
        self.settings = Settings("fixture-model", "high", 32768, 8192, 1, 2, 20_000_000, 12)
        self.key = "FICTIONAL_TEST_CREDENTIAL_NOT_A_PROVIDER_KEY"
        self.out = self.root / "collection"
        self.approval_path = self.root / "approval.json"
        self.requests = []
        self.after_request = lambda: None
        self.addCleanup(patch.stopall)
        patch("socket.socket.connect", side_effect=AssertionError("External network forbidden")).start()
        self.transport = patch("provider.httpx.HTTPTransport",
            side_effect=lambda **kwargs: httpx.MockTransport(self.handler)).start()
        self.configure()

    def configure(self):
        self.config = configuration(self.bank, self.settings, self.out, fingerprint(self.key), "TEST ONLY")
        self.approval = approval_template(self.config)
        self.approval.update({g: True for g in GATES})
        self.approval.update(expires_at=(datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                             approval_reference="SYNTHETIC TEST ONLY; not user authorisation")
        self.approval_path.write_bytes(wire(self.approval))

    def handler(self, request):
        body = strict_json(request.content)
        expected = self.bank.items[self.bank.schedule[len(self.requests)]["item_id"]]
        self.assertEqual(body["instructions"], expected["instruction"])
        self.assertEqual(strict_json(body["input"][0]["content"]), expected["packet"])
        self.assertEqual(len(body["input"]), 1)
        self.assertNotIn("previous_response_id", body)
        self.assertNotIn("conversation", body)
        self.assertEqual(body["tools"], [])
        self.assertFalse(body["store"])
        self.assertNotIn("SEALED_ANSWER_NEVER_READ", wire(body).decode())
        self.requests.append(body)
        self.after_request()
        return httpx.Response(200, json=response_record(synthetic_answer(expected["packet"])))

    def batch(self, **kwargs):
        return LiveQualificationBatch(self.bank, self.settings, self.out,
            approved_config=kwargs.get("config", self.config), approval_path=self.approval_path,
            api_key=kwargs.get("key", self.key))

    def test_preflight_and_template_cannot_dispatch(self):
        result = preflight(self.bank, self.settings)
        self.assertEqual(result["items"], 72)
        self.assertLessEqual(result["max_padded_bytes"], 32768)
        template = approval_template(self.config)
        self.assertTrue(all(template[g] is False for g in GATES))
        self.assertIsNone(template["expires_at"])
        self.approval_path.write_bytes(wire(template))
        with self.assertRaises(ValueError):
            self.batch()
        self.assertFalse(self.out.exists())
        self.transport.assert_not_called()

    def test_each_unverified_gate_denies_before_collection_or_transport(self):
        for gate in GATES:
            with self.subTest(gate=gate):
                altered = {**self.approval, gate: False}
                self.approval_path.write_bytes(wire(altered))
                with self.assertRaises(ValueError):
                    self.batch()
        self.assertFalse(self.out.exists())
        self.transport.assert_not_called()

    def test_wrong_binding_expiry_and_missing_record_deny(self):
        for field, value in (("configuration_hash", "0" * 64), ("expires_at", "2000-01-01T00:00:00+00:00"),
                             ("expires_at", "2999-01-01T00:00:00"), ("approval_reference", "")):
            with self.subTest(field=field, value=value):
                self.approval_path.write_bytes(wire({**self.approval, field: value}))
                with self.assertRaises(ValueError):
                    self.batch()
        self.approval_path.unlink()
        with self.assertRaises(FileNotFoundError):
            self.batch()
        self.transport.assert_not_called()

    def test_changed_key_settings_destination_and_runtime_deny(self):
        with self.assertRaises(ValueError):
            self.batch(key="ANOTHER_FAKE_KEY")
        for field, value in (("output_path", str(self.root / "other")), ("runtime_hashes", {}),
                             ("scoring_procedure_sha256", "0" * 64),
                             ("settings", {**self.config["settings"], "model": "another-model"})):
            changed = deepcopy(self.config)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.batch(config=changed)
        self.transport.assert_not_called()

    def test_full_schedule_live_path_uses_only_mock_transport(self):
        batch = self.batch()
        summary = batch.run()
        self.assertEqual(summary["counts"], {"structurally_valid": 144})
        self.assertEqual(len(self.requests), 144)
        self.assertEqual(self.transport.call_count, 144)
        self.assertEqual(summary["charged_nusd"], 144 * 200)
        self.assertEqual(summary["held_nusd"], 0)
        self.assertFalse(summary["qualified"])
        self.assertEqual([r["id"] for r in summary["outcomes"]], [r["id"] for r in self.bank.schedule])
        for path in self.out.rglob("*.json"):
            self.assertNotIn(self.key, path.read_text(encoding="utf-8"))
        for path in self.out.glob("attempt-*/call-01-response.raw"):
            usage = strict_json(path.with_name("call-01-usage.json").read_bytes())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), usage["response_hash"])
        self.assertEqual(len(list(self.out.glob("attempt-*/call-01-response.raw"))), 144)
        commitment = commit_collection(self.out)
        record = self.out / "collection-freeze.json"
        self.assertEqual(hashlib.sha256(record.read_bytes()).hexdigest(), commitment)
        for name, expected_hash in strict_json(record.read_bytes())["files"].items():
            self.assertEqual(hashlib.sha256((self.out / name).read_bytes()).hexdigest(), expected_hash)
        with self.assertRaises(FileExistsError):
            commit_collection(self.out)
        with self.assertRaises(ValueError):
            batch.run()
        with self.assertRaises(FileExistsError):
            self.batch()

    def test_revocation_after_first_response_stops_before_next_reservation(self):
        self.after_request = lambda: self.approval_path.unlink()
        result = self.batch().run()
        self.assertEqual(result["stop"], "approval_or_configuration_changed")
        self.assertEqual(result["counts"], {"structurally_valid": 1, "not_run": 143})
        self.assertEqual(result["held_nusd"], 0)
        self.assertEqual(len(self.requests), 1)

    def test_expiry_after_first_response_stops(self):
        from live_qualification import datetime as original_datetime
        class Later:
            fromisoformat = original_datetime.fromisoformat
            @staticmethod
            def now(tz):
                return original_datetime.now(tz) + timedelta(hours=2)
        self.after_request = lambda: patch("live_qualification.datetime", Later).start()
        result = self.batch().run()
        self.assertEqual(result["stop"], "approval_or_configuration_changed")
        self.assertEqual(len(self.requests), 1)

    def test_operator_stop_after_first_response(self):
        self.after_request = lambda: (self.out / "STOP").write_text("Stop")
        result = self.batch().run()
        self.assertEqual(result["stop"], "operator_stop")
        self.assertEqual(len(self.requests), 1)

    def test_configuration_change_during_collection_stops(self):
        batch = self.batch()
        self.after_request = lambda: setattr(batch, "settings", replace(self.settings, reasoning_effort="low"))
        result = batch.run()
        self.assertEqual(result["stop"], "approval_or_configuration_changed")
        self.assertEqual(len(self.requests), 1)

    def test_shared_budget_denies_second_attempt(self):
        self.settings = replace(self.settings, budget_nusd=32768 + 8192 * 2 + 199)
        self.configure()
        result = self.batch().run()
        self.assertEqual(result["stop"], "budget_exhausted")
        self.assertEqual(len(self.requests), 1)

    def test_uncertain_usage_stops_without_retry(self):
        self.transport.side_effect = lambda **kwargs: httpx.MockTransport(
            lambda request: httpx.Response(200, json={"model": "fixture-model", "service_tier": "default"}))
        result = self.batch().run()
        self.assertEqual(result["stop"], "usage_uncertain")
        self.assertEqual(result["held_nusd"], 32768 + 8192 * 2)
        self.assertEqual(result["counts"], {"failed": 1, "not_run": 143})
        self.assertEqual(self.transport.call_count, 1)

    def test_preflight_rejects_oversized_request(self):
        with self.assertRaises(ValueError):
            preflight(self.bank, replace(self.settings, max_input_tokens=4096))
        self.transport.assert_not_called()

    def test_incomplete_collection_cannot_be_committed(self):
        batch = self.batch()
        with self.assertRaises(ValueError):
            commit_collection(batch.folder)
        self.transport.assert_not_called()


if __name__ == "__main__":
    unittest.main()
