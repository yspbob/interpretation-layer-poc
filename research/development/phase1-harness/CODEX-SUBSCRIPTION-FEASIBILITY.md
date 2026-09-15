# Can we run the assessments through our Codex subscription?

15 September 2026. **The subscription connection works. The qualification route is not ready yet.**

Two small artificial questions completed through Codex CLI with ChatGPT authentication required and API credential environment variables excluded. No reserved question, reference or answer key was used. These are connection probes, not qualification answers or experimental guidance.

The subsequent [separate profile checks](CODEX-PROFILE-CHECKS.md) are complete using a local simulator. Three connection failures stopped without retries, but the client still advertised tools and no hard output token limit was established. The later [cost decision](EXECUTION-COST-DECISION.md) records the user’s choice of subscription only. Next test actual tool denial locally. Neither route should receive reserved questions until its configuration and collection procedure are fixed.

## What we checked

The installed client reports version `0.154.0-alpha.6.2`. Its bundled catalogue lists `gpt-6-astra` and High effort. Both probes requested those settings. The CLI reports ChatGPT login, and both invocations explicitly required that authentication method. These checks used the existing subscription; no API key was supplied.

Both answers matched the requested JSON schema. Each run had a different session ID. The first question supplied a random artificial marker. The second supplied no marker and asked the model to report one only if it was present in the conversation. It returned `NOT_PROVIDED`. This is a useful observation, but a model failing to repeat a marker does not prove that every unwanted source of context was absent.

The two completion events reported 9,937 input tokens and 67 output tokens in total. There were no tool execution events in the saved logs. Absence of a tool call does not prove that no tool was available. The logs also do not identify a served model snapshot, so the requested model and effort must not be presented as independently verified backend settings.

Two earlier launches failed during configuration loading, before any session or completion event. One used the wrong format for a list of settings. The other used `tools.view_image`, a documented field that this client rejected under strict configuration. Both failures are preserved. The successful probes used the recognized feature setting instead.

## What the instruction checks found

Separate local checks rendered prompts without invoking a model. We placed artificial markers in the temporary profile's global `AGENTS.md` and the temporary working folder's project `AGENTS.md`.

With `project_doc_max_bytes=0`, the project marker disappeared but the global marker remained. The positive control, with project instructions enabled, included both. A fresh task and disabled project instructions therefore do not, by themselves, establish an empty instruction context.

The first skill exclusion configuration named skill folders. The skill catalogue remained in the rendered prompt. Naming the actual `SKILL.md` files removed it in this client. The earlier assertion that both instruction markers would disappear failed; that failure is retained rather than reported as a passed isolation test.

Even after skill exclusion, the rendered input retained Codex permission, collaboration and environment messages. The local rendering command is not a capture of the exact request sent during the successful subscription probes. It shows why we need a fixed, inspected Codex configuration and why qualification would apply to that configuration rather than automatically to the API version.

## Requirements identified by the connection probes

The list below records the gates identified at this step. The later profile report distinguishes what was checked from what remains unresolved.

1. Use a dedicated clean profile. Keep personal instructions, project state, skills, memories, plugins and earlier sessions outside the assessment inputs. Verify the final configuration with artificial markers before exposing reserved material. Do not alter the user's ordinary Codex profile to achieve this.
2. Verify which tools the model can actually access and what happens on a connection failure. The two successful probes do not establish that tools are unavailable or that the client cannot make an internal retry.
3. Establish the usage limits, stop behaviour and records for the batch. Event logs and final answers are available; the exact request, complete tool definitions and raw provider response are not present in the captured JSON event stream. Resolve those audit differences explicitly before claiming equivalence with the API runner.

No qualification bank, role instruction, drafter instruction or scoring threshold changed. No additional live probe or qualification batch is scheduled automatically. The user authorised investigation of the subscription alternative; that does not authorise API spending or exposure of reserved cases through an unverified route.

Recorded totals are in [codex-subscription-feasibility.json](codex-subscription-feasibility.json). Full logs and investigation scripts are kept in the private record identified in `PROJECT_STATE.md`.

The relevant official documentation describes [subscription authentication](https://learn.chatgpt.com/docs/auth), [automated execution and event logs](https://learn.chatgpt.com/docs/non-interactive-mode), and [configuration controls](https://learn.chatgpt.com/docs/config-file/config-reference). Where this installed client's observed behaviour differs, the observations above take precedence for this experiment.
