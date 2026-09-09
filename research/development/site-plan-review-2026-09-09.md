# Website and working-plan review — 9 September 2026

Status: **design and presentation review, not experimental validation.** The user requested a thorough review and resolution of issues across the public website and plan. This record accompanies working revision `pilot-draft-2026-09-09.6`. No model comparison, component qualification or containment experiment was run for this review.

## Scope and basis

The review covered The Experiment, Progress & findings, their shared examples and case-library presentation, all sections of the canonical working plan, the component contracts, the H04 completion record, the change register and the plan-directory entry point. It checked the inventory's 84 claims and screening totals for consistency with the site's description. It did not independently reimplement or validate all 84 candidate cases.

The review compared the design with [Chapter 4 of the playbook](https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html#4-the-interpretation-layer). The technical POC still omits owner certification and maintenance, so neither a positive code result nor this review can establish the full proposal. Existing project instructions and ordinary review remain part of the baseline.

The evaluation references remain relevant: [Anthropic's guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distinguishes assessment methods and discusses task, harness and grading failures; [Zheng et al.](https://arxiv.org/abs/2306.05685) motivates presentation and model-preference checks. This design uses evidence-supported, narrower claims where independent expertise is unavailable. It does not present an evidence-only assessment as equivalent to expert validation of ambiguous architectural judgements.

The containment rationale was checked against [OpenAI's incident account](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) and [Hugging Face's technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline). The relevant lesson is to examine indirect routes through supporting services as well as the workload boundary. These accounts do not validate the proposed runner.

## Findings and resolutions

| Finding | Resolution in this revision |
|---|---|
| The verifier's decisions could be mistaken for independent scores of guidance quality. | A separate guidance assessor uses the prepared reference evidence. The verifier's admission is a treatment output, not its own success label. |
| The qualification narrative emphasised three components while intervention assessment also needs qualification. | Section 9A identifies five assessment jobs: verification, runtime review, guidance assessment, code assessment and intervention assessment. Different review instructions must qualify for their actual input conditions. These jobs need separate contexts, not necessarily different model products. |
| Historical implementation, discovery snapshot and correct answer were insufficiently distinguished. | Each backtest needs its own starting revision, target change and time-appropriate requirements. Historical code is assessed under the same criteria, including its violations. Later policy cannot silently become a task requirement. |
| Repeated patterns or hidden policy could become unjustified obligations. | Criteria distinguish observable behaviour, recommendations and enforceable requirements. Non-inferable hidden policy is an uncertainty control, not an obligation that a code-only agent must magically discover. |
| A task-blind drafter could still receive a pack selected using the hidden solution. | Source selection requires a recorded task-neutral scope. Task hints, exact instructions and sharing of guidance are part of the exposure record. |
| Preparation could continue until a useful guide appeared, concealing failures. | Declare preparation and revision limits. Freeze the admitted subset at exhaustion, including an empty guide; both guidance treatments receive it and retain the cost and outcome. |
| The overall resource cap did not explain how preparation was charged. | The working policy uses equal total method allowances. Each guidance treatment carries its attributed preparation cost, allocated over a task set fixed in advance, with failed attempts retained. First-use cost and actual experiment spend are reported separately. Numerical caps are not selected by this review. |
| Identical review points are impossible when agents take different paths. | Match the trigger policy, correction allowance and common tests. Initial and final reviews are required; intermediate counts can differ. Pauses must block coding turns and mutating tool dispatch. |
| All uncertainty appeared to stop work, and frozen guidance could appear unquestionable. | Only an unresolved issue preventing a necessary decision blocks the attempt. Review can identify a guide defect and require an evidence-supported action without rewriting the guide. |
| Invalid agent output could be classified as infrastructure failure and excluded. | Agent errors, refusals and budget exhaustion remain method outcomes. External/integrity failures need recorded causes and a predeclared block/retry rule. All scheduled attempts, exclusions and retries remain visible. |
| Repeated tasks and shared preparation could be counted as independent, and execution order could confound results. | Retain family, replicate and shared-guide identifiers; balance or randomise treatment order with fresh state. Report differing information conditions and task types separately. |
| Regrading a revised judge could leave an exposed confirmation set labelled confirmatory. | Requalify affected roles and rescore consistently, but classify confirmation material used for repair as exploratory. A new confirmatory claim requires fresh families. |
| Containment requirements did not sufficiently explain trusted components or forged outputs. | The controller/gateway/runtime/evaluator are an explicit trusted base. Requirements cover bounded gateway destinations, collected artifacts, pause semantics, test tampering and forged success reports. Implementation and validation remain pending. |
| Controls were described as fifteen missing-authority cases; H04's library panel ignored its development task. | The site now includes conflict and enforcement-gap controls, and gives H04 its actual development status without calling it a historical backtest or qualified trial. Inventory classifications and recorded results are unchanged. |
| Repeated review explanations obscured the page's structure; disclosure IDs were not usable anchors. | Removed the duplicated walkthrough, retained one detailed execution explanation, added cost detail and stable disclosure targets, and kept readiness on Progress. |
| The plan-directory README directed readers to an obsolete source of authority. | It now leads with the local canonical working plan and labels the older records as historical. |

## Decisions that still require work

These are explicit readiness gates, not issues resolved merely by better prose. Section 9B is the authoritative gate table.

1. Select the concrete isolation runtime and interfaces, implement them and demonstrate the required restrictions before model calls.
2. Build historical cases with justified criteria, actual project-instruction audits, valid alternatives and runnable environments. Discovery snapshots and authored examples alone are insufficient.
3. Construct separate qualification families and fix role-specific limits, precision, coverage, sample sizes and acceptance rules before seeing qualification results.
4. Fix the pilot's model settings, preparation/reuse limits, budgets, treatment order, scoring, retry and audit configuration. Obtain authorisation for model expenditure before calls.
5. Use feasibility evidence to set the main comparison, endpoint, worthwhile benefit/cost limits and sample-size justification; preserve fresh confirmation families.

The review does not invent numerical acceptance rates or claim empirical reliability. The next implementation milestone remains the model-free isolated runner, followed by component qualification.

## Verification

Application type and lint checks and the static Pages build passed. Eleven browser checks passed at desktop and mobile widths: route navigation, expandable sections, all example tabs, unique IDs and local fragment/download links, overflow checks, case search, the H04 detail panel, empty-result recovery, pagination, both filters and the latest plan download. No browser exceptions or failed local resources were recorded. The technical diagram, comparison table and readiness cards were visually inspected.

All 84 inventory records have unique IDs; screening totals, family totals, per-project counts and pinned source references agree. The structured download equals the website data. The NetBox and Wagtail examples were checked against their pinned upstream documentation; the HTTPX cookie example was checked against its pinned local documentation and implementation. The canonical plan and change register were synchronised into their downloads.

Historical H04 observations and their hashes are preserved; this review does not rerun them or relabel them as independent validation. Browser checks establish website behaviour, not the reliability or containment of the proposed experiment.
