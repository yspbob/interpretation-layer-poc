"""Identity enforcement and sensitivity of development scoring; no model calls."""
from copy import deepcopy
import unittest

from fixtures import review
from harness import digest, validate_review
from interpretation_examples import examples, check_verdict
from jsonschema import ValidationError


class InterpretationTests(unittest.TestCase):
    def setUp(self):
        self.examples = examples()
        self.packet = self.examples["matching_setting"]["packet"]
        self.draft = self.packet["candidate"]

    def test_expected_verdicts_and_every_wrong_alternative(self):
        for name, example in self.examples.items():
            for verdict in ("admit", "reject", "unresolved"):
                with self.subTest(name=name, verdict=verdict):
                    answer = review(example["packet"]["candidate"], verdict)
                    self.assertEqual(check_verdict(answer, example), verdict == example["expected"])

    def test_same_id_cannot_refer_to_changed_claim_scope_or_exceptions(self):
        answer = review(self.draft)
        for field, value in (("text", "A replacement claim"), ("scope", "Default settings"),
                             ("exceptions", ["Except some inputs"])):
            with self.subTest(field=field):
                changed = deepcopy(self.draft)
                changed["claims"][0][field] = value
                self.assertRaises(ValueError, validate_review, answer, changed, self.packet["sources"])

    def test_wrong_id_rejected_even_with_correct_version(self):
        answer = review(self.draft)
        answer["decisions"][0]["claim_id"] = "C2"
        self.assertRaises(ValueError, validate_review, answer, self.draft, self.packet["sources"])

    def test_scope_rewrite_field_is_not_accepted(self):
        answer = review(self.draft)
        answer["decisions"][0]["supported_scope"] = "Default settings"
        self.assertRaises(ValidationError, validate_review, answer, self.draft, self.packet["sources"])

    def test_correct_identity_does_not_make_misinterpretation_pass(self):
        example = self.examples["partial_inputs"]
        answer = review(example["packet"]["candidate"])
        answer["decisions"][0]["reason"] = "Red returns 1, so all inputs do."
        validate_review(answer, example["packet"]["candidate"], example["packet"]["sources"])
        self.assertFalse(check_verdict(answer, example))

    def test_neither_blanket_admission_nor_blanket_abstention_passes(self):
        for verdict in ("admit", "unresolved", "reject"):
            self.assertFalse(all(check_verdict(review(e["packet"]["candidate"], verdict), e)
                                 for e in self.examples.values()))

    def test_expected_answers_are_separate_from_packets(self):
        for example in self.examples.values():
            self.assertEqual(set(example["packet"]),
                             {"role", "contract", "sources", "candidate", "candidate_hash"})
            self.assertEqual(example["packet"]["candidate_hash"], digest(example["packet"]["candidate"]))


if __name__ == "__main__":
    unittest.main()
