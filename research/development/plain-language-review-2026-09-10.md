# Website wording review — 10 September 2026

Status: proposed rewrites, banked for the next authorised website update. The published pages and working plan have not been changed by this review.

The user identified that the sentence about repository snapshots was difficult to understand and asked for the same problem to be checked elsewhere. This review covers the source text for The Experiment, Progress & findings, their expandable explanations, technical overview and diagram, examples and shared case-detail interface. It is a wording review, not browser testing, a fresh review of every underlying inventory claim or a new validation of the experiment.

## Finding and approach

The difficulty is concentrated in the assessment procedure, technical readiness and risk/action text. Many sentences combine an unfamiliar label, several conditions and a limitation without first explaining the activity. The opening paragraph, three comparison cards and concrete NetBox example already explain their purpose more directly and should largely be retained.

Use full sentences that identify who does what and why. Explain an unfamiliar term when it first matters. Give the action before its qualification; split a paragraph when it mixes the process, exceptions and evidence status. Technical detail belongs in the relevant disclosure, but opening a disclosure should not require the reader to understand research terminology already. Preserve necessary qualifications rather than shortening by deleting them.

The wording below is proposed, not final implementation. Check it against the surrounding paragraph when applying it to avoid repetition. In particular, preserve the distinction between planned controls and implemented, tested behaviour. This review does not introduce new scoring rules or alter the pilot scope.

## The Experiment

### 1. Case-selection heading

Source: `website/app/experiment-details.tsx`, first method step.

Current: “Prepare a task with a defensible assessment”.

Proposed: **Choose a task and establish how to judge the result.**

Explain in the following paragraph that the criteria come from applicable project requirements and reproducible checks before an agent attempts the task. A heading alone should not carry that whole qualification.

### 2. Historical starting code

Source: the “How are tasks selected and assessment criteria established?” disclosure.

Current: “The repository snapshots in the candidate inventory are discovery material, not necessarily those historical starting points.”

Proposed: “We inspected one version of each repository to find potential test cases. For each historical task we select, the experiment will start from the code as it stood before that change was made. That may be a different version from the one we initially inspected.”

Retain the adjacent requirement that the task and rules must apply at that historical time; later documentation cannot create a new obligation retrospectively.

### 3. Choosing what the drafter may read

Source: second method step.

Current: “Its source scope is chosen without clues from the hidden solution.”

Proposed: “The files the layer may read are selected without using the hidden historical fix to guide that choice. Otherwise, the file selection itself could give away where the answer lies.”

Keep the existing statement that the drafter does not receive the later change task.

### 4. Withholding a written explanation of a rule

Source: “Does the layer read the documentation, or work the rule out from code?”

Current: “Other narrative disclosures are withheld consistently across the matched groups.”

Proposed: “Any other written material that gives away the rule is withheld from all three groups in this test. The same restrictions apply to each group.”

This belongs after the explanation that actual applicable AGENTS.md files remain intact and a rule stated in them makes that case documentation-visible. Do not turn the rewrite into permission to remove real project instructions.

### 5. What happens when preparation ends

Source: same disclosure.

Current: “Preparation has a fixed budget and revision limit; when it ends, both guidance groups receive the same admitted subset, even if it is empty.”

Proposed: “Preparation stops when its budget or allowed revisions are exhausted. Both groups that use guidance then receive the same set of claims accepted by the verifier. If no claims were accepted, both receive an empty guide.”

Retain the surrounding requirement that missing and incorrect guidance remain outcomes, and that another assessment checks the saved guide independently of the verifier. Here, acceptance means admission based on evidence, not project-owner approval.

### 6. Explaining judge qualification

Source: “How will the assessments be shown to be reliable?”

Current: “Each assessment job must be qualified for its own inputs and purpose; a verifier cannot grade its own success.”

Proposed: “Each reviewer or judge must be tested on the kind of decision it will make, using only the information it will receive during the experiment. A component that checks proposed guidance cannot also provide the independent verdict on how well it performed.”

Keep the separate roles, tests on different decision families and predeclared error limits in the subsequent explanation.

### 7. Repairing scoring after seeing trial results

Source: same disclosure.

Current: “A main-trial result used to repair the assessment becomes exploratory; confirmation requires fresh cases.”

Proposed: “If a main-trial result is used to change how the work is judged, it becomes part of developing the assessment. The revised method must then be tested on fresh cases before it can support a confirmatory conclusion.”

Retain the requirement to validate changed assessors again and rescore all affected implementations consistently. Do not imply that merely rerunning the same cases restores an independent confirmation.

### 8. Separating different kinds of task

Source: “What conclusions would the comparison support?”

Current: “The first pilot’s scored task comparisons use eligible historical backtests.”

Proposed: “For the first pilot, agents will repeat real changes previously made in the selected projects. A task can enter the comparison only after its requirements and assessment have passed the case checks.”

The rest of this paragraph also needs splitting: explain separately why authored development examples are reported separately, why a task that states the rule cannot test its discovery, and why related tasks do not count as wholly independent evidence.

## Progress & findings

### 9. Explaining the existing scripted checks

Source: technical-readiness entry “Independent evaluation”.

Current: “The 25 H04 comparisons reproduce authored expectations.”

Proposed: “In the H04 development example, 25 comparisons produced the outcomes specified in advance by the case author. This checks the scripted example; it does not establish that an AI judge is reliable.”

Retain the following open work on independent guidance and intervention assessments, model qualification and historical scoring.

### 10. Explaining role-specific file packs

Source: technical-readiness entry “Input packs and component contracts”.

Current: “H04 exports hashed role packs and has component contracts.”

Proposed: “The H04 example prepares a separate set of input files for each role and records a fingerprint of each file so changes can be detected. It also specifies what each component may receive and what it must return.”

Retain that historical case packs and the audit of applicable project instructions have not been prepared. File fingerprints do not prove isolation or correctness.

### 11. Counting related cases

Source: risk “Case counts overstate independent evidence”.

Current: “Group related challenges and repeats, qualify cases before counting them, and size confirmation from the planned effect and observed variability.”

Proposed: “Keep tasks that test the same underlying decision together in the analysis, including repeated attempts. Count a task toward the trial only after it passes the case checks. Use the pilot to estimate how much results vary, then choose a main-trial size that can detect the improvement worth pursuing.”

The existing numbers can remain as supporting evidence, after explaining why 52 candidate rows do not mean 52 independent decisions.

### 12. Risk titles and library labels

Source: risks and evidence record.

Suggested replacements:

- “Public-source knowledge and alternative disclosures” → “An agent may already know the code or find the rule elsewhere”.
- “Some key behavior sits outside the checkout” → “Some rules depend on libraries we have not yet checked”.
- “Technical success would not establish organisational authority” → “A successful technical test cannot show that an owner approves the guidance”.
- “Search by decision, repository or screening disposition” → “Search by topic or repository, or filter by why a case was kept or set aside”.

The shared “What remains” paragraph in case details needs the same treatment: explain that each candidate still needs a concrete task, checked dependencies, a justified assessment and a review of what the agent's files reveal. These are required preparation steps, not evidence that the candidate has already passed.

## Technical detail

### 13. Clarify short diagram labels without removing the product names

Source: `website/app/runtime-diagram.tsx` and `website/app/technical-setup.tsx`.

“Bounded JSON”, “permitted input pack”, “sealed assessment store” and “completed-block ledger” are compact engineering labels. Explain them at first use as results with a fixed size limit, the files a role is allowed to read, assessment records hidden from working agents, and a record of completed comparisons. The diagram can then use shorter labels while the adjacent prose explains their purpose.

Keep requested technology names, exact interface distinctions and security qualifications. A readable explanation should help the reader understand why the component exists, not replace technical accuracy with vague promises of safety.

### 14. Explain the safety checks on returned files

Source: “What makes a run inspectable and repeatable?”

Current: “Collection checks paths, symlinks, archive entries, output limits and message order before accepting untrusted artifacts.”

Proposed: “The runner treats returned files and messages as untrusted. Before accepting them, it checks where files would be written, whether links or archive contents could reach outside the allowed folder, whether results exceed size limits, and whether messages arrive in the expected order.”

This is still a planned requirement. Do not present it as an already tested protection.

## Apply in the next batch

Address these passages together with the already banked owner/verification distinction and the separate validation-during-work step. Preserve the agreed familiarity probes, break-even discussion and implementation takeaways as their own content changes, requiring the corresponding plan updates. Do not quietly incorporate them as if this wording review had already amended the experiment.

Review every revised paragraph in context for actor, action, reason and evidence status. Avoid repeating warnings merely because several passages touch the same limitation. Retain useful detail behind disclosures and preserve clear opening text. No browser checks or new experiment runs were performed for this review.
