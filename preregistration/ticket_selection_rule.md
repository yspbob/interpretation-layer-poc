# Ticket-selection rule — v1.2 (v1.0 fixed 31 Aug 2026; v1.1 pre-screen-execution; v1.2 post-audit, pre-T0: PARTIAL grades also exclude, sample = all fully-matching qualifiers, N = 25)

Parameters fixed at ratification: file cap = 20; size floor = 5 files total with a pre-registered fallback to 4 on pool exhaustion (amendment v1.1, 31 Aug 2026 — added before any screen execution); recency window = 24 months (fixing PR merged on or after 1 Sep 2024); N = 20 at v1.0-v1.1, superseded by amendment v1.2: the sample is every fully-matching qualifier (N = 25 at selection). The rule executes without discretion; anything requiring judgment during execution is a rule defect and forces a published amendment before proceeding.

## The rule

1. **Universe.** Closed issues in netbox-community/netbox carrying the label `type: bug`, closed as completed, whose closing reference is a single merged PR in the same repository.
2. **Test-carrying requirement.** The fixing PR's diff must (a) add or modify at least one file under a `tests/` path, and (b) modify at least one non-test Python source file. Both checked mechanically from the diff file list. (c) **Size floor (amendment v1.1, pre-execution):** the PR must touch at least 5 files in total, test files included; if the screens exhaust the qualifying pool below N = 20, the floor relaxes to 4 for the remainder, newest-first — a pre-registered fallback, not a discretionary choice. Grounds recorded: the unfloored survivor distribution (median 2 files, 64% single-source-file) would let most of the sample contribute near-zero conformance signal.
3. **Ordering.** Candidates ordered by issue closed date, newest first (recency preferred; the training-data contamination note is pre-answered in the plan: contamination is identical in both arms, the paired delta survives it).
4. **Mechanical exclusions**, applied in order, each recorded with the excluding clause:
   a. fixing PR touches more than 20 files (harness bound);
   b. fixing PR is a revert, a release-branch merge, or a dependency bump;
   c. fix touches only docs/, templates, migrations, or JS/CSS assets (conformance instruments are Python import topology; a ticket must be able to move them);
   d. issue closed as duplicate or not-planned;
   e. fixing PR merged before 1 Sep 2024.
5. **Screens, executed in order on the survivors, each result recorded per ticket:**
   a. **Fail-then-pass:** the fixing PR's tests must fail at the PR's parent commit and pass at the merge commit, both in the containerised suite (GitHub Actions on the fork, NetBox's own CI recipe). Tickets failing the screen are excluded with run logs kept.
   b. **Symptom-test audit:** graded check that the test exercises the symptom the issue text describes (MATCH / PARTIAL / MISMATCH); mismatches excluded before T0 is set. **Amendment v1.2 (owner, 31 Aug 2026 — made after the audit grades were produced, before T0 froze and before the pre-registration closes; grades are blind to any experiment outcome): PARTIAL grades are excluded alongside MISMATCH, and the sample is every fully-matching qualifier rather than the newest 20 — N = 25 at selection, no spares remaining. The timing of this amendment is disclosed in the write-up.**
6. **Selection.** Walk the ordered, screened list from newest; select until N=20 qualify. If the universe exhausts below 20, the actual N is reported and recorded before proceeding — shrinking N silently is not permitted.
7. **T0.** The parent commit of the earliest-merged fixing PR among the selected tickets. The fact graph and knowledge corpus are built at T0 and never see anything later.
8. **Blindness.** The corpus-drafting stage never sees the ticket list; corpus coverage is uniform over every subsystem the fact graph identifies.

## Execution outputs (committed to this repository)

A selection log (every candidate issue ID, its fate, the clause that decided it), the selected ticket list, the per-ticket screen results, and the computed T0 — all committed before any corpus work starts.
