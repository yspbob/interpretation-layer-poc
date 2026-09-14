"""Fixed qualification schedule with a shared ledger. Simulation only for now.

No answer key is loaded and no semantic verdict is inferred from schema validity.
The provider adapter owns request construction and each fresh SDK connection.
"""
from collections import Counter
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import threading
from types import SimpleNamespace

from harness import (MAX_INPUT, assess_guidance, digest, ids, refs_valid, require,
                     validate_draft, validate_review, wire)
from provider import PROMPTS, SCHEMAS, Provider, Settings, strict_json
from schemas import validate

ROLES = ("verifier", "guidance_assessor", "verifier_assessor")
SAFE_ID = re.compile(r"[A-Za-z0-9_]{1,80}\Z")


def read_confined(root, name):
    require(isinstance(name, str) and "\\" not in name and ":" not in name,
            "Invalid bank path")
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and ".." not in relative.parts
            and str(relative) == name, "Invalid bank path")
    path = root.joinpath(*relative.parts)
    require(path.resolve(strict=True).is_relative_to(root), "Bank path escaped root")
    for part in [path, *path.parents]:
        if part == root:
            break
        require(not part.is_symlink() and not getattr(part, "is_junction", lambda: False)(),
                "Bank link denied")
    require(path.stat().st_size <= MAX_INPUT, "Bank file too large")
    with path.open("rb") as stream:
        raw = stream.read(MAX_INPUT + 1)
    require(len(raw) <= MAX_INPUT, "Bank file too large")
    return raw


@dataclass(frozen=True)
class Bank:
    items: dict
    schedule: list
    freeze_hash: str
    material_hash: str

    def verify(self):
        require(digest({"items": self.items, "schedule": self.schedule}) == self.material_hash,
                "Bank changed after loading")


def load_bank(folder, freeze_name, expected_freeze_hash):
    """Read only frozen input files; never open scoring keys or investigator notes."""
    root = Path(folder).resolve(strict=True)
    raw = read_confined(root, freeze_name)
    require(hashlib.sha256(raw).hexdigest() == expected_freeze_hash, "Freeze mismatch")
    manifest = strict_json(raw)
    active = manifest["active_bank"]
    require(SAFE_ID.fullmatch(active.replace("-", "_")) is not None, "Invalid bank name")

    def frozen(name):
        raw = read_confined(root, name)
        require(hashlib.sha256(raw).hexdigest() == manifest["files"].get(name),
                "Frozen input mismatch")
        return strict_json(raw)

    schedule = frozen(f"{active}/schedule.json")
    require(isinstance(schedule, list) and len(schedule) == 144, "Expected fixed 144 call schedule")
    cases = set()
    for row in schedule:
        require(isinstance(row, dict) and set(row) == {"id", "item_id", "role", "case", "repetition"},
                "Unexpected schedule fields")
        for key in ("id", "item_id", "case"):
            require(isinstance(row[key], str) and SAFE_ID.fullmatch(row[key]), "Invalid schedule identifier")
        require(row["role"] in ROLES and type(row["repetition"]) is int
                and row["repetition"] in (1, 2), "Invalid schedule role or repetition")
        cases.add(row["case"])
    require(len(cases) == 4 and len(ids(schedule, "id")) == 144, "Wrong family or call count")
    items = {}
    for case in sorted(cases):
        prefix = f"{active}/{case}"
        sources, reference = frozen(prefix + "/sources.json"), frozen(prefix + "/reference.json")
        require(frozen(prefix + "/role-prompts.json") == {r: PROMPTS[r] for r in ROLES},
                "Frozen role prompts differ from runtime")
        require(len(reference["units"]) > 0, "Empty reference scope")
        ids(reference["units"], "id")
        for source in sources["files"].values():
            require(hashlib.sha256(source["text"].encode()).hexdigest() == source["sha256"],
                    "Source text hash mismatch")
        for unit in reference["units"]:
            refs_valid(unit.get("evidence", []), sources)
        case_items = frozen(prefix + "/items.json")
        require(len(case_items) == 18, "Expected eighteen items per family")
        require(Counter(i["role"] for i in case_items) == {r: 6 for r in ROLES}, "Wrong role balance")
        for item in case_items:
            require(set(item) == {"id", "role", "instruction", "packet", "response_schema"},
                    "Unexpected item fields")
            require(isinstance(item["id"], str) and SAFE_ID.fullmatch(item["id"])
                    and item["id"] not in items, "Invalid or duplicate item")
            role, packet = item["role"], item["packet"]
            require(packet["role"] == role and item["instruction"] == PROMPTS[role]
                    and item["response_schema"] == SCHEMAS[role], "Role contract changed")
            require(packet["sources"] == sources, "Item source mismatch")
            require(("reference" in packet) == (role != "verifier"), "Wrong reference access")
            if role != "verifier":
                require(packet["reference"] == reference, "Item reference mismatch")
            draft = packet["submission"]["draft"] if role == "verifier_assessor" else packet["candidate"]
            validate_draft(draft, sources)
            if role == "verifier_assessor":
                validate_review(packet["submission"]["review"], draft, sources)
            items[item["id"]] = {"case": case, **item}
    require(len(items) == 72, "Wrong total item count")
    for row in schedule:
        require(row["item_id"] in items, "Unknown scheduled item")
        item = items[row["item_id"]]
        require((row["case"], row["role"]) == (item["case"], item["role"]), "Schedule metadata mismatch")
    for item_id in items:
        require(sorted(r["repetition"] for r in schedule if r["item_id"] == item_id) == [1, 2],
                "Missing or duplicated repetition")
    material = {"items": items, "schedule": schedule}
    return Bank(items, schedule, expected_freeze_hash, digest(material))


def validate_answer(answer, packet):
    role = packet["role"]
    validate(answer, SCHEMAS[role])
    if role == "verifier":
        validate_review(answer, packet["candidate"], packet["sources"])
    elif role == "guidance_assessor":
        # This checks identity and coverage IDs; discard its semantic aggregation.
        assess_guidance(answer, packet["candidate"], packet["reference"])
    else:
        require(answer["review_hash"] == packet["review_hash"], "Wrong assessed submission")
        require(ids(answer["decisions"], "claim_id") == ids(packet["submission"]["draft"]["claims"], "id"),
                "Assessment must address exactly the submitted claims")


class QualificationBatch:
    """One immutable schedule, one output folder, no resume or automatic retries.

    Only a supplied local response handler is accepted. A live entry point and
    its protocol/account approval binding must be reviewed separately.
    """
    def __init__(self, bank, settings, folder, *, mock_handler):
        require(callable(mock_handler), "A local simulation handler is required")
        bank.verify()
        settings.validate()
        self.bank, self.settings = deepcopy(bank), settings
        self.reserve = (settings.max_input_tokens * settings.input_nusd_per_token
                        + settings.max_output_tokens * settings.output_nusd_per_token)
        self.attempt_settings = replace(settings, max_calls=1, budget_nusd=self.reserve)
        self.handler = lambda request: mock_handler(request)  # Always truthy: MockTransport only.
        self.folder = Path(folder)
        self.lock = threading.Lock()
        self.started = False
        self.charged = self.held = 0
        self.events, self.outcomes = [], []
        # Validate every outgoing packet and bound before creating a batch or dispatching.
        for item in self.bank.items.values():
            p = item["packet"]
            adapter = SimpleNamespace(settings=self.attempt_settings, mode="provider-simulation",
                bound_run="qualification", calls=0, prompts=PROMPTS, schemas=SCHEMAS,
                source_hash=digest(p["sources"]), reference_hash=digest(p.get("reference")))
            Provider.request(adapter, self.message(item))
        self.folder.mkdir(parents=True, exist_ok=False)
        self.save("policy.json", {"mode": "provider-simulation", "settings": asdict(settings),
            "freeze_hash": bank.freeze_hash, "material_hash": bank.material_hash,
            "schedule": bank.schedule, "reserve_per_attempt_nusd": self.reserve,
            "role_prompts": PROMPTS, "schemas": SCHEMAS,
            "runtime_hashes": {n: hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest()
                               for n in ("qualification_batch.py", "provider.py", "harness.py", "schemas.py")},
            "semantic_assessment": "pending; structural acceptance is not a correct verdict",
            "restart": "Existing folders cannot be reused. No automatic resume or retry."})

    def message(self, item):
        return {"mode": "provider-simulation", "packet": deepcopy(item["packet"]),
                "instruction": item["instruction"], "run_id": "qualification", "call_id": 1}

    def save(self, name, value):
        with (self.folder / name).open("xb") as stream:
            stream.write(wire(value))
            stream.flush()
            os.fsync(stream.fileno())

    def event(self, kind, **data):
        row = {"index": len(self.events), "kind": kind, "charged_nusd": self.charged,
               "held_nusd": self.held, "previous": self.events[-1]["hash"] if self.events else None, **data}
        row["hash"] = digest(row)
        self.save(f"event-{row['index']:04}.json", row)
        self.events.append(row)

    def run(self):
        require(self.lock.acquire(blocking=False), "Concurrent batch run denied")
        try:
            require(not self.started, "Batch already used")
            self.started = True
            self.bank.verify()
            stop, interrupt = None, None
            for index, row in enumerate(self.bank.schedule):
                if stop is None and self.charged + self.held + self.reserve > self.settings.budget_nusd:
                    stop = "budget_exhausted"
                if stop is not None:
                    self.outcomes.append({**row, "status": "not_run", "cause": stop})
                    continue
                item = self.bank.items[row["item_id"]]
                self.held += self.reserve
                self.event("reserved", scheduled=row, packet_hash=digest(item["packet"]), reserve_nusd=self.reserve)
                connection = None
                try:
                    packet = item["packet"]
                    connection = Provider(self.attempt_settings, packet["sources"], packet.get("reference"),
                        self.folder / f"attempt-{index + 1:03}", mock_handler=self.handler)
                    connection.bind("qualification")
                    response = connection.call(self.message(item))
                    validate_answer(response["response"], packet)
                    self.save(f"answer-{index + 1:03}.json", response)
                    connection.finish()
                    status, cause = "structurally_valid", None
                except BaseException as error:
                    status, cause = "failed", type(error).__name__
                    if isinstance(error, OSError):
                        stop = "recording_failed"
                    if not isinstance(error, Exception):
                        interrupt, stop = error, "interrupted"
                # No release on unknown usage, even if a failed call might have cost nothing.
                known = (connection is not None and connection.last_record is not None
                         and connection.held == 0)
                if known:
                    self.charged += connection.charged
                    self.held -= self.reserve
                else:
                    stop = stop or "usage_uncertain"
                self.outcomes.append({**row, "status": status, "cause": cause,
                                      "usage_known": known, "semantic_assessment": "pending"})
                self.event("outcome", outcome=self.outcomes[-1])
            summary = {"mode": "provider-simulation", "model_calls": 0, "qualified": False,
                       "scheduled": len(self.bank.schedule), "outcomes": self.outcomes,
                       "counts": dict(Counter(r["status"] for r in self.outcomes)), "stop": stop,
                       "charged_nusd": self.charged, "held_nusd": self.held,
                       "budget_nusd": self.settings.budget_nusd, "price_basis": "simulated",
                       "semantic_assessment": "pending"}
            self.save("summary.json", summary)
            if interrupt is not None:
                raise interrupt
            return summary
        finally:
            self.lock.release()
