# First guidance assessment case: authentication in HTTPX

11 September 2026. Case H06, authentication flow family.

**Status:** A public development case for Phase 1. The source has been inspected and 15 local behaviour checks matched their expected results. No model drafted guidance or assessed an answer. This case does not qualify an assessor, prove inference from undocumented code or establish a benefit from using the layer.

HTTPX is the working choice for developing this first case. The final trial repository and set of cases remain open until the selection and access checks are complete. The [selection record](../phase-one-case-selection-2026-09-11.md) explains this choice and its limits.

## The question this case makes concrete

HTTPX lets developers add authentication to both synchronous and asynchronous clients. Much of the authentication logic can be shared. Some operations, such as reading a file or waiting for a lock, need an implementation appropriate to the client's mode.

A useful guide should explain that boundary without turning it into a blanket ban on authentication doing I/O. It should also explain which work the framework performs and when a custom implementation takes responsibility for it.

The independent assessment will examine whether an answer captures those distinctions, supports its claims and avoids inventing restrictions. It will not judge how closely the wording matches this document.

## Sources and their role

Use HTTPX commit `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`, the version already recorded in the candidate inventory. The source hashes are in [source-manifest.json](source-manifest.json). No `AGENTS.md` file was found anywhere in the complete archive at this commit. That observation does not remove the need to inspect the instructions in any later version.

| Source | What it contributes |
|---|---|
| [Authentication guide](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/authentication.md#L125) | Published usage guidance, body requirements and alternatives for specialised or unsupported modes. |
| [Auth base class](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_auth.py#L22) | The common generator and the two adapters; shows exactly where body reads happen. Its docstrings also disclose guidance. |
| [Client dispatch](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L937) and [async dispatch](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1652) | Each client invokes the appropriate adapter. |
| [Request body access](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py#L462) | Reading content requires it to have been loaded; synchronous and asynchronous reads follow different paths. |
| [Upstream authentication examples in tests](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/tests/client/test_auth.py#L86) | Examples using body requirements and separate synchronous and asynchronous methods. These examples are corroborating evidence, not an automatic answer key. |

These sources support a technical usage contract. They do not certify an owner's approval of a newly generated guide. The local probes below check selected mechanics, not all consequences of violating that contract.

## Decisions covered by this assessment

There are six decision units in one family. They are not six independent experimental cases.

| ID | What a supported answer should explain | Qualification or valid alternative |
|---|---|---|
| D1 | A common `auth_flow` can provide shared authentication logic through the default synchronous and asynchronous adapters. | HTTP requests can be yielded for the client to perform. This does not mean arbitrary blocking calls inside the common flow become asynchronous. |
| D2 | When the common flow needs an unread request body, `requires_request_body` makes the default adapter load it before calling that flow. | An already loaded body does not need to be read again. Do not claim that every authentication scheme must enable the flag. |
| D3 | `requires_response_body` makes the default adapter load a response before returning it to the common flow. | A flow that only checks response headers does not need the body. An already loaded response is another valid case. |
| D4 | Custom I/O or locking can use the appropriate `sync_auth_flow` and `async_auth_flow` implementations. | Overriding the method does not itself make a blocking operation safe for an asynchronous client. The chosen operation still needs appropriate behaviour. |
| D5 | A scheme can explicitly support only one client mode and reject the other. | Requiring every scheme to support both modes would invent an obligation. Any later coding task may separately require both. |
| D6 | The body flags are implemented by the default adapters. Replacing an adapter bypasses those reads unless the override performs or delegates them. | A custom adapter can load the body itself or preserve the base behaviour through appropriate delegation. The flag is not a global guarantee. |

D1 to D5 combine published guidance with implementation evidence. D6 is an implementation consequence of the adapter structure, checked locally. These are provenance descriptions, not proof that a model would infer any of them independently.

## What the agents may receive

The development prompt is: “Prepare guidance for developers extending HTTPX authentication at the supplied version. Explain which logic can be shared, which behaviour needs a specialised implementation, and what the framework does on their behalf. Support each claim with its source and record exceptions or uncertainty.”

For this development specification, propose complete files rather than answer revealing excerpts: the `httpx/` Python package, the full authentication guide and the package licence. The drafter and verifier receive the same source permission. Record their exact file hashes when the dispatcher builds the pack. No later coding task has been chosen for this case, and none is supplied.

The independent assessor may also receive the case reference, source evidence and saved draft, verifier decisions and resulting guide. It must assess the claims itself; verifier acceptance is not the expected score. In assessor qualification, the expected labels for the examples below must remain outside the model's inputs.

Keep this README, the selection record, probe code and results, expected example labels, inventory and research conversation out of drafter and verifier inputs. No actual isolated pack or provider context has been built or dispatched. The proposed file scope is a development input specification, not a completed disclosure audit.

**Information condition:** documentation visible. Both the guide and source docstrings state parts of the rule. Removing the guide would not make this a clean code inference case. Do not strip these disclosures merely to claim that a rule was hidden.

## Example answers and expected assessment

These are authored development examples. They illustrate judgements to specify and later qualify; they are not observed model answers or an independent qualification set.

| Example claim or output | Expected assessment and reason |
|---|---|
| “Use the common flow for shared logic and yield requests for the client to send. Use specialised methods when authentication needs other I/O.” | Supported for D1 and D4. Check that the answer supplies the relevant evidence. |
| “Authentication must never perform I/O.” | Materially overbroad. It erases the supported specialised implementations. |
| “Every authentication scheme must implement both modes.” | Unsupported obligation; D5 permits explicit rejection of an unsupported mode. |
| “Setting the body flag guarantees the body is available even after replacing the entire adapter.” | Incorrect. D6 and the override probes show why this is not guaranteed. |
| “No body flag is needed if the flow only reads headers.” | Valid exception. Do not reject it for departing from a body dependent example. |
| “A specialised adapter can load the body itself before using it.” | Valid alternative; confirm that the answer uses the appropriate read operation. |
| A correct account of shared logic that says nothing about body access or overrides. | Credit supported claims and record D2, D3 and D6 as omissions. It is incomplete, not wholly incorrect. |
| An empty guide. | Zero recovered decisions and six omissions in this audited scope. It contains no unsupported assertions, but cannot pass solely for that reason. Retain the preparation outcome and cost. |
| “The project owner approved this new guide.” | Unsupported authority claim. Public documentation cannot establish that approval. |

For each decision, record supported, partially supported, contradicted or omitted, with source evidence and a short reason. Record unsupported added obligations separately. A claim can express several decisions; split it for assessment. Multiple phrasings of the same decision earn coverage once. Accept semantically equivalent wording and justified alternatives.

Count coverage only against these six audited decisions. Report material errors, omissions and unsupported authority separately rather than hide them inside one percentage. Wrong advice about body availability, unsafe mode substitution or a blanket prohibition is a material error. Numerical qualification thresholds and the overall pass rule are still open; this case does not silently set them.

## Local verification

[Recorded results](recorded-results.json) contain 15 checks. Public client calls verify shared and specialised dispatch using a mock transport. Direct adapter checks compare unread request and response bodies with and without the flags in both modes. Additional checks show the override exception and an explicit refusal of an unsupported mode.

All 15 matched the expectations written in [probe.py](probe.py). Deliberately missing body reads are expected to raise the appropriate error; they are not successful authentication implementations. The run used Python 3.13.12 and the dependency versions recorded in the result. This investigator environment does not qualify the proposed experimental runtime.

To reproduce, extract the pinned archive into a local directory, verify its archive hash against the manifest, and use the dependency versions recorded in the result. Run `python research/development/h06-guidance-assessment/probe.py --source PATH_TO_PINNED_HTTPX --output local-runs/h06-guidance-results.json`. The script checks the recorded package and reference file hashes before importing the source. It uses no model or external network service. It records its own hash and the actual dependency versions; different environments require review, not an assumption of equivalence.

The checks do not measure event loop blocking, race conditions, memory growth, real authentication services or cryptographic security. They do not validate a verifier, semantic assessor or operating system boundary. Broader claims remain outside this case.

## Next action

Use this case to specify the restricted input and assessment records. Check the remaining candidate families before final trial selection, and construct separate qualification cases. This whole H06 family is now development material because its expected answers are public here. Do not count it as an untouched test of an assessor tuned using this case. Before any guide is prepared for a later coding comparison, choose and record its compatible historical tasks and source versions. This development guide has no declared reuse in Phase 2.
