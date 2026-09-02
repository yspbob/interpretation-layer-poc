# Interpretation-layer POC

> **Work in progress.** This experiment is underway and no results exist yet. Everything in this repository can still change through the plan's gated amendment process; every change is dated in the git history. Nothing here is a result.

A pre-registered experiment: does serving **evidence-verified architectural knowledge** (fact graph → draft → verify → serve + enforce) to a coding agent measurably improve **architectural conformance**, and possibly outcome quality, on real historical tickets — versus the same agent, same tickets, same prompt, without it? Since plan v1.1 the design is a 2×2: with or without the knowledge base, with or without the maintainers' own hand-written agent guide (`AGENTS.md`).

Target codebase: [NetBox](https://github.com/netbox-community/netbox), worked on via the fork [yspbob/netbox](https://github.com/yspbob/netbox), branch `poc/interpretation-layer` (carries the screen workflows only; every run starts from a historical pre-fix commit with the harness strip list applied). **No code PRs will be opened against upstream.**

This repository holds the pre-registration (the plan with its amendment history, the selection rule, endpoints, analysis plan), the three rounds of independent methodological review that shaped it, the harness scripts, raw screen logs, the fact graph, the public status page (`docs/`), and, later, run logs and results.

## Where things are

| Path | What |
|---|---|
| `preregistration/plan/` | The plan, every ratified version, copied from the project record (`yspbob/AI-Playbook-src`) with its commit hashes |
| `preregistration/reviews/` | Independent methodological review, rounds 1 to 3 |
| `preregistration/ticket_selection_rule.md`, `selected_tickets.md` | The selection rule (frozen at v1.3) and the 25 tickets with T0 |
| `preregistration/strip_list.md`, `served/AGENTS.md`, `shared_prompt_operational.md` | What every checkout has removed, what arms B and D receive, the operational text all arms share |
| `preregistration/analysis_plan.md`, `tier_split_procedure.md`, `degradation_ladder.md` | Estimand, tests, success rule, rule admissibility and hold-out procedure, budget cuts in fixed order |
| `preregistration/gate_reports/` | Gate 1 report and rulings, the 32-fact audit sample (published as they are transferred from the project record) |
| `factgraph/` | Deterministic extractor (v2: imports plus Django string references), the store at T0, slice API, row hash, audit samples, per-ticket rebuild |
| `data/` | Ticket universe as fetched, prescreen log, screen results, symptom audit, staleness table, name-coupling table |
| `scripts/` | Fetch, prescreen, matrix, per-test screen derivation, verdict parser, power simulation |
| `statuspage/`, `docs/` | Status page generator, its state file, and the generated page |

## Status

Phase 1 built; Gate 2 hand audit awaiting the owner. Pre-Phase-2 items from plan v1.2 executed (see the status page). Scored runs have not begun.

## Scope honesty

One codebase, one language, lab conditions. Mechanism demonstration, not production evidence, not a claim about organisations, not a benchmark of any vendor's model. Every sceptic-facing table (staleness, name coupling, memorisation probe, verifier and scorer calibrations) is published whichever way the result lands.
