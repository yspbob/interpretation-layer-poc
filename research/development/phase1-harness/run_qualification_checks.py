"""Offline rehearsal only. No credentials, live switch, or answer key input."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import io
import json
from pathlib import Path
import platform
import unittest
from unittest.mock import patch
import uuid

from harness import require, wire
from provider import Settings, httpx, strict_json
from qualification_batch import QualificationBatch, load_bank
from test_provider import response_record
from test_qualification_batch import synthetic_answer, synthetic_bank

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path)
    parser.add_argument("--freeze", default="freeze-v3.json")
    parser.add_argument("--freeze-sha256")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.bank:
        require(args.freeze_sha256 and args.output, "Private rehearsal needs a freeze commitment and protected output folder")
        require(not args.output.resolve().is_relative_to(ROOT), "Private bank output must stay outside the public repository")
        require(not args.bank.resolve().is_relative_to(ROOT), "Private bank must stay outside the public repository")
    else:
        require(args.freeze_sha256 is None, "A freeze commitment requires a bank")
    folder = args.output or ROOT / "local-runs/batch-checks" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    folder.mkdir(parents=True, exist_ok=False)
    test_count = 0
    if not args.bank:
        suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
        log = io.StringIO()
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
        (folder / "tests.txt").write_text(log.getvalue(), encoding="utf-8")
        require(result.wasSuccessful(), "Offline unit tests failed; inspect tests.txt")
        test_count = result.testsRun
        freeze_hash = synthetic_bank(folder / "synthetic-bank")
        bank = load_bank(folder / "synthetic-bank", "freeze.json", freeze_hash)
    else:
        bank = load_bank(args.bank, args.freeze, args.freeze_sha256)
    settings = Settings("fixture-model", "low", 32768, 8192, 1, 2, 20_000_000, 12)
    requests = []

    def handler(request):
        body = strict_json(request.content)
        packet = strict_json(body["input"][0]["content"])
        expected = bank.items[bank.schedule[len(requests)]["item_id"]]
        require(packet == expected["packet"], "Wrong packet or dispatch order")
        require(body["instructions"] == expected["instruction"], "Wrong role instruction")
        require(set(body["input"][0]) == {"role", "content"} and len(body["input"]) == 1,
                "Unexpected input history")
        require("previous_response_id" not in body and "conversation" not in body and body["tools"] == [],
                "Unexpected shared history or tools")
        requests.append({"bytes": len(request.content), "role": packet["role"],
                         "sha256": hashlib.sha256(request.content).hexdigest()})
        return httpx.Response(200, json=response_record(synthetic_answer(packet)))

    with patch("socket.socket.connect", side_effect=AssertionError("Network denied")), \
         patch("provider.httpx.HTTPTransport", side_effect=AssertionError("Live transport denied")):
        batch = QualificationBatch(bank, settings, folder / "batch", mock_handler=handler)
        result = batch.run()
    require(result["counts"] == {"structurally_valid": 144} and len(requests) == 144,
            "Fixed schedule rehearsal incomplete")
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "mode": "provider-simulation",
              "bank_kind": "private_frozen_inputs" if args.bank else "public_synthetic_inputs",
              "tests_passed": test_count, "scheduled": 144, "simulated_sdk_requests": len(requests),
              "qualification_model_calls": 0, "experimental_guidance_runs": 0,
              "qualified": False, "semantic_assessment": "not performed",
              "max_encoded_request_bytes": max(r["bytes"] for r in requests),
              "charged_nusd_simulated": result["charged_nusd"], "held_nusd": result["held_nusd"],
              "freeze_hash": bank.freeze_hash, "material_hash": bank.material_hash,
              "python": platform.python_version(), "platform": platform.system(),
              "dependencies": {n: version(n) for n in ("openai", "httpx2", "jsonschema")},
              "source_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in HERE.glob("*.py")},
              "limits": ["Local simulated responses, not verified provider behaviour or billing.",
                         "No scoring key was loaded. Synthetic responses are not qualification answers.",
                         "No automatic recovery from process termination or permission to start a new paid batch."]}
    (folder / "check-summary.json").write_bytes(wire(report))
    print(json.dumps({k: report[k] for k in ("bank_kind", "tests_passed", "simulated_sdk_requests",
                                            "qualification_model_calls", "max_encoded_request_bytes")}))
    print("Protected check record:", folder)


if __name__ == "__main__":
    main()
