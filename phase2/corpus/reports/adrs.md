# reports — retro-ADRs

## ADR-R1: Keep the `reports` directory and `REPORTS_ROOT` after reports were folded into scripts

**Context.** Reports are deprecated from v4.0 and their functionality merged into custom scripts, yet installations may still have report files on disk and `ScriptModule` rows whose `file_root` is `'reports'` [code:docs/customization/reports.md:1-4] [code:netbox/core/choices.py:30-36].

**Decision.** The empty package, the `REPORTS_ROOT` setting, the `'reports'` root choice and the `Report` shim class are all retained; settings and `extras/reports.py` each carry a comment that the retention is required by migration `0109_script_model` [code:netbox/netbox/settings.py:166-167] [code:netbox/extras/reports.py:9-10] [code:netbox/extras/migrations/0109_script_model.py:9-18].

**Consequences.** The directory is a compatibility surface with no code of its own: 0 classes, 0 functions, unchanged since 2018 [fg:modules:reports] [fg:churn:reports]. Removing it would break the migration's `ROOT_PATHS` lookup and the `ManagedFile` root-path mapping for existing `'reports'` rows [code:netbox/extras/migrations/0109_script_model.py:15-18] [code:netbox/core/models/files.py:78-86].

**Evidence.** The comments naming the migration dependency [code:netbox/netbox/settings.py:166] [code:netbox/extras/reports.py:9]; the deprecation notice [code:docs/customization/reports.md:3-4]; churn [fg:churn:reports].
