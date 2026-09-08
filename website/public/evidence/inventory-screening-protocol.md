# Development decision inventory protocol

This is an exploratory inventory, not a preregistration or confirmatory benchmark. The twelve previously audited NetBox cases are counted once and flagged as previously exposed. No model performance is used to select cases.

Repositories: frozen existing NetBox snapshot; newly pinned Wagtail, Paperless-ngx, HTTPX. Wagtail and Paperless extend the original shortlist; HTTPX tests transfer outside Django applications. Repository selection is purposive and all four use Python, so it cannot support language-wide generalisation.

Target: inspect roughly 60â€“100 candidate decisions. Do not invent or split cases to reach a quota. Report distinct mechanism families separately from candidate rows; variants and repetitions do not increase independent family counts.

Required candidate record: explicit project reference at pinned source, corresponding implementation anchor where available, bounded interpretation, family, evidence depth, proposed discrimination challenge, disclosure risks, disposition and reason. Find reference candidates before drafting an interpretation; inspect code for support and exceptions. Published behaviour contracts qualify as references but must not be mislabelled architectural intent or owner acceptance.

Dispositions: advance to fixture development (plausible substantive implementation evidence); control (authority-negative or conflict case); calibration only (local behaviour, parameter defaults or easy extraction); defer (reference/code/scope unresolved); reject/merge (unsupported, trivial or duplicate). These are screening decisions, not final benchmark eligibility.

Architectural relevance requires reasoning about a boundary, lifecycle, interaction, dependency or exception with a meaningful plausible alternative. Multiple files alone are not sufficient. Merely copying an API default or documented command is calibration at best. Code visibility does not establish hidden business rationale or normative authority.

Final eligibility still requires semantic disclosure review, independent gold review, validated challenge fixtures and evaluator, then untouched held-out case construction. Do not expose this inventory, labels or references to future blinded drafters. A curated candidate list is not an exhaustive catalogue of project decisions.
