# Codex blocked the tested tool calls

15 September 2026. **The local tool check passed for all ten advertised paths.** No model was called and no reserved question was used.

We made a local simulator return harmless tool requests to the real Codex client. This tests what the client does when a tool is requested, without relying on a model to choose the right test. Eight paths were denied by a hook before their tool handler ran. The two execution paths refused because the code execution host was disabled.

| Tested paths | Observed result |
| --- | --- |
| Execution and waiting for execution | Both refused: code execution host disabled. |
| The two user input tools | Both blocked by the deny hook. |
| Listing agents, sending messages, requesting follow ups, interrupting, spawning and waiting | All six blocked by the deny hook. |

No real agent was started or contacted. The spawn test omitted required arguments, while messaging tests used nonexistent targets. The hook denied those calls before argument handling. This checks the dispatch boundary, not every possible argument combination.

## Why we trust this particular result

A control test requested the agent list without the hook. It returned the artificial session's root agent. With the working hook, the same call returned a denial instead. A separate startup marker confirmed that hooks loaded. The audit checked each captured request and response, including the tool definitions and absence of authentication headers.

The first configurations did not block the agent listing call. We retained those failures. An interactive check also exposed a hook command failure. The working Windows configuration uses an explicit clean profile, a hooks file, and PowerShell's invocation operator before the quoted Python command. The corrected configuration worked in noninteractive execution, so an interactive collection interface is not required by this result.

The test invocation explicitly trusted only its inspected local hook definitions using Codex's documented automation option. The ordinary user profile was unchanged. The hook and its configuration must be inspected and committed before any assessment launcher uses that option.

## What this permits next

Reuse the Fable delivery pattern with a small Codex adapter: load the frozen packet directly, start a fresh session, retain the first answer and check its identity. Fix the working profile and require a successful local startup and denial check before dispatch. Stop collection on configuration drift, hook errors, attempted tool use, extra turns or uncertain allowance. Do not silently accept a run whose tools became available.

The earlier failures also show that a broken hook can leave a tool callable. This result is not a general containment guarantee. [Codex documents exceptions to hook coverage](https://learn.chatgpt.com/docs/hooks), so any newly exposed tool requires review. The tested calls cover the actual ten path catalogue in this installed version; hosted tools were not present in that catalogue.

Next prepare the bounded launcher and collection audit without model calls. Then define a small public subscription check using the actual assessment schema, subject to verified included allowance and disabled paid usage. The reserved qualification batch remains unopened for model execution until its subscription protocol and collection checks are ready.

All 21 completed artificial sessions and 42 local requests are recorded across the configuration attempts and final checks. Those request counts are not model calls or retries of qualification questions. The [aggregate audit](codex-tool-denial-results.json) identifies the ten paths and private evidence commitment. The 288 committed files preserve configurations, inputs, simulated responses, failures and audit scripts. Generated runtime databases are outside that commitment. Astra remains unqualified, with zero qualification answers and zero experimental guidance runs.
