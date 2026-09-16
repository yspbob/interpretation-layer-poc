# NetBox bulk edits: keep failed changes out of notifications

**Worked guide, 16 September 2026.** Applies to synchronous bulk updates at NetBox revision `d13c98b9ea8c55dafdcdecbf3058a731814a7ead`. Written with investigator knowledge of an existing development case; this is not a blind model result.

## The task

Add item-specific validation errors to a bulk PATCH request containing distinct, existing object IDs. Keep the documented all-or-nothing update behaviour. This bounded task adapts the existing historical feature case; it does not specify a new response envelope or duplicate-ID policy.

## Guidance to use while implementing

### 1. Reporting several errors must not permit partial commits

If any item fails, none of the batch's edits should remain committed. Collecting errors changes what the caller learns; it does not change the transaction guarantee. Preserve one transaction boundary covering the batch's writes. This is an explicit [API contract](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/docs/integrations/rest-api.md#L664).

### 2. Check queued events separately from database rollback

The write path has two effects:

- The save changes database state and creates change records.
- The signal handler also adds an event to a dictionary held in the request context. When that context completes normally, it passes queued events to the configured processing pipeline.

The second effect is not a database write. Returning an error response after a rollback can still reach that normal request-completion path. Therefore, before the request finishes, discard events belonging to the undone changes. A test that checks only the response and database can miss this failure.

Trace: [save signals](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/core/signals.py#L125-L155) → [enqueueing](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/extras/events.py#L115-L157) → [context storage](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/context.py#L10-L12) → [request completion](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/context_managers.py#L11-L31). The required cleanup is an inference across these sources and the batch contract.

### 3. Scope cleanup to what was undone

The project already has a [queue-clearing signal](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/core/signals.py#L269-L276), used by an [aborted bulk UI operation](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/views/generic/bulk_views.py#L1122-L1129). Its handler clears the entire request queue. Use it only where that queue belongs to the aborted work; do not turn this into a rule to delete unrelated events after every error.

A successful batch must retain its normal events. A different implementation that prevents dispatch of rolled-back changes could also satisfy the rule; the sources do not require copying one particular helper.

### 4. Preserve the normal update path

The existing [bulk loop](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/api/viewsets/mixins.py#L237-L249) takes snapshots, validates each serializer and calls `perform_update`. That [update method](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/api/viewsets/__init__.py#L320-L336) saves and validates the saved object against permissions. Replacing this path with direct writes requires accounting for those behaviours. This is a source-based regression concern; the existing reproduction did not test permission failures.

## Minimum behavioural checks

For the existing fixture with two sites and one matching webhook rule:

| Scenario | Committed edits | New change records | Queued webhook jobs |
|---|---:|---:|---:|
| Both edits valid | 2 | 2 | 2 |
| Valid item processed before invalid item | 0 | 0 | 0 |
| Invalid item processed before valid item | 0 | 0 | 0 |
| Both items invalid | 0 | 0 | 0 |

Make the fixture exercise both processing orders. Also check that errors identify the failed items. The event counts above belong to this configured fixture, not every NetBox save.

This guide does not establish background-job, concurrency, nested-transaction or remote-delivery behaviour. Exact response formatting and broader API compatibility need their own task decisions.

[Source check, existing observations and usefulness review](REVIEW.md)
