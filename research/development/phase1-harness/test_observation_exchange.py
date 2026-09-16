"""Artificial account handoffs only: no client process, credentials or network."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from harness import wire
from subscription_batch import exchange_observation


class ObservationExchangeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.now = 1000.0
        self.monotonic = 0.0
        self.pending = None
        self.deliver_at = 1.0
        self.guard_count = 0
        self.receipt_change = lambda receipt: receipt
        self.addCleanup(patch.stopall)
        patch("subscription_batch.time", SimpleNamespace(
            time=lambda: self.now, monotonic=lambda: self.monotonic,
            sleep=self.advance)).start()
        patch("subprocess.Popen", side_effect=AssertionError("Process forbidden")).start()
        patch("socket.socket.connect", side_effect=AssertionError("Network forbidden")).start()

    def guard(self):
        self.guard_count += 1

    def deliver(self):
        row = json.loads(self.pending.read_bytes())
        receipt = {"scheduled_id": row["scheduled_id"], "observed_at": self.now,
                   "raw": {"ordinaryUsageAllowed": True, "accountId": "artificial",
                           "rateLimits": {"limitId": "codex",
                                          "primary": {"usedPercent": 20},
                                          "credits": {"hasCredits": False, "balance": "0"}}}}
        response = self.pending.with_name(self.pending.name.replace(".request.", ".response."))
        temporary = response.with_suffix(".tmp")
        temporary.write_bytes(wire(self.receipt_change(receipt)))
        temporary.rename(response)

    def advance(self, seconds):
        self.now += seconds
        self.monotonic += seconds
        if self.deliver_at is not None and self.monotonic >= self.deliver_at:
            self.deliver()
            self.deliver_at = None

    def exchange(self, identifier="S", guard=None):
        self.pending = self.root / (identifier + ".request.json")
        with redirect_stdout(io.StringIO()):
            return exchange_observation(self.root, {"id": identifier}, guard or self.guard)

    def test_144_sequential_fresh_handoffs(self):
        ids = []
        for position in range(144):
            identifier = f"S{position:03}"
            self.deliver_at = self.monotonic + 1
            receipt = self.exchange(identifier)
            ids.append(receipt["scheduled_id"])
            self.assertEqual(receipt["observed_at"], self.now)
            self.assertEqual(receipt["remaining_percent"], 80)
            self.advance(2)  # Artificial collection time; no model call.
        self.assertEqual(len(set(ids)), 144)
        self.assertEqual(len(list(self.root.glob("*.request.json"))), 144)
        self.assertEqual(len(list(self.root.glob("*.response.json"))), 144)

    def test_missing_receipt_times_out_without_waiting_in_real_time(self):
        self.deliver_at = None
        with self.assertRaisesRegex(ValueError, "Account observer timeout"):
            self.exchange()
        self.assertLessEqual(self.monotonic, 120.25)

    def test_receipt_at_deadline_is_accepted(self):
        self.deliver_at = 120
        self.assertEqual(self.exchange()["scheduled_id"], "S")

    def test_receipt_after_deadline_is_rejected(self):
        self.deliver_at = 120.25
        with self.assertRaisesRegex(ValueError, "Account observer timeout"):
            self.exchange()

    def test_old_observation_is_rejected(self):
        self.receipt_change = lambda r: {**r, "observed_at": 999}
        with self.assertRaisesRegex(ValueError, "Old account receipt"):
            self.exchange()

    def test_future_observation_is_rejected(self):
        self.receipt_change = lambda r: {**r, "observed_at": self.now + 1}
        with self.assertRaisesRegex(ValueError, "Old account receipt"):
            self.exchange()

    def test_wrong_position_is_rejected(self):
        self.receipt_change = lambda r: {**r, "scheduled_id": "different"}
        with self.assertRaisesRegex(ValueError, "Old account receipt"):
            self.exchange()

    def test_duplicate_request_cannot_resume(self):
        self.exchange()
        with self.assertRaises(FileExistsError):
            self.exchange()

    def test_stop_is_checked_even_when_receipt_is_ready(self):
        self.pending = self.root / "S.request.json"
        self.pending.write_bytes(wire({"scheduled_id": "S", "requested_at": self.now}))
        self.deliver()
        self.pending.unlink()
        def stopped():
            raise ValueError("Operator stop")
        with self.assertRaisesRegex(ValueError, "Operator stop"):
            self.exchange(guard=stopped)

    def test_clock_rollback_does_not_extend_timeout(self):
        self.deliver_at = None
        def rollback(seconds):
            self.monotonic += seconds
            self.now -= seconds
            if self.monotonic > 121:
                raise AssertionError("Wall clock rollback bypassed the deadline")
        with patch("subscription_batch.time.sleep", side_effect=rollback):
            with self.assertRaisesRegex(ValueError, "Account observer timeout"):
                self.exchange()

    def test_receipt_read_crossing_deadline_is_rejected(self):
        self.deliver_at = 119.75
        original = Path.read_bytes
        def slow_read(path):
            data = original(path)
            if path.name.endswith(".response.json"):
                self.now += 1
                self.monotonic += 1
            return data
        with patch.object(Path, "read_bytes", slow_read):
            with self.assertRaisesRegex(ValueError, "Account observer timeout"):
                self.exchange()


if __name__ == "__main__":
    unittest.main()
