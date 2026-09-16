# Research brief: find a useful case for testing repository guidance

## Your assignment

Research and recommend a concrete software-change task on which we can fairly compare a capable coding agent working directly from a repository with the same agent given an additional repository guide. Produce up to three ranked candidates and recommend one. This document contains the context and requirements; no access to our private study repository or earlier conversations is needed.

This assignment is task research, not guide writing or implementation. Use public primary sources and inspect actual code. Do not launch coding-agent trials, generate a candidate patch, purchase services or use paid APIs. The user will arrange any later experimental runs separately within their existing credits. Do not delegate to other model sessions without a separate request.

## What we are trying to learn

Our proposed interpretation layer reconstructs evidence-backed guidance about a software system: constraints, relationships between components, reasons for established patterns, and exceptions. A later coding agent receives that guidance alongside an ordinary change request and the same repository sources available to an unguided agent.

The question is whether that guide improves engineering work enough to justify producing and checking it. We need a task where connecting repository-specific facts could matter. We are not trying to prove that a weaker agent can be made to fail or that adding an answer to a prompt improves its answer.

Example of the mechanism: a change appears to be contained by a database transaction, but a separate request-context queue also stores notifications. Correctness depends on understanding both lifecycles. Guidance could connect those facts before a coder chooses an implementation. The task must still state the required user-visible behaviour to both coding conditions.

## What has already happened

- One small newly specified HTTPX task was implemented in two fresh contexts, with and without a previously saved task-blind guide. Both passed 9/9 common acceptance checks and 104 relevant original regression cases. No correctness advantage was observed.
- Two further newly specified HTTPX tasks were screened without guidance: an ordered multipart-fields wrapper and a per-request redirect-limit extension. They passed 11/11 and 12/12 common checks, respectively, plus 199 relevant original regression cases each. Neither qualified for a follow-up comparison under the fixed selection rule. That two-task allocation is closed.
- These were Astra High coding attempts with explicit requirements and ten-minute supervised limits. The guide limit was five minutes and 600 words. These are historical settings, not a required budget for a different repository. Do not make a task difficult merely by giving it an unrealistic time limit.
- The checks were finite and focused; passing them does not establish complete correctness. The results also do not prove that guidance has no value. They show that increasing the scope of these explicit library changes did not provide the needed comparison case.
- A separate NetBox worked example exposed a real relationship between transaction rollback and queued notifications. Its guide was written with knowledge of the defect. That demonstrates an actionable explanation, not independent discovery or comparative benefit. It is already exposed development material.

We need a better reason for selecting the next task than “it has more requirements.” We cannot promise an unguided failure in advance. Do not select for an arbitrary score such as 5/10, and do not recommend repeated trials until one fails.

## Candidate requirements

1. **A meaningful change.** Give a concrete user or maintainer need, preferably supported by a public issue, design discussion or other project record. A newly authored request is acceptable if clearly labelled as our proposed requirement rather than maintainer-approved intent. We prefer a new study request over replaying a known solution.
2. **A repository-specific reason for guidance to help.** Identify at least one important obligation that requires connecting multiple source locations or established behaviours. Explain the relationship and why a generic programming rule or the feature prompt alone does not supply its implementation implications. Possible areas include transaction and event lifecycles, caches and authoritative state, authorization across entry points, cancellation and resource ownership, or compatibility across multiple interfaces. These are leads, not required categories.
3. **Fair, complete requirements.** Both coders must receive the same full product contract, including important error behaviour. Do not hide an obligation from the unguided coder or put a task-specific answer only in the guide. Any scored expectation needs explicit task support or an identifiable existing compatibility contract available to both agents. Exclude unresolved central requirements.
4. **A bounded task.** Aim for one understandable feature or change with a runnable local evaluation. Cross-component reasoning can matter even when the resulting patch is small. Avoid projects requiring production credentials, customer data, external paid services or a large new harness. We work on Windows; an existing Linux/container route may be proposed, but dependencies and setup cost must be explicit and unverified setup must remain labelled.
5. **Observable correctness.** Specify behavioural checks that distinguish a meaningful failure from a working implementation. Include a normal successful path, a relevant failure/boundary path and preservation of existing behaviour. Tests must accept different valid implementations. Setup failure, timeout, missing prose and cosmetic differences alone are not useful evidence of a guidance opportunity.
6. **A guide that can be prepared independently of the task.** Identify source material from which a neutral repository guide could explain the relevant relationships without receiving the selected request, expected patch, screening failure or evaluation fixtures. If the alleged advantage requires telling the guide author the answer, reject the candidate.
7. **Honest exposure reporting.** Public code may be familiar to modern models. Do not claim unseen code or zero training familiarity. Distinguish a new request from a new repository or decision family. Disclose whether you read a historical implementation or fix and separate it from the candidate task materials. A historical implementation can inform research but is not the answer key for scoring.

## Optional lead: a NetBox preview operation

One current idea is a new bulk-update preview: validate proposed edits using applicable ordinary update and permission checks, report item errors, and leave no persisted edits, change records or notifications from the preview. Normal updates must retain their behaviour. This is only a candidate idea. Feature absence, exact API semantics and feasible evaluation have not been established. Challenge or reject it if an existing feature already covers it, the mechanism is too obvious to add value, or setup is disproportionate. Do not give it preference simply because we suggested it.

Our existing evidence concerns an older bulk-error-reporting feature, not a preview implementation. At the historical feature revision, mixed valid/invalid updates rolled back database edits but still queued a notification. Successful updates retained their normal notifications. The observation concerns queued jobs, not delivery by a worker.

Primary source starting points, pinned to the historical feature revision:

- [Bulk update and validation-error handling](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/api/viewsets/mixins.py)
- [Save signals and event handling](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/core/signals.py)
- [Request-context completion](https://github.com/netbox-community/netbox/blob/6068f417876e79b6d588bd8b05a7a4e515378b51/netbox/netbox/context_managers.py)
- [Earlier REST API contract](https://github.com/netbox-community/netbox/blob/d13c98b9ea8c55dafdcdecbf3058a731814a7ead/docs/integrations/rest-api.md)

These are exposed leads, not certification of a new task. A distinct project or decision family is welcome if better supported. Do not rerun or repackage the known NetBox defect as a fresh discovery.

## Research process and stopping point

Inspect sources before ranking candidates. Prefer official repositories, tests, project documentation, issues and maintainer discussions; use commit-pinned links for code claims. Search summaries and intuition about what an agent “should miss” are insufficient.

Keep a short list of alternatives examined and concrete reasons for rejecting them. This is not an exhaustive benchmark survey. Return at most three well-supported candidates; fewer is better than padding the list. If none qualifies, report that result and the specific missing evidence rather than inventing confidence. Do not spend effort on new assessor qualification, elaborate scoring infrastructure or model runs.

## Deliverables

Return two Markdown documents, separating researcher analysis from a possible coder-facing request:

### 1. CASE-RESEARCH.md

Start with the recommended case and the strongest reason to choose it. Include a comparison table for up to three candidates with repository, pinned baseline, requested change, relevant source relationship, practical evaluation route, setup burden and main uncertainty.

For each serious candidate provide:

- Exact repository URL, baseline commit and relevant file/function links. Explain why that baseline is appropriate and whether the requested feature is absent there; state the scope of the check.
- Evidence for the user need and each important existing obligation. Separate documented contracts, observed code behaviour, your inference and investigator-authored requirements. List contradictions or uncertainties.
- The plausible ordinary implementation mistake and its observable consequence. Label it a hypothesis unless there is actual evidence; a historical developer bug is not proof a current agent will fail.
- What a task-blind repository guide could explain, and which sources support it. Do not write the guide or the patch.
- A small evaluation matrix: scenario, required outcome, supporting requirement/source and how to observe it. Include successful behaviour and safeguards against a fix that merely disables functionality.
- Environment and dependency requirements, likely setup effort and existing relevant tests. Distinguish inspected commands from commands actually executed. Do not claim a working runtime without checking it.
- Familiarity/exposure risks, limitations and reasons to reject the candidate despite apparent difficulty.

End with one recommended next preparation action and a clear verdict: ready for bounded preparation, needs specific evidence first, or unsuitable. Do not invent a probability of agent failure or a guaranteed guidance benefit.

### 2. CANDIDATE-TASK.md

For the recommended case, draft a standalone coder-facing request containing the pinned repository baseline, goal, complete behavioural requirements, scope and non-goals. Include source-derived compatibility obligations in ordinary user-facing language. Mark unresolved requirements explicitly; a request with central unresolved requirements is not ready for use.

Exclude your predicted failure, solution sketch, guide text, historical fix, study outcomes, researcher rankings and evaluator fixtures. This separation supports later review; the document is not yet an approved experimental packet.

## How any later comparison would work

We would first freeze the request, common checks, source access and bounded execution limits. If a separately approved screen produces an eligible behavioural failure, a subsequent comparison must use fresh unguided and guided attempts: the screening failure is not the comparison baseline. Guidance would be frozen before comparison and not tailored to the observed failure. Both comparison attempts would receive identical requirements, source access, model settings and limits except for the guide.

All screened passes, failures, incomplete attempts and preparation costs must be retained. If another fixed cap produces no eligible failure, that remains a result. Your research should improve the rationale for choosing a case, not guarantee a favourable experiment.
