# NetBox batch rollback: runtime reproduction

11 September 2026. Completed local investigator reproduction: three revisions, four request scenarios per revision. No model was called.

## The question

If a batch edit fails, does NetBox discard both the database changes and the notifications prepared for those changes?

The experiment sends four kinds of request to each historical revision. A successful request is included to confirm that the test can observe normal saves and event processing. The database is recreated for each revision.

## Observations

Every failed request in all three runs returned HTTP 400, left both records unchanged and retained no new change log records. Every successful request returned HTTP 200, saved both records, created two change log records and queued two webhook jobs.

The difference is in the queued jobs after a failed request:

| Request | Before the feature | Feature merge | Later QA |
|---|---|---|---|
| Both edits valid | 2 jobs, as required | 2 jobs, as required | 2 jobs, as required |
| Valid edit, then invalid edit | 1 incorrect job | 1 incorrect job | No jobs |
| Invalid edit, then valid edit | No jobs | 1 incorrect job | No jobs |
| Both edits invalid | No jobs | No jobs | No jobs |

For the incorrect jobs inspected, the payload said the record was edited even though the database had restored its original description. The associated snapshots also described the undone change.

The issue therefore existed before the feature. The feature expanded it: processing continued after an invalid item, allowing a later valid item to queue an event before the batch was rolled back. It would be wrong to describe every observed failure as introduced by that feature.

The later QA revision eliminated the incorrect jobs in both mixed batches while preserving successful writes and their events. All twelve request scenarios completed. Three observations violated the scoped event rule; those failures remain in the results. They are failures of the tested historical behaviour, not model outcomes.

## What ran

The probe used NetBox's real Django request routing, middleware, serializers, model saves, signal handling and event pipeline. PostgreSQL stored the records. Redis stored the actual queued webhook jobs. These components were not replaced with stubs. Requests came through Django REST Framework's test client, authenticated as a test superuser.

Four request scenarios ran per revision. They are related checks of one decision family, not four independent experimental cases. The script checked HTTP responses, final database values, change log counts and successful event processing. Rule violations in a failed batch are recorded as observations rather than hidden by calling the entire probe a success.

No worker executed the webhook jobs. The target URL was loopback only, and the containers used an internal network without published host ports. The measured endpoint is queued dispatch, not an actual notification received elsewhere. Authentication, permissions, bulk creation, deletion, background processing and concurrent requests are outside this check.

## Reproduction and evidence

Use the [local setup instructions](LOCAL_SETUP.md) and [PowerShell runner](run-local.ps1). The [probe](reproduce.py) is identical across revisions. It uses the pinned source revisions listed in the candidate record and a separate disposable database for each. Source files implementing the behaviour are unmodified.

The complete observations are published for the [starting revision](results/starting.json), [feature merge](results/feature.json) and [later QA](results/later-qa.json), with a [runtime manifest](results/runtime-manifest.json). All three used Python 3.12.14, PostgreSQL 17.11 and Redis 7.4.11. The first two had identical installed Python package versions, including Django 6.0.6. The later QA used its own requirements, including Django 6.0.7.

The local run records the probe and configuration hashes, Python and installed package versions, source revision, API responses, database rows, job payloads and snapshots. The Docker image records include service digests. A future build can resolve different transitive dependencies or base image updates; compare these records before treating reruns as the same environment. The run does not claim byte identical image builds.

The later QA version is a historical comparator. Its broader patch and dependency changes do not isolate the effect of a single helper function, and its code is not the only acceptable repair. The scoped expected behaviour comes from the earlier evidence described in the [candidate record](README.md).

## Implication for the POC

This is a concrete development reference for the difference between undoing database writes and cancelling their queued consequences. It does not establish that an interpretation layer discovers the rule more reliably than an ordinary agent. Both can read the earlier documentation, cleanup convention and implementation.

The case also shows why a guide cannot simply declare existing behaviour to be the rule. One path violated a guarantee supported elsewhere in the project. The assessment must preserve that disagreement and the evidence for resolving it.

The next Phase 1 work is to turn the scoped claims into explicit guidance assessment records, then implement the restricted drafting, verification and independent assessment path. Keep this public family in development, and use separate material for qualification. No new model spending or experimental runs are authorised by this reproduction.
