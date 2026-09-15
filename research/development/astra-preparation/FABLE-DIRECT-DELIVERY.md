# Deliver the assessment file directly

15 September 2026. The user has chosen this route, operated by Codex. The [fixed procedure](FABLE-DIRECT-PROCEDURE.md) and private freeze govern qualification. No qualification calls through this route are recorded in this development report.

## Why change the delivery method?

The two small subagent tests worked, but the larger public packet exposed a problem. The coordinator read a 30,037 byte file and generated a 31,093 byte prompt for its worker. The source text changed. The worker still returned a valid JSON assessment, so checking the response format alone would have missed the delivery failure.

This route also asks the coordinator to generate thousands of tokens merely to copy a file. We will not use that relay for the real tests. A fresh assessor session can receive the file directly, without a coordinator model rewriting it.

## What the direct check established

A local program loaded the public file and inserted its text into a fresh interactive Claude Code session. The saved user input matched all 30,025 bytes, including the final newline. The full assessment instructions, schema and packet also matched after parsing. This sample exceeds the largest frozen qualification attachment, which is 23,555 bytes.

The response record identified Fable 5.1 at High effort. The saved tool list was empty and there were no tool calls. One recorded response contained the correct candidate identity, all twelve claim decisions and all twelve coverage decisions. The existing response validator accepted it. We did not use this artificial example to estimate assessor accuracy.

The direct session displayed 20 seconds of response time. The failed relay displayed 2 minutes 5 seconds for its coordinator and worker. These are observations from different public samples, not a controlled speed or cost comparison. Both used included Max allowance; refreshed paid credit spending remained zero.

## A preparation mistake we preserved

Our first synthetic packet used invalid values for the candidate kind and provenance fields. The packet renderer did not check that nested candidate schema. An initial local audit also called the schema validator with reversed arguments. We corrected that audit, preserved the failure and validated the corrected candidate before the direct submission. The direct result passed the correctly invoked validator.

The earlier sample still demonstrates a source copying error: the original and delegated source strings differ. It cannot establish handling of a valid qualification input. Neither sample contained private qualification evidence or scoring keys. No frozen question or reference changed.

## Selected operating configuration

Use interactive Claude Code 2.1.270 with a custom assessor as the primary agent, explicit `claude-fable-5-1`, High effort and no tools. Use restricted settings, empty MCP configuration, disabled project instructions and automatic memory, and a disabled updater for the process. Clear API credential environment overrides and verify Claude Max before submission. The exact tested options and worker instruction are saved with the private audit.

Start a new session for each scheduled response. Load only that position's unchanged input.txt through the local file loader, then submit it once. Do not ask a model to copy it, pass a path for the assessor to explore, or resume an earlier assessment. Keep the prepared assessor instruction separate from the packet and commit both before qualification.

Before each call, check included allowance, the frozen file hash, client version and model settings. Pause if allowance is uncertain or insufficient. Use the existing fifteen minute deadline and 128,000 byte answer processing limit. Preserve the first response and any failure. Never retry or coach a submitted item.

After each response, compare the recorded user input byte for byte with the permitted file. Inspect original response records for model, effort, tools, extra user messages, additional responses and completion. Run the existing structure and identity checks. Stop before the next item on a delivery or access deviation; retain invalid answers without repair. Defer semantic scoring until completion or formal stop.

The new route must use its own complete 48 response schedule and configuration record. The three desktop responses remain separate and unscored. Reuse the unchanged questions, order and four scoring gates, not the old desktop captures as substitutes for new positions. All 61 files in the original desktop freeze were verified unchanged after these checks.

## Limits and next action

The client adds application and account context. Fresh sessions and matching saved inputs do not reveal all provider processing or establish absence of prior model knowledge. No interrupted output occurred in these checks. Any unidentifiable continuation or retry remains a qualification limitation; do not certify it from a single response record.

The direct procedure uses a private freeze and a local audit against the existing 48 packets. These use file and transcript checks with the existing validator. They do not require another desktop clicking workflow or a general orchestration system. The direct packet check is complete; do not repeat it without a relevant change or unresolved failure. PROJECT_STATE.md records the current freeze and execution position.

The private record is `C:/Users/Yaroslav/Documents/Codex/poc-private/fable-packet-check-2026-09-15/`. It retains both attempts, exact inputs, original outputs, preparation mistakes, audits and usage observations. Raw account and machine context stays outside public Git. The website update remains banked.
