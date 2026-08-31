# Interpretation-layer POC

A pre-registered experiment: does serving **certified architectural knowledge** (fact graph → draft → certify → serve + enforce) to a coding agent measurably improve **architectural conformance**, and possibly outcome quality, on real historical tickets — versus the same agent, same tickets, same prompt, without it?

Target codebase: [NetBox](https://github.com/netbox-community/netbox), worked on via the fork [yspbob/netbox](https://github.com/yspbob/netbox), branch `poc/interpretation-layer` (in-repo agent-instruction files stripped there so both experiment arms run identically). **No code PRs will be opened against upstream.**

This repository holds the harness implementation, the pre-registration (selection rules, prompts, endpoints, analysis plan — committed before any scored run), raw run logs, and results.

## Design in one paragraph

Two arms, identical system prompts including a prescriptive tool-usage protocol; the only difference is whether the knowledge-serving MCP layer is attached. ~20 closed bug tickets selected by a mechanical, pre-registered rule; each ticket's fixing PR must carry tests that fail before the fix and pass after (checked by execution). Agents run from pre-fix checkouts; the knowledge corpus is frozen at T0, set before the earliest selected ticket, so the layer never sees the future. Primary endpoint: conformance to certified structural rules. Pass rate and design metrics are secondary. k=3 runs per ticket per arm; paired analysis; the claim is a distribution, not an anecdote.

## Status

Phase 1 in progress: ticket selection (rule fixed, see `preregistration/`), fact-graph construction next. Scored runs have not begun.

## Scope honesty

One codebase, one language, lab conditions. Mechanism demonstration, not production evidence, not a claim about organisations, not a benchmark of any vendor's model.
