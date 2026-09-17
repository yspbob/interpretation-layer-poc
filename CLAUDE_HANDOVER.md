# Handover to Claude: interpretation-layer POC

Prepared 17 September 2026. This is an investigator/research handover, not an input for a blinded experimental agent. It contains the current position without requiring the earlier conversation.

## Start here

The immediate blocker is finding a concrete software-change task on which repository guidance has a plausible opportunity to help a capable coding agent. The user asked Claude/Fable to research candidates. A standalone research brief is already prepared at `research/exploratory/fresh-task-comparison/FABLE-CASE-RESEARCH-BRIEF.md`. Follow it if available; the essential assignment is also summarized below.

Do not restart qualification, repeat the completed screens or launch a coding comparison. This handover transfers context and the research task; it does not open a new experimental allocation.

## What the project is testing

The interpretation layer reconstructs evidence-backed guidance about a software system: constraints, relationships between components, established patterns and exceptions. We want to know whether providing that guide improves subsequent engineering work enough to justify its preparation and checking costs, compared with a capable agent using the same repository directly.

The formal plan has three phases: reconstruct guidance, test its use, then test interaction during work. Formal qualification and further infrastructure work are paused after substantial preparation. No model assessment role is qualified, and there have been zero qualified controlled pilot guidance runs. The exploratory work below is real completed work, but is separate from that formal trial.

## Completed results to preserve

| Work | Observed result | What it establishes |
|---|---|---|
| NetBox worked guide and implementation review | Mixed valid/invalid bulk updates rolled back database edits but still queued a notification; the successful control retained normal notifications. | A concrete cross-component obligation. The investigator already knew the defect when writing the guide, so this is not independent discovery or comparative benefit. |
| FC-01: one new HTTPX task, one neutral guide, two coding attempts | Guided and unguided attempts both passed 9/9 acceptance checks and 104 relevant original regressions. | No observed correctness advantage on this task. Preserve the null result and preparation cost. |
| Two further unguided HTTPX screens | First passed 11/11 acceptance checks; second passed 12/12. Each passed 199 relevant original regression cases, with one upstream skip and two predeclared exclusions. | Neither qualified for the conditional guidance comparison. The allocation stopped after two sessions; no new guide or comparison followed. |

The exploratory coding contexts used Astra High and ten-minute supervised limits. The previous guide limit was five minutes and 600 words. These historical limits are not a validated budget for a new repository. Relevant tests passed; full correctness, the full upstream suite and general guidance effectiveness were not established. Contexts were fresh, but inherited general project instructions and lacked an operating-system read boundary. The investigator audited recorded access; no independent certification is claimed.

The user correctly challenged the lack of room to measure improvement when ordinary agents pass everything. We agreed to a bounded screening approach and to retaining all outcomes. A low score such as 5/10 is not itself a valid selection criterion, and indefinite searching for a failure is not authorized.

## Immediate research assignment

Find up to three source-backed candidate tasks and recommend one. Prefer a small meaningful change whose correctness requires connecting repository-specific facts across components. Examples include transactions and events, cache invalidation, authorization across entry points, or cancellation and resource ownership. Complexity alone is insufficient.

For each serious candidate establish:

1. A concrete user need, repository URL, exact baseline commit and primary-source links to relevant code, tests and documented contracts. Label an investigator-authored request as such; do not infer maintainer approval.
2. Whether the requested feature is absent at that baseline and what existing behaviour must remain compatible. Exclude unresolved central requirements.
3. A specific reason neutral repository guidance could help. Identify supporting sources without writing the guide or a patch. Predicting that an ordinary agent might miss a relationship is a hypothesis, not an observed failure.
4. A small behavioural evaluation matrix, including a working normal path, a meaningful failure/boundary path and preservation of existing behaviour. Accept different valid implementations. Timeout, setup failure, missing prose or cosmetic issues alone are not useful eligibility criteria.
5. A practical local evaluation route, dependencies, setup burden, prior exposure and uncertainty. We use Windows; do not assume a Linux runtime, containers, databases or credentials are available. Do not build a large new harness merely to justify a candidate.

Return **CASE-RESEARCH.md** with the ranked shortlist, evidence, evaluation route, limitations and one recommended next action. Separately return **CANDIDATE-TASK.md**, a standalone coder-facing request for the recommendation, with full requirements and scope but no predicted failure, solution sketch, guide, historical fix or evaluator fixtures. If no suitable candidate is supported, say what is missing rather than padding the list.

Both experimental coders must receive the full product contract and identical underlying source access. Do not withhold an obligation from the unguided coder, make only its time limit restrictive or smuggle a task-specific answer into the guide. Guide preparation must exclude the selected task, its solution, screening failure and evaluator. A researcher exposed to those materials cannot subsequently act as the task-blind guide author in this context.

A later approved screen would use fixed inputs, tests and stopping rules. On an eligible failure, the comparison must use fresh guided and unguided attempts; the screening failure is not the comparison baseline. Retain every screened success, failure, incomplete attempt and cost. Public repositories may be familiar to models; a new request does not prove an unseen decision family.

## Optional lead, not a selected task

Consider a NetBox bulk-update preview that runs applicable ordinary validation and permission checks, reports item errors, and leaves no persisted edits, change records or notifications from the preview. Normal updates must retain their behaviour. Feature absence, exact API semantics and evaluation feasibility remain unverified. Reject the idea if it is already implemented, insufficiently useful or disproportionately costly to prepare. Other projects are welcome.

The lead is motivated by an already exposed NetBox rollback/event-queue relationship, not a newly discovered failure. Source starting points are [bulk updates](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/api/viewsets/mixins.py), [save signals](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/core/signals.py), and [request completion](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/context_managers.py). Do not present the known defect or existing worked guide as fresh blind evidence.

## Authorization and working style

- The current requested work is research and preparation. All previous experimental allocations are closed. Unused conditional sessions are not transferable to another case.
- The user's spending ceiling is the existing available credits, with no top-up or API fallback. An earlier 5% stop preference was retained as a reserve for the last allocation. Historical approval to spend added credits is not blanket authorization for new runs. Do not purchase credits, redeem a reset or dispatch model trials from this handover.
- The user wants a concrete case and is frustrated by excessive preparation and divergence. Keep the investigation bounded, report evidence rather than speculation, and push back when a proposal would weaken the comparison. Do not rebuild the qualification machinery.
- Website body changes are banked. Do not release them as part of research. Keep results, proposed directions and unvalidated controls clearly distinguished.

## Repository access and continuity

Public project: `https://github.com/yspbob/interpretation-layer-poc`.

Current local checkout: `C:/Users/yaros/Documents/Codex/2026-09-08/ple/interpretation-layer-poc`.

Private evidence repository: `https://github.com/yspbob/interpretation-layer-poc-private`, with the last recorded local root `C:/Users/yaros/Documents/Codex/poc-private`. Private evidence is unnecessary for initial public candidate research. Never copy raw sessions, evaluator fixtures, sealed cases, account records or credentials into the public project or a blinded agent's context.

**The public remote is behind this local checkout.** The freshness check on 17 September found 18 unpublished commits before this handover, with no incoming changes. The latest preceding local commit is `a140372` (Fable research brief). Automatic approval review blocked publication because earlier unpublished history contains account/credit metadata. Do not bypass this block, push through a different route, reset the local history or claim the remote has these documents. A fresh remote clone alone is not current; use this local checkout or the supplied handover/brief. Resolving the publication issue is separate work.

Private evidence was last reported successfully published at `0e2e0ad36d87369e656937788fef614487e5091c`. Its manifest then covered 16,913 files and 217,819,440 bytes. Private freshness and runtime readiness have not been rechecked for this handover.

If working in the checkout, read `AGENTS.md`, `PROJECT_STATE.md`, then `preregistration/plan/working_plan_2026-09-05.md` (current plan `.34`, especially section 1A). Read dated status carefully: older setup instructions and historical next steps must not override the latest completed results. `START_HERE.md` covers setup on another machine; it is not permission to resume qualification. Recheck tools and environments on the actual host rather than assuming saved paths are operational.

Before edits, use `node scripts/project-sync.mjs start` and preserve unfinished work. For Git ownership errors on this known shared checkout, a command-local `safe.directory` setting has been used; do not weaken global ownership checks. Update project state after meaningful work, explicitly stage reviewed files and commit locally. Normal publication uses the sync helper, but the existing public approval block must first be resolved. Private changes require their own sync, immutable-evidence checks, refreshed transfer manifest, explicit commit and private publish helper. Do not alter previous freezes or outputs.

## File map

All paths below are relative to the public project root:

- `research/exploratory/fresh-task-comparison/FABLE-CASE-RESEARCH-BRIEF.md`: full standalone research assignment.
- `research/exploratory/fresh-task-comparison/NEXT-CASE-PROPOSAL.md`: optional NetBox preview rationale and limitations.
- `research/exploratory/fresh-task-comparison/README.md`: completed FC-01 comparison.
- `research/exploratory/fresh-task-comparison/SCREENING-RESULT.md`: completed two-screen outcome.
- `research/exploratory/netbox-bulk-guide/IMPLEMENTATION-REVIEW.md`: exposed NetBox finding and saved observations.
- `research/implementation-takeaways.md`: implementation implications; recent entries IL-041 and IL-042 concern screening and selection.

**First useful action:** research the candidate shortlist under the brief, or review the returned research if the user has already obtained it. Establish one well-supported, runnable case before preparing another experiment. No new case is selected yet.
