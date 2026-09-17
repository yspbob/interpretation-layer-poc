# Phase 2 drafter brief (identical for every subsystem; fixed before dispatch, 17 Sep 2026)

You are drafting one subsystem's part of the interpretation layer for the NetBox codebase at commit ea4c205 (2 July 2025). Work only from two inputs: the fact-graph slice for the subsystem (a digest and a full JSON file) and the read-only source tree at /home/claude/screen/t0_src. Do not use network access, do not read files anywhere else, do not run anything.

Write three Markdown files into the output directory you are given:

1. map.md — what the subsystem is and how it is put together: its modules by role (models, views, forms, tables, filtersets, API, GraphQL, signals, tests, migrations), what it depends on and what depends on it, its entry points, its coupling to other subsystems through both edge kinds (import edges and string references such as ForeignKey targets), and where change concentrates (churn). At most 1,500 words.
2. patterns.md — the established patterns and conventions you can see in the code, each stated once with at least two instances cited, and any exceptions to them. At most 1,200 words.
3. adrs.md — retro-ADRs: decisions the code implies but nobody wrote down. For each: context, the decision as the code embodies it, consequences, and the evidence. At most 1,200 words.

Citation rule, enforced mechanically after you finish: every paragraph or bullet that asserts anything must end with at least one citation, either a fact-graph row id in the form [fg:<row id>] (ids are printed in the digest and the slice: modules:<module>, symbols:<module>:<name>, imports:<src>-><dst>, model_refs:<module>:<lineno>, churn:<module>, entrypoints:<module>, subsystems:<name>) or a code location in the form [code:<path from repo root>:<line>] or [code:<path>:<start>-<end>] with the range at most 60 lines. A claim without a valid citation is deleted before anyone reads it. Cite what supports the claim, not the nearest line.

Do not propose changes. Do not describe how to run or test anything. Write for an engineer who is about to change this subsystem and needs to know what is true, what is connected to what, and why things are the way they are.
