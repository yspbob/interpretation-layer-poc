# generate_secret_key — map

## What it is

`generate_secret_key` is a single-file subsystem, `netbox/generate_secret_key.py`: 7 lines of code, 0 classes, 0 functions, no tests, no migrations, no data files [fg:subsystems:generate_secret_key] [fg:modules:generate_secret_key].

The file is a standalone script: under a `python3` shebang it imports `secrets`, defines a 76-character `charset` of ASCII letters, digits and punctuation, and prints 50 characters chosen with `secrets.choice` [code:netbox/generate_secret_key.py:1-6]. There is no `__main__` guard and no function; the code runs at import time [code:netbox/generate_secret_key.py:3-6].

## Module roles

The only role is "operator helper script"; none of the Django roles (models, views, forms, tables, filtersets, API, GraphQL, signals, tests, migrations) exist here [fg:modules:generate_secret_key].

## Dependencies

The fact graph records no outbound import edges to NetBox subsystems and no inbound edges; the file imports only the standard-library `secrets` module and does not import Django or `netbox.settings` [fg:subsystems:generate_secret_key] [code:netbox/generate_secret_key.py:3].

## What depends on it

Nothing imports it. Its coupling to the rest of the codebase is by name and by contract with `SECRET_KEY` validation in settings, as follows [fg:subsystems:generate_secret_key].

- `netbox/netbox/settings.py` enforces that `SECRET_KEY` is a `str` of at least 50 characters, and the `ImproperlyConfigured` message names this script by path (`python {BASE_DIR}/generate_secret_key.py`) as the remedy [code:netbox/netbox/settings.py:205-212]. The script's output length (50) matches that minimum exactly [code:netbox/generate_secret_key.py:6].
- `configuration_example.py` ships `SECRET_KEY = ''` with a comment stating the 50-character, mixed-charset expectation the script satisfies [code:netbox/netbox/configuration_example.py:65-69].
- The installation, configuration and development docs point operators at the script [code:docs/installation/3-netbox.md:171-174] [code:docs/configuration/required-parameters.md:186] [code:docs/development/getting-started.md:120].

Downstream of the value it produces, `settings.py` derives `DEPLOYMENT_ID` by SHA-256 of `SECRET_KEY`, so the key is also the seed of the census identifier [code:netbox/netbox/settings.py:621-622].

## Entry points

The fact graph lists no entry points; the file registers nothing with Django [fg:modules:generate_secret_key]. It is run directly as a script, which is the only way its top-level `print` executes [code:netbox/generate_secret_key.py:1-6].

## Churn

5 commits by 4 authors between 2016-06-21 and 2023-02-26, the highest commit count of the four one-file subsystems despite being the shortest Python file among the executable ones [fg:churn:generate_secret_key]. The last change predates T0 by more than two years, so the file is stable [fg:churn:generate_secret_key].
