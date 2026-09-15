# Lessons to carry into the guidance drafter

15 September 2026. Saved following the user's request to retain lessons from this exercise for the drafter.

The exercise has exposed weaknesses in evidence presentation and assessment reasoning. Those observations can inform the drafter, but they do not show that a revised drafter will perform better. No experimental guidance has been produced yet. The points below are requirements to consider when preparing its instructions and input format, not changes already installed in the drafter.

## State where a rule applies

A useful rule explains the relevant configuration, starting conditions and exceptions. Two statements about different stages can both be true. Before describing them as contradictory, establish that they concern the same circumstances.

The [original Fable qualification](FABLE-QUALIFICATION-RESULTS.md) contained explanations that confused missing support with contradictions between statements about different conditions. The proposed drafter response is to put scope beside each claim and preserve exceptions instead of compressing them into a broad rule. This transfer to drafting remains untested.

## Missing evidence does not prove the opposite

If the permitted sources do not establish a claim, preserve that uncertainty. Do not turn “we have no evidence of approval” into “the owner rejected it”, or an absent implementation into a claim that its behaviour cannot occur.

The original assessment errors and the [revised evidence instructions](assessment-evidence-instructions-v2.txt) support this distinction. For the drafter, unresolved claims should identify what is missing using only its permitted sources. The hidden assessment reference must not be used to fill the gap.

## Follow the code far enough to support the claim

An excerpt that calls another function does not establish every effect of that function. Supply the relevant implementation where needed, or limit the claim to what the visible code establishes. A narrow statement about direct calls must not sound like a guarantee about all resulting behaviour.

The [repair record](FABLE-REPAIR.md) documents omitted called implementation. The [six development responses](FABLE-REPAIR-RESULTS.md) also show why wording matters: one explanation admits two readings, which change its assessment. Preserve that ambiguity rather than treating it as an unequivocal model failure. The drafter should make the intended meaning explicit.

## Explain what an observation establishes

Name the setup, input and observed fields. A reader should be able to tell what was tested without guessing the meaning of an array position, an empty value or a scenario name. State the limit of the observation as well as its result.

The original review found misread observations. The development repair made their fields and setups explicit. Several error patterns did not recur in the selected checks, but evidence and instructions changed together. We cannot attribute an improvement to either change alone or assume the same effect for the drafter.

## Keep the origin of each claim visible

Distinguish a documented rule, a restatement of executable code and a conclusion assembled from several pieces of evidence. Give source locations and explain the connection. Do not present a rule found in the supplied guide as a discovery from undocumented code, or public documentation as owner approval of the new guidance.

This implements the existing [working plan](../../../preregistration/plan/working_plan_2026-09-05.md), rather than a new empirical finding. Provenance records what supports a claim; it does not reveal the model's internal reasoning or prove the absence of prior familiarity.

## Preserve useful detail without filling gaps with guesses

A guide that contains no false statements can still omit important guidance. The drafter should state the supported rules it can recover, including their exceptions, and make unresolved areas visible. It must not use the assessor's hidden list of expected rules to make its guide appear complete.

The assessment specification already separates support from coverage. Applying the distinction to the drafter is a design requirement, not evidence that it can reconstruct every relevant rule. Future evaluation must assess the original output, including empty or incomplete results.

When input size is a problem, first remove repeated metadata while preserving the evidence and its meaning. The [Q05 preparation](Q05-READINESS.md) demonstrated that this can make a packet fit the current development bound. It did not test whether shorter inputs improve model accuracy. Do not remove indispensable evidence silently to meet a limit.

## How we will use this record

Before the first drafter configuration is fixed, map these lessons to its instructions, input records and permitted output fields. Record which changes are adopted and their rationale. Use separate development examples to check the proposed behaviour before fixing the configuration for an experiment. Do not change the verifier or assessment prompts indirectly while doing that work.

Keep new qualification case contents, expected answers and investigator verdicts out of the drafter's prompt and examples. The lessons here draw on the earlier development review and public preparation findings, not on the sealed answers of the replacement families. If a reserved family is later used to develop a behaviour, record the exposure and exclude it from evaluating that revised behaviour.

The drafter prompt and output schema have not changed in this step. Any claim of improved drafting needs an actual comparison; these lessons alone cannot establish it.
