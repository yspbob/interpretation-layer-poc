# H04: response lifetime development case

Date: 8 September 2026. Status: **one executable development case and scripted component trace. Zero model calls, zero blinded comparisons, no qualified judges.**

HTTPX is a Python HTTP client. This case develops the response-lifetime family from inventory record H04 at commit `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`. The application task is to pass just the first response chunk to a consumer while preserving errors and releasing the response. The borrowed client must remain open.

## Artifacts and independent basis

- [Component contracts](../component-contracts-v0.1.md) specify the verifier, checker, ordinary reviews, final judge and shared controls.
- [Task](task.md) supplies the concrete change request. [Candidates](candidates.py) contain two valid implementations, two consequential cleanup errors and an unfinished implementation. Each function can be copied as `preview` into the task's `preview.py`; these are authored examples, not agent outputs.
- [Reference](reference.json) records the source pin, archive hash, criteria and expected scenario verdicts. It was written before the first execution. Expected labels come from the task, pinned source and observable cleanup behaviour, not a generated guide. There has been no independent human review.
- [Scripted trace](trace.json) records proposed claims, verifier verdicts, consultation, initial plan, a changed approach, correction and final review. Its verdicts are deliberately supplied by the investigator; matching the replay does not test whether a model would choose them.
- [Runner](run.py) imports the actual pinned HTTPX implementation, uses an instrumented in-process mock stream, exports hashed role packs, checks the file broker and checkpoint state transitions, and scores the candidate behaviour.
- [Recorded results](recorded-results.json) preserve actual observations, reference comparisons, hashes, environment versions, exact role input manifests and replayed states.

The [pinned async documentation](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/async.md#L85) permits manual streaming while assigning cleanup responsibility to the caller. The [context-manager implementation](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1542) places response closure in a finally clause. [Manual send](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1594) returns an unread streaming response; the [response iterator](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py#L1037) closes it after exhaustion. These support both the failure and the legitimate alternative.

## Observed behaviour

All 25 candidate/scenario verdicts matched the prewritten reference. A cell says whether the candidate met all three criteria in that scenario; deliberately broken examples should fail.

| Candidate | First chunk | Empty body | HTTP error | Consumer error | Stream error | Overall |
|---|---|---|---|---|---|---|
| Context manager | Pass | Pass | Pass | Pass | Pass | Pass |
| Manual send with finally | Pass | Pass | Pass | Pass | Pass | Pass |
| Manual send without close | Fail | Pass | Fail | Fail | Fail | Fail |
| Manual send, normal-path close only | Pass | Pass | Fail | Fail | Fail | Fail |
| Unfinished function | Fail | Fail | Fail | Fail | Fail | Fail |

The harness measures response and stream closure **before** cleaning up the fixture or closing the client. It also checks the returned chunk, consumer calls, amount read, original error preservation and borrowed-client state. Empty-body success alone would miss both seeded errors because exhausting the iterator closes it. The observed open stream establishes the missing cleanup; this mock test does not measure socket leaks or pool exhaustion.

The replay admits a scoped cleanup claim, rejects a universal ban on manual streaming and leaves invented owner approval unresolved. Only the scoped claim enters the example frozen guide. GUIDE and INTERACT packs have the same guide hash; DIRECT has no guide. Drafter and verifier packs omit the task and candidate solutions. Ordinary reviewer and checker packs show their respective inputs. Changed-plan packs contain the submitted code, not the expected decision. Final-judge packs contain neutral `preview.py` files, task, reference requirements, source evidence and observations, without expected labels, guide files or treatment names. No pack was dispatched to a model.

The checker trace proceeds with the context-managed plan, requests revision after a switch to manual send without cleanup, accepts explicit closure in a finally clause as a supported alternative, then reviews the final submission. Six control checks exercise correction exhaustion, acceptance on the second correction, terminal unresolved decisions, malformed decisions, known lifecycle-structure changes and verdict combination. Seventy-one broker denials cover prohibited file names, traversal/absolute requests and input tampering across the role packs.

## Reproduce on either machine

Use Python 3.12 and the pinned dependencies in [requirements.txt](requirements.txt). From the repository root, create a local virtual environment if absent, then run:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r research/development/h04-response-lifetime/requirements.txt
New-Item -ItemType Directory -Force sources,local-runs | Out-Null
Invoke-WebRequest -Uri 'https://codeload.github.com/encode/httpx/zip/b5addb64f0161ff6bfe94c124ef76f6a1fba5254' -OutFile local-runs/httpx-source.zip
Expand-Archive -LiteralPath local-runs/httpx-source.zip -DestinationPath sources
.venv/Scripts/python.exe research/development/h04-response-lifetime/run.py
```

Reuse an existing unchanged extraction rather than overwriting it. The runner rejects an archive hash mismatch, changed extracted source bytes or different declared dependency versions. `--source`, `--archive` and `--output` accept explicit paths. It writes fresh packs and the latest result under ignored `local-runs/`; the checked-in result is a reviewed snapshot. Initial setup uses the network; behaviour probes use only MockTransport and do not issue outbound requests. A hash mismatch after a changed GitHub archive must be investigated, never fixed by silently accepting a new hash.

## Limits and exact next step

This whole family, its answers and all variants here are public development material. The task explicitly requires resource cleanup; it is useful for developing evaluation and interaction controls, not establishing substantive recovery of a rule from code. These documentation-visible packs contain narrative disclosures and are not eligible code-inference packs.

The file broker rejects prohibited requests, but the investigator process can access the rest of this checkout. It is not an OS/container boundary. Real filesystem/network isolation, unrestricted semantic change detection, full runner pause enforcement, model output schema validation, real usage accounting and model qualification remain unimplemented. Async cancellation during cleanup, failing cleanup calls and real socket/pool behaviour are untested. No comparative benefit, judge accuracy or production cost follows from these checks.

Next implement a model-free isolated role runner: validate structured inputs/outputs, dispatch only immutable packs into fresh restricted processes/containers, verify filesystem and network denials, and enforce initial, changed-plan and final checkpoints including terminal stops. Keep H04 as the regression case. Then prepare different families and freeze qualification coverage, error limits and model settings before any authorised qualification calls.
