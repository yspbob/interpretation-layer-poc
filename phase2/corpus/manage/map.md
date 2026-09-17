# manage — map

## What it is

`manage` is a single-file subsystem consisting of `netbox/manage.py`: 11 lines of code, no classes, no functions, no tests, no migrations, and no data files [fg:subsystems:manage] [fg:modules:manage].

The file is the standard Django command-line launcher: under a `python3` shebang it sets `DJANGO_SETTINGS_MODULE` to `netbox.settings` if the variable is not already set, imports `execute_from_command_line` from `django.core.management`, and hands it `sys.argv` [code:netbox/manage.py:1-10].

## Module roles

There is only one module and it fills only the "entry point / launcher" role; none of the usual roles (models, views, forms, tables, filtersets, API, GraphQL, signals, tests, migrations) are present [fg:modules:manage].

## Dependencies

The fact graph records no outbound import edges to other NetBox subsystems and no inbound edges from any subsystem; the import section of the slice is empty in both directions [fg:subsystems:manage]. This is because the only imports are the standard library (`os`, `sys`) and Django itself, and the Django import is deferred inside the `__main__` guard [code:netbox/manage.py:2-8].

The one real coupling is by string, not by import: the literal `"netbox.settings"` binds the launcher to the settings package at `netbox/netbox/settings.py`, which is the module that in turn imports the operator's `configuration` module and validates it [code:netbox/manage.py:6] [code:netbox/netbox/settings.py:44-53]. The fact graph's string-reference table (`model_refs`) is empty for this module because that table tracks model field targets, not settings-module names [fg:modules:manage].

## What depends on it

No Python module depends on `manage.py`; every consumer is a shell, service or CI definition that invokes it as a process, as follows [fg:subsystems:manage].

- `upgrade.sh` runs `migrate`, `trace_paths`, `collectstatic`, `remove_stale_contenttypes`, `reindex --lazy` and `clearsessions` through `python3 netbox/manage.py` [code:upgrade.sh:97-128].
- The GitHub CI workflow runs `collectstatic`, `makemigrations --check` and the test suite through it [code:.github/workflows/ci.yml:90-106]; the translation workflow runs `makemessages` through it [code:.github/workflows/update-translation-strings.yml:48].
- The pre-commit configuration runs `check` and `makemigrations --check` as local hooks through it [code:.pre-commit-config.yaml:8-22].
- The systemd units in `contrib/` run the `housekeeping` and `rqworker` commands through it [code:contrib/netbox-housekeeping.service:14] [code:contrib/netbox-rq.service:14] [code:contrib/netbox-housekeeping.sh:9].
- User-facing HTML templates tell operators to run `manage.py migrate` or `manage.py collectstatic` when the database or static files are out of date [code:netbox/templates/exceptions/programming_error.html:13] [code:netbox/templates/media_failure.html:30] [code:netbox/templates/core/inc/plugin_installation.html:21-22].

## Entry points

The fact graph lists no entry points for this module because it registers no URL routes, management commands or signal handlers [fg:modules:manage]. Operationally the file *is* an entry point: the `if __name__ == "__main__"` guard is the only executable path [code:netbox/manage.py:5-10].

## Sibling launcher

`netbox/netbox/wsgi.py` performs the same `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")` before building the WSGI application, and the production service unit points gunicorn at `netbox.wsgi` with `--pythonpath /opt/netbox/netbox`, so the two files are the CLI and HTTP halves of the same bootstrap [code:netbox/netbox/wsgi.py:1-7] [code:contrib/netbox.service:16].

## Churn

The file has 2 commits by 2 authors between 2016-03-01 and 2024-10-23, i.e. it was created at the project's origin and has been touched once since [fg:churn:manage]. Change does not concentrate here; the launcher is effectively frozen and the behaviour it launches lives in `netbox.settings` and the management commands of other apps [fg:churn:manage] [code:netbox/manage.py:6-10].
