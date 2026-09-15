# Checking the claim we actually submitted

15 September 2026. Public development checks, not qualification.

The verifier must decide whether the evidence supports the claim it received. It must not quietly change the claim or the conditions under which it applies. Those conditions are its scope.

The stopped qualification attempt exposed a problem with how we recorded that decision. The verifier repeated the scope in different words, and a check requiring identical text rejected its answer. That failure alone did not establish that it had misunderstood the claim. We have preserved the failed run and changed the interface for future work.

## What changed

The controller now supplies a fingerprint of the complete draft. The verifier returns that fingerprint and the ID of each claim it judges. The fingerprint covers the claim text, scope, exceptions and supporting records. A decision for an earlier version cannot approve a changed version. The released guide still copies admitted claims directly from the submitted draft.

The verifier no longer returns a replacement scope. It returns a verdict, evidence references and an explanation. It must admit the whole claim, reject it when evidence contradicts it, or leave it unresolved when the evidence or wording does not settle the question. A narrower alternative can appear in its explanation, but cannot justify approving the original claim.

This is contract `phase1-development-v0.2` and assessment instruction version `astra-assessment-instructions-v3`. Only the verifier instructions changed. The drafter and assessment instructions keep their previous wording. Old packets and recorded answers retain their original contract. The frozen qualification bank has not been converted, retried or declared compatible with this change. Reproducing the stopped attempt requires its saved runtime, not the current code.

## Correct identity does not prove correct understanding

A verifier can refer to the right claim and still read it incorrectly. We therefore added three pairs of public examples. Each pair includes a claim the evidence supports, so refusing everything cannot pass.

| Example | Evidence and claim | Required decision |
| --- | --- | --- |
| Some inputs observed | A claim covers both supported inputs, but only one has been observed. | Unresolved. The missing observation is not a contradiction. |
| All inputs observed | The same claim is supported by observations for both inputs in the complete supported set. | Admit. |
| Different setting | The claim concerns default settings. The evidence says the default does the opposite; a special setting supports the behaviour. | Reject. The special setting cannot rescue the original claim. |
| Matching setting | The claim explicitly concerns that special setting. | Admit. |
| Ambiguous wording | The claim says a function normalises names, without defining normalisation. The evidence describes trimming spaces but preserving case. | Unresolved. Explain why different readings matter. |
| Precise wording | The claim explicitly says the function trims leading and trailing spaces. | Admit. |

These are invented examples with short, explicit evidence. They do not make claims about a real library. The packets, expected decisions and requirements for each explanation were fixed before dispatch. Only packets were sent to the model; expected answers and this assessment record were excluded.

## How the checks work

The offline tests reject a changed draft fingerprint, an unknown claim ID and a returned scope replacement. They also exercise every alternative verdict for all six examples. A deliberately mistaken admission with the correct fingerprint passes the identity check but fails the verdict check. This demonstrates that identity and correctness are separate checks.

For the live development check, each packet gets one fresh Astra High subscription session. The investigator checks the verdict, cited passage and explanation against the saved criteria. The verdict comparison is automated; the explanation review is recorded judgement by the same investigating assistant that prepared the examples, not an independent human review or a qualified assessor.

These simple examples can expose a specific defect. Success cannot establish reliability on unfamiliar or difficult cases. They are development material and must not be counted as independent qualification evidence. The original eleven qualification responses and their stopped outcome remain unchanged.

## Result

All six first responses gave the expected verdict. The investigating assistant also checked their explanations and cited passages against the saved criteria. All six met those requirements. The incomplete evidence and ambiguous wording cases remained unresolved; the wrong setting case was rejected; all three supported claims were admitted. Suggestions to narrow or clarify a claim were requests for a new draft, not approvals of a silently changed claim.

All 122 offline tests passed, including seven new interpretation tests and a check that the other role instructions stayed unchanged. The first test invocation was blocked by Windows temporary folder permissions. A permitted rerun exposed two outdated test expectations, which were updated for the new contract before the successful final suite and live calls.

The six calls used separate sessions and the included subscription allowance. No packet was retried, no tool attempt was recorded and no copied login file remained. The client reported 30,396 input tokens and 1,554 output tokens. A final account check showed 30% remaining allowance and no paid credits; account percentage changes also include the supervising task. We did not use an API billing route or call Fable.

The input commitment is `0883a10aed391fb7c29e111ab90fd0e9fe62befd39dd50451715bf539ffe2aca`. Collection was committed before inspecting answers, and all 130 recorded file hashes verified. Its commitment is `00722523c9fe7807876caffdd03b9a7e8cbbd10fef62e2490c72398a7aad1d83`. Raw session and account records remain private. The [aggregate audit](verifier-interpretation-results.json) records each verdict, explanation review and evidence reference.

The next step is to assess which qualification material remains suitable after the earlier exposure and this interface change, then prepare the corresponding allocation. The six examples do not qualify Astra and do not authorise resuming the closed batch. The drafter, coding judge and interactive checker are unchanged.
