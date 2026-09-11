# Working on the interpretation-layer POC

This repository is the shared project for two Windows machines using Codex. The user does not want to request or write a handover. Maintain continuity as part of ordinary work.

## At the start of a piece of work

Read `PROJECT_STATE.md`. Before editing, run `node scripts/project-sync.mjs start` from this repository. It fetches GitHub and fast-forwards a clean main branch. Read the state and these instructions again if the pull changed them. Then read the current plan linked in the state, and the files relevant to the request. Do not assume this chat contains the latest decisions. Batch related edits and decisions into one save per completed piece of work. Do not fetch, commit or push for every quick question or clarification; save a discussion when it changes an agreed decision or the next step. Never make empty commits just to mark activity.

If the checkout has unfinished changes, inspect and preserve them. Do not reset, auto-stash, force-push or overwrite them. If the machines have diverged, reconcile the actual changes explicitly. A failed fetch means that freshness is unknown; explain this before work that could conflict. The simple automatic routine expects main in the saved project folder; an existing worktree or feature branch needs deliberate integration, not an automatic branch switch.

## Before completing meaningful work

1. Update `PROJECT_STATE.md` with decisions, completed work, verification, unresolved issues and the exact next step. Record meaningful discussion-only decisions too. Maintain `research/implementation-takeaways.md` when a discussion or observation has implications for practical implementation; preserve its source, evidence status, uncertainty and next action. Do not transcribe the whole conversation or invent agreement.
2. If the method changed, update the canonical working plan and its change register. Run `node scripts/sync-plan.mjs` to refresh the website downloads, and review both explanation and progress views for semantic consistency.
3. If website source or published downloads changed, follow `website/README.md` to build and update Pages. Run the checks relevant to the work; keep unimplemented controls and unvalidated research clearly labelled.
4. Review the diff and explicitly stage only this task's public project files. Commit them with a descriptive message. The user's request for seamless two-machine work authorizes saving these reviewed changes to this POC repository without a separate handover request. It does not authorize paid model runs, unrelated publication or disclosure of sealed evaluation material.
5. Run `node scripts/project-sync.mjs publish` and confirm it succeeds. Only then say the work is saved to GitHub. If a push fails, retain the local commit and state exactly that it is not yet available on the other machine. Do not conceal a sync failure behind a successful local test.

This is a routine performed by the agent, not an installed background service. It cannot save after the app is killed, guarantee progress while offline, or synchronize a live chat transcript. No user-operated finish command is required. Do not create timer-based commits or a scheduled automation without a separate request.

## Research and publication boundaries

- Current authority: `preregistration/plan/working_plan_2026-09-05.md`. Older ratified plans and existing NetBox harness files are historical, not the redesigned pilot specification.
- The first trial has three functional phases under plan section 1A: reconstruct guidance, test its use, then test interaction. The restricted Phase 1 path now has a tested scripted rehearsal. The immediate step is implementing and testing its provider adapter without model calls, as recorded in PROJECT_STATE.md. Separate qualification cases and model settings remain open. Coding execution and the interactive checker are later phase gates, unless an exposed Phase 1 tool actually requires execution containment. Component contracts and the H04 scripted case are development material, not model qualification. Zero blinded runs have been completed. Neither judge qualification nor experimental benefit has been demonstrated.
- The first pilot uses evidence-backed historical public-project tasks and reports possible prior model familiarity; it does not prove inference entirely from unseen code. Private rule-changing variants are optional later work requiring independent justification, not a pilot prerequisite. Exclude unresolved central requirements from scored cases; keep historical code as a comparator, never an answer key.
- Preserve claim-level provenance, reference uncertainty, matched reviews and budgets, changed-plan checks and independent scoring. Owner approval cannot be inferred from public documentation. Containers do not establish absence of training-data knowledge.
- This repository and its website are public. Keep secrets, local environments, raw private chats and future sealed fixtures outside it. In particular, never feed `PROJECT_STATE.md`, the research review, evaluator answers or investigator-visible inventory into an agent that is meant to be blind. Build explicit allowlisted packs in fresh contexts.
- Write clear full sentences and introduce terms before examples. Keep explanation and progress separate. Match the playbook's colours and fonts. Use ordinary anchor navigation, which works on GitHub Pages.
- The user explicitly wants reasoned pushback when a point is mistaken or would weaken the experiment. Explain the disagreement and a workable alternative; do not manufacture disagreement or turn an untested idea into a finding. Bank website comments until the user requests application or release, as recorded in PROJECT_STATE.md.
- Do not use old sibling workspace folders as the source of truth or automatically copy from them. This checkout contains the editable website and current planning record.
