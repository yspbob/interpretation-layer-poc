# Research context and development records

`repositories.json` records the four upstream URLs and exact commits used for the candidate inventory. The inventory and screening records are in `website/public/evidence/` and served through the study website. They are already investigator-visible development material, not a sealed benchmark.

`development/playbook-and-original-poc-review.md` preserves the initial full-playbook assessment. Later decisions in the canonical working plan supersede its recommendations.

`development/recorded-probe-results.json` records fifteen successful checks from the earlier exploratory work. It is historical output, not a new run on the current machine. The Paperless checks execute selected upstream definitions with stubs; they do not validate the full application.

The corresponding portable script is `development/inventory_definition_probes.py`. To reproduce it, create clean upstream checkouts under `sources/httpx` and `sources/paperless-ngx`, detach each at its exact commit in `repositories.json`, and use a separate Python environment with HTTPX's dependencies. The recorded run used httpcore 1.0.9, anyio 4.13.0 and certifi 2026.2.25; this record does not constitute a complete frozen runtime. Verify the source pins before running. Invoke the script from any working directory; it writes a fresh result to ignored `local-runs/cross-repository-development-probes.json`. Preserve the original record and explicitly document differences in a reproduction.

Source checkouts, Python environments and local outputs are intentionally not transferred through Git. Constructing fully reproducible, isolated runtime images is still pilot preparation work. Never use this investigator workspace directly as a blind agent's input pack.
