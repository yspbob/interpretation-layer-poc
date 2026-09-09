# Working pilot plan: interpretation-layer validation

Plan ID: **pilot-draft-2026-09-09.8**
Updated: **9 September 2026**
Status: **Working design for pilot preparation. Not a frozen preregistration, not an implemented experiment, and not a result.**

This document incorporates the research review and the subsequent website-design discussion. It is the current planning document for the redesigned POC. The previous ratified v1.2 plan is preserved as a historical record; its NetBox-only four-arm design, 25-ticket sample, 300-run schedule and success rule must not be silently inherited by this pilot.

The canonical working copy is now `preregistration/plan/working_plan_2026-09-05.md` in the POC repository. This consolidates the active project for work on two machines. The playbook project record and older local deliverables are historical snapshots. Identical current copies are maintained in this repository's website evidence downloads. The website explains this plan; it is not a separate source of experimental decisions. Its voice is factual and explanatory: it describes the process, decisions and reasons behind it, completed work and open choices. It does not adopt the playbook’s first-person voice for proposals and conclusions.

## 1. What this POC should establish

Chapter 4 proposes capturing evidence about a system, drafting guidance, obtaining owner approval, serving the relevant guidance during work, and checking compliance. We need evidence that the added technical machinery is useful rather than merely plausible.

The full proposal contains two connected cycles. Drafting, verification and owner review establish a version of guidance; consultation, planning, implementation and checking use that version across tasks. The first drafting cycle establishes a baseline. Subsequent evidence or decision changes can trigger review of affected guidance, without reopening every decision for every task. Observations from use can enter that review, but cannot themselves approve or silently rewrite a decision. This distinction clarifies the explanation; it does not add a maintenance experiment. The current pilot verifies support without owner certification and freezes guidance during each matched comparison. Ongoing maintenance remains outside scope.

The pilot has three questions:

1. Can the layer derive useful, appropriately qualified guidance from the sources it is allowed to see?
2. Does giving that guidance to an agent improve a later code change compared with a capable agent working directly from the same sources?
3. Does structured consultation and checking add value beyond supplying the guidance and providing ordinary review?

Keep inference quality, handling of documentation, downstream code quality and interaction effects separate. A correct explanation alone does not establish that the layer helps with engineering work. A benefit must also be considered against preparation, verification, consultation and review costs.

This first POC is designed to be as self-contained as possible, minimising external dependencies on project maintainers, organisational approvals and ongoing operational involvement. Public code and recorded decisions allow the technical mechanism to be tested without requiring that participation. Later iterations could involve owners and examine ongoing maintenance if the remaining research questions require them; neither is added to this pilot by this scope clarification.

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

**Assess the historical implementation too.** For every historical backtest, pin the starting revision, task, actual implementation of that task and the rules applicable at that time. Keep the target historical solution and its assessment outside experimental agent packs; audit later commits, tests and documentation for disclosures. The known implementation is a comparator, not an automatically correct answer. Establish task requirements, guardrail criteria, exceptions and reproducible checks independently of generated guidance before scoring either implementation. Record historical violations and unresolved disagreements rather than redefining the rules to excuse the original code. Do not retrospectively impose a rule that did not apply to the task. Authored development examples and semantic variants must remain labelled as such; H04 is not evidence that this historical comparison has been completed.

Each runnable case needs a valid solution, a meaningful incorrect change and an evidence-supported alternative or exception. A second valid solution can supply the alternative; do not invent an exception merely to fill a quota. Check that the assessment distinguishes them. Simple API defaults and easily copied facts may calibrate the machinery but must not inflate the substantive inference result. Missing-authority cases test whether the layer declines to invent a commitment; they do not imply checking the support status of every interface on every call.

**Keep the evidence in time.** The four inventory pins identify discovery snapshots, not the starting revisions of every future backtest. Each historical case needs its own starting revision, target change and dependencies. Separate requirements available when the task began from later evidence used only to assess it. Later documentation may corroborate an older rule only with evidence that it already applied; it cannot silently add a new obligation. Record whether the task states a target rule directly. Such a task can test application of an explicit requirement, but cannot establish downstream benefit from discovering that rule. Report authored tasks, historical backtests and unpublished variants separately. Controls that test only claim interpretation or missing authority are not automatically coding tasks and must not inflate the downstream task sample. A hidden, non-inferable policy cannot be treated as a discoverable obligation in the code-inference condition; score evidence handling within what that condition can establish.

**Distinguish a pattern from an obligation.** Observed code can establish behaviour or a structural regularity. Requiring later code to copy that regularity needs an applicable published constraint or a demonstrated consequence for the task. A recommendation is not automatically a mandatory guardrail. The case assessment records the basis and severity of each requirement before either implementation is scored.

Resolve central dependency gaps or exclude the affected cases with a recorded reason. The current deferred records are W06, W14, W15, P12, P19 and H09. Pin the rest of each runnable environment as well.

Candidate counts do not establish statistical sufficiency. Related cases, semantic variants and repeated runs remain grouped under their underlying decisions. Any case used to tune prompts, rules or scoring against model outcomes becomes development material. The new inventory is investigator-visible and must not be described as an already sealed holdout.

## 4. Separate two information conditions

**Preserve actual project instructions.** Use the project's actual `AGENTS.md` files from the backtest's starting revision, including applicable directory-specific instructions. Record paths, scope and hashes, or absence when no file exists. The same applicable files must reach DIRECT, GUIDE and INTERACT; the drafter and verifier use the corresponding permitted project evidence. Do not invent substitute instructions, take later revisions or remove real instructions to weaken the non-IL baseline. Project instructions do not grant access beyond the experiment's role and containment contract.

If these instructions state the target rule, classify the case as documentation-visible. It is not eligible for a code-inference claim for that rule. Keep the actual instructions intact and audit other disclosures for any case selected for code inference. Any separate redaction diagnostic would require a separately declared design; it is not the ordinary baseline.

**Code-inference condition.** Select cases whose applicable AGENTS.md instructions do not disclose the target rule. Withhold other project statements that reveal the target decision, together with alternative narrative disclosures. Review comments, docstrings, tests, examples, error messages, generated files, histories and dependencies for the same information. The allowed code may contain evidence from which the rule can be inferred. The case inventory, challenge labels, investigator discussion and reference answers must not reach the experimental drafter, coder or checker.

**Documentation-visible condition.** Supply the declared documentation as well as the code. Test extraction, interpretation of scope, conflict handling and recognition of authority. Guidance may cite the exact permitted guide section here. Results must not be blended with code-inference results and described as successful recovery from code.

These are information conditions crossed with the three treatment conditions below, not extra independent examples. Eligible cases may differ between information conditions; declare eligibility prospectively and report it. There is no fixed total run count yet.

Record guidance provenance at claim level: direct documentation extraction, executable-text restatement, structural or behavioural inference, or unresolved. Include permitted evidence references, scope, exceptions and counter-evidence. A string present in executable code is not automatically evidence of substantive inference.

## 5. Prepare and freeze the guidance

The drafter receives only its declared evidence, without the downstream task or reference assessment. It produces proposed rules, their scope, evidence and exceptions. Automated checks validate references and structure; a separately calibrated verifier assesses support and overclaims using only the permitted evidence. Retain rejected and disputed claims in the investigator record so verification costs and failure rates remain visible.

Select the drafter's source scope by a recorded, task-neutral rule, such as a declared subsystem at the starting revision. Do not select filenames, excerpts or questions using the hidden solution and then describe the pack as task-blind. Record the scope, any unavoidable clues and the tasks intended to share its guide. The same source scope remains available to every coding group.

Set a preparation budget, claim/revision limits and a stopping rule before drafting. The verifier may admit, reject or mark a claim unresolved; only admitted claim versions enter the guide. Any revised claim must be checked again. On exhaustion, freeze the admitted subset, including an empty guide when nothing was admitted. Run both guidance treatments with that same result and retain the preparation failure; do not regenerate until a helpful guide appears. An integrity failure is handled separately under section 9.

Freeze the resulting guidance before revealing downstream change tasks. Both guidance conditions receive identical guidance for a matched case and information condition. Do not repair that guidance using a hidden answer or feedback from the downstream scorer. Missing or incorrect guidance is an outcome, not a reason to quietly remove a case.

Website examples are illustrative. They are neither actual layer outputs nor final agent instructions and must not be copied into a blinded agent pack as presumed correct guidance. Actual guidance needs precise references, applicable APIs, requirements and exceptions, limited to evidence the agent is allowed to see.

## 6. Compare three approaches fairly

| ID | What the coding agent receives | Review and interaction |
|---|---|---|
| DIRECT | Task plus permitted code, documentation and actual applicable AGENTS.md instructions for that information condition. | Ordinary plan and code review using those sources. |
| GUIDE | The same sources plus the frozen generated guidance. | Ordinary plan and code review with that guidance available, without the structured layer consultation. |
| INTERACT | Exactly the same sources and frozen guidance as GUIDE. | Consultation with the layer and explicit checks of the proposed approach against applicable rules. |

The first comparison is GUIDE versus DIRECT. INTERACT versus GUIDE examines the additional structured interaction. INTERACT versus DIRECT describes the complete tested package. Choose the confirmatory primary comparison, endpoint and treatment of multiple comparisons before the main trial; the website's emphasis must not choose them retrospectively.

All three receive the same review-trigger policy, correction allowance, ordinary task tests, tools and a predeclared overall resource cap. Use the same coding and review model settings across matched conditions unless a separately declared experiment tests model choice. The first two reviewers may identify rule violations through ordinary review; they must not be deliberately weakened to favour the layer. Every group receives review. DIRECT uses the permitted sources; GUIDE adds the frozen guidance; INTERACT additionally uses targeted questions about applicable rules, compliance and legitimate exceptions. Ordinary reviewers may ask useful questions too; INTERACT makes the rule-and-exception exchange a required structured step. Its effect concerns that package, not proof that any single question caused an improvement.

**Charge preparation to the method that uses it.** The working budget policy is an equal total method allowance for each matched task, including its allocated drafting and verification cost plus coding, consultation, ordinary review and tool execution. Declare the accounting unit, prices and allocation before runs. With a guide reused across a predeclared set of N tasks, allocate its preparation cost equally across all N, including failed or unfinished tasks; otherwise charge the full cost to one task. GUIDE and INTERACT each carry that same attributed preparation cost even when the experiment physically generates their shared guide once. Report actual experiment spend separately to avoid double-counting that shared invocation. A preparation allocation reduces the remaining work allowance; it is not free extra effort. Budget exhaustion remains an outcome.

Report preparation, per-task usage, latency and researcher effort separately, including the first-use cost and declared reuse assumption. Final evaluation and building research fixtures are study costs, outside the agents' method allowance, and must still be reported. An additional comparison with equal execution-only budgets would answer a different question and must be separately declared. Exact amounts and operational time/call limits remain open. Add a small supplied-reference-rule diagnostic, reported separately, to check whether a task can benefit from correct guidance at all.

Match attempts by task, starting snapshot, information condition and replicate. Randomise or counterbalance treatment execution order before running the block, with fresh state and unchanged model settings. Do not always run the most assisted group last. If an unpinnable model service changes or the environment drifts, record it and apply the predeclared block/retry rule. Related tasks, repeated attempts and tasks sharing generated guidance are correlated; retain these group identifiers for analysis. Describe the documentation-visible baseline as existing project practice within the permitted scope, not a comparison against newly written expert guidance or every possible harness.

## 7. Proposed interactive procedure

The following is a **pilot default to build and validate**, not a claim that controls already exist.

1. **Consult and submit a plan before editing.** The coding agent asks what exists, what can be reused and which constraints apply. It submits the components it will change, the relevant rules and evidence, and any exception it intends to use.
2. **Review in a separate session.** The checker receives the task, submitted plan, current changes, permitted source material and applicable frozen guidance. It does not receive the coder's private reasoning, withheld reference documents or answer key. The check concerns whether the reasoning and proposed action respect the evidence, not whether a citation string is present.
3. **Return a decision with consequences.** The checker returns `proceed`, `revise` or `unresolved`, with a reason and relevant evidence. A revision can correct a violation or defend a legitimate alternative. The proposed allowance is **at most two correction rounds per checkpoint**, within the overall task budget. An unresolved decision or exhausted allowance stops the attempt; retain and assess unfinished work rather than calling the refusal a success.
4. **Check during implementation and recheck material changes.** The runner checks incoming code submissions against the approved plan while the task is in progress. At preconfigured review checkpoints and whenever a material change is detected, it pauses further work and sends the relevant plan and changes to the reviewer. Work resumes only after the required decision permits it. These in-run checks are triggered by submissions and detected changes, not an assertion of continuous semantic inspection. Matched groups receive the same checkpoint opportunities and limits. A new dependency, different component to reuse, or newly claimed exception requires an updated plan before further work. Mechanical checks can detect some file or dependency changes; semantic review is still needed. Validate detection of undeclared changes rather than relying only on self-report. Required checkpoints and limits on submissions must be specified in the case/run configuration before the pilot.
5. **Keep evaluation separate.** Ordinary task checks are common across conditions. After the run, the independent evaluator assesses historical and agent implementations against the same pre-established task requirements and guardrails, records justified improvements over the historical code, and separately judges whether interventions were justified. The runtime checker does not grade its own success, and hidden-test feedback must not leak back into a running condition.

Every attempt has an initial-plan checkpoint and a final-submission review before it is marked complete, with the same correction allowance. Intermediate checks use the same predeclared triggers and limits in all groups. Different code paths may cause different numbers or times of checks; equality means the policy and opportunity, not identical transcripts. The controller applies common mechanical triggers without treatment-specific thresholds, and qualified review covers the declared semantic scope. At a pause, no new coding turn or mutating tool action is dispatched until the review decision permits it. Pending work must be stopped or drained into an immutable submission under the runner contract. A final review can request correction; independent scoring happens only after the attempt becomes terminal.

An unresolved issue stops the attempt only when it prevents a necessary decision. An unrelated unknown is recorded without blocking valid work. A checker can identify a mistake in the frozen guide and request a source-supported correction to the proposed action; it cannot edit the guide or treat it as superior to its evidence. The later assessment records that guidance defect separately.

The interactive treatment adds structured rule-specific questions to an otherwise credible review process. It is not an unrestricted conversation with an oracle or an extra pool of free model effort. Do not change frozen guidance during the run. Record every question, response, decision, revision and stop.

Humans prepare and review cases before runs and examine results afterwards. No unrecorded human intervention resolves a live attempt. Owner-authority questions remain unresolved in this technical test. Ongoing renewal and organisation-wide enforcement are outside this pilot.

## 8. Isolation and credibility requirements

**Required before model runs; not implemented or validated.** Containment must be enforced outside the agents. Fresh conversations and instructions alone do not establish separation. In the July 2026 Hugging Face incident, agents used a shared package service as an unauthorised message board and obtained internet access through that service, as described in [OpenAI's retrospective](https://openai.com/index/hugging-face-incident-and-the-road-ahead/). [Hugging Face's technical account](https://huggingface.co/blog/agent-intrusion-technical-timeline) describes the subsequent intrusion. These reports motivate the requirements below; they do not validate this POC's controls.

- **Separate every role and run.** Use fresh contexts and isolated execution environments for each role, condition and repetition. Supply immutable, hashed input packs and private temporary storage. Do not expose shared writable caches, workspaces, another agent's history, host mounts or administrative sockets. Destroy temporary execution state after retaining the required audit evidence outside it.
- **Restrict and record communication.** Permit only declared, schema-validated exchanges through a controller outside the agent environments. Bind each exchange to its run, role and checkpoint. Deny other network access by default, including local networks, host services, metadata endpoints and indirect access through supporting services. Keep model credentials in the external logged gateway. The design must avoid relying on a single workload or supporting service to prevent wider access. Schema validation controls the permitted route and message structure; it does not certify message content as trustworthy or prove that every possible covert route is absent.
- **Minimise and test exposed services.** Inventory every tool, filesystem mount, storage service, network endpoint and supporting capability available to an agent. Expose only what its task requires, review each capability for unintended host access or communication, and test the boundary again after relevant changes. Pinned, preinstalled read-only dependencies are one implementation measure; package services are not the entire threat model. A required environment change stops the attempt for a recorded revision rather than granting ad hoc broader access.
- **Protect evaluation and enforcement.** Keep hidden references and scoring authority outside the coder and runtime reviewers. Give the final judge only its declared assessment pack. Execute candidate code in a separate restricted environment so it cannot read the full answer store or alter the scorer. Keep permissions, controller configuration, credentials, audit logs and stop controls outside all agent-writable environments; treat submitted artifacts and outputs as untrusted data.
- **Test the boundaries before authorising model calls.** Use model-free adversarial probes in controlled local fixtures to test forbidden file and answer access, cross-role and cross-run messages, shared-cache writes, direct and indirect network access, credential exposure, controller tampering and stop enforcement. Record the tested paths, environment configuration and observed denials. Do not test against third-party systems. Repeat the relevant checks after boundary or dependency changes.
- **Stop on containment failure.** An external supervisor must stop affected runs, retain evidence and invalidate affected matched comparisons when an unauthorised boundary crossing is detected or required enforcement fails. Investigate the scope before restarting in clean environments under a recorded retry decision. Preserve failed attempts in the audit record; do not report a containment failure as a task success or silently continue with broader access.

Record complete model inputs and outputs, tool activity, source and environment hashes, settings, versions, failures and exclusions. The existing file-broker checks establish only narrow input-handling behaviour. The isolated runner must demonstrate these requirements before model qualification or experimental runs. Report protection against specified, tested escape paths and remaining limitations; do not claim guaranteed containment or treat a container label as evidence of security.

Do not run a blinded drafter in the investigator conversation: this conversation has seen the answer material. Use unpublished changes that alter the correct rule to test whether answers follow supplied evidence, and meaning-preserving renamings to check robustness. Containers restrict runtime access; they cannot prove that a public repository was absent from training data.

Publishable audit records must be replayable and honest about this limit. Do not expose secrets or make materials public merely because an older attached plan said to publish. On 8 September 2026, the user requested publication of the current explanation and progress website through the POC GitHub repository as a rendered website. GitHub Pages is the public publication target; the separate Sites preview retains its existing access settings. This publication does not authorise disclosure of future withheld evaluation material or change the experimental method.

### 8A. Technical architecture and data flow

The required architecture separates the controller, role invocations, candidate-code execution and final evaluation. This is a design specification, not a completed deployment. Section 8C specifies VirtualBox, Ubuntu and rootless Podman as the proposed stack. Its implementation and qualification, and the provider gateway selection, remain open.

1. **Prepare immutable packs.** A pack builder selects pinned sources and actual applicable project instructions, adds only the role's permitted material, and produces a file/hash manifest. The target historical implementation and final assessment stay in a separate investigator store. The drafter has no downstream task; the verifier adds only proposed claims to the drafter's evidence.
2. **Dispatch through an external controller.** The runner binds exchanges to run, role and checkpoint IDs and tracks awaiting-plan, awaiting-review, work-permitted, revision and terminal states. It supplies matched opportunities and resource limits across treatments. The controller mediates every designed route between roles; agents cannot address one another or change its permissions. A separate model gateway holds credentials and records authorised calls and usage.
3. **Execute generated code separately.** A restricted workspace receives the submission and the checks appropriate to its phase. Common task checks may return permitted feedback; final-only observations reach evaluation after the attempt ends. Candidate code cannot access the full assessment store, host files, controller or administrative interfaces.
4. **Evaluate independently.** The scorer receives anonymised code, independently established requirements and test observations. An external comparison joins historical and agent criterion results. A separate intervention assessor reviews objections and stops against what the reviewer could know at that checkpoint. Final scores, withheld tests and historical solutions do not return to active experimental roles.
5. **Retain external audit records.** Record manifests, exact inputs/outputs, environment and model versions, tool actions, decisions, changes, stops and usage outside agent-writable storage. Reports exclude credentials and sealed material. Treat returned code, logs and artifacts as untrusted when collecting and processing them.

During execution, agents must have no general access to the host, other runs or external services. Narrowly defined routes for task input, review exchange and result collection are necessary and belong in the tested boundary. Literal zero interaction with the underlying host is not a defensible guarantee. The working design uses a disposable VirtualBox guest around rootless Podman execution; this is a proposed platform, not a validated boundary. Any chosen runtime must pass the section 8 probes and record residual limitations before model calls; no technology label substitutes for that evidence.

The controller, gateway, isolation runtime and evaluator form the trusted computing base and must be versioned and tested. The gateway accepts only bounded model requests with fixed provider destinations; it must not act as a generic URL fetcher or command proxy. Validate collected paths, symlinks, archives, output size and message sequencing outside the workload. Final code runs without the full reference store or candidate-writable grading logic; use external observations where feasible and probe forged success reports, test tampering and instructions embedded in outputs. These are required tests of the chosen implementation, not a claim that arbitrary hostile code can never defeat it.

### 8B. Tools, technologies and selection record

The following choices describe a working implementation direction, not a deployed or qualified stack. Preserve the distinction between the H04 rehearsal and the full experiment.

| Component | Working technology choice and rationale | Selection status |
|---|---|---|
| Runner | Python with a project-specific controller, extending the existing pack, checkpoint and result-recording code. Add an orchestration framework only if its benefits justify the additional dependencies and it preserves explicit dispatch and stop control. | Proposed; full runner not implemented. |
| Agent access | A provider API or SDK behind the external bounded gateway. It must expose the inputs, outputs, tool requests and usage needed for the audit and permit controller-enforced limits. | Provider, models, SDK and any agent framework remain to be selected. No model integration exists in H04. |
| Isolation | VirtualBox 7.2 series, Ubuntu Server 24.04 LTS amd64 and rootless Podman, with no guest network adapters, read-only ISO inputs and bounded serial output. See section 8C. | Proposed; exact releases, compatibility and containment remain to be validated on each host. |
| Assessment | Python-based behaviour probes and each project's relevant tests, plus separately qualified model assessments for interpretation. Use pinned dependencies and the appropriate test environment for each historical case. | Proposed architecture; H04 supplies narrow scripted checks only. |
| Records | JSON for structured run records, SHA-256 to identify exact artifacts, and Git/GitHub for reviewed public versions. Place credentials, sealed fixtures and protected audit records outside public Git and agent-writable storage. | JSON/hash records and public Git already support H04. A separate private GitHub repository is the user-selected design for sealed fixtures and confidential records; it has not been created. Credentials remain local. |

**Implemented development tools.** The H04 record reports Python 3.12.14 on Windows. Its custom runner uses `asyncio`, HTTPX `MockTransport`, Python assertions and a narrow `ast` comparison of known lifecycle calls and `finally` blocks. It writes JSON observations and hashed role packs. These tools do not implement model invocation, OS isolation or general semantic change detection. Exact dependency pins are in [requirements.txt](https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/h04-response-lifetime/requirements.txt), observed versions in [recorded-results.json](https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/h04-response-lifetime/recorded-results.json), and reproduction commands in the [H04 README](https://github.com/yspbob/interpretation-layer-poc/tree/main/research/development/h04-response-lifetime).

**Selection and reproduction.** Before building the isolated runner, record the chosen runtime, controller interfaces, permitted tools and reasons for their selection. Before qualification, fix model/provider identifiers, SDK/framework versions, prompts and settings. Each run manifest records the runner commit, OS/runtime/image identifiers or digests, source and dependency pins, test commands, network/filesystem policy, configuration hashes, record locations and reproduction command. Provider versions that cannot be fixed must be disclosed under section 6. Keep secrets out of manifests and public reports. A software upgrade affecting behaviour or boundaries requires the relevant checks again.

### 8C. Concrete execution design and two-machine continuity

The [isolated runner design v0.1](https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/isolated-runner-design-v0.1.md) specifies the proposed stack, threat model, preparation state, container restrictions, input/output contract, reset policy and qualification probes. It is an implementation design, not evidence of containment. The laptop has 32 GB RAM and the home PC has 64 GB; the home PC is not permanently available. Either machine should execute locally, with the laptop as the common resource baseline. The laptop's Windows Home edition rules out assuming the Windows Hyper-V role. VirtualBox compatibility with its actual Windows backend, and the home PC's capabilities, require checks before installation and execution.

Run one worker VM at a time. Supply only allowlisted files on a read-only ISO and collect bounded structured output through a virtual serial port connected to a Windows named pipe. Disable all VM network adapters and host integration during execution. Run generated tools/code in rootless Podman inside the guest; model calls occur through the external Windows controller and provider gateway. No generated command executes on the Windows host. The serial interface and parser remain exposed boundaries requiring adversarial tests; this is not a claim of zero physical host interaction.

Each agent role also has a separate provider context, permitted history and tool workspace, keyed to its role, attempt and treatment. No shared provider memory, retrieval index, browser/tool session or writable role cache is permitted. Disable provider-hosted tools unless they can meet the same reviewed boundaries. The controller alone selects recipients and builds allowlisted payloads; private assessment material never enters working-role packs. Test role spoofing, stale sessions and forbidden-pack markers as well as code isolation.

Use a fresh guest clone and restricted container for every bounded tool batch. Carry forward only validated workspace files, with no persistent processes or shared writable caches. Stop execution before review, enforce terminal states externally, and record reset overhead under the same policy for all treatments. The initial model-free profile proposes a 4-vCPU/8-GiB VM and a 2-CPU/4-GiB worker; storage, process, time and output limits are specified in the design for testing. These are provisional engineering settings, not frozen experimental allowances.

Complete each matched DIRECT/GUIDE/INTERACT block on one host. Before continuing on the other, verify public and private revisions, installed environment/image hashes and host-specific qualification evidence. Record host grouping and timing; equal limits do not imply equal CPU speed. Interrupted blocks retain their original records and follow a predeclared whole-block retry/exclusion policy, never an unrecorded move with renewed budgets.

A separate private GitHub repository will hold small sealed fixtures, confidential run bundles and the block ledger. Keep credentials local and VM/container storage outside Git. Verify private storage access and a successful reservation before starting a block, then save and verify its private evidence before the sanitised public progress update. The existing public sync helper does not implement private synchronisation. Large immutable image distribution requires a verified artifact source or demonstrated identical local build before cross-machine execution. No private repository creation, installation or model expenditure is authorised merely by recording this design.

## 9. Outcomes, analysis and stopping

For historical backtests, report **task correctness** and **guardrail compliance** separately for both the historical implementation and every agent condition. Apply identical, independently established criteria and evidence-backed exceptions. Record per-criterion results and the difference from the historical implementation. If the agent avoids a confirmed historical violation while delivering the required behaviour, count that in its favour; do not penalise a legitimate alternative for code differences. Record newly introduced violations and behavioural regressions as adverse outcomes. Compliance gains must not conceal a failure to complete the task correctly. Unsupported or disputed rules remain unresolved and cannot create improvement credit.

The historical implementation is a comparator, not a fourth treatment or an extra independent case. The main treatment comparisons remain DIRECT, GUIDE and INTERACT. Exact points, weights, aggregation and handling of unresolved criteria remain open and must be fixed before the relevant scored runs. This decision requires assessment of the historical code and qualification cases where the agent improves on it; no such comparison is claimed by the existing H04 rehearsal.

Report supported guidance, missed relevant rules within a declared audited scope, unsupported claims of authority, conflicts and exceptions separately. The inventory is not exhaustive and cannot supply a repository-wide recall denominator.

For downstream work, report task correctness, consequential rule violations, legitimate alternatives accepted, empty or unfinished changes and resource use. For interaction, also report missed violations, unnecessary objections, correction rounds and justified versus unjustified stops. No primary denominator may quietly discard unsuccessful or inactive attempts. Report infrastructure failures separately under a predeclared retry rule; that retry rule remains to be fixed.

Use per-criterion `pass`, `fail` or `insufficient_evidence`, with an applicability field and an evidence-backed reason for any criterion marked not applicable. A valid exception satisfies or removes the obligation within its documented scope; it does not earn a penalty for departing from preferred code. A confirmed required-behaviour failure prevents a successful-task claim. Missing evidence cannot silently become a pass. Publish correctness and guardrail results without a single weighted score until points and aggregation have been fixed. If the evidence cannot resolve a requirement central to the task, the case cannot support that confirmatory endpoint; retain its unresolved result in the research record.

**Separate agent failure from infrastructure failure.** Invalid output produced by an agent, refusal, missing submissions, exhausted budgets and unsupported answers are method outcomes, not automatic infrastructure exclusions. A demonstrable external outage, corrupted input pack or failed isolation boundary is an infrastructure/integrity event. Record the cause and affected matched block; unknown attribution stays explicit. Define retry eligibility and limits before runs, never retry merely for an unfavourable score, and preserve the original attempt. Report all scheduled and started attempts, valid matched comparisons, exclusions and retries by group. Excluding an invalid block from the causal comparison does not remove it from the operational failure report.

Use paired comparisons with grouping for related decisions, repetitions and shared guidance. Report information conditions and historical/authored/variant task types separately, alongside case-family and repository breakdowns, uncertainty and harm. Do not attribute differences between two information conditions to documentation alone when their eligible tasks differ. The pilot is for validating tasks, scoring and feasibility; it does not inherit the old plan's significance threshold, equivalence margin or automatic extension rule.

Choose the minimum worthwhile improvement, acceptable additional cost, primary endpoint, analysis and confirmation sample size before confirmatory outcomes. Estimate variability and floor/ceiling effects from pilot work, not an optimistic pilot effect. Neither 52 rows nor 39 named families is a power calculation.

### 9A. Establish whether each assessment role is reliable

**Working qualification procedure; not executed.** Qualification establishes fitness for a specified role and scope. It does not certify general intelligence or the correctness of every future judgement. Mechanical checks need validation too.

#### 1. Define the role and the evidence it may use

| Role | Decision to qualify | Examples of errors to measure |
|---|---|---|
| Guidance verifier, during preparation | Admit, reject or leave a proposed claim unresolved using only the drafter's evidence. | Admitting an unsupported obligation; rejecting a supported scoped claim; overlooking an exception. |
| Ordinary reviewer and interactive checker, during work | Proceed, request a revision or stop on a necessary unresolved decision, using that group's permitted inputs. | Missing a consequential error; blocking a valid alternative; claiming access to hidden evidence. Qualify each treatment's actual review instructions. |
| Guidance assessor, after preparation is frozen | Assess support, scope, provenance and omissions in a declared audited scope, using the separately prepared reference assessment. | Accepting an invented rule or authority claim; treating copied text as inference; inventing a repository-wide recall denominator. |
| Final code judge, after the attempt ends | Assess each historical or agent implementation against task requirements and applicable guardrails. | Passing broken behaviour; penalising a valid alternative; excusing a violation because historical code also contains it. |
| Intervention assessor, after the attempt ends | Assess whether an objection, correction request or stop was justified by the evidence available at that checkpoint. | Treating every objection as useful; judging a review by facts it could not see; mistaking later success for proof that an intervention caused it. |

These are separate assessment jobs, not necessarily five different model products. Keep their contexts and outputs separate. The verifier's admission decision is part of the treatment; it cannot serve as the independent score of that treatment's guidance. A model/version passing one role does not qualify its other roles or different input permissions.

#### 2. Establish the expected assessment before testing the assessor

For each item, create an evidence record containing the source and dependency revisions, submitted claim/plan/code, applicable criterion and severity, legitimate exceptions, expected decision, and the evidence supporting it. Record which facts were available to the role at that point. Historical code is evidence to examine, not an automatic answer key.

Use executable observations for behavioural requirements. Check the test with a valid implementation and a deliberately wrong one; passing an unrelated existing suite is insufficient. For a documented obligation, identify the exact statement, its scope and why it applied at that time. A repeated code pattern alone cannot establish organisational authority. Record who or what checked the expected assessment, including the absence of independent human review.

An AI may help prepare an item, but its explanation or another model's agreement cannot be the sole justification for the label. Without a qualified person to resolve an ambiguous interpretation, rely on reproducible behaviour or unambiguous source evidence, or keep that dimension unresolved. Only dimensions with defensible expected assessments can support confirmation.

#### 3. Develop instructions, then test on unused decision families

Allocate whole families and their variants to development, qualification or experimental confirmation, with hashes and exposure records. Judge development and pilot tuning material cannot also validate the revised judge or support confirmation. Keep expected candidate labels out of all judge inputs. Reference criteria and test observations may be supplied only to roles entitled to receive them.

Develop the rubric and input format on development examples. Include correct work, consequential errors, legitimate alternatives, empty or unfinished work, missing evidence and unsupported authority. The suite must include historical violations avoided by a correct agent solution, and apparent compliance improvements that break behaviour. Include misleading citations, instructions embedded in candidate material, repeated grading and harmless presentation changes. Mix authored examples with independently checked natural outputs when available; qualify only the coverage actually represented.

Before opening qualification results, freeze the model/settings, instructions, input builder, checks, verdict-combination rules, split, sample size and acceptance limits. If a failed qualification item informs a revision, move its family into development and use fresh families for the next qualification. Do not repeatedly tune against a nominal holdout.

#### 4. Measure errors with explicit denominators

Count separately: confirmed violations accepted; valid work rejected; justified unresolved decisions; unnecessary unresolved decisions; and verdict changes under repetition or irrelevant presentation changes. Report the number of eligible examples for each rate, grouped by family, criterion and severity. State coverage gaps and uncertainty; a pooled accuracy figure cannot establish reliability on rare serious errors.

For each role, the qualification specification must contain maximum tolerated error rates, required precision, minimum coverage and the decision rule for passing. These values are still open and must be fixed before qualification results are inspected. The report applies that rule and lists every exception or critical miss. An unfilled specification is a failed readiness gate, not permission to run and choose convenient thresholds afterwards.

A reproducible behavioural failure cannot be overridden by fluent model reasoning. Investigate conflicts as possible errors in the fixture or assessment. An unresolved result remains in its denominator. Combine per-criterion results using the rules frozen for that experiment; no compliance score may conceal failure of required behaviour.

#### 5. Remove irrelevant clues and keep the assessments separate

Score code individually without origin, treatment or model labels, generated guides or persuasive agent summaries. Retain the evidence needed to judge it fairly, and record clues that cannot be removed. The controller holds the mapping needed to join scores afterwards. Guidance and interaction assessments use separate inputs; a transcript may reveal the group, so it cannot be described as fully blinded.

On qualification material, repeat grading, vary harmless presentation and, for any secondary pairwise comparison, reverse order. A different model family can help find disagreements, but cannot replace evidence. The reference record must support the answer without asking an assessor to certify itself. Intervention quality measures whether the review was justified; treatment comparisons, not an individual successful correction, estimate the benefit of interaction.

#### 6. Audit results and handle changes without moving the target

Before pilot scoring, specify an audit sample covering all groups and verdict types, the adjudication method and the response to disagreements. Investigate all mechanical/model conflicts and critical-error disagreements. Retain old scores, unresolved disputes and versions.

If a new valid alternative exposes a flaw in the criteria, document the source evidence and amendment. If the rubric, tests, model or instructions change, qualify the affected roles again and rescore every affected matched condition, including historical comparators, under the same version. Material used for the repair becomes development material. A confirmation result repaired using its own outcomes is exploratory; a new confirmatory claim requires fresh held-out families. If reliability is inadequate, narrow the claim to validated checks or report it as inconclusive.

The pilot must also test whether an apparent treatment benefit survives plausible adverse reclassification, including unequal judging errors between groups. Do not claim an effect smaller than the assessment uncertainty supports.

The use of distinct code, model and human assessment methods is informed by [Anthropic's agent-evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). Presentation and model-preference controls are motivated by [Zheng et al., Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685). These sources motivate the checks; they do not establish this experiment's reliability. Our evidence-only route is deliberately narrower where expert review is unavailable.

### 9B. Decisions that must be closed before the next stage

The investigator records each decision and its evidence in a versioned configuration. Publishing this working plan does not close these gates or authorise model expenditure.

| Before this activity | Required record | Status on 9 September 2026 |
|---|---|---|
| Implementing the isolated runner | Selected execution boundary, threat model, permitted interfaces, output collection, pause/stop semantics and probe plan. | Working architecture and interfaces proposed in section 8C; host compatibility, exact pins and implementation remain open. |
| Any model invocation, including qualification | Passed isolation/controller probes for the exact configuration; bounded gateway and logging; authorised budget. | Not established. |
| Held-out component qualification | Role-specific evidence records and splits, frozen instructions/settings, error definitions, numerical limits, sample size and acceptance rule. | Procedure specified; fixtures and numerical gates incomplete. |
| Pilot comparisons | Qualified components, eligible cases and disclosure audits, guidance preparation/reuse limits, matched budgets and order, scoring/stop/retry rules and audit configuration. | Not frozen; zero runs. |
| Main confirmation | Fresh families excluded from tuning, primary contrast and endpoint, minimum worthwhile benefit and cost limit, multiplicity/grouping analysis, repetitions and sample-size justification. | To be set using feasibility evidence before confirmation outcomes. |

## 10. Execution sequence and current state

### First development case completed; next build the isolated role runner

**Development milestone completed on 8 September 2026; model components and isolation remain unvalidated.** [Component contracts v0.1](https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/component-contracts-v0.1.md) and the [H04 response-lifetime case](https://github.com/yspbob/interpretation-layer-poc/tree/main/research/development/h04-response-lifetime) now provide a concrete task, pinned evidence, two valid implementations, two consequential errors, an unfinished implementation, prewritten reference verdicts and a scripted preparation/checking/final-assessment trace. All 25 behaviour comparisons matched their reference expectations. These are investigator-authored development examples and a mechanical replay, not model outputs or independent qualification.

The H04 development contracts and recorded trace cover the following. The later plan also requires independent guidance and intervention assessments, which H04 has not implemented:

- **Verifier:** claim and evidence format, sufficient support, contradictions, exceptions, unresolved claims, and the conditions for admitting a claim to the frozen guide.
- **Checker:** initial consultation and targeted questions, the distinction between revise and unresolved, changed-plan triggers, the proposed correction limit, and the exact difference from ordinary review in DIRECT and GUIDE.
- **Judge:** case-specific scoring criteria, how mechanical and model judgements combine, and the treatment of incomplete work and insufficient evidence.
- **Shared controls:** explicit input and output records, allowed files for each role, enforced information boundaries, logging, failure handling, versioned instructions and model settings. Demonstrate the boundaries with attempts to access prohibited inputs.

The worked case must contain the pinned evidence, a concrete task, a valid solution, a deliberate consequential mistake, a valid exception or alternative, expected verifier/checker/judge decisions, and independent evidence supporting those expectations. It should demonstrate preparation and verification of guidance, its use during the task, intervention on a changed approach, and final assessment. Keep the evaluator's reference material outside every experimental component that is not permitted to see it. A manually traced case or scripted output may help develop the specification but must not be reported as a model run.

The completion record should show what each component received, what it returned, and whether those results matched the justified expectations. Label the case and all tuning outputs as development material. It cannot count as independent qualification or evidence that the layer improves outcomes. Exact models, budgets, validation sample and acceptance thresholds may remain open while the surrounding software is built, but must be fixed before their corresponding qualification or scored runs.

The runnable prototype checks six control behaviours and records 71 denied file-broker requests, including traversal, prohibited inputs and tampering. It exports hashed documentation-visible drafter, verifier, coder/reviewer, checker and anonymised final-judge packs. A broker allowlist is not a sandbox: the investigator process still has filesystem access, and network/OS isolation has not been demonstrated. No code-inference pack has passed a disclosure audit. No model was called.

For this development case, any confirmed required behavioural failure makes the final result fail; otherwise missing evidence stays insufficient, and all required checks must pass for a scoped pass. Incomplete work fails completion. A second corrected submission may proceed, a further revise stops, and unresolved stops immediately. These are explicit development defaults, not a ratified confirmation endpoint. Scripted lifecycle-call and finally-structure comparisons detect the known candidate changes; general semantic detection and runner-enforced pauses remain open.

**Exact next step:** check and provision the proposed VirtualBox/Ubuntu/Podman stack on the laptop without weakening host security, then implement a model-free isolated role runner with structured record validation, immutable pack dispatch, the containment controls and adversarial checks in section 8, and enforced initial, changed-plan and final checkpoints. Use H04 as a regression case. Then prepare different families and fix the qualification coverage, error limits, model settings and budgets before authorised qualification calls. The development milestone remains the last implementation step. The subsequent website and plan reviews do not authorise model runs; the readiness gates in section 9B apply.

| Stage | Required work | Current state |
|---|---|---|
| Frame and inventory | Review the playbook claim, inspect references and select candidate repositories. | Completed as exploratory preparation. |
| Specify and trace one development case | Write component contracts and trace their inputs and decisions on one evidence-backed case. | H04 contracts, executable checks and scripted trace complete as development. No model role exercised or qualified. |
| Build and test the runner | Enforce inputs and checkpoints; test isolation, plan-change handling, logging and checker failures. | Narrow pack broker, state transitions and lifecycle triggers exercised in H04. Isolated dispatch and a complete blinded runner remain the next implementation work. |
| Build pilot cases | Select a spread of decision families; resolve dependencies; construct tasks, alternatives and unpublished variants. | Not complete. Final case list and pilot size remain open. |
| Validate scoring and inputs | Establish reference verdicts, develop rubrics, qualify each judging role on held-out families under section 9A, and check semantic disclosures. | Protocol proposed; fixtures, numerical acceptance limits and qualification runs not complete. |
| Fix pilot configuration | Record cases, inputs, models, prompts, budgets, correction limits, exclusions and retry policy before runs. | Not frozen. |
| Run the pilot | Execute fresh matched conditions; retain all attempts; move tuning material out of confirmation. | Not started. |
| Freeze and run confirmation | Specify final primary claims, endpoints, sample, grouping, thresholds and protocol before confirmation. | Not started. |
| Update the playbook | Report bounded conclusions, limitations, cost and negative or inconclusive results. | No effectiveness conclusion exists. |

Numerical settings still open include case count, repetitions, model budgets, reviewer settings, success thresholds and statistical precision. The two-correction-round proposal is the current pilot starting point, not an inherited ratified threshold. Updating this plan does not authorise unrequested paid runs or freeze the experiment.

## 11. Keep the plan, implementation and description aligned

The Experiment page describes the planned method, technical architecture, decision rationale, requirements and enduring limitations. Progress & findings owns completed work, validation results, implementation gaps, next actions and the inventory's readiness. Keep a brief planned-method label and identify provisional design choices without repeating component status throughout the explanation. The canonical plan retains both requirements and dated status for traceability.

For each change discussed in the working conversation, classify it before editing:

- **Presentation only:** typography, navigation, clearer wording or an illustrative example. Update the website without claiming that the experiment changed.
- **Method or scope:** inputs, arms, checkpoints, rule provenance, case eligibility, scoring, thresholds, costs or authority. Update this plan and the change register in the same work, then reflect it in the website and any affected runner specifications.
- **Completed work:** require an inspectable artifact or execution record before changing status. A described control is not an implemented control.

Record whether an item is a user constraint, a working proposal, an agreed decision, implemented, validated or frozen. Do not promote an assistant's suggested default to ratified status. Before a freeze, amendments are dated working revisions; after a freeze, preserve the previous protocol and record the amendment, reason, exposure to outcomes and affected runs before further collection.

The current change register is `plan_changes_2026-09-05.md`. Run `node scripts/sync-plan.mjs --check` from the repository root to compare this plan and register with the website source downloads and published Pages files. That check detects copy drift; semantic agreement between the prose and experimental design still requires review during each substantive edit.

For continuity across machines, Codex maintains `PROJECT_STATE.md` and saves reviewed files and decisions to GitHub at the end of a completed piece of work. The user does not need to request a handover. Quick exchanges that do not change the work require no separate save. These operational changes do not alter experimental conditions, qualify any component or authorize model runs.
