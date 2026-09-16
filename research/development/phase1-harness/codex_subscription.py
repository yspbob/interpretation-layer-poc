"""Single packet collector for Codex subscription checks and approved batches.

No batch dispatch, credential discovery, API fallback, retry or semantic scoring.
The operator supplies a reviewed client/catalogue and a fresh account observation.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
from types import SimpleNamespace

from harness import digest, ids, refs_valid, require, validate_draft, validate_review, wire
from provider import Provider, PROMPTS, SCHEMAS, api_schema, strict_json
from qualification_batch import validate_answer

CLIENT_HASH = "960c111d47afd61669954b9df9e56083e302edbfa3ef6962d81dcc14a30051dc"
MINIMUM_REMAINING_PERCENT = 5
ROLES = ("verifier", "guidance_assessor", "verifier_assessor")
SYSTEM_SKILLS = ("imagegen", "openai-docs", "plugin-creator", "review-agent", "skill-creator", "skill-installer")
WARNINGS = {
    "`--dangerously-bypass-hook-trust` is enabled. Enabled hooks may run without review for this invocation.",
    "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; enable `features.code_mode_host` and install `codex-code-mode-host`.",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def toml(value):
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k) + "=" + toml(v) for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ",".join(map(toml, value)) + "]"
    return json.dumps(value)


class ProfileSkillError(ValueError):
    """Retain the exact rejected listing even if the entry later disappears."""

    def __init__(self, message, directory, entries, unexpected):
        super().__init__(message)
        self.observation = {"directory": str(directory), "observed_entries": entries,
                            "unexpected_entries": unexpected, "observed_at_ns": time.time_ns()}


def verify_skill_entries(directory, permitted, message):
    entries = [p.name for p in directory.iterdir()]
    unexpected = []
    for name in entries:
        if name in permitted:
            continue
        # The pinned Windows client does not discover a regular desktop.ini
        # as a skill. Never extend this exception to a directory or link.
        if name == "desktop.ini":
            try:
                info = (directory / name).lstat()
                if stat.S_ISREG(info.st_mode) and not (
                        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
                    continue
            except OSError:
                pass  # An uncertain type still stops collection.
        unexpected.append(name)
    if unexpected:
        raise ProfileSkillError(message, directory, entries, unexpected)


def verify_profile(home, work):
    """Fresh profiles must not acquire instruction files or workspace inputs."""
    require(not any(work.iterdir()), "Working folder is no longer empty")
    require(not any((home / name).exists() for name in ("AGENTS.md", "AGENTS.override.md")),
            "Unexpected profile instructions")
    roots = {work, *work.parents, Path.home()}
    require(not any((root / ".agents" / "skills").exists() for root in roots),
            "Discoverable external skills")
    require(not Path("/etc/codex/skills").exists(), "Discoverable administrator skills")
    skills = home / "skills"
    if skills.exists():
        verify_skill_entries(skills, (".system",), "Unexpected profile skill")
        system = skills / ".system"
        if system.exists():
            verify_skill_entries(system, (*SYSTEM_SKILLS, ".codex-system-skills.marker"),
                                 "Unreviewed bundled skill")


def load_packet(path, expected_hash):
    require(sha(path) == expected_hash, "Packet commitment changed")
    packet = strict_json(Path(path).read_bytes())
    require(packet.get("role") in ROLES, "Only assessment roles permitted")
    # Reuse the exact role/identity checks without creating a provider or credential.
    adapter = SimpleNamespace(mode="simulation", bound_run="public", calls=0,
        prompts=PROMPTS, schemas=SCHEMAS, source_hash=digest(packet["sources"]),
        reference_hash=digest(packet.get("reference")), settings=SimpleNamespace(
            model="gpt-6-astra", reasoning_effort="high", max_output_tokens=8192,
            request_byte_limit=100000, input_padding_tokens=4096, max_input_tokens=100000))
    Provider.request(adapter, {"mode": "simulation", "run_id": "public", "call_id": 1,
        "packet": packet, "instruction": PROMPTS[packet["role"]]})
    sources = packet["sources"]
    for source in sources["files"].values():
        require(hashlib.sha256(source["text"].encode()).hexdigest() == source["sha256"], "Source text hash mismatch")
    draft = packet["submission"]["draft"] if packet["role"] == "verifier_assessor" else packet["candidate"]
    validate_draft(draft, sources)
    if packet["role"] == "verifier_assessor":
        validate_review(packet["submission"]["review"], draft, sources)
    if "reference" in packet:
        require(bool(packet["reference"]["units"]), "Empty reference")
        ids(packet["reference"]["units"], "id")
        for unit in packet["reference"]["units"]:
            refs_valid(unit.get("evidence", []), sources)
    return packet


def audit_events(folder, packet, code):
    """Save the first answer even if later events invalidate the collection."""
    folder = Path(folder)
    events = [strict_json(line) for line in (folder / "events.jsonl").read_bytes().splitlines() if line]
    answers = [e["item"]["text"] for e in events if e.get("type") == "item.completed"
               and e["item"].get("type") == "agent_message"]
    if answers:
        (folder / "first-answer.txt").write_text(answers[0], encoding="utf-8")
    require(code == 0, "Client failed or collection stopped")
    require(not (folder / "STOP").exists(), "Stop requested before collection completed")
    require(not (folder / "stderr.txt").read_bytes().strip(), "Unreviewed client diagnostic")
    require((folder / "startup-ok").exists(), "Startup hook did not execute")
    require(not (folder / "tool-attempt.json").exists(), "Tool attempt invalidates collection")
    allowed = {"thread.started", "turn.started", "turn.completed", "item.started", "item.updated", "item.completed"}
    for e in events:
        require(e.get("type") in allowed, "Unexpected client event")
        if "item" in e:
            item = e["item"]
            require(item.get("type") in {"error", "reasoning", "agent_message"}, "Tool or unreviewed item")
            if item["type"] == "error":
                require(item.get("message") in WARNINGS, "Unreviewed client error")
    counts = {t: sum(e["type"] == t for e in events) for t in ("thread.started", "turn.started", "turn.completed")}
    require(all(n == 1 for n in counts.values()) and len(answers) == 1, "Expected one session, turn and answer")
    answer = strict_json(answers[0])
    require(strict_json((folder / "last-answer.json").read_bytes()) == answer, "First and last answer differ")
    validate_answer(answer, packet)
    usage = next(e["usage"] for e in events if e["type"] == "turn.completed")
    require(all(type(usage.get(k)) is int and usage[k] >= 0 for k in ("input_tokens", "output_tokens")), "Usage missing")
    return {"status": "structurally_valid", "role": packet["role"], "usage": usage,
        "thread_id": next(e["thread_id"] for e in events if e["type"] == "thread.started"),
        "answer_hash": digest(answer), "qualified": False}


def run_packet(packet_path, packet_hash, folder, exe, catalog, *, mock_url=None,
               auth_path=None, account_observation=None, deadline=300,
               qualification_permit=None, dispatch_guard=None):
    """One attempt. Qualification requires the batch's bound permit and guard."""
    require(0 < deadline <= 300, "Deadline exceeds public check limit")
    packet = load_packet(packet_path, packet_hash)
    require(sha(exe) == CLIENT_HASH, "Unreviewed client binary")
    if mock_url is not None:
        require(mock_url.startswith("http://127.0.0.1:") and auth_path is None, "Local simulation only")
    else:
        require(auth_path is not None and account_observation is not None, "Subscription evidence required")
        if qualification_permit is None:
            require(account_observation.get("public_probe_only") is True, "Qualification permit required")
        else:
            require(set(qualification_permit) == {"packet_hash", "output_path", "allocation_hash", "approval_reference"}, "Invalid permit")
            require(qualification_permit["packet_hash"] == packet_hash
                    and qualification_permit["output_path"] == str(Path(folder).resolve())
                    and all(isinstance(qualification_permit[k], str) and qualification_permit[k]
                            for k in ("allocation_hash", "approval_reference")), "Permit binding mismatch")
            require(account_observation.get("public_probe_only") is False and callable(dispatch_guard), "Batch guard required")
            dispatch_guard()
        require(0 <= time.time() - account_observation["observed_at"] <= 120, "Stale account check")
        require(account_observation.get("ordinary_usage_allowed") is True
                and account_observation.get("remaining_percent", 0) > MINIMUM_REMAINING_PERCENT
                and account_observation.get("credits_balance") == "0"
                and account_observation.get("has_credits") is False, "Included allowance uncertain")
        auth = strict_json(Path(auth_path).read_bytes())
        require(auth.get("auth_mode") == "chatgpt" and not auth.get("OPENAI_API_KEY"), "ChatGPT authentication required")
        require(auth.get("tokens", {}).get("account_id") == account_observation.get("account_id"), "Account mismatch")
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=False)
    home, work = folder / "home", folder / "work"
    home.mkdir(); work.mkdir()
    (folder / "packet.json").write_bytes(wire(packet))
    (folder / "instructions.txt").write_text(PROMPTS[packet["role"]], encoding="utf-8")
    (folder / "schema.json").write_bytes(wire(api_schema(SCHEMAS[packet["role"]])))
    shutil.copyfile(catalog, folder / "models.json")
    (home / "config.toml").write_text('[features]\nhooks = true\n', encoding="utf-8")
    (folder / "deny.py").write_text('import json,sys\nfrom pathlib import Path\nx=json.load(sys.stdin)\nPath('
        + repr(str(folder / "tool-attempt.json")) + ').write_text(json.dumps(x))\nprint(json.dumps({"hookSpecificOutput":'
        '{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"POC_DENY_ALL"}}))\n')
    (folder / "startup.py").write_text('from pathlib import Path\nPath('
        + repr(str(folder / "startup-ok")) + ').write_text("yes")\nprint("{}")\n')
    hooks = {"PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "timeout": 3,
        "command": f'& "{sys.executable}" "{folder / "deny.py"}"'}]}],
        "SessionStart": [{"hooks": [{"type": "command", "timeout": 3,
        "command": f'& "{sys.executable}" "{folder / "startup.py"}"'}]}]}
    (home / "hooks.json").write_bytes(wire({"hooks": hooks}))
    settings = {"model": "gpt-6-astra", "model_reasoning_effort": "high", "project_doc_max_bytes": 0,
        "web_search": "disabled", "approval_policy": "never", "sandbox_mode": "read-only",
        "memories.use_memories": False, "memories.generate_memories": False, "history.persistence": "none",
        "features.hooks": True, "model_instructions_file": str(folder / "instructions.txt"),
        "model_catalog_json": str(folder / "models.json"), "forced_login_method": "chatgpt",
        "cli_auth_credentials_store": "file"}
    for feature in ("apps plugins shell_tool unified_exec code_mode_host code_mode browser_use computer_use "
                    "multi_agent multi_agent_v2 goals sleep_tool view_image skill_search skill_mcp_dependency_install "
                    "workspace_dependencies tool_suggest shell_snapshot unbounded_connection_retries").split():
        settings["features." + feature] = False
    settings["skills.config"] = [{"path": str(home / "skills/.system" / name / "SKILL.md"), "enabled": False}
        for name in SYSTEM_SKILLS]
    if mock_url:
        settings.update({"model_provider": "poc_probe", "features.enable_request_compression": False})
        for k, v in {"name": "Local artificial probe", "base_url": mock_url, "requires_openai_auth": False,
                     "wire_api": "responses", "request_max_retries": 0, "stream_max_retries": 0,
                     "stream_idle_timeout_ms": 1500, "supports_websockets": False}.items():
            settings["model_providers.poc_probe." + k] = v
    args = [str(exe), "-a", "never", "exec", "--strict-config", "--ephemeral", "--skip-git-repo-check",
            "--json", "--color", "never", "-C", str(work), "--dangerously-bypass-hook-trust",
            "--output-schema", str(folder / "schema.json"), "-o", str(folder / "last-answer.json")]
    for k, v in settings.items():
        args.extend(["-c", k + "=" + toml(v)])
    args.append("-")
    (folder / "invocation.json").write_bytes(wire({"args": args, "deadline_seconds": deadline,
        "mode": "simulation" if mock_url else ("subscription_qualification" if qualification_permit else "public_subscription_probe"), "packet_hash": packet_hash,
        "qualification_permit": qualification_permit,
        "account_observation": account_observation, "client_hash": CLIENT_HASH}))
    committed = {str(p.relative_to(folder)): sha(p) for p in folder.rglob("*") if p.is_file()}
    (folder / "input-commitment.json").write_bytes(wire(committed))
    (folder / "collector.py").write_bytes(Path(__file__).read_bytes())
    # Exercise the exact hooks before giving the client any authentication.
    for script, payload in (("startup.py", b"{}"), ("deny.py", b'{"tool_name":"public_preflight"}')):
        check = subprocess.run(["powershell", "-NoProfile", "-Command", f'& "{sys.executable}" "{folder / script}"'],
            input=payload, capture_output=True, timeout=10)
        (folder / (script + ".preflight")).write_bytes(check.stdout + check.stderr)
        require(check.returncode == 0, "Hook command failed")
        if script == "deny.py":
            require(strict_json(check.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny", "Denial failed")
    (folder / "startup-ok").unlink(); (folder / "tool-attempt.json").unlink()
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("CODEX", "OPENAI", "POC_OPENAI"))
           and k.upper() not in {"HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"}}
    env["CODEX_HOME"] = str(home)
    code = None
    started = time.monotonic()
    try:
        if dispatch_guard:
            dispatch_guard()
        if not mock_url:
            require(0 <= time.time() - account_observation["observed_at"] <= 120, "Account check expired during preparation")
        if auth_path:
            shutil.copyfile(auth_path, home / "auth.json")
        verify_profile(home, work)
        with (folder / "events.jsonl").open("xb") as out, (folder / "stderr.txt").open("xb") as err:
            process = subprocess.Popen(args, cwd=work, env=env, stdin=subprocess.PIPE, stdout=out, stderr=err)
            try:
                process.stdin.write(wire(packet)); process.stdin.close()
                while process.poll() is None:
                    if dispatch_guard:
                        dispatch_guard()
                    require(time.monotonic() - started <= deadline, "Deadline reached")
                    require(not (folder / "STOP").exists() and not (folder / "tool-attempt.json").exists(), "Stop or tool attempt")
                    verify_profile(home, work)
                    require(all(sha(folder / name) == value for name, value in committed.items()), "Input drift")
                    require(sum((folder / name).stat().st_size for name in ("events.jsonl", "stderr.txt")) < 1000000, "Output record limit")
                    time.sleep(.1)
                code = process.returncode
            finally:
                if process.poll() is None:
                    process.kill(); process.wait(timeout=10)
        require(not (folder / "STOP").exists(), "Stop requested before collection completed")
        verify_profile(home, work)
        if dispatch_guard:
            dispatch_guard()
        require(sum((folder / name).stat().st_size for name in ("events.jsonl", "stderr.txt", "last-answer.json")
                    if (folder / name).exists()) < 1000000, "Output record limit")
        require(all(sha(folder / name) == value for name, value in committed.items()), "Input drift")
        result = audit_events(folder, packet, code)
        result.update(mode="simulation" if mock_url else ("subscription_qualification" if qualification_permit else "public_subscription_probe"), elapsed_seconds=round(time.monotonic() - started, 2))
        (folder / "result.json").write_bytes(wire(result))
        return result
    except Exception as exc:
        # Preserve first output even when an external stop invalidates the attempt.
        try:
            audit_events(folder, packet, code)
        except Exception:
            pass
        failure = {"error": str(exc), "exit_code": code}
        if isinstance(exc, ProfileSkillError):
            failure["profile_observation"] = exc.observation
        (folder / "failure.json").write_bytes(wire(failure))
        raise
    finally:
        (home / "auth.json").unlink(missing_ok=True)
