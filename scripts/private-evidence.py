"""Snapshot or verify private evidence bytes. Never prints evidence contents."""
import argparse
import hashlib
import json
from pathlib import Path
import re

MANIFEST = "TRANSFER_MANIFEST.json"
EXCLUDED_DIRS = {".git", "env", ".venv", "venv", "__pycache__", "node_modules"}
SECRET_PATTERNS = [
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    rb"\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|eyJ[A-Za-z0-9_-]{25,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,})",
    rb'"(?:access_token|refresh_token|id_token|OPENAI_API_KEY|ANTHROPIC_API_KEY)"\s*:\s*"[^"\s]{20,}"',
]


def excluded(path):
    return (bool(set(path.parts) & EXCLUDED_DIRS) or path.name == MANIFEST
            or path.name.lower() == "auth.json" or path.name.startswith(".env")
            or path.suffix.lower() in {".pem", ".key", ".pyc"}
            or any(s in path.name.lower() for s in (".sqlite", ".db-wal", ".db-shm"))
            or path.suffix.lower() == ".db")


def inventory(root):
    files, omitted = {}, []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError("Linked path requires review: " + str(rel))
        if not path.is_file() or ".git" in rel.parts:
            continue
        if excluded(rel):
            if rel.name != MANIFEST:
                omitted.append(rel.as_posix())
            continue
        data = path.read_bytes()
        if any(re.search(pattern, data) for pattern in SECRET_PATTERNS):
            raise ValueError("Possible credential requires local review: " + str(rel))
        files[rel.as_posix()] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    return {"version": 1, "files": files, "excluded_local_files": omitted,
            "note": "Transfer integrity only. Excluded files stay on the source PC. This does not validate model execution on the destination."}


def verify(root):
    manifest = json.loads((root / MANIFEST).read_bytes())
    assert manifest["version"] == 1
    for name, expected in manifest["files"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("Missing or unsafe evidence path: " + name)
        data = path.read_bytes()
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("Evidence bytes changed: " + name)
    return {"verified_files": len(manifest["files"]), "bytes": sum(x["bytes"] for x in manifest["files"].values())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("snapshot", "verify"))
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    if args.mode == "snapshot":
        result = inventory(root)
        (root / MANIFEST).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(verify(root)))
