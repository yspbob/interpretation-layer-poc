# Fixed Fable qualification procedure

14 September 2026. This specifies the existing guidance assessor test through Claude Desktop, using Fable 5.1 at High effort and only the included Max allowance. It does not start model calls. The private freeze commits to the exact inputs, order, instructions, schema, scoring criteria and procedure before responses are opened.

## Inputs and order

Use the existing four families and six guidance challenges per family. Each runs twice in a separate incognito chat: 24 distinct challenges and 48 scheduled responses. Preserve the order of the existing Astra schedule after filtering it to the guidance assessor role. Do not select, rearrange or omit challenges based on answers. The 144 call Astra schedule remains unchanged.

Each scheduled folder contains a file named input.txt. It has the unchanged role prompt, response schema and permitted packet from the frozen bank. That packet contains the candidate, its identity hash, source excerpts and the reference criteria the assessor may use. Candidate and source instructions have no authority. There is no expected candidate answer, Astra assessment, investigator commentary or schedule metadata in the attachment. The private schedule maps neutral folder numbers to the original items; never upload the schedule or freeze record.

The desktop delivery wrapper is fixed separately. It prohibits tools and asks for JSON in the chat. Unlike the controlled API request, the schema is text in the attachment, not a provider enforced response format. The local validator checks the returned structure and identities; it cannot establish that the decisions or reasons are correct.

## Before each session

Apply [desktop procedure version 2](FABLE-DESKTOP.md), including the separate cloud execution restriction, disabled connectors, fresh incognito chats and High effort. The earlier diagnostic settings were restored afterwards, so do not assume they remain off. The recorded app version was 1.52386.3. Record the installed app version and exposed settings; a changed app version needs a public operating check before continuing this frozen schedule.

Check the private freeze hash and every scheduled file before dispatch. Use only that position's input.txt and the common wrapper. Check included allowance before every request and after the session. Pause before submission if a plan limit is near, uncertain or reached. No API requests or usage credits are authorised. An available subscription percentage is an observation, not a technical spending cap; retain this limitation and do not run unattended.

## Save the first answer

Before submitting, create a private attempt record with the schedule position, input and wrapper hashes, displayed model and effort, settings observations, usage observation and dispatch time. If that record already exists, inspect it rather than submitting again. A saved dispatch with no clear outcome is an uncertain attempt, not permission to retry.

Submit once. Preserve the complete first answer, visible tool activity and completion observation before closing the chat. Capture screenshots and refreshed accessibility text. Verify that the capture reaches the end of the answer; the earlier rehearsal showed that accessibility text can lag behind the screen. If the response is long, retain the successive visible portions with overlap. Do not infer missing text or ask the model to complete it.

Retain the raw capture separately from parsed JSON. A single enclosing Markdown code fence may be removed for parsing; other extra prose, duplicate JSON keys, malformed JSON or more than one JSON object fail structural validation. Validate the unchanged schema, candidate hash, exactly one decision per submitted claim and exactly one decision per reference unit. Empty candidates require an empty claims array and the full reference coverage assessment. Keep original text even if parsing fails. A response over the existing 128,000 byte local answer limit fails; this is a processing limit, not a claim that the app enforces an output token cap.

The operating rehearsal covered plain text attachment reading at 32,768 bytes. The actual attachments and wrapper must fit that envelope without removing source content. Byte fit is not a token limit guarantee. The previous H06 review demonstrated preservation of a longer answer, while the two restricted diagnostics returned short JSON. Complete capture of the actual qualification response shape must therefore be checked on every attempt, not assumed from those diagnostics.

## Failures and pauses

Malformed, refused, incomplete and missing answers remain unsuccessful scheduled items. Do not retry, regenerate or coach them. A completed but structurally invalid answer does not by itself authorise changing the prompt. Continue to the next scheduled position only if the input, settings, capture and access requirements remain intact.

A tool call, flagged response, displayed model change, missing input or loss of required settings stops the session. Preserve the attempt and report the deviation. Do not count it as a pass. The app's safety routing setting is unchanged; no immutable backend version is claimed.

Allow up to fifteen minutes after dispatch for the first answer to complete. This is an operator deadline, not a provider enforced timeout. If it is still running, record the incomplete attempt, stop it through the app and close the session after capture. Any later text stays in the audit record and cannot replace the deadline result. No automatic retry follows.

An ordinary break or exhausted included allowance can pause between calls. Resume at the first never submitted position using the same freeze and settings; check prior records first. If dispatch is uncertain, mark that position unsuccessful and preserve its uncertainty. Do not submit it again. A material configuration or input defect requires an amendment before further calls. Any qualification answer used to tune the role makes the affected family development material under the existing rule.

## Scoring and decision

Freeze the existing [qualification criteria](QUALIFICATION.md) and the bank's item specific expected decisions, acceptable alternatives and severity through their original freeze commitment. The desktop input builder does not read scoring keys. They stay available only to the investigator who scores the saved answers.

Inspect response structure during execution, but defer semantic scoring and reconciliation until the schedule completes or is formally stopped. Reading a response to preserve it does not permit feedback to a later attempt. Match every decision and its reason to the fixed evidence. Preserve both correct objections and mistaken objections; agreement between models is not an answer key. Record unresolved reference defects and follow the correction and exposure rules rather than changing a label silently.

All four existing gates apply: no serious errors; at least 44 of 48 successful responses and 10 of 12 in every family; at least 22 of 24 consistent repeat pairs with correct reasons; and at least seven of eight baseline versus valid alternative comparisons meeting the stated rule. Missing and unrun items prevent a premature pass. Report the denominators, exact label agreement and failures separately. These are exploratory tolerances, not a population accuracy guarantee.

A pass applies only to this supplementary desktop assessor and the tested scope. It does not qualify Astra, the verifier, a coding judge or the interpretation layer. Qualification results remain separate from the two H06 development reviews and two access diagnostics. No experimental guide exists yet.
