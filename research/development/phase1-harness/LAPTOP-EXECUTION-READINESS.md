# Laptop execution readiness

16 September 2026. Local validation and allocation preparation are complete. **No new model call was made and no role is qualified.** The replacement allocation still requires explicit approval.

Subsequent status: the user approved this configuration, and its allocation stopped at attempt six. Read [the stop and scoring report](SUBSCRIPTION-QUALIFICATION-V02-STOP.md). The preparation record below is historical; it is not a pending approval or permission to resume.

## Concrete proposal

| Setting | Proposed execution |
|---|---|
| Bank | Frozen Q01, Q05, Q06 and Q08; contract v0.2 and assessment instructions v3 |
| Allocation | At most 144 sequential fresh attempts, 48 per assessment role |
| Route | Existing Codex subscription, Astra High; zero additional spending |
| Limits | Five minutes per attempt, one megabyte of output records, allowance above 5% before each dispatch |
| Stops | First failed or uncertain collection, tool attempt, changed inputs/configuration, operator stop, approval expiry or unavailable allowance |
| Continuation | No automatic retry or resume; retain every attempted position and record any later decision explicitly |
| Approval | Pending; both approval flags are false |

The four scoring requirements are unchanged. The [bank readiness record](../astra-preparation/POST-REPAIR-READINESS.md) discloses earlier exposure, the Q07 retirement and the criterion amendments. Nothing is carried forward from the closed allocation as a new answer or approval. The [version 2 subscription protocol](SUBSCRIPTION-PROTOCOL.md) governs this proposal.

Configuration commitment: `a5c3d268913acbbac63a0847ae400e9fcb6112e536d85fc43d569ddd596d1dcb`.

Private preparation: `laptop-execution-allocation-v2-2026-09-16/prepared-allocation.json`. The account, full local paths, exact execution arguments and unapproved template are private. The proposed output folder does not yet exist. A future approval must be a separate record bound to this configuration, with an explicit reference and expiry; do not edit the frozen pending template.

## Installed client and evidence

The laptop reports `codex-cli 0.154.0-alpha.6.2`, the same version string as the home PC, but its executable bytes differ. The collector now pins the laptop executable SHA-256 `960c111d47afd61669954b9df9e56083e302edbfa3ef6962d81dcc14a30051dc`. An unchanged version label was not treated as sufficient evidence. The home PC's earlier binary is no longer accepted by this working collector; historical snapshots remain intact.

The saved local catalogue has SHA-256 `204961f0710b407a651cc8fe19ae3cf2a77d0d91e92dbbf17c930aebcb2b15f8`. Captured loopback requests selected `gpt-6-astra` with High reasoning effort. The live proposal also binds Python 3.13.12, dependency versions, all nine execution/protocol files, prompts, schemas, bank, schedule, account and output directory.

The final **24 local simulator cases passed their declared checks**:

- Three artificial assessment packets each completed with one structurally valid answer and recorded usage. Their answers were scripted, not model reasoning.
- Four deliberately contaminated preparations were refused before any request: profile instructions, workspace instructions, an ancestor skill and an extra profile skill.
- HTTP failure, disconnected stream and idle timeout each stopped after one local request. These observations concern the simulator transport, not hidden subscription retries.
- Deadline, operator stop, changed committed instructions and a newly added workspace file each stopped collection.
- All ten advertised tool paths were exercised. Eight reached the denial hook and collection stopped. The code execution and wait paths returned a disabled-host failure and collection was rejected. No agent was spawned or contacted; targets and calls were artificial.

The captured requests contained no authorization header, available-skills catalogue, project instructions or investigator state. The final test script used no authentication and no client-hash override. All **127 offline harness tests passed**, including account gates, approval revocation, first-answer retention, completion-time stop handling and the new profile checks. Boundary tests refuse 4.99% and 5%, and allow 5.01% past the allowance gate, in both collector and coordinator. The 24 client probes preceded this threshold amendment; client settings are unchanged. Account-binding checks remain private; login credentials were neither copied into the simulator nor archived.

## Failures retained and resulting changes

The first canary probe demonstrated that `project_doc_max_bytes=0` does not exclude instructions inserted into the separate profile. It also found an available skill inserted into the working folder. The earlier collector accepted those artificial responses because it checked changes to known input files, not newly added instruction locations.

A second probe tested the client's experimental `skip_host_skill_discovery` setting. It still included the workspace skill description and emitted a previously unreviewed diagnostic. Those responses failed collection. The setting and an intermediate warning allowance were removed; the final configuration does not rely on them.

The collector now checks before launch, during collection and after completion that the working folder is empty, profile instruction files are absent, and checked external skill directories are absent. It also rejects extra profile skills and unreviewed bundled skill names. The six bundled skill paths are explicitly disabled. This follows the documented distinction between [repository, user, administrator and bundled skill locations](https://learn.chatgpt.com/docs/build-skills), while treating observed request captures as the evidence for this installed client.

The initial and intermediate probes, scripts, captures and failures remain preserved alongside the final checks. They were local artificial tests and did not expose a reserved packet to a model.

## Remaining limits and next step

These are tests of specified input and tool paths, not proof of arbitrary operating-system containment. Input checks can have races; hooks have previously failed open when broken. OpenAI's [hook documentation](https://learn.chatgpt.com/docs/hooks) also excludes hosted tools and cautions that specialized paths can bypass the general hook boundary. No hosted tool appeared in the captured catalogue, and the code host remained disabled.

Some forced local tool attempts produced a second simulator request before collection stopped. The subscription route therefore promises one collector attempt per position, not exactly one backend request. It records intended inputs, settings, events, first answers and usage, but does not independently capture the authenticated provider wire exchange, identify an immutable served model snapshot, disable every hidden retry or enforce a provider token cap. The public source families may also have prior model familiarity.

Private evidence commitment: `e3d1b9a4553c68ec4d0e38c3dcd32cc084b77d94af95bd03c82d87a19a21dfad`, covering 1,518 records. Generated client caches were excluded with an explicit inventory. Earlier research freezes are unchanged.

The amended allocation and 127-test record have commitment `8a5be3e5f2bc39ea3e8c1a0a2a76fcbc21fdc5c95e2931a900c6ea4c771f5eab`. The earlier 10% proposal is preserved and superseded. Account observations remain private and must be refreshed before dispatch.

Next obtain approval for the concrete configuration and protocol limits, then obtain fresh account evidence before each dispatch. The user explicitly selected a 5% stop threshold and intends to arrange more allowance. This does not authorise this task to buy or redeem credits. Any continuation after a recorded stop requires an explicit, preserved decision. Zero experimental guidance runs have been completed.
