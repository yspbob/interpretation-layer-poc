# reports — map

## What it is

`reports` is the placeholder package `netbox/reports/__init__.py`: the fact graph records 1 line of code, 0 classes, 0 functions, no tests, no migrations, no data [fg:subsystems:reports] [fg:modules:reports]. The file has no content beyond that; it exists to make `netbox/reports/` a directory that is tracked in git and importable as a package [fg:modules:reports] [code:.gitignore:12-13].

The directory is the default location for operator-supplied legacy report modules: `settings.py` sets `REPORTS_ROOT` to `os.path.join(BASE_DIR, 'reports')` unless the configuration overrides it, with `BASE_DIR` being `netbox/` [code:netbox/netbox/settings.py:166-167] [code:netbox/netbox/settings.py:32].

## Module roles

None of the Django roles are present; the module is a directory marker only [fg:modules:reports].

## Dependencies and dependents

The fact graph records no import edges in either direction and no string references [fg:subsystems:reports]. All coupling is by filesystem path through the `REPORTS_ROOT` setting, as follows [code:netbox/netbox/settings.py:167].

- `core.choices.ManagedFileRootPathChoices` defines `REPORTS = 'reports'` as one of two managed-file roots, annotated as mapping to `settings.REPORTS_ROOT` [code:netbox/core/choices.py:30-36].
- `core.models.files.ManagedFile._resolve_root_path` maps the `'reports'` root to `settings.REPORTS_ROOT` when the storage backend is the local `ScriptFileSystemStorage` [code:netbox/core/models/files.py:78-86].
- Migration `extras/0109_script_model.py` reads `settings.REPORTS_ROOT` at migration time to import report files from disk, and the settings file carries a comment saying `REPORTS_ROOT` is retained for that migration [code:netbox/extras/migrations/0109_script_model.py:9-18] [code:netbox/netbox/settings.py:166-167].
- `.gitignore` excludes everything under `netbox/reports/` except `__init__.py`, so operator reports never enter version control while the package marker stays [code:.gitignore:12-13].
- Installation docs assign ownership of `/opt/netbox/netbox/reports/` to the service user, and upgrade docs copy the directory across versions [code:docs/installation/3-netbox.md:88-91] [code:docs/installation/upgrading.md:110-114].

## Relationship to `scripts`

The `reports` root is the deprecated twin of `scripts`: the `Report` class in `extras/reports.py` is now a thin subclass of `BaseScript` kept "for extras/migrations/0109_script_models.py", and the customization docs state reports are deprecated since v4.0 with functionality merged into custom scripts [code:netbox/extras/reports.py:1-13] [code:docs/customization/reports.md:1-4]. Note that `ScriptFileSystemStorage.base_location` returns `SCRIPTS_ROOT` only, so a report under `REPORTS_ROOT` is addressed through `ManagedFile.full_path`, not through the storage's base location [code:netbox/extras/storage.py:6-14] [code:netbox/core/models/files.py:74-86].

## Entry points

None are recorded [fg:modules:reports].

## Churn

3 commits by 1 author between 2017-09-19 and 2018-08-07; the file has not changed in the seven years before T0 [fg:churn:reports].
