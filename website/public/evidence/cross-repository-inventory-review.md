# Interpretation-layer validation: broader decision inventory

5 September 2026 · Exploratory source-based screening · No blinded model trial

## Verdict

**There is enough material to develop a serious cross-repository pilot. The inventory is not yet a sufficiently qualified confirmatory benchmark.** Keep NetBox and add Wagtail, Paperless-ngx, and HTTPX. NetBox does not need to carry the entire study, and there is no evidence here that starting again with a single replacement repository would improve it.

The screen now contains **84 candidate records**: the original twelve NetBox cases, 68 additional substantive/control/calibration candidates, and four explicitly rejected examples. Of these, **52 advance to fixture development**, covering **39 named mechanism families**. Fifteen are uncertainty, authority, or conflict controls; six are deferred; four are calibration only; three are merged into other cases; four are rejected.

“Advance” means a plausible explicit reference and implementation-grounded challenge were found. It does not mean the code-only rule has already been recovered by an agent, the evaluator is validated, the information is adequately withheld, or a fixture passes. Family labels prevent obvious duplicate counting; they do not establish statistical independence.

Six of the advancing cases were in the original development audit. Excluding those leaves **46 newly inventoried advancing candidates across 33 named families**. That is the more relevant stock for planning fresh work. It is not 84 independent positive demonstrations and should not be presented that way.

| Repository | Advance | Families within advance | Controls | Deferred | Calibration | Merged/rejected |
|---|---:|---:|---:|---:|---:|---:|
| netbox | 13 | 11 | 6 | 0 | 1 | 1 |
| wagtail | 13 | 10 | 3 | 3 | 0 | 2 |
| paperless-ngx | 15 | 11 | 2 | 2 | 0 | 2 |
| httpx | 11 | 7 | 4 | 1 | 3 | 2 |

## Why these repositories

**NetBox — retain for continuity and infrastructure conventions.** The additional material includes transactional permission checks on the resulting saved state, permission-constraint composition, scheduling under an advisory lock, worker subscriptions, and startup registration. These are more relevant to the interpretation-layer claim than formatting or simple API defaults. Existing extraction work remains useful, but method bodies and deployment configuration must be inspectable. [N14: docs/administration/permissions.md:113](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/administration/permissions.md#L113), [N16: docs/plugins/development/background-jobs.md:43](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/background-jobs.md#L43), [N17: docs/plugins/development/background-jobs.md:127](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/background-jobs.md#L127)

**Wagtail — add for lifecycle, representations, and scoped permissions.** Its strongest candidates concern page-tree grants, choosing assets versus reading their contents, document serving routes, revision/workflow composition, translation identity, rich-text expansion, block validation, and image renditions. These provide plausible alternative implementations and important exceptions. Wagtail also exposes a practical problem: several apparently local search APIs now re-export implementation from `modelsearch`; revision relation handling depends on `django-modelcluster`. Those cases are deferred rather than credited from import stubs. [W03: docs/topics/permissions.md:52](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L52), [W08: docs/topics/snippets/features.md:296](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/snippets/features.md#L296), [W13: docs/advanced_topics/streamfield_validation.md:36](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/streamfield_validation.md#L36), [W14: wagtail/search/signal_handlers.py:1](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/search/signal_handlers.py#L1)

**Paperless-ngx — add for processing stages, ownership, and extension boundaries.** The watcher/worker split, pre/post hooks, ordered workflow mutations, global versus object permissions, classifier training selection, parser competition, and selective remote processing offer substantial material. Its OCR, database, task queue, and filesystem requirements will make some runnable fixtures heavier than the HTTPX cases. Its current versioning behavior also requires care when using older-sounding documentation as gold. [P01: docs/usage.md:1164](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L1164), [P05: docs/usage.md:485](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L485), [P15: docs/development.md:408](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L408), [P17: docs/development.md:474](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L474)

**HTTPX — add as a contrasting library and inexpensive local test surface.** Its resource ownership, request preparation, streaming, hooks, authentication flows, routing, and transport boundaries extend the scope beyond Django applications. Local transports allow useful behavior checks without live network services. Some candidates are still straightforward API facts, and the real connection/retry implementation is in `httpcore`; forwarding a parameter is not evidence that its complete semantics were inspected. [H04: docs/async.md:87](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/async.md#L87), [H06: docs/advanced/authentication.md:125](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/authentication.md#L125), [H09: docs/advanced/transports.md:17](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/transports.md#L17)

All four repositories are Python; three are Django-based. This is a deliberate initial comparison, not evidence of generalisation across languages, organisations, proprietary systems, or architectural styles. Existing public decision records remain historical references, not owner approval of the layer's proposed policies.

## Concrete findings from checking references against implementation

**HTTPX's cookie guidance overstates enforcement.** The compatibility guide says per-request client cookies are unsupported. The pinned implementation accepts them and emits a deprecation warning. A local mock-transport probe confirmed that the cookie reaches the request. Correct interpretation distinguishes a recommendation/deprecation from a runtime ban. [H11: docs/compatibility.md:114](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L114), [H11: httpx/_client.py:806](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L806)

**HTTPX's encoding guidance conflicts internally.** Its compatibility guide describes automatic charset detection, while the dedicated text-encoding guide and implementation use UTF-8 as the default no-charset fallback. Probes confirmed both UTF-8 fallback and an explicitly configured detection callable. This is a conflict case, not a single-document answer key. [H12: docs/compatibility.md:101](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L101), [H12: httpx/_models.py:167](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py#L167)

**Paperless's PDF-editing wording is incomplete for the inspected path.** The guide describes altering the original file. Rotation and page deletion in the pinned code instead write a temporary PDF and enqueue it with a `root_document_id` to create a version. The candidate is now a conflict control. The audit does not assert full original-byte retention: that requires tracing and exercising the subsequent version pipeline. [P14: docs/usage.md:806](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L806), [P14: src/documents/bulk_edit.py:446](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/bulk_edit.py#L446), [P14: src/documents/bulk_edit.py:814](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/bulk_edit.py#L814)

**Paperless has a meaningful archive exception.** A mandatory display rendition is retained even when archive generation is set to never. Probes of the upstream decision function confirmed the distinction between mandatory and optional output. Parser selection probes also confirmed tie precedence, declining with a None score, and excluding a declared remote parser when remote processing is disabled. The metadata gate does not itself prevent an undeclared plugin from making a remote call. [P13: docs/configuration.md:964](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/configuration.md#L964), [P16: docs/development.md:442](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L442), [P17: docs/development.md:474](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L474)

**NetBox's background-event rule needs a narrower scope.** The inspected implementation queues webhook delivery and script execution, but does not move every event-rule operation into a worker. Notification creation occurs in another branch. A blanket “all event handling is asynchronous” interpretation would be an overclaim. Its worker class also contains an overly broad comment about all configured queues; actual default subscriptions are high, default, and low. Narrative inside code needs provenance and verification too. [N15: netbox/extras/events.py:156](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/events.py#L156), [N17: netbox/core/management/commands/rqworker.py:8](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/core/management/commands/rqworker.py#L8)

These findings reinforce the experiment's substantive question: can the layer construct useful interpretations while preserving boundaries, exceptions, disagreement, and uncertainty? Exact reproduction of a document is insufficient.

## What was actually done

The repositories were pinned as follows. NetBox retains the original historical snapshot; the three new repositories use the fetched default-branch snapshots, not necessarily released versions. Their dates are intentionally reported because this inventory is not yet a date-matched historical task experiment.

| Repository | Pinned source | Commit timestamp |
|---|---|---|
| netbox | [ea4c205a37ba](https://github.com/netbox-community/netbox/tree/ea4c205a37baa3e58e6e481158c15c6154cceeff) | 2025-07-02T13:59:56-04:00 |
| wagtail | [bddc5eaf2e77](https://github.com/wagtail/wagtail/tree/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417) | 2026-09-01T13:01:56+01:00 |
| paperless-ngx | [835c4e51d0b1](https://github.com/paperless-ngx/paperless-ngx/tree/835c4e51d0b145007bfac934009713dd8bbf3598) | 2026-09-05T02:09:31-07:00 |
| httpx | [b5addb64f016](https://github.com/encode/httpx/tree/b5addb64f0161ff6bfe94c124ef76f6a1fba5254) | 2026-02-23T10:40:42Z |

The screen enumerated documentation paths and reviewed selected relevant guide sections and implementation paths. Every recorded primary reference and implementation anchor resolves locally at its pinned commit; referenced files have SHA-256 records. The original twelve retain their earlier audit evidence and are flagged as such. Navigation anchors on those earlier code files are not substitutes for their decision-specific prior evidence.

Fifteen new development probes passed: nine HTTPX checks using the pinned package with local mock transports or an in-process ASGI app, and six Paperless checks using actual upstream definitions with small stubs. These checked specific discrepancies and challenge outcomes. They were not full NetBox/Wagtail/Paperless application tests, blinded agent runs, a comparison of experimental arms, or container/network-isolation verification. The probes did not issue outbound HTTP requests.

All four source checkouts remained free of tracked modifications. Outputs include an editable CSV inventory, detailed case cards, machine-readable references/source hashes, and probe results.

## What the counts do and do not establish

The earlier 40–60 figure was a provisional planning range for eligible decisions, not a statistical calculation. Although 52 advancing rows fall inside it, pruning reveals only 39 named families, including original development material. Further disclosure and fixture review will remove or merge more cases. **Do not declare the sample sufficient from the row count.**

The final size depends on the primary comparison, the smallest worthwhile improvement, case difficulty, variation, and dependence between challenges. Use a pilot to estimate variation and floor/ceiling behavior, then calculate or simulate power for the chosen paired, grouped analysis. Do not size the study from an optimistic observed pilot effect. Repeated runs measure model variability; code variants and related challenges remain grouped under their parent decisions. Four repositories also provide very little basis for estimating variability across repositories.

Keep inference accuracy, unsupported-authority claims, conflict handling, and downstream coding effects as separate outcomes. Controls and simple calibration facts should not be blended into a single success percentage that makes weak architectural recovery look strong. Report case families and per-repository effects, as well as all attempts and failures.

## Rejections, dependencies, and withholding

The exclusions are explicit. Lockable ordering is merged into workflow composition; parser identity into parser discovery; no-proxy exclusions into mount precedence. Trailing-newline rules, indentation, shortcut help, and status-code naming preferences are rejected from the substantive set. The rejection list is a bounded log of inspected examples, not an exhaustive account of every irrelevant sentence in the repositories.

Deferred cases are W06 (clustered revision relations), W14/W15 (`modelsearch`), P12 (soft-delete/restore semantics), P19 (insufficiently traced audit-actor integration), and H09 (transport retries). Their missing evidence is documented. Core framework dependencies also need pinned versions when fixtures run; the list above highlights the cases where the missing dependency contains the central mechanism.

Each record includes lexical disclosure triage and a case-specific challenge. **No new repository has passed semantic withholding review.** Source-name matches are leads, not leak counts. Docstrings, comments, executable error messages, examples, tests, release notes, generated files, and dependency source can disclose answers. Gold documents, inventory titles, challenge descriptions, and these audit outputs must be outside drafter inputs. The earlier NetBox stripped-input manifest covers only that earlier prototype, not these new repositories.

An investigator necessarily sees reference answers while constructing gold. The critical separation is between that work and the experimental agents. Do not run a blind drafter in this conversation. The original twelve remain development cases. Newly inventoried cases may be allocated prospectively only under a frozen protocol, with fresh isolated agent contexts and no performance-based selection; they should not be described as an already sealed or independently constructed holdout. If they are used to tune prompts or scoring against model outputs, move them to development and replace them in confirmation.

## Recommended next gate

Proceed to a **sealed pilot**, not the original large paid trial. Select a small spread of families from all four repositories, using explicit eligibility criteria before outcomes are visible. Include a recoverable convention, a valid exception, a conflict, and missing-authority cases. Resolve any central dependency evidence for selected cases; implement meaningful application challenges; independently check the gold and scoring; then freeze allowed inputs, prompts, resource budgets, and analysis.

Give the layer and a strong direct-analysis baseline the same permitted evidence, account for construction and verification costs, and freeze interpretations before downstream challenges. Add a diagnostic supplied-rule condition to check whether the task can benefit from guidance at all. Build unpublished semantic variants and meaning-preserving renamings as separate controls, rather than treating public-source success as proof that training knowledge was absent.

Run every arm/repetition in a fresh isolated environment with the narrow logged model gateway previously discussed, and keep grading outside. Publish complete replayable artifacts only when authorised. This inventory did not build that harness or initiate paid model runs.

**The material-supply gate passes for a pilot. Benchmark readiness, statistical sufficiency, isolation integrity, and interpretation-layer effectiveness remain separate gates.**
