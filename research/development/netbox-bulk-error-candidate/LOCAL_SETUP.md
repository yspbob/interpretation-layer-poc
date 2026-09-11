# Running the NetBox reproduction on Windows

Use Docker Desktop with its WSL 2 backend on each machine. The project files and reproduction script travel through the shared GitHub repository. Each machine builds its own environment; do not copy live databases or Docker's virtual disk between machines.

The laptop's 32 GB is expected to be sufficient for this narrow task. Start with an 8 GB WSL limit and run one revision at a time. This is an initial resource allocation, not a measured minimum. PostgreSQL is limited to 1 GB, Redis to 256 MB and the probe container to 4 GB. Image builds also use the WSL environment. These settings do not describe the capacity needed for a future local language model.

All three revisions completed on the current PC with this 8 GB WSL cap. Spot checks during database setup were below 1 GB combined for the three running containers; these are not peak measurements and exclude image building and Windows. The laptop has not yet been tested.

## Once on each machine

Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) with the WSL 2 backend. Start it and confirm the engine is running. A separate Ubuntu installation is not required for this Docker workflow.

WSL supports a memory cap in the Windows user's `.wslconfig`. For this project, the starting settings are:

```ini
[wsl2]
memory=8GB
swap=2GB
```

Preserve any existing settings when adding these values. The cap applies to WSL as a whole, including other WSL work. Apply changes when it is safe to restart WSL; do not interrupt other running tasks. See [Microsoft's WSL configuration documentation](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

## Run the reproduction

From the shared project folder in PowerShell:

```powershell
./research/development/netbox-bulk-error-candidate/run-local.ps1
```

The script builds and tests the starting revision, feature merge and later QA revision sequentially. For just one revision, add `-Revision starting`, `-Revision feature` or `-Revision later-qa`.

Each attempt uses a uniquely named Compose project and a fresh database. It leaves results under `local-runs/netbox-runtime/`, which is excluded from Git. On completion or failure it removes only that attempt's containers and disposable volumes. It retains images to make later builds faster. It does not start on a schedule or publish results automatically.

The first build downloads source, packages and base images. At runtime the containers use an internal network with no published host ports. No webhook worker starts, and the configured webhook destination is loopback. The check observes real jobs placed in Redis, not delivery to an external recipient.

## Reading the result

`observations.json` records the source revision, script and configuration hashes, installed package versions, database state, change log counts, API responses and queued webhook jobs. `images.json` records image identities and service digests; `container-log.txt` preserves application output.

A completed probe can expose a rule violation. That is a result, not necessarily a broken test runner. Check `completed`, the four scenario records and `satisfies_scoped_rule` separately. An unexpected response, failed database check or failed successful batch control stops the command. Failed attempts remain in their own result folders.

The historical later QA version is a comparator. It does not define the rule or excuse an unresolved earlier requirement. These are public development checks, with investigator access to the sources and expected behaviour. They do not qualify an AI judge or demonstrate agent isolation.
