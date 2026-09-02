# Independent methodological review, round 3: plan v1.2

Subject: `poc_interpretation_layer_plan.md` RATIFIED v1.2 at `yspbob/AI-Playbook-src@c06a3c9` (3 Sep 2026). Rounds 1 and 2 reviewed v1.0 (`aa47da7`) and v1.1 (`ffcd16d`).

State at review time, checked:

- Plan: v1.2, absorbing the round-2 findings N1 to N8.
- Public artifacts repo `yspbob/interpretation-layer-poc`: still at `2ba057f` (2 Sep). No new commits, no branches.
- Fork `yspbob/netbox@poc/interpretation-layer`: still at `8afdb78`.
- Live status page: still the 1 Sep generation. No WIP banner, byline still "pre-registered experiment, all artifacts public", file lists still empty for the five merge-commit tickets.

Summary in one line: the design is now in good shape; the plan has started describing things as done that have not happened; nothing has been executed since 2 Sep.

---

## 1. Closure of round-2 findings

| # | Finding | Plan v1.2 | Executed | Residual |
|---|---|---|---|---|
| N1 | Rule set fixed before corpus | Resolved: criterion and seed pre-Phase-2, rule set derived after Gate 4, family-level hold-out | n/a until Gate 4 | See R2 (a discretionary step remains) |
| N2 | Scoring rewards inaction | Resolved: strict pass, conditional class (ii), pooled counts, both-arms-opportunity rule, count endpoint, scope report | n/a | Threats table row still carries the old wording; see R1 |
| N3 | Budget ladder | Resolved: four rungs, thresholds before dry run, outcomes unseen until rung chosen | Thresholds not yet committed | Ladder is internally coherent (keeping B supports the C vs B TOST) |
| N4 | Direction and parity | Resolved: layer-favouring side of zero; TOST with committed margin | Margin value still owed | Adequate |
| N5 | AGENTS.md operational help | Resolved: trimmed served copy, operational text in the shared prompt for all arms | Trimmed file not committed | Adequate |
| N6 | Scorer independence | Resolved: two model families or labelled prompt agreement; 20-patch human anchor | n/a | Adequate |
| N7 | Feature stratum constraints | Resolved: merged after T0, universe caveat, ladder-linked funding | Rule not written | Adequate |
| N8 | Overstatement and stale page | Half resolved: "bit-for-bit" corrected; publication ratified for now | Not executed: nothing published, page unchanged | See R1 |

Round-1 items F1 to F13: all still resolved at plan level, none executed. The round-2 execution checklist is now section 7 of the plan; every one of its ten items is open.

---

## 2. Residual findings

### R1. The plan now asserts, in the present tense, actions that have not happened

**Defect. Redo cost: none; it is either an execution or a wording fix.**

The v1.2 header says "Both review documents are published with this plan." Section 0 says "everything moves to the public repo now" and "Status page live". Phase 5 says the full pre-registration "is published to the public repo NOW, ahead of Phase 2". The threats table says "Published to the public repo now, marked WIP". At review time the public repo has no plan, no reviews, no rulings, no 32-fact sample, no WIP banner, and the page served is the 1 Sep build. A ratified plan that states as fact something a reader can falsify in one click is worse for credibility than a plan that says "owed". The same applies inside the document: the threats row "Hidden-test name coupling" still says "class-(ii) unscoreable and excluded from denominator", which section 2 of the same version explicitly reversed under N2.

Fix. Either execute checklist items 1 and 6 before the next ratification, or change every present-tense publication claim to "to be published in the next public commit; until then the page carries no public-artifacts claim". Correct the stale threats row to match the N2 text. Also fix the section 0 heading, which still reads "Execution state at v1.1". Small, but a plan that is going to be quoted should not disagree with itself.

### R2. Rule derivation after Gate 4 is still a discretionary step, and it happens after the AGENTS.md oracle comparison

**Judgment call. Redo cost: none.**

The N1 ordering fixes the main problem. What remains: "derived ... from what the verified corpus actually claims plus the fact graph" is a human (or Munin) selection step, and it now takes place after Phase 3's oracle comparison has told the builder which corpus conventions coincide with the maintainers' `AGENTS.md`. A builder who then favours those conventions as rules makes arms B and D conform by construction on Tier 2 (they hold the file), which inflates B minus A and biases the C versus B parity test towards B. The primary contrast is untouched.

Fix. Make the candidate list mechanical: every verified corpus claim tagged as a pattern claim or policy block is a candidate; admissibility (a) to (c) is applied to all candidates by script; the family-stratified split runs on whatever survives, with the committed seed. No discretionary pick. If a discretionary step must remain, run rule derivation before the oracle comparison and commit it first.

### R3. Tier 2 rule families need a minimum size or the primary endpoint can be held out of existence

**Judgment call. Redo cost: none.**

Family-level hold-out is right, but if only three or four families survive admissibility, a random split can leave Tier 2 with one family and a handful of opportunities across 25 tickets, and the MDE goes through the roof. The plan already commits an MDE with the pre-registration, so this will be visible, but the split procedure should say what happens when it is unacceptable.

Fix. Pre-register in the split procedure: Tier 2 must hold at least two families and a committed minimum number of expected opportunities (from the held-out-PR base rates, for instance 3 per ticket on average); if the seed produces a split below that, the next seed in a committed sequence is used, and the count of rejected seeds is reported. This keeps the split mechanical while preventing an empty primary endpoint.

### R4. Small items

- "Two scorers from two different model families (neither the eval agent's)": the Phase 3 verifier is from the OpenAI family. If one scorer is also OpenAI, verifier kills and scorer judgments share a family; say whether that is accepted.
- The degradation ladder drops D before B. That is coherent because B enables the C versus B TOST, but the plan calls D versus B "the named headline secondary"; a reader will notice the headline secondary is the first thing cut. Either rename it or say why the parity contrast outranks it under budget pressure.
- The extension rule (k=5 for all arms) and rung 4 (k=2) are both defined; state that the extension rule is void under any rung, not only rung 4, or that it applies only at the full design.
- Section 0 still reports "3,155 import edges"; the store has 3,155 import rows and 3,130 distinct edges. Pick one and say which.

---

## 3. What to do next, in order

Nothing in this round needs new design work. The order of operations that ends the "asserted but not done" problem:

1. Checklist items 1 and 6 first (publish, WIP banners, regenerate the page, fix the Pages deployment, footer with generator commit). This is the visible face and it is currently contradicting a ratified document.
2. Checklist items 2 to 5 (universe text and tail probe; `model_refs`; per-ticket graphs and staleness table; verbose 5a and coupling table). All mechanical; a day.
3. Checklist items 7 to 10 (strip list, trimmed AGENTS.md, shared prompt operational section, ladder thresholds, split procedure with seed and R3 minimums, success rule and TOST margin text, grader-design note).
4. Then, and only then, open Phase 2.

---

## 4. The sceptic's reading, updated

1. "The plan says its pre-registration and reviews are public now; they are not, and the dashboard has been showing the same wrong numbers and the same 'all artifacts public' line since 1 September."
2. "The rules that score the primary endpoint are still hand-picked, after the builder has seen which of the corpus's claims match the maintainers' own file."
3. "Depending on one random seed, the primary endpoint may consist of one rule family with a few dozen opportunities across the whole sample."

Sentence 1 is defused by executing checklist items 1 and 6 and by R1's wording rule. Sentence 2 by R2. Sentence 3 by R3.

---

## 5. What is good in v1.2

The corrections are precise rather than defensive: the direction of the success rule, the TOST framing for parity, the conditional class (ii), the pooled denominators and the both-arms rule are each stated in a form a statistician can execute without asking questions. The degradation ladder is the rare budget rule written before the budget bites, and the instruction that dry-run outcomes stay unseen until the rung is chosen is exactly the right discipline. The N1 reordering with family-level hold-out and a committed seed turns the primary endpoint from an object of suspicion into a defensible instrument. And the "bit-for-bit" correction shows the document is being edited for accuracy, not for effect; the remaining present-tense overclaims in R1 are the same habit in the other direction and will be just as easy to fix.

---

## Erratum (3 Sep 2026, added by the reviewer during implementation)

Rounds 2 and 3 stated that the live status page was still serving the 1 Sep generation and that the GitHub Pages deployment was stale. That was wrong. The reviewer's fetch tool was returning a cached copy; a direct browser load with a cache-busting query on 3 Sep shows the 2 Sep generation, and the repository's `pages build and deployment` run for commit `2ba057f` completed successfully at 11:33 on 2 Sep. The deployment was never behind `main`. The rest of the page findings (hard-coded state, empty file lists for merge-commit tickets, the 328k figure, the missing cards, the "all artifacts public" byline before publication) stand and are addressed in the pre-Phase-2 commit. The lesson is recorded in the generator: the footer now carries the source commit so a stale copy is recognisable at a glance.
