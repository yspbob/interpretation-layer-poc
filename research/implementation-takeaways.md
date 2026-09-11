# Takeaways for a practical interpretation layer

Started: 10 September 2026. Updated as the POC develops.

This record connects the POC's design discussions and eventual observations to practical implementation decisions. The initial entries come from planning discussions, not experimental results. No ROI, familiarity, model-quality or production-maintenance result has been established by these entries.

The [working plan](../preregistration/plan/working_plan_2026-09-05.md) remains the experimental specification. Recording a takeaway does not amend that plan, release website changes or authorize new experiments. The 10 September release applies the agreed method changes and explanations in working plan `pilot-draft-2026-09-10.1` and both website views. The statuses below distinguish that publication from implementation and experimental evidence.

## How to maintain this record

Add or revise an entry when a discussion, implementation difficulty or observation has a practical consequence. Record the source and date, what was learned or proposed, its evidence and decision status, the implementation implication, remaining uncertainty and the next action. Link inspectable artifacts when evidence exists. Include adverse and inconclusive observations, not just ideas that favour the layer.

Keep stable entry IDs. Preserve important revisions and reasons through dated notes and Git history. Distinguish proposed or agreed design implications from implemented behaviour, observations on development cases and independently validated findings. Do not promote an attractive idea to a demonstrated result. When an entry changes the pilot method, carry it into the plan and change register at the authorised update; when it concerns production only, retain that boundary.

## IL-001: Measure when reused guidance recovers its preparation cost

**Source:** 10 September discussion of comparable time, cost and ROI. The user proposed break-even as a useful measure and highlighted reuse across changes.

**Status:** Analysis design recorded in plan section 6A on 10 September; numerical settings and measurement implementation remain open. No return has been measured.

**Takeaway:** Preparing and verifying a guide creates an initial cost that may be recovered across multiple applicable tasks. Report cumulative costs alongside task quality and estimate the point at which a method becomes less costly than DIRECT. Calculate GUIDE and INTERACT separately. More uses do not guarantee a better return if the guidance adds cost without sufficient benefit.

**Practical implication:** Record preparation and verification costs against a guidance version, its declared reuse set, and the execution/review costs and outcomes of all attempts using it. Retain failed preparation and unsuccessful tasks. Reuse should involve distinct tasks that genuinely share guidance; repeated attempts on one task establish variability, not breadth of reuse. Preserve equal-budget comparisons and add economic analysis rather than replacing the quality comparison.

**What remains uncertain:** The cost allocation policy, quality requirements, uncertainty calculation and useful reuse horizon need specification. Monetary costs, human effort and elapsed time must remain distinguishable. Production maintenance and avoided-loss value are outside the current frozen-guide pilot. A simple preparation-cost divided by per-task-saving estimate assumes positive, stable savings and comparable outcomes; report no supported break-even when those conditions fail. Do not extrapolate an observed result indefinitely.

**Next action:** Implement the section 6A records and set its numerical assumptions and analysis configuration before economic runs. Declare reuse sets before runs. Report estimates separately from directly observed cumulative savings.

**Budget procedure added on 10 September:** Section 6B now requires a study spending ceiling, development calibration of all three methods under a selection rule recorded in advance, and fixed allowances before scored comparisons. A second budget level is planned where affordable to test whether the conclusion depends on the allowance. This is an agreed design, not a calibrated budget or evidence of savings. Production teams would choose spending policies for their own workload; a useful allowance in this POC would not establish a universal operating budget.

**Explanation released on 10 September:** The website now describes this procedure and separates cost recovery observed during the experiment from estimates about further use. Progress records that amounts remain open and calibration has not run. The wider writing review changes how these takeaways are explained, not their evidence status.

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

**Status:** Existing POC scope requirement; the production-versus-POC clarification is applied in the 10 September release. No new owner or approval mechanism is introduced.

**Takeaway:** Evidence can support guidance without giving it organisational authority. The full production proposal includes owner approval; the technical POC has no responsible project owner and cannot certify newly constructed rules on one’s behalf.

**Practical implication:** Represent evidence support and approval status separately. Label the production approval step where it appears, and explain the POC's verifier-based admission alongside it. A verifier accepting a claim must not silently confer owner approval. An agent cannot resolve a missing organisational decision by asserting authority.

**Next action:** Preserve the explicit preparation-cycle distinction as the implementation develops. The plan already records the absence of owner certification.

## IL-005: Make validation during task execution an explicit stage

**Source:** 10 September user review of the specific “Apply the guidance to each task” block. Existing detailed method and contracts already describe in-process checkpoints.

**Status:** Presentation clarification of an existing planned control; model-free rehearsal is not validation of the proposed full runtime.

**Takeaway:** Combining plan review, execution and rechecking in one short step hides a central behaviour of the layer. Make the sequence explicit: consult and plan; check the plan; implement and check during work; review the resulting change.

**Practical implication:** Agents can ask follow-up questions. Defined checkpoints and material changes trigger checks of the work so far, targeted questions and proceed/revise/unresolved decisions. Required checks must pause further work when necessary. Do not describe continuous semantic monitoring that the runner does not provide. Maintain matched review rules and correction limits across experimental groups.

**Next action:** The usage-cycle block now has four explicit steps, including checks during implementation. Implement and test that planned behaviour in the runner. Preserve the distinction between live review with correction opportunities and independent assessment after the attempt ends.

## IL-006: Test for evidence of familiarity before interpreting public-code results

**Source:** 10 September discussion. The user agreed to two targeted probes during repository screening and case selection, rather than every experimental run.

**Status:** Procedure added to plan section 2A and explained on the website on 10 September. Prompts, sampling, scoring and thresholds are not yet specified; no familiarity probes have run.

**Takeaway:** Model self-reports cannot establish absence of prior familiarity. Test observable recall: during repository screening, ask for distinctive missing details with newly written comparison snippets; during case selection, test reconstruction of particular historical fixes without repository access. Exact, unusual details are more suggestive than a conventional correct solution that could be reasoned out.

**Practical implication:** Use the exact intended model versions in fresh, separate probe sessions without browsing or file access beyond the declared prompt. Predefine prompts, scoring, repeated attempts and reporting, and retain failures. Keep all probes outside the experimental agents' histories. Revisit when models or selected material change; do not repeat as an extra source of information during every run. Anonymisation remains optional and may change task difficulty.

**What remains uncertain:** These are indicators with false positives and missed recall. Report “detected” or “not detected by these probes,” never “proved unfamiliar.” Newly written controls are not perfect matches. Familiarity does not automatically disqualify a repository, and non-detection does not prove inference solely from supplied code. Any use of probe outcomes in selection must be declared, with rejected candidates and reasons retained, rather than hiding positive findings.

**Research basis:** The missing-detail proposal adapts [Testset Slot Guessing](https://arxiv.org/abs/2311.09783); this is not a validated repository-specific detector. [Membership-inference evaluation](https://arxiv.org/abs/2402.07841) illustrates the limits of inferring training membership. [Code countermeasure research](https://arxiv.org/abs/2403.16898) cautions against treating performance changes after transformations as straightforward evidence of memorisation.

**Next action:** Implement the two probes and fix their samples, prompts, scoring, repeats and execution boundaries before any authorised model calls. Keep the first-pilot claim limitation in place.


### IL-006 clarification: familiarity created by our own work

**Source:** 11 September user question about source inspection and incognito execution, assessed in the [approach review](development/approach-and-reading-review-2026-09-11.md).

**Status:** Explanation of existing separation requirements, applied to the website and plan on 11 September. This is not a newly validated control. Provider settings remain to be verified for the selected experimental interface.

**Takeaway:** Keep three things distinct: prior training knowledge, intended reading during an attempt, and information inherited from other tasks. Fresh experimental sessions address the third only when history, files, memory and retrieval access are actually controlled. They cannot erase prior training knowledge.

**Next action:** Verify those boundaries in the runner and explain them plainly. Preserve permitted history within an attempt and intentionally supplied guidance. Never pass the investigator's conversation or hidden assessment feedback to a working role. Check provider training and retention policies separately; an incognito label is not an isolation test.

## IL-007: Separate guidance preparation from repeated use and explain pilot differences

**Source:** 10 September clarification of when guidance is prepared, followed by the user's requirement to explain every material production-versus-POC difference.

**Status:** Applied to the explanation and working plan on 10 September; production cadence and maintenance effectiveness remain untested.

**Takeaway:** Preparation produces a version for a compatible repository state and permitted source set. Reuse that version across its declared tasks; it is neither a new guide for every coding run nor one universal guide for the whole experiment. Production would add review of changed evidence and proposed new rules. Nightly checks are a possible cadence, with earlier review for consequential changes, not a fixed validated requirement.

**Practical implication:** Identify guidance versions and their applicability explicitly. Explain production intent beside POC simplifications in authority, preparation, reuse, maintenance, interaction, access, evaluation and economics. State what each difference prevents the experiment from concluding. Keep actual implementation and validation status separate from the proposed method.

**Next action:** Carry guide identity and reuse compatibility into the runner and future production design. The current release implements the explanation and specification only; it does not run preparation, maintenance or model trials.

## IL-008: Validate a narrow use before building broader capability

**Source:** 10 September discussion of POC complexity and the user's request to divide the work into phases.

**Status:** Agreed scope and presentation decision, recorded in plan section 1A. No comparative result supports it yet.

**Takeaway:** The first implementation needs enough capability to run a credible comparison in one selected setting. Wider repository coverage, operation on multiple execution hosts and production maintenance can each be separate decisions after evidence exists.

**Practical implication:** Keep the integrity controls needed for the selected use: justified evidence, limited inputs, isolation, matched reviews and budgets, qualified assessment and complete records. Narrow the coverage being built and qualified instead of removing these controls. Describe possible later capabilities separately from current commitments and actual progress.

**What remains uncertain:** A small first trial can expose defects in the method and supply preliminary observations. It cannot establish general effectiveness, production return or readiness for owner governance and maintenance.

**Next action:** Choose the first repository and decision families, review existing tooling and qualify one execution host. Use the first trial report to decide whether further work is justified, including when results are negative or inconclusive.


### IL-008 refinement: phase by function, not only by coverage

**Source:** 10 September follow-up. The user pointed out that the first phase still carried most of the work, then accepted splitting the first trial itself.

**Status:** Agreed implementation sequence in plan revision .4, not an empirical finding.

**Refinement:** Narrowing the number of repositories leaves most infrastructure in place if the first result still requires every role. Assess guidance reconstruction first, add coding use second, and add interaction third. Each phase should deliver evidence before the next capability is built. Keep the integrity controls required by each exposed capability.

**Limits:** Guidance quality does not establish coding usefulness. Results collected in different phases cannot isolate the interaction effect; rerun matched groups in Phase 3. Assessment feedback and guidance repairs must not contaminate later claims of blinded reconstruction.

**Next action:** Build the restricted preparation and independent guidance assessment path first. Leave code execution and interactive checking out unless an actually exposed capability requires their controls.

## IL-009: Preserve unsuccessful preparation when assessing later usefulness

**Source:** [Approach and reading review, 11 September](development/approach-and-reading-review-2026-09-11.md), prompted by the user's request to analyse the approach. This is an assistant recommendation based on the difference between the Phase 2 page wording and working plan section 5.

**Status:** Agreed by the user and applied on 11 September in plan revision .1 and both website views. This clarifies existing retention of empty guides and failed preparation; it is not an experimental finding.

**Takeaway:** A verifier's decision to admit a claim and an independent assessment of the resulting guide serve different purposes. Selecting only guides that score well in the latter can hide preparation failures when assessing the overall method's usefulness.

**Practical implication:** Keep the original draft, verifier decisions, released guide version, independent assessment, preparation cost and intended uses separately traceable. Preserve empty outputs and failures. Do not infer overall preparation reliability from results collected only after successful preparation.

**What remains uncertain:** The study may reasonably stop or repair the method between phases. A test of only successful guides can answer a narrower question. The transition policy now distinguishes these choices. Numerical gates remain open.

**Next action:** Implement the recorded transition policy and preserve preparation outcomes, costs and feedback history. Retain the separation between development feedback and blinded preparation.


## IL-010: Explain when a custom implementation bypasses framework support

**Source:** 11 September inspection and local checks of HTTPX H06 at the inventory's pinned commit. See the [guidance assessment case](development/h06-guidance-assessment/README.md).

**Status:** An implementation observation supported by source inspection and selected local behaviour checks. It is not evidence of model interpretation quality or a measured production benefit.

**Takeaway:** A configuration flag can work through a particular framework method rather than apply everywhere. A custom override may bypass that method. Guidance needs to explain that boundary, not merely repeat the flag's name or promise.

**Practical implication:** Record which implementation supplies a guarantee, when it runs and what an override must preserve or replace. Accept a valid alternative that performs the required work itself. Include both the usual path and an override when checking a proposed guide.

**What remains uncertain:** The H06 checks cover dispatch and body availability, not concurrency safety, event loop blocking, real authentication services or other frameworks. Whether the layer reliably recovers and communicates this distinction is untested.

**Next action:** Use the case when specifying development assessment records, then qualify the assessor on separate families. Do not generalise the observation into a universal rule about all configuration flags.
