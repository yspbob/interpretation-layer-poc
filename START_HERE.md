# Continue the POC on either Windows machine

Once the project is set up, open it in Codex and say **“Continue the POC”**, or simply ask for the next change. Codex is instructed to get the latest files first and save both its work and the relevant decisions to GitHub before finishing. You do not need to prepare a handover or remember a finish command.

## One-time setup on each machine

1. Have Git and Node.js 22.13 or newer available. Sign in to GitHub on that machine with access to `yspbob/interpretation-layer-poc`; keep credentials in the machine's credential manager.
2. Clone [the POC repository](https://github.com/yspbob/interpretation-layer-poc) into a normal local folder. Use a separate clone on each machine, rather than syncing a working folder through OneDrive.
3. Add that folder as a local Codex project named **Interpretation layer POC**. Make the repository root the primary folder, so Codex discovers `AGENTS.md`. Work directly in that saved folder for this sequential workflow.
4. Start a conversation in the project and say “Continue the POC.” The project record gives it the current decisions and next step even when the previous conversation is unavailable.

Codex can perform the clone and dependency checks. The app's project selection and any GitHub sign-in may need your interaction. The two clones do not have to use identical folder paths.

If you want a setup prompt for a fresh Codex conversation:

> Set up https://github.com/yspbob/interpretation-layer-poc in a local folder for this Windows machine. If an existing clone is present, preserve it and check its state. Read AGENTS.md and PROJECT_STATE.md, retrieve the latest saved work safely, and tell me which folder to add as the primary folder of my Interpretation layer POC project. Do not start a model experiment as part of setup.

## What gets carried across

The code, editable website, current plan, recorded decisions and next step travel through GitHub. `PROJECT_STATE.md` is maintained by Codex, not by you. The entire conversation, running processes, installed dependencies and credentials are not copied.

Use one machine for editing at a time. Let the current task finish before continuing on the other machine. If connectivity fails, Codex must say that the latest changes have not been saved remotely. If the app closes mid-task, unfinished work stays on that machine until it is recovered. The helper stops on conflicts rather than choosing which machine's work to discard.

This is an agent work routine, not continuous filesystem synchronization or a background service. A completed save is reported with a Git commit; merely closing Codex does not trigger a save.

Local projects provide folder access, and repository instructions provide durable context for later conversations. See the [official OpenAI documentation on projects](https://learn.chatgpt.com/docs/projects). This setup does not assume that creating a local project synchronizes its chat history.

## First continuation on the laptop

The user confirmed on 15 September that the laptop has not run any POC work. Its 32 GB memory is the known hardware constraint; its installed tools and ability to execute the tests are unverified. Do not treat results from the home PC as laptop checks.

The first laptop task is to retrieve both repositories, verify the private evidence and recreate the small Python environment. This does not need NetBox, Docker, VirtualBox or a database server. Those belong to other tasks and should be installed only when the selected work needs them.

1. Read `PROJECT_STATE.md`, then safely sync the public checkout. If Git or Node is absent, arrange that basic setup before using the sync helper. Preserve any existing folders and unfinished changes.
2. Check that GitHub CLI (`gh`) is available, since the private sync helper uses it to check visibility. Sign in to GitHub locally with access to the private repository. Clone [the private evidence repository](https://github.com/yspbob/interpretation-layer-poc-private) outside the public checkout. The suggested location is `%USERPROFILE%/Documents/Codex/poc-private`. Do not copy either machine's credentials.
3. Confirm private visibility and sync using `node scripts/private-project-sync.mjs start "C:/actual/path/poc-private"`. The private helper refuses a different repository or unverified visibility. Subsequent work follows the same fetch, review, commit and publish routine as the public project.
4. Use Python 3.13.12 for parity with the recorded development environment. Check what is installed first; do not overwrite another environment. Recreate `local-runs/phase1-env` in this checkout using that Python installation. Never copy the home PC's virtual environment.
5. Run the commands below. They install the pinned development dependencies, check transfer integrity and run the offline suite. They do not dispatch model requests. Record the actual versions and results on the laptop before claiming it is ready.

```powershell
# From the public repository root, after creating the virtual environment:
./local-runs/phase1-env/Scripts/python.exe -m pip install -r research/development/phase1-harness/provider-lock.txt
./local-runs/phase1-env/Scripts/python.exe -m pip check
./local-runs/phase1-env/Scripts/python.exe scripts/private-evidence.py verify "C:/actual/path/poc-private"
./local-runs/phase1-env/Scripts/python.exe -m unittest discover -s research/development/phase1-harness -p "test*.py"
```

The current suite has 122 tests. It uses artificial records and simulated responses. Windows sandbox restrictions previously prevented tests from using their temporary folders; use an approved normal local invocation if that happens, without weakening permanent Windows settings. Record any failure rather than silently skipping a test.

Website work additionally needs `npm ci --no-audit --no-fund` inside `website/`. It is unnecessary for the immediate evidence and qualification review.

## What to continue after setup

The verifier repair passed six public development examples. Astra is still unqualified. The next research step is to review exposure and compatibility before preparing a new qualification allocation. Read the [repair report](research/development/phase1-harness/VERIFIER-INTERPRETATION.md), [stopped attempt](research/development/phase1-harness/SUBSCRIPTION-QUALIFICATION-STOP.md), current plan and private evidence required for that review. Do not restart completed work or invent a fresh bank simply because the machine changed.

Private records contain reserved cases, raw answers and investigator notes. They must never be supplied wholesale to an agent being tested. Verify their saved hashes, keep original freezes unchanged and give evaluated agents only their permitted packets. Local paths in historical records describe the original host; do not edit those records to match the laptop or execute their old launch scripts. The old qualification allocation is closed. Current contract v0.2 does not silently accept older frozen packets.

Before any later model dispatch, check the laptop's actual client, catalogue, clean profile, tools, account allowance and stop controls. The home PC's pinned client path and validation do not qualify a different installation. Use the subscription only, without API billing or paid credits, and a separately reviewed allocation for reserved work. No model run is part of laptop setup.

Private evidence is synchronized through its own repository. Credentials, installed tools, temporary databases and live processes are excluded. The initial transfer manifest records exclusions; the original files remain on the home PC. Public and private repositories have separate commits, so record their relationship when a piece of work changes both. Let one machine finish and publish before starting on the other.
