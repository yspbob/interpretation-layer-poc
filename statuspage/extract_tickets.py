#!/usr/bin/env python3
"""Deterministic ticket-data extraction for the status page (v2, plan v1.2 F10).
Reads preregistration/selected_tickets.md, the merge commits in a full netbox clone
(FG_UPSTREAM, default /tmp/netbox-up), titles and URLs from data/ticket_universe_raw.json,
and the labelled LLM-written overviews from statuspage/overviews.json. Writes statuspage/tickets.json.
File lists come from `git diff --name-only <merge>^1 <merge>` (first parent): `git show` on a
two-parent merge commit lists nothing, which is what emptied five cards in v1."""
import json, re, subprocess, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONE = os.environ.get("FG_UPSTREAM", "/tmp/netbox-up")
SEL = os.path.join(ROOT, "preregistration", "selected_tickets.md")
OUT = os.path.join(ROOT, "statuspage", "tickets.json")

rows = []
for line in open(SEL, encoding="utf-8-sig"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*#(\d+)\s*\|\s*(\d+)\s*\|\s*([\d-]+)\s*\|\s*([\d-]+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([0-9a-f]{40})\s*\|", line)
    if m:
        rows.append(dict(seq=int(m.group(1)), issue=int(m.group(2)), pr=int(m.group(3)),
                         closed=m.group(4), merged=m.group(5), files=int(m.group(6)),
                         audit=m.group(7), commit=m.group(8)))
assert len(rows) == 25, len(rows)

universe = {i["number"]: i for i in json.load(open(os.path.join(ROOT, "data", "ticket_universe_raw.json"), encoding="utf-8-sig"))}
overviews = json.load(open(os.path.join(ROOT, "statuspage", "overviews.json")))

def sh(args):
    return subprocess.run(args, cwd=CLONE, capture_output=True, text=True, check=True).stdout

for r in rows:
    files = [f for f in sh(["git", "diff", "--name-only", r["commit"] + "^1", r["commit"]]).splitlines() if f]
    assert len(files) == r["files"], (r["issue"], len(files), r["files"])
    title = sh(["git", "show", "--format=%s", "--no-patch", r["commit"]]).strip()
    subs = sorted({f.split("/")[1] for f in files if f.startswith("netbox/") and "/" in f[7:]})
    r["title"] = universe[r["issue"]]["title"] if r["issue"] in universe else title
    r["merge_title"] = title
    r["parent"] = sh(["git", "rev-parse", r["commit"] + "^1"]).strip()
    r["files_list"] = files
    r["subsystems"] = subs
    r["issue_url"] = f"https://github.com/netbox-community/netbox/issues/{r['issue']}"
    r["pr_url"] = f"https://github.com/netbox-community/netbox/pull/{r['pr']}"
    r["overview"] = overviews[str(r["issue"])]

json.dump(rows, open(OUT, "w"), indent=1)
print("tickets:", len(rows), "| files total:", sum(len(r["files_list"]) for r in rows),
      "| subsystems touched:", sorted({s for r in rows for s in r["subsystems"]}))
