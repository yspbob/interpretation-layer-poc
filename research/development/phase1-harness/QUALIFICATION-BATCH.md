# Qualification runner: offline checks complete

**Update, 15 September:** [The revised bank rehearsal](../astra-preparation/ASTRA-BATCH-READINESS.md) passed all 144 scheduled requests after assessment instruction binding. All 73 tests passed. The earlier results below remain historical; the new record contains the current input commitment and limits.

The runner now rehearses the fixed 144 call qualification schedule with one shared spending record. It reuses the existing provider adapter and creates a fresh connection for each scheduled call. It currently accepts only locally supplied responses. It has no live execution switch, credential argument or permission to spend.

This work tests the machinery that will deliver the reviewer tests. It does not test whether any reviewer gives a correct answer.

## What it does

The loader requires the expected hash of a private freeze record. It reads only the scheduled items, source packs, permitted references and role contracts covered by that freeze. It does not load scoring keys, investigator notes or the project state. It checks every input before starting the batch, including source identity, reference permissions, response identity fields, item balance and the two scheduled repetitions.

Before each call, the runner saves a reservation for the maximum configured cost. All attempts draw from the same batch allowance. It saves the request, response, usage and outcome, and preserves the original order. Records are written to new files and flushed before dispatch. The ledger links each event to the preceding event by hash.

An invalid answer with known usage remains a failed item and its cost is charged. The runner proceeds to the next scheduled item without retrying it. If usage is unknown, it stops the batch and retains the full reservation. Calls that could not run remain listed in the summary. A budget stop also preserves the unrun part of the schedule.

An existing output folder cannot be reused, and a batch object cannot run twice or concurrently. An interrupt records the current uncertain attempt and the remaining schedule when the process can still write. A hard process kill can prevent a final summary; the previously written reservation remains the last record. There is no automatic recovery, renewed budget or retry policy.

## Recorded checks on 14 September 2026

All 72 tests passed: 20 new batch tests and 52 existing controller and provider tests. The batch checks covered:

* The full fixed schedule, fresh inputs and the absence of hidden answers in requests.
* One shared allowance, reservation before dispatch and a stop before another call would exceed the allowance.
* Timeouts, missing usage and reported usage exceeding the reserved bounds.
* Invalid JSON, wrong assessment identities, repeated claim IDs and changed scope on admission.
* Changed frozen files, duplicated schedule entries, unexpected input fields and references sent to the wrong role.
* Reused folders, repeated or concurrent execution, interrupted calls and failed reservation writes.
* A simulation handler that evaluates as false, to ensure it still cannot select a live transport.

Separately, the full 144 request schedule completed with public synthetic material and with the actual frozen private inputs. These are two rehearsals of the same schedule, not 288 qualification answers. Every request passed through the existing SDK path to a local simulated response. Socket connections and live HTTP transport were disabled during the checks.

The private rehearsal's largest encoded request was 28,346 bytes. Its settings used a fictional model identifier, low reasoning effort and artificial prices. This does not establish the token count, compatibility, price or behaviour of the intended live model. Actual study settings still need verification.

The synthetic responses deliberately make no claim of correctness. The runner checks their structure, claim IDs, scope and record identity. It does not load the answer key or declare a reviewer qualified. Evidence based scoring, including review of the explanations, remains a separate step.

Machine readable public totals and source hashes are in [qualification-batch-results.json](qualification-batch-results.json). Raw private requests and responses remain outside this repository. The original bank freeze was not modified.

## Reproduce the offline checks

From the repository root, with the existing Phase 1 environment:

```powershell
local-runs/phase1-env/Scripts/python.exe research/development/phase1-harness/run_qualification_checks.py
```

This runs the relevant tests and a full synthetic rehearsal. It writes a new ignored folder under `local-runs/batch-checks`. A private bank rehearsal additionally requires `--bank`, `--freeze`, `--freeze-sha256` and `--output`. Both the bank and output must be outside this public checkout. Use the current private state record to select the exact freeze; do not substitute a later hash without reviewing the change.

The first restricted test invocation could not access temporary test folders. The recorded successful checks ran with filesystem access to those folders while retaining the explicit network denials.

## What comes next

Complete the controlled familiarity connection and prepare the actual model/account checks. Before live qualification, freeze the full protocol and settings, bind any live batch entry point to the authorised allocation, and verify it with simulation. Any recovery after interruption needs an explicit policy that retains prior spending and attempts. No paid call is authorised by the existence of this runner.

Keep this implementation focused on the fixed schedule. Coding execution, interaction and a general assessment platform are outside this step.
