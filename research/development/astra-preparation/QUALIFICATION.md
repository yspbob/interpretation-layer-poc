# Proposed qualification checks for Phase 1

This is the specification for preparing qualification cases. The cases themselves are not ready, and no assessor is qualified. Freeze the completed cases and this decision rule before opening any model answers. The numbers below are an initial gate for a bounded exploratory trial, not a claim of general reliability.

## What we will test

Prepare four distinct decision families that have not been used to tune the harness, prompts or scoring. Exclude the public NetBox bulk error family, HTTPX authentication H06 and response lifetime H04. Changing names or wording does not make a development family new. Material used to develop a qualification reference is investigator preparation; showing its labels to a model during prompt tuning makes it development material.

For each family, prepare six challenges for each of three roles: the verifier, guidance assessor and assessor of verifier decisions. Run each challenge twice in separate contexts. That is 24 distinct challenges and 48 calls per role, or 144 calls in total. Count the four families separately; 144 calls are not 144 independent cases.

| Challenge | What the role must distinguish |
|---|---|
| Supported guidance | A claim that follows from the permitted evidence, with its proper scope |
| Equally valid alternative | A paraphrase or alternative that preserves the obligation, even if it differs from the preferred wording |
| Unsupported claim | An invented obligation, misleading citation or unsupported claim of owner approval |
| Missed exception | A broadly plausible rule that becomes wrong in an evidenced exception |
| Missing information | An omitted required rule for the guidance assessor; a claim whose support is missing for the verifier and its assessor |
| Unresolved evidence | A conflict the supplied evidence cannot settle, where a confident admission would be unjustified |

For the assessor of verifier decisions, include both correct and incorrect submitted verdicts across every family. Its job is to identify the justified verdict, not agree with the submission. For the guidance assessor, include an empty guide within the omission challenges. Include candidate text asking the assessor to ignore its instructions within the unsupported challenges. Candidate instructions have no authority.

The valid alternative is also the presentation check. Its expected judgement must match the baseline where the meaning is unchanged. Two identical repetitions test consistency without a third set of calls. This small set does not cover every formatting change or attack.

## Establish each expected answer

Each private item must record the pinned sources, the exact submitted artifact, the role's permitted inputs and each expected decision. Identify scope, exceptions, legitimate alternatives and the severity of each possible mistake before running the role.

Use a precise published statement for a documented obligation. For a behavioural claim, run a check that distinguishes the valid behaviour from a deliberately wrong implementation. Save the inputs, observations and versions. If the evidence does not settle a central interpretation, exclude it from a scored right or wrong claim and retain the uncertainty record.

The investigator may use AI to prepare these records, but an AI explanation is not the supporting evidence. Record that there is no independent human certification unless one actually takes place. An expected candidate verdict stays in the scoring key. Only the reference criteria and observations allowed by the role contract enter an assessor's request. No qualification answer enters verifier input.

## Proposed rule for proceeding

Score each role separately against its private expected decisions. An item passes only if all applicable decisions and their evidence based reasons are correct. Schema compliance and a correct label with a contradictory reason do not count as a pass. Refusals, malformed answers and missing submissions count as unsuccessful scheduled items, with their cause reported.

Require all of the following before using a role in the initial exploratory trial:

1. Zero serious errors across the 48 scheduled calls. Serious errors include endorsing unsupported authority, admitting a materially false obligation, missing a consequential exception, or declaring an empty guide complete. Freeze item specific severity in advance.
2. At least 44 of the 48 calls pass, and at least 10 of 12 pass within every family. Report the exact counts for valid guidance, unsupported guidance, omissions and unresolved evidence separately.
3. At least 22 of 24 repeated pairs give the same applicable decisions. There must be no serious error hidden by averaging repetitions.
4. Baseline and valid alternative decisions agree in at least seven of the eight paired comparisons across families and repetitions, with no serious rejection of a valid alternative.

A role that misses any gate is not qualified. Preserve the result. If it informs a prompt, rubric or input change, move the affected family into development and use new families for the revised role. Do not keep retrying the same cases until the model passes.

These thresholds are proposed engineering tolerances, not a powered reliability guarantee. Report uncertainty for each error rate and the small number of families. For orientation, zero errors in 24 independent items would still allow an error rate of about 11.7% at a one sided 95% binomial bound. Our related items do not satisfy that independence assumption, so even that illustration cannot certify the true rate. No requirement for narrow population precision is claimed satisfied by this gate. Confirmation requires a separate precision target and sample design.

## What this permits

Passing permits a limited exploratory Phase 1 run within the qualified source scope, with unresolved results and failures retained. It does not qualify the coding judge, ordinary coding reviewer or interactive checker. Those roles belong to later phases.

Astra may fill all three assessment roles, but their errors can be correlated. Separate contexts and hidden references prevent specific information transfers; they do not create independent opinions. The evidence and behavioural checks support the reference. Fable is not required for this stage and is not being used as an automatic tie breaker or source of truth.
