# Takeaways for a practical interpretation layer

Started: 10 September 2026. Updated as the POC develops.

This record connects the POC's design discussions and eventual observations to practical implementation decisions. The initial entries come from planning discussions, not experimental results. No ROI, model quality or production maintenance benefit has been established. IL-006 now includes a preliminary familiarity observation with explicit execution limits.

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

**Status:** Procedure added to plan section 2A and explained on the website on 10 September. The prepared prompts and scoring were used in a preliminary screen through 24 fresh Astra subagents on 13 September. It found no exact source matches. The controlled API screen remains pending.

**Takeaway:** Model self-reports cannot establish absence of prior familiarity. Test observable recall: during repository screening, ask for distinctive missing details with newly written comparison snippets; during case selection, test reconstruction of particular historical fixes without repository access. Exact, unusual details are more suggestive than a conventional correct solution that could be reasoned out.

**Practical implication:** Use the exact intended model versions in fresh, separate probe sessions without browsing or file access beyond the declared prompt. Predefine prompts, scoring, repeated attempts and reporting, and retain failures. Keep all probes outside the experimental agents' histories. Revisit when models or selected material change; do not repeat as an extra source of information during every run. Anonymisation remains optional and may change task difficulty.

**What remains uncertain:** These are indicators with false positives and missed recall. Report “detected” or “not detected by these probes,” never “proved unfamiliar.” Newly written controls are not perfect matches. Familiarity does not automatically disqualify a repository, and non-detection does not prove inference solely from supplied code. Any use of probe outcomes in selection must be declared, with rejected candidates and reasons retained, rather than hiding positive findings.

**Research basis:** The missing-detail proposal adapts [Testset Slot Guessing](https://arxiv.org/abs/2311.09783); this is not a validated repository-specific detector. [Membership-inference evaluation](https://arxiv.org/abs/2402.07841) illustrates the limits of inferring training membership. [Code countermeasure research](https://arxiv.org/abs/2403.16898) cautions against treating performance changes after transformations as straightforward evidence of memorisation.

**Next action:** Preserve the [preliminary result](development/astra-preparation/SUBAGENT-SCREEN.md) without treating it as proof of unfamiliarity. Verify the eventual experimental configuration and complete the required controlled gates before scored work. The historical task diagnostic remains later case selection work. Keep the first pilot limitation in place.


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


## IL-011: Follow an operation beyond the database transaction

**Source:** [NetBox NB-BULK-01 candidate investigation](development/netbox-bulk-error-candidate/README.md), 11 September 2026. Earlier code and documentation were inspected alongside the historical feature and later upstream QA.

**Status:** Source supported implementation observation and upstream reported correction. NetBox runtime reproduction and model assessment remain pending.

**Takeaway:** A database rollback does not necessarily undo related work held elsewhere. In this NetBox path, change events are queued in memory and processed after the request. Guidance about a failed batch needs to account for those events as well as the database writes.

**Practical implication:** When reconstructing a transaction rule, follow its consequences through event queues and other side effects. Record what each mechanism protects, where cleanup occurs and what successful operations must preserve. Do not turn this into an instruction to clear all events whenever any error occurs.

**What remains uncertain:** The full request path has not been reproduced here. The earlier source already contains a cleanup convention; this is not proof of discovering an undocumented decision or of superiority over an ordinary agent.

**Next action:** Reproduce the bounded NetBox case before admitting a runtime reference. Keep code observations, documented guarantees and inferred scope separately traceable.


### IL-011 runtime update: existing behaviour can violate the supported rule

**Source:** [Local NetBox reproduction](development/netbox-bulk-error-candidate/reproduction.md), completed on 11 September with real PostgreSQL and Redis.

**Evidence:** All twelve request scenarios completed across three revisions. Failed batches restored the records and their change logs. The starting revision nevertheless queued an incorrect webhook job in one mixed ordering; the feature did so in both orderings. The later QA queued no jobs for failed batches and retained successful events. These are related checks of one public development family. Delivery to a recipient was not tested.

**Practical implication:** A guide must distinguish a supported guarantee from code that currently violates it. Repeating the API implementation would preserve this defect. Record the conflicting paths and the evidence for the rule; do not treat the historical implementation as an answer key.

**Limits and next action:** Model reconstruction and added value remain untested. Turn the scoped rule, exceptions and uncertainty into assessment records, and qualify on separate material. The local container setup is a development environment, not qualified agent containment.


## IL-012: Separate releasing guidance from assessing its quality

**Source:** [First Phase 1 harness](development/phase1-harness/README.md), 11 September 2026, implementing the previously agreed preparation and assessment separation.

**Status:** Implemented and checked with authored examples. This is an engineering control, not an observed model benefit.

**Takeaway:** Save the exact guide that verification released before assessing it. Otherwise a later assessment can quietly turn an unsuccessful preparation into a successful looking guide. Record the original draft, corrections, rejected claims and omissions alongside that released version.

**Practical implication:** A production dashboard can show both release status and independent quality evidence. A later review may justify a new version, but it should preserve the earlier version and explain what changed. An empty guide should remain visible as an outcome with missing coverage, not appear successful merely because it contains no false claims.

**What remains uncertain:** The rehearsal does not show whether models make sound admission or assessment decisions. Independent model qualification, operating costs and the benefit of a production dashboard remain untested.

**Next action:** Preserve this separation in the actual provider adapter and qualification runs. Do not let assessment feedback enter working role inputs without recording a new development or preparation stage.


## IL-013: An uncertain call must not silently become a free retry

**Source:** [Provider adapter development](development/phase1-harness/PROVIDER.md), 13 September 2026, implementing the POC's existing spending and failure requirements.

**Status:** Implemented control checked with simulated timeouts, missing usage and HTTP failures. No real provider charge was measured.

**Takeaway:** When a model request times out, the caller may not know whether it reached the provider or incurred a charge. Automatically repeating it can consume more money and create an unrecorded extra attempt.

**Practical implication:** Reserve an allowance before sending a request. Keep that reservation if usage is unknown, stop further calls and reconcile the outcome. Preserve refusals and invalid answers in cost records when usage is available. A production rules dashboard should distinguish known cost from amounts awaiting reconciliation.

**What remains uncertain:** Configured rates and token bounds must match the selected provider. This control cannot reverse a charge or cap unrelated account activity. Its operational cost and effect on the layer's return remain untested.

**Next action:** Verify provider pricing and usage behaviour during the separately authorised connection check, then preserve the same accounting in qualification and guidance runs.

## IL-014: Separate review roles can still share the same blind spots

**Source:** User agreement on 13 September 2026 to start with Astra and defer Fable, and the [qualification preparation](development/astra-preparation/QUALIFICATION.md).

**Status:** Design implication. No model qualification or correlated error measurement has run.

**Takeaway:** Fresh contexts prevent a reviewer from inheriting another role's conversation. They do not guarantee that the roles will make different mistakes. Repeated agreement can therefore overstate the confidence justified by the evidence.

**Practical implication:** Show the evidence supporting a rule alongside its review verdict and model configuration. Use behavioural checks and justified references where possible. Adding a second model is a possible source of another opinion, not automatic certification.

**What remains uncertain:** We do not yet know how often Astra's verifier and assessors will make the same error, or whether adding another model would justify its cost.

**Next action:** Qualify each actual role on separate evidence justified cases, preserve disagreement and unresolved decisions, and keep claims limited to the tested model configuration.


## IL-015: Preserve conflicting evidence when checking a rule

**Source:** [First qualification case preparation](development/astra-preparation/Q01-READINESS.md), 13 September 2026. Detailed case evidence remains private until it can be released without compromising qualification.

**Status:** A reference preparation observation. No model or interpretation layer benefit has been measured.

**Takeaway:** A quotation can be authentic and still be too broad for the situation being assessed. A reviewer needs to consider the relevant exceptions and contrary evidence before approving the proposed scope.

**Practical implication:** Keep the source of each assertion and any conflicting evidence visible in the rule record. Explain why one interpretation is supported. If the evidence cannot settle the claim, retain the uncertainty and identify what would resolve it. A dashboard should show this reasoning alongside the admission decision.

**What remains uncertain:** The preparation shows how to justify one reference. It does not establish that a model will notice the conflict, resolve it correctly or save time by doing so. Behavioural observations establish what happened under tested conditions; they cannot establish owner approval.

**Next action:** Preserve counterevidence in qualification inputs and test the actual assessment roles. Keep legitimate cautious verdicts in the scoring rules where the evidence does not justify a single answer.


## IL-016: Challenge the assessment reference as well as the candidate

**Follow up, 13 September:** The complete verdict review reproduced counterexamples to a purportedly equivalent paraphrase and a rule that blurred consecutive operations. It also made coverage explicit when a guide contradicts itself. A production assessment should preserve those distinctions: correct wording somewhere in a guide is not evidence that the whole guide is reliable. These are preparation defects supported by source and runtime evidence, not a measured benefit from the layer. Keep the audit bounded to demonstrated issues and required checks.

**Source:** [Qualification bank evidence review](development/astra-preparation/BANK-READINESS.md), 13 September 2026. The underlying source and runtime records are committed by hash and remain private until qualification permits release.

**Status:** A preparation finding supported by an observed exception and a constructed scoring counterexample. No model benefit has been measured.

**Takeaway:** The expected answer can contain a mistake. A runtime check contradicted an overbroad reference assertion, which was corrected before model testing. Separately, the proposed repeat check could penalise two verdicts that the same scoring key accepted.

**Practical implication:** Test whether the reference accounts for known exceptions and permits legitimate alternatives. Preserve the old reference and explain changes with evidence. In production, an adverse review should remain open to a demonstrated flaw in the rule or assessment criterion; an earlier approval is not proof of correctness.

**What remains uncertain:** These corrections show specific preparation defects. They do not measure how frequently such defects occur, whether an AI will find them or how much review effort a production layer will save.

**Next action:** Keep references and scoring rules versioned. During qualification, retain any disagreement with executable evidence and investigate it before interpreting a model failure. Material used to revise a role after seeing its answers becomes development material.

## IL-017: Keep unsuccessful reviews and their cost visible

**Source:** [Qualification batch rehearsal](development/phase1-harness/QUALIFICATION-BATCH.md), 14 September 2026.

**Status:** Software behaviour demonstrated with local responses. No model reliability or production cost finding.

The batch checks show why each attempt needs both an outcome and a spending record. An unusable answer can still incur a known charge. A timeout can leave usage unknown. These require different accounting, while both attempts must remain visible. The implemented runner charges known usage, preserves uncertain reservations and does not automatically retry.

**Limit and next action:** Simulated usage does not certify provider billing. Verify actual usage and prices before any authorised live run, and preserve this separation in its records. Do not infer permission to restart a stopped batch with a fresh budget.


## IL-018: A second model can expose a disagreement, not settle it

**Source:** User discussion and the [Fable desktop procedure](development/astra-preparation/FABLE-DESKTOP.md), 14 September 2026.

**Status:** Agreed assessment design, now exercised in two public H06 development reviews at High effort. No qualification or experimental result.

Astra fills both preparation and assessment roles in the controlled workflow. Fable will assess finished guidance separately to look for errors that Astra misses. Preserve each initial verdict before comparison. Resolve disputes through sources and reproducible checks rather than a vote. Agreement can still conceal a faulty shared reference.

**Uncertainty and next action:** The benefit and shared error rate are unmeasured. Qualify the recorded desktop configuration before relying on its judgements, report both useful corrections and mistaken objections, and keep its results separate from controlled API scores. The user subsequently authorised reference challenges and both applicable reviews at High effort. Preserve reference revisions and resolve objections against evidence before changing labels.


## IL-019: Check reviewer objections as carefully as approvals

**Source:** [Fable H06 reviews and evidence checks](development/astra-preparation/FABLE-H06-REVIEW.md), 14 September 2026.

**Status:** Preparation findings supported by pinned source and twelve focused behaviour checks. One public development family, not a measured benefit from the layer.

The reference review found useful qualifications about which request a flag prepares and whether a documentation example actually produces its intended error. It also challenged an already loaded body exception using a counterexample whose body was not loaded. We retained the exception after checking both states. A second model is useful as a source of specific challenges, not as a final authority.

**Practical implication:** Keep the original verdict and investigate its counterexample against the rule's actual conditions. Record both accepted and rejected objections. Documentation may support an intended usage rule while its example code still needs correction.

**Uncertainty and next action:** This does not estimate either model's reliability. Qualify the chosen configuration before using scores. The desktop rehearsal also showed that disabling connectors leaves attachment tools available; permitted evidence, reading tools and observed access need separate records before any sealed test.


## IL-020: Check separate tool controls and preserve their limits

**Source:** [Desktop access rehearsal](development/astra-preparation/FABLE-DESKTOP-CONTROLS.md), 14 September 2026.

**Status:** Two public operating diagnostics, not a finding about guidance quality or general isolation.

Turning off connectors left attachment tools active in the earlier review. Turning off the separate cloud execution feature allowed the tested text attachment to be read without visible tool calls. A fresh chat did not return the preceding chat's random marker. Skills still appeared in menus, and the provider's complete context remained invisible.

**Practical implication and next action:** Record actual feature settings and observed access separately. Recheck restrictions when starting a session, especially after restoring settings for ordinary use. Do not turn a successful diagnostic into a claim that every hidden access path is blocked. Check the real packet format before qualification and keep this desktop route separate from controlled API scores.


Follow through on IL-020, 14 September: the [desktop qualification freeze](development/astra-preparation/FABLE-QUALIFICATION-READINESS.md) now preserves each permitted input and its order, separately from expected answers. Exact input equality and byte fit passed. These checks still cannot establish provider context or answer correctness. Next apply the same fixed procedure to qualification and preserve actual access and capture failures.


## IL-021: Count the effort needed to operate the assessment

**Source:** The first three frozen Fable qualification responses and the user's concern about elapsed time and Codex usage, 14 September 2026. Execution details are in PROJECT_STATE.md; raw captures remain private.

**Status:** An observed preparation cost, not a result about reviewer accuracy or the layer's return.

Desktop assessment requires more than waiting for an answer. This session repeatedly checked settings and allowance, uploaded the permitted file, and captured and checked each response. Three answers were preserved before the user raised the cost of continuing. Window changes, capture layout and a file dialog also required operator attention.

**Practical implication:** Record operator effort alongside model usage when choosing how to run an assessment. An included subscription allowance does not make the whole process free.

**Uncertainty and next action:** This session does not provide a controlled time comparison with another route. Review whether delivery can be made more efficient while preserving the frozen inputs, first answers and access records. No replacement route or reduced test has been agreed.


Follow through on IL-021, 14 September: the [delivery comparison](development/astra-preparation/DELIVERY-OPTIONS-2026-09-14.md) measures input sizes and separates token price, reasoning assumptions, operator effort and setup work. It compares direct API, subscription automation, manual delivery and a reduced second reviewer role. These are options, not measured savings or agreed method changes. Choose the delivery route before implementing another integration; preserve the original responses when changing configuration.


## IL-022: A fresh worker is not proof of a single attempt

**Source:** [Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents), inspected 14 September 2026, and the user's proposal to delegate one test to each worker.

**Status:** Documented application behaviour, not yet observed in our rehearsal.

Ordinary subagents start separate conversations, but custom workers can receive project instructions. Conversation forks inherit earlier history. Claude Code can also continue an interrupted worker response automatically. These distinctions matter when a study requires only the permitted evidence and preserves the first answer.

**Next action:** Inspect the effective worker inputs and raw response records in the two public rehearsals. Record any inherited material, extra generation or fallback. Do not call the route qualified merely because two toy outputs are correct.

Follow through on IL-022, 15 September: the [public rehearsal](development/astra-preparation/FABLE-SUBAGENT-REHEARSAL.md) completed with two fresh Fable 5.1 High workers. Exact inputs, empty tool lists and one recorded response per worker were verified. Neither worker record contains the other marker. Both records do contain standard application and account context, so a fresh worker is not a context containing only our own text. An earlier attempt failed because safe mode disabled the custom agent; that failure is retained. No interrupted response was observed or tested. Check the full packet delivery method and record these limits before qualification, without changing the frozen questions or treating this diagnostic as assessor validation.

## IL-023: Deliver evidence without asking a model to copy it

**Source:** [Public packet delivery checks](development/astra-preparation/FABLE-DIRECT-DELIVERY.md), 15 September 2026.

**Status:** Observed transport failure and successful direct delivery check. Not an assessment of guidance quality.

A coordinator changed source text while relaying a larger packet, although its worker returned valid assessment JSON. Direct insertion into a fresh assessor preserved every byte. Checking only the answer format would have missed the altered evidence.

**Practical implication and next action:** Use ordinary file handling to deliver evidence and compare the actual saved input with the approved packet. Do not spend model output generating copies of that packet. Preserve failed attempts, including our own synthetic schema mistakes. Freeze the direct procedure before qualification; one public example does not prove reliability for every input or reveal hidden provider activity.

Follow through on IL-023, 15 September: the user selected direct delivery operated by Codex. The fixed procedure and new private freeze preserve all 48 original files and scoring criteria. Six local failure tests and the saved public transcript passed the audit. Account checks and uncertain provider behaviour remain explicit operator limits. Qualification starts with fresh sessions under this configuration; the three older desktop responses cannot fill positions in the new schedule.
