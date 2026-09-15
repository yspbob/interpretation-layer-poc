# Codex subscription collection check

15 September 2026. This is a development result, not model qualification.

The small collector now delivers an assessment packet to Codex, saves the first answer and checks it with the existing response validators. All three public examples completed through the existing subscription. No reserved qualification case was sent.

## What we checked

Each example described an artificial source file containing `DEFAULT_TIMEOUT = 30`. The verifier checked a claim about that assignment. The guidance assessor checked the same claim and its coverage of the reference requirement. The verifier assessor checked a submitted admission decision. All three returned the straightforward supported decision with a source based explanation. This is a connection and recording check, not a meaningful test of difficult assessment.

Each call requested Astra at High effort and used a separate empty working folder and Codex profile. Only the ChatGPT login cache was temporarily copied into that profile. Project instructions, previous conversations and the ordinary profile configuration were not copied. The temporary login copies were removed after collection. Account observations before each call showed included allowance available and no paid credits; the final check showed 38% remaining. API credential variables were excluded and ChatGPT authentication was required. No separately billed API route was used.

The three session records each contain one completed turn and one answer, with valid identifiers, source references where required and a usage record. There were no recorded tool attempts or retries. The client reported **15,187 input tokens and 364 output tokens** across the three calls. No call was repeated.

## Checks before and around those calls

Sixteen focused unit tests pass. They cover changed packets, injected answer fields, source hashes, wrong response identities, duplicate JSON fields, extra answers and turns, missing startup confirmation, unexpected diagnostics, tool events, failed calls and subscription account gates.

Tests using the actual client and a local simulated provider returned valid records for all three roles. The captured local requests contained the exact packet once and no project state or skills catalogue. Forced tool use, a deadline and changed inputs stopped collection. A stop request arriving as an answer finished exposed a race: the first implementation accepted that answer. The collector now checks for a stop again at completion and during the answer audit. The failure and corrected checks are retained.

The final audit also checks source bytes and citation coordinates before dispatch. These input checks and the final stop check were added after the three live examples. The saved inputs and answers pass the final checks without another model call. Role instructions, schemas and model settings were unchanged.

## What this does not establish

The local capture establishes what the simulator received. The authenticated subscription calls have saved input files, invocation settings, client events and answers, but no captured raw provider request or immutable served model identifier. The requested model and effort are recorded; a separately verified backend snapshot is not.

A forced tool test also produced a second local request before the external stop took effect. Tool execution was denied and the collection was rejected, but the launcher does not guarantee exactly one provider request. Client internal retries and a hard provider token limit remain unverified. The five minute deadline and record size limit are local operational controls.

Astra remains unqualified. There are zero qualification answers and zero experimental guidance runs. The earlier two subscription connection probes and 24 familiarity responses remain separate.

## Next step

Fix the subscription qualification protocol and connect this collector to the existing fixed schedule. Explicitly record the client audit limits above, stop on uncertain allowance, and retain every failed attempt. Do not expand the bank or add another assessment framework. The 144 responses, role instructions and four acceptance requirements remain unchanged. Reserved dispatch requires that protocol and its concrete allocation to be fixed first.

The [aggregate result](codex-collector-results.json) contains totals and the private evidence commitment. Raw records and temporary client files are not published. The collector is [codex_subscription.py](codex_subscription.py); its focused checks are [test_codex_subscription.py](test_codex_subscription.py).
