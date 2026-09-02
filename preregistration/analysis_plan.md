# Analysis plan (plan v1.2, F6 / N2 / N4). Fixed before Phase 2; numerical margins marked PROPOSED pending owner ratification

## Unit, arms, replicates

- Unit of analysis: the ticket (N = 25 bug tickets; the feature stratum is analysed separately and only descriptively).
- Arms: A (stripped checkout), B (A + served AGENTS.md), C (A + layer), D (B + layer). k = 3 runs per ticket per arm at rung 0 to 3 of the ladder; runs are replicates and are pooled or averaged within ticket and arm before any test. No statistic is ever computed over runs as if they were independent.

## Endpoints and pooling

- **Primary: held-out conformance rate per opportunity.** For ticket i and arm X, `V_iX` = total Tier 2 violations over the k runs, `O_iX` = total Tier 2 opportunities over the k runs, `r_iX = V_iX / O_iX`. A ticket enters a contrast only if both compared arms have `O > 0`; the number of dropped tickets is reported per contrast.
- **Companion count endpoint:** `v_iX` = mean Tier 2 violations per run. Always defined. Reported next to the rate as the check that rate and count agree in sign.
- **Patch-scope report (per arm):** median files and lines changed per run; fraction of runs touching at least one module the reference fix touched; fraction of runs with an empty patch. Descriptive; makes conformance-by-inaction visible.
- **Secondary: strict pass.** `p_iX` = fraction of the k runs in which every test ID in `data/failpass_matrix_v2.json` for ticket i passes on the agent's patch, with the touched apps' test modules green. Class (ii) runs (import or attribute crash on a symbol the reference PR invented, with a non-empty patch that touches the module where the symbol lives and whose symptom tests could not run) are reported as a per-arm fraction and are plain fails in `p_iX`. Empty or wrong-file patches are plain fails.
- **Secondary: design deltas.** Static-analysis and topology deltas over changed code, paired, per the plan; exploratory.
- **Judged tier:** rubric scores; corroborating only.
- **Process telemetry:** Tier 1 checker firings, corrections, turns and tokens per arm; descriptive.

## Contrasts and tests

- **Primary estimand:** `Δ = mean_i (r_iC - r_iA)` over tickets with opportunities in both arms. Fewer violations are better, so a negative Δ favours the layer.
- Test: paired permutation test (sign-flip, 10,000 permutations, seed 20260903) on the per-ticket differences; Wilcoxon signed-rank reported alongside. Interval: 95% two-sided percentile bootstrap over tickets (10,000 resamples, tickets resampled with their paired structure intact, seed 20260903).
- **Success rule:** the 95% bootstrap CI for Δ lies entirely below zero. A CI entirely above zero is reported as harm. A CI containing zero is a null read against the declared MDE, never as "no effect".
- **Named secondaries, same estimator:** `D - B` (augmentation), `B - A` (context). The A x B interaction `(D - B) - (C - A)` is exploratory.
- **Parity (TOST):** for `C vs B` and `D vs B`, equivalence is claimed only if the 90% CI for the difference in rate lies within `[-m, +m]`. PROPOSED margin: `m = 0.5 x r̄_A`, half the observed mean Tier 2 violation rate in arm A, floored at 0.02 and capped at 0.10 in absolute rate. The margin is fixed as a formula now; its numeric value is computed from arm A once and recorded before any parity test is run.
- **Pass rate:** paired per-ticket proportions, same permutation and bootstrap machinery; never McNemar over runs.
- Everything not named above is exploratory and labelled so in the write-up.

## Power and MDE

`scripts/power_mde.py` (committed with this file) simulates the primary test under a beta-binomial model for per-ticket violation rates with the base rates measured on the 50 held-out PRs (`phase4/admissibility.json`) and the opportunity counts implied by them. The MDE is the smallest reduction in mean rate detected with 80% power at N = 25 and k = 3. The number is committed in `preregistration/power_statement.md` at Gate 5, before any scored run, together with the inputs used. The same script gives the MDE at k = 2 (ladder rung 4) and at k = 5 (extension).

## Extension rule (defined stopping)

If, and only if, the primary CI includes both zero and `-MDE`, every ticket is extended to k = 5 in all arms present, and the k = 5 analysis replaces the k = 3 analysis entirely. No other data-dependent collection. The rule is void at ladder rungs 2 to 4.

## Covariates and splits (exploratory, pre-declared)

- Staleness (`data/staleness.json`: months after T0, touched-module survival, touched modules absent from T0), expected to attenuate the effect.
- Training cutoff: tickets merged before vs after the pinned model's published cutoff.
- Memorisation probe flag (`data/memorisation_probe.json`, produced before scoring).
- Name coupling (`data/name_coupling.json`), for the pass endpoint only.
Each split is reported as the primary estimand within stratum with its CI; no stratum result changes the success rule.

## Reporting

One results table per contrast (Δ, CI, permutation p, Wilcoxon p, N tickets used, N dropped), the companion count endpoint, the patch-scope report, the class (ii) fractions, and the four exploratory splits, whichever way the result lands.
