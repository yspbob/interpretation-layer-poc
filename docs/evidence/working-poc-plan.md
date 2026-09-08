# Working pilot plan: interpretation-layer validation

Plan ID: **pilot-draft-2026-09-08.1**
Updated: **8 September 2026**
Status: **Working design for pilot preparation. Not a frozen preregistration, not an implemented experiment, and not a result.**

This document incorporates the research review and the subsequent website-design discussion. It is the current planning document for the redesigned POC. The previous ratified v1.2 plan is preserved as a historical record; its NetBox-only four-arm design, 25-ticket sample, 300-run schedule and success rule must not be silently inherited by this pilot.

The canonical working copy remains `poc_interpretation_layer_plan.md` in the playbook project record. Identical copies are maintained in the POC repository, the website's evidence downloads and the working deliverables. The website explains this plan; it is not a separate source of experimental decisions.

## 1. What this POC should establish

Chapter 4 proposes capturing evidence about a system, drafting guidance, obtaining owner approval, serving the relevant guidance during work, and checking compliance. We need evidence that the added technical machinery is useful rather than merely plausible.

The pilot has three questions:

1. Can the layer derive useful, appropriately qualified guidance from the sources it is allowed to see?
2. Does giving that guidance to an agent improve a later code change compared with a capable agent working directly from the same sources?
3. Does structured consultation and checking add value beyond supplying the guidance and providing ordinary review?

Keep inference quality, handling of documentation, downstream code quality and interaction effects separate. A correct explanation alone does not establish that the layer helps with engineering work. A benefit must also be considered against preparation, verification, consultation and review costs.

There is no maintainer-recruitment dependency. Published project decisions and documented behaviour provide reference evidence, not owner approval of newly generated rules. Unrecorded organisational intent, owner certification, adoption, ongoing renewal and production economics remain outside the technical claim. A positive result would support the layer in the situations tested, not prove its universal necessity or the full playbook loop.

## 2. Current evidence and repository selection

The inventory is complete: **84 candidate records**, including **52 candidates to develop across 39 named decision families**, 15 controls, six deferred records, four calibration cases, three merged records and four rejected records. Six advancing candidates belong to the original development audit; excluding those leaves 46 new advancing candidates across 33 families. The original twelve audited cases remain development material.

Fifteen new local development checks passed. These are checks of selected implementation behaviour, not agent comparisons, end-to-end application validation or isolation tests. There have been **zero blinded model runs**.

| Project | Pinned source | Why it is in the candidate pool |
|---|---|---|
| NetBox | `ea4c205a37baa3e58e6e481158c15c6154cceeff` | Infrastructure conventions, permissions, change history and background jobs; continuity with earlier work. |
| Wagtail | `bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417` | Publishing, revisions, representations, permissions and extension boundaries. |
| Paperless-ngx | `835c4e51d0b145007bfac934009713dd8bbf3598` | Document processing, ordered workflows, ownership and parser boundaries. |
| HTTPX | `b5addb64f0161ff6bfe94c124ef76f6a1fba5254` | A library outside Django, with request lifecycles, transports and relatively inexpensive local checks. |

All four use Python and three use Django. This is purposive selection, not a representative sample of engineering organisations. A repository enters the runnable pilot only after its selected cases and dependencies pass validation. The earlier fact graph and ticket screens are reusable preparation assets, not evidence that the redesigned test is ready.

## 3. Build eligible cases before selecting a confirmation sample

For each candidate, record the published reference, corresponding implementation, relevant exceptions, any disagreement, the decision family, a proposed change task, disclosure risks and the screening decision. Find reference evidence before evaluating generated guidance; do not construct the answer key from the layer's output.

Published documentation is not unquestionable truth. Reconcile disagreements with implementation before scoring, and distinguish observed behaviour, recommendations, enforceable constraints and commitments that code cannot establish. Preserve a documented exception when available rather than rejecting an entire API category.

Each runnable case needs a meaningful incorrect change and at least one legitimate solution or exception. Test the evaluator against both. Simple API defaults and easily copied facts may calibrate the machinery but must not inflate the substantive inference result. Missing-authority cases test whether the layer declines to invent a commitment; they do not imply checking the support status of every interface on every call.

Resolve central dependency gaps or exclude the affected cases with a recorded reason. The current deferred records are W06, W14, W15, P12, P19 and H09. Pin the rest of each runnable environment as well.

Candidate counts do not establish statistical sufficiency. Related cases, semantic variants and repeated runs remain grouped under their underlying decisions. Any case used to tune prompts, rules or scoring against model outcomes becomes development material. The new inventory is investigator-visible and must not be described as an already sealed holdout.

## 4. Separate two information conditions

**Code-inference condition.** Withhold the project statements that reveal the target decision, together with alternative narrative disclosures. Review comments, docstrings, tests, examples, error messages, generated files, histories and dependencies for the same information. The allowed code may contain evidence from which the rule can be inferred. The case inventory, challenge labels, investigator discussion and reference answers must not reach the experimental drafter, coder or checker.

**Documentation-visible condition.** Supply the declared documentation as well as the code. Test extraction, interpretation of scope, conflict handling and recognition of authority. Guidance may cite the exact permitted guide section here. Results must not be blended with code-inference results and described as successful recovery from code.

These are information conditions crossed with the three treatment conditions below, not extra independent examples. Eligible cases may differ between information conditions; declare eligibility prospectively and report it. There is no fixed total run count yet.

Record guidance provenance at claim level: direct documentation extraction, executable-text restatement, structural or behavioural inference, or unresolved. Include permitted evidence references, scope, exceptions and counter-evidence. A string present in executable code is not automatically evidence of substantive inference.

## 5. Prepare and freeze the guidance

The drafter receives only its declared evidence, without the downstream task or reference assessment. It produces proposed rules, their scope, evidence and exceptions. Automated checks validate references and structure; a separately calibrated verifier assesses support and overclaims using only the permitted evidence. Retain rejected and disputed claims in the investigator record so verification costs and failure rates remain visible.

Freeze the resulting guidance before revealing downstream change tasks. Both guidance conditions receive identical guidance for a matched case and information condition. Do not repair that guidance using a hidden answer or feedback from the downstream scorer. Missing or incorrect guidance is an outcome, not a reason to quietly remove a case.

Website examples are illustrative. They are neither actual layer outputs nor final agent instructions and must not be copied into a blinded agent pack as presumed correct guidance. Actual guidance needs precise references, applicable APIs, requirements and exceptions, limited to evidence the agent is allowed to see.

## 6. Compare three approaches fairly

| ID | What the coding agent receives | Review and interaction |
|---|---|---|
| DIRECT | Task plus permitted code and documentation for that information condition. | Ordinary plan and code review using those sources. |
| GUIDE | The same sources plus the frozen generated guidance. | Ordinary plan and code review with that guidance available, without the structured layer consultation. |
| INTERACT | Exactly the same sources and frozen guidance as GUIDE. | Consultation with the layer and explicit checks of the proposed approach against applicable rules. |

The first comparison is GUIDE versus DIRECT. INTERACT versus GUIDE examines the additional structured interaction. INTERACT versus DIRECT describes the complete tested package. Choose the confirmatory primary comparison, endpoint and treatment of multiple comparisons before the main trial; the website's emphasis must not choose them retrospectively.

All three receive the same required review checkpoints, correction allowance, ordinary task tests and a predeclared overall resource cap. Use the same coding and review model settings across matched conditions unless a separately declared experiment tests model choice. The first two reviewers may identify rule violations through ordinary review; they must not be deliberately weakened to favour the layer.

Count drafting, verification, review and consultation effort. Record actual usage and completion at comparable budgets. If guidance is reused, report the number of tasks sharing its cost and show preparation costs separately. Add a small supplied-reference-rule diagnostic, reported separately, to check whether a task can benefit from correct guidance at all.

## 7. Proposed interactive procedure

The following is a **pilot default to build and validate**, not a claim that controls already exist.

1. **Consult and submit a plan before editing.** The coding agent asks what exists, what can be reused and which constraints apply. It submits the components it will change, the relevant rules and evidence, and any exception it intends to use.
2. **Review in a separate session.** The checker receives the task, submitted plan, current changes, permitted source material and applicable frozen guidance. It does not receive the coder's private reasoning, withheld reference documents or answer key. The check concerns whether the reasoning and proposed action respect the evidence, not whether a citation string is present.
3. **Return a decision with consequences.** The checker returns `proceed`, `revise` or `unresolved`, with a reason and relevant evidence. A revision can correct a violation or defend a legitimate alternative. The proposed allowance is **at most two correction rounds per checkpoint**, within the overall task budget. An unresolved decision or exhausted allowance stops the attempt; retain and assess unfinished work rather than calling the refusal a success.
4. **Recheck material changes.** The runner receives code submissions and compares them with the plan. A new dependency, different component to reuse, or newly claimed exception requires an updated plan before further work. Mechanical checks can detect some file or dependency changes; semantic review is still needed. Validate detection of undeclared changes rather than relying only on self-report. Required checkpoints and limits on submissions must be specified in the case/run configuration before the pilot.
5. **Keep evaluation separate.** Ordinary task checks are common across conditions. The independent evaluator sees the reference assessment after the run and judges the final code and whether interventions were justified. The runtime checker does not grade its own success, and hidden-test feedback must not leak back into a running condition.

The interactive treatment adds structured rule-specific questions to an otherwise credible review process. It is not an unrestricted conversation with an oracle or an extra pool of free model effort. Do not change frozen guidance during the run. Record every question, response, decision, revision and stop.

Humans prepare and review cases before runs and examine results afterwards. No unrecorded human intervention resolves a live attempt. Owner-authority questions remain unresolved in this technical test. Ongoing renewal and organisation-wide enforcement are outside this pilot.

## 8. Isolation and credibility requirements

Use a fresh container and fresh agent contexts for each condition and repetition, with the filesystem and network restricted to declared inputs and the logged model gateway. Keep grading outside. Verify the restrictions with negative tests, including attempts to reach withheld material, undeclared files and forbidden network destinations. Record complete model inputs and outputs, tool activity, source and container hashes, settings, versions, failures and exclusions.

Do not run a blinded drafter in the investigator conversation: this conversation has seen the answer material. Use unpublished changes that alter the correct rule to test whether answers follow supplied evidence, and meaning-preserving renamings to check robustness. Containers restrict runtime access; they cannot prove that a public repository was absent from training data.

Publishable audit records must be replayable and honest about this limit. Do not expose secrets or make materials public merely because an older attached plan said to publish. On 8 September 2026, the user requested publication of the current explanation and progress website through the POC GitHub repository as a rendered website. GitHub Pages is the public publication target; the separate Sites preview retains its existing access settings. This publication does not authorise disclosure of future withheld evaluation material or change the experimental method.

## 9. Outcomes, analysis and stopping

Report supported guidance, missed relevant rules within a declared audited scope, unsupported claims of authority, conflicts and exceptions separately. The inventory is not exhaustive and cannot supply a repository-wide recall denominator.

For downstream work, report task correctness, consequential rule violations, legitimate alternatives accepted, empty or unfinished changes and resource use. For interaction, also report missed violations, unnecessary objections, correction rounds and justified versus unjustified stops. No primary denominator may quietly discard unsuccessful or inactive attempts. Report infrastructure failures separately under a predeclared retry rule; that retry rule remains to be fixed.

Use paired comparisons with grouping for related decisions and repetitions. Report case-family and repository breakdowns, uncertainty and harm as well as benefits. The pilot is for validating tasks, scoring and feasibility; it does not inherit the old plan's significance threshold, equivalence margin or automatic extension rule.

Choose the minimum worthwhile improvement, acceptable additional cost, primary endpoint, analysis and confirmation sample size before confirmatory outcomes. Estimate variability and floor/ceiling effects from pilot work, not an optimistic pilot effect. Neither 52 rows nor 39 named families is a power calculation.

### 9A. Calibrate and validate the judges before trusting their scores

**Status: proposed validation protocol, not executed.** Calibration means developing the rubric and instructions on examples with established outcomes. Validation means testing the frozen judge on different examples whose expected verdicts were not used for that development. Neither a strong model name nor agreement between model judges is sufficient validation.

**Separate the roles.** The guidance verifier checks claims against the drafter's allowed evidence. The runtime checker decides whether to proceed, request revision or leave a question unresolved, using only its treatment's permitted inputs. The final outcome judge scores finished work using the independent reference assessment. Each role needs its own rubric and validation; passing one role's test does not qualify the others. An evaluator of intervention quality additionally examines whether objections were justified from the evidence available at that moment, rather than condemning a runtime checker for not knowing a withheld fact.

**Establish reference verdicts without asking the judge to certify itself.** For every calibration or validation item, preserve the pinned source, precise requirement, relevant exception, submitted patch or plan, expected verdict and evidence establishing that verdict. Use executable checks of observable behaviour wherever possible. Validate those checks with a known valid solution and a deliberately broken solution; an existing test suite passing does not prove it covers the target requirement. Published statements establish documented recommendations or commitments within their scope, not new owner approval. An AI may help construct an item, but its own explanation or another model's agreement cannot be the sole basis for the label. Record who or what independently checked it, including any lack of independent human review. If no qualified reviewer is available for a judgement that cannot be settled by reproducible behaviour or unambiguous reference evidence, keep that dimension exploratory and unresolved. Restrict confirmatory claims to dimensions with defensible reference verdicts.

**Build a challenging qualification set.** Include correct changes, seeded consequential errors, valid exceptions, different legitimate implementations, incomplete or empty changes, unsupported claims of authority and cases where the evidence is insufficient. Add misleading explanations: correct-looking citations accompanying wrong code, and a correct solution without persuasive prose. A NetBox history example could include preserving state before a direct edit, preserving it too late, and correctly relying on framework handling. These are illustrative designs, not constructed or validated fixtures. Mix deliberately constructed examples with independently checked natural development outputs; an exclusively synthetic suite may miss the mistakes agents actually make. The four simple inventory calibration records are starting material, not an adequate qualification set by themselves.

**Separate development from validation.** Assign whole decision families, including their variants, to rubric development or held-out judge validation before inspecting validation scores. Keep expected verdicts outside the judge input. A final outcome judge may receive reference requirements and test evidence, but never an item label saying whether this candidate should pass. Once a failed validation example is used to revise the judge, it becomes development material; use fresh held-out families for another qualification attempt. Keep judge qualification material out of the agent confirmation sample and prevent validation outputs from reaching experimental agents. Publish the split manifest, hashes and exposure history with the eventual audit record.

**Score specific claims, not presentation quality.** Prefer reproducible checks for behaviour. Use the model judge only for dimensions needing interpretation, with a per-criterion verdict of pass, fail or insufficient evidence and exact supporting references. An unresolved verdict must not disappear from denominators or silently count as a pass. Define in advance how mixed mechanical and model verdicts combine and how unresolved dimensions affect the primary endpoint. No fluent explanation can override a confirmed behavioural failure; investigate an apparent conflict as a possible fixture or judging error.

**Test bias and consistency.** Score final outcomes individually with treatment labels, model names, guidance files and persuasive agent summaries removed unless essential to the declared endpoint. Preserve the task, final code, relevant reference material and independently produced checks. Hide only irrelevant metadata, never evidence needed for a fair judgement; record residual clues that can reveal a treatment. Evaluate interaction transcripts separately because they can reveal the condition. On qualification material, test repeated grading, harmless formatting or identifier changes, misleading citations and instructions embedded in untrusted comments or explanations. If pairwise judging is used as a secondary check, reverse presentation order. Consider a different model family for an independent disagreement audit; this can expose shared assumptions but is not a replacement for reference evidence. Freeze its sampling and adjudication policy before outcomes.

**Measure both kinds of error and set a gate.** Report the fraction of actual violations passed, valid solutions rejected, appropriate and inappropriate unresolved verdicts, and verdict changes under repetition or irrelevant presentation changes. Break these down by criterion, severity, repository and decision family. Report denominators and uncertainty with grouping for related items; a pooled accuracy percentage can hide failure on rare but important errors. Set tolerable missed-error and false-objection rates, required precision, coverage and the qualification sample size before inspecting held-out validation outcomes. These numerical limits remain open and are a prerequisite to qualification, not a permission to select convenient thresholds later. Inspect every critical-error miss before accepting the affected scoring dimension. Do not claim an effect smaller than the judging uncertainty supports: test whether the apparent treatment benefit survives plausible adverse reclassification, including unequal judging errors between conditions.

**Freeze, audit and respond to failure.** Record the model version, instructions, rubric, input builder, executable checks, settings and verdict-combination rules before scored comparisons. During the pilot, audit a preselected sample spanning all conditions and verdict types against independent evidence; investigate all mechanical/model conflicts and critical-error disagreements. Record unresolved disputes rather than forcing agreement by majority vote. If the judge or rubric changes, version it, qualify it again and regrade all affected matched conditions under the same version. Preserve old scores and amendment history. If reliability remains inadequate, narrow the scored claim to validated checks or report the affected result as inconclusive. Do not keep running a confirmation trial with an unqualified primary judge.

This design draws on the distinction between code, model and human graders in [Anthropic's agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), and the observed position, verbosity and self-preference biases in [Zheng et al., Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685). These sources motivate controls; they do not validate this POC's judge.

## 10. Execution sequence and current state

### Immediate next step: specify the components and build one complete development case

**Recorded next preparation step, agreed on 5 September 2026. Not completed.** The current design is sufficient to begin a prototype, but it is not a complete implementation specification for the verifier, checker and judge. Write the missing behavioural contracts and exercise them on one complete case before expanding the implementation or attempting independent qualification.

The specification must define:

- **Verifier:** claim and evidence format, sufficient support, contradictions, exceptions, unresolved claims, and the conditions for admitting a claim to the frozen guide.
- **Checker:** initial consultation and targeted questions, the distinction between revise and unresolved, changed-plan triggers, the proposed correction limit, and the exact difference from ordinary review in DIRECT and GUIDE.
- **Judge:** case-specific scoring criteria, how mechanical and model judgements combine, and the treatment of incomplete work and insufficient evidence.
- **Shared controls:** explicit input and output records, allowed files for each role, enforced information boundaries, logging, failure handling, versioned instructions and model settings. Demonstrate the boundaries with attempts to access prohibited inputs.

The worked case must contain the pinned evidence, a concrete task, a valid solution, a deliberate consequential mistake, a valid exception or alternative, expected verifier/checker/judge decisions, and independent evidence supporting those expectations. It should demonstrate preparation and verification of guidance, its use during the task, intervention on a changed approach, and final assessment. Keep the evaluator's reference material outside every experimental component that is not permitted to see it. A manually traced case or scripted output may help develop the specification but must not be reported as a model run.

The completion record should show what each component received, what it returned, and whether those results matched the justified expectations. Label the case and all tuning outputs as development material. It cannot count as independent qualification or evidence that the layer improves outcomes. Exact models, budgets, validation sample and acceptance thresholds may remain open while the surrounding software is built, but must be fixed before their corresponding qualification or scored runs.

The user requested this next step to be recorded; this update records the sequence and does not claim that the specification or worked case has been built.

| Stage | Required work | Current state |
|---|---|---|
| Frame and inventory | Review the playbook claim, inspect references and select candidate repositories. | Completed as exploratory preparation. |
| Specify and trace one development case | Write component contracts and exercise the verifier, checker and judge on one complete evidence-backed case. | Agreed immediate preparation step; not complete. |
| Build pilot cases | Select a spread of decision families; resolve dependencies; construct tasks, alternatives and unpublished variants. | Not complete. Final case list and pilot size remain open. |
| Validate scoring and inputs | Establish reference verdicts, develop rubrics, qualify each judging role on held-out families under section 9A, and check semantic disclosures. | Protocol proposed; fixtures, numerical acceptance limits and qualification runs not complete. |
| Build and test the runner | Enforce inputs and checkpoints; test isolation, plan-change handling, logging and checker failures. | Not implemented as a complete blinded trial. |
| Fix pilot configuration | Record cases, inputs, models, prompts, budgets, correction limits, exclusions and retry policy before runs. | Not frozen. |
| Run the pilot | Execute fresh matched conditions; retain all attempts; move tuning material out of confirmation. | Not started. |
| Freeze and run confirmation | Specify final primary claims, endpoints, sample, grouping, thresholds and protocol before confirmation. | Not started. |
| Update the playbook | Report bounded conclusions, limitations, cost and negative or inconclusive results. | No effectiveness conclusion exists. |

Numerical settings still open include case count, repetitions, model budgets, reviewer settings, success thresholds and statistical precision. The two-correction-round proposal is the current pilot starting point, not an inherited ratified threshold. Updating this plan does not authorise unrequested paid runs or freeze the experiment.

## 11. Keep the plan, implementation and description aligned

For each change discussed in the working conversation, classify it before editing:

- **Presentation only:** typography, navigation, clearer wording or an illustrative example. Update the website without claiming that the experiment changed.
- **Method or scope:** inputs, arms, checkpoints, rule provenance, case eligibility, scoring, thresholds, costs or authority. Update this plan and the change register in the same work, then reflect it in the website and any affected runner specifications.
- **Completed work:** require an inspectable artifact or execution record before changing status. A described control is not an implemented control.

Record whether an item is a user constraint, a working proposal, an agreed decision, implemented, validated or frozen. Do not promote an assistant's suggested default to ratified status. Before a freeze, amendments are dated working revisions; after a freeze, preserve the previous protocol and record the amendment, reason, exposure to outcomes and affected runs before further collection.

The current change register is `plan_changes_2026-09-05.md`. A local consistency check compares the canonical plan with its POC, website and deliverable copies, including the GitHub website source and published Pages files. That check detects copy drift; semantic agreement between the prose and experimental design still requires review during each substantive edit.
