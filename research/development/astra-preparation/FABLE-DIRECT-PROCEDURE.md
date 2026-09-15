# Fixed procedure for direct Fable assessment

15 September 2026. Configuration `fable-direct-v1`. The user chose direct delivery operated by Codex. Use included Max allowance only. This record does not claim assessor qualification.

## The work to run

Use the original 48 input files in their frozen order. Their role instruction, sources, candidate, reference criteria and response schema remain unchanged. Each file receives a new interactive assessor session. The three responses previously collected through Claude Desktop stay separate and unscored.

The existing four scoring gates remain unchanged: no serious errors; at least 44 successful responses overall and 10 in each family; at least 22 consistent repeat pairs with correct reasons; and at least seven successful baseline versus alternative comparisons. The full definitions in the preserved QUALIFICATION.md govern scoring. Do not inspect expected answers or change the criteria during collection.

## The fixed application setup

Use Claude Code 2.1.270, model `claude-fable-5-1`, High effort, and the frozen custom worker as the primary agent. The frozen configuration specifies restricted settings, empty MCP configuration, no tools, disabled project instructions and automatic memory, and a disabled updater. Clear API credential overrides. Stop if the subscription provider or environment redirects execution to an unapproved provider or billing route.

Create each session in a separate neutral folder outside the POC repository. Copy only agents.json and mcp.json there. The operator loads the permitted input locally and inserts its complete text directly; a model never copies it and the assessor has no file reading tools. Keep the package schedule, investigator notes, freeze, answers, audit files and earlier responses outside the session folder.

The CLI adds standard application instructions, environment, date, model and account context. Preserve that context in private records and check for project instructions or other study material. This is not a claim that the provider sees only our packet. No hidden provider retry or training familiarity guarantee is made.

## Before sending each file

Verify the package freeze, exact file hash and client version. Confirm Fable 5.1 High and Claude Max. Refresh the usage view before every submission. Pause when any relevant usage window is 80% used or more, or allowance is uncertain. This conservative pause point does not change the qualification criteria. Do not enable paid continuation. Account usage is an observation, not a technical spending cap; Codex must supervise the run.

Create a private attempt directory exclusively for that position. Record its input and configuration hashes, session identity, actual settings, allowance observation and time. An existing attempt record must be inspected, never overwritten or silently restarted. Save the source bytes before dispatch. Mark dispatch immediately before submitting once. An uncertain dispatch is an unsuccessful attempt, not permission to retry.

## Capture and check the result

Retain the original application transcript and first response. Wait no longer than fifteen minutes after dispatch. If unfinished, preserve the transcript at the deadline, interrupt the session and keep later text separately. A late answer cannot replace the deadline result.

Run the local audit against the actual submitted file. It checks exact user input, an unchanged worker instruction, client version, model and High effort, empty recorded tool lists, tool events and recorded response identities. Streaming fragments with the same response identity count as one response. Extra identities or iterations, missing records, compaction, API errors and access deviations stop collection before another submission.

The operator also checks visible warnings, final completion, permitted application context and timing. The audit cannot prove that unrecorded provider attempts did not occur. Preserve uncertainty and stop when the first answer cannot be identified. Do not use maxTurns as proof of one generation.

Use the existing strict answer validator, candidate identity and exact claim and reference coverage checks. Preserve raw text. One enclosing JSON Markdown fence may be removed only for parsing; never repair the answer. More than 128,000 answer bytes fails the local limit. A completed structural failure remains unsuccessful and may proceed to the next position only when delivery and access controls are intact.

Save the audit, usage after the response and the original records outside public Git before closing the session. Close it without another model prompt. Do not retry, resume, coach or ask for a corrected answer. Resume an ordinary pause only at a never submitted position after checking all prior attempt records.

## What to report

During collection, report counts, failures, timing and allowance. Do not score reasons or reconcile the model's answers until the full schedule completes or is formally stopped. Apply the original scoring criteria afterwards and report every unsuccessful or unrun position. A pass would apply only to this supplementary assessor configuration and tested scope.

The operator uses local file handling, transcripts and the existing validator. Routine interface work should not become a separate development project. User intervention is reserved for sign in or an account action that genuinely needs them. No further public model rehearsal is required for this unchanged configuration.
