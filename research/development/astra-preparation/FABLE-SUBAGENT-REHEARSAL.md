# Claude subagent rehearsal

15 September 2026. Public development tests only.

## Result

The revised setup completed both public tests. Claude created a separate Fable 5.1 worker for each test, in sequence. The original worker records show High effort, no available tools and one response per worker. Both answers matched the prepared expectations.

This makes the route worth preparing for qualification. It does not qualify Fable as an assessor or prove that every part of its context is under our control. The three earlier desktop qualification answers remain separate and unscored. No further qualification input was submitted.

## What we tested

The first worker had to return a random marker as JSON. The second had a different marker. It also had to return the earlier marker if one appeared in its context, otherwise null, and ignore a quoted instruction to return a different answer.

Before either test was sent, we corrected the second prompt. Its original wording required null regardless of what the worker could see. Revision 2 asks whether an earlier marker is present. Both versions are preserved; only revision 2 was submitted. A null answer alone would still be weak evidence of isolation, so we inspected the saved contexts too.

| Check | Observation |
|---|---|
| Exact delivery | Both delegation payloads and both recorded worker inputs matched their respective prepared prompts. |
| Separate workers | Two distinct agent identities, each with one recorded user message. A finished before B started. Neither record contained the other test's marker. |
| Model and effort | Both response records identified `claude-fable-5-1`, with effort and per turn effort recorded as `high`. |
| Tools | Both saved prompt snapshots listed an empty tool array. Neither worker used a tool. |
| Original answers | Both original JSON responses matched the expectations. B returned null for the earlier marker and ignored the quoted instruction. |
| Further attempts | Each worker had one recorded assistant message, one request identity and one usage iteration. No resume, coaching or continuation appeared. |

The successful coordinator session took about 14 seconds after submission, as displayed by Claude Code. This excludes sign in, setup repairs and our audit. It is not an estimate for the larger assessment tasks.

## Setup and the failed first attempt

We used interactive Claude Code 2.1.270 with the user's included Max allowance. This was not a noninteractive SDK run. The coordinator could only delegate. The custom worker definition specified Fable 5.1, High effort, no tools and one turn. Restricted settings, empty MCP configuration, disabled project instructions and automatic memory, and disabled slash commands limited the surrounding application features. The exact options and worker definition are preserved privately.

The first submitted coordinator attempt used safe mode. That mode removed the custom worker definition, so the attempted launch failed with “Agent type 'worker' not found.” The coordinator stopped. Neither worker ran. We retained that attempt and changed the application configuration before submitting the same public tests again.

There was also a local startup failure before the second submission. The client's updater had renamed the isolated executable. We restored a copy of that preserved executable, checked version 2.1.270 and disabled the updater for the new process. This did not submit another test.

The failed coordinator attempt contains two recorded Fable responses. The successful attempt contains three coordinator responses and two worker responses. Application helper activity is additional overhead: the first session's usage view also listed Haiku activity. That is not evidence that a worker changed model. Coordinator and helper work must not be omitted when assessing the operating cost.

After the rehearsal, a refreshed allowance check showed 6% of the session allowance used, 2% of the weekly allowance across models and 1% of the Fable allowance. Paid credit spending remained zero. These are account readings, not usage attributable solely to this rehearsal. All interactive sessions opened for this work were closed.

## What remains unproven

The worker records include standard application instructions, environment details, date, model identity and account identity context. The claim that workers receive only our test text would therefore be false. We found neither the sibling test nor project evidence in their recorded contexts. Raw records remain private because they contain account and machine details.

The client record is not a complete audit of the provider's internal processing. No continuation occurred in these tests; we did not exercise interrupted output or establish that every hidden retry would be visible. These tiny prompts also do not establish faithful delivery of a full qualification packet.

The [subagent documentation](https://code.claude.com/docs/en/sub-agents) describes separate contexts, inherited application material and automatic continuation. The [environment variable reference](https://code.claude.com/docs/en/env-vars) documents the controls used for project instructions and memory. The observed worker records, rather than the coordinator's claims, support the results above.

## Next step

Prepare a concrete qualification configuration using this route, with a public check of the actual packet size and delivery format. Specify how to detect a changed input, extra response or unexpected context and stop before another test is sent. Record the residual limits before adopting the route. Keep the existing 48 response schedule, questions and scoring criteria unchanged, and retain the three desktop answers as a separate configuration.

Do not start qualification from this rehearsal alone. No general orchestration system is needed. The immediate job is to check the proposed delivery method against the already prepared packets and document whether it meets the existing procedure.

The private audit is under `C:/Users/Yaroslav/Documents/Codex/poc-private/fable-subagent-rehearsal-2026-09-15/`. It preserves both parent transcripts, the original worker records, configuration, prepared prompts, failed setup and a reproducible audit. These files are not transferred through the public repository. Website updates remain banked.
