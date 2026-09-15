# The qualification runner is ready for configuration

15 September 2026. The scoring procedure and controlled execution command are implemented. Both have been checked without calling a model. **Astra remains unqualified.**

## What this step establishes

The runner can deliver the fixed set of 144 assessment requests, record what happened and stop when approval or spending conditions no longer permit another request. It does not decide whether an answer is correct. That review happens after collection under the [scoring procedure](SCORING-PROCEDURE.md).

All 86 controller, provider and batch tests passed. The new checks exercise approval denial, expiry, revocation, changed configuration, an operator stop, exhausted budget, uncertain usage and the full delivery sequence. Existing tests cover malformed answers, input separation, interrupted attempts and recording failures.

The exact private bank also completed all 144 requests through the live controller branch, with the HTTP transport replaced by a local simulator. The credential, model name, prices and answers were fictional. Socket connections were blocked. The loader opened only the freeze and 17 permitted input files; it did not open an answer key. Requests matched their scheduled packets and instructions exactly.

This rehearsal also checked original response bytes against the recorded response hashes and verified the commitment covering the whole collection. It does not establish actual API compatibility, account access, billing or assessment quality. The internal counter named `model_calls` counts attempted provider calls; in this transport simulation it does not represent model generations. The public report correctly records zero live model calls.

See [the recorded totals and source hashes](live-qualification-results.json). Previous input commitments and rehearsals remain preserved. The new runtime has a separate commitment; it does not rewrite the earlier runtime snapshot.

## How approval controls execution

The preparation command checks every distinct request and creates a configuration record and an approval template. Every approval gate starts false. Preparation reads no credential and makes no request.

The configuration binds the input bank, role instructions, schemas, source code, scoring procedure, dependency versions, model settings, prices, batch budget, credential fingerprint, account record label and destination folder. A change requires a new reviewed configuration. The credential itself is supplied only at execution and is not saved in the records.

Before execution, the operator must record actual model access, account verification, provider data settings, price verification, a justified input allowance and the user's spending approval. The approval includes its scope reference and expiry. These entries are attestations backed by separate evidence. Setting a flag does not prove a provider setting or create user consent. The account label alone does not identify a verified provider account.

The runner rechecks the approval file, configuration and expiry before each attempt. Removing or changing the approval stops the next attempt. Creating a file named `STOP` inside the collection folder also stops before the next attempt. These controls do not cancel a request already in flight.

Every attempt reserves its full configured maximum before possible dispatch. An answer with known usage settles that reservation, even when the answer is invalid. Missing or untrusted usage stops the batch and keeps the reservation. The schedule is never retried, resumed automatically or silently shortened. An existing collection folder cannot be reused.

## What the record preserves

Each request has one supplied input and no prior response or conversation identifier. The three roles receive their declared sources and references. This follows the API's distinction between [independent requests and explicitly supplied conversation state](https://developers.openai.com/api/docs/guides/conversation-state). It prevents this runner from forwarding earlier answers; it does not establish absence of prior model familiarity or a provider retention guarantee.

The provider adapter now saves the exact response body before parsing it, including a body that later fails validation. This closes a recording gap: the previous adapter saved parsed JSON but calculated a hash of the original bytes. The raw file now allows that hash to be checked directly.

After a normal completion or recorded stop, the command commits the policy, schedule, requests, responses, usage, ledger and summary. Semantic scoring starts only after this commitment exists. A process kill or disk failure may prevent formal closure. In that case, preserve the existing files and reconcile the collection before scoring. Do not start a replacement batch to hide an interrupted one.

All inputs, approvals and response collections stay outside the public checkout. A hash makes later changes detectable against the saved record; it is not independent proof that the operator followed the protocol. Private records still need protected storage and an agreed audit route. Public Git does not transfer them to the other machine.

## The remaining gate

Verify the actual Astra API identifier and supported settings, the intended account and data policy, prices and input allowance. Then prepare a concrete maximum cost and protocol allocation for approval. The largest simulated request used 32,741 of the 32,768 development allowance. Recheck it with the actual identifier and settings. This byte based estimate is not a validated provider token bound.

No live qualification call, new Fable export, further repair cycle or experimental guidance run is authorised by this implementation. The sample and all four acceptance requirements remain unchanged.

## Operator entry points

Run `live_qualification.py --help` in the existing Phase 1 Python environment for the required arguments. `prepare` creates new private configuration and approval files after preflight. `execute` requires those files and the explicit `POC_OPENAI_API_KEY` environment value. Never place a credential in a command line or in the public repository.

Use `run_qualification_checks.py` to reproduce the public synthetic tests. The exact private rehearsal script and runtime are preserved alongside its separately committed record; they are not an option to dispatch live requests.
