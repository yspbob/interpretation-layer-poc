# Current project state

Updated: 8 September 2026. This record is maintained by Codex during normal work; the user does not need to prepare a handover.

## Purpose and current position

We are testing whether the interpretation layer proposed in [chapter 4 of the AI Engineering Playbook](https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html#4-the-interpretation-layer) produces useful, defensible guidance and improves subsequent engineering work. A positive result would support the mechanism in the tested situations, not prove that every organisation needs it.

The redesigned POC is still being prepared. There are **zero blinded model runs**. The verifier, interactive checker and final judge have not been built or qualified under the current protocol.

## Read next

- [Current working plan](preregistration/plan/working_plan_2026-09-05.md), especially sections 9A and 10: component qualification and the immediate development step.
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

The website has separate explanation and progress routes. Its method is presented as four visible steps with optional detail. Progress identifies one complete development example as the next substantive task. GitHub Pages serves `docs/` from main; editable source is in `website/`.

## Next substantive task

Write the verifier, checker and judge contracts, then construct one complete development case with pinned evidence, a concrete task, a valid change, a consequential mistake and a legitimate exception or alternative. Define expected decisions from independent evidence before comparing actual outputs. Trace guidance preparation, use, a changed approach and final assessment. Label all of this as development, not qualification or benefit evidence.

The user has so far requested that this step be recorded. Do not interpret this setup work as permission to launch paid or blinded runs. Case selection, model settings, budgets, repetitions, qualification thresholds, confirmation endpoint and sample size remain open.

## Current operational work

The user works on a Windows home PC and Windows laptop with Codex, and wants to switch without an explicit handover. The repository now holds the current plan, editable website and this project record. `AGENTS.md` requires Codex to retrieve the latest state before editing and save reviewed changes and decisions to GitHub before ending meaningful work. The sync helper rejects dirty starts and divergent history; it does not overwrite work or claim to synchronize chat transcripts.

A local Codex project needs to point at this repository on each machine. Project registration and GitHub authentication are one-time machine setup. This setup has not yet been exercised on the physical second machine. Opening a project alone does not establish that this existing conversation is visible there.

The sync routine passed a local two-clone test covering transfer, dirty-work refusal, unpublished commits, divergent history and a server-rejected push. A fresh dependency installation and GitHub Pages build succeeded in the consolidated checkout, with both routes and referenced local assets checked. Plan/download consistency and application type/lint checks passed. These are operational checks, not POC experiment results. Publication is confirmed by Git's remote commit and the live website, rather than a self-reported flag in this file.

To keep overhead low, related edits and decisions are saved in one commit per completed piece of work. Quick questions with no change to the agreed plan require no push. The website build is required only when its source or downloads change.

## Reading and presentation preferences

The audience is playbook readers seeking evidence for an unproven mechanism. Use plain, human prose, explain terms, and let readers choose when to open detail. Keep examples explicitly illustrative and introduce repositories before using them. Retain the playbook's navy, gold, warm background and Source Serif / Source Sans typography. The user steers in conversation; the website presents the design, status, risks and findings rather than providing process editing tools.
