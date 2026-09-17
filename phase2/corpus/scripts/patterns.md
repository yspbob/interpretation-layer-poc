# scripts — patterns

## Pattern: operator content directories are tracked by an empty `__init__.py` and a gitignore carve-out

`netbox/scripts/` and `netbox/reports/` each consist of a content-less `__init__.py` [fg:modules:scripts] , and `.gitignore` ignores each directory's contents while re-including only the marker [code:.gitignore:12-15].

## Pattern: the directory is reached only through `settings.SCRIPTS_ROOT`

No Python consumer hard-codes the path; each reads `settings.SCRIPTS_ROOT`, defaulted from `BASE_DIR` and overridable in configuration [code:netbox/netbox/settings.py:171] [code:netbox/netbox/configuration_example.py:217-219]. Instances: `ScriptFileSystemStorage.base_location` [code:netbox/extras/storage.py:12-14], `ManagedFile._resolve_root_path` [code:netbox/core/models/files.py:78-86], `BaseScript.load_yaml`/`load_json` [code:netbox/extras/scripts.py:575-590], migration 0129 [code:netbox/extras/migrations/0129_fix_script_paths.py:25].

## Exception: the package marker is not used for importing

Although the directory is a package, scripts are loaded via `importlib.util.spec_from_file_location` and a storage-backed loader, then placed in `sys.modules` under their bare `python_name` (no `scripts.` prefix) [code:netbox/extras/models/mixins.py:64-77]. The `__init__.py` therefore serves git tracking and directory existence, not Python import semantics [code:.gitignore:14-15] [fg:modules:scripts].

No pattern or decision is observable in the file itself, which has no content [fg:modules:scripts].
