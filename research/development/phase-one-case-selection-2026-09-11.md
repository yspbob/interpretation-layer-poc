# Starting Phase 1 case selection

11 September 2026. Selection is in progress; this is not a frozen trial allocation.

## Working choice

Use HTTPX H06, the authentication flow family, to develop the first guidance assessment case. It covers shared logic, mode dependent operations, body handling and valid alternatives. It is sufficiently bounded to inspect and probe without a running database or web application. That makes it useful for developing the assessment procedure before selecting the full trial set.

This is a working choice for development, not a claim that HTTPX is the best final repository. No model results were used to choose it. The final repository, additional families, source conditions and qualification allocation remain open.

## Comparison with the existing candidates

The comparison below uses the recorded inventory and its documented limitations. Only the selected H06 source was newly inspected in this piece of work; the other repositories were not reaudited.

| Candidate | Reason to consider it | Reason for the current choice |
|---|---|---|
| HTTPX H06: authentication flow | A meaningful distinction between reusable logic, framework behaviour and custom I/O, with supported exceptions. | Selected for the first development case. Its mechanics can be checked locally and its documentation and code can be reconciled directly. |
| NetBox N14: permission checks after a write | Strong interaction between the saved state, permissions and transaction rollback. | Remains promising. Validating the full write path requires more framework and database preparation. That does not make it a weaker research question. |
| Wagtail W03: chooser visibility and content access | A useful distinction between hiding an item in a selection interface and protecting its contents. | Remains promising. Its serving configuration and permission paths require a broader case definition. |
| Paperless P05: ordered workflow mutations | Later assignments, merged collections and removal exceptions make a substantive composition question. | Remains promising. Earlier probes used definitions with stubs; the full workflow requires additional validation. |

Existing H04 work helps with HTTPX familiarity and mechanics, but did not determine this choice. H06 addresses a different decision family. HTTPX remains a public Python library with possible prior model familiarity; a successful result here would not establish effectiveness across application frameworks, languages or organisations.

## What the inspection changed

H06 is suitable for developing an assessment of available guidance. It cannot be described as a clean undocumented rule reconstruction case: the authentication guide and source docstrings disclose important parts of the rule. The specification therefore declares documentation visible inputs and records provenance for each decision.

The code also exposes a consequential exception: body reading flags are honoured by the base adapters. A complete custom override bypasses those reads. Fifteen local checks support selected dispatch and body handling observations. They do not measure model judgement or validate the complete runtime. See the [case and results](h06-guidance-assessment/README.md).

## Selection status and remaining gates

Initial inventory screening stays complete. Case selection is now in progress, with one concrete public development case. H06 must stay out of untouched qualification or confirmation if it informs prompts or scoring. Historical inventory counts are preserved; this new exposure is recorded here and in the case, rather than rewriting what was known on 5 September.

Before selecting the final trial, examine whether the remaining HTTPX families offer enough distinct, substantive decisions for the intended claim. Retain an alternative repository if they mainly reduce to restating documented API facts. Complete the reference and input reviews, model familiarity checks and qualification design under the working plan. Familiarity probes remain subject to the existing runtime and model call gates.

There are no reserved Phase 2 tasks or reusable experimental guides yet. Select their compatible tasks and source versions before the preparation used in that comparison. The H06 development example does not authorise a later historical coding trial or paid model calls.
