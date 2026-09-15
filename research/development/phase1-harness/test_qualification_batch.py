"""Public synthetic fixtures only. All SDK traffic is local and sockets are denied."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from harness import CONTRACT, digest, wire
from provider import PROMPTS, SCHEMAS, Settings, httpx, strict_json
from qualification_batch import QualificationBatch, load_bank
from test_provider import response_record


def synthetic_bank(root):
    """Four artificial families exercising the bank format, not qualification answers."""
    root.mkdir()
    files, schedule = {}, []

    def save(name, value):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = wire(value)
        path.write_bytes(raw)
        files[name] = hashlib.sha256(raw).hexdigest()

    for number in range(4):
        case = f"S{number}"
        text = f"Synthetic source {number}: a named value exists.\n"
        sha = hashlib.sha256(text.encode()).hexdigest()
        evidence = [{"path": "source.txt", "sha256": sha, "start": 1, "end": 1, "supports": "Synthetic evidence"}]
        sources = {"revision": f"synthetic-{number}", "condition": "synthetic",
                   "instruction_paths": [], "files": {"source.txt": {"text": text, "sha256": sha}}}
        reference = {"units": [{"id": "U1", "requirement": "ASSESSOR_REFERENCE_ONLY", "evidence": evidence}]}
        candidate = {"claims": [{"id": "C1", "text": "A named value exists.", "scope": "Synthetic source only",
            "kind": "observation", "provenance": "executable_text_restatement", "exceptions": [],
            "evidence": evidence, "counter_evidence": []}]}
        review = {"candidate_hash": digest(candidate), "action": "freeze", "decisions": [{"claim_id": "C1", "verdict": "admit",
            "reason": "Synthetic review", "evidence": evidence,
            "contradictions": [], "missing_evidence": []}]}
        items = []
        for role in ("verifier", "guidance_assessor", "verifier_assessor"):
            for n in range(6):
                packet = {"role": role, "contract": CONTRACT, "sources": sources}
                if role == "verifier_assessor":
                    packet.update(submission={"draft": candidate, "review": review}, reference=reference)
                    packet["review_hash"] = digest(packet["submission"])
                else:
                    packet["candidate"] = candidate
                    packet["candidate_hash"] = digest(candidate)
                    if role == "guidance_assessor":
                        packet.update(candidate_hash=digest(candidate), reference=reference)
                identifier = f"{case}_{role}_{n}"
                items.append({"id": identifier, "role": role, "packet": deepcopy(packet),
                              "instruction": PROMPTS[role], "response_schema": SCHEMAS[role]})
                for rep in (1, 2):
                    schedule.append({"id": identifier + f"_R{rep}", "item_id": identifier,
                                     "role": role, "case": case, "repetition": rep})
        prefix = f"prepared/{case}"
        for name, value in (("sources.json", sources), ("reference.json", reference), ("items.json", items),
                            ("role-prompts.json", {r: PROMPTS[r] for r in ("verifier", "guidance_assessor", "verifier_assessor")})):
            save(prefix + "/" + name, value)
        # Deliberately not valid JSON. Loading these files would make the test fail.
        (root / prefix / "scoring-key.json").write_text("SEALED_ANSWER_NEVER_READ")
    save("prepared/schedule.json", schedule)
    manifest = {"active_bank": "prepared", "files": files}
    raw = wire(manifest)
    (root / "freeze.json").write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def synthetic_answer(packet):
    role = packet["role"]
    draft = packet["submission"]["draft"] if role == "verifier_assessor" else packet["candidate"]
    reason = "Synthetic transport response; no claim of semantic correctness."
    if role == "verifier":
        return {"candidate_hash": digest(draft), "action": "stop_unresolved", "decisions": [{"claim_id": c["id"], "verdict": "unresolved",
            "reason": reason, "evidence": [],
            "contradictions": [], "missing_evidence": []} for c in draft["claims"]]}
    if role == "guidance_assessor":
        return {"candidate_hash": packet["candidate_hash"],
                "claims": [{"claim_id": c["id"], "verdict": "unresolved", "reason": reason} for c in draft["claims"]],
                "coverage": [{"unit_id": u["id"], "verdict": "unresolved", "reason": reason} for u in packet["reference"]["units"]]}
    return {"review_hash": packet["review_hash"], "decisions": [
        {"claim_id": c["id"], "expected": "unresolved", "reason": reason} for c in draft["claims"]]}


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.freeze_hash = synthetic_bank(self.root / "bank")
        self.settings = Settings("fixture-model", "low", 32768, 8192, 1, 2, 20_000_000, 12)
        self.addCleanup(patch.stopall)
        patch("socket.socket.connect", side_effect=AssertionError("Network forbidden")).start()
        patch("provider.httpx.HTTPTransport", side_effect=AssertionError("Live transport forbidden")).start()
        self.requests = []

    def load(self):
        return load_bank(self.root / "bank", "freeze.json", self.freeze_hash)

    def handler(self, request):
        body = strict_json(request.content)
        self.requests.append(body)
        packet = strict_json(body["input"][0]["content"])
        return httpx.Response(200, json=response_record(synthetic_answer(packet)))

    def batch(self, handler=None, settings=None):
        return QualificationBatch(self.load(), settings or self.settings, self.root / "run",
                                  mock_handler=handler if handler is not None else self.handler)

    def alter_frozen(self, name, mutate):
        """Recommit a synthetic bad input to distinguish integrity from contract checks."""
        root = self.root / "bank"
        path = root / name
        path.write_bytes(wire(mutate(strict_json(path.read_bytes()))))
        manifest = strict_json((root / "freeze.json").read_bytes())
        manifest["files"][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        (root / "freeze.json").write_bytes(wire(manifest))
        self.freeze_hash = hashlib.sha256((root / "freeze.json").read_bytes()).hexdigest()

    def test_full_schedule_fresh_contexts_shared_ledger_no_keys_or_semantic_pass(self):
        batch = self.batch()
        summary = batch.run()
        self.assertEqual(summary["counts"], {"structurally_valid": 144})
        self.assertEqual(summary["charged_nusd"], 144 * 200)
        self.assertEqual(summary["held_nusd"], 0)
        self.assertFalse(summary["qualified"])
        self.assertEqual(summary["model_calls"], 0)
        self.assertEqual([r["id"] for r in summary["outcomes"]], [r["id"] for r in batch.bank.schedule])
        for body in self.requests:
            self.assertEqual(len(body["input"]), 1)
            self.assertEqual(body["tools"], [])
            self.assertFalse(body["store"])
            self.assertNotIn("previous_response_id", body)
            self.assertNotIn("conversation", body)
            self.assertNotIn("SEALED_ANSWER_NEVER_READ", wire(body).decode())
            p = strict_json(body["input"][0]["content"])
            self.assertEqual("reference" in p, p["role"] != "verifier")
            if p["role"] == "verifier":
                self.assertNotIn("ASSESSOR_REFERENCE_ONLY", wire(body).decode())
        previous = None
        for path in sorted((self.root / "run").glob("event-*.json")):
            event = strict_json(path.read_bytes())
            self.assertEqual(event["previous"], previous)
            previous = event.pop("hash")
            self.assertEqual(digest(event), previous)
        self.assertEqual(len(list((self.root / "run").glob("attempt-*"))), 144)

    def test_budget_reserves_next_full_call_across_attempts(self):
        reserve = 32768 + 8192 * 2
        summary = self.batch(settings=replace(self.settings, budget_nusd=reserve + 199)).run()
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(summary["stop"], "budget_exhausted")
        self.assertEqual(summary["counts"], {"structurally_valid": 1, "not_run": 143})
        self.assertEqual(summary["charged_nusd"], 200)

    def test_budget_too_small_has_no_dispatch(self):
        summary = self.batch(settings=replace(self.settings, budget_nusd=1)).run()
        self.assertFalse(self.requests)
        self.assertEqual(summary["counts"], {"not_run": 144})

    def test_timeout_retains_reserve_stops_and_does_not_retry(self):
        def timeout(request):
            self.requests.append(request)
            raise httpx.ReadTimeout("PRIVATE_TOKEN_MUST_NOT_ENTER_ERRORS")
        b = self.batch(handler=timeout)
        summary = b.run()
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(summary["held_nusd"], b.reserve)
        self.assertEqual(summary["counts"], {"failed": 1, "not_run": 143})
        self.assertEqual(summary["stop"], "usage_uncertain")
        self.assertNotIn("PRIVATE_TOKEN_MUST_NOT_ENTER_ERRORS", wire(summary).decode())

    def test_usage_missing_or_over_bound_stops(self):
        for problem in (None, {"input_tokens": 32769, "output_tokens": 0, "total_tokens": 32769}):
            with self.subTest(problem=problem):
                def handler(request):
                    packet = strict_json(strict_json(request.content)["input"][0]["content"])
                    return httpx.Response(200, json=response_record(synthetic_answer(packet), usage=problem))
                b = QualificationBatch(self.load(), self.settings, self.root / f"usage-{problem is None}", mock_handler=handler)
                summary = b.run()
                self.assertEqual(summary["held_nusd"], b.reserve)
                self.assertEqual(summary["stop"], "usage_uncertain")

    def test_known_usage_malformed_answer_is_charged_and_not_retried(self):
        def handler(request):
            if not self.requests:
                self.requests.append(strict_json(request.content))
                data = response_record({})
                data["output"][0]["content"][0]["text"] = '{"bad":'
                return httpx.Response(200, json=data)
            return self.handler(request)
        summary = self.batch(handler=handler).run()
        self.assertEqual(len(self.requests), 144)
        self.assertEqual(summary["counts"], {"failed": 1, "structurally_valid": 143})
        self.assertEqual(summary["charged_nusd"], 144 * 200)
        self.assertEqual(summary["held_nusd"], 0)
        self.assertEqual(summary["outcomes"][0]["status"], "failed")

    def test_wrong_output_identity_and_duplicate_claims_fail_after_billing(self):
        def handler(request):
            body = strict_json(request.content)
            packet = strict_json(body["input"][0]["content"])
            answer = synthetic_answer(packet)
            if packet["role"] == "guidance_assessor":
                answer["candidate_hash"] = "0" * 64
            elif packet["role"] == "verifier_assessor":
                answer["decisions"] *= 2
            else:
                answer["decisions"][0].update(verdict="admit", supported_scope="Changed scope")
            return httpx.Response(200, json=response_record(answer))
        summary = self.batch(handler=handler).run()
        self.assertEqual(summary["counts"], {"failed": 144})
        self.assertEqual(summary["charged_nusd"], 144 * 200)

    def test_existing_folder_and_second_run_denied(self):
        b = self.batch(settings=replace(self.settings, budget_nusd=1))
        b.run()
        self.assertRaises(ValueError, b.run)
        self.assertRaises(FileExistsError, self.batch)

    def test_interrupt_records_unknown_attempt_and_remaining_schedule(self):
        def handler(request):
            raise KeyboardInterrupt()
        b = self.batch(handler=handler)
        self.assertRaises(KeyboardInterrupt, b.run)
        summary = strict_json((self.root / "run/summary.json").read_bytes())
        self.assertEqual(summary["stop"], "interrupted")
        self.assertEqual(summary["held_nusd"], b.reserve)
        self.assertEqual(summary["counts"], {"failed": 1, "not_run": 143})

    def test_reservation_is_durable_before_dispatch(self):
        checked = []
        def handler(request):
            event = strict_json((self.root / "run/event-0000.json").read_bytes())
            self.assertEqual(event["kind"], "reserved")
            self.assertGreater(event["held_nusd"], 0)
            self.assertTrue((self.root / "run/attempt-001/call-01-reservation.json").exists())
            checked.append(True)
            raise httpx.ReadTimeout("Stop after checking reservation")
        self.batch(handler=handler).run()
        self.assertEqual(checked, [True])

    def test_reservation_write_failure_prevents_dispatch(self):
        b = self.batch()
        with patch.object(b, "save", side_effect=OSError("disk unavailable")):
            self.assertRaises(OSError, b.run)
        self.assertFalse(self.requests)
        self.assertRaises(ValueError, b.run)

    def test_concurrent_run_denied(self):
        b = self.batch()
        with b.lock:
            self.assertRaises(ValueError, b.run)
        self.assertFalse(self.requests)

    def test_mutated_loaded_bank_denied(self):
        bank = self.load()
        bank.schedule.reverse()
        self.assertRaises(ValueError, QualificationBatch, bank, self.settings, self.root / "run", mock_handler=self.handler)

    def test_changed_frozen_input_and_wrong_freeze_denied(self):
        self.assertRaises(ValueError, load_bank, self.root / "bank", "freeze.json", "0" * 64)
        (self.root / "bank/prepared/schedule.json").write_text("[]")
        self.assertRaises(ValueError, self.load)

    def test_duplicate_schedule_repetition_denied(self):
        self.alter_frozen("prepared/schedule.json", lambda x: [x[0], *x[0:143]])
        self.assertRaises(ValueError, self.load)

    def test_reference_in_verifier_pack_denied(self):
        def change(items):
            items[0]["packet"]["reference"] = {"units": []}
            return items
        self.alter_frozen("prepared/S0/items.json", change)
        self.assertRaises(ValueError, self.load)

    def test_extra_packet_fields_denied_before_dispatch(self):
        def change(items):
            items[0]["packet"]["history"] = "FORBIDDEN_HISTORY"
            return items
        self.alter_frozen("prepared/S0/items.json", change)
        self.assertRaises(ValueError, self.batch)
        self.assertFalse(self.requests)

    def test_input_over_bound_denied_before_dispatch(self):
        self.assertRaises(ValueError, self.batch, settings=replace(self.settings, max_input_tokens=1))
        self.assertFalse(self.requests)

    def test_manifest_path_traversal_denied(self):
        root = self.root / "bank"
        m = strict_json((root / "freeze.json").read_bytes())
        m["active_bank"] = "../outside"
        (root / "freeze.json").write_bytes(wire(m))
        self.freeze_hash = hashlib.sha256((root / "freeze.json").read_bytes()).hexdigest()
        self.assertRaises(ValueError, self.load)

    def test_falsey_handler_cannot_select_live_transport(self):
        outer = self
        class Handler:
            def __bool__(self): return False
            def __call__(self, request): return outer.handler(request)
        b = self.batch(handler=Handler(), settings=replace(self.settings, budget_nusd=49152))
        summary = b.run()
        self.assertEqual(summary["counts"], {"structurally_valid": 1, "not_run": 143})


if __name__ == "__main__":
    unittest.main()
