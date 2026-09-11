"""Authored example answers and assessments. These scripts are NOT AI judgements."""
from copy import deepcopy


def reference_at(sources, path, needle, supports):
    item = sources["files"][path]
    start = next(i for i, line in enumerate(item["text"].splitlines(), 1) if needle in line)
    return {"path": path, "sha256": item["sha256"], "start": start, "end": min(start + 20, len(item["text"].splitlines())),
            "supports": supports}


def claims_for(sources, reference):
    if reference["case_id"] == "NB_BULK_01":
        refs = [reference_at(sources, *args) for args in [
            ("docs/integrations/rest-api.md", "bulk update of objects is an all-or-none", "The documented batch guarantee"),
            ("netbox/netbox/context_managers.py", "if events :=", "Queued events are processed after the request"),
            ("netbox/core/signals.py", "Delete any queued events", "Existing cleanup for an aborted transaction"),
            ("netbox/netbox/api/viewsets/mixins.py", "def perform_bulk_update", "The earlier API batch path; inspect the whole function for rollback and missing cleanup"),
        ]]
        texts = [
            "If a synchronous batch update fails, none of its database edits should remain. A successful batch keeps its edits.",
            "Saving can queue an event in memory. The request processor later flushes that queue. Rolling back database writes does not undo that separate queue.",
            "Discard events for an aborted batch before dispatch, while preserving events for successful committed changes. Existing UI cleanup supports this obligation.",
            "The earlier API implementation can violate the supported event rule. Its current behaviour is evidence to explain, not automatic authority for a rule. This guide has not received owner approval.",
        ]
        exceptions = ["Successful batches retain changes.", "Events depend on supported object types and configuration.",
                      "Do not discard unrelated events or prescribe every nested savepoint policy.",
                      "Concurrent requests, actual delivery and owner intention remain outside the evidence."]
    else:
        ref = reference_at(sources, "httpx/_auth.py", "class Auth:", "Authentication adapter structure")
        refs = [ref] * len(reference["units"])
        texts = [u["requirement"] for u in reference["units"]]
        exceptions = ["Respect the alternatives and limits stated in the claim."] * len(texts)
    result = {"claims": [dict(id=f"C{i+1}", text=text, kind="recommendation",
                            scope="Supplied version and the declared development family only",
                            exceptions=[exceptions[i]],
                            provenance="documentation_extraction" if i == 0 else "structural_inference",
                            evidence=[refs[i]], counter_evidence=[])
                       for i, text in enumerate(texts)]}
    if reference["case_id"] == "NB_BULK_01":
        for claim in result["claims"][1:]:
            claim["evidence"] = list(refs) + [reference_at(sources, "netbox/core/signals.py", "queue = events_queue.get()", "Saving modifies a separate context queue")]
    else:
        for claim in result["claims"]:
            claim["provenance"] = "structural_inference" if claim["id"] == "C6" else "documentation_extraction"
            claim["evidence"] = [dict(ref, start=23, end=116), reference_at(sources, "docs/advanced/authentication.md", "If you _do_ need", "Mode specific adapters and the documented unsupported mode alternative")]
            claim["evidence"][1]["end"] = len(sources["files"]["docs/advanced/authentication.md"]["text"].splitlines())
    return result


def review(draft, verdict="admit", action="freeze", overrides=None):
    overrides = overrides or {}
    return {"action": action, "decisions": [dict(claim_id=c["id"], verdict=overrides.get(c["id"], verdict),
             reason="Authored development decision; not a semantic model judgement.",
             supported_scope=c["scope"], evidence=c["evidence"], contradictions=[], missing_evidence=[])
             for c in draft["claims"]]}


def assessment(draft, reference, bad_ids=(), missing_ids=()):
    return {"candidate_hash": "0" * 64,
            "claims": [dict(claim_id=c["id"], verdict="unsupported" if c["id"] in bad_ids else "supported",
                            reason="Authored assessment: the deliberately false rollback statement is unsupported; the other scoped claims are retained.")
                       for c in draft["claims"]],
            "coverage": [dict(unit_id=u["id"], verdict="missing" if u["id"] in missing_ids else "covered",
                              reason="Authored coverage for this particular submitted guide.") for u in reference["units"]]}


def verifier_assessment(draft, overrides=None):
    overrides = overrides or {}
    return {"review_hash": "0" * 64, "decisions": [dict(claim_id=c["id"], expected=overrides.get(c["id"], "admit"),
            reason="Authored independently of the replayed verifier decision.") for c in draft["claims"]]}


def scenarios(sources, reference):
    good = claims_for(sources, reference)
    bad = deepcopy(good)
    bad["claims"][0]["text"] = "Database rollback always clears all notifications automatically."
    empty = {"claims": []}
    partial = {"claims": good["claims"][1:]}
    unit1 = reference["units"][0]["id"]
    all_units = [u["id"] for u in reference["units"]]
    rejection = {"C1": "reject"}
    good_score = assessment(good, reference)
    bad_score = assessment(bad, reference, ["C1"], [unit1])
    empty_score = assessment(empty, reference, missing_ids=all_units)

    def case(drafts, reviews, original, released, judgments):
        return drafts, reviews, {"original": original, "released": released, "reviews": judgments}

    return {
        "supported": case([good], [review(good)], good_score, good_score, [verifier_assessment(good)]),
        "bad_admission": case([bad], [review(bad)], bad_score, bad_score, [verifier_assessment(bad, rejection)]),
        "false_rejection": case([good], [review(good, "reject")], good_score, empty_score, [verifier_assessment(good)]),
        "empty": case([empty], [review(empty)], empty_score, empty_score, [verifier_assessment(empty)]),
        "corrected": case([bad, good], [review(bad, action="revise", overrides=rejection), review(good)],
                          bad_score, good_score, [verifier_assessment(bad, rejection), verifier_assessment(good)]),
        "exhausted": case([bad] * 3, [review(bad, action="revise", overrides=rejection)] * 3,
                          bad_score, assessment(partial, reference, missing_ids=[unit1]),
                          [verifier_assessment(bad, rejection)] * 3),
        "unresolved": case([good], [review(good, "unresolved", "stop_unresolved")],
                           good_score, empty_score, [verifier_assessment(good)]),
    }
