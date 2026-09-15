# What the separate Codex profile established

15 September 2026. **The local investigation is complete. The subscription runner is still not ready for qualification.**

We tested the installed Codex CLI with four empty profiles and artificial questions. Each profile sent its request to a small simulator on this computer. The simulator supplied either an answer or a connection failure. It did not forward requests to a model, and none of the four requests contained an authentication header. No model tokens were used by these checks.

This let us inspect what the client actually sent. It also let us test failures without risking the reserved questions or paying for unsuccessful attempts. The user's normal Codex profile was unchanged.

## What worked

The four captured requests contained the artificial question and the supplied test instruction, along with Codex's own permission, collaboration and environment messages. They did not contain the project state or a skills catalogue. These were newly created profiles, with no copied credentials or conversation history. They are test profiles, not an authenticated assessment installation.

The client made exactly one request in each of these tests:

| Simulator behaviour | What the client did |
| --- | --- |
| Returned an artificial answer | Recorded the answer and completed the turn. |
| Returned a server error | Recorded a failed turn and stopped. |
| Closed the response stream early | Recorded a failed turn and stopped. |
| Left the response stream idle | Reached the configured idle timeout, recorded a failed turn and stopped. |

Request and stream retries were both explicitly set to zero. No retry occurred in these three failure cases. That is evidence for this local provider configuration; it does not establish the behaviour of every failure or the authenticated subscription route.

## What prevents us from using it yet

**The requests still advertise tools.** Disabling the relevant features did not remove all tool definitions. The captured requests included execution, user input and agent collaboration tools, with automatic tool choice. The client warned that its code execution host was disabled and would fail closed. We did not attempt tool execution, so this is evidence of advertised tools, not proof that they could run. It is also not proof that they were safely unavailable.

The first summary looked only for a top level `tools` field and recorded null. The definitions were actually inside an `additional_tools` input item. A second audit found and recorded them. The original summary is preserved with this correction; null must not be read as a successful tool exclusion check.

**A hard output token limit is not established.** None of the captured requests included `max_output_tokens`. A process deadline can limit how long the local program runs, but it does not establish a provider generation limit. The simulator's usage numbers were invented to test the event format. They are not evidence that a real usage stop works.

**The record is complete only for this simulator.** We saved the exact local request bytes, the artificial response and the client events. That does not demonstrate the same capture on the authenticated subscription connection. This check also did not use the assessment response schema. The earlier live connection probes returned structured answers, but the combined assessment configuration has not been verified.

## The practical recommendation

Do not send the qualification bank through this configuration. The investigation found enough uncertainty to make further integration a separate piece of work. It did not show that subscription execution is impossible.

My recommendation is to price the existing API runner before building a workaround. That runner already has explicit request limits and collection controls tested in simulation. Actual model access, account settings and costs still need verification. Preparing a costed option makes no model call and does not commit the user to spending.

The next step is therefore to establish that concrete API option, then decide whether the subscription savings justify more work. The user has not approved an API allocation or adopted a different experimental method. The 144 response schedule, questions, role instructions, drafter and acceptance requirements are unchanged. Astra remains unqualified, with zero qualification answers and zero experimental guidance runs.

The private evidence commitment covers 30 files, including both the initial summary and the corrected audit. Its hash is `c3c6a169177b524c799be2e36a13833690282f1575c2fafc83b453e5b5e18cfa`. The profile databases and bundled skill copies remain private and are outside that commitment. See `PROJECT_STATE.md` for the local location. The [earlier subscription investigation](CODEX-SUBSCRIPTION-FEASIBILITY.md) retains the two actual connection probes and their separate usage record.
