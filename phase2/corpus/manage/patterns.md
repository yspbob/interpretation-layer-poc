# manage — patterns

## Pattern: settings module is defaulted, never forced

Both process launchers set `DJANGO_SETTINGS_MODULE` with `os.environ.setdefault(...)` rather than assignment, so an operator's pre-set value wins. Instances: the CLI launcher [code:netbox/manage.py:6] and the WSGI launcher [code:netbox/netbox/wsgi.py:5]. These are the only two places in the tree that name the variable [code:netbox/manage.py:6] [code:netbox/netbox/wsgi.py:5].

## Pattern: indirection to the operator's configuration is two-level

The launcher names only `netbox.settings`; the settings module then locates the operator's configuration through a second environment variable, `NETBOX_CONFIGURATION`, defaulting to `netbox.configuration` [code:netbox/manage.py:6] [code:netbox/netbox/settings.py:44-46]. The same two-level path is what the WSGI launcher follows [code:netbox/netbox/wsgi.py:5].

## Pattern: Django import is deferred under the `__main__` guard

The `django.core.management` import sits inside `if __name__ == "__main__":`, after the settings variable is set, so importing the file does not import Django [code:netbox/manage.py:5-8]. This differs from the WSGI launcher, which imports Django at module top level before setting the variable; it is the one observable divergence between the two launchers [code:netbox/netbox/wsgi.py:1-5] [code:netbox/manage.py:5-8].

## Pattern: invoked by path, always as `netbox/manage.py`

Every consumer runs the file by its path relative to the repository root, never by installing a console script. Instances: `upgrade.sh` [code:upgrade.sh:97-103], CI [code:.github/workflows/ci.yml:91-94], pre-commit [code:.pre-commit-config.yaml:13-20], and the systemd units, which use the absolute install path `/opt/netbox/netbox/manage.py` [code:contrib/netbox-housekeeping.service:14] [code:contrib/netbox-rq.service:14].

## Exception: no NetBox-specific code

The file contains nothing beyond the Django default launcher shape (no `sys.path` manipulation, no version check, no local imports); it has 0 classes and 0 functions [fg:modules:manage] [code:netbox/manage.py:1-10]. The Python-version check and configuration validation that a reader might expect here live in `netbox/netbox/settings.py` instead [code:netbox/netbox/settings.py:34-38] [code:netbox/netbox/settings.py:56-60].
