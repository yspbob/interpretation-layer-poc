# Independent methodological review: interpretation-layer POC

Subject: `poc_interpretation_layer_plan.md`, RATIFIED v1.0 with the ticket-set amendment (N=25, 150 runs) and section 6, at `yspbob/AI-Playbook-src@aa47da7`. Executed artifacts at `yspbob/interpretation-layer-poc@2ba057f`; the fork branch `yspbob/netbox@poc/interpretation-layer`; the live page at yspbob.github.io/interpretation-layer-poc as served on 2 Sep 2026.

Reviewer's position: no part in the design, no obligation to its authors. Where a finding rests on something I could execute rather than read, I executed it. Specifically: I re-ran an equivalent of the deterministic extractor at T0 and it reproduces the committed store exactly (965 modules, 3,130 distinct import edges, identical sets); I rebuilt the same graph at each of the 25 pre-fix checkouts to measure drift; I diffed each reference PR to see what its hidden tests depend on; and I inspected upstream NetBox history at each pre-fix checkout. Numbers below come from those runs unless attributed to a document.

Conventions: **Defect** means I am confident the problem is real and material. **Judgment call** means a reasonable designer could disagree about the weight or the remedy. **Redo cost** says whether the fix touches an executed phase.

---

## 1. Findings, ranked by severity

### F1. Arm A is not bare: 20 of the 25 pre-fix checkouts ship maintainer-written agent instructions

**Defect. Redo cost: none (harness not yet built), but the status page and plan text are currently false.**

Gap. The plan and README say in-repo agent-instruction files are stripped on the fork branch so both arms run identically. But runs start from each ticket's *historical* parent commit, not from the branch, and upstream NetBox added `CLAUDE.md` on 3 Mar 2026 (#21559) and `AGENTS.md` plus `.claude/skills/` on 6 May 2026 (CAP-100, #22120). Checked per checkout: 20 of 25 tickets have `CLAUDE.md`; 17 of those also have the full `AGENTS.md` and skills. Only the five oldest (#21129, #20670, #20389, #18900, #19806) are clean.

Why it matters. `AGENTS.md` is, almost line for line, the entry rung of the playbook's own section 4: "Don't reach across app boundaries except via FK relations and public APIs", "Every UI model needs model, serializer, filterset, form, table, views, URL route, and tests", "Extras: cross-cutting features belong in the extras app", plus a repository map and per-layer conventions. It is human-certified architectural knowledge written by the maintainers. So for 80% of the sample the comparison as executable today is "maintainer rules file" versus "maintainer rules file plus a machine map from 2025", not "nothing" versus "the layer". Any agent runtime that auto-loads `CLAUDE.md` (Claude Code does) makes this worse, and an API-driven agent will `cat` it anyway because the usage protocol tells it to look for architectural guidance. The effect is heterogeneous across tickets (5 clean, 3 with a short `CLAUDE.md`, 17 with the full set), which also breaks the paired-design assumption that the only between-arm difference is the tool. The status page sentence "Files that carry instructions for AI coding tools are stripped from the copy, so neither test arm gets hidden help" is not true of anything that will actually run.

Cheapest adequate fix. Pre-register a strip list applied by the harness at every checkout, both arms, before the agent starts: `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.cursor*`, `.github/copilot-instructions.md`, `GEMINI.md`, `.windsurfrules`, and the `claude*.yml` workflows (harmless but tidy). Log the strip per run. Correct the page and README wording to "stripped at checkout by the harness". Then treat `AGENTS.md` as the gift it is: it is the maintainer-certified oracle the plan says it cannot get. Use it *after* the corpus is frozen and *outside* the served content as a validation set for Phase 3 (what fraction of the maintainers' stated conventions did the pipeline rediscover; what did it assert that they contradict). That is a far stronger certification story than cross-vendor agreement alone, at zero API cost. Optional and budget-permitting: a third arm served `AGENTS.md` alone is the most interesting comparator available (human rules file vs generated layer); if unaffordable at k=3, say so and do not run it at k=1.

### F2. The primary endpoint is at serious risk of a floor effect: import-topology rules will rarely fire on bug-fix-sized changes

**Defect in the endpoint's operationalisation; judgment call on the remedy. Redo cost: none if fixed before Phase 2.**

Gap. Conformance is the declared primary endpoint, scored as "violations of certified rules", with two or three structural rules compiled into CI (import-linter over the fact graph's topology). The fact graph is an import graph. I measured what the 25 human reference fixes do to that graph: 15 of 25 add no new non-test import edge at all; 10 add between one and four; only 5 add any cross-subsystem edge (7 edges in total), and every one of those points at the shared core (`netbox`, `core`, `utilities`), the sanctioned direction. Amendment v1.1 was introduced precisely because "the unfloored survivor distribution would let most of the sample contribute near-zero conformance signal", but a five-file floor does not change this: bug fixes in a mature layered Django app almost never create the kind of edge an import-direction rule can catch.

Why it matters. If the rules are of the import-direction kind, the likely outcome is zero violations in both arms across 150 runs: a null on the primary endpoint that says nothing, with the secondary endpoints then carrying a claim the plan explicitly says they must not carry. There is a second, opposite failure: if rules are chosen at Gate 4 *because* the bare agent breaks them at the dry run, the served arm will trivially "conform", and the headline becomes "telling an agent a rule makes it follow the rule", which no sceptic will count as evidence for section 4. The plan pre-answers circularity for the design axis but not for the primary endpoint, where it bites harder.

Cheapest adequate fix. Pre-register, before Phase 2 starts, a rule admissibility criterion that is independent of agent behaviour: (a) the rule is evidenced from the fact graph or code; (b) all 25 reference fixes conform to it (maintainer ground truth; a rule the maintainers' own merged fix violates is not their rule); (c) the rule is *at risk* in bug-fix-sized work, demonstrated by running it over a held-out set of at least 50 recent merged upstream PRs that are not in the sample and counting how many touch code where the rule applies and how many violate it. Publish those base rates. Then define conformance as a rate over opportunities (violations per rule-at-risk instance), not a raw count, and state the minimum detectable effect at N=25 under the measured base rate. To get a base rate above zero, the rule set will need pattern rules that bug fixes actually exercise, and NetBox has them in abundance: form/filterset/serializer/bulk-edit field parity (ticket #22990 is literally a parity bug), `restrict()` on querysets that reach the UI or API (#22578, #22429), `router.db_for_write` awareness in signals (#22922), ordered querysets before pagination (#18900), changelog coverage of state changes (#22644), `_()` wrapping of user-facing strings, a migration accompanying every model change. Most of these are checkable by AST or grep; the rest by rubric. Keep the import-direction rules, but do not let the primary endpoint rest on them alone.

### F3. The pre-registration is not publicly verifiable, and the page says it is

**Defect. Redo cost: none.**

Gap. The plan, which is the pre-registration document (endpoints, arms, protocol, analysis plan, threats), lives in a private repo. The public repo contains the selection rule, the selected tickets, screen outputs and the fact graph, and nothing else: no plan, no gate reports, no rulings (the page cites "R-247"), no 32-fact audit sample (the page says it is "filed"), no usage protocol text, no rubric, no verifier prompt, no analysis plan, no power calculation. The page byline says "pre-registered experiment, all artifacts public" and the intro says "Every rule, ticket and threshold is published before the results exist".

Why it matters. A pre-registration nobody outside can read at a timestamp is, to a hostile reader, indistinguishable from a plan written after the fact. The commit hash of a private repo proves nothing to anyone without access. Everything else in the design inherits its credibility from this one property, and it is currently absent.

Cheapest adequate fix. Copy the plan into the public repo now, with its amendment history preserved (the v0.8 ratification commit, the 31 Aug and 2 Sep amendments), and keep the public copy canonical from here on. Commit the Gate 1 report, the rulings referenced on the page, and the 32-fact sample with its verification commands. Before Phase 3: the verifier model ID, prompt and threshold. Before Phase 5: the verbatim system prompt for both arms, the rubric, the analysis plan and the power statement, as a single tagged commit. Optionally anchor that tag with a free external timestamp (OpenTimestamps, or an OSF registration) so the date does not rest on a git author field. Until then the page must not say "all artifacts public".

### F4. "Passed" is not solution-agnostic: hidden tests in at least 13 of 25 tickets reference identifiers the reference fix invented

**Defect in a stated property of the endpoint; the endpoint is secondary, so the damage is bounded. Redo cost: none.**

Gap. The plan describes the pass verdict as "SWE-bench-style: deterministic, solution-agnostic". Diffing each reference PR: the added tests import or call symbols that did not exist before the fix in at least 13 tickets, for example `QuerySetNotOrdered` (#18900), `JobFailed` (#19806), `M2MAddRemoveFields` (#21763), `NetBoxTaggableManagerField` (#22301), `ScriptRouter`/`ScriptViewSet` (#22745), `PinnedConnectionRouter` and new signal handler names (#22922), `ConfirmCollector`/`CountOnly` (#22812), `PortMapping` reconciliation helpers (#22644), `user_may_grant_token` (#22429), `normalize_integer_range` (#22228), `TableConfigForm`/`TableConfigBulkEditForm` (#22237), `ChoiceSetField` (#22324), `assertNotCacheable` (#22985). Two PRs also ship migrations the tests may depend on. A correct fix that names its new exception `UnorderedQuerySetError` fails at import time.

A related weakness in screen 5a: the workflow runs whole test modules and records the module exit code, so "fails before the fix" is satisfied by an `ImportError` on a symbol that does not exist yet. For those tickets the screen has not shown that the test detects the bug by execution; the symptom audit covers that gap by reading, not by running.

Why it matters. Both arms suffer equally, so the paired delta is not biased, but the pass rate is compressed towards a floor that has nothing to do with correctness, which destroys what little power N=25 had, and makes any pass-rate narrative ("the layer did not hurt correctness") hollow. The word "solution-agnostic" will be quoted back.

Cheapest adequate fix. Drop "solution-agnostic" from the plan. Pre-register a failure taxonomy applied mechanically from the test log: (i) symptom test fails, (ii) import/attribute failure on a symbol introduced by the reference PR, (iii) migration/fixture failure, (iv) infrastructure. Report strict pass alongside pass-excluding-(ii). Per ticket, record whether the issue text itself names the interface (some do; #19806 asks for a way to mark a job failed), since those tickets are legitimately testable on the name. At scoring, run the specific test IDs, not the module, and re-derive the 5a verdict per test ID from a `-v 2` log; this is a few lines of parsing on the existing workflow.

### F5. Temporal freeze is answered for leakage but not for staleness: the corpus is up to 14 months behind the checkouts it is served against

**Defect in the threats table (unlisted threat); judgment call on the remedy. Redo cost: none for the minimum fix; moderate for the strong fix.**

Gap. T0 is 27 Jun 2025 (v4.3.3); the newest checkout is 27 Aug 2026 (v4.6.9). Measured against T0: the codebase at the 2026 checkouts has 252 modules and 884 import edges the frozen map does not know about (26% and 28% growth); 6.6% of T0's top-level symbols are gone; 5 of the 25 fixes touch at least one module that does not exist at T0 (#22990, #22745, #22644, #22324, #22301). Within touched modules the served facts mostly still hold (edge survival 92 to 100%, symbol survival 96 to 100%), so the map is more incomplete than wrong. Note the cause: amendment v1.2 moved T0 from 1 Apr 2026 (the N=20 selection) back to Jun 2025 to gain five tickets, which doubled the staleness for every ticket. The plan does not mention the trade.

Why it matters. A layer that is rebuilt nightly in section 4 is being tested at a staleness no production deployment would tolerate, which biases against arm B. If B wins anyway the result is conservative; if B does not, the null is confounded with staleness and cannot be interpreted. Either way the write-up needs the number.

Cheapest adequate fix. Build the deterministic fact graph at each ticket's parent commit (no LLM, no leakage: the parent commit contains nothing from that ticket's fix; minutes each, I did it), and pre-register per-ticket staleness (served-but-stale facts, and touched modules absent from the map) as a reported covariate with the expectation that it attenuates the effect. Stronger and still cheap: serve, next to the T0 corpus, a mechanically generated "changed since drafted" note per subsystem derived from that per-ticket graph, which is exactly what section 4's nightly rebuild would provide; pre-register it as part of the treatment. The alternative, re-amending to the 20 newest MATCH tickets (T0 would become the parent of #21763, 30 Mar 2026; maximum staleness five months), costs a fact-graph rebuild (minutes, the extractor is reproducible) and a fresh 32-fact audit (hours), loses five tickets, and looks like a third data-informed change to the rule. I would not do it, but it should be a conscious choice rather than an accident of v1.2.

### F6. The statistics plan does not yet exist as a plan: unit of analysis, estimand, test and stopping rule are unspecified

**Defect. Redo cost: none; must be closed before Phase 5.**

Gap. (a) "McNemar for pass/fail" with k=3 runs per ticket per arm: McNemar on 75 run-pairs treats replicate runs of one ticket as independent, which they are not (pseudo-replication; the correlated unit is the ticket). (b) Conformance, the primary endpoint, has no estimand (violations per run? per opportunity? per ticket?), no test, no confidence-interval method and no success criterion; "conformance deltas" is not a plan, and the claim-upgrade decision in section 1 is therefore discretionary. (c) The only power statement is about the pass rate at N=20; the sentence "the continuous endpoints carry the sensitivity" is unsupported for a count endpoint whose base rate may be zero (F2). (d) "Extend to k=5 if the signal is ambiguous" is undefined optional stopping. (e) The plan still says "120 runs" in two places and "150" in another.

Cheapest adequate fix. One committed analysis plan: unit is the ticket; per ticket, compute the mean over k runs of each outcome in each arm; primary estimand is the mean paired difference (B minus A) in conformance rate per opportunity, tested by a paired permutation or Wilcoxon signed-rank test at N=25 with a bootstrap-over-tickets CI; pass rate as paired difference of per-ticket pass proportions, not McNemar on runs; state the MDE for the primary endpoint under the measured base rate. Either drop the k=5 extension or define it numerically in advance (for instance: if the 95% CI on the primary estimand includes both zero and the MDE, extend all tickets to k=5 and report the extension as the pre-registered rule) and use the k=5 analysis as the only analysis. Fix the run counts.

### F7. The ticket universe is silently truncated at GitHub's 1,000-result search cap

**Defect. Redo cost: none if handled by disclosure.**

Gap. `ticket_universe_raw.json` holds exactly 1,000 issues; the search sorts by created-desc, so the truncated tail is the oldest-created issues. The earliest closed date in the file is 18 Oct 2024 although the window opens 1 Sep 2024, and October has 8 issues against November's 19. The fetch script anticipates this ("window splitting required") but the warning output is not committed, and rule item 1 describes a universe the execution did not fetch. Since v1.2 defines the sample as *every* fully matching qualifier, the universe boundary became load-bearing at the same moment it became wrong.

Why it matters. It is small in practice (the tail is old and old PRs rarely carry tests), but it is exactly the kind of thing a reviewer finds in ten minutes and uses to ask what else was not checked.

Cheapest adequate fix. Amend rule item 1 to state the universe as executed ("the 1,000 most recently created closed type:bug issues as of 31 Aug 2026, closed on or after 1 Aug 2024") and commit the fetch log. Optionally re-fetch the tail with date splitting and report how many additional primary-tier qualifiers exist there; if any do, disclose that they were excluded by the cap rather than add them, because adding them moves T0.

### F8. Certification: the verifier can only confirm evidencedness, its accuracy is unmeasured, and it is pinned too late

**Defect in labelling and timing; judgment call on the rest. Redo cost: none.**

Gap. The cross-vendor verifier sees a claim and its cited slice, so the most it can establish is that the slice supports the claim. It cannot tell a decision from an accident, which is the whole point of a retro-ADR, and it cannot know whether a true regularity matters. That is fine if labelled, but the plan's own vocabulary ("certified", "certify") and the page's hypothesis card ("verified knowledge base") drift towards more. Second, "any disagreement kills the claim" from a single model call has unknown sensitivity and specificity; LLM judges are noisy at exactly this task. Third, the plan pins the verifier "before any scored run", but the verifier is used in Phase 3, and its kill rate shapes the corpus; a verifier could be shopped on the corpus outcome (choose the one that kills least) while still satisfying the letter of the pre-registration. The page's judge card repeats the wrong timing.

Cheapest adequate fix. Pin model, prompt and threshold before Phase 3 opens, not before Phase 5. Calibrate the verifier once with controls: 20 to 30 true fact-graph claims and the same number mutated mechanically (swap a module name, flip an import direction, change a number) and report its confusion matrix; this is a few dozen calls. Label served artifacts "evidence-verified", reserve "certified" for maintainer-merged content, and report the kill rate: if the verifier removes almost nothing, say plainly that verification was not doing work. Use `AGENTS.md` (F1) as the external validity check on the surviving corpus. And note that the pre-verification draft corpus is a free placebo of matched volume; if a third arm is ever run, that is the content to serve.

### F9. Contamination is not "identical in both arms, so the paired delta survives it"

**Defect in reasoning; the fix is cheap. Redo cost: none.**

Gap. The argument assumes contamination adds a constant to both arms. It does not. If the model has memorised the merged fix, arm A reproduces it, sits near the ceiling on pass and inherits the human fix's conformance; arm B, told to justify structure against served rules, may depart from the memorised fix. Contamination therefore compresses the delta towards zero on conformance and can push it negative on pass. A null becomes uninterpretable, and a positive result is understated, but neither is "survived". Separately, the plan does not say what text the agent receives: a GitHub issue *thread* often contains maintainer comments describing the intended fix and a link to the PR, which is a direct leak of the answer.

Cheapest adequate fix. Pre-register the input: issue title and body only (first revision if the API gives it), no comments, no linked-PR metadata, delivered as a file the harness writes. Record the pinned model's training cutoff and stratify the 25 tickets by merged-before or merged-after it as a pre-registered exploratory split (the sample spans Jul 2025 to Aug 2026, so both strata are likely populated). Add a 25-call memorisation probe: ask the eval model, without tools, to describe the fix given only the issue title and number, and score similarity to the actual diff; report it per ticket as a covariate.

### F10. The status page does not meet its own section 6 build rules, and several of its statements outrun the artifacts

**Defect. Redo cost: none.**

Gap, itemised against what section 6 requires:

- "Nothing on the page is hand-maintained" is untrue of the page as generated: the eight honesty cards, the seven phase statuses, the Gate 1 scores (`scores = {...}`), "R-247", "32-fact sample filed" and the "extraction bug fixed, on record" claim are string literals in `generate_status_page.py`, backed by nothing in the public repo (F3).
- "Files in the fixing PR" is empty for #22812, #22852, #22228 and #21763 and shows 2 of 17 files for #20670, because `extract_tickets.py` uses `git show --name-only` on merge commits with two parents. Use `git diff --name-only <merge>^ <merge>`. The header count (from `selected_tickets.md`) contradicts the list on the same card.
- "328k lines of Python" is not derivable from the map, which totals 292,610 lines under `netbox/` (155,377 code, 121,327 data, 15,906 migrations). State which count is meant and where it comes from.
- "Two of the seven stages are done" sits above a pipeline that shows stage 1 as active and awaiting Gate 2.
- The honesty cards omit the threats a cold reader most needs: training contamination (the largest known threat is absent from the page entirely), corpus staleness (F5), the builder and scorers being models from the drafting vendor, hidden-test coupling (F4), the universe cap (F7), and the fact that arm A checkouts carried maintainer instruction files (F1).
- "Tickets picked by rule, not by hand ... HOLDS": rule v1.0 was committed two minutes before execution, which is fine and git-verifiable, but v1.1 was written after seeing the survivor distribution (its own text says so) and v1.2 after seeing the audit grades. Both were blind to outcomes and both are disclosed, which is the right practice; the card should say "rule amended twice in response to what the pool looked like, before any outcome existed", and the plan should now freeze the rule against further amendment except infrastructure exclusions.
- "The judge is chosen before ... any result exists that it could be picked to favour" repeats the timing error in F8.
- The page served at review time was the 1 Sep generation while `main` held the 2 Sep rewrite; section 6 promises the page never describes a state the repo does not hold. Check the Pages deployment, and put the generator's commit hash in the footer so lag is visible.
- The footer says the full plan and rulings "live in the project record", which a cold reader cannot open (F3).

Cheapest adequate fix. Move every hand-typed fact into a committed `statuspage/state.json` (or into the gate reports) that the generator reads, so the page's own rule holds; fix the file-list bug; reconcile the LOC figure; add cards for contamination, staleness, model scorers and the strip list; reword the selection and judge cards; footer with generator commit.

### F11. The fact graph misses Django's dominant cross-app coupling mechanism

**Judgment call on severity; cheap to fix without invalidating the audit. Redo cost: low.**

Gap. The graph's dependency edges are Python imports. In Django, cross-app coupling mostly travels through string model references: at T0 there are 256 `ForeignKey/ManyToManyField/OneToOneField/GenericRelation('app.Model')` declarations, 143 of them cross-app (dcim to ipam alone: 23), plus signal connections, `apps.get_model` lookups and template references. None of these are import edges. An agent that adds `ForeignKey(to='ipam.VLAN')` in `dcim` creates exactly the kind of boundary crossing the layer exists to govern, and import-linter will not see it.

Why it matters. The map presented as "how the subsystems depend on each other" understates real coupling, the served topology is incomplete in a way that matters for the rules F2 asks for, and the design axis (b) "new cross-module edges" will miss the most common kind.

Cheapest adequate fix. Add a `model_refs` table to the extractor (a regex or AST pass over field declarations; deterministic; minutes) as a new table, leaving the existing tables and the drawn audit sample untouched; draw a small supplementary audit for the new table. Let the rules and the topology instrument consume both edge kinds.

### F12. Practical implementability of Phases 2 to 6 is under-costed, and one design ambiguity decides what "enforce" means

**Judgment call, except the ambiguity, which must be resolved before Phase 4. Redo cost: none.**

Gap. (a) The eval harness ("Python orchestrator, agent runs via the Anthropic API") is a bespoke agent runtime with file editing, shell, test execution, turn and token caps, MCP attachment, logging and a strip step (F1). That is the largest engineering item in the plan and is not in the "days each" estimate. (b) "The rest of the suite stays green" means a full NetBox suite run per scored run: roughly 150 runs of 20 to 30 minutes on CI, plus flake handling that the plan only covers at the ticket level. (c) Phase 3 cost scales with claim count, which is uncapped. (d) The plan does not say whether the CI-compiled rules are available to the agent during the run (the fork branch's CI) or applied only at scoring. If arm B can run the rule checker and iterate, "conformance" measures a linter loop; if the rules sit in the fork's CI config, arm A sees them too. (e) Five of the 25 merge commits have two parents; "parent commit" must be defined as the first parent (the workflow already does this implicitly).

Cheapest adequate fix. Use an off-the-shelf, version-pinned agent runtime with a headless mode and MCP support rather than a bespoke orchestrator; it saves weeks and is more credible ("a standard agent, not ours"). If Claude Code is used, the strip in F1 is mandatory because it auto-loads `CLAUDE.md`. Pre-register "rest of suite" as the test modules of the touched apps, with the full suite run only for runs that pass the ticket's tests. Cap claims per subsystem for verification. State that rules live outside the checkout and are applied only at scoring (or, if enforcement during the run is meant to be part of the treatment, say so and rename the endpoint). Define parent as first parent.

### F13. Ambiguities that should be findings rather than guesses

- "Three parallel model graders, one grade per ticket" (symptom audit): three graders with a majority, or each ticket graded once by one of three? State it; if majority, publish the three grades.
- The rubric's "two independent scorers": humans or models? Almost certainly models, given one person; say so, use a vendor other than the eval agent's, pin them, calibrate with seeded violations, and report kappa.
- The README calls arm A "the bare agent, zero tuning"; the plan gives it the full usage protocol. It is a primed agent without content. Use one description.
- "Same model ... identical turn and token caps": say whether B's retrieval turns count against the cap (they should, and the write-up should report budget consumed by protocol steps per arm).
- The threats table has 20 rows; the brief says 18. Trivial, but the count is quoted.
- Rule 4b's "dependency bump" exclusion is not implemented in `prescreen.ps1` (only `Revert|Release v`). Harmless here, since a dependency bump would not carry tests, but the log claims a clause it never applied.

---

## 2. Improvements that are not defects

- Store hash: `sha256(factgraph.db)` depends on SQLite version and page layout; a hash over canonicalised row dumps would let an outsider reproduce it. The extractor itself is reproducible (I matched it exactly), which is worth stating on the page.
- State the audit sample's inferential meaning: 32 facts with zero errors bounds the extractor's per-fact error rate at roughly 9% at 95% confidence (rule of three). It audits the extractor, not the map; say that.
- Blocked run order: for each ticket run A and B adjacently in random order, rather than fully randomising 150 runs, so that model drift over weeks cannot land unevenly on one arm.
- Report "retrieved" and "cited" in arm A as well: an agent told to cite ADR identifiers with no tool may invent them. Hallucinated citations in A are a finding in their own right.
- Publish the per-ticket staleness table (F5) and the per-ticket hidden-test coupling table (F4) as artifacts now; both are mechanical and both strengthen the write-up regardless of result.
- The playbook's own framing is "authority rather than model capability". The identical-prompt design isolates content provision, not certification. Unless a placebo arm runs, write the claim as "serving evidence-verified estate knowledge" and keep "certification" for the discussion.
- Record, for every scored run, the exact commit stripped, the strip log, the MCP call log, the token and turn usage, and the model snapshot ID, in one JSON per run committed to the public repo; this is cheaper to do from the start than to reconstruct.
- Add the generator's commit hash and the source commit of every artifact to the page footer.
- Section 4 of the plan says "Calendar: fits around the 1 Sep call". That date has passed; remove or update, since the ratified document will be quoted.

---

## 3. The sceptic's reading

The three-sentence dismissal a hostile expert would post about the finished study as currently designed:

1. "They compared an agent that already had NetBox's own `AGENTS.md` in its working tree against the same agent plus a year-old machine-generated map, and called the difference the interpretation layer."
2. "The primary endpoint is conformance to rules they wrote themselves and then served to one arm, on bug fixes that almost never touch those rules, so the result is either zero-versus-zero or a tautology, and the pre-registration that would tell us which lived in a private repo."
3. "Half the hidden tests fail on anything that does not reuse the maintainers' exact class names, the model had probably seen most of the fixes, and the statistics treat 75 correlated runs as 75 observations, so none of the numbers mean what the page says they mean."

Which fixes defuse each sentence:

- Sentence 1 is defused by F1 (strip at checkout, pre-registered, logged) together with F5 (staleness measured and either served as a change note or disclosed as a covariate). Using `AGENTS.md` as a validation oracle turns the strongest attack into the strongest supporting evidence.
- Sentence 2 is defused by F2 (agent-independent rule admissibility with measured base rates, conformance as a rate over opportunities, MDE stated), F3 (public pre-registration with timestamps) and F8 (verifier pinned before Phase 3, calibrated, and labelled as evidence-verification).
- Sentence 3 is defused by F4 (failure taxonomy, per-test scoring, "solution-agnostic" removed), F9 (issue body only, cutoff stratification, memorisation probe) and F6 (ticket as unit, estimand and test declared, stopping rule fixed).

---

## 4. What is already good

The temporal ordering is right and rare: tickets first, T0 after, corpus blind to the ticket list, with the whole selection walk committed in a sequence of small timestamped commits that a reviewer can replay, and I could. The extractor is honest about being an extractor: no model in the loop, provenance on every row, and it reproduces bit-for-bit from the stated commit. The fail-then-pass screen overlays the PR's tests onto the pre-fix checkout rather than trusting the PR description, which is more than most agent evaluations bother with, and the symptom audit's PARTIAL grades were written down and acted on rather than quietly carried. The amendments are dated, their motivation is stated in the text, and the decision to exclude PARTIALs was made blind to any outcome. The identical-prompt design with a tool-availability gate is the correct way to hold the instruction constant. The primary endpoint is declared and the rest are labelled exploratory, which most studies of this kind never do. And the status page, whatever its current defects, exists to be audited: its honesty cards name threats by the way they would be exploited, and the amber ones say what is still owed. That is the right instinct; the fixes above are about making the page's claims as auditable as its intent.
