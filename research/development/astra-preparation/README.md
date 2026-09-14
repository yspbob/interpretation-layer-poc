# Prepare the first Astra checks

Astra remains the model for the controlled workflow. On 14 September, the user added [Fable 5.1 through Claude Desktop](FABLE-DESKTOP.md) as a supplementary guidance assessor using the included Max allowance. Its settings, record capture and qualification are still pending. The Astra schedule is unchanged; no Fable review or API spending has occurred.

We will first look for signs that Astra can recall details from NetBox and HTTPX. Then we will test the verifier and assessors against cases with defensible expected answers. A preliminary screen has now run through 24 fresh Astra subagents at the user's request. It found no exact matches to the selected hidden source text. The controlled API screen and assessment qualification have not run. No API spending has been authorised. See [the result and its limits](SUBAGENT-SCREEN.md).

## What is ready

[All four qualification cases](BANK-READINESS.md) are prepared and checked, with their source evidence and expected answers kept private. Across the bank, 42 authored scenarios passed and 13 deliberate faults were detected. Fourteen upstream test invocations and three separately recorded adapted methods passed. These are checks of four families, not model qualification.

The proposed settings and allocations are in [settings.json](settings.json). The offline packet builder prepares 24 separate requests and keeps the answers in a different file outside the public repository. It has no provider connection, credential handling or live mode. The request builder and exact match scorer have automated checks using public toy examples.

The private screening material contains three source excerpts and three authored controls for each repository. Each item is scheduled twice in a fresh request. The source revisions are the existing NetBox starting revision d13c98b9ea8c55dafdcdecbf3058a731814a7ead and HTTPX b5addb64f0161ff6bfe94c124ef76f6a1fba5254. These are deliberately chosen diagnostic examples, not a random sample of either repository. NetBox and HTTPX remain development material; four separate qualification families are now prepared.

The private folder contains the selection specification, provenance, exact expected completions, requests and a hash manifest. It is local to the preparation machine. Public Git sync does not transfer it to the laptop. The request file alone is eligible for the screening transport; neither the scoring key nor this project conversation is a model input.

## How to read the familiarity result

Each source excerpt hides at least seven words from a comment. The model must return one completion. We retain the surrounding code, including ordinary project clues, but do not supply the file path, revision, answer or whether the item is a control. The authored controls cover similar programming situations. They cannot establish the probability of recalling public code, and their wording may be harder or easier to guess.

The primary measure is an exact completion after whitespace is normalised. Case, punctuation and spelling must still match. A sensible paraphrase does not count as specific recall. Report paraphrases as observations, without changing the score. Repeated completions of one excerpt remain one item when interpreting familiarity.

For each repository, apply this provisional diagnostic rule before deciding what the answers mean:

1. If at least two distinct source items match exactly on both repetitions, and no control matches, report a specific recall signal consistent with familiarity.
2. A single source match, inconsistent repetitions or any control match makes the interpretation inconclusive. Preserve all counts and inspect whether the prompt made the answer predictable. Do not upgrade a result using a new threshold.
3. If no source or control matches and all requests completed validly, report that these probes found no specific recall signal. This is not proof that the model has never seen the code.
4. Missing, refused or invalid answers make the screen incomplete. Keep them in the report. Do not replace them automatically.

This is a small diagnostic, not a validated membership detector or a statistical test. Its threshold is a proposed operating rule. A positive result does not automatically exclude a repository. Record the indication, examine the relevance of the recalled material and retain the public source limitation. Final source selection may require another screen if it uses different material. The historical task diagnostic in plan section 2A remains a later case selection step before Phase 2.

## Model settings and proposed spending

Use `gpt-6-astra` with high reasoning effort and the standard service tier. Each request has no tools, shared conversation or previous response. The same model and effort are proposed for the four Phase 1 roles. Their role prompts and input permissions remain different, so this screen is not a test of every role's propensity to recall information. No dated immutable model snapshot has been verified; record the requested and returned identity and the service date, and stop on an unexpected identity.

The [official model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) was checked on 13 September. The reservation calculation uses $12.50 per million input tokens, allowing for the stated cache write rate, and $50 per million output tokens. The proposed input sizes stay below the higher price threshold. These are estimates for approval, not verified account charges or an invoice guarantee.

| Stage | Maximum scheduled calls | Proposed allowance |
|---|---:|---:|
| Connection check and familiarity screen | 1 ordinary check plus 24 probe calls | $10 |
| Separate development calibration | 12 calls | $10 |
| Qualification, after its cases are ready | 144 calls | $120 |
| Reserve, requiring a separate allocation | None yet | $10 |
| Total preparation proposal | | $150 |

For screening, reserve up to 8,192 input and 4,096 output tokens per call, or $0.3072 at these rates. The 25 scheduled calls reserve at most $7.68. Qualification and development allow 32,768 input and 8,192 output tokens per call, or $0.8192. Reasoning tokens use the output allowance. An incomplete answer at that limit is retained; changing a limit creates a new configuration.

The $150 is a proposed ceiling for preparation only. It does not include experimental guidance runs or Phases 2 and 3. Each stage needs its own explicit allocation before execution. Unused money does not authorise more attempts, and the reserve does not authorise retries. There is no automatic top up or parallel execution on both machines.

## What must be finished before a paid request

The existing adapter supports the four study roles. It does not yet accept the separate familiarity request format. Connect the prepared requests through the same destination, freshness, logging and spending controls, with a ledger covering the whole screening batch. Test that connection with simulated replies and denied network access. Do not call the SDK directly from this offline builder to bypass those controls.

Check the actual account's model access, training opt in and retention settings, and establish the input token bound. The [provider data policy](https://developers.openai.com/api/docs/guides/your-data) distinguishes model training, response storage and abuse monitoring. Sending `store: false` does not establish zero retention or verify the account settings. No account setting has been inspected here.

Freeze the final packet and request hashes, scoring rule, order, settings and authorised allocation before dispatch. The ordinary connection check must contain no probe or qualification answers. Complete the required familiarity work before final experimental material selection. The separate cases described in [QUALIFICATION.md](QUALIFICATION.md) can be prepared while the controlled execution gates remain open. All four are now prepared. The controlled qualification batch runner now passes its offline checks and full schedule rehearsals. See [the runner record](../phase1-harness/QUALIFICATION-BATCH.md). The separate familiarity connection, actual provider checks and authorised live entry point remain open. Do not request qualification spending approval until those cases and their evidence are ready to review.

## Reproduce the offline checks

From the repository root:

```powershell
local-runs/phase1-env/Scripts/python.exe -m unittest discover -s research/development/astra-preparation -p test_prepare.py -v
```

To prepare a private selection specification, supply absolute paths outside this checkout. The output directory must not already exist:

```powershell
local-runs/phase1-env/Scripts/python.exe research/development/astra-preparation/prepare.py C:/path/outside/repository/selection.json C:/path/outside/repository/prepared
```

Private case contents are intentionally absent from this public reproduction guide. The protocol, code and eventual redacted results can be shared; sealed inputs require deliberate protected transfer if execution moves to the other machine.
