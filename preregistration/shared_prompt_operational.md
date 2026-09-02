# Shared system prompt: operational section (plan v1.2, N5). Status: PROPOSED text, pending owner ratification

This section is identical in all four arms and is the only place operational help appears. It is the content that upstream's `AGENTS.md` carried in its Commands, Development Setup and Testing sections, restated so that no arm gains a capability from a served file. The full shared prompt (task framing, usage protocol, output format) is committed separately before Phase 5; this file fixes the operational part now because the served `AGENTS.md` for arms B and D was trimmed on the strength of it.

---

## Working in this repository

- The Django project root is `netbox/`. Run every `manage.py` command from that directory, not from the repository root.
- Tests use Django's test runner (`django.test.TestCase`), not pytest. Before running any test, set the environment variable `NETBOX_CONFIGURATION=netbox.configuration_testing`. A PostgreSQL database and a Redis instance are available to the test configuration in this environment; you do not need to start or configure them.
- Run a single test module with `python manage.py test <app>.tests.<module>` and a single test with `python manage.py test <app>.tests.<module>.<TestCase>.<test_method>`. `--keepdb` reuses the test database between runs and saves several minutes. The full suite takes a long time; prefer the modules that cover the code you change.
- Test modules mirror the app layout under `<app>/tests/`: `test_api.py`, `test_filtersets.py`, `test_models.py`, `test_views.py`, `test_forms.py`, `test_tables.py`.
- Generate migrations with `python manage.py makemigrations` after changing a model; never hand-write a migration.
- Lint with `ruff check` from the repository root (configuration in `pyproject.toml`: line length 120, single quotes). Do not run `ruff format` on existing files.
- `netbox/netbox/configuration.py` is git-ignored; do not create or commit it.

---

Notes for the record: the wording above paraphrases upstream `AGENTS.md` (commit `c1135de8f`) sections "Commands", "Development Setup" and "Testing"; it adds nothing upstream does not say, and it omits the `mkdocs`, `nbshell`, `collectstatic` and release commands, which no ticket needs. If the owner prefers the upstream wording verbatim, substitute it; the requirement is only that all four arms receive the same text.
