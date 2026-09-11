"""Controller tests use authored records, never pretend to test AI judgement."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from fixtures import assessment, review, verifier_assessment
from harness import Controller, digest, source_pack, validate_draft, validate_review


class Replay:
    mode = "scripted-development"

    def __init__(self, change=None):
        self.messages = []
        self.change = change

    def call(self, message):
        self.messages.append(deepcopy(message))
        output = {"response": deepcopy(message["response"]), "reads": []}
        return self.change(message, output) if self.change else output


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "source.txt").write_bytes(b"A supported scoped rule.\n")
        self.sha = hashlib.sha256((self.root / "source.txt").read_bytes()).hexdigest()
        self.sources = source_pack(self.root, {"source.txt": self.sha}, "pinned", [])
        self.reference = {"units": [{"id": "U1", "requirement": "A scoped rule"}]}
        self.draft = {"claims": [{"id": "C1", "text": "A supported scoped rule", "kind": "constraint",
            "scope": "This case", "exceptions": [], "provenance": "documentation_extraction",
            "evidence": [{"path": "source.txt", "sha256": self.sha, "start": 1, "end": 1, "supports": "Rule"}],
            "counter_evidence": []}]}

    def run_case(self, drafts=None, reviews=None, scores=None, transport=None, **limits):
        drafts = [self.draft] if drafts is None else drafts
        reviews = [review(drafts[-1])] if reviews is None else reviews
        scores = scores or {"original": assessment(drafts[0], self.reference),
                           "released": assessment(drafts[-1], self.reference),
                           "reviews": [verifier_assessment(d) for d in drafts]}
        self.transport = transport or Replay()
        self.controller = Controller(self.sources, self.reference, self.transport, self.root / "run", **limits)
        return self.controller.run(drafts, reviews, scores)

    def test_freeze_precedes_assessment_and_sources_match(self):
        result = self.run_case()
        self.assertEqual(result["scores"]["released"]["verdict"], "pass")
        self.assertEqual(result["guide_hash"], digest(self.draft))
        self.assertEqual([m["packet"]["role"] for m in self.transport.messages],
                         ["drafter", "verifier", "guidance_assessor", "guidance_assessor", "verifier_assessor"])
        for message in self.transport.messages:
            self.assertEqual(message["packet"]["sources"], self.sources)
            if message["packet"]["role"] in {"drafter", "verifier"}:
                self.assertNotIn("reference", message["packet"])
        kinds = [e["kind"] for e in self.controller.events]
        self.assertLess(kinds.index("frozen"), len(kinds)-4)
        self.assertRaises(ValueError, self.controller.run, [], [], {})

    def test_empty_guide_has_missing_coverage(self):
        empty = {"claims": []}
        score = assessment(empty, self.reference, missing_ids=["U1"])
        result = self.run_case([empty], scores={"original": score, "released": score, "reviews": [verifier_assessment(empty)]})
        self.assertEqual(result["claim_count"], 0)
        self.assertEqual(result["scores"]["released"]["missing_units"], 1)

    def test_assessment_cannot_repair_wrong_admission(self):
        score = assessment(self.draft, self.reference, bad_ids=["C1"])
        result = self.run_case(scores={"original": score, "released": score,
                                     "reviews": [verifier_assessment(self.draft, {"C1": "reject"})]})
        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(result["scores"]["released"]["verdict"], "fail")
        self.assertEqual(len(result["verifier_errors"]), 1)
        self.assertEqual(result["guide_hash"], digest(self.draft))

    def test_two_corrections_then_freeze(self):
        result = self.run_case([self.draft]*3, [review(self.draft, action="revise")]*3)
        self.assertEqual(result["status"], "revision_exhausted")
        self.assertEqual(result["invocations"], 11)
        drafters = [m["packet"] for m in self.transport.messages if m["packet"]["role"] == "drafter"]
        self.assertEqual(len(drafters), 3)
        self.assertEqual(set(drafters[1]), {"role", "contract", "sources", "previous_draft", "feedback"})

    def test_call_budget_stops_and_retains_records(self):
        result = self.run_case(max_calls=1)
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["invocations"], 1)
        self.assertTrue((self.root / "run/invocation-01-output.json").exists())
        self.assertTrue((self.root / "run/result.json").exists())

    def test_timeout_is_infrastructure_failure(self):
        def timeout(message, output):
            raise subprocess.TimeoutExpired("worker", 1)
        result = self.run_case(transport=Replay(timeout))
        self.assertEqual(result["failure_class"], "infrastructure")
        self.assertEqual(self.controller.events[-2]["kind"], "invocation_failed")

    def test_output_limit_stops(self):
        result = self.run_case(transport=Replay(lambda m, o: {"response": "x"*128001}))
        self.assertEqual(result["status"], "stopped")
        self.assertIn("output byte limit", result["reason"])

    def test_candidate_hash_tampering_rejected(self):
        def change(message, output):
            if message["packet"]["role"] == "guidance_assessor":
                output["response"]["candidate_hash"] = "0"*64
            return output
        result = self.run_case(transport=Replay(change))
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["preparation_status"], "frozen")
        self.assertTrue((self.root / "run/frozen-guide.json").exists())

    def test_missing_coverage_rejected(self):
        def change(message, output):
            if message["packet"]["role"] == "guidance_assessor":
                output["response"]["coverage"] = []
            return output
        self.assertEqual(self.run_case(transport=Replay(change))["status"], "stopped")

    def test_invalid_citations_and_duplicate_claims(self):
        for field, value in [("path", "../reference.json"), ("sha256", "0"*64), ("end", 2)]:
            with self.subTest(field=field):
                draft = deepcopy(self.draft)
                draft["claims"][0]["evidence"][0][field] = value
                self.assertRaises(ValueError, validate_draft, draft, self.sources)
        draft = deepcopy(self.draft)
        draft["claims"] *= 2
        self.assertRaises(ValueError, validate_draft, draft, self.sources)

    def test_verifier_cannot_add_or_omit_claim(self):
        verdict = review(self.draft)
        verdict["decisions"][0]["claim_id"] = "Invented"
        self.assertRaises(ValueError, validate_review, verdict, self.draft, self.sources)
        self.assertRaises(ValueError, validate_review, review({"claims": []}), self.draft, self.sources)

    def test_source_tampering_traversal_and_missing_instructions(self):
        for allowed, instructions in [({"source.txt": "0"*64}, []), ({"../source.txt": self.sha}, []),
                                      ({"source.txt": self.sha}, ["AGENTS.md"])]:
            with self.subTest(allowed=allowed):
                self.assertRaises(ValueError, source_pack, self.root, allowed, "pin", instructions)

    def test_live_gateway_and_resume_denied(self):
        transport = Replay()
        transport.mode = "live"
        self.assertRaises(ValueError, Controller, self.sources, self.reference, transport, self.root / "live")
        self.run_case()
        self.assertRaises(FileExistsError, Controller, self.sources, self.reference, Replay(), self.root / "run")

    def test_reference_not_sent_through_working_role(self):
        controller = Controller(self.sources, self.reference, Replay(), self.root / "deny")
        self.assertRaises(ValueError, controller.invoke, "drafter", {"reference": self.reference}, self.draft)

    def test_narrowed_admission_requires_redraft(self):
        verdict = review(self.draft)
        verdict["decisions"][0]["supported_scope"] = "A different scope"
        self.assertRaises(ValueError, validate_review, verdict, self.draft, self.sources)


if __name__ == "__main__":
    unittest.main(verbosity=2)
