# scripts — retro-ADRs

## ADR-S1: Ship an empty, git-tracked `netbox/scripts/` as the default `SCRIPTS_ROOT`, while keeping operator files out of the repository

**Context.** Custom scripts are operator-authored Python files that NetBox must find on disk, and installations are upgraded by cloning a new tree and copying the old script directory across [code:docs/installation/upgrading.md:110-114] [code:netbox/netbox/settings.py:171].

**Decision.** The directory exists in the repository with only `__init__.py`, `.gitignore` excludes everything else under it, and `SCRIPTS_ROOT` defaults to it relative to `BASE_DIR` with a configuration override [fg:modules:scripts] [code:.gitignore:14-15] [code:netbox/netbox/settings.py:171] [code:netbox/netbox/configuration_example.py:217-219].

**Consequences.** A fresh checkout always has a valid `SCRIPTS_ROOT` for `ScriptFileSystemStorage.base_location` to point at, so storage initialisation does not depend on the operator creating a directory [code:netbox/extras/storage.py:6-14]. Operator scripts cannot be accidentally committed [code:.gitignore:14-15]. The marker has needed no change since its single 2019 commit; all evolution of script handling has happened in `extras` and `core` instead [fg:churn:scripts] [code:netbox/extras/migrations/0129_fix_script_paths.py:25].

**Evidence.** Empty module row [fg:modules:scripts]; gitignore carve-out [code:.gitignore:14-15]; setting default and override [code:netbox/netbox/settings.py:171] [code:netbox/netbox/configuration_example.py:217-219]; churn [fg:churn:scripts].

## ADR-S2: Load scripts by file location through storage, not by package import

**Context.** Scripts may live outside the media root or in a non-filesystem storage backend, and `SCRIPTS_ROOT` may be relocated by configuration [code:netbox/extras/storage.py:6-11] [code:netbox/netbox/settings.py:171].

**Decision.** `PythonModuleMixin.get_module` builds a spec from the file path, reads the source through the `"scripts"` storage backend, and `exec`s it into a module keyed by bare `python_name` [code:netbox/extras/models/mixins.py:21-77].

**Consequences.** The `scripts` package marker is not on the import path of any script, so the fact graph shows no import edges touching this subsystem even though scripts are executed from its directory [fg:subsystems:scripts] [code:netbox/extras/models/mixins.py:70-77]. Two script files with the same basename in different roots would collide in `sys.modules` under the same `python_name` [code:netbox/extras/models/mixins.py:53-62] [code:netbox/extras/models/mixins.py:74].

**Evidence.** The loader [code:netbox/extras/models/mixins.py:21-35]; `get_module` [code:netbox/extras/models/mixins.py:64-77]; the empty edge sets [fg:subsystems:scripts].
