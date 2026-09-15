# Subscription qualification runner

The existing qualification schedule is connected to the Codex collector. The [subscription protocol](SUBSCRIPTION-PROTOCOL.md) defines the run: 144 sequential positions, unchanged role instructions and scoring, fresh account checks and no additional spending. Preparation and rehearsal do not start a model run.

The coordinator uses the existing bank loader, packet checks, response validators and durable file writer. It adds subscription account checks and a shared attempt record. It does not introduce a new judge or change the assessment cases.

## How an actual run works

Preparation produces a configuration record and an approval template whose approval fields are false. The record binds the private input bank, output folder, account, client binary, model catalogue, runtime, role instructions, schemas, protocol and scoring procedure. The selected model is Astra at High effort.

After the concrete allocation is approved, execution checks it again before every attempt and while the collector is running. A reservation is saved before dispatch. The first answer is retained and checked for format and identity. The next position starts only after the previous one finishes successfully and a new account observation is supplied. Unexpected tool activity, changed settings, reused sessions, failed collection or uncertain allowance stops the batch.

The supervising Codex task obtains the account observations using the app's usage tool. The runner requests one observation per scheduled ID through a local file exchange. A response must have been obtained after that request and still be fresh when dispatch begins. This is agent operated; it does not ask the user to click through each attempt. An absent observer stops execution after two minutes. Raw account receipts stay in the private exchange directory; their hashes are included in the saved observations.

All 144 positions appear in the final summary, including those left unrun by a stop. A collection commitment is saved before semantic scoring. A crashed process with an unfinished reservation needs reconciliation; it must not silently restart or repeat a packet. The output folder and allocation cannot be reused.

## Operator entry points

Use `subscription_batch.py prepare` with the frozen bank, client, catalogue, account identity, intended output folder and a new preparation file. This loads the permitted bank inputs and writes the unapproved configuration. It makes no model call.

Use `subscription_batch.py execute` with the same preparation inputs, an approved allocation, the ChatGPT login cache and the private account observation exchange directory. The command checks that the prepared configuration still matches. Execution requires the supervising task to service each account request with a fresh app tool result. It never falls back to an API key.

The exact private preparation record and invocation inputs are recorded in PROJECT_STATE.md. Do not place login caches, account receipts, reserved packets or raw responses in public Git.

## Evidence and limits

The [test results](subscription-batch-results.json) distinguish simulated answers from actual model responses. Rehearsal tests schedule handling and recording, not whether Astra makes good judgements. The three earlier public examples remain the only new live collection checks; no qualification answer has been collected.

The subscription route has less direct transport evidence than the API adapter. In particular, it does not independently identify the served backend snapshot or capture every provider request. The [protocol](SUBSCRIPTION-PROTOCOL.md) records those limits rather than treating an answer as proof of stronger isolation. Qualification, if achieved, will be reported within that scope.
