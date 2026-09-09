# Plan changes reconciled on 5 September 2026

Current plan: **pilot-draft-2026-09-09.4**. Status: working redesign, not a new ratified preregistration.

## Historical comparison and clearer review explanation — 9 September 2026

The user clarified that these are backtests and that the actual implementation can itself violate the guidelines. The agreed assessment must score both historical and agent implementations for task correctness and compliance with independently established, applicable guardrails. Avoiding a historical violation while completing the task correctly counts in the agent's favour; matching the original code is not the objective. The historical implementation remains a comparator, not a fourth treatment. Exact points, weights and aggregation remain open and must be set before scored runs.

Sections 3, 7, 9 and 9A and the judging-contract addendum record case preparation, information boundaries, paired criterion reporting and required qualification examples. Historical exceptions and unresolved evidence remain explicit. H04 is still authored development material; no historical comparison, model score or new validation has been produced by this release.

The website replaces the ambiguous reference-answer wording and explains the two assessment dimensions. The dense review explanation is now a three-row table in the proposed comparison section: every group gets review at matched checkpoints and correction limits; INTERACT adds structured questioning to the guidance available in GUIDE. This presentation change preserves the existing matched resource limits and ordinary-review controls. Both pages and the plan downloads are aligned in this authorised release. During review, the user corrected the earlier voice preference: the POC informs readers about its process and the decisions behind it, while the playbook makes proposals and conclusions. Both pages now use factual process language, with named actors and explicit status, rather than copying the playbook’s first-person voice. This supersedes the earlier narrative-voice preference; the playbook itself is unchanged.

## Agent containment requirement — 9 September 2026

The user raised the Hugging Face incident as a design concern, banked the proposed requirements, and then authorised this release. Section 8 now requires isolation for each role and run, communication through an external controller, preinstalled read-only dependencies, protection of evaluation and enforcement, adversarial boundary tests and externally enforced stops. It explicitly covers indirect internet access and unauthorised messages through supporting services, drawing on the linked primary incident accounts.

This is an agreed requirement for the runner before model calls, not implemented or validated containment. The existing H04 file broker does not meet it. Component contracts and both website views reflect that status. No model run, new containment test or effectiveness result is claimed. Tested escape paths and residual limitations must be reported; absolute prevention is not promised. The next substantive step remains the model-free isolated runner, now subject to these requirements.

## Narrative voice and scope rationale — 9 September 2026

The user asked to bank comments and apply them only on an explicit instruction, then requested a review and release of both pages using the playbook's language. The live playbook uses first-person singular for the author's own recommendations and judgement, declarative or named-actor prose for mechanisms, and plural narration where an actual team is involved. The Experiment and Progress & findings pages, including shared examples and detail panels, now follow that distinction without attributing automated preparation checks to personal human review.

This release also applies the banked scope-note revision: the first POC minimises dependence on maintainers, organisational approvals and ongoing operational involvement. Later iterations could involve owners or test maintenance if needed to answer remaining questions. Evidence verification still does not establish owner approval, guidance stays frozen within a matched comparison, and maintenance is outside the current pilot. This is editorial and scope-rationale clarification; no experimental condition, outcome or qualification status changed. Future comments remain banked until an explicit request to apply them.

## Two connected cycles — 9 September 2026

The user identified that consecutive boxes conflated drafting/approval with usage, and raised the distinction between the first preparation pass and ongoing maintenance. The explanation now separates the two cycles, connects them through versioned approved guidance in the full proposal, and shows evidence from use returning for review. Initial preparation establishes a baseline; later maintenance rechecks affected claims. It does not imply automatic approval or rewriting guidance during a task. The page explicitly distinguishes the full proposal from this pilot's evidence verification and frozen guidance. This is a presentation and scope clarification: no maintenance experiment, owner participation, new experimental condition or result has been added. The isolated role runner remains the next substantive research task.

## Development milestone — 8 September 2026

The user requested continuation of the POC, then asked to stop after the next step and continue tomorrow. Contracts v0.1 and the public H04 response-lifetime case are now implemented as a scripted development rehearsal. All 25 candidate/scenario verdicts matched prewritten expectations; two valid implementations passed overall, two cleanup errors and unfinished work failed. Six control checks and 71 file-broker denials passed. These results establish the narrow fixture and control behaviour, not model judgement, independent qualification or benefit.

The contracts make development defaults explicit: scoped claim admission with exceptions; reject versus unresolved; acceptance on a second correction, terminal exhaustion and unresolved; matched ordinary-review checkpoints; and case scoring in which confirmed failures dominate, missing evidence stays insufficient and incomplete work remains a failure. Hashed documentation-visible role packs and anonymised final-judge inputs are inspectable. Whole-family development exposure, no independent human review and the absence of OS/network isolation are recorded. These are working implementation choices, not user-ratified numerical gates or a frozen endpoint. No scored model outcome was inspected, and zero model calls were made.

Next implement model-free isolated role dispatch and checkpoint enforcement. Do not launch it in the background after this save. Qualification settings and independent family coverage remain open.

## Publication update — 8 September 2026

The user requested the current explanation and progress website on the POC GitHub repository, accessible as a rendered web page. Publish a self-contained static build through the repository's existing GitHub Pages setting, with both routes and evidence downloads. Preserve the earlier status page as history. The website's experimental content and results status are unchanged. The source and rendered downloads carry the same working plan; the separate Sites preview's access is unchanged.

| Change | Recorded status | Effect on the working plan |
|---|---|---|
| Validate the layer's added value rather than assume it is necessary. | Study objective from the user; bounded technical claim in the working design. | Separate guidance quality, downstream benefit, interaction and cost; leave universal necessity unproved. |
| No accessible project owner to certify newly constructed rules. | User constraint. | Remove maintainer recruitment as a prerequisite; use published references and record unresolved authority. |
| Broader repository inventory. | Exploratory work completed. | Four pinned candidate repositories, 84 records, 52 advancing across 39 families; runnable eligibility still pending. |
| Distinguish inference from reading documentation. | Working method. | Separate code-only and documentation-visible conditions and record claim provenance. |
| Public source knowledge cannot be ruled out by containers. | Method limitation and control requirement. | Use audited runtime isolation, full input records, unpublished semantic variants and renaming controls. |
| Prepared guidance versus interactive use. | Proposed design carried from the discussion. | DIRECT, GUIDE and INTERACT conditions; matched guidance in the latter two. Retire the old four-arm design for this draft. |
| Specific review checkpoints and consequences. | Concrete pilot proposal, not implemented. | Plan check, submitted-change review, changed-plan trigger, proceed/revise/unresolved decisions and proposed two-round correction limit. |
| Strong comparison rather than extra free review for the layer. | Fairness requirement; exact settings open. | Match checkpoint opportunities and resource caps, count all preparation and review costs, and distinguish ordinary review from structured interaction. |
| Runtime checking must not grade its own success. | Working method. | Separate final evaluator and hidden references; score false objections, missed violations and incomplete attempts. |
| Judge calibration and independent qualification need an explicit procedure. | Proposed in response to the user's question; no calibration executed. | Section 9A adds evidence-backed reference verdicts, role-specific rubrics, family-separated development and validation, bias tests, separate error rates, a predeclared qualification gate and regrading after changes. Numerical limits and sample size remain open. |
| The design needs implementation contracts and a complete worked case before qualification. | Contracts and H04 scripted development case completed on 8 September; no model qualification. | Section 10 records the executable evidence and the next isolated-runner work. H04 cannot count as independent validation. |
| The method section is too convoluted to follow. | Presentation change requested by the user. | Present one visible sequence through a test, with optional detail beside the relevant step. Preserve method requirements in the working plan; keep current status in Progress & findings. |
| Examples are illustrations, not frozen prompts. | Presentation clarification with input-control implications. | Label the website examples; keep them out of blind packs and specify actual instructions separately. |
| Wagtail example needs a specific reason for scrutiny. | Case-description clarification. | Identify dependence on internal permission machinery and its documented exception; do not suggest checking every interface indiscriminately. |
| A larger row count does not prove sample sufficiency. | Finding from inventory review; final design open. | Group related decisions, retain development exposure and size confirmation only after endpoint and precision choices. |
| Typography, paragraph widths, introductory context and navigation. | Website changes completed. | No change to scientific eligibility, endpoints or evidence status. |
| Keep the description and working plan in sync. | Explicit user instruction. | Canonical plan, synchronized copies, amendment register and future-edit checklist. No recurring background automation requested. |

## Superseded assumptions in the current working design

On 8 September, the user requested continuity between two Windows machines using Codex, without an explicit handover. The POC repository becomes the canonical home of the current plan, editable website and project state; earlier playbook-project and local copies are snapshots. Codex maintains the state and saves reviewed changes after each completed piece of work, bundling related decisions rather than pushing after every message. No experimental settings or evidence status changed. The automatic routine is an agent instruction, not a background service or chat-history synchronization.

The historical v1.2 plan remains intact in the project record's history directory. Its NetBox-only scope, 25 historical tickets, A/B/C/D factorial layout, 300-run schedule, prior Tier 1/Tier 2 scoring and numerical success/equivalence/extension rules are not the specification for the redesigned pilot. Legacy scripts and preregistration files still describe that earlier experiment and must be reviewed before reuse.

No scored results were reclassified or removed in this reconciliation. No live agent comparison, new container trial or paid model run was initiated. The pilot configuration and confirmatory protocol remain unfrozen.

## Next substantive decisions

Contracts and the H04 scripted case now record inputs, proposed component decisions, observed behaviour and reference comparisons. Next implement and test the isolated role runner and checkpoint enforcement described in section 10. Keep H04 in development and establish fresh qualification families.

The judge qualification gate now needs an explicit coverage and precision target, tolerable error rates, a development/validation split, an audit sample and a policy for combining mechanical, model and unresolved verdicts. Without independent expertise for ambiguous labels, restrict scored claims to defensible references and reproducible checks; do not substitute model agreement for ground truth.

Select and validate the pilot cases; set the exact coding/checking models and prompts; decide budgets and repetitions; test checkpoint enforcement and changed-plan detection; calibrate the scorer; verify allowed inputs; specify infrastructure retries; and record the pilot configuration before running it. Choose the confirmatory primary comparison, meaningful improvement and sample size separately before confirmation.
