# First Astra qualification attempt: stopped at position 11

15 September 2026. No role qualified. No experimental guide was produced.

The user approved up to 144 sequential attempts through the existing subscription. The runner collected ten records that passed its format and identity checks. The eleventh response failed a contract check, so the runner stopped and left 133 positions unrun. Nothing was retried.

## Why it stopped

When the verifier admits a claim, the validator requires its returned scope field to match the submitted scope string exactly. The eleventh response admitted four claims but expanded their scope into explanatory wording. All four failed that text comparison.

For one of those claims, the expansion reproduced the test conditions already supplied in the packet. The stop therefore does not, by itself, demonstrate that the verifier misunderstood those conditions or invented a broader rule. We have not established that every reformulation is equivalent or that the whole answer is correct.

The instruction said that admission requires the exact submitted scope. The output schema described the scope field only as a string. It did not explicitly say to copy the original string verbatim. This is a confirmed mismatch between the accepted representation and the response. It is a reason to clarify that interface before another qualification attempt, while preserving the check against admitting a changed claim.

The frozen failure remains a failure. We have not relaxed the validator, rewritten the answer or counted it as a pass. An incomplete collection cannot qualify any role under the existing protocol. The first ten records have not undergone semantic scoring; passing the collection checks does not mean their judgements were correct.

## What was verified

All eleven attempts used different session IDs and each returned one completed client response. No tool attempt was recorded. Account receipts matched their saved hashes and showed available included allowance with no paid credits. All temporary login copies were removed.

The collection commitment covers 326 files, all verified. A separate 35 file audit preserves the authorisation, account receipts, failed scope comparison and reconciled usage. The original collection was not modified. The eleven responses reported **114,960 input tokens and 7,031 output tokens**. The original summary counted only the ten accepted records; the separate audit adds usage from the rejected answer. No separately billed API route or reset credit was used.

The exposure record contains four guidance assessor responses, six verifier assessor responses and one verifier response. The remaining positions were not sent. The [aggregate audit](subscription-qualification-stop.json) records the family totals without publishing reserved content.

The supervising task surfaced the final tool result several minutes after the runner had stopped and initially described the attempt as still running. That status was corrected. The runner had stopped normally, committed its records and made no further call. This was a monitoring delay, not a deadline overrun.

## Next step

Make the exact copying requirement explicit and check it on public development material. Then decide what fresh qualification material is needed for the revised verifier. Preserve the exposure record and do not silently reuse these responses to certify a repair. No prompt change or further model run has been made or authorised as part of closing this batch.
