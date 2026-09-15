"""Explicitly approved, fixed qualification batch. Import and prepare never dispatch."""
import argparse
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import os
from pathlib import Path
import platform
import sys
from types import SimpleNamespace

from harness import CONTRACT, digest, require, wire
from provider import PROMPTS, SCHEMAS, Provider, Settings, httpx, strict_json
from qualification_batch import QualificationBatch, load_bank

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
GATES = ("spending_authorised", "pricing_verified", "input_bound_verified",
         "provider_data_policy_verified", "model_access_verified", "account_verified")


def fingerprint(key):
    require(isinstance(key, str) and bool(key.strip()), "Explicit provider credential required")
    return hashlib.sha256(key.encode()).hexdigest()


def preflight(bank, settings):
    """Build every distinct request without opening a connection or reading a key."""
    records = {}
    for name, item in bank.items.items():
        p = item["packet"]
        adapter = SimpleNamespace(settings=settings, mode="provider-live", bound_run="qualification",
            calls=0, prompts=PROMPTS, schemas=SCHEMAS, source_hash=digest(p["sources"]),
            reference_hash=digest(p.get("reference")))
        body = Provider.request(adapter, {"mode": "provider-live", "packet": p,
            "instruction": item["instruction"], "run_id": "qualification", "call_id": 1})
        encoded = httpx.Request("POST", "https://api.openai.com/v1/responses", json=body).content
        require(len(encoded) <= settings.request_byte_limit and
                len(encoded) + settings.input_padding_tokens <= settings.max_input_tokens,
                "Serialized request exceeds configured allowance")
        records[name] = {"body_hash": digest(body), "encoded_bytes": len(encoded)}
    return {"items": len(records), "request_manifest_hash": digest(records),
            "max_padded_bytes": max(r["encoded_bytes"] for r in records.values()) + settings.input_padding_tokens}


def configuration(bank, settings, output, key_fingerprint, account_label):
    bank.verify()
    settings.validate()
    require(isinstance(key_fingerprint, str) and len(key_fingerprint) == 64
            and all(c in "0123456789abcdef" for c in key_fingerprint), "Credential fingerprint required")
    require(isinstance(account_label, str) and bool(account_label.strip()), "Account record label required")
    files = ("live_qualification.py", "qualification_batch.py", "provider.py", "harness.py", "schemas.py")
    return {"version": "qualification-live-v1", "freeze_hash": bank.freeze_hash,
            "material_hash": bank.material_hash, "scheduled": len(bank.schedule),
            "settings": asdict(settings), "output_path": str(Path(output).resolve()),
            "credential_sha256": key_fingerprint, "account_label": account_label,
            "runtime_hashes": {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in files},
            "scoring_procedure_sha256": hashlib.sha256((HERE / "SCORING-PROCEDURE.md").read_bytes()).hexdigest(),
            "dependencies": {n: version(n) for n in ("openai", "httpx2", "jsonschema")},
            "python": platform.python_version(), "platform": platform.system(),
            "prompts_hash": digest(PROMPTS), "schemas_hash": digest(SCHEMAS),
            "policy": "Fixed schedule, one attempt each, no automatic retry or resume; stop on uncertain usage."}


def approval_template(config):
    return {"configuration_hash": digest(config), "expires_at": None,
            "approval_reference": None, **{gate: False for gate in GATES}}


def validate_approval(approval, config):
    require(isinstance(approval, dict) and set(approval) == {"configuration_hash", "expires_at", "approval_reference", *GATES},
            "Exact batch approval record required")
    require(approval["configuration_hash"] == digest(config), "Approval is for another configuration")
    require(all(approval[g] is True for g in GATES), "Live verification or spending gate is open")
    require(isinstance(approval["approval_reference"], str) and bool(approval["approval_reference"].strip()),
            "User approval reference required")
    require(isinstance(approval["expires_at"], str), "Approval expiry required")
    expires = datetime.fromisoformat(approval["expires_at"])
    require(expires.tzinfo is not None and datetime.now(timezone.utc) < expires, "Batch approval expired")


def commit_collection(folder):
    """Commit a completed or formally stopped collection before semantic scoring."""
    folder = Path(folder)
    require((folder / "summary.json").is_file(), "Collection summary is required before commitment")
    files = {}
    for path in sorted(folder.rglob("*")):
        require(not path.is_symlink() and not getattr(path, "is_junction", lambda: False)(), "Collection link denied")
        if path.is_file():
            files[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    record = {"version": "collection-commitment-v1", "files": files, "semantic_scoring": "not started"}
    with (folder / "collection-freeze.json").open("xb") as stream:
        stream.write(wire(record))
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(wire(record)).hexdigest()


class LiveQualificationBatch(QualificationBatch):
    """Same ledger as simulation, with per-attempt approval and configuration checks."""
    mode = "provider-live"

    def __init__(self, bank, settings, folder, *, approved_config, approval_path, api_key):
        self.api_key = api_key
        self.approved_config = deepcopy(approved_config)
        self.approval_path = Path(approval_path).resolve(strict=True)
        self.approval_raw = self.approval_path.read_bytes()
        self.batch_approval = strict_json(self.approval_raw)
        actual = configuration(bank, settings, folder, fingerprint(api_key), approved_config["account_label"])
        require(actual == approved_config, "Actual batch differs from approved configuration")
        validate_approval(self.batch_approval, actual)
        # Parent performs all packet preflights before creating the output folder.
        super().__init__(bank, settings, folder, mock_handler=lambda request: (_ for _ in ()).throw(
            AssertionError("Simulation connection must not be used by live batch")))
        self.save("live-allocation.json", {"configuration": actual,
            "configuration_hash": digest(actual), "approval": self.batch_approval,
            "approval_sha256": hashlib.sha256(self.approval_raw).hexdigest()})

    def before_attempt(self):
        if (self.folder / "STOP").exists():
            return "operator_stop"
        try:
            require(self.approval_path.read_bytes() == self.approval_raw, "Approval file changed or revoked")
            actual = configuration(self.bank, self.settings, self.folder,
                                   fingerprint(self.api_key), self.approved_config["account_label"])
            require(actual == self.approved_config, "Configuration changed")
            validate_approval(self.batch_approval, actual)
        except (ValueError, OSError, KeyError, TypeError):
            return "approval_or_configuration_changed"
        return None

    def make_connection(self, item, index):
        # Approval is checked again after the durable batch reservation.
        require(self.before_attempt() is None, "Dispatch approval is no longer valid")
        packet = item["packet"]
        folder = self.folder / f"attempt-{index + 1:03}"
        policy = digest({"settings": asdict(self.attempt_settings),
                         "source_hash": digest(packet["sources"]),
                         "reference_hash": digest(packet.get("reference")), "contract": CONTRACT,
                         "ledger_path": str(folder.resolve()), "prompts": PROMPTS, "schemas": SCHEMAS})
        approval = {"policy_hash": policy, "expires_at": self.batch_approval["expires_at"],
                    **{k: self.batch_approval[k] for k in GATES[:4]}}
        return Provider(self.attempt_settings, packet["sources"], packet.get("reference"), folder,
                        api_key=self.api_key, approval=approval)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "execute"))
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--freeze-sha256", required=True)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--account-label")
    parser.add_argument("--credential-sha256")
    args = parser.parse_args()
    # Public checkout paths cannot hold sealed inputs, credentials or captured answers.
    for path in (args.bank, args.output, args.config, args.approval, args.settings):
        require(not path.resolve().is_relative_to(PROJECT), "Live artifacts must be outside the public checkout")
    bank = load_bank(args.bank, args.freeze, args.freeze_sha256)
    settings = Settings(**strict_json(args.settings.read_bytes()))
    if args.mode == "prepare":
        config = configuration(bank, settings, args.output, args.credential_sha256, args.account_label)
        preflight(bank, settings)
        # No credential is read and no network call is possible in prepare mode.
        require(not args.config.exists() and not args.approval.exists() and not args.output.exists(),
                "Preparation files or output folder already exist")
        for path, value in ((args.config, config), (args.approval, approval_template(config))):
            with path.open("xb") as stream:
                stream.write(wire(value))
        print("Configuration prepared; every approval gate is false. No model calls.")
    else:
        config = strict_json(args.config.read_bytes())
        key = os.environ.get("POC_OPENAI_API_KEY")
        batch = LiveQualificationBatch(bank, settings, args.output, approved_config=config,
                                       approval_path=args.approval, api_key=key)
        summary = batch.run()
        commit_collection(args.output)
        print("Batch stopped. Review the private collection and usage records before scoring.")
        return 0 if summary["stop"] is None else 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        # Do not print credentials, provider bodies or private packet contents.
        print(f"Qualification command stopped ({type(error).__name__}). Check the private configuration and records.", file=sys.stderr)
        sys.exit(1)
