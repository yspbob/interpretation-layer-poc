# Independent methodological review, round 2: plan v1.1

Subject: `poc_interpretation_layer_plan.md` RATIFIED v1.1 at `yspbob/AI-Playbook-src@ffcd16d` (3 Sep 2026), against the executed artifacts. Round 1 reviewed v1.0 at `aa47da7`.

What has and has not changed since round 1, checked at review time:

- The plan moved from v1.0 to v1.1 and absorbs the round-1 findings F1 to F13, most of them well.
- The public artifacts repo (`yspbob/interpretation-layer-poc`) has no commits after `2ba057f` (2 Sep). No new branches. Every artifact-level fix the plan now requires is still owed.
- The fork branch `yspbob/netbox@poc/interpretation-layer` is unchanged at `8afdb78`.
- The live status page still serves the 1 Sep generation. It does not even carry the 2 Sep copy rewrite that is on `main`, so the deployment has been stale for more than a day, and the page still says "pre-registered experiment, all artifacts public", which v1.1 section 5 now expressly forbids until publication.

So the honest one-line summary is: the design is now substantially sound on paper, nothing has yet been executed against it, and the public face of the experiment currently contradicts its own ratified plan.

Conventions as in round 1: **Defect** (confident, material), **Judgment call** (reasonable people could differ), **Redo cost** (does the fix touch an executed phase). Where I could check a v1.1 statement by execution, I did.

---

## 1. Closure of the round-1 findings

| # | Round-1 finding | Plan v1.1 | Artifacts | Residual |
|---|---|---|---|---|
| F1 | Arm A not bare (maintainer agent files in 20/25 checkouts) | Resolved: strip list, logged per run, AGENTS.md as validation oracle, 2×2 arms | Not executed (harness not built; page still claims files are stripped) | See N5 (AGENTS.md's operational help), N3 (cost of four arms) |
| F2 | Primary endpoint floor effect | Resolved in principle: agent-independent admissibility, ≥50 held-out PRs, rate per opportunity, tier split | Not executed | See N1 (timing of rule derivation), N2 (opportunity denominators) |
| F3 | Pre-registration not public | Partially resolved: publication promised "no later than the Phase 5 pre-registration commit" | Not executed; plan, review, rulings, 32-fact sample all still private | Deferral is weaker than needed; see N8 |
| F4 | Hidden-test name coupling; "solution-agnostic" | Resolved: withdrawn, per-test scoring, taxonomy | Not executed (5a re-derivation per test ID still owed) | The class-(ii) exclusion creates a new loophole; see N2 |
| F5 | Corpus staleness | Resolved: per-ticket graphs, covariate, change note, citation revalidation; T0 re-pick explicitly rejected | Not executed | Residual semantic staleness is disclosed; adequate |
| F6 | Statistics plan | Resolved: ticket as unit, estimand, test, CI, stopping rule | Power statement still owed at pre-registration | Direction and parity wording; see N4 |
| F7 | Universe truncated at 1,000 | Resolved: universe-as-executed stated, tail probe, fetch log | Not executed; `ticket_selection_rule.md` item 1 still describes the nominal universe | Do the rule-text amendment and the probe now, they are minutes of work |
| F8 | Verifier: labelling, calibration, pin timing | Resolved | Not executed | Adequate |
| F9 | Contamination reasoning; issue-thread leak | Resolved: input restriction, cutoff strata, memorisation probe | Not executed | Adequate; report stratum sizes |
| F10 | Status page hard-coded, wrong file lists, missing cards, LOC | Resolved in the build rules | Not executed at all; live page is the 1 Sep version | See N8 |
| F11 | String-reference coupling missing | Resolved: `model_refs` table as a new table | Not executed | Adequate |
| F12 | Harness practicality, enforcement ambiguity, first parent | Resolved: off-the-shelf runtime, tiers, first parent, suite-health rule | Not executed | Adequate |
| F13 | Ambiguities | Mostly resolved (arm A described as primed; caps include retrieval) | Symptom-audit "three graders, one grade" still unstated; rule 4b still unimplemented in `prescreen.ps1` | Minor |

Net: 13 of 13 addressed at plan level, 0 of 13 executed. That is expected three days in, but the closure claim must be phrased that way.

---

## 2. New findings introduced or exposed by v1.1, ranked

### N1. The rule set and its tier assignment are fixed before the corpus exists, which lets the corpus be written towards the rules

**Defect. Redo cost: none; it is an ordering change.**

Gap. Phase 4 says the three-tier rule architecture is "all fixed PRE-PHASE-2" and "assignment of admissible rules between tiers is stratified-random and committed before Phase 2". Phase 2 then says the drafting stage "never sees ... the rule set". But the builder who writes the drafting prompts, chooses the fact-graph slices to feed, and decides what a "pattern claim" looks like will know the rule set, including which rules are held out. The drafting *stage* is blind; the drafting *design* is not. With the held-out rules being the primary endpoint, the corpus can be steered, without anyone intending it, to describe exactly the conventions that will be scored. The v1.1 sentence "held-out rules are never served as rules; the corpus may describe the underlying conventions, which is the point" makes this steering look legitimate, and a sceptic will say the primary endpoint was written into the treatment.

Why it matters. Round 1's F2 asked for the admissibility *criterion* to be fixed before Phase 2. It did not ask for the rule *set* to be fixed then, and doing so is the wrong order.

Cheapest adequate fix. Fix the admissibility criterion and the tier-split procedure before Phase 2 (as now). Derive the candidate rule set only after the corpus is frozen at Gate 4, from what the verified corpus actually claims plus the fact graph, apply admissibility, then do the stratified-random tier split, with the random seed committed in advance. That way the corpus cannot have been written towards Tier 2, and Tier 2 rules are by construction conventions the served corpus describes, which is what the hypothesis needs. Additionally, stratify the split by rule *family* (parity, permissions, migrations, topology, ...) and hold out whole families, so a live Tier 1 checker cannot teach a Tier 2 rule from the same family through its error messages. Keep the wording "obedience to held-out rules came through the layer", not "through the serving channel": the checker also changes agent behaviour and both channels are the treatment.

### N2. Two new scoring rules reward doing nothing: the class-(ii) exclusion and the per-opportunity denominator

**Defect. Redo cost: none.**

Gap 1. Pass: "Class (ii) runs [import/attribute crash on a symbol the reference PR invented] are unscoreable-by-test: excluded from the pass denominator." Mechanically, an empty patch, a wrong-file patch or a crashed run all produce the same signature: the hidden test imports the invented symbol, the import fails, no symptom test runs. On the 13 coupled tickets, an arm that produces nothing usable is excluded from the denominator instead of failing, so pass rate rises with the fraction of runs that made no attempt. Both arms can exploit this differently (the layer arm, told to justify structure, may spend its budget and ship less), so the bias is not symmetric.

Gap 2. Conformance (primary): "violations divided by rule-at-risk instances in the patch". A patch with zero rule-at-risk instances has an undefined rate, and a small patch has a tiny denominator. A run that conforms by inaction, changing one line where the fix needs six files, scores perfectly. Nothing in v1.1 says how zero-opportunity runs or zero-opportunity tickets enter the primary estimand, nor how the k runs are pooled (mean of rates or pooled counts).

Cheapest adequate fix. Pass: keep strict pass as the pre-registered pass metric (symmetric, unarguable); report class (ii) as a descriptive per arm; and make "unscoreable" a conditional label rather than an exclusion: a run is class (ii) only if the patch is non-empty, touches the module where the reference symbol lives, and the symptom tests still cannot run. Optionally add a judged "addresses the symptom" score for class (ii) runs by the Tier 3 scorers, labelled judged. Conformance: pre-register (a) pooled counts per ticket and arm (sum of violations over sum of opportunities across the k runs), (b) a ticket enters the primary estimand only if both arms have at least one opportunity in that ticket, with the count of dropped tickets reported, (c) a companion count endpoint, violations per run, that is always defined, as the named check that rate and count agree in sign, and (d) a patch-scope report per arm (files and lines changed, and a mechanical "touches the modules the reference fix touched" fraction) so conformance-by-inaction is visible in the write-up.

### N3. The budget doubled and there is no pre-registered degradation ladder

**Defect in planning, given the stated constraints. Redo cost: none.**

Gap. v1.0 was 150 scored runs. v1.1 is 4 arms × 25 × k=3 = 300, up to 500 on the extension rule, plus a feature stratum of up to 8 tickets × 4 arms × 3 = 96, plus verifier calibration, scorer calibration, the memorisation probe, per-claim verification, and a live checker that adds turns to arms C and D. Each run is an agentic session on a 290k-line Django repo with test execution. The plan says "budget decisions ... are made [at Gate 5] with real numbers", which is right, but it does not say what gets cut in what order. A cut decided at Gate 5 after seeing two dry-run tickets, all arms, is a data-informed design change on the arm structure of the primary contrast.

Cheapest adequate fix. Commit the ladder now: (1) feature stratum dropped; (2) arm D dropped (the augmentation secondary becomes B vs A and C vs A only); (3) arm B dropped; (4) k=2 for all remaining arms with the extension rule void; the primary contrast C vs A at k=3 on 25 tickets is the floor below which the experiment is not run. State the per-run cost threshold that triggers each rung before the dry run, and state that the dry-run result on outcomes will not be looked at before the rung is chosen (score the dry run only after the budget decision is committed).

### N4. "Parity is a win" and "CI excludes zero" are not yet decision rules

**Defect in wording, cheap to fix. Redo cost: none.**

Gap. Section 1: "if C matches B, that is a win". At N=25 a non-significant C versus B difference is almost guaranteed whatever the truth, so "matches" needs an equivalence test with a pre-registered margin, or the sentence will be read as claiming a result the design cannot support. Analysis plan: "Success = the confidence interval excludes zero" is direction-free; a CI excluding zero on the wrong side is a harm, not a success. Also unstated: the sign convention (fewer violations is better), a one- or two-sided interval, and the bootstrap's resampling unit (tickets, with the paired structure kept).

Cheapest adequate fix. Success = the 95% two-sided bootstrap-over-tickets CI for (C minus A) in held-out violations per opportunity lies entirely below zero. For parity: pre-register a two one-sided tests (TOST) margin for C versus B, or replace "matches" with "is not detectably worse than, at the declared margin", and report the CI either way. Same for D versus B.

### N5. The pinned AGENTS.md carries operational help, not only architecture, so arms B and D get a capability the others lack

**Defect, cheap to fix. Redo cost: none.**

Gap. The pinned `AGENTS.md` (checked at `c1135de` and at upstream HEAD, identical since 7 May 2026, and it references none of the 25 issues) contains the full command table and testing section: `NETBOX_CONFIGURATION=netbox.configuration_testing`, `manage.py test --keepdb --parallel 4`, the single-module invocation, the test-module conventions per app. An agent that knows how to run NetBox's tests iterates; one that has to discover the settings module may burn its turn cap. That advantage sits in B and D only. It does not touch the primary contrast (C versus A), but it contaminates the named secondary D minus B in neither direction and inflates B minus A with something that is not "hand-written architectural guidance".

Cheapest adequate fix. Put the operational instructions (how to run the suite, the settings module, the single-module form) into the shared system prompt for all four arms, verbatim from the harness, and strip the Commands, Development Setup and Testing sections from the pinned AGENTS.md served to B and D, keeping its Architecture, Conventions and Gotchas. Commit the served version.

### N6. Scorer independence and the same-vendor judge pool

**Judgment call. Redo cost: none.**

Gap. Tier 3 uses "two independent cross-vendor model scorers ... different vendor from the eval agent", and section 5 says "verify and judge: cross-vendor frontier model over the OpenAI API". Two scorers that are the same model with two prompts, or two models from one vendor, share training and failure modes; the reported kappa will be inflated and the "two independent scorers" language will be challenged. The verifier and the scorers being the same model family also couples Phase 3 kills to Phase 5 judgments.

Cheapest adequate fix. Use two different model families for the two scorers (one OpenAI, one from a third vendor via API; both pinned), or if budget forbids, say plainly that the two scorers are two pinned prompts on one model and that kappa measures prompt agreement, not independent judgment. YP's hand-scored anchor sample then matters more; size it (for instance 20 patches, stratified by arm, blind).

### N7. The feature stratum needs its own temporal constraint and a pre-set funding rule

**Judgment call. Redo cost: none.**

Gap. Feature tickets are selected by "an analogous pre-registered rule" and "funded or dropped at Gate 5 on measured cost". Two gaps: (a) any feature ticket whose fixing PR merged *before* T0 is a future leak into the corpus (the corpus at T0 knows that feature); the stratum must be restricted to PRs merged after T0, and the rule must say so; (b) "funded on measured cost" without a threshold written before the dry run is a Gate 5 discretion. (c) Feature tickets from 2026 sit in the most stale region of the corpus; report their staleness with the rest.

Cheapest adequate fix. Write the feature-stratum rule now with "merged after T0" as item 1, the universe as executed (same 1,000-cap caveat), and the funding threshold as a number in the N3 ladder.

### N8. Two statements in v1.1 outrun the evidence, and the live page now contradicts the plan

**Defect. Redo cost: none.**

Gap 1. Phase 1 and section 5 say the extractor "was independently reproduced bit-for-bit by the external reviewer". That is more than I did. I re-implemented the module walk and import resolution and matched the committed store's module set (965) and distinct import-edge set (3,130) exactly; I did not rebuild the churn table, and I did not reproduce the SQLite file or its sha (which section 5 rightly says depends on layout). Say "module and import-edge sets reproduced exactly by an independent re-implementation".

Gap 2. Section 0 says "Status page live". The page served at review time is the 1 Sep generation, behind `main` by two commits, still with the empty file lists, the 328k figure, the eight original cards, and the byline "pre-registered experiment, all artifacts public", which v1.1 section 5 forbids until publication. The plan now has a rule the page breaks. Either GitHub Pages is not building from `main:/docs`, or a build failed; check the Pages source and the deployment log, and add the generator commit hash to the footer as section 6 now requires so lag is visible.

Gap 3. F3 was resolved by deferring publication to the Phase 5 commit. Nothing in the v1.1 plan is confidential, the review is cited as "on the project record" but is not public, and the page will keep claiming public pre-registration in the meantime. Publishing the plan and its history to the public repo now costs one commit and removes the contradiction; deferring it keeps the experiment's central credibility claim unverifiable for weeks.

---

## 3. Execution checklist owed before Phase 2 opens (from v1.1's own PRE-PHASE-2 items plus this round)

Each line is something a reviewer can verify from the public repo; none requires redoing an executed phase.

1. Publish `poc_interpretation_layer_plan.md` (v1.1 with history), the round-1 and round-2 reviews, R-247 and R-256, and the 32-fact sample with its verification commands, to the public repo (F3, N8).
2. Amend `preregistration/ticket_selection_rule.md` item 1 to the universe as executed; commit the fetch log; run and commit the date-split tail probe (F7).
3. Add `model_refs` to `build_factgraph.py` as a new table; rebuild; confirm the existing tables are byte-identical in row dumps; draw the supplementary audit (F11).
4. Build the 25 per-ticket fact graphs and commit the staleness table (F5); the numbers to expect from my run: 2026 checkouts have 252 modules and 884 edges absent from T0; 5 tickets touch a module absent from T0.
5. Re-run the 5a workflow with `-v 2` and re-derive verdicts per test ID (F4); commit the per-ticket coupling table (13 of 25 by my count; re-verify).
6. Fix `extract_tickets.py` to use `git diff --name-only <merge>^ <merge>`; move hand-typed state into `statuspage/state.json`; add the six required cards; reconcile the LOC figure; regenerate; verify the live page shows the generator commit (F10, N8).
7. Commit the strip list, the pinned and trimmed AGENTS.md for arm B (N5), the shared prompt's operational section, and the degradation ladder (N3), all before Phase 2, since Phase 2 prompts must not be written by someone who has not yet committed to them.
8. Reorder Phase 4: criterion and split procedure now; rule set and split after Gate 4 (N1). Update the "PRE-PHASE-2" labels accordingly.
9. Rewrite the success rule with direction and the parity margin (N4).
10. Symptom audit: state whether "three parallel graders, one grade per ticket" is a majority or a single grader; publish the three grades if they exist (F13).

---

## 4. The sceptic's reading, updated

The three-sentence dismissal of the study as v1.1 would run it:

1. "They fixed the rules they would score before writing the knowledge base that was supposed to discover them, so of course the served corpus described the held-out conventions."
2. "The pass rate excludes every run that produced nothing, the conformance rate is undefined for every run that did nothing, and the arm told to deliberate did less, so both headline numbers reward inaction."
3. "Three days after an outside review found the pre-registration was private and the dashboard wrong, the dashboard still says all artifacts are public and still shows the same wrong numbers."

Which fixes defuse each: sentence 1 by N1 (corpus frozen before rule derivation, family-level hold-out, committed seed); sentence 2 by N2 (strict pass kept, conditional unscoreable label, pooled counts, both-arms-at-risk rule, companion count endpoint, patch-scope report); sentence 3 by N8 and checklist items 1 and 6 (publish now, fix the deployment, footer with generator commit).

---

## 5. What is good in v1.1

The 2×2 with AGENTS.md as arm B is the right response to F1: it turns the worst confound into the most interesting comparison the study can make, and the parity framing, once given a margin, is the honest way to read it. The tier split is a real idea, not a patch: separating "the guarantee and its cost" from "the effect through knowledge" is exactly the distinction section 4 of the playbook needs and did not have. The contamination paragraph now says the true thing (compression, not cancellation). The staleness handling keeps T0 and instead serves what a nightly rebuild would serve, which tests the layer as designed rather than as frozen. The analysis plan names its unit, estimand and stopping rule, and the extension rule is the rare case of optional stopping done correctly. And the plan's own instruction that my mechanical claims be re-verified before being relied on is the right stance towards a reviewer; the numbers are reproducible from the public artifacts and the commands are in round 1, so that re-verification is an afternoon.

---

## Erratum (3 Sep 2026)

The statement that the live page "still serves the 1 Sep generation" was a fetch-cache artefact on the reviewer's side, not a deployment fault; see the erratum appended to round 3. The other N8 items stand.
