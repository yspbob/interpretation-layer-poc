# How qualification answers will be scored

Version: qualification-scoring-v1. Fixed before collection. This procedure does not change the four acceptance requirements in [QUALIFICATION.md](../astra-preparation/QUALIFICATION.md).

The purpose is to check whether Astra can give defensible assessments. Correct labels alone are insufficient. We also read the explanation and check what it says against the evidence.

## Finish collection before scoring

Keep all 144 scheduled positions. Do not replace a refusal, failed request or missing answer with another attempt. An operational stop leaves the remaining positions marked as not run. They do not disappear from the denominator.

After collection completes or is formally stopped, save a commitment covering the policy, schedule, requests, original responses, usage records, ledger and summary. The execution command creates this commitment after a normal completion or recorded stop. An interruption or recording failure requires an investigator to reconcile the saved records and formally close collection first; it must not trigger a replacement attempt. Record why collection stopped and any unresolved spending. Do not open answers for semantic scoring until this commitment exists. The collector may check response format and identity during collection; it must not consult expected answers or alter later inputs based on apparent performance.

Use the original committed input bank and its separate keys. Record the input commitment, collection commitment, scoring procedure hash and investigator identity in the scoring record. An incomplete or damaged collection cannot receive a qualification pass.

## Review each answer

Review each response on its own before comparing its repetition or another role's answer. Use the submitted artifact, the role's permitted evidence and the expected decisions. The verifier must not receive credit based on evidence available only to its assessor.

For each claim, record the actual label and whether the frozen key permits it. For a guidance assessment, do the same for every coverage unit. Then read the complete explanation, including statements outside the labelled decision. Record the relevant response passage and source passage or named observation. A citation that exists but does not support the explanation is not enough.

Use three explanation outcomes:

| Outcome | Meaning |
|---|---|
| Pass | The explanation supports the verdict under the stated conditions and adds no materially false assertion. |
| Fail | A required reason is missing, or the explanation makes an unsupported or contradictory factual claim. |
| Ambiguous | At least two plausible readings have different outcomes. Record both readings and their evidence. |

Accept correct paraphrases and explicitly permitted alternative verdicts. Read statements in context. Distinguish what a wrapper calls directly from the effects of the called implementation. Missing evidence does not establish the opposite claim. Apply the declared coverage rule across the whole candidate; a separate contradiction fails claim support without erasing another complete correct statement.

Check the frozen serious error categories separately. Record yes, no or ambiguous, with the item specific basis. Do not invent a new serious category after seeing an answer. An operational failure is unsuccessful, but is not automatically a serious semantic error.

Each response record contains its scheduled ID, original response hash, completion status, actual labels, label agreement, explanation outcome, cited basis, serious error finding and overall outcome. Every required claim and coverage unit must be addressed. An empty guide still has coverage requirements. A summary sentence cannot substitute for these records.

## Preserve uncertainty

A completed response passes only when all required labels and reasons pass and there is no serious error. Failed, refused, malformed and uncompleted positions are unsuccessful. Retain their operational cause separately from semantic errors.

For an ambiguous explanation, preserve a conservative result that counts it unsuccessful and a more favourable result only where a recorded, source supported reading permits that result. Report both totals. If qualification depends on that interpretation, report qualification as unresolved and do not use the role for scoring yet. This is not permission to choose the reading that lets it pass.

If a source check exposes a flawed reference or key, preserve the original scoring and record the affected items, evidence and proposed correction. Do not rewrite answers or silently change the key. Show the sensitivity of the conclusion to the correction. Material that informs a revised rubric or instruction becomes development for that revision; it cannot silently certify the repaired role.

## Audit the scoring

The investigator performs a second source check after the first scoring pass. This is a consistency check by the same investigator, not independent human certification. Save the second check before comparing it with the initial decision where practical; do not claim the investigator has forgotten the first review.

The audit selection rule is fixed now. Rank scheduled IDs by SHA256 of the input freeze hash, a colon and the scheduled ID. Within each family and role, select the lowest ranked baseline or valid alternative response and the lowest ranked response from the other four challenges. This selects 24 positions across the twelve family and role combinations, without choosing favourable results.

Also audit every failed or ambiguous semantic assessment, every serious error finding, and every disagreement between repeated answers. For each role, add the lowest ranked completed response for any actual verdict type absent from the selected audit. Audit every operational failure against its collection record. Deduplicate the selected positions and save the final list and selection reason. If an audited decision changes, keep both versions and review every other response affected by the same reason.

## Apply the existing requirements

Calculate results separately for each of the three roles, always using 48 scheduled responses:

1. No predefined serious errors.
2. At least 44 complete responses pass, including at least 10 of 12 in each family.
3. At least 22 of 24 repeated pairs give permitted decisions and correct reasons in both responses. Also report exact label agreement separately.
4. At least seven of eight baseline and valid alternative comparisons pass, with no serious rejection of a valid alternative. Compare the two challenges within each family and repetition. Both answers must have correct reasons and matching applicable decisions, allowing only the alternatives explicitly permitted by the key.

Keep counts by family and challenge. A pair of wrong answers agreeing with each other does not pass. Apply all four requirements to both uncertainty interpretations. Publish the conclusion, limitations, deviations and source justified corrections together. Fable agreement cannot substitute for this evidence review.

The qualified scope, if these checks eventually pass, is the bounded documentation available assessment tested here. It would not qualify coding judges, interactive checkers or all forms of evidence. No model is qualified by this written procedure or by a simulated answer.
