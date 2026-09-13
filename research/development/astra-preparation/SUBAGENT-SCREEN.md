# Preliminary familiarity screen using Astra subagents

At the user's request, the prepared questions were run through fresh Codex subagents on 13 September 2026. This gives us a first observation without building the separate API screening connection. It does not qualify that connection or replace the controlled execution requirements for the study.

## Result

Neither repository produced an exact match to a hidden source completion. The controls produced no exact matches either. All 24 responses were valid JSON; one control response used the permitted empty completion.

| Material | Distinct excerpts | Responses | Exact matches |
|---|---:|---:|---:|
| NetBox source | 3 | 6 | 0 |
| Controls paired with NetBox | 3 | 6 | 0 |
| HTTPX source | 3 | 6 | 0 |
| Controls paired with HTTPX | 3 | 6 | 0 |

Under the scoring rule written before execution, this is **no specific recall signal in these selected excerpts**. It is not evidence that Astra has never encountered NetBox or HTTPX. The model could know the projects without recalling these particular sentences exactly. Six source excerpts provide little coverage, and the controls do not establish the detector's sensitivity.

Several answers described what the visible code was doing. That was not sufficient for an exact recall score. We did not loosen the rule after seeing plausible answers. Both repositories remain candidates; this result does not settle their suitability or remove the public source limitation.

## How the run was performed

The parent dispatched 24 new subagents, one per prepared request, requesting gpt-6-astra with high reasoning effort. Each spawn used `fork_turns: none`, so it did not inherit this investigation's conversation. Each task received the same fixed instruction and its one masked excerpt, without the scoring key or other probe answers. At most three subagents ran concurrently. Dispatch followed the previously prepared order; completion order could differ.

No subagent was asked to check its own answer, score another answer or inspect the repository. Each returned a single completion. The parent saved all responses before applying the existing exact match scorer. Normalisation changed whitespace only. Repetitions of one excerpt were not counted as independent source examples. No failed score was retried.

The completed source and control questions are exploratory screening material. Keep them and their outputs out of experimental role contexts. If they inform a revised detector, record that development exposure before choosing new diagnostic material.

## Differences from the planned API screen

These differences were disclosed before dispatch:

* The instruction prohibited tool use, but tool capabilities were not disabled. This run has no independent tool activity audit or tested access denial.
* The application manages additional instructions and provider requests. We recorded the submitted task prompts and requested model settings, not the complete provider input or an immutable backend version.
* The API's output limits, service tier, usage records and batch spending ledger were not applied. This run used Codex capacity. No project API key or API runner was used, and no claim of zero account cost is made.

The private record contains the submitted prompt text reconstructed from the prepared packets, the agent task names, all returned JSON answers and hashes. The model tool calls in the parent conversation record the actual dispatches. This is less complete evidence than recording and auditing each provider request. The public [result record](subagent-results.json) contains counts, item outcomes, limitations and hashes without publishing the excerpts or hidden completions.

## Next step

Prepare the separate qualification cases and their supporting evidence. The familiarity observation does not qualify the verifier or assessors. Before formal API results, finish the required access and account checks and establish whether this screen matches the eventual model configuration. The planned controlled screen remains pending; any decision to accept the preliminary observation in its place needs an explicit protocol change before scored runs. No API spending is authorised by the user's request to use subagents.
