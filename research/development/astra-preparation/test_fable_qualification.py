"""Synthetic checks of private desktop packaging; no live calls or hidden labels."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from prepare_fable_qualification import ROOT, WRAPPER, parse, prepare, render
from qualification_batch import load_bank, validate_answer
from harness import digest
from provider import strict_json
from test_qualification_batch import synthetic_bank, synthetic_answer


class DesktopPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sha = synthetic_bank(self.root / "bank")
        self.bank = load_bank(self.root / "bank", "freeze.json", self.sha)
        self.addCleanup(patch.stopall)
        patch("socket.socket.connect", side_effect=AssertionError("No network permitted")).start()
        self.item = deepcopy(next(i for i in self.bank.items.values() if i["role"] == "guidance_assessor"))

    def test_complete_schedule_and_exact_allowed_content(self):
        result = prepare(self.bank, self.root / "out")
        rows = strict_json((self.root / "out/schedule.json").read_bytes())
        self.assertEqual(result["scheduled_responses"], 48)
        expected = [r for r in self.bank.schedule if r["role"] == "guidance_assessor"]
        self.assertEqual([r["id"] for r in rows], [r["id"] for r in expected])
        for row in rows:
            raw = (self.root / "out" / row["input_path"]).read_bytes()
            item = self.bank.items[row["item_id"]]
            self.assertEqual(parse(raw)["packet"], item["packet"])
            self.assertNotIn(b"SEALED_ANSWER_NEVER_READ", raw)
            self.assertNotIn(row["item_id"].encode(), raw)
            validate_answer(synthetic_answer(parse(raw)["packet"]), item["packet"])
        self.assertEqual((self.root / "out/wrapper.txt").read_text(), WRAPPER)

    def test_existing_output_preserved(self):
        prepare(self.bank, self.root / "out")
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare(self.bank, self.root / "out")

    def test_public_output_denied(self):
        with self.assertRaisesRegex(ValueError, "public checkout"):
            prepare(self.bank, ROOT / "local-runs/forbidden-private-output")

    def test_bank_mutation_and_freeze_tampering_denied(self):
        self.bank.schedule.pop()
        with self.assertRaisesRegex(ValueError, "changed after loading"):
            prepare(self.bank, self.root / "out")
        (self.root / "bank/freeze.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Freeze mismatch"):
            load_bank(self.root / "bank", "freeze.json", self.sha)

    def test_extra_answer_field_and_changed_identity_denied(self):
        self.item["packet"]["expected_answer"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "Unexpected input"):
            render(self.item)
        del self.item["packet"]["expected_answer"]
        self.item["packet"]["candidate_hash"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Changed candidate"):
            render(self.item)

    def test_oversized_input_denied_without_truncation(self):
        self.item["packet"]["candidate"]["claims"][0]["text"] = "x" * 40000
        self.item["packet"]["candidate_hash"] = digest(self.item["packet"]["candidate"])
        with self.assertRaisesRegex(ValueError, "byte envelope"):
            render(self.item)

    def test_capture_validator_rejects_missing_duplicate_and_wrong_identity(self):
        packet = self.item["packet"]
        for change in (lambda a: a.update(candidate_hash="0"*64),
                       lambda a: a["coverage"].clear(),
                       lambda a: a["claims"].append(deepcopy(a["claims"][0]))):
            answer = synthetic_answer(packet)
            change(answer)
            with self.assertRaises(ValueError):
                validate_answer(answer, packet)


if __name__ == "__main__":
    unittest.main()
