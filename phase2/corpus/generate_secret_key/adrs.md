# generate_secret_key — retro-ADRs

## ADR-G1: Generate the key with `secrets.choice` over an explicit charset, not with Django's own utility

**Context.** Django's `SECRET_KEY` must be set by the operator before NetBox will start; settings refuses to load without it [code:netbox/netbox/settings.py:56-58] [code:netbox/netbox/settings.py:173].

**Decision.** The helper uses the standard-library `secrets` module and a hard-coded 76-character alphabet, and does not import Django (whose `get_random_secret_key` would require the Django package on the path) [code:netbox/generate_secret_key.py:3-6].

**Consequences.** The script works before NetBox's virtual environment or configuration exists, which is the point in the install sequence where the docs invoke it [code:docs/installation/3-netbox.md:171-174]. The alphabet includes shell-significant characters (`!`, `$`, `&`, `(`, `)`), which is a property of the chosen charset rather than of any validation in settings, which checks only type and length [code:netbox/generate_secret_key.py:5] [code:netbox/netbox/settings.py:206-208].

**Evidence.** The script body [code:netbox/generate_secret_key.py:1-6]; the settings check [code:netbox/netbox/settings.py:205-212]; zero import edges [fg:subsystems:generate_secret_key].

## ADR-G2: Enforce the 50-character minimum in settings and point the error at this script

**Context.** A short or non-string `SECRET_KEY` would silently weaken sessions and signing; the example configuration ships it empty [code:netbox/netbox/configuration_example.py:69].

**Decision.** `settings.py` raises `ImproperlyConfigured` if `SECRET_KEY` is not a `str` or is shorter than 50 characters, and the message embeds the absolute path of `generate_secret_key.py` built from `BASE_DIR` [code:netbox/netbox/settings.py:205-212] [code:netbox/netbox/settings.py:32].

**Consequences.** The script's location (`netbox/generate_secret_key.py`, one directory above the settings package) is load-bearing for an error message and for three documentation pages, so moving or renaming it would change user-visible text [code:netbox/netbox/settings.py:211] [code:docs/installation/3-netbox.md:174] [code:docs/development/getting-started.md:120]. The key also seeds `DEPLOYMENT_ID`, so regenerating it changes the census identity of an installation [code:netbox/netbox/settings.py:621-622].

**Evidence.** Settings validation [code:netbox/netbox/settings.py:205-212]; docs references [code:docs/configuration/required-parameters.md:186]; churn showing the file has been revised by four authors, consistent with its contract being adjusted over time [fg:churn:generate_secret_key].
