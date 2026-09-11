# A stronger candidate: errors in a NetBox batch edit

11 September 2026. Candidate NB-BULK-01. Public investigator research, not a frozen task, an agent input pack or a model result.

## The task in plain language

NetBox keeps records of network infrastructure. Its API lets a client edit several records in one request. A user asked for an error against each item that failed, so they could understand what to correct without repeatedly submitting the batch.

Changing that response looks straightforward. The harder part is preserving what happens around the edit. If one item fails, the database must undo the whole batch. NetBox also prepares notifications while records are being saved. Those notifications must not announce changes that the database has undone.

This is the leading candidate for further case development. HTTPX H06 remains useful for developing the assessment machinery, but it no longer determines which repository we investigate first for a substantive comparison.

## Why this is worth investigating

The API guide clearly states that a batch update either succeeds entirely or changes nothing. That fact is documentation visible. The more demanding question is how to preserve it when work also happens outside the database transaction.

The starting code queues events in memory as records change. Another part of the application sends those events for processing when the request finishes. Rolling back the database does not, by itself, empty that queue. Other NetBox write paths already clear queued events when they abort a transaction.

A useful guide would connect these facts and explain the boundary of the database guarantee. It would need to identify which operations require event cleanup and which successful operations should still produce events. Merely advising the agent to use a transaction would be incomplete.

There is no hidden fact that only the interpretation layer gets to read. The ordinary agent receives the same permitted documentation, code and repository instructions. It may make the connection itself. Equal performance would be a valid result.

## Historical sources and starting point

The feature request is [NetBox issue 20054](https://github.com/netbox-community/netbox/issues/20054), opened on 8 August 2025. [PR 22646](https://github.com/netbox-community/netbox/pull/22646) implemented it and merged on 15 July 2026. [PR 22901](https://github.com/netbox-community/netbox/pull/22901), merged on 14 August, subsequently corrected several problems, including events being dispatched after writes were rolled back.

The proposed starting revision is `d13c98b9ea8c55dafdcdecbf3058a731814a7ead`, the first parent of feature merge `6068f417876e79b6d588bd8b05a7a4e515378b51`. This is the source immediately before that merge, rather than the inventory snapshot or the PR API's base field. The later QA merge is `3793160eba4d54070552eacfc1502027a7e042c1`.

The [source manifest](source-manifest.json) records the exact files retrieved, revisions and content hashes. The complete starting tree listed one AGENTS.md file, at the root. It must remain available in matched inputs. The inspected material does not justify calling this an entirely undocumented rule.

## What the earlier evidence supports

All links in this table point to the proposed starting revision. Later fixes are not used to invent earlier requirements.

| Evidence | What it establishes | Limit |
|---|---|---|
| [API guide: bulk updates](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/docs/integrations/rest-api.md#L662-L664) | A failed update aborts the batch without retaining any of its edits. | This alone does not explain the event queue. |
| [Save signal handling](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/core/signals.py#L125-L155) and [event enqueueing](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/extras/events.py#L115-L157) | Changes can create an event in memory during the write path. | Delivery depends on event support, configuration and later processing. |
| [Request event tracking](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/context_managers.py#L9-L31) | Queued events are flushed when this request context completes normally. | A source trace does not exercise the full request stack. |
| [Existing queue cleanup](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/core/signals.py#L269-L276) and [bulk UI cleanup](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/netbox/netbox/views/generic/bulk_views.py#L1122-L1129) | The project already treats aborted writes as a reason to discard queued events. | This supports a scoped rule, not a universal instruction to clear every queue on every error. |
| [Event rule documentation](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/docs/features/event-rules.md) | These events can trigger webhooks, scripts or notifications about object changes. | It does not certify a maintainer's unrecorded intentions. |

The main candidate rule is therefore supported by connecting documented batch behaviour, implementation evidence and an existing cleanup convention. Record those sources separately in any eventual claim assessment. Do not label the whole rule as purely inferred from code.

The original bulk update path also takes snapshots and calls the normal update method, which checks permissions against the saved object. These are relevant neighbouring behaviours, not several newly independent cases. They should inform a later regression review without turning the first case into an assessment of every bulk API feature.

## What the historical change adds to the investigation

At the feature merge, `perform_bulk_update` saves valid items, gathers validation errors, marks the transaction for rollback if errors exist, and returns normally. The caller produces an error response. The inspected event tracking code still flushes the queued events after normal request completion. The later QA change explicitly addresses this path by discarding events on rollback.

This is a source supported failure mechanism and an upstream reported correction. We have not reproduced the fault in a running NetBox installation. We also have not established that the feature introduced every affected failure: earlier exception handling paths may already have had related problems. Do not describe this as a measured regression or assume the later implementation is the only correct solution.

The feature PR's description and implementation differ on validation sequencing. Its final code validates and saves each item in turn, so later validation sees earlier writes. The PR description is useful historical context, not an authoritative algorithm specification.

## Boundaries of a fair case

Focus further development on synchronous bulk updates. Creation, deletion and background jobs need separate scope decisions and evidence. The historical request includes wording that could suggest partial success; reconcile this with the existing documented batch guarantee before freezing a task. Exclude any unresolved central requirement from scoring.

The later QA also introduced response conventions and rules for duplicate or missing identifiers. Do not silently backdate those decisions into the expected answer. Keep the historical feature request and implementation in the investigator record until a task brief has been checked against the earlier contract.

The drafter and verifier must not receive this record, later patches, the selected task or scoring material. Prepare a task neutral source pack with the earlier documentation and applicable instructions. The coding agent can receive the eventual task, but no historical solution or later QA answers. Assess lawful alternatives by behaviour, not by whether they copy the upstream helper.

This public discussion exposes the candidate family. If it is used to develop prompts or assessment examples, keep it in development and qualify the method on different families. No untouched qualification claim is made here. Choosing a known problematic change is also deliberate selection: success on it would not show how frequently ordinary tasks benefit from the layer.

## Work completed and next step

The feature, its actual starting parent and the later QA change have been located. Selected earlier documentation and source paths were inspected and hashed. This establishes a plausible task and a reason to investigate it. No NetBox integration test, model call, guidance preparation, cost measurement or isolation test ran.

Next, reproduce the relevant behaviour in the pinned NetBox environment with PostgreSQL and Redis. Compare the starting revision and feature merge, checking database state and event dispatch separately, with a successful batch as a control. Keep outbound webhook delivery local to the test environment. Establish what already failed before the feature, and confirm the reference can distinguish a complete fix from a database only fix.

Only after that check should this candidate become a worked development case. Phase 1 still assesses guidance; the historical coding task establishes a plausible later use. One candidate is not evidence of repeated guide reuse, a final repository allocation or a sufficient trial sample. Additional compatible tasks must be reserved before preparing guidance intended for their comparison.
