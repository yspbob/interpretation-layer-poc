# Use the existing subscription

15 September 2026. **The user chose subscription only. Do not set up or charge an API account for this work, and do not use paid credits.**

We priced the API after the local Codex checks left several controls unresolved. The conservative proposal was $240 for 144 assessments and $10 for connection checks, before tax. The user rejected that cost. The API account has not been set up. No API request or charge occurred.

The price calculation is retained for traceability, not as a requested budget. At the published Standard rates, the model costs $10 per million ordinary input tokens, $12.50 for cache writes and $50 for output, including reasoning. We budgeted all input at the highest of those input rates rather than assume caching savings. Cache writes replace the ordinary input rate; they are not an extra fee on top. [Pricing](https://developers.openai.com/api/docs/pricing) and [cache accounting](https://developers.openai.com/api/docs/guides/prompt-caching).

| Reasoning and answer tokens per assessment | Cost for 144 assessments, using the full input allowance |
| --- | --- |
| 4,096 | $88.47 |
| 8,192 | $117.96 |
| 16,384 | $176.95 |
| 25,000 | $238.98 |

These are scenarios, not predicted usage. Each assumes 32,768 input tokens. The earlier simulation used an 8,192 output limit, without evidence that this was enough for Astra. OpenAI recommends initially allowing at least 25,000 reasoning and output tokens; that recommendation informed the larger proposal, but it does not prove our questions need that many. [Reasoning token guidance](https://developers.openai.com/api/docs/guides/reasoning).

An offline preflight with gpt-6-astra, High effort and the proposed larger output allowance passed for all 72 distinct requests. It read the 18 permitted bank files with socket connections blocked. The largest serialized request plus padding was 32,740 bytes. That is not a verified provider token count. The [calculation record](astra-api-cost.json) retains these figures. No account access or output sufficiency was established.

## What changes now

The API recommendation was premature. The [profile investigation](CODEX-PROFILE-CHECKS.md) found advertised tools, not successful tool execution. It also failed to establish an API style output spending cap. Neither observation, on its own, proves that subscription execution cannot support this assessment.

For the subscription route, distinguish three controls:

* **Evidence isolation:** each assessment must receive only its permitted packet in a fresh context. It must not obtain other files, earlier answers or another agent's context.
* **Execution limits:** fix the model, effort, attempt count and operational time limits before qualification. Record usage and stop on unexpected activity or incomplete collection. There is still no automatic retry.
* **Payment limits:** use only the included allowance. Verify that paid usage is disabled and stop when the included allowance is unavailable or its status is uncertain. A subscription run is not free of resource costs, even when it adds no charge.

A finite request count and a local deadline do not prove a hard provider token cap. Any change from the API controls needs an explicit subscription protocol amendment before reserved questions are sent. Do not silently apply weaker controls or present the two routes as identical.

## The next small check

The user pointed to completed Fable delivery as the practical precedent. Its [48 collected answers](../astra-preparation/FABLE-QUALIFICATION-RESULTS.md) establish that subscription delivery and automatic collection can work for this project. Reuse its frozen packet, fresh session and first answer recording pattern. Preserve the later correction about stale account readings. This supports trying the same approach with Astra; it does not establish that Codex has the same controls as Claude Code.

Use the local simulator to attempt harmless tool calls in the clean test profile. Check whether each advertised path is disabled or denied before execution, and retain both the attempted call and the denial. No model or reserved question is needed for this check.

Codex documents a PreToolUse hook that can deny local calls before execution, including nested calls from code mode. Its documentation also warns that hosted tools and some specialized paths are outside that hook mechanism. A hook alone is therefore not an established isolation boundary. Verify the actual exposed paths, configuration and failure behaviour before relying on it. [Documented tool coverage and denials](https://learn.chatgpt.com/docs/hooks).

Keep this investigation bounded. If it cannot establish the required isolation, report the specific unresolved path and offer an explicitly limited development exercise. Do not charge the API, reduce qualification standards without agreement, or describe an uncontrolled run as qualification.

The questions, 144 response schedule, role instructions, drafter and acceptance requirements remain unchanged. Astra remains unqualified. There are still zero experimental guidance runs.
