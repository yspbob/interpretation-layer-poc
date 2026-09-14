# Choosing how to deliver the reviewer tests

14 September 2026. Decision support requested by the user after the desktop schedule paused. No replacement route or spending has been approved. The three captured answers remain unscored.

The current problem is the effort needed to deliver and preserve the tests. We do not yet know whether the reviewer passes them. Changing the delivery method must not become a reason to change the questions, remove difficult cases or relax the pass criteria.

## Options

| Route | Additional cash cost | Effort and limitations |
| --- | --- | --- |
| Continue Codex control of Claude Desktop | None while within the included allowance | The intervals between the first three submissions averaged 5.55 minutes. At that pace, 45 more would take about 4.2 hours, before additional setup or recovery. This extrapolation is based on only two intervals. It is not a model latency measurement. |
| User submits the prepared files | None while within the included allowance | Budget roughly 90 to 150 minutes of active handling, plus model waiting time. This is an estimate, not a measured manual trial. The user would submit each case separately and preserve the complete first answer. |
| Direct Claude API, sequential requests | Approximately $12 to $44 for 48 answers under the scenarios below | Most delivery and capture work can be automatic. Requires an Anthropic connection, tested settings and an authorised budget. Our existing batch controller and validation can be reused, but the current provider adapter is for OpenAI. |
| Anthropic Message Batches API | Approximately $6 to $22 under the same scenarios | Half the token price, with asynchronous completion. It changes the stopping procedure because other requests may already be running when a problem is detected. |
| Claude Agent SDK or noninteractive Claude Code | Potentially covered by a separate Max automation credit | Avoids desktop clicks and can save machine readable responses. Eligibility, credit balance, model access and the restricted configuration remain unverified. This is a different assessed configuration from the desktop app. |

The subscription routes still consume allowance and operator effort. They are not economically free. Anthropic documents Max access to Fable subject to shared weekly limits and a Fable allocation. Availability for the remaining schedule must be checked rather than inferred from the subscription name. See [Fable on subscription plans](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan).

## What the API estimate includes

The 48 frozen desktop inputs, each including the common wrapper, total 950,466 bytes. The smallest is 13,924 bytes and the largest 23,908. These are measured file sizes, not provider token counts. For planning, allow 250,000 to 500,000 input tokens across the schedule. This deliberately broad approximation allows for code, JSON and tokenizer differences. It is not an enforced upper bound. The final API message structure must be counted before setting a spending reservation. Anthropic offers a [token counting endpoint](https://platform.claude.com/docs/en/build-with-claude/token-counting); it was not called for this review.

Fable 5.1 standard prices are $10 per million input tokens and $50 per million output tokens. Its Batch API has a 50% discount. These rates were checked against the [official model page](https://platform.claude.com/docs/en/models/fable-5-1/overview) on 14 September. No cache savings are assumed.

| Average output per response, including reasoning | Standard API, 48 responses | Batch API, 48 responses |
| --- | --- | --- |
| 4,000 tokens | $12.10 to $14.60 | $6.05 to $7.30 |
| 8,000 tokens | $21.70 to $24.20 | $10.85 to $12.10 |
| 16,000 tokens | $40.90 to $43.40 | $20.45 to $21.70 |

These are scenarios, not a confidence interval or forecast of observed API usage. Hidden reasoning is charged as output; short visible JSON does not establish a cheap response. [Anthropic's thinking documentation](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) explains that the output allowance includes thinking and final text.

The estimates exclude tax, currency conversion, setup diagnostics, manual scoring and later experimental guidance or reference reviews. The existing Astra preparation proposal of $150 is separate and remains unauthorised. Its 144 qualification calls have a proposed maximum reservation of $117.9648 at the existing input, output and conservative rates; this is not expected spending. Current [Astra prices](https://developers.openai.com/api/docs/models/gpt-6-astra) match those rates.

A possible Fable qualification ceiling is $60: 48 requests reserving 32,768 input tokens at $12.50 per million and 16,384 output tokens at $50 per million total $58.9824. This calculation is conditional on verifying the input bound and prices, enforcing those settings and retaining truncations as failures. It does not establish that 16,384 output tokens are sufficient at High effort. That limit needs a public development check and a recorded configuration before qualification. Diagnostics would need their own allocation. No such budget or new output limit is approved here.

## The Max automation credit

Anthropic's [Agent SDK billing guidance](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) states that eligible Max 5x accounts can claim $100 monthly and Max 20x accounts $200 monthly for Agent SDK and noninteractive Claude Code usage. This is separate from interactive subscription usage and requires an initial opt in. Paid continuation can occur if usage credits are enabled after the included credit is exhausted. Direct API key use does not receive this credit.

The user's plan variant, eligibility, claim status and remaining balance have not been inspected. The previous permission to use included desktop allowance does not authorise activating credit or paid continuation. Check the account before relying on this option.

Claude Code documents structured response capture, restricted operation and controls for built in tools, MCP and customisation. See the [programmatic usage guide](https://code.claude.com/docs/en/headless) and [CLI reference](https://code.claude.com/docs/en/cli-reference). These make it a plausible route, not a qualified one. Check all effective instructions and tools, fresh context, model identity, usage and complete first response records. In particular, one application turn must not be assumed to mean one provider request; retry and fallback behaviour need verification. Do not create a large integration solely to avoid a modest API bill.

## What manual submission would involve

Prepare numbered local folders with only the allowed input, the fixed prompt, an operator checklist and a destination for the answer. Expected answers and investigator notes stay elsewhere. The existing packages already contain the allowed inputs; preparation would mainly make the operator steps and return locations easier to follow.

For each of the 45 remaining positions, the user would check the settings and allowance, open a fresh incognito chat, attach that position's file, send the fixed prompt once, and save the first complete response with the required screenshots and model observation before closing the chat. No correction, regeneration or second attempt is permitted. A local import check can detect missing fields or incomplete records without scoring correctness. Copying and validating a response must not edit its wording.

Folders can be grouped for convenience, but cases cannot share one conversation or one combined attachment. The user would act as operator, not as an independent subject expert or answer adjudicator. Changing operator can retain the existing app configuration, but record the change and rehearse the capture procedure on public material first. Fresh contexts and honest records do not prove that provider hidden context or prior training familiarity is absent.

## Recommendation and treatment of the first three answers

Prefer sequential direct API delivery if a modest separate budget is acceptable. It provides the simplest inspectable request and response record and can stop before the next request when a required control fails. Check the Max automation credit as a bounded alternative if avoiding that cash spend is important. Prefer manual submission over further screenshot driven automation if the subscription desktop route is retained.

The Batch API saves roughly $6 to $22 in these scenarios. For this small schedule, that saving does not justify making cancellation and failure accounting more complicated before the simpler route works. The provider documents completion within up to 24 hours, possible expiry, concurrent processing and cancellation that is not immediate. See [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing).

Browser automation might avoid native file dialog problems but would still need capture and access checks. A different or cheaper model would change the reviewer being tested and require its own qualification. Deferring Fable is possible, but removes the extra model assessment the user requested. None of these is the preferred next step merely to rescue the existing UI method.

The user also asked for further alternatives. A small local submission assistant could present the next allowed input and prompt, then accept and validate the pasted first response. The user would handle Claude while local software handles numbering, completeness and saving. This is a proposed convenience tool, not implemented or a replacement for app access evidence. A pasted answer alone does not prove which model or context produced it.

Interactive Claude Code operated by the user is another subscription route. The billing guidance above distinguishes it from noninteractive automation: interactive use consumes the subscription allowance. Saved session records may reduce capture work, but the effective instructions, tools, retries, model and raw answer records still need checking. Running an automated schedule through an apparently interactive interface must not be used to misrepresent its billing route.

A reduced Fable role is a substantive design option: Astra supplies scored assessments, while Fable only challenges reference rules and disputed conclusions. Every objection still needs source or behaviour checks. This would avoid claiming an unqualified Fable score, but would remove the planned second scored assessment and weaken that part of the comparison. It requires explicit agreement and an amended plan, not relabelling the existing unfinished qualification as complete.

Keep all three desktop responses and their limitations. If the user takes over the same tested desktop configuration, resume at position 004 after documenting the operator change. If delivery switches to the API or Agent SDK, declare and qualify that configuration separately, normally using the full unchanged 48 response schedule. Do not pool three desktop answers with 45 answers from a different configuration or select the better response. Document prior exposure of three scheduled inputs; no semantic scoring or prompt tuning has occurred. A configuration change requires an amendment before calls, not silent replacement of the current freeze.

No new model requests, account changes, uploads or correctness scoring occurred during this options review. The website update remains banked. The immediate decision is delivery route and any associated budget, not a change to the research questions or pass criteria.
