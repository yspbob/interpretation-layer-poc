# Prepare Astra's Phase 1 qualification

15 September 2026. Specification for preparation, not a frozen batch or permission to run it.

We need to check that Astra can assess guidance before we use its scores to judge the interpretation layer. This document keeps the existing test size and acceptance rules. It replaces material that helped shape the revised instructions.

## What stays in scope

| Role | What it receives | What we test |
|---|---|---|
| Verifier | A proposed guide and the sources available to its drafter | Whether it admits supported claims, rejects unsupported ones and preserves uncertainty |
| Guidance assessor | A saved guide, permitted sources and separately prepared reference criteria | Whether it recognises correct claims, errors and missing rules |
| Assessor of verifier decisions | A submitted review, its candidate guide, permitted sources and reference criteria | Whether the verifier's decisions were justified |

Each role starts in a separate context. The verifier never receives the hidden assessment reference. Expected candidate answers, investigator notes and earlier model answers stay out of all requests. The third role sees the submitted verdict because that is what it must assess, but does not receive the expected verdict.

These are the three roles already represented in the harness. Combining the two assessment jobs now would create a new configuration to develop and test. The drafter's performance is measured in the experiment itself. Coding judges and interactive checkers remain outside this qualification.

## Which material remains usable

| Existing family | Treatment in the revised batch | Basis |
|---|---|---|
| Q01 | Retain its complete set of 18 items, subject to the final input and reference audit | It was not selected for the instruction repair. All six challenges for each role remain available. |
| Q02, Q03 and Q04 | Development only for all three revised roles; replace them with three distinct families | Their evidence and failures shaped common instructions and reference presentation. The committed repair selection explicitly retires them. |
| NetBox bulk error, HTTPX H06 and H04 response lifetime | Continue to exclude | They are already public development material. |

Q01 was evaluated with Fable, and its result is known. Retaining it does not make the batch wholly unseen across models. Its eligibility rests on the recorded development split, not its passing score. Do not select individual successful items or modify Q01 in response to its Fable answers. If its contents are used to tune the revised instructions, retire the whole family too.

An integrity check on 15 September matched all 48 files in the original bank commitment and all 26 in the repair commitment. The six repair inputs belong only to Q02, Q03 and Q04. Q01 retains six items per role. This establishes the recorded contents and selection, not an absence of every possible influence on the investigator. See [the compact audit record](astra-qualification-revision-audit.json).

## What the replacements must cover

Prepare three genuinely different decision families with new identifiers. Different wording, repository names or versions of the retired decisions are not sufficient. Start with one complete replacement before expanding to the other two.

For each family, prepare the same six challenges for each role: supported guidance, a valid alternative, an unsupported claim, a missed exception, missing information and unresolved evidence. Include correct and incorrect submitted verifier decisions. Across the complete bank retain an empty guide, a partly complete guide, a false provenance claim and instructions embedded in candidate text. Treat these as evidence requirements, not additional batches.

Use exact source revisions and passages. For behaviour, retain the setup, named observations and a check that detects a relevant deliberate fault. Include called implementation when a scored assertion depends on its effects. Otherwise limit the expected answer to what the supplied evidence establishes. A central ambiguity that cannot be resolved must not become a scored right or wrong claim.

Prepare the source record and expected answers before any qualification response. Explain legitimate alternative verdicts and any item specific serious errors. Do not impose the preferred wording when another interpretation is supported. Read an explanation as a whole: distinguish direct calls in an excerpt from effects of the code it invokes. If a later ambiguity remains, preserve it and report its effect on the result; do not silently choose the reading that lets the role pass.

The original bank represents documentation available cases with authored candidates. Retaining that scope avoids expanding preparation. It does not qualify assessment under every source condition. In particular, assessors used with code only inputs need applicable qualification evidence before that condition can receive scored results.

## Size and acceptance rules

Keep four families, six challenges per role and two fresh repetitions per challenge. That is 72 distinct role items and 144 scheduled responses, including 48 responses per role. Three replacement families require 54 new role items; they do not add calls to the earlier schedule. Repetitions test variability, not independent cases.

Apply the four existing requirements separately to each role:

1. No errors in the predefined serious categories.
2. At least 44 of 48 complete responses pass, including at least 10 of 12 in every family.
3. At least 22 of 24 repeated pairs give permitted decisions with correct reasons in both responses.
4. At least seven of eight baseline and valid alternative comparisons agree, with no serious rejection of a valid alternative.

Use the detailed definitions in [QUALIFICATION.md](QUALIFICATION.md). Correct labels accompanied by an unsupported factual explanation do not pass. Report exact label agreement separately from acceptable alternatives. Malformed, refused and uncompleted scheduled items remain unsuccessful, with the cause visible. Apply the frozen severity definitions rather than creating new ones after seeing the answers.

These are bounded exploratory tolerances, not a statistical guarantee of general reliability. Preserve each role's results and uncertainty. Failure ends that qualification attempt; it does not authorise coaching or retries.

## What needs preparing before execution

The [proposed role instructions](astra-assessment-instructions-v2.json) retain the existing output schemas and add the evidence distinctions learned during development. They are now installed in the provider adapter and checked against the declared revision. The revised input bank passed its full offline rehearsal; see [batch readiness](ASTRA-BATCH-READINESS.md). The loader requires exact agreement with runtime prompts and rejects the old freeze. Actual live configuration remains outstanding.

The loader accepts four family identifiers rather than hardcoding Q01 through Q04. Replacing three families therefore does not require a general scheduling framework. Reuse the fixed schedule design and existing source, identity and separation checks.

Before the first response, commit a new private bank containing the eligible Q01 material, three replacements, role instructions, schemas, expected answers stored separately, schedule, scoring rules and file hashes. Preserve the original bank. Rehearse that exact input configuration with simulated responses, including rejection of a changed prompt, source file or expected answer in a permitted pack.

Keep the previously proposed Astra High setting and input/output limits as proposals pending actual provider and account verification. The older cost estimate is not a current quote or spending approval. Verify actual access, request identity, usage accounting and the bounded live entry point, then present the exact allocation before paid requests. The existing simulation does not establish these facts. Any additional familiarity or connection work must be separately accounted for; it is not hidden inside the 144 qualification responses.

Collect original answers without retries, then score only after collection completes or is formally stopped. Freeze the reason review procedure and audit sample before collection. Investigator checks rely on sources and observations, without independent human certification. Preserve failures, ambiguous explanations and plausible alternative scoring. Do not rely on Fable agreement to resolve them.

## Fable's separate job

Fable is now an advisory reviewer, not a supplementary scorer. Its [instructions and objection record](FABLE-ADVISORY-REVIEW.md) keep it separate from Astra qualification. It reviews saved experimental guides and may challenge references during preparation. Its objections require source checks; silence does not certify anything. This specification adds no Fable qualification batch or model call.

## Next concrete deliverable

The four families are assembled and [the complete offline rehearsal passed](ASTRA-BATCH-READINESS.md). Q01 retention and the proposed runtime prompt binding are complete. Next fix the explanation scoring and audit procedure and prepare the bounded live entry point using simulation. Actual model/account verification and an authorised allocation remain gates. The input commitment is not a complete live protocol freeze. Preserve the separate drafter learning record without exposing reserved case answers or changing drafting on their basis.
