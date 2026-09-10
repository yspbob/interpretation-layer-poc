# Takeaways for a practical interpretation layer

Started: 10 September 2026. Updated as the POC develops.

This record connects the POC's design discussions and eventual observations to practical implementation decisions. The initial entries come from planning discussions, not experimental results. No ROI, familiarity, model-quality or production-maintenance result has been established by these entries.

The [working plan](../preregistration/plan/working_plan_2026-09-05.md) remains the experimental specification. Recording a takeaway does not amend that plan, release website changes or authorize new experiments. Proposed changes below remain queued for the next explicitly requested plan and website update.

## How to maintain this record

Add or revise an entry when a discussion, implementation difficulty or observation has a practical consequence. Record the source and date, what was learned or proposed, its evidence and decision status, the implementation implication, remaining uncertainty and the next action. Link inspectable artifacts when evidence exists. Include adverse and inconclusive observations, not just ideas that favour the layer.

Keep stable entry IDs. Preserve important revisions and reasons through dated notes and Git history. Distinguish proposed or agreed design implications from implemented behaviour, observations on development cases and independently validated findings. Do not promote an attractive idea to a demonstrated result. When an entry changes the pilot method, carry it into the plan and change register at the authorised update; when it concerns production only, retain that boundary.

## IL-001: Measure when reused guidance recovers its preparation cost

**Source:** 10 September discussion of comparable time, cost and ROI. The user proposed break-even as a useful measure and highlighted reuse across changes.

**Status:** Agreed direction for the next planning update; calculation and measurement design remain to be specified. No return has been measured.

**Takeaway:** Preparing and verifying a guide creates an initial cost that may be recovered across multiple applicable tasks. Report cumulative costs alongside task quality and estimate the point at which a method becomes less costly than DIRECT. Calculate GUIDE and INTERACT separately. More uses do not guarantee a better return if the guidance adds cost without sufficient benefit.

**Practical implication:** Record preparation and verification costs against a guidance version, its declared reuse set, and the execution/review costs and outcomes of all attempts using it. Retain failed preparation and unsuccessful tasks. Reuse should involve distinct tasks that genuinely share guidance; repeated attempts on one task establish variability, not breadth of reuse. Preserve equal-budget comparisons and add economic analysis rather than replacing the quality comparison.

**What remains uncertain:** The cost allocation policy, quality requirements, uncertainty calculation and useful reuse horizon need specification. Monetary costs, human effort and elapsed time must remain distinguishable. Production maintenance and avoided-loss value are outside the current frozen-guide pilot. A simple preparation-cost divided by per-task-saving estimate assumes positive, stable savings and comparable outcomes; report no supported break-even when those conditions fail. Do not extrapolate an observed result indefinitely.

**Next action:** At the next authorised update, specify a bounded break-even analysis and the records needed to support it. Declare reuse sets before runs. Report estimates separately from directly observed cumulative savings.

## IL-002: Use costs and outcomes to prompt maintenance review

**Source:** 10 September discussion following IL-001. The user identified an economic maintenance rule and agreed it could be a takeaway for production.

**Status:** Emerging design finding from planning; candidate review policy, not a validated trigger or experimental result.

**Takeaway:** Guidance can need review because its evidence has changed or because experience suggests it no longer justifies its delivery and enforcement costs. The playbook already includes maintenance; this discussion adds a more explicit economic reason to initiate a review.

**Practical implication:** Preserve evidence-change signals, applicability/reuse counts, checking effort, unnecessary objections and supported benefit observations for each guidance version or related group. These can prompt review of wording, scope, duplication, delivery or enforcement. Record the resulting decision and its reason.

**What remains uncertain:** Rare use does not establish low value. Necessary security, correctness or other obligations must not be retired merely because measured time savings are small. The obligation and the way the layer represents/enforces it are separate decisions. Thresholds and responsibility for maintenance have not been tested, and this POC has no responsible project owner to exercise that production process.

**Next action:** Collect useful review signals where feasible in the POC. Keep the guide frozen during each declared comparison. Actual renewal, rule retirement and production maintenance remain outside this pilot.

## IL-003: Give humans evidence for guidance decisions, not a misleading ROI ranking

**Source:** 10 September user proposal for a dashboard of rule ROI to support human decisions, following IL-002.

**Status:** Agreed production design direction; dashboard not built and benefit attribution not validated.

**Takeaway:** A production dashboard could bring together applicability, reuse, preparation/checking/maintenance costs, supported benefits, avoidable objections, evidence freshness and estimated break-even. A responsible human would decide what to retain, revise, combine or retire, within their authority and applicable obligations.

**Practical implication:** Make costs and observations traceable to guidance versions, tasks and related rule groups. Show uncertainty and evidence links. Distinguish mandatory obligations from optional recommendations. Keep a decision history instead of allowing a low score to silently remove guidance.

**What remains uncertain:** Several rules can contribute to one outcome, and preparation work can be shared. Prefer guide-version or group-level economics until individual attribution is defensible. Do not duplicate the same benefit across rules or label a compliance observation as a monetised avoided incident without justification. Human decision rights and production workflows require later design.

**Next action:** Use IL-001 and IL-002 to identify data worth retaining. Capture the dashboard as a production implication; do not add a dashboard implementation or live maintenance to the current pilot scope.

## IL-004: Keep evidence verification distinct from owner approval

**Source:** 10 September user correction of the website sentence about a responsible owner approving guidance. This reinforces an existing boundary in the working plan and component contracts.

**Status:** Existing POC scope requirement; clarification banked for the website. No new owner or approval mechanism is introduced.

**Takeaway:** Evidence can support guidance without giving it organisational authority. The full production proposal includes owner approval; the technical POC has no responsible project owner and cannot certify newly constructed rules on one’s behalf.

**Practical implication:** Represent evidence support and approval status separately. Label the production approval step where it appears, and explain the POC's verifier-based admission alongside it. A verifier accepting a claim must not silently confer owner approval. An agent cannot resolve a missing organisational decision by asserting authority.

**Next action:** Clarify the preparation-cycle block in the next website batch while preserving the production step. The plan already records the absence of owner certification.

## IL-005: Make validation during task execution an explicit stage

**Source:** 10 September user review of the specific “Apply the guidance to each task” block. Existing detailed method and contracts already describe in-process checkpoints.

**Status:** Presentation clarification of an existing planned control; model-free rehearsal is not validation of the proposed full runtime.

**Takeaway:** Combining plan review, execution and rechecking in one short step hides a central behaviour of the layer. Make the sequence explicit: consult and plan; check the plan; implement and check during work; review the resulting change.

**Practical implication:** Agents can ask follow-up questions. Defined checkpoints and material changes trigger checks of the work so far, targeted questions and proceed/revise/unresolved decisions. Required checks must pause further work when necessary. Do not describe continuous semantic monitoring that the runner does not provide. Maintain matched review rules and correction limits across experimental groups.

**Next action:** Expand that specific usage-cycle block at the next website release. Preserve the distinction between live review with correction opportunities and independent assessment after the attempt ends.

## IL-006: Test for evidence of familiarity before interpreting public-code results

**Source:** 10 September discussion. The user agreed to two targeted probes during repository screening and case selection, rather than every experimental run.

**Status:** Agreed addition queued for the next plan and website update. Prompts, sampling, scoring and thresholds are not yet specified; no familiarity probes have run.

**Takeaway:** Model self-reports cannot establish absence of prior familiarity. Test observable recall: during repository screening, ask for distinctive missing details with newly written comparison snippets; during case selection, test reconstruction of particular historical fixes without repository access. Exact, unusual details are more suggestive than a conventional correct solution that could be reasoned out.

**Practical implication:** Use the exact intended model versions in fresh, separate probe sessions without browsing or file access beyond the declared prompt. Predefine prompts, scoring, repeated attempts and reporting, and retain failures. Keep all probes outside the experimental agents' histories. Revisit when models or selected material change; do not repeat as an extra source of information during every run. Anonymisation remains optional and may change task difficulty.

**What remains uncertain:** These are indicators with false positives and missed recall. Report “detected” or “not detected by these probes,” never “proved unfamiliar.” Newly written controls are not perfect matches. Familiarity does not automatically disqualify a repository, and non-detection does not prove inference solely from supplied code. Any use of probe outcomes in selection must be declared, with rejected candidates and reasons retained, rather than hiding positive findings.

**Research basis:** The missing-detail proposal adapts [Testset Slot Guessing](https://arxiv.org/abs/2311.09783); this is not a validated repository-specific detector. [Membership-inference evaluation](https://arxiv.org/abs/2402.07841) illustrates the limits of inferring training membership. [Code countermeasure research](https://arxiv.org/abs/2403.16898) cautions against treating performance changes after transformations as straightforward evidence of memorisation.

**Next action:** Specify the two probes in the next authorised planning batch. Fix their design and execution boundaries before any model calls. Keep the first-pilot claim limitation in place.
