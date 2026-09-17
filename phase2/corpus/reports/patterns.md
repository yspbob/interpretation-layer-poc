# reports — patterns

## Pattern: operator content directories are tracked by an empty `__init__.py` and a gitignore carve-out

`netbox/reports/` and `netbox/scripts/` both consist of a content-less `__init__.py` [fg:modules:reports] , and `.gitignore` ignores each directory's contents while re-including only that marker file [code:.gitignore:12-15].

## Pattern: the directory is addressed only through a `*_ROOT` setting derived from `BASE_DIR`

Nothing names the directory by literal path in Python; consumers go through `settings.REPORTS_ROOT`, whose default is computed from `BASE_DIR` and can be overridden in configuration [code:netbox/netbox/settings.py:167] [code:netbox/netbox/configuration_example.py:210-212]. Instances of consumers: `ManagedFile._resolve_root_path` [code:netbox/core/models/files.py:78-86] and migration 0109 [code:netbox/extras/migrations/0109_script_model.py:15-18]. The same holds for `SCRIPTS_ROOT` [code:netbox/netbox/settings.py:171].

No pattern or decision is observable in the file itself, which has no content [fg:modules:reports].
