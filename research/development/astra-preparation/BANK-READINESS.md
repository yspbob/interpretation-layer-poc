# Four qualification cases prepared

The private qualification bank is prepared and checked. It contains four distinct families, with six items for each of three assessment roles in every family. That is 72 distinct role items and 144 planned calls after two repetitions. No qualification calls have run, and no assessor is qualified.

## Evidence checks

Across the four families, 42 authored behavioural scenarios passed and the checks detected 13 deliberate faults. Fourteen relevant upstream test invocations passed. Three additional upstream methods passed with a local fixture; those are recorded separately because the full upstream suite was not run for that case.

The source records preserve exact revisions, file hashes, excerpt locations and counterevidence. All 72 role items passed source, citation, schema and input separation checks. The scoring keys stay outside the model requests. The verifier does not receive the assessment reference. The role prompts were unchanged.

The largest encoded request plus the existing development padding is 32,441, within the proposed allowance of 32,768. This is a development check, not verification of actual provider token accounting.

## Gaps found through evidence

The user requested rigorous checks and asked that reported gaps be supported by facts. The review found and addressed these discrepancies:

1. **Some candidates gave away their intended assessment.** Their metadata called unsupported assertions unresolved or said approval evidence was absent. The final candidates remove those clues. The original versions remain preserved. Q01's expected verdicts did not change.
2. **One rule omitted a failure path.** The source described an exception to its asserted outcome. A targeted runtime check reproduced that exception, and a deliberate fault showed that the check could detect mishandling it. The rule and its valid alternative now preserve that distinction.
3. **The repeat check could penalise two legitimate answers.** Some items allow either rejection or an unresolved verdict. A calculation using the actual keys showed that permitted labels could yield only 16, 20 and 16 identical pairs across the three roles, below the proposed minimum of 22. This is a constructed counterexample, not model output. The proposed gate now recognises explicitly allowed alternatives when both answers have correct reasoning. Exact label changes remain a separate reported measure.
4. **An early probe inferred an exit status.** It translated a caught exception into the expected status instead of recording the command's actual exit. The revised probe records the actual outcome. The earlier run is preserved as superseded.

5. **Omission checks covered only empty guides.** The earlier bank had no partly complete guide. One item now retains three correct claims while omitting a required rule, with the missing coverage recorded explicitly.
6. **No item challenged a false claim of undocumented inference.** One challenge now states the behaviour correctly but falsely says the supplied documentation does not state it. The documentation contradicts that assertion. The key rejects the false attribution while preserving credit for correct behavioural coverage. This does not claim access to a model's internal reasoning.

Five targeted supplementary scenarios checked assertions that were not directly exercised by the original probes. They are included in the 37 total, not counted again.

These are findings about preparation quality. They are not evidence that the interpretation layer helps an agent.

## Adversarial review of the expected answers

The subsequent review examined every expected verdict: 295 claim decisions and 96 coverage decisions across all 72 items. The private record traces them to the permitted evidence, checks alternatives and explains the treatment of omissions and serious mistakes.

Three issues were addressed:

1. A supposedly equivalent paraphrase assumed a starting state that its scope did not require. A runtime counterexample showed that a correct reviewer could reject it and receive a serious error. The paraphrase now preserves the actual state transition.
2. Another rule blurred successful completion with success of a following step. A targeted check reproduced completion followed by failure. A separate check also exposed an unstated entry precondition. The wording now preserves both boundaries.
3. The coverage rule did not explain how to score a guide that states a rule correctly and contradicts it elsewhere. The reference now gives coverage credit for the complete correct statement, while the contradictory claim still fails its own assessment. Coverage cannot make that guide pass.

Five new runtime scenarios passed. They are included in the cumulative 42; the earlier 13 deliberate faults and upstream test counts are unchanged. The revised bank passed all 72 source, schema, identity and request checks. During editing, that audit caught a newly miscalculated submission hash; it was corrected and the failed check was retained. Previous freezes remain intact.

The expected verdict labels, role prompts, proposed thresholds and 144 call schedule did not change. The reference wording did change, before any qualification answers. No further demonstrated verdict mismatch was identified in this review. This is a bounded investigator audit, not a proof that no gaps remain.

## Limits and remaining work

All four cases use authored candidates and make documentation available. They concern Python libraries or applications. There are no naturally generated model answers in the bank. Any eventual qualification claim must stay within the represented source conditions, cases and roles.

The bank now includes conflicting source material and instructions embedded in a candidate. The conflict is an explicitly fictional deployment scenario. It tests whether an assessor avoids inventing a decision; it is not evidence of a historical owner dispute.

Codex prepared and checked the references. There is no independent human certification. Published evidence and reproduced behaviour support the expected answers; AI agreement is not the basis for them. Detailed records remain private until they can be released without compromising qualification. The hashes below commit to those records but do not independently certify their contents.

The complete execution protocol, criteria and settings still need to be frozen before model answers are opened. The [qualification batch runner](../phase1-harness/QUALIFICATION-BATCH.md) now completes the fixed 144 call schedule in simulation. It does not yet expose an authorised live batch entry point. Actual model access, account settings and input bounds remain unverified. No API spending is authorised.

**Next:** finish the controlled familiarity connection and actual provider/account checks. Freeze the full protocol and bind a live batch entry point to an explicitly authorised allocation before model qualification. The offline runner is complete; no paid calls are authorised.

Private bank freeze SHA256: `bc256b1d390f2f595c0212d157892572fd64226701200236ffcf28add0ef8ae9`.

Private audit SHA256: `ab18e11b0eef432ab1a498916f481eaeed50c0d1647ec7eda29c11b450a23f22`.

The private files remain on the preparation PC. Public Git sync does not transfer them to the laptop. The [first Q01 readiness report](Q01-READINESS.md) remains a historical record of that earlier version.
