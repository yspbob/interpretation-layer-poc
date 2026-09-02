# Rule admissibility and tier-split procedure (plan v1.2, F2 / N1 / R2 / R3). Fixed before Phase 2

What is fixed now: the admissibility criterion, the candidate-generation rule, the family taxonomy, the split procedure, its seed and its minimums. What is deliberately NOT fixed now: the rule set itself. Rules are derived only after the corpus is frozen at Gate 4, so the corpus cannot be written towards the rules that score it.

## 1. Candidate generation (mechanical, no discretionary pick)

Every claim in the frozen, evidence-verified corpus that carries the tag `pattern` or `policy` (the drafting schema tags every claim; the tags are assigned by the drafting pipeline, not by hand) is a candidate rule. Nothing else is. The list is produced by a script from the corpus store and committed as `phase4/candidates.json` before any admissibility check runs. The builder does not add, remove or reword candidates; a candidate that cannot be compiled or judged is recorded as `not_compilable` and drops out at step 3, with the reason logged.

## 2. Family taxonomy (fixed now)

Each candidate is assigned one family by a keyword rule applied to its claim text and cited evidence kind, in this order; the first match wins, and the assignment script is committed with this file:

| Family | Assigned when the claim concerns |
|---|---|
| `parity` | the same field or model appearing across forms, filtersets, serializers, tables, bulk-edit or GraphQL types |
| `permissions` | `restrict()`, object permissions, tokens, ownership or visibility checks on querysets reaching the UI or API |
| `persistence` | migrations accompanying model changes, `save()`/`clean()` placement, signals, database routing (`router.db_for_write`) |
| `changelog` | `ObjectChange` records, event rules, notifications, job status handling |
| `api_surface` | ordering before pagination, serializer `url` fields, viewset method exposure, GraphQL filter shapes |
| `i18n_ui` | translation wrapping, template and table conventions |
| `topology` | module-to-module or app-to-app import direction, string-reference coupling, placement of cross-cutting features in `extras`/`core`/`utilities` |
| `other` | anything else |

## 3. Admissibility (mechanical; scripts committed with the rule set)

A candidate becomes an admissible rule only if all three hold:

- (a) **Evidenced:** its citations resolve in the T0 store (`factgraph.db`, both edge kinds) or to code lines at T0; checked by script.
- (b) **Maintainer-consistent:** all 25 reference fixes conform to it when the rule is applied to the reference patch (first parent to merge commit). A rule the maintainers' own merged fixes violate is not their rule.
- (c) **At risk in bug-fix-sized work:** applied to the 50 most recent merged upstream PRs labelled `type: bug` that are not in the sample and were merged after T0 (list committed as `phase4/heldout_prs.json` before the rules exist), the rule is *applicable* (at least one opportunity) in at least 5 of the 50 and *violated* at least once across the 50, OR applicable in at least 10 of the 50. Applicability and violation base rates per rule are committed.

Rules of kind `topology` are admitted on the same terms; they may not be the only family in Tier 2 (step 5).

## 4. Compilation

An admissible rule is `compiled` if a deterministic checker exists for it (import-linter, AST or grep over the patch) and the checker agrees with a hand check on the 25 reference fixes; otherwise it is `judged` and goes to Tier 3 regardless of the split. Only compiled rules enter the Tier 1 / Tier 2 split.

## 5. Split (family-stratified, seeded, with minimums; R3)

- Seed: `20260903` (the ratification date of plan v1.2), committed here before Phase 2. Seed sequence for retries: `20260903, 20260904, 20260905, ...`.
- Procedure: shuffle the list of families present among compiled rules with `random.Random(seed)`; assign families alternately to Tier 2 and Tier 1 starting with Tier 2, so that whole families are held out and Tier 2 gets the larger half when the count is odd.
- Minimums, checked after each split: Tier 2 holds at least two families and at least one family other than `topology`; the expected number of Tier 2 opportunities per ticket, estimated as the sum over Tier 2 rules of (applicability rate on the 50 held-out PRs x mean opportunities per applicable PR), is at least 3.0; Tier 1 holds at least one compiled rule (the live checker must have something to check).
- If a split fails a minimum, the next seed in the sequence is used; the number of rejected seeds and the reason for each rejection are reported in `phase4/tier_split.md`.

## 6. Timing and blindness

- Steps 1 to 5 run after Gate 4 (corpus frozen) and before Gate 5 (dry run). The Phase 3 `AGENTS.md` oracle comparison is run after step 5 has been committed, so that oracle knowledge cannot influence which conventions become rules (R2).
- The drafting pipeline (Phase 2) never sees this file's taxonomy in its prompts; the tags it assigns (`pattern`, `policy`, `fact`, `decision`) are part of the drafting schema and are needed for citation checking regardless of this procedure.
- The held-out rules are never shown to any arm as rules; the corpus that arms C and D receive may describe the underlying conventions, which is the hypothesis.

## 7. Outputs committed at Gate 5

`phase4/candidates.json`, `phase4/heldout_prs.json`, `phase4/admissibility.json` (per candidate: a, b, c results and base rates), `phase4/tier_split.md` (families, seed used, rejected seeds, Tier 1 and Tier 2 rule IDs, expected opportunities), and the checker sources for Tier 1 and Tier 2.
