# Review of the approach and its explanation

11 September 2026

**Status:** Review recommendations, not agreed method changes or experimental findings. The user requested an assessment of gaps and asked that the text be easily digestible. Website changes below are banked for application. No model runs were performed.

Reviewed the current working plan, especially sections 1A, 5, 6, 8, 9A and 10, against the continuous explanation and phase panels in the website source. This is a review of the specification and writing, not a new browser inspection or validation of the proposed controls.

## Overall judgement

Keep the three phases. They ask useful, different questions: can the layer reconstruct supported guidance; does the guidance help an agent change code; and does interaction add further value? Each phase can finish with an unfavourable result. No additional phase or comparison group is needed to address the issues below.

The strongest existing safeguards should remain. The plan preserves failed attempts, distinguishes documented rules from inferred claims, charges preparation costs, matches ordinary reviews, separates assessment from treatment and acknowledges possible familiarity with public code. It also requires the three groups to run together in Phase 3. Those are already planned controls, not missing features discovered by this review. They have not yet been validated.

## 1. Clarify which guidance continues into Phase 2

The Phase 2 panel in `website/app/coding-plans.tsx` says to use guidance that has passed the first phase's evidence checks. This can be read as selecting only successful guides. Section 5 of the working plan instead requires the comparison to retain missing or incorrect guidance and to use the frozen admitted subset, even when it is empty.

These can coexist only if the distinction is explicit. The verifier decides which claims enter the guide. Independent assessment then measures how well that process worked. Selecting only the guides that score well in independent assessment would hide preparation failures from the later comparison.

**Recommendation:** Distinguish the decision to continue the study from selection within a fixed comparison. The study may stop or repair its method after Phase 1. Once a comparison and its preparation procedure are fixed, keep every preparation outcome that belongs to that comparison. Pass on the verifier's frozen result, including an empty guide, and retain its cost and failure record. This does not mean forwarding raw claims the verifier rejected. A separate test using only successful guides can be informative, but its conclusion must explicitly apply only to that selected set.

This is the highest priority clarification because it changes what a positive result would mean.

## 2. Set the order for choosing tasks and preparing guidance

The plan already requires task neutral inputs and a declared reuse set before preparation. The phase narrative nevertheless leaves room to read task selection as something done after seeing the guide. That could favour tasks for which the generated guidance happens to be useful.

**Recommendation:** Before drafting guidance intended for later comparison, reserve the intended coding tasks or fix an explicit selection procedure that does not depend on the guide's results. Establish compatible code versions and source access. The investigator may make these arrangements without showing the tasks or answers to the drafter and verifier. Full coding infrastructure need not be built at this point.

Record the guide version, its source files, permitted revisions, preparation cost and intended uses. If hidden assessment feedback changes the guide or its preparation, retain that history and treat affected work as development. These safeguards largely exist in sections 1A and 5; the missing piece is one clear operational sequence across the phase boundary.

## 3. Complete one concrete Phase 1 assessment specification

The plan requires assessment of support, exceptions, uncertainty, omissions and verifier mistakes. It correctly rejects an invented measure of recall across an entire repository. The selected cases, numerical limits and qualification material remain open.

**Recommendation:** Before building a general assessment framework, work through one bounded case. State which sources and decisions are being assessed, which answers those sources support, which alternatives are valid, what counts as a serious error and how missing guidance is recorded. Explain how duplicate or differently worded claims are treated. Then use separate cases to qualify the actual assessor.

The resulting measure can describe coverage of the audited decisions. It cannot establish that the guide has recovered every important rule in the project. This is necessary specification work already anticipated by the plan, not a proposal to add a larger benchmark.

## 4. Make current requirements distinguishable from later requirements

Section 1A clearly limits Phase 1 to drafting, verification and independent guidance assessment. Some inherited detailed sections still describe coding cases and all three methods in general terms. For example, the budget calibration section still says to try all three methods, despite its phase allocation note.

**Recommendation:** Label requirements where they appear according to the activity that needs them. Phase 1 needs reliable guidance assessment and tested access restrictions. It does not need the code judge or interactive checker. If a Phase 1 tool can execute code, that exposed capability still needs the relevant execution controls. Resolve stale wording rather than adding another overview for the reader to reconcile.

The eventual conclusions also need to stay bounded. Phase 2 tests the combined preparation and guidance method against direct source use. It does not separately identify the contribution of every component or prove that this architecture is necessary. The current plan already limits that claim appropriately.

## 5. Make the explanation easier to read

The continuous overview is an improvement. Keep “How the three phases fit together” visible. Its job is to explain why the phases exist and how their results connect. The selected phase should then explain what happens next, without repeating the full overview. The optional full method currently repeats substantial material and should be checked for duplication when these edits are applied.

Use a named actor, an action and its purpose. Introduce a term before relying on it. Give important qualifications their own sentence instead of appending several to one sentence. Do not shorten the text merely to reduce its word count. Avoid hyphens in new explanatory prose, apart from technical identifiers and links.

Examples of proposed rewrites:

**Current:** “The drafter, verifier and independent assessor need separate contexts and explicit access boundaries.”

**Proposed:** “Each agent starts in a separate conversation and receives only the files assigned to it. The system must prevent the drafter and verifier from opening the assessment answers. We also record exactly what each agent received.”

Separate conversations alone do not establish isolation. The technical detail must continue to explain how access is prevented and tested.

**Current:** “Qualify the code assessor on separate cases before relying on its scores.”

**Proposed:** “Before the assessor scores the experiment, test it on other cases with well supported expected answers. Check whether it can recognise both a valid solution and a plausible mistake.”

**Current:** “Declare which compatible tasks share a guide before preparation, and retain that allocation for failed tasks too.”

**Proposed:** “Before preparing a guide, record which tasks will use it and check that it applies to their code versions. Share the preparation cost across those tasks. If a task fails, keep its share of the cost in the results.”

Apply this reading check to both the explanation and progress views. Progress should state what exists, what remains untested and the next action in ordinary language. Technical specifications can retain precise terminology where it is defined.

## 6. Explain familiarity acquired during the POC

The user asked whether our own source inspection makes the model familiar with the project and whether experimental tasks should run in incognito mode.

Reading the permitted code during an attempt is intended. Carrying earlier research, answers or feedback into an independent attempt is a different matter. Prior familiarity from model training is different again. A fresh conversation can address inherited conversation history; it cannot erase training knowledge.

The current plan already requires separate role and attempt contexts, controlled histories, no shared memory or retrieval stores, and separate familiarity probes. Explain this in ordinary language. Each independent attempt starts with only its assigned inputs. Within that attempt, the agent can retain its permitted working history. Guidance deliberately passed to a coding agent is an experimental input; the drafter's whole conversation and hidden assessment feedback are not.

For example, an investigator can inspect a historical fix while preparing the study. The coding agent must still start separately with the task and permitted starting files. It must not inherit the investigator's conversation or gain access to the saved answer. We cannot use this research conversation as the blinded participant.

**Recommendation:** Describe a fresh experimental session rather than rely on an incognito label. Check the actual request history, files, retrieval access and tool state. Record provider training and retention settings separately. A private browser window or a request to forget is not evidence that these boundaries hold. The runner still needs to implement and test the existing controls.

OpenAI's [conversation state documentation](https://developers.openai.com/api/docs/guides/conversation-state) explains that requests are independent unless conversation state is supplied or linked. Its [data controls documentation](https://developers.openai.com/api/docs/guides/your-data) states that API data is not used for training unless the customer opts in, while storage and retention are separate controls. Checked 11 September 2026. This does not establish the configuration of an eventual provider account or of this Codex session. Before choosing an experimental interface, verify its actual settings; do not infer them from a product label.

## Recommended next action

Resolve the guidance selection rule and the task selection sequence first. Apply the agreed interpretation consistently to the plan and website, together with the writing improvements. Then specify one Phase 1 case and its assessment before implementing the restricted role path. Keep the current limits on model calls and publication of assessment material. No new experimental benefit, qualification or owner approval is established by this review.
