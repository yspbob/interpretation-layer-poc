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

## Future experiment execution

The [runner design](https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/isolated-runner-design-v0.1.md) proposes local VirtualBox/Ubuntu/Podman execution on either machine, using the 32 GB laptop as the common baseline. The home PC does not need to remain on. Runtime installation and containment qualification are separate from this repository setup and have not been completed.

Codex can inventory each machine with `powershell -NoProfile -File scripts/runner-preflight.ps1 -MachineAlias laptop` (use `home` on the home PC). On machines that block local scripts, a reviewed invocation may add `-ExecutionPolicy Bypass` for that process only; do not change the persistent execution policy. This changes no machine settings; its report stays in ignored `local-runs/`. Unknown observations are not passes, and the report never authorises model runs.

A separate private GitHub repository is the chosen future home for sealed cases and confidential records. It has not been created; the existing sync script handles only the public project. Once implemented, the agent must verify the private save and matching environment before continuing on the other machine. Complete comparison blocks stay on one host. VM disks, credentials and active processes are not transferred through Git, and no manual handover document is required.
