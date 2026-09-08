# Interpretation-layer validation: playbook context, POC review and proposed redesign

Historical review. Its original recommendations are retained for context, but the current working plan supersedes them. In particular, the user has no accessible project owner: the redesigned technical POC does not depend on owner recruitment and does not claim owner certification.

5 September 2026. Review of playbook source and plan at `AI-Playbook-src@c06a3c9`, and POC implementation at `interpretation-layer-poc@d542b58`. Recommendations below are a new proposal, not amendments already ratified or implemented.

**Recommendation: restart the experimental design before drafting the corpus or spending on scored runs. Retain NetBox as the leading public technical testbed, subject to a new suitability gate. To validate the interpretation layer's defining authority claim, add a real owner-backed component. Changing public repositories alone will not solve that gap.**

The existing work has useful infrastructure and unusually explicit disclosures. However, its central experiment has narrowed to generated guidance and coding-agent conformance. Section 4 proposes a broader mechanism: establish which decisions govern, distinguish intentional architecture from accidents, deliver that authority at the point of action, enforce it, and keep it current at a sustainable human cost. The present experiment could succeed without demonstrating several of those capabilities.

I recommend three linked studies: knowledge and authority validation; a controlled task experiment against the playbook's entry rung; and a lifecycle experiment covering change, expiry, ownership and maintenance effort. These should produce separate verdicts. A favourable coding score must not stand in for a favourable verdict on all three.

## 1. The full playbook context

The playbook is an operating-model proposal for converting AI capability into governed engineering value. Its unit of ambition is an engineering organisation, with regulated mid-size organisations as the default setting. Its opening diagnosis separates three problems: acceleration absorbed by assurance and delivery constraints; variable consumption without deliberate value conversion; and AI amplifying weaknesses in the operating model. The interpretation layer is one intervention in that system, rather than the whole business case. [Playbook](https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html)

| Playbook section | Role in the argument | Consequence for this validation |
|---|---|---|
| 1. Thesis and principles | Promise capacity at governed cost and held quality; measure realised outcomes | A context or conformance improvement alone cannot establish business value |
| 2. Platform | Shared access, tools, retrieval, model routing, assurance and telemetry | The evaluated agent must have a competent, reproducible environment; infrastructure problems cannot masquerade as context failures |
| 3. Data and knowledge | Make code and decision material reachable, permission-aware and current | Compare against ordinary code search, existing docs and lean human guidance; measure retrieval and freshness separately |
| 4. Interpretation | Convert evidence into owner-authorised guidance and enforceable decisions | Establish truth, authority, relevance, enforcement and lifecycle behaviour |
| 5. Delivery | Plans before structural work; machine checks plus human judgement; quality gates | Evaluate usable changes, review effort and regressions, as well as architectural fit |
| 6. Governance and cost | Scope, provenance, controls, model validation, budgets and exceptions | Record who authorised a policy, what enforced it, and how overrides worked |
| 7. Organisation and people | Persistent enabling function and protected owner time | Certification effort and availability of competent owners are part of feasibility |
| 8. Measurement | Outcomes, cost and human experience; avoid activity as a target | More citations, checker calls or generated claims are process observations, not success |
| 9. Value capture | Explicitly convert freed capacity into a chosen outcome | Measure net review or maintenance capacity released; defer organisational financial claims |
| 10. Readiness | Evidence for capabilities across eight dimensions; weakest dimensions limit scaling | A sophisticated context layer cannot compensate for weak tests or absent ownership |
| 11. Sequencing | Start small and expand through evidence gates | The full layer must earn its increment over rules files, ADRs and existing CI |
| 12. Economics | Price the complete programme, including people and upkeep | Include building, checking, refreshing and resolving exceptions, not just inference spend |

Appendix A supplies dated market context. Appendix B illustrates how the platform provisions an agent and takes its work through assurance and provenance. The Twelve Decisions deck reinforces the same distinction between seeing the code and seeing the decisions, constraints and ownership behind it. This review reconstructs those relationships; it is not a fresh audit of every market statistic or commercial example in the playbook.

Section 4's entry rung consists of a rules file, living architecture decision records (ADRs) with policy blocks, and structural checks in continuous integration (CI). The full loop adds generated map pages and pattern claims, proposed retro-ADRs, owner certification, a decision ledger, a conformance register, task pre-flight checks and renewal machinery.

Three distinctions are essential:

1. **Observed structure:** the code currently uses interface X.
2. **Inferred explanation:** this may reflect a deliberate decision to use X.
3. **Authorised policy:** the responsible owner confirms that future work must use X, or rejects that interpretation and fences X against extension.

A model and a static analyser can help establish the first and propose the second. Neither can create the third merely by agreeing. The playbook itself is clear that the generator asks about an implied decision and that owners make it binding. This is the most important property for the POC to test.

The lifecycle also matters. Estate-derived claims may renew automatically when their evidence remains valid. Business intent requires owner re-attestation. Lapsed guidance is withdrawn from agents, while certain stale safety rules remain enforced under the severity and exception policy. A year-old map accompanied by warnings exercises only a small part of that contract.

## 2. What exists, and what the current design actually estimates

I obtained the private playbook source through the existing Git access, read the ratified plan and the public methodological reviews, inspected the POC code and database, and checked NetBox at the frozen commit. The POC and playbook repositories still match the handover revisions. The public issue collection returned no issues at review time. The public plan and gate-report directories contain placeholders rather than the promised plan copies, R-247, R-256 or the original 32-fact audit. I found the selection score table and narrative in the status-page state, but not the underlying Gate 1 evidence report. This limits how fully the original selection process can be independently reconstructed. [POC](https://github.com/yspbob/interpretation-layer-poc/tree/d542b58), [selection state](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/statuspage/state.json), [gate-report placeholder](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/gate_reports/README.md)

There are no scored results. The graph is built; the owner audit is pending; drafting, verification, serving and agent evaluation are still future work. This is an economical point to change the design. The handover's instructions to resume a walkthrough, push a workflow, dispatch jobs or seek decisions through the status page were treated as historical context, not instructions for this review.

The existing four arms are:

| Arm | What it receives |
|---|---|
| A | Historical checkout stripped of agent files, with shared operational help |
| B | A plus a trimmed maintainer AGENTS.md |
| C | A plus the generated layer, retrieval protocol and live checker |
| D | B plus the generated layer |

The primary contrast is C minus A in held-out rule-violation rate. D minus B, the more operationally relevant augmentation contrast, is secondary and is the first arm contrast lost when the budget ladder removes D. Existing developer documentation stays in every arm, so A is not literally code without knowledge. [Analysis plan](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/analysis_plan.md), [strip policy](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/strip_list.md)

A positive result would support a bounded statement: under this model, harness, task selection and scoring system, the generated guidance and enforcement package improved measured behaviour relative to the stripped baseline. It would not establish that certification is correct, that the package beats a maintained entry rung, or that the full loop reduces senior-engineer work over time.

## 3. Strengths worth preserving

The experiment selects tasks before drafting the corpus, records amendments, uses historical starting states, separates live checks from held-out scoring, gives the ticket rather than the replicate the role of statistical unit, pins model settings in the proposed execution protocol, and reports difficult issues such as stale knowledge and test naming dependence. These are substantial assets.

The later reviews also corrected important weaknesses: hidden agent files, ambiguous merge parents, operational help unequal between arms, overly favourable handling of unscoreable patches, and the distinction between evidence verification and genuine owner certification. These corrections should survive a redesign.

Keep the repository, extraction machinery, historical task inventory, screening infrastructure, graph comparison tools, cost logging approach and status-page generator. Treat the 25 familiar tasks as development material. Preserve their historical record instead of quietly replacing it. The restart should be a new protocol with a stated reason and new confirmatory holdout, rather than another claim that the old protocol remains unchanged.

## 4. Why the present POC is insufficient for the intended claim

### Authority is optional in the experiment but central in the playbook

The plan acknowledges that Yaroslav cannot certify architectural truth for a project he does not own. It substitutes an evidence audit and a cross-vendor model verifier, with maintainer participation opportunistic. That is honest labelling, but it removes the layer's defining decision step from the required evidence.

A citation can be accurate while the proposed policy is wrong. Repeated code may represent an accident, a deprecated practice, a compatibility exception or an intentional boundary. A second model reading the same evidence may reproduce the same mistaken explanation. Its calibration on swapped module names and reversed import directions tests obvious factual corruption, not the harder error of converting a genuine regularity into an unjustified obligation.

Require examples where an owner accepts a proposed decision, rejects another, records a scoped exception and changes a previous decision. Test that the system subsequently treats those four cases differently. Until an authorised owner participates, label this part a controlled policy simulation or evidence-verification study, not certification of NetBox's architecture.

### The baseline does not establish the value of moving beyond the entry rung

The playbook explicitly advises most organisations to start with lean guidance, ADRs and CI. The POC makes the comparison against stripped agent guidance primary. C versus A bundles generated knowledge, pre-flight procedure, retrieval and checker access. A win cannot identify which ingredient mattered, and could mostly reflect giving one arm more structured assistance.

That bundle comparison is legitimate as a package experiment, but insufficient as the main investment test. The headline should be the full layer versus a competent maintained entry rung. Ordinary developer docs and shared CI belong in that baseline. Retain simpler comparisons as diagnostic experiments.

Nor does equivalence to one maintainer file establish lower senior-maintainer cost. That needs measured construction and maintenance effort, coverage and quality. A hand-written guide may also be incomplete, outdated or aspirational; it is a valuable reference, not a complete truth oracle.

### The scoring standard is selected from the treatment's own knowledge

Candidate rules are every pattern or policy claim in the frozen generated corpus. They are admitted only if all 25 reference fixes conform and if they meet applicability criteria on another set of merged PRs. Whole rule families are then withheld from the live checker. [Tier procedure](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/tier_split_procedure.md)

This avoids drafting directly towards a known live-checker split, but does not create an independent architectural gold standard. Conventions the generator fails to discover never become candidates and cannot penalise its missing coverage. Selecting rules partly against the 25 reference solutions also makes the evaluation instrument depend on those solutions. A merged fix is evidence of accepted practice in context, not proof that every aspect of it expresses a universal rule.

Build a separate, owner-authored inventory of governing obligations and permitted exceptions. Keep it from the corpus builders. Use it to measure both what the pipeline gets right and what it misses. Rules derived from the corpus remain useful as a secondary question: can agents apply what they have been told? They should not alone define whether the pipeline discovered the right knowledge.

Withholding checker feedback is still useful, but distinguish that from withholding truth. The agent should receive the actual policy it must obey. Hidden evaluators can test new situations and the consequences of those policies without hiding the governing policy itself. Cross-family semantic overlap also needs checking; keyword family names do not guarantee independence.

### The primary denominator is affected by the treatment

Under the committed analysis, a ticket enters a contrast only if both arms produce at least one rule opportunity. The treatment can change patch size, location and whether work is completed, which changes both denominator and eligibility. This is selection after treatment, not a fixed comparison population.

For example, A produces three violations across ten opportunities. C produces no substantive patch and zero opportunities. The ticket disappears from the primary comparison, while the companion count favours C, zero versus three. A descriptive scope report reveals the failure but does not prevent a favourable primary verdict. The same problem can occur with incomplete patches that retain a few easy opportunities. [Endpoint definition](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/analysis_plan.md)

Make the task population fixed before execution. Define task-level obligations from the request and authoritative requirements, independently of the reference patch's exact layout. The primary usable-outcome measure should require both behavioural completion and satisfaction of applicable architectural obligations. Empty, incomplete and timed-out runs remain in the denominator. Report architectural quality separately, including extra violations introduced anywhere in the patch, so a joint metric does not hide the mechanism. Correct alternative designs must be allowed.

### The POC tests stale knowledge as its default operating state

The committed staleness data show a median age of 11.4 months, a maximum of 14.0 months, and six of 25 tickets touching at least one module absent at T0. These are useful stress-test conditions, but the playbook proposes an actively renewed system. The present treatment is a frozen corpus with deterministic notes and flags, rather than the proposed regeneration and recertification loop. [Staleness table](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/data/staleness.md)

Use a fresh, time-valid corpus at each evaluation snapshot as the main condition. Freeze the algorithm, prompts and permissions before evaluation, not one old output forever. For historical tasks, build each corpus only from that task's pre-fix snapshot and earlier decision material. A held-out drafting environment must not see solutions, task-specific selection notes or future history. An alternative is a recent common snapshot followed by prospective tasks.

Then test staleness deliberately: frozen output; drift detection only; full renewal and owner re-attestation. Structural evidence survival does not establish semantic freshness. The current comparison uses symbol names and dependency identities, so a function can retain its name while its behaviour changes completely.

### Bug-fix size is a weak substitute for architecture-relevant demand

The sample is selected through test-carrying bug fixes and a floor of four or five changed files including tests. That can enrich opportunities, but does not establish a need for architectural interpretation. A large bug fix may mostly require implementation skill. Conversely, a two-file change may require a crucial decision about an allowed boundary.

The feature stratum is exploratory and is the first scope dropped for cost, although placement, reuse and decisions about new interfaces are close to section 4's motivating use cases. Replace file count as the main proxy with a predeclared task taxonomy: reuse, boundary crossing, permissions across interfaces, model/API/UI consistency, exceptions, deprecated interfaces and new capability placement. Include tasks where the layer should add little, to measure unnecessary overhead.

Use separately labelled natural tasks and deliberately constructed challenge tasks. The latter can establish mechanisms under controlled conditions; they cannot estimate how often those situations occur in ordinary work.

## 5. Repository selection, reassessed

The stored shortlist compared NetBox, Paperless-ngx and Wagtail on seven criteria. The recorded scores sum to 32/35, 31/35 and 28/35 respectively. Those totals are arithmetic over the recorded judgements, not independently established measurements. Five earlier exclusions were Saleor, Redash, Directus, Zulip and Ghost. The underlying Gate 1 report is missing, so those exclusions cannot be fully audited. [Recorded comparison](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/statuspage/state.json)

**NetBox remains a good technical candidate.** It combines a shared core with domain apps, repeated model/form/filter/API patterns, permissions, signals, jobs, migrations and an inspectable test history. The historical CI specifies PostgreSQL, Redis and Python test execution. The database contains 965 modules, 3,155 import rows representing 3,130 distinct edges, and 391 string-reference rows, including 186 cross-app rows. My database query found 108,509 lines in non-test Python modules after excluding migrations and the extractor's flagged data modules. This is a credible size for the experiment, although it is the extractor's line-count convention, not cloc. [Historical CI](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/.github/workflows/ci.yml), [extractor](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/factgraph/build_factgraph.py)

However, NetBox is a modular Django application, not a representative multi-service organisational estate. It cannot alone establish cross-repository ownership, service contracts or business constraints invisible in code. It also has substantial developer documentation already at T0. The adding-models guide explicitly covers model bases, migrations, forms, filters, tables, REST and GraphQL components and tests. Rediscovering these may establish useful packaging and retrieval, but not recovery of undocumented organisational intent. [T0 developer guide](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/index.md), [adding models](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/adding-models.md)

| Candidate | Appropriate role | Assessment |
|---|---|---|
| NetBox | Main public technical study | Best-supported current option. Keep conditionally; repair extraction and task evaluation, and establish authority access separately |
| Paperless-ngx | Smaller feasibility comparison or replication | Its backend separates documents, mail and other concerns and has a dedicated backend CI workflow. Potentially cheaper scope; owner access and useful task yield remain untested |
| Wagtail | Alternative public replication | Rich extension points, permissions, content types and documented development practices. Its documentation is an advantage for truth checking, not an automatic reason to reject it |
| A real owner-backed private codebase | Main authority and lifecycle study | Preferred if available. It supplies decisions, exceptions and business intent that public code alone cannot establish. Reproducibility and confidentiality would need a shareable evidence strategy |
| A controlled fork or small designed estate | Mechanism challenge suite | Useful immediately for conflicting decisions, expiry and fencing. Authority applies only to the experiment's fork; it cannot be attributed to upstream maintainers |

The Paperless and Wagtail assessments are desk screening, not completed environment benchmarks. Their relevant source structures and test/development material were inspected; historical ticket yield, runtime and owner participation have not been established. [Paperless backend](https://github.com/paperless-ngx/paperless-ngx/tree/dev/src), [backend CI](https://github.com/paperless-ngx/paperless-ngx/blob/dev/.github/workflows/ci-backend.yml), [Wagtail structure](https://github.com/wagtail/wagtail/tree/main/wagtail), [Wagtail development](https://docs.wagtail.org/en/stable/contributing/developing.html)

Several original screening premises should change:

- **Thin documentation is not inherently desirable.** Documentation and recorded decisions supply independent truth and make a stronger comparison possible. What matters is the gap between accessible material and correctly applied authority.
- **Owner access should be a hard gate for the authority study.** It was absent from the seven criteria. No weighted total should compensate for its absence.
- **The Redash inactivity exclusion should not be carried forward as a current fact.** The repository has recent merged work, including a Databricks change on 2 September and a security-document update on 3 September 2026. This does not establish adequate task yield, but it contradicts an unqualified current description of inactivity. [Merged Databricks PR](https://github.com/getredash/redash/pull/7795), [security-document PR](https://github.com/getredash/redash/pull/7799)
- **Size needs one counting method and a scoped interpretation.** GitHub repository size is stored data, not source lines. A large repository may still have a bounded useful subsystem. Saleor's original exclusion was not independently reproduced here.
- **Well-documented projects should remain eligible.** Rejecting Zulip or Ghost solely because generated guidance might add little favours a favourable setting instead of testing when the additional machinery earns its cost.

For the revised Gate 1, require: an owner or a clearly limited claim; enough architecture-relevant tasks; valid behavioural tests; recoverable pre-task knowledge; independently checkable decisions; a reproducible environment; and an affordable end-to-end run. Score complexity, portability and coverage only after those requirements pass. Do not select a repository because the treatment happens to beat the baseline in a preliminary trial; use a separate development split and freeze the confirmatory selection.

My present selection is therefore **NetBox for the technical experiment, plus an owner-backed setting for authority and lifecycle**. Wagtail is a reasonable public alternative if NetBox fails the new gates. Paperless is a reasonable lower-scope alternative if environment and human-review effort dominate. There is no evidence yet that switching to either would improve causal validity by itself.

## 6. Concrete implementation and statistical findings

These findings come from source inspection, database queries and small local reproductions. They are not agent-performance results, and I did not run the full NetBox test suite or paid agent trials.

| Finding | Evidence and consequence | Required treatment |
|---|---|---|
| Imported submodules are omitted | The extractor records `ImportFrom.module` but ignores alias names. A scan found 193 syntactically identifiable submodule-reference candidates absent from the graph. A definite example is `account.urls` importing `account.views` through `from . import views`; the graph records the package rather than this module relationship | Resolve module aliases/re-exports appropriately; audit precision and recall by dependency form; rebuild affected stores |
| Ownership is not actually represented | The schema has churn and author counts but no current owner identity or owner-to-component relation | Add explicit owner provenance and unresolved-owner states. Commit authorship is not authority |
| String-reference coverage is narrower than the broad coupling claim | The implementation handles selected field declarations and `get_model` calls. It is not a complete model of signal registration, runtime calls or all dynamic Django dependencies | State supported edge kinds and use separate recall tests for omitted forms |
| Reproducibility is being confused with correctness | Matching extraction outputs does not detect shared modelling errors. The current status state still contains a byte-for-byte independent-rebuild claim despite the plan's correction | Distinguish same-code reproducibility, independent extraction agreement and semantic validity |
| The screen parser can accept a broken post-fix suite | In a local two-test example, one fail-to-pass test plus another test still failing after the fix produces `SCREEN_PASS` under the committed reduction | Require all required post-fix tests and environment health checks to pass, plus at least one symptom-relevant pre-fix failure |
| Test-ID selection can miss fixture effects | Whole-module fallback happens only if no changed test method is found; a patch changing a fixture and one method may affect other tests that are omitted | Include fixture/import/decorator dependants or use safe module-level coverage for those cases |
| The coupling count is a screening flag, not definitive ground truth | The 13/25 report uses added diff lines and name matches, rather than proving a symbol is newly introduced and that a legitimate alternative would fail | Confirm against before/after symbol inventories and task requirements; separate required public interfaces from reference-only helpers |
| T0 date conventions are mixed | Git reports author date 27 June 2025 and committer date 2 July 2025 for the same T0 commit. The staleness script subtracts 27 June from committer dates, so even the T0 checkout reports 0.2 months | Use one timestamp definition consistently. This does not invalidate the pinned commit, but changes reported age |
| Power calculation differs from the decision rule | The script approximates a bootstrap-CI success criterion with a sign-flip test, forces at least one opportunity per run, and takes explicit baseline inputs; merged human PR rates are not an agent baseline | Simulate the complete revised estimator and success rule using a separate agent pilot, including zeros, failures, clustering and missingness |
| Adaptive extension is not statistically resolved by preregistration alone | Extending when a first CI is inconclusive and reporting an ordinary final CI does not itself establish error control | Use fixed sample size, or calibrate a sequential design and its final intervals under the complete stopping rule |
| Extension reserve is too small | 300 to 500 runs is a 66.7% increase. If 300 runs cost 80% of the cap, 500 cost 133.3% at the same average cost | Price the maximum authorised design or remove the extension. A 20% reserve does not fund it |
| Design documents disagree | The plan's prose floor says k=3, but the ladder permits k=2. Selection still contains an obsolete stop-at-20 step beside the all-qualifier amendment | Resolve once in the new version, with a single authoritative decision specification |

Implementation references: [graph extractor](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/factgraph/build_factgraph.py), [slice API](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/factgraph/slice_api.py), [historical account import](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/account/urls.py), [screen verdicts](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/scripts/failpass_verdicts.py), [test-ID extraction](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/scripts/failpass_testids.py), [name-coupling script](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/scripts/name_coupling.py), [staleness implementation](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/factgraph/build_per_ticket.py), [power script](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/scripts/power_mde.py), [budget ladder](https://github.com/yspbob/interpretation-layer-poc/blob/d542b58/preregistration/degradation_ladder.md).

Additional execution safeguards belong in the new harness. Historical trees must be exported without accessible future git objects, remote lookups, solutions or grading files. Root-only stripping does not establish that nested or global agent guidance is absent. Runs need isolated databases and caches; `--keepdb` must not share state across arms. Per-ticket graph JSON contains reference-derived touched-module fields, which must stay in evaluator storage and never enter served change notes. This is a prospective leakage risk, not an observed leak: the serving implementation does not yet exist.

A live checker exposed as a tool is also not a guarantee. It can be skipped, its result can go uncorrected, and its coverage can be incomplete. Mandatory final gates must operate outside agent control, recording blocked submissions and overrides. The rule-split procedure needs a bounded failure disposition too: changing seeds cannot satisfy minimums if too few families or opportunities exist at all.

Treat contamination and future guidance as threats with uncertain direction. A modern guide can reveal a later design or recommend APIs unavailable at an older checkout. Memorisation can compress or otherwise change arm differences. Published training cutoffs and negative recall probes are useful diagnostics, not certificates that a task is uncontaminated.

## 7. A stronger validation programme

### Study A: can the pipeline recover useful knowledge without manufacturing authority?

Select a bounded set of active components with a competent owner. Before generation, the owner creates a hidden reference set of facts, patterns, decisions, known accidents, exceptions, conflicts and missing information. Keep construction examples separate from the test set. Obtain expectations from source history and owners, not solely from what the model generates.

Run extraction, drafting, verification and certification in recorded stages. Measure factual precision and recall; coverage of important known patterns; unsupported policy assertions; valid decisions recovered; correctly escalated uncertainty; retrieval of applicable decisions; false rejection by the verifier; and owner minutes per accepted artefact. Include ordinary cases and deliberately difficult counterexamples, reporting them separately.

The difficult cases should include correct citations attached to a false generalisation, a deprecated pattern still common in code, a legitimate scoped exception, conflicting sources, wrong ownership, business intent absent from the code, and evidence that remains structurally present after its meaning changes. Mutation calibration should cover these semantic errors, not only corrupted identifiers.

An unverified-output comparison can be performed offline to estimate what verification removes and what valid content it loses. There is no need to expose unverified policy as production authority. A verifier that rejects everything is not useful, so precision must be accompanied by recall, retained coverage and review cost.

### Study B: does the layer improve usable work over a competent entry rung?

Use fresh held-out tasks after the harness and scoring contract are frozen. Retain the current 25 as development tasks because their solutions and characteristics have informed multiple rounds of design.

The essential comparison is:

| Condition | Common foundations and added capability |
|---|---|
| Entry rung | Same capable agent, operational help, repository docs, lean owner guidance, ADRs and normal CI |
| Full layer | Entry rung plus generated and certified task-scoped knowledge, pre-flight checks, decision lookup, live feedback and recorded lifecycle behaviour |

This estimates the practical incremental package value. Optional component-removal experiments can then answer narrower questions. Give one condition the same verified corpus as static scoped files and another the same corpus through active retrieval, with the same checks, to test delivery. Hold corpus and retrieval fixed while removing live checker feedback to test enforcement assistance. Compare raw-source retrieval and verified-claim retrieval with the same interface to test the combined transformation and verification stage. Study A supplies the cleaner verification-specific evidence.

Do not multiply all these into a full factorial by default. Preserve the main comparison, adequate tasks and owner validation first. Run component tests on a separate predeclared diagnostic subset, and label their scope.

The main outcome is the proportion of attempted tasks producing an acceptable change: independently tested behavioural completion, no material new regressions, and satisfaction of applicable owner-defined architectural requirements. Every assigned task and run stays accounted for. Record justified abstention separately for ambiguity/authority challenges; it is not a successful bug fix, but may be the correct response in a deliberately unanswerable governance case.

Architectural obligations must allow semantically correct alternatives and cannot require the reference fix's file layout or private helper names. Validate hidden tests using the reference fix, seeded bad fixes and, where practical, alternative valid implementations. The existing fail-then-pass and symptom audit are useful starting points, but neither alone proves solution independence. SWE-bench's own validation approach explicitly considers whether requirements and tests make tasks solvable from the available information. [SWE-bench Verified](https://www.swebench.com/verified.html)

Report task completion, architecture violations by severity, regressions, review and repair minutes, wall time, inference cost, retrieval cost and the fraction of tasks with no useful layer contribution. Check that any conformance improvement does not come with an unacceptable decline in functional completion. Choose a practical improvement threshold and acceptable harm margins before the confirmatory sample; statistical significance alone is not the investment decision.

Use ticket-level paired estimates with blocked random arm order. Account for tasks sharing fixes, release branches or the same underlying rule; 25 tickets from one repository are not 25 independent repositories. Repeated runs estimate stochastic variation and do not substitute for diverse tasks. Start sample planning with a separate pilot across difficulty and task types, then simulate the actual estimator and decision rule. Prefer fixed sampling. If precision is inadequate at the affordable sample, publish a feasibility finding rather than forcing a success/failure claim.

### Study C: does authority survive change at a sustainable cost?

Use chronological real changes plus controlled interventions. At each point, compare a frozen layer with the renewed layer, using only information available at that time. Assess:

| Change | Expected behaviour to validate |
|---|---|
| Evidence changes | Affected claims are detected and re-derived or withdrawn |
| A name survives but semantics change | Semantic review or relevant tests detect the stale claim |
| Owner rejects a retro-ADR | It remains rejected; the accidental pattern is not promoted to policy |
| Policy changes without a code change | The owner-led change supersedes guidance and checks |
| Owner leaves | Ownership becomes unresolved and is escalated; no silent renewal by an absent authority |
| Knowledge expires | Agent serving and rule enforcement follow the declared, distinct expiry policies |
| Urgent exception is authorised | Only the scoped exception is allowed; its author, reason and expiry are recorded |
| Existing code violates a new policy | The conformance register records the inherited breach while merge checks handle new violations |
| Sources conflict or contain instructions masquerading as policy | Authority/provenance rules preserve the intended decision hierarchy |

Measure detection precision and recall, time to correction, stale guidance served, false blocks, unowned findings, valid exceptions mishandled, and owner workload. Capture at least a complete renewal/exception cycle before calling the loop demonstrated.

Price the total cost per acceptable outcome, including amortised build and knowledge maintenance, and measure net senior-review time. Keep a separate cost breakdown for the initial experiment, since prototype engineering effort is not automatically steady-state cost. The layer earns scale only if the observed benefits plausibly cover the continuing work it creates.

## 8. How to proceed without preserving sunk-cost constraints

1. **Archive the current protocol as an unexecuted scored experiment.** Preserve all existing artefacts and known weaknesses. Write a new claim-to-evidence contract separating technical, authority, lifecycle and economic claims.
2. **Reopen repository suitability.** Assess NetBox, Wagtail and Paperless against hard evidence requirements. Prefer whichever real setting supplies credible owner access; retain NetBox as the public technical candidate meanwhile.
3. **Repair the instruments before generation.** Fix dependency extraction and test screening; audit supported edge types and ownership; remove grading material from agent environments; establish an independent scoring inventory.
4. **Run a small feasibility study on development material.** Establish that the target failures involve missing or misapplied knowledge, that useful guidance reaches the agent, and that the environment and reviewer process are affordable. A task the model cannot implement even with authoritative help may be inappropriate for this mechanism test.
5. **Freeze a new confirmatory design.** Specify task and decision holdouts, models, prompts, authority inputs, environment snapshots, rubrics, tests, sample size, cost bounds, practical success and harm thresholds, and failure handling.
6. **Run the three studies and report each verdict.** Include negative results and costs. Replicate across another repository and model-harness pair before generalising beyond the first setting. Use a real team pilot to assess delivery and organisational value later.

No specific budget, maintainer commitment or private repository has been assumed. The handover's USD 600 was proposed, not an authorisation for spending. Owner availability remains the main unresolved input for the authority study; it need not block the public technical analysis or controlled challenge design.

## 9. What evidence would justify which claim?

| Evidence obtained | Defensible claim |
|---|---|
| Reproducible graph and successful retrieval | The technical components operate on the tested scope |
| Independent knowledge truth set plus owner certification cases | The pipeline can produce useful proposals and preserve authority in this setting |
| Better usable outcomes than the entry rung | The full package provides incremental task-level value for these tasks and this agent |
| Successful renewal, rejection, expiry and exception cases | The lifecycle loop was demonstrated under the tested changes |
| Lower total review/maintenance burden at held quality | The tested scope has evidence for an economic advantage |
| Prospective team deployment with sustained outcomes | Production evidence for that deployment, with broader transfer still open |

The current plan's proposed upgrade to section 4 should depend on which rows have actually been achieved. A technical package result alone warrants wording about evidence-verified guidance and conformance. An end-to-end interpretation-layer claim requires the owner and lifecycle rows too.

Relevant research reinforces the need for this distinction. Gloaguen and colleagues' June revision finds that repository context files do not generally improve task success and increase average inference cost, despite instructions being followed. Lulla and colleagues report lower runtime and token usage in a different setup. Khatri's smaller multi-repository ablation finds little correctness movement and highlights implementation rather than missing-knowledge failures. These studies evaluate different interventions and outcomes; none tests this complete authority loop. Their collective implication is to measure knowledge need, usable completion and cost locally, rather than assume more guidance helps. [Gloaguen et al., v2](https://arxiv.org/html/2602.11988v2), [Lulla et al., v2](https://arxiv.org/abs/2601.20404v2), [Khatri, v1](https://arxiv.org/abs/2607.27250v1)

**Decision proposed:** restart the protocol, keep the reusable infrastructure, retain NetBox conditionally for the public technical study, and make genuine decision authority plus lifecycle evidence mandatory for validating the interpretation layer as described in the playbook.
