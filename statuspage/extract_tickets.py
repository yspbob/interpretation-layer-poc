#!/usr/bin/env python3
"""Deterministic ticket-data extraction for the status page.
Reads preregistration/selected_tickets.md + merge commits in the fork clone + issues.json.
Writes tickets.json. LLM-written overviews are merged from overviews.json and labelled."""
import json, re, subprocess, os

CLONE = "/home/claude/poc_netbox"
SEL = "/home/claude/interpretation-layer-poc/preregistration/selected_tickets.md"
ISSUES = "/mnt/user-data/uploads/AI-Workbook/_poc_transfer/issues.json"
OUT = "/home/claude/poc/statuspage/tickets.json"

rows = []
for line in open(SEL):
    m = re.match(r"\|\s*(\d+)\s*\|\s*#(\d+)\s*\|\s*(\d+)\s*\|\s*([\d-]+)\s*\|\s*([\d-]+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([0-9a-f]{40})\s*\|", line)
    if m:
        rows.append(dict(seq=int(m.group(1)), issue=int(m.group(2)), pr=int(m.group(3)),
                         closed=m.group(4), merged=m.group(5), files=int(m.group(6)),
                         audit=m.group(7), commit=m.group(8)))
assert len(rows) == 25, len(rows)

issues = {it["number"]: it for it in json.load(open(ISSUES, encoding="utf-8-sig"))}
overviews = json.load(open("/home/claude/poc/statuspage/overviews.json"))

def sh(args):
    return subprocess.run(args, cwd=CLONE, capture_output=True, text=True).stdout

for r in rows:
    files = [f for f in sh(["git", "show", "--name-only", "--format=", r["commit"]]).splitlines() if f]
    title = sh(["git", "show", "--format=%s", "--no-patch", r["commit"]]).strip()
    subs = sorted({f.split("/")[1] for f in files if f.startswith("netbox/") and "/" in f[7:]})
    r["title"] = issues[r["issue"]]["title"] if r["issue"] in issues else title
    r["merge_title"] = title
    r["files_list"] = files
    r["subsystems"] = subs
    r["issue_url"] = issues[r["issue"]]["url"] if r["issue"] in issues else f"https://github.com/netbox-community/netbox/issues/{r['issue']}"
    r["pr_url"] = f"https://github.com/netbox-community/netbox/pull/{r['pr']}"
    r["overview"] = overviews[str(r["issue"])]

json.dump(rows, open(OUT, "w"), indent=1)
print("tickets:", len(rows), "| files total:", sum(len(r["files_list"]) for r in rows),
      "| subsystems touched:", sorted({s for r in rows for s in r["subsystems"]}))
