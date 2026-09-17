# manage — retro-ADRs

## ADR-M1: Keep the stock Django launcher unmodified; put all bootstrap logic in `netbox.settings`

**Context.** NetBox needs a Python-version check, an operator-supplied configuration module, and validation of required parameters before any management command runs [code:netbox/netbox/settings.py:34-60].

**Decision.** `manage.py` stays as the 11-line Django default and only names `netbox.settings`; the version check, `NETBOX_CONFIGURATION` lookup and required-parameter validation all execute at settings import time [code:netbox/manage.py:1-10] [code:netbox/netbox/settings.py:34-60].

**Consequences.** Both the CLI launcher and the WSGI launcher get identical bootstrap behaviour for free, because both just import `netbox.settings` [code:netbox/manage.py:6] [code:netbox/netbox/wsgi.py:5]. The launcher almost never changes: 2 commits in eight years [fg:churn:manage]. A misconfiguration is reported as `ImproperlyConfigured` at settings import rather than by the launcher, so every `manage.py` invocation (including `check` and `makemigrations --check` in pre-commit) fails identically when configuration is absent [code:netbox/netbox/settings.py:47-53] [code:.pre-commit-config.yaml:13-20].

**Evidence.** The file body [code:netbox/manage.py:1-10]; the settings-side checks [code:netbox/netbox/settings.py:34-60]; churn [fg:churn:manage].

## ADR-M2: Operational automation shells out to `manage.py` rather than importing Django

**Context.** Upgrades, scheduled housekeeping, background workers and CI all need to run Django operations [code:upgrade.sh:97-128] [code:contrib/netbox-rq.service:14].

**Decision.** Each of these is expressed as a process invocation of `python3 netbox/manage.py <command>`: `upgrade.sh` chains six commands [code:upgrade.sh:97-128]; systemd units run `housekeeping` and `rqworker` [code:contrib/netbox-housekeeping.service:14] [code:contrib/netbox-rq.service:14]; CI and pre-commit run `collectstatic`, `makemigrations --check`, `check` and `test` [code:.github/workflows/ci.yml:90-106] [code:.pre-commit-config.yaml:13-20].

**Consequences.** The fact graph shows zero import edges into or out of the module, so no Python-level coupling can break when the file changes, but path-level coupling is spread across shell, YAML and unit files that the graph does not track [fg:subsystems:manage] [code:upgrade.sh:97] [code:.github/workflows/ci.yml:91]. Even the user-facing error templates depend on the file's name and location as documentation [code:netbox/templates/exceptions/programming_error.html:13] [code:netbox/templates/media_failure.html:30].

**Evidence.** Empty import edges [fg:subsystems:manage]; the invocation sites listed above [code:upgrade.sh:97-128] [code:contrib/netbox-rq.service:14].
