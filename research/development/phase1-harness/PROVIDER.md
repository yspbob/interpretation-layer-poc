# The first model connection

The harness now has a connection to the OpenAI Responses API through the official Python SDK. It has been tested with simulated provider responses. No real endpoint, credential or model has been exercised, and Astra has now been selected for the first stage. Fable is deferred.

This replaces the rehearsal's answer delivery mechanism. The controller still owns drafting, verification, corrections, guide release and separate assessment. The connection sends the role's permitted information and receives its structured answer. It does not receive the authored answers used in development tests.

## What it sends

Each call is a fresh request. The drafter receives the fixed source pack, plus its previous draft and the verifier's feedback when a correction is needed. The verifier receives the sources and candidate claims. Assessment receives its declared candidate or review and the separate reference. Candidate identities are supplied explicitly so assessment can identify the artifact it evaluated.

The connection rejects unexpected fields, changed source hashes, changed reference hashes, stale call numbers and requests for another attempt. It supplies no conversation identifier, previous response identifier, remote tools, file upload, browser or execution capability. Source URLs are text; the connection does not fetch them. Each SDK client is newly created, so cookies do not carry between calls.

The destination is fixed to the Responses endpoint. Environment proxy and base URL settings cannot redirect it. Redirects and automatic retries are denied. Credentials are passed explicitly by the trusted host process and are absent from role inputs, saved request bodies and exception messages.

Structured output format is requested through `text.format`. The provider schema uses a conservative subset; the controller retains stricter local validation, including citation hashes and line ranges. Refusals, incomplete responses, unexpected tool outputs, duplicate JSON keys and invalid records stop the attempt. Nothing executes the model's output.

These request fields follow the [Responses API reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create) and [structured output documentation](https://developers.openai.com/api/docs/guides/structured-outputs). Their compatibility with the eventual model still needs a live qualification check. Setting `store` to false is a request setting; it does not by itself verify provider retention, training policy or account configuration.

## How the spending stop works

The operator supplies the model, reasoning setting, token allowances, rates and total allowance. There is no default experimental model or price. Before a request can leave, the connection saves its exact body and reserves enough of the remaining allowance for the configured maximum input and output tokens. All roles in that attempt share the same ledger.

When a response includes valid usage, the ledger replaces the reservation with the amount calculated at the configured rates. It records the original usage breakdown, including any reported reasoning tokens. It applies the full configured input rate without claiming a cache discount. A refusal or malformed answer still retains its usage and calculated cost.

If the connection times out, cannot obtain valid usage, sees an unexpected model or service tier, or observes tokens beyond the reserved allowance, it stops. The reservation remains held for investigation. It never assumes the call was free or tries again automatically. Reopening the same ledger or reusing the connection for another attempt is denied. Reservations are flushed to disk before dispatch. A completed controller attempt closes its connection.

Amounts use integer billionths of a US dollar to avoid rounding during these checks. The test rates are fictional. This is a control over the configured allowance, not an unconditional guarantee about a provider invoice. The input screen uses request bytes plus padding as a conservative development check. Before live use, verify the selected model's input bound and upper billing rates, including any applicable cache write charges. A wrong bound or price can make a single call more expensive than reserved; the connection can stop subsequent calls but cannot undo that charge.

The cap is for one authorised attempt. It does not control unrelated account activity or spending from the other machine. Each further attempt requires its own reviewed allocation. An approval record binds the settings, evidence, prompts, schemas and exact ledger path, and expires. It records operator authorisation; it is not a cryptographic proof of consent or an account wide quota service.

## What the tests establish

The combined suite has 52 passing controller and connection tests. The full NetBox and HTTPX development scenarios also pass through the actual SDK, making 49 simulated requests across eight scenarios. The simulation supplies answers at the HTTP transport boundary, after request construction. A socket guard blocks real connections during these tests.

The checks cover role inputs, shared budgets, usage settlement, timeouts, HTTP errors, retries, redirects, environment overrides, cookies, malformed outputs, model and price tier changes, disk failures, stale attempts and concurrent calls. The earlier 15 controller checks remain included. See [provider-results.json](provider-results.json) for the recorded results and exact script hashes.

These are tests of the connection and workflow. Authored answers and token usage are not evidence of model judgement, cost or benefit. The controlled model path reads supplied text and has no execution tools. It does not run arbitrary agent code inside the earlier Docker worker, and it does not extend that worker's containment claims. HTTP timeouts and response size checks are not a proof against every runtime or infrastructure failure.

## Reproduce without calling a model

From the repository root, after the existing source preparation:

```powershell
local-runs/phase1-env/Scripts/python.exe -m pip install -r research/development/phase1-harness/provider-requirements.txt -c research/development/phase1-harness/provider-lock.txt
local-runs/phase1-env/Scripts/python.exe research/development/phase1-harness/run_provider_checks.py
```

The command has no live mode. Missing source caches can be prepared using the earlier harness setup; fetching pinned public source is separate from provider testing. Full test logs, request bodies, responses and ledgers are saved under ignored `local-runs/provider-checks/`. The public summary contains hashes and outcomes. Private future assessment material must stay outside the public repository.

The library contains the real SDK transport, but constructing it requires an explicit credential and an unexpired approval matching the policy. There is no approval or credential checked into this project. The 52 tests use only simulated transport, including checks that an unapproved live connection is rejected. The SDK and transport are pinned to OpenAI 3.13.0 and HTTPX2 2.12.0. The official [SDK guide](https://developers.openai.com/api/docs/libraries) identifies the Python client used here.

## The next decision

The user selected Astra alone. The [preparation package](../astra-preparation/README.md) contains private familiarity packets and proposed settings, qualification criteria and spending. The separate familiarity request format still needs a controlled transport and a batch ledger. Verify account and input assumptions before seeking screening authorisation, and prepare separate qualification cases before seeking that allocation. Both NetBox and H06 remain public development material. A successful first connection test will not, by itself, qualify the verifier or assessor.
