# Using the guide to review a real implementation

16 September 2026. **Verdict: request a change to failed-batch event handling.**

Reviewed the historical feature merge `6068f417876e79b6d588bd8b05a7a4e515378b51` against the [worked guide](README.md). This is an already exposed development case, reviewed by the same investigator who wrote the guide and knows the previous findings. It tests whether the advice translates into concrete review actions; it cannot measure improvement over ordinary review.

## The actionable finding

**A failed bulk update can still queue a notification describing a change that was rolled back.** In [`perform_bulk_update`, lines 273–292](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/api/viewsets/mixins.py#L273-L292), valid items are saved while invalid items contribute errors. The final error branch marks the database transaction for rollback but leaves the request's event queue untouched. The caller then returns HTTP 400 normally at lines 253–265.

The [save signal](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/core/signals.py#L152-L155) adds events to request-context storage. The [request context](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/context_managers.py#L18-L30) flushes that queue on normal completion. Database rollback does not remove these dictionary entries. This is the specific missing obligation identified by guide sections 2 and 3.

**Requested repair:** on this synchronous validation-error path, discard events belonging to the aborted batch after rollback and before request completion. Preserve the successful path. The existing `clear_events` signal clears the entire queue, so use it only after establishing that the queue contains solely the aborted work; otherwise retain unrelated events. Keep snapshots, serializer validation and `perform_update`. This is a repair requirement, not an implemented or runtime-validated patch. Exception paths and background jobs need separate review before a broader fix.

## Applying each part of the guide

| Guide instruction | Concrete review result |
|---|---|
| Keep the batch atomic | The loop uses one outer transaction and marks it for rollback when errors exist. Saved observations show no committed edits or change records for failures. |
| Check the event queue separately | **Fails:** both mixed valid/invalid cases leave one queued webhook job. |
| Scope cleanup and preserve success | There is no cleanup on the identified failure path. The repair must preserve the two jobs in the all-valid control; unconditional queue clearing would violate this requirement. |
| Preserve normal update behaviour | Snapshots, per-item serializer validation and `perform_update` remain in the loop. The latter still saves and checks saved-object permissions. Permission failure behaviour was not exercised. |
| Identify failed items | In all three saved failed scenarios, response error IDs match the invalid input IDs. |

## Existing checks that make the finding concrete

Rechecked the four saved [feature-merge observations](../../development/netbox-bulk-error-candidate/results/feature.json); no requests were rerun.

| Scenario | Committed edits | New change records | Queued jobs: observed / required |
|---|---:|---:|---:|
| Both valid | 2 | 2 | 2 / 2 |
| Valid then invalid | 0 | 0 | **1 / 0** |
| Invalid then valid | 0 | 0 | **1 / 0** |
| Both invalid | 0 | 0 | 0 / 0 |

Seven feature-revision files match the existing source manifest. Both mixed processing orders matter: the implementation continues saving after validation errors. The successful case prevents accepting a fix that merely disables all events. Jobs were queued, not delivered by a worker. The fault predates this feature; the feature expands the affected ordering, as the [earlier reproduction](../../development/netbox-bulk-error-candidate/reproduction.md) records.

## Decision

The guide is actionable in this case: it yields a precise change request, a bounded repair requirement and checks that would reject both the existing defect and unconditional event suppression. That meets this small usability checkpoint. It does **not** establish that the guide caused discovery, outperformed a capable reviewer or repaid its preparation cost; the known defect informed the guide itself.

Keep qualification paused. The next informative step, if continuing, is a small task with a different, previously unreviewed change, comparing ordinary review with review using guidance. Repeating this known case or adding qualification infrastructure would not resolve the remaining value question. No new model allocation, application execution or comparison design is authorised by this review.
