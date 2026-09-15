"""Transfer integrity tests use temporary artificial files, not private evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("private_evidence", Path(__file__).with_name("private-evidence.py"))
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class TransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "record.json").write_bytes(b'{"value":1}\r\n')

    def freeze(self):
        manifest = evidence.inventory(self.root)
        (self.root / evidence.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        return manifest

    def test_exact_bytes_and_exclusions(self):
        (self.root / "auth.json").write_text("not for transfer")
        (self.root / "state.sqlite").write_text("temporary database")
        manifest = self.freeze()
        self.assertEqual(set(manifest["files"]), {"record.json"})
        self.assertEqual(evidence.verify(self.root)["verified_files"], 1)

    def test_even_line_ending_changes_fail(self):
        self.freeze()
        (self.root / "record.json").write_bytes(b'{"value":1}\n')
        self.assertRaises(ValueError, evidence.verify, self.root)

    def test_missing_file_fails(self):
        self.freeze()
        (self.root / "record.json").unlink()
        self.assertRaises(ValueError, evidence.verify, self.root)

    def test_secret_marker_stops_snapshot(self):
        (self.root / "record.json").write_text("-----BEGIN PRIVATE KEY-----")
        self.assertRaises(ValueError, evidence.inventory, self.root)

    def test_path_outside_root_fails(self):
        manifest = self.freeze()
        manifest["files"] = {"../outside": {"bytes": 0, "sha256": "0" * 64}}
        (self.root / evidence.MANIFEST).write_text(json.dumps(manifest))
        self.assertRaises(ValueError, evidence.verify, self.root)


if __name__ == "__main__":
    unittest.main()
