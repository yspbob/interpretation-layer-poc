"""Reproduce public, authored Phase 1 development scenarios without a model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import urllib.request
import uuid

from fixtures import scenarios
from harness import Controller, DockerReplay, digest, require, source_pack, wire

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def packs(fetch=False):
    nb = read(HERE.parent / "netbox-bulk-error-candidate/source-manifest.json")
    hx = read(HERE.parent / "h06-guidance-assessment/source-manifest.json")
    specifications = [
        ("netbox", ROOT / "local-runs/netbox-bulk-review/starting-source", nb["starting_revision"],
         {f["path"]: f["sha256"] for f in nb["files"] if f["revision"] == nb["starting_revision"]},
         ["AGENTS.md"], "netbox-community/netbox"),
        ("h06", ROOT / f"local-runs/h06-source/httpx-{hx['source_commit']}", hx["source_commit"],
         {p: sha for p, sha in hx["files"].items() if p.startswith("httpx/") or p in
          {"docs/advanced/authentication.md", "LICENSE.md"}}, [], "encode/httpx"),
    ]
    result = {}
    for name, folder, revision, allowed, instructions, repo in specifications:
        if fetch:
            for path, expected in allowed.items():
                target = folder / path
                if target.exists():
                    continue  # Existing mismatches stop source_pack; never silently overwrite.
                data = urllib.request.urlopen(f"https://raw.githubusercontent.com/{repo}/{revision}/{path}", timeout=30).read()
                require(hashlib.sha256(data).hexdigest() == expected, "Downloaded source mismatch")
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(data)
        result[name] = source_pack(folder, allowed, revision, instructions)
    return result


def audit(folder, sources):
    calls = []
    for path in sorted(folder.glob("invocation-*-input.json")):
        message = read(path)
        packet = message["packet"]
        role = packet["role"]
        require(digest(packet["sources"]) == digest(sources), "Different permitted evidence")
        allowed = {"role", "contract", "sources"}
        if role == "drafter":
            allowed |= {"previous_draft", "feedback"}
        elif role == "verifier":
            allowed |= {"candidate"}
        elif role == "guidance_assessor":
            allowed |= {"candidate", "reference"}
        elif role == "verifier_assessor":
            allowed |= {"submission", "reference"}
        require(set(packet) <= allowed, "Unexpected role input")
        if role in {"drafter", "verifier"}:
            require("reference" not in packet, "Reference leaked")
        output = read(path.with_name(path.name.replace("-input", "-output")))
        require({r["path"] for r in output["reads"]} == set(sources["files"]), "Read trace incomplete")
        require(all(r["allowed"] and r["sha256"] == sources["files"][r["path"]]["sha256"]
                    for r in output["reads"]), "Read trace mismatch")
        calls.append({"role": role, "input_hash": digest(message), "output_hash": digest(output)})
    previous = None
    for path in sorted(folder.glob("event-*.json")):
        event = read(path)
        sha = event.pop("hash")
        require(event["previous"] == previous and digest(event) == sha, "Audit chain mismatch")
        previous = sha
    return {"invocations": calls, "terminal_event_hash": previous}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docker", default=shutil.which("docker"))
    parser.add_argument("--fetch-sources", action="store_true", help="Fetch only pinned public input files before running workers")
    args = parser.parse_args()
    require(args.docker is not None, "Docker not found; pass --docker with its installed path")
    sources = packs(args.fetch_sources)
    transport = DockerReplay(args.docker)
    folder = ROOT / "local-runs/phase1" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    folder.mkdir(parents=True)
    report = {"status": "scripted development only; authored answers, not model judgements",
              "model_calls": 0, "host": platform.platform(), "python": sys.version,
              "image_id": transport.image_id,
              "docker_version": subprocess.check_output([args.docker, "version", "--format", "{{.Server.Version}}"], text=True).strip(),
              "script_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(HERE.iterdir()) if p.suffix in {".py", ".json"} or p.name in {"Dockerfile", "requirements.txt"}},
              "source_packs": {name: {"hash": digest(pack), "revision": pack["revision"],
                              "files": {p: f["sha256"] for p, f in pack["files"].items()},
                              "instruction_paths": pack["instruction_paths"]} for name, pack in sources.items()},
              "runs": [], "boundary_probes": []}
    for name, pack in sources.items():
        reference = read(HERE / ("netbox-reference.json" if name == "netbox" else "h06-reference.json"))
        cases = scenarios(pack, reference)
        if name == "h06":
            cases = {"supported": cases["supported"]}
        for label, fixture in cases.items():
            run_folder = folder / f"{name}-{label}"
            controller = Controller(pack, reference, transport, run_folder)
            result = controller.run(*fixture)
            require(result["status"] != "stopped", f"{name}/{label} stopped: {result}")
            expected_status = {"exhausted": "revision_exhausted", "unresolved": "unresolved"}.get(label, "frozen")
            expected_verdict = "pass" if label in {"supported", "corrected"} else "fail"
            require(result["status"] == expected_status and result["scores"]["released"]["verdict"] == expected_verdict,
                    "Unexpected workflow outcome")
            record = {"case": name, "scenario": label, "result": result,
                      "audit": audit(run_folder, pack)}
            report["runs"].append(record)
            print(f"{name}/{label}: {result['status']}; authored assessment {expected_verdict}", flush=True)
    denied = ["PROJECT_STATE.md", "../netbox-reference.json", "/etc/passwd", "https://example.com", "research/implementation-takeaways.md"]
    for _ in range(2):
        probe = transport.call({"mode": "scripted-development", "probe_boundary": True,
            "packet": {"role": "drafter", "sources": sources["netbox"]}, "reads": denied})
        require(probe["response"]["uid"] == 65534 and all(v is True for k, v in probe["response"].items() if k != "uid"),
                "Container boundary probe failed")
        require(all(not r["allowed"] for r in probe["reads"]), "Read boundary probe failed")
        report["boundary_probes"].append(probe)
    report["total_role_invocations"] = sum(r["result"]["invocations"] for r in report["runs"])
    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    (folder / "report.json").write_bytes(wire(report))
    print(f"Report: {folder / 'report.json'}")


if __name__ == "__main__":
    main()
