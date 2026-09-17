# generate_secret_key — patterns

## Pattern: operator helper scripts live beside `manage.py`, under a `python3` shebang, with no Django import

Both top-level scripts in `netbox/` start with `#!/usr/bin/env python3` and import only the standard library at module top level [code:netbox/generate_secret_key.py:1-3] [code:netbox/manage.py:1-3]. Neither is imported by any NetBox module: the fact graph shows zero import edges for each [fg:subsystems:generate_secret_key] .

## Pattern: the script's contract is duplicated as a number in three places

The value 50 appears as the script's output length [code:netbox/generate_secret_key.py:6], as the minimum enforced in settings [code:netbox/netbox/settings.py:208], and as prose in the example configuration and docs [code:netbox/netbox/configuration_example.py:66] [code:docs/configuration/required-parameters.md:186]. No constant is shared; the script and the validator agree by convention only [code:netbox/generate_secret_key.py:6] [code:netbox/netbox/settings.py:208-211].

## Exception: no `__main__` guard

Unlike `manage.py`, which wraps its work in `if __name__ == "__main__":`, this script executes `print(...)` at module level, so importing it would print a key [code:netbox/generate_secret_key.py:5-6] [code:netbox/manage.py:5-10]. Nothing in the tree imports it, so the difference is latent [fg:subsystems:generate_secret_key].
