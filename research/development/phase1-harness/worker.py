"""Trusted replay worker. Returns supplied scripts, never judges their truth."""
import hashlib
import json
import os
from pathlib import Path
import socket
import sys

MAX_INPUT = 8_000_000
raw = sys.stdin.buffer.read(MAX_INPUT + 1)
if len(raw) > MAX_INPUT:
    raise ValueError("Input limit exceeded")
message = json.loads(raw)
packet = message["packet"]
assert message["mode"] == "scripted-development"
reads = []
for name in message.get("reads", []):
    item = packet["sources"]["files"].get(name)
    reads.append({"path": name, "allowed": item is not None,
                  "sha256": hashlib.sha256(item["text"].encode()).hexdigest() if item else None})
if message.get("probe_boundary"):
    def write_blocked(path):
        try:
            Path(path).write_text("boundary probe")
            return False
        except OSError:
            return True
    def connect_blocked():
        try:
            with socket.create_connection(("1.1.1.1", 443), timeout=1):
                return False
        except OSError:
            return True
    response = {
        "uid": os.getuid(), "root_write_denied": write_blocked("/forbidden"),
        "worker_write_denied": write_blocked("/app/worker.py"),
        "network_connect_denied": connect_blocked(),
        "docker_socket_absent": not Path("/var/run/docker.sock").exists(),
        "reference_absent": "reference" not in packet,
        "project_state_absent": not Path("/workspace/PROJECT_STATE.md").exists(),
        "fresh_marker_absent": not Path("/tmp/prior-role").exists(),
    }
    Path("/tmp/prior-role").write_text("freshness probe")
else:
    response = message["response"]
print(json.dumps({"response": response, "reads": reads}))
