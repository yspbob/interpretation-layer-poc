"""Run controller/SDK checks with no network and retain a reproducible summary."""
from copy import deepcopy
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

import httpx2 as httpx

from fixtures import scenarios
from harness import Controller, digest, require, wire
from provider import Provider, Settings, strict_json
from run import HERE, ROOT, packs, read
from test_provider import response_record


def replay_handler(fixture, requests):
    drafts, reviews, assessments = fixture
    counts = {"drafter": 0, "verifier": 0, "guidance_assessor": 0, "verifier_assessor": 0}

    def handler(request):
        body = strict_json(request.content)
        packet = strict_json(body["input"][0]["content"])
        role = packet["role"]
        index = counts[role]
        counts[role] += 1
        if role == "drafter":
            answer = deepcopy(drafts[index])
        elif role == "verifier":
            answer = deepcopy(reviews[index])
        elif role == "guidance_assessor":
            answer = deepcopy(assessments["original" if index == 0 else "released"])
            answer["candidate_hash"] = packet["candidate_hash"]
        else:
            answer = deepcopy(assessments["reviews"][index])
            answer["review_hash"] = packet["review_hash"]
        requests.append({"role": role, "hash": digest(body), "packet": packet})
        return httpx.Response(200, json=response_record(answer),
                              headers={"x-request-id": f"req_simulated_{len(requests)}"})
    return handler


def main():
    folder = ROOT / "local-runs/provider-checks" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    folder.mkdir(parents=True)
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    (folder / "tests.txt").write_text(log.getvalue(), encoding="utf-8")
    print(f"Tests: {result.testsRun}; failures: {len(result.failures)}; errors: {len(result.errors)}", flush=True)
    require(result.wasSuccessful(), "Controller or adapter checks failed; inspect local tests.txt")
    report = {"status": "SDK and workflow simulation; no real provider contacted",
              "model_calls": 0, "tests": {"passed": result.testsRun, "failed": 0,
                "names": [line.split(" ... ")[0] for line in log.getvalue().splitlines() if line.endswith(" ... ok")]},
              "test_log_hash": hashlib.sha256((folder / "tests.txt").read_bytes()).hexdigest(),
              "platform": platform.platform(), "dependencies": {p: version(p) for p in ["openai", "httpx2", "jsonschema"]},
              "scripts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir()
                          if p.suffix == ".py" or p.name in {"provider-requirements.txt", "provider-lock.txt", "requirements.txt"}},
              "scenarios": []}
    settings = Settings("fixture-model", "low", 2_000_000, 30000, 2, 8, 100_000_000, 12,
                        request_byte_limit=1_500_000)
    source_packs = packs()
    # This patch blocks actual network sockets throughout every SDK scenario.
    with patch("socket.socket.connect", side_effect=AssertionError("Unexpected socket connection")):
        for case, sources in source_packs.items():
            reference = read(HERE / ("netbox-reference.json" if case == "netbox" else "h06-reference.json"))
            fixtures = scenarios(sources, reference)
            if case == "h06":
                fixtures = {"supported": fixtures["supported"]}
            for label, fixture in fixtures.items():
                directory = folder / f"{case}-{label}"
                requests = []
                connection = Provider(settings, sources, reference, directory / "connection",
                                      mock_handler=replay_handler(fixture, requests))
                controller = Controller(sources, reference, connection, directory / "attempt")
                outcome = controller.run()
                expected = {"exhausted": "revision_exhausted", "unresolved": "unresolved"}.get(label, "frozen")
                require(outcome["status"] == expected, f"Unexpected workflow result for {case}/{label}: {outcome}")
                require(outcome["scores"]["released"]["verdict"] == ("pass" if label in {"supported", "corrected"} else "fail"),
                        "Independent assessment outcome changed")
                for request in requests:
                    packet = request["packet"]
                    require(digest(packet["sources"]) == digest(sources), "Source mismatch")
                    if request["role"] in {"drafter", "verifier"}:
                        require("reference" not in packet, "Reference disclosure")
                require(outcome["provider_summary"]["reserved_nusd"] == 0, "Unsettled successful simulation")
                report["scenarios"].append({"case": case, "scenario": label, "outcome": outcome,
                    "source_hash": digest(sources), "reference_hash": digest(reference),
                    "requests": [{"role": r["role"], "hash": r["hash"]} for r in requests]})
                print(f"{case}/{label}: {outcome['status']}; {len(requests)} simulated SDK requests", flush=True)
    report["simulated_requests"] = sum(len(s["requests"]) for s in report["scenarios"])
    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    report["limitations"] = ["All answers and token usage were authored; no model quality or real prices measured",
        "No live endpoint, credential, data retention or model compatibility check",
        "Input token ceiling and rates must be verified for selected live model",
        "No arbitrary code execution or new container qualification"]
    (folder / "report.json").write_bytes(wire(report))
    print(f"Report: {folder / 'report.json'}")


if __name__ == "__main__":
    main()
