# Does this guide add something useful?

16 September 2026. One investigator-assisted exploratory guide. Assessor qualification and fresh-bank preparation are paused by user agreement. This is a smaller diagnostic alongside the formal plan, not a completed controlled Phase 1 run.

## Source check

Twelve starting-revision files were retrieved and verified against the existing source manifest. Later implementation patches were not needed to justify the guide. The author had already read the historical investigation, reference and reproduction results; the guide therefore cannot demonstrate independent discovery. Claim review was performed by the same investigator, without a qualified assessor, separate Fable review or independent human certification.

| Guide claim | Evidence status | Check and limit |
|---|---|---|
| Failed bulk updates keep no edits | Explicit documentation | Starting-revision API guarantee; also observed in the earlier reproduction. |
| Database rollback can leave queued events | Cross-file inference, backed by prior runtime evidence | Signals modify request-context storage; request completion flushes it. The reproduced mixed batch retained a job despite database rollback. |
| Remove consequences of aborted work; preserve successful events | Supported scoped inference | Earlier cleanup convention and all-or-nothing contract support it. Whole-queue clearing is not justified for unrelated or partially committed work. No owner approval is inferred. |
| Preserve snapshots and saved-object permission checks | Direct source observation and regression advice | Both appear in the starting update path. Permission failure behaviour was not exercised by the prior runtime check. |

No unsupported factual claim was identified in this scoped review. This is not a completeness or reliability score. The precise response envelope remains open; this guide cannot resolve it from unrelated later conventions.

## What the existing runtime evidence tells us

The [11 September reproduction](../../development/netbox-bulk-error-candidate/reproduction.md) exercised real NetBox requests with PostgreSQL and Redis. It is reused here, not rerun. All failed batches restored the database and left no new change records. Queued jobs differed:

| Scenario | Starting revision | Feature merge | Later QA |
|---|---:|---:|---:|
| Both edits valid | 2 | 2 | 2 |
| Valid then invalid | 1 | 1 | 0 |
| Invalid then valid | 0 | 1 | 0 |
| Both invalid | 0 | 0 | 0 |

This demonstrates that the guide addresses a real failure mode and that database-only checks would miss it. The fault already existed before the feature. The later QA is a historical comparator with other changes, not proof that a particular helper caused the improvement. Jobs were inspected in the queue; no worker delivered a webhook.

## What the guide adds

The useful addition is a concrete obligation to review two effects of a save: database changes and queued events. It gives the implementer source locations, a cleanup boundary, a successful-operation control and two mixed processing orders to test. These are actionable review and test decisions.

The transaction guarantee alone is ordinary documentation extraction. The more useful connection crosses the signal, context storage and request-completion code. However, the previous investigator write-up already made that connection. This turn packages established research into an implementation guide; it does not discover a new rule or show that an ordinary coding agent would miss it.

## Effort and decision

Incremental work was one interactive investigator turn: recheck twelve pinned files, write one guide, compare its claims with sources and reuse the saved runtime observations. No extra drafter/assessor process, model batch, application run or new harness was started. This conversation itself consumes model usage; its incremental tokens, credits and active working time were not separately metered. The earlier source investigation and runtime reproduction are substantial sunk preparation and must not disappear from a later cost comparison.

**Decision:** the guide is specific enough to justify one small exploratory task-use check. There is still no evidence that it improves coding quality, saves time or pays for preparation. Before spending effort on more qualification infrastructure, test whether a proposed implementation review with this guide actually checks the event queue and the successful path. An already exposed historical example can test usability, but not provide an unbiased DIRECT-versus-GUIDE effect estimate.

Keep the current qualification results closed and unchanged. Do not start another fresh bank merely because this worked guide is readable. If the next check adds little beyond ordinary review, stop or simplify the interpretation-layer approach.
