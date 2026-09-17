#!/usr/bin/env python3
"""
M-013 Phase 2 mechanical evidence check (plan v1.2: "claims without evidence are rejected
mechanically before any human sees them").

Rules, fixed before drafting:
- A draft file is Markdown. Every paragraph or bullet that asserts something must carry at least one
  citation of the form [fg:<row id>] or [code:<path>:<line>] or [code:<path>:<start>-<end>].
- Headings (# ...), blank lines, and lines that are only citations are not claims.
- [fg:...] must name a row id present in the subsystem's slice (ids: modules:<module>,
  symbols:<module>:<name>, imports:<src>-><dst>, model_refs:<module>:<lineno>, churn:<module>,
  entrypoints:<module>, subsystems:<name>).
- [code:path:line] must name a file (any type) that exists in the T0 tree; the line (or every line of the range)
  must exist and the range must be at most 60 lines.
- A claim with no citation, or whose every citation fails, is REMOVED and logged. A claim with at least
  one valid citation is kept; its failed citations are dropped and logged.
Version 2 (17 Sep 2026, after batch 2): the path pattern accepted only .py files, narrower than the
stated rule; widened to any file in the tree. Rule text unchanged. Both batches re-checked with v2.
Usage: check_citations.py <subsystem> <draft dir> <out dir>
"""
import json, os, re, sys

T0 = "/home/claude/screen/t0_src"
CIT = re.compile(r"\[(fg|code):([^\]]+)\]")


def load_ids(sub):
    sl = json.load(open(f"/home/claude/screen/phase2/slices/{sub}.json"))
    ids = {f"subsystems:{sub}"}
    for k in ("modules", "symbols", "imports_out", "imports_in", "model_refs", "model_refs_in", "churn", "entrypoints"):
        for r in sl[k]:
            ids.add(r["id"])
    return ids


def check_code(ref):
    m = re.match(r"^([\w./\-]+):(\d+)(?:-(\d+))?$", ref.strip())
    if not m:
        return False, "malformed"
    path, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    p = os.path.join(T0, path)
    if not os.path.isfile(p):
        return False, "no such file at T0"
    n = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
    if a < 1 or b > n or b < a:
        return False, f"line out of range (file has {n} lines)"
    if b - a > 60:
        return False, "range longer than 60 lines"
    return True, "ok"


def is_claim(line):
    s = line.strip()
    if not s or s.startswith("#"):
        return False
    if CIT.sub("", s).strip(" -*|") == "":
        return False
    return True


def process(sub, src, dst):
    ids = load_ids(sub)
    log = {"subsystem": sub, "files": {}}
    os.makedirs(dst, exist_ok=True)
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".md"):
            continue
        kept, removed, dropped_cits = [], [], []
        out = []
        for i, line in enumerate(open(os.path.join(src, fn), encoding="utf-8"), 1):
            raw = line.rstrip("\n")
            if not is_claim(raw):
                out.append(raw)
                continue
            cits = CIT.findall(raw)
            valid = []
            for kind, ref in cits:
                if kind == "fg":
                    ok = ref.strip() in ids
                    why = "ok" if ok else "no such row in slice"
                else:
                    ok, why = check_code(ref)
                if ok:
                    valid.append((kind, ref))
                else:
                    dropped_cits.append({"line": i, "cit": f"[{kind}:{ref}]", "why": why})
            if valid:
                new = raw
                for kind, ref in cits:
                    if (kind, ref) not in valid:
                        new = new.replace(f"[{kind}:{ref}]", "")
                out.append(re.sub(r"[ \t]+$", "", new))
                kept.append(i)
            else:
                removed.append({"line": i, "text": raw[:200], "why": "no valid citation" if cits else "no citation"})
        open(os.path.join(dst, fn), "w", encoding="utf-8").write("\n".join(out) + "\n")
        log["files"][fn] = {"claims_kept": len(kept), "claims_removed": len(removed), "citations_dropped": len(dropped_cits),
                            "removed": removed, "dropped": dropped_cits}
    json.dump(log, open(os.path.join(dst, "check_report.json"), "w"), indent=1)
    tot_k = sum(v["claims_kept"] for v in log["files"].values()); tot_r = sum(v["claims_removed"] for v in log["files"].values())
    print(f"{sub}: kept {tot_k}, removed {tot_r}, citations dropped {sum(v['citations_dropped'] for v in log['files'].values())}")
    return log


if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2], sys.argv[3])
