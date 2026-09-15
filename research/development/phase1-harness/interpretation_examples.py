"""Public development examples. Expected decisions never enter model packets."""
import hashlib

from harness import CONTRACT, digest


def examples():
    rows = [
        ("partial_inputs", "Every supported input returns 1.", "The supplied observations for this version only.",
         "Supported inputs are exactly red and blue.\nObserved: red returns 1.\nBlue has not been tested; no implementation is supplied.\n",
         "unresolved", "Red alone cannot establish the result for blue. There is no observed contradiction."),
        ("complete_inputs", "Every supported input returns 1.", "The supplied observations for this version only.",
         "Supported inputs are exactly red and blue.\nObserved: red returns 1.\nObserved: blue returns 1.\n",
         "admit", "Both inputs in the complete supported set have the stated result."),
        ("wrong_setting", "The function preserves fragments in URLs.", "Default settings in this version.",
         "This version has two settings.\nDefault settings remove fragments from URLs.\nSetting keep_fragment=True preserves fragments in URLs.\n",
         "reject", "The default explicitly removes fragments. The special setting cannot rescue the claim."),
        ("matching_setting", "The function preserves fragments in URLs.", "With keep_fragment=True in this version.",
         "This version has two settings.\nDefault settings remove fragments from URLs.\nSetting keep_fragment=True preserves fragments in URLs.\n",
         "admit", "The stated setting explicitly preserves fragments."),
        ("ambiguous_wording", "The function normalises names.", "The supplied function only. Normalises has no further definition.",
         "For every text input, the function removes leading and trailing spaces.\nIt preserves the case of every letter.\nNo definition of normalisation is supplied.\n",
         "unresolved", "Normalisation might mean trimming or changing case; these readings yield different verdicts. Clarification is needed."),
        ("precise_wording", "For every text input, the function removes leading and trailing spaces.", "The supplied function only.",
         "For every text input, the function removes leading and trailing spaces.\nIt preserves the case of every letter.\nNo definition of normalisation is supplied.\n",
         "admit", "The explicit trimming claim matches the evidence without assuming a meaning for normalisation."),
    ]
    result = {}
    for name, claim, scope, text, verdict, reason in rows:
        sha = hashlib.sha256(text.encode()).hexdigest()
        source = {"revision": "artificial-interpretation-v1", "condition": "public_development",
                  "instruction_paths": [], "files": {"observations.txt": {"text": text, "sha256": sha}}}
        draft = {"claims": [{"id": "C1", "text": claim, "scope": scope,
            "kind": "observation", "provenance": "documentation_extraction", "exceptions": [],
            "evidence": [], "counter_evidence": []}]}
        result[name] = {"packet": {"role": "verifier", "contract": CONTRACT, "sources": source,
                                  "candidate": draft, "candidate_hash": digest(draft)},
                        "expected": verdict, "reason_requirement": reason}
    return result


def check_verdict(answer, example):
    """Only the verdict check. A human or recorded evidence review must check the reason."""
    from harness import validate_review
    packet = example["packet"]
    validate_review(answer, packet["candidate"], packet["sources"])
    return answer["decisions"][0]["verdict"] == example["expected"]
