# Budget degradation ladder (plan v1.2, N3). Rungs RATIFIED in the plan; thresholds PROPOSED, pending owner ratification

The full design is 4 arms x 25 tickets x k=3 = 300 scored runs, plus the feature stratum (up to 8 tickets x 4 arms x 3 = 96 runs), plus verification, calibration and probe calls. If the per-run cost measured at the Gate 5 dry run makes that unaffordable, cuts happen in the order below and no other. The rung is chosen on cost alone: the dry run's outcome files are not opened until the rung is committed (the harness writes outcomes to a directory the scoring script only reads after `preregistration/ladder_decision.md` exists).

## Rungs (from the plan, section 2, fixed)

| Rung | Design | Scored runs |
|---|---|---|
| 0 | Full: A, B, C, D at k=3 on 25 bug tickets, plus the feature stratum | 300 + up to 96 |
| 1 | Feature stratum dropped | 300 |
| 2 | Arm D dropped (augmentation secondary reduces to B vs A and C vs A; the C vs B parity test stays) | 225 |
| 3 | Arm B dropped | 150 |
| 4 | k=2 for all remaining arms; the k=5 extension rule is void | 100 |
| stop | Below rung 4 the experiment is not run | - |

The k=5 extension rule applies only at rung 0 or rung 1 (all four arms present at k=3); at rungs 2 and 3 it is void as well, because extending only some arms would unbalance the blocked design.

## Thresholds (PROPOSED)

Let `c` be the mean cost per scored run measured at the dry run (all arms, both tickets, including the checker and MCP calls, at the pinned model and caps), and `C` the scored-run budget cap the owner sets. The proposal below reserves 20% of `C` for the k=5 extension at rung 0 or 1 and is otherwise a straight division:

| Rung | Chosen when |
|---|---|
| 0 | `c x 396 <= 0.8 C` |
| 1 | `c x 300 <= 0.8 C` |
| 2 | `c x 225 <= C` |
| 3 | `c x 150 <= C` |
| 4 | `c x 100 <= C` |
| stop | otherwise |

Proposed default cap: `C = USD 600` for scored runs, separate from the Phase 3 verification cap (set at Gate 4) and from calibration and probe calls (budgeted at USD 60). At that cap the full design needs `c <= 1.21`, rung 1 `c <= 1.60`, rung 2 `c <= 2.67`, rung 3 `c <= 4.00`, rung 4 `c <= 6.00` per run. The owner replaces `C` with the real figure before the dry run; the rung formulas do not change.

## Recording

`preregistration/ladder_decision.md` is committed at Gate 5 with: measured `c` per arm and overall, `C`, the rung chosen, and the date. It is committed before any dry-run outcome is read, and the commit hash of that file is cited in the write-up.
