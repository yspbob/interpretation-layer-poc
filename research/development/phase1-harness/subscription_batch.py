"""Existing qualification schedule over the subscription collector. No API fallback."""
from collections import Counter
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import platform
import sys
import threading
import time

from codex_subscription import CLIENT_HASH, load_packet, run_packet, sha
from harness import digest, require, wire
from provider import PROMPTS, SCHEMAS, strict_json
from qualification_batch import QualificationBatch, load_bank, validate_answer

HERE = Path(__file__).resolve().parent
RUNTIME = ("subscription_batch.py", "codex_subscription.py", "qualification_batch.py",
           "live_qualification.py", "provider.py", "harness.py", "schemas.py",
           "SUBSCRIPTION-PROTOCOL.md", "SCORING-PROCEDURE.md")


def configuration(bank, output, exe, catalog, account_id):
    bank.verify()
    require(sha(exe) == CLIENT_HASH, "Unreviewed client")
    require(isinstance(account_id, str) and account_id, "Account identity required")
    return {"version": "subscription-qualification-v1", "freeze_hash": bank.freeze_hash,
        "material_hash": bank.material_hash, "schedule_hash": digest(bank.schedule),
        "output_path": str(Path(output).resolve()), "account_id": account_id,
        "client_path": str(Path(exe).resolve()), "client_hash": sha(exe),
        "catalog_path": str(Path(catalog).resolve()), "catalog_hash": sha(catalog),
        "runtime_hashes": {n: sha(HERE / n) for n in RUNTIME},
        "prompts_hash": digest(PROMPTS), "schemas_hash": digest(SCHEMAS),
        "python": platform.python_version(), "python_path": str(Path(sys.executable).resolve()),
        "dependencies": {n: version(n) for n in ("openai", "httpx2", "jsonschema")},
        "model": "gpt-6-astra", "effort": "high", "max_attempts": 144,
        "deadline_seconds": 300, "minimum_remaining_percent": 10,
        "extra_spending": 0, "automatic_retry": False, "automatic_resume": False}


def approval_template(config):
    return {"configuration_hash": digest(config), "run_authorised": False,
            "protocol_accepted": False, "approval_reference": None, "expires_at": None}


def validate_approval(approval, config):
    require(set(approval) == set(approval_template(config)), "Unexpected approval fields")
    require(approval["configuration_hash"] == digest(config), "Approval binding mismatch")
    require(approval["run_authorised"] is True and approval["protocol_accepted"] is True, "Approval still pending")
    require(isinstance(approval["approval_reference"], str) and approval["approval_reference"].strip(), "Approval reference required")
    expires = datetime.fromisoformat(approval["expires_at"])
    require(expires.tzinfo is not None and datetime.now(timezone.utc) < expires, "Approval expired")


def account_observation(raw, scheduled_id):
    """Normalise a fresh app tool response; retain its raw record separately."""
    limits = raw.get("rateLimitsByLimitId", {}).get("codex") or raw.get("rateLimits")
    require(limits and limits.get("limitId") == "codex", "Core limits unavailable")
    windows = [limits[k]["usedPercent"] for k in ("primary", "secondary") if limits.get(k) is not None]
    require(bool(windows) and all(type(v) in (int, float) and 0 <= v <= 100 for v in windows), "Invalid core window")
    credits = limits.get("credits") or {}
    return {"observed_at": time.time(), "scheduled_id": scheduled_id,
            "source": "codex_app.get_usage_limits", "source_hash": digest(raw),
            "public_probe_only": False, "ordinary_usage_allowed": raw.get("ordinaryUsageAllowed"),
            "remaining_percent": min(100 - v for v in windows), "core_used_percent": windows,
            "has_credits": credits.get("hasCredits"), "credits_balance": credits.get("balance"),
            "account_id": raw.get("accountId")}


class SubscriptionBatch:
    """One process and allocation; save every position, stop on first failure."""
    save = QualificationBatch.save

    def __init__(self, bank, folder, config, *, approval_path=None, auth_path=None, simulation_collector=None):
        self.bank = deepcopy(bank)
        self.folder = Path(folder).resolve()
        self.config = deepcopy(config)
        self.simulation = simulation_collector is not None
        self.collector = simulation_collector if self.simulation else run_packet
        self.auth_path = auth_path
        self.approval_path = Path(approval_path) if approval_path else None
        self.approval_raw = self.approval_path.read_bytes() if self.approval_path else None
        self.started = False
        self.lock = threading.Lock()
        require(not self.simulation or auth_path is None, "Simulation cannot receive credentials")
        require(self.simulation or (approval_path is not None and auth_path is not None), "Live approval and login required")
        self.guard()
        self.folder.mkdir(parents=True, exist_ok=False)
        self.save("policy.json", {"configuration": config, "mode": "simulation" if self.simulation else "subscription_qualification",
            "schedule": self.bank.schedule, "approval": strict_json(self.approval_raw) if self.approval_raw else None})
        # Preflight all distinct packets before any attempt, using the collector's exact loader.
        self.packets = {}
        for identifier, item in self.bank.items.items():
            path = self.folder / (identifier + ".packet.json")
            self.save(path.name, item["packet"])
            load_packet(path, digest(item["packet"]))
            self.packets[identifier] = path
        self.events = []

    def guard(self):
        require(not (self.folder / "STOP").exists(), "Operator stop")
        self.bank.verify()
        actual = configuration(self.bank, self.folder, self.config["client_path"], self.config["catalog_path"], self.config["account_id"])
        require(actual == self.config, "Configuration changed")
        if not self.simulation:
            require(self.approval_path.read_bytes() == self.approval_raw, "Approval changed or revoked")
            validate_approval(strict_json(self.approval_raw), self.config)

    def event(self, kind, **data):
        row = {"index": len(self.events), "kind": kind,
               "previous": self.events[-1]["hash"] if self.events else None, **data}
        row["hash"] = digest(row)
        self.save(f"event-{len(self.events):04}.json", row)
        self.events.append(row)

    def run(self, observe_account):
        require(self.lock.acquire(blocking=False), "Concurrent execution denied")
        try:
            require(not self.started, "Allocation already used")
            self.started = True
            outcomes, seen_sessions = [], set()
            stop = None
            attempts = input_tokens = output_tokens = 0
            prior_finished_at = 0
            for index, row in enumerate(self.bank.schedule):
                if stop is not None:
                    outcomes.append({**row, "status": "not_run", "cause": stop})
                    continue
                attempted = False
                try:
                    self.guard()
                    observation = observe_account(deepcopy(row))
                    self.save(f"account-{index+1:03}.json", observation)
                    require(observation["scheduled_id"] == row["id"] and observation["account_id"] == self.config["account_id"], "Account position mismatch")
                    require(prior_finished_at <= observation["observed_at"] <= time.time()
                            and time.time() - observation["observed_at"] <= 120, "Fresh observation required")
                    require(observation.get("source") == "codex_app.get_usage_limits"
                            and observation.get("public_probe_only") is False, "Account evidence source required")
                    require(observation["ordinary_usage_allowed"] is True and observation["remaining_percent"] > 10
                            and observation["has_credits"] is False and observation["credits_balance"] == "0", "Allowance unavailable or uncertain")
                    self.guard()
                    item = self.bank.items[row["item_id"]]
                    attempt_folder = self.folder / f"attempt-{index+1:03}"
                    permit = {"packet_hash": digest(item["packet"]), "output_path": str(attempt_folder),
                        "allocation_hash": digest(self.config), "approval_reference": "simulation" if self.simulation else strict_json(self.approval_raw)["approval_reference"]}
                    self.event("reserved", scheduled=row, packet_hash=permit["packet_hash"])
                    attempted = True
                    attempts += 1
                    result = self.collector(self.packets[row["item_id"]], permit["packet_hash"], attempt_folder,
                        self.config["client_path"], self.config["catalog_path"], auth_path=self.auth_path,
                        account_observation=observation, deadline=300, qualification_permit=permit, dispatch_guard=self.guard)
                    self.guard()
                    answer = strict_json((attempt_folder / "first-answer.txt").read_bytes())
                    validate_answer(answer, item["packet"])
                    require(result["status"] == "structurally_valid" and result["role"] == row["role"]
                            and result["answer_hash"] == digest(answer), "Collector identity mismatch")
                    require(result["thread_id"] not in seen_sessions, "Session reused")
                    seen_sessions.add(result["thread_id"])
                    require(all(type(result["usage"].get(k)) is int and result["usage"][k] >= 0 for k in ("input_tokens", "output_tokens")), "Unknown usage")
                    input_tokens += result["usage"]["input_tokens"]
                    output_tokens += result["usage"]["output_tokens"]
                    self.save(f"answer-{index+1:03}.json", {"response": answer, "collection": result})
                    outcomes.append({**row, "status": "structurally_valid", "cause": None, "usage_known": True})
                    self.event("outcome", outcome=outcomes[-1])
                    prior_finished_at = time.time()
                except Exception as exc:
                    stop = str(exc)
                    outcomes.append({**row, "status": "failed" if attempted else "not_run", "cause": stop, "usage_known": False})
                    self.event("stopped", outcome=outcomes[-1], attempted=attempted)
            summary = {"mode": "simulation" if self.simulation else "subscription_qualification", "qualified": False,
                "scheduled": len(self.bank.schedule), "collector_attempts": attempts,
                "model_calls": 0 if self.simulation else None, "model_call_note": "Client attempts do not prove backend request count.",
                "counts": dict(Counter(r["status"] for r in outcomes)), "outcomes": outcomes, "stop": stop,
                "known_input_tokens": input_tokens, "known_output_tokens": output_tokens,
                "failed_attempt_usage": "unknown; inspect retained events" if stop and any(r["status"] == "failed" for r in outcomes) else None,
                "semantic_assessment": "not started", "additional_spending_authorised": 0}
            self.save("summary.json", summary)
            # Generated caches are not research records. Copied credentials must be gone.
            # Commit the explicit records, not the profile databases (which may be open).
            files = {}
            for p in self.folder.rglob("*"):
                require(not p.is_symlink() and not getattr(p, "is_junction", lambda: False)(), "Collection link denied")
                if not p.is_file():
                    continue
                rel = p.relative_to(self.folder)
                if "home" in rel.parts and p.name not in ("config.toml", "hooks.json"):
                    require(p.name != "auth.json", "Copied login remains")
                    continue
                files[rel.as_posix()] = sha(p)
            self.save("collection-freeze.json", {"version": "subscription-collection-v1", "files": files, "semantic_scoring": "not started"})
            return summary
        finally:
            self.lock.release()


def exchange_observation(directory, row, guard):
    """The supervising Codex task supplies a fresh app-tool result for each ID.

    No account polling API, model call or browser automation runs in this process.
    The supervisor writes the response atomically after receiving the request.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    requested_at = time.time()
    request = directory / (row["id"] + ".request.json")
    with request.open("xb") as stream:
        stream.write(wire({"scheduled_id": row["id"], "requested_at": requested_at}))
    print(wire({"account_check_requested": row["id"], "exchange_directory": str(directory)}).decode(), flush=True)
    response = directory / (row["id"] + ".response.json")
    while not response.exists():
        guard()
        require(time.time() - requested_at <= 120, "Account observer timeout")
        time.sleep(.25)
    envelope = strict_json(response.read_bytes())
    require(envelope["scheduled_id"] == row["id"] and requested_at <= envelope["observed_at"] <= time.time(), "Old account receipt")
    observation = account_observation(envelope["raw"], row["id"])
    observation["observed_at"] = envelope["observed_at"]
    return observation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "execute"))
    for name in ("bank", "freeze", "freeze-sha256", "output", "client", "catalog", "account-id", "prepared"):
        parser.add_argument("--" + name, required=True)
    for name in ("approval", "auth", "observations"):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    bank = load_bank(args.bank, args.freeze, args.freeze_sha256)
    config = configuration(bank, args.output, args.client, args.catalog, args.account_id)
    prepared = Path(args.prepared)
    if args.mode == "prepare":
        # Preflight in memory; no client or account connection is opened.
        with prepared.open("xb") as stream:
            stream.write(wire({"configuration": config, "approval_template": approval_template(config)}))
        print("Prepared allocation; approval remains false. No model calls.")
    else:
        require(all((args.approval, args.auth, args.observations)), "Approval, login and account observation exchange required")
        require(strict_json(prepared.read_bytes())["configuration"] == config, "Prepared configuration changed")
        b = SubscriptionBatch(bank, args.output, config, approval_path=args.approval, auth_path=args.auth)
        result = b.run(lambda row: exchange_observation(args.observations, row, b.guard))
        print(wire({"counts": result["counts"], "stop": result["stop"], "qualified": False}).decode())


if __name__ == "__main__":
    main()
