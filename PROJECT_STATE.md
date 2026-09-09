# Current project state

Updated: 9 September 2026. This record is maintained by Codex during normal work; the user does not need to prepare a handover.

## Purpose and current position

We are testing whether the interpretation layer proposed in [chapter 4 of the AI Engineering Playbook](https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html#4-the-interpretation-layer) produces useful, defensible guidance and improves subsequent engineering work. A positive result would support the mechanism in the tested situations, not prove that every organisation needs it.

The redesigned POC is still being prepared. There are **zero blinded model runs**. Component contracts and a scripted development trace now exist; no model verifier, interactive checker or final judge has been exercised or qualified under the current protocol.

## Read next

- [Current working plan](preregistration/plan/working_plan_2026-09-05.md), especially sections 9A and 10: component qualification and the immediate development step.
- [Component contracts v0.1](research/development/component-contracts-v0.1.md) and [H04 worked development case](research/development/h04-response-lifetime/README.md), including its recorded results and reproducible runner.
- [Decision and plan change register](preregistration/plan/plan_changes_2026-09-05.md).
- [Study explanation](https://yspbob.github.io/interpretation-layer-poc/) and [Progress & findings](https://yspbob.github.io/interpretation-layer-poc/progress/).
- [Full playbook context and original POC review](research/development/playbook-and-original-poc-review.md). This is historical analysis: later decisions in the working plan supersede its recommendations, especially the owner-recruitment proposal.

The old NetBox-only preregistration and harness remain for traceability. Do not inherit their four conditions, 25-ticket selection, 300-run schedule or numerical success rules into the redesigned pilot.

## Decisions to preserve

- No accessible project owner is available. The technical experiment uses published references and reproducible behaviour; it cannot certify that newly inferred rules express an owner's unrecorded intentions.
- Separate deriving guidance from code from reading guidance in documentation. Record the provenance and qualifications of individual claims.
- Compare DIRECT (sources and ordinary review), GUIDE (the same plus frozen guidance) and INTERACT (the same guidance plus structured consultation and checking). Match checkpoints, correction opportunities and resource limits; include preparation and review costs.
- Check the initial plan and material changes of approach during execution. The working proposal allows two correction rounds per checkpoint. Unresolved or exhausted attempts remain in the results.
- Separate runtime review from final evaluation. Qualify verifier, checker and judge independently against defensible references and legitimate exceptions, with separate development and validation families. Exact numerical gates are still open.
- Isolation must record the actual files, tool access and network boundaries. It does not erase prior model knowledge of public sources. Unpublished semantic variants and other controls are required.
- The public candidate inventory is investigator-visible preparation material. It is not a sealed holdout. Never run a purported blind drafter in the conversation that has already seen its answers.
- Keep substantive website changes synchronized with the plan. Clearly distinguish a proposal, an agreed next step, implementation, validation and a frozen protocol.

## What exists

An inventory contains 84 records across four pinned repositories: NetBox, Wagtail, Paperless-ngx and HTTPX. Of these, 52 advance to case development across 39 families; 15 are controls, six deferred, four calibration, three merged and four rejected. The original twelve NetBox audit cases are development material. These counts do not establish statistical sufficiency.

Fifteen recorded development probes passed (nine HTTPX, six Paperless). These were selected behaviour checks, not full applications, container isolation checks or model comparisons. See `research/development/recorded-probe-results.json`. The portable probe script and source pins are retained alongside the current website source.

The website has separate explanation and progress routes. Its method is presented as four visible steps with optional detail. Progress records the first executable, scripted development example and identifies isolated role dispatch as the next substantive task. GitHub Pages serves `docs/` from main; editable source is in `website/`.

## Latest explanation update

On 9 September, the user identified that the explanation conflated drafting/approval with usage. The website now presents two connected cycles, with versioned approved guidance passed from preparation to repeated task use, and new evidence returned for review. It distinguishes an initial baseline from subsequent maintenance and makes clear that the POC tests evidence-supported, frozen guidance without owner certification. Maintenance remains outside the pilot; no research scope or results changed. The canonical plan and change register record this clarification. Application type/lint checks, static build and link/asset checks passed; the two-panel desktop layout was inspected in the browser. The explanation and progress views still describe the same pilot scope.

## Next substantive task

Implement a model-free isolated role runner: validate structured input/output records, dispatch immutable allowlisted packs into fresh restricted processes/containers, prove filesystem/network denials, and enforce initial, changed-plan and final checkpoints with terminal stops. Use H04 as the regression case. Then prepare distinct qualification families and fix coverage, error limits, models and budgets before authorised qualification calls.

Completed in this piece of work: contracts v0.1 and H04 at the pinned HTTPX source, with a concrete preview task, two valid solutions, two cleanup mistakes, unfinished work, prewritten reference verdicts, scripted guidance/checker trace and anonymised final-judge inputs. All 25 behaviour comparisons matched expectations; six control checks and 71 broker denials passed. The public result records exact source/artifact/input hashes, Python/dependency versions and observations before harness cleanup. The whole family is development material, with no independent human review. The broker is not OS isolation; semantic change detection is narrow, and no model judgement was tested.

The user requested continuation, then asked to stop after this development milestone and continue tomorrow. Work is paused at this milestone pending the user's next continuation request; no scheduled or background work is requested. Do not interpret this setup work as permission to launch paid or blinded runs. Case selection, model settings, budgets, repetitions, qualification thresholds, confirmation endpoint and sample size remain open.

## Current operational work

The user works on a Windows home PC and Windows laptop with Codex, and wants to switch without an explicit handover. The repository now holds the current plan, editable website and this project record. `AGENTS.md` requires Codex to retrieve the latest state before editing and save reviewed changes and decisions to GitHub before ending meaningful work. The sync helper rejects dirty starts and divergent history; it does not overwrite work or claim to synchronize chat transcripts.

A local Codex project needs to point at this repository on each machine. Project registration and GitHub authentication are one-time machine setup. This setup has not yet been exercised on the physical second machine. Opening a project alone does not establish that this existing conversation is visible there.

This milestone's H04 checks, application type/lint checks and GitHub Pages build passed. The plan downloads and both explanation/progress views have been reconciled. The fixture's text files use LF endings so their recorded hashes survive transfer between Windows checkouts.

The sync routine passed a local two-clone test covering transfer, dirty-work refusal, unpublished commits, divergent history and a server-rejected push. A fresh dependency installation and GitHub Pages build succeeded in the consolidated checkout, with both routes and referenced local assets checked. Plan/download consistency and application type/lint checks passed. These are operational checks, not POC experiment results. Publication is confirmed by Git's remote commit and the live website, rather than a self-reported flag in this file.

To keep overhead low, related edits and decisions are saved in one commit per completed piece of work. Quick questions with no change to the agreed plan require no push. The website build is required only when its source or downloads change.

## Reading and presentation preferences

The audience is playbook readers seeking evidence for an unproven mechanism. Use plain, human prose, explain terms, and let readers choose when to open detail. Keep examples explicitly illustrative and introduce repositories before using them. Retain the playbook's navy, gold, warm background and Source Serif / Source Sans typography. The user steers in conversation; the website presents the design, status, risks and findings rather than providing process editing tools.
