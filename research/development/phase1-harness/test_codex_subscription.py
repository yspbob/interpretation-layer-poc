"""Artificial packets and collection failure tests; no provider calls."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
import time
from unittest.mock import patch

from harness import CONTRACT, digest, wire
from codex_subscription import audit_events, load_packet, run_packet, sha
from test_qualification_batch import synthetic_answer


def public_packet(role):
    text = "DEFAULT_TIMEOUT = 30\n"
    import hashlib
    evidence = [{"path": "widget.py", "sha256": hashlib.sha256(text.encode()).hexdigest(),
                 "start": 1, "end": 1, "supports": "The constant is assigned 30."}]
    sources = {"revision": "public-artificial-widget-1", "condition": "artificial",
               "instruction_paths": [], "files": {"widget.py": {"text": text, "sha256": evidence[0]["sha256"]}}}
    draft = {"claims": [{"id": "C1", "text": "DEFAULT_TIMEOUT is assigned 30.", "scope": "The supplied widget.py only",
        "kind": "observation", "provenance": "executable_text_restatement", "exceptions": [],
        "evidence": evidence, "counter_evidence": []}]}
    reference = {"units": [{"id": "U1", "requirement": "Identify the value assigned to DEFAULT_TIMEOUT in widget.py.", "evidence": evidence}]}
    review = {"action": "freeze", "decisions": [{"claim_id": "C1", "verdict": "admit", "reason": "Line 1 assigns 30.",
        "supported_scope": "The supplied widget.py only", "evidence": evidence, "contradictions": [], "missing_evidence": []}]}
    packet = {"role": role, "contract": CONTRACT, "sources": sources}
    if role == "verifier_assessor":
        packet.update(submission={"draft": draft, "review": review}, reference=reference)
        packet["review_hash"] = digest(packet["submission"])
    else:
        packet["candidate"] = draft
        if role == "guidance_assessor":
            packet.update(reference=reference, candidate_hash=digest(draft))
    return packet


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet = public_packet("guidance_assessor")

    def write_events(self, extra=None, answer=None):
        answer = answer or synthetic_answer(self.packet)
        events = [{"type": "thread.started", "thread_id": "artificial"}, {"type": "turn.started"},
                  {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(answer)}},
                  {"type": "turn.completed", "usage": {"input_tokens": 100, "output_tokens": 20}}]
        events += extra or []
        (self.root / "events.jsonl").write_text("\n".join(map(json.dumps, events)))
        (self.root / "last-answer.json").write_bytes(wire(answer))
        (self.root / "startup-ok").write_text("yes")
        (self.root / "stderr.txt").write_text("")
        return answer

    def test_three_role_loads_and_audits(self):
        for role in ("verifier", "guidance_assessor", "verifier_assessor"):
            self.packet = public_packet(role)
            p = self.root / "packet.json"; p.write_bytes(wire(self.packet))
            self.assertEqual(load_packet(p, sha(p)), self.packet)
            self.write_events()
            self.assertFalse(audit_events(self.root, self.packet, 0)["qualified"])

    def test_changed_packet_and_injected_answer_rejected(self):
        p = self.root / "packet.json"; p.write_bytes(wire(self.packet))
        with self.assertRaises(ValueError): load_packet(p, "0" * 64)
        self.packet["expected_answer"] = "admit"; p.write_bytes(wire(self.packet))
        with self.assertRaises(ValueError): load_packet(p, sha(p))

    def test_duplicate_json_rejected(self):
        p = self.root / "packet.json"; p.write_text('{"role":"verifier","role":"verifier"}')
        with self.assertRaises(ValueError): load_packet(p, sha(p))

    def test_wrong_identity_rejected(self):
        answer = synthetic_answer(self.packet); answer["candidate_hash"] = "0" * 64
        self.write_events(answer=answer)
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_extra_answer_preserves_first_and_fails(self):
        first = self.write_events([{"type": "item.completed", "item": {"type": "agent_message", "text": "{}"}}])
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)
        self.assertEqual(json.loads((self.root / "first-answer.txt").read_text()), first)

    def test_extra_turn_rejected(self):
        self.write_events([{"type": "turn.started"}])
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_tool_attempt_rejected(self):
        self.write_events(); (self.root / "tool-attempt.json").write_text("{}")
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_unreviewed_error_rejected(self):
        self.write_events([{"type": "item.completed", "item": {"type": "error", "message": "hook failed"}}])
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_missing_startup_rejected(self):
        self.write_events(); (self.root / "startup-ok").unlink()
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_failed_client_preserves_first(self):
        self.write_events()
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 1)
        self.assertTrue((self.root / "first-answer.txt").exists())

    def test_last_answer_changed_rejected(self):
        self.write_events(); (self.root / "last-answer.json").write_text("{}")
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_unreviewed_diagnostic_rejected(self):
        self.write_events(); (self.root / "stderr.txt").write_text("Hook failed")
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_tool_event_rejected_without_hook_marker(self):
        self.write_events([{"type": "item.completed", "item": {"type": "command_execution"}}])
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)

    def test_source_bytes_checked_against_citation_hash(self):
        self.packet["sources"]["files"]["widget.py"]["text"] = "changed"
        p = self.root / "packet.json"; p.write_bytes(wire(self.packet))
        with self.assertRaises(ValueError): load_packet(p, sha(p))

    def test_stop_present_when_finished_answer_is_audited(self):
        self.write_events(); (self.root / "STOP").write_text("Stop")
        with self.assertRaises(ValueError): audit_events(self.root, self.packet, 0)
        self.assertTrue((self.root / "first-answer.txt").exists())

    def test_account_gates_prevent_launch(self):
        p = self.root / "packet.json"; p.write_bytes(wire(self.packet))
        auth = self.root / "auth.json"
        auth.write_text('{"auth_mode":"chatgpt","tokens":{"account_id":"artificial"}}')
        good = {"observed_at": time.time(), "public_probe_only": True, "ordinary_usage_allowed": True,
                "remaining_percent": 50, "credits_balance": "0", "has_credits": False, "account_id": "artificial"}
        bad = [{"observed_at": time.time() - 121}, {"has_credits": True}, {"credits_balance": "10"},
               {"remaining_percent": 0}, {"account_id": "wrong"}, {"public_probe_only": False}]
        with patch("codex_subscription.CLIENT_HASH", sha(p)), patch("subprocess.Popen") as launch:
            for changes in bad:
                with self.subTest(changes=changes), self.assertRaises(ValueError):
                    run_packet(p, sha(p), self.root / "run", p, p, auth_path=auth, account_observation={**good, **changes})
            launch.assert_not_called()
        self.assertFalse((self.root / "run").exists())


if __name__ == "__main__":
    unittest.main()
