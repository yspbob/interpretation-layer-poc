# Ticket-selection rule — v1.0, fixed 31 Aug 2026, before execution

Parameters fixed at ratification: file cap = 20; recency window = 24 months (fixing PR merged on or after 1 Sep 2024); N = 20. The rule executes without discretion; anything requiring judgment during execution is a rule defect and forces a published amendment before proceeding.

## The rule

1. **Universe.** Closed issues in netbox-community/netbox carrying the label `type: bug`, closed as completed, whose closing reference is a single merged PR in the same repository.
2. **Test-carrying requirement.** The fixing PR's diff must (a) add or modify at least one file under a `tests/` path, and (b) modify at least one non-test Python source file. Both checked mechanically from the diff file list.
3. **Ordering.** Candidates ordered by issue closed date, newest first (recency preferred; the training-data contamination note is pre-answered in the plan: contamination is identical in both arms, the paired delta survives it).
4. **Mechanical exclusions**, applied in order, each recorded with the excluding clause:
   a. fixing PR touches more than 20 files (harness bound);
   b. fixing PR is a revert, a release-branch merge, or a dependency bump;
   c. fix touches only docs/, templates, migrations, or JS/CSS assets (conformance instruments are Python import topology; a ticket must be able to move them);
   d. issue closed as duplicate or not-planned;
   e. fixing PR merged before 1 Sep 2024.
5. **Screens, executed in order on the survivors, each result recorded per ticket:**
   a. **Fail-then-pass:** the fixing PR's tests must fail at the PR's parent commit and pass at the merge commit, both in the containerised suite (GitHub Actions on the fork, NetBox's own CI recipe). Tickets failing the screen are excluded with run logs kept.
   b. **Symptom-test audit:** graded check that the test exercises the symptom the issue text describes; mismatches excluded before T0 is set.
6. **Selection.** Walk the ordered, screened list from newest; select until N=20 qualify. If the universe exhausts below 20, the actual N is reported and recorded before proceeding — shrinking N silently is not permitted.
7. **T0.** The parent commit of the earliest-merged fixing PR among the selected tickets. The fact graph and knowledge corpus are built at T0 and never see anything later.
8. **Blindness.** The corpus-drafting stage never sees the ticket list; corpus coverage is uniform over every subsystem the fact graph identifies.

## Execution outputs (committed to this repository)

A selection log (every candidate issue ID, its fate, the clause that decided it), the selected ticket list, the per-ticket screen results, and the computed T0 — all committed before any corpus work starts.
