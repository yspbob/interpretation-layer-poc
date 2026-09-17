# scripts — map

## What it is

`scripts` is the placeholder package `netbox/scripts/__init__.py`: 1 line of code by the fact graph's count, 0 classes, 0 functions, no tests, no migrations, no data [fg:subsystems:scripts] [fg:modules:scripts]. It has no content; it exists so `netbox/scripts/` is tracked in git and importable as a package [fg:modules:scripts] [code:.gitignore:14-15].

The directory is the default location for operator-supplied custom scripts: `settings.py` sets `SCRIPTS_ROOT` to `os.path.join(BASE_DIR, 'scripts')` unless overridden, where `BASE_DIR` is `netbox/` [code:netbox/netbox/settings.py:171] [code:netbox/netbox/settings.py:32].

Do not confuse it with the repository-root `scripts/` directory, which holds `verify-bundles.sh` and git hooks and is invoked by CI [code:.github/workflows/ci.yml:103].

## Module roles

No Django roles are present; the module is a directory marker only [fg:modules:scripts].

## Dependencies and dependents

The fact graph records no import edges and no string references in either direction [fg:subsystems:scripts]. Coupling is by filesystem path through `settings.SCRIPTS_ROOT`, as follows [code:netbox/netbox/settings.py:171].

- `core.choices.ManagedFileRootPathChoices.SCRIPTS = 'scripts'` is one of the two managed-file roots [code:netbox/core/choices.py:30-36].
- `ManagedFile._resolve_root_path` maps the `'scripts'` root to `settings.SCRIPTS_ROOT` for local storage [code:netbox/core/models/files.py:78-86].
- `extras.storage.ScriptFileSystemStorage.base_location` returns `settings.SCRIPTS_ROOT`, making it the base of the `"scripts"` storage backend [code:netbox/extras/storage.py:6-14].
- `PythonModuleMixin.get_module` loads a `ScriptModule` by `spec_from_file_location` plus a custom loader that reads the file through that storage and `exec`s it into a fresh module registered under `python_name` in `sys.modules` [code:netbox/extras/models/mixins.py:21-77]. The package marker plays no part in this: modules are loaded from file paths, not imported as `scripts.<name>` [code:netbox/extras/models/mixins.py:64-77].
- `BaseScript.load_yaml` and `load_json` (deprecated, slated for removal in v4.4) join `settings.SCRIPTS_ROOT` with a filename [code:netbox/extras/scripts.py:565-594].
- Migrations `0109_script_model` and `0129_fix_script_paths` read `settings.SCRIPTS_ROOT` [code:netbox/extras/migrations/0109_script_model.py:15-18] [code:netbox/extras/migrations/0129_fix_script_paths.py:25].
- Installation docs assign ownership of `/opt/netbox/netbox/scripts/` to the service user; upgrade docs copy the directory between versions [code:docs/installation/3-netbox.md:88-91] [code:docs/installation/upgrading.md:110-114].

## Entry points

None are recorded [fg:modules:scripts].

## Churn

1 commit by 1 author on 2019-08-09, the file's creation; it has never been modified [fg:churn:scripts]. Change concentrates entirely in the consumers of `SCRIPTS_ROOT` (extras scripts, storage, migrations), not here [fg:churn:scripts] [code:netbox/extras/migrations/0129_fix_script_paths.py:25].
