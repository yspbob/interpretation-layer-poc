# Proposed next case: bulk-update preview

16 September 2026. **Discussion proposal only. No selected task, changed protocol or new experimental allocation.** The user identified the absence of a suitable comparison case as a blocker and asked to resolve it. The two-screen allocation remains closed.

## Concrete candidate

Consider adding a preview mode to a NetBox bulk-update operation. The proposed user-visible contract is to validate proposed edits using the applicable ordinary update and permission checks, report item errors, and leave no persisted edits, change records or notifications from the preview. A normal non-preview update must retain its existing behaviour. Exact API, supported inputs and error semantics need inspection of the pinned source before this becomes a selected request. The absence of an existing equivalent feature has not been verified.

## Why this case is worth checking

The existing [implementation review](../netbox-bulk-guide/IMPLEMENTATION-REVIEW.md) records a concrete separation between database rollback and request-context notification state: both mixed valid/invalid scenarios leave a queued job despite no committed edits or change records. The successful control retains two jobs. Those observations concern the historical error-reporting change, not this proposed preview feature, and do not demonstrate an agent failure on the new task.

This motivates a different selection criterion: a small product change whose correctness depends on an evidenced relationship across transaction, validation, permission and event-handling code. Simply increasing the number of requirements in another library helper has not yielded an eligible failure in our two screens. A repository guide could make the relevant relationships easier to find; that is a hypothesis to test, not an observed advantage.

Both coding conditions must receive the complete product contract and the same underlying source access. Do not hide the no-side-effects requirement, shorten only the ordinary attempt, require an arbitrary implementation, or engineer a low score. Tests must accept any implementation satisfying the contract. Guidance can explain how existing project mechanisms interact without supplying a task-specific patch.

## Exposure and cost limits

The investigator and project already know the NetBox event-queue finding and the worked guide. This candidate is inspired by that exposed mechanism and cannot be described as an untouched decision family or independent confirmation. The previously written guide was informed by the known defect. Do not pass it off as a newly blind reconstruction. Any later guide procedure must explicitly retain these limitations and keep the new request and evaluation out of a task-blind author's context.

Before selection, inspect the pinned source to establish whether the feature is absent, whether the contract has a bounded implementation, and whether the available local runtime can evaluate real side effects without substantial new setup. Reject this candidate if it depends on unresolved product semantics or disproportionate environment work. No validation of that readiness is claimed here.

The recommendation is to prepare one concrete case for review, not to extend the completed screen or search indefinitely for a failure. A new fixed allocation would need a separate execution decision and must remain within the user's existing-credit ceiling. An unguided pass remains a valid possible result. Do not promise a low baseline or a positive guidance result.
