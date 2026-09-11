# First guidance harness

This is a working rehearsal of the Phase 1 process. It passes authored drafts, reviews and assessments between separate containers and checks the resulting records. It makes no model calls. Passing this rehearsal does not qualify an AI verifier or demonstrate that the interpretation layer helps.

## What happens in one attempt

1. The drafter receives a fixed selection of source files. It returns claims with their evidence, scope, exceptions and provenance.
2. The verifier reviews every claim. It can admit a claim, reject it or leave it unresolved. A proposed change goes back to the drafter as a new version.
3. When preparation ends, the controller saves exactly the admitted claims. That guide remains an outcome even if it is empty or preparation has exhausted its corrections.
4. A separate guidance assessor examines the original draft and the released guide. It checks unsupported claims and missing required rules. Another assessment examines every verifier decision.

Assessment cannot repair the released guide or send hidden answers back into drafting. In this rehearsal, each role's answer is supplied by `fixtures.py`. The worker returns that answer; it does not reason about the source. The controller validates the records and combines the supplied judgements. In particular, a valid citation proves that a passage exists, not that it supports a claim.

## The NetBox assessment reference

The [runtime reproduction](../netbox-bulk-error-candidate/reproduction.md) establishes the behaviour behind this public development case. The reference asks whether guidance explains four related points:

| Point | What useful guidance must explain |
| --- | --- |
| B1 | A failed synchronous batch leaves none of its database edits committed. Successful batches retain their edits. |
| B2 | Saving can queue an event outside the database. Rolling back database writes does not undo that queue. |
| B3 | Failed batches must not dispatch notifications about undone changes. Events for successful changes must still work. |
| B4 | The earlier API can violate the supported rule. Guidance must explain that conflict and distinguish documented requirements from inference. |

The [full reference](netbox-reference.json) records the evidence, exceptions, serious errors and unresolved questions. Existing cleanup supports the rule; the later correction is not its sole justification. Several implementation techniques may satisfy the rule. An assessor must not demand one particular helper function, claim owner approval or extend these observations to concurrency and actual webhook delivery.

These four points belong to one family. The [HTTPX reference](h06-reference.json) provides a second development family, using the six related decisions already recorded in [H06](../h06-guidance-assessment/README.md). Neither family is untouched qualification material.

## What the rehearsal tests

Seven NetBox scenarios cover a supported guide, a bad admission, a false rejection, an empty draft, a successful correction, exhausted corrections and an unresolved stop. HTTPX provides one further supported example. Expected outcomes are authored explicitly. They are checks of workflow behaviour, not eight independent research results.

The controller also has 15 tests covering malformed citations, missing assessment coverage, tampered candidate identities, limits, timeout recording, terminal runs, forbidden reference disclosure and changes to admitted scope. The recorded container replay uses 49 role invocations and two boundary probes. See [results.json](results.json).

Every invocation starts a fresh container with no network, host mounts or Docker socket. It runs as an unprivileged user, with a read only root filesystem, a small temporary directory and fixed resource limits. Probes attempt an external connection, forbidden writes and reads outside the permitted pack. A marker written into one container is absent in the next.

These checks apply to the trusted replay worker. They do not qualify arbitrary code execution, prompt injection resistance or a live provider connection. The worker receives its authored response alongside the role packet, so this is deliberately not a blinded experiment. No training familiarity claim follows from container isolation.

## Reproduce it on either Windows machine

Install Docker using the shared [local setup guide](../netbox-bulk-error-candidate/LOCAL_SETUP.md), then use Python 3.12 or newer and Node only for the existing project workflow. The replay runs one small container at a time and does not start NetBox, PostgreSQL or Redis.

From the repository root in PowerShell:

```powershell
python -m venv local-runs/phase1-env
local-runs/phase1-env/Scripts/python.exe -m pip install -r research/development/phase1-harness/requirements.txt
docker build -t phase1-replay:dev research/development/phase1-harness
local-runs/phase1-env/Scripts/python.exe research/development/phase1-harness/test_harness.py
local-runs/phase1-env/Scripts/python.exe research/development/phase1-harness/run.py --fetch-sources
```

The optional fetch happens in the trusted setup process before role dispatch. It downloads only pinned public files and verifies their hashes. Existing mismatched files stop the run; they are not overwritten. NetBox retains the root AGENTS.md and all starting revision files in the investigator source manifest. HTTPX uses its Python package, authentication guide and licence. The historical coding task, feature solution, later QA and investigator runtime answers are absent from the working role packets. Assessment receives a separate reference.

If Docker is not on the current shell's path, add its installed `resources/bin` directory before these commands. No separate Linux distribution is required. The laptop still needs its own installation and replay; success on this PC does not qualify the other machine.

Full inputs, outputs and an audit chain stay under the ignored `local-runs/phase1/` directory. The public report contains hashes, source manifests and outcomes, not copies of every upstream file. These hashes support reproduction and detection of later changes to the recorded files; they are not independent attestation of the operator or proof that no other process ran. The local records are not synchronised through GitHub.

The development defaults allow two corrections and at most twelve role invocations. Each worker has a thirty second timeout, 128 MB memory and an 8 MB input limit. The controller accepts at most 128 KB of output; this acceptance check is not a streaming disk quota. Model usage and price fields are unavailable, and the report records zero model calls. These limits are development settings, not ratified experimental budgets.

## What comes next

Add the actual provider adapter and test it without spending money first. Unlike this replay, it must send only the declared role input, never a fixture answer. It must enforce allowed destinations, credentials, request limits and usage recording outside the roles. The [tool review](tooling-review.md) identifies candidates to reuse.

Then fix model settings and qualification criteria, prepare separate assessment families and seek the required authorisation for model spending. The live verifier and assessors still need qualification before collecting a guidance result. Coding execution and the interactive checker remain work for later phases.
