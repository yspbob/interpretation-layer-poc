#!/usr/bin/env python3
"""Plan v1.2 item F4: per-test-ID verdicts for screen 5a, from the v2 workflow logs.

Input: a directory holding the downloaded artifacts of the fork's "fail-then-pass screen v2"
workflow (one subfolder per ticket, each with meta_<issue>.txt, pre_<issue>.log, post_<issue>.log).
Output: data/failpass_results_v2/<issue>.json and data/failpass_results_v2/summary.md.

Per test ID:  pre  in {ok, FAIL, ERROR, IMPORT_ERROR, MISSING}
              post in {ok, FAIL, ERROR, IMPORT_ERROR, MISSING}
              discriminating = pre in {FAIL, ERROR} and post == ok
              import_only    = pre == IMPORT_ERROR and post == ok   (the module could not be
                               imported before the fix: the test detects a missing symbol,
                               not necessarily the symptom; counted separately)
Ticket verdict: SCREEN_PASS if at least one discriminating test; SCREEN_PASS_IMPORT_ONLY if the
only before-fix failures are import-level; SCREEN_FAIL otherwise. Ticket-level verdicts are
compared against the v1 module-level verdicts committed in data/failpass_results/summary.txt.

Usage: failpass_verdicts.py ARTIFACT_DIR
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE = re.compile(r"^(test\w*) \(([\w.]+)\)(?: \(.*?\))? \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)\s*$")
FAILED_IMPORT = re.compile(r"^(?:ERROR|FAIL): ([\w.]+) \(unittest\.loader\._FailedTest")

def parse(log_text):
    res = {}
    for line in log_text.splitlines():
        m = LINE.match(line.strip())
        if m:
            name, qual, status = m.group(1), m.group(2), m.group(3)
            tid = qual if qual.endswith("." + name) else f"{qual}.{name}"
            res[tid] = "ok" if status == "ok" else ("SKIP" if status.startswith("skipped") else status)
            continue
        m = FAILED_IMPORT.match(line.strip())
        if m:
            res[f"__import__:{m.group(1)}"] = "IMPORT_ERROR"
    return res

def status_for(tid, results):
    if tid in results:
        return results[tid]
    mod = tid
    while "." in mod:
        mod = mod.rsplit(".", 1)[0]
        if f"__import__:{mod}" in results:
            return "IMPORT_ERROR"
    return "MISSING"

def main(art_dir):
    out_dir = os.path.join(ROOT, "data", "failpass_results_v2")
    os.makedirs(out_dir, exist_ok=True)
    matrix = {r["issue"]: r for r in json.load(open(os.path.join(ROOT, "data", "failpass_matrix_v2.json")))}
    v1 = {}
    for line in open(os.path.join(ROOT, "data", "failpass_results", "summary.txt")):
        m = re.match(r"(SCREEN_\w+) issue=(\d+)", line)
        if m:
            v1[int(m.group(2))] = m.group(1)
    summary = ["# Screen 5a, v2 verdicts per test ID", "",
               "| Issue | v1 verdict (module) | v2 verdict (per test) | discriminating | import-only | not discriminating |",
               "|---|---|---|---|---|---|"]
    for sub in sorted(os.listdir(art_dir)):
        d = os.path.join(art_dir, sub)
        metas = [f for f in os.listdir(d) if f.startswith("meta_")]
        if not metas:
            continue
        issue = int(re.search(r"\d+", metas[0]).group())
        pre = parse(open(os.path.join(d, f"pre_{issue}.log"), errors="replace").read())
        post = parse(open(os.path.join(d, f"post_{issue}.log"), errors="replace").read())
        ids = matrix[issue]["test_ids"] if issue in matrix else []
        # expand bare module IDs to whatever ran in the post log
        expanded = []
        for tid in ids:
            if tid.count(".") <= 2:   # bare module
                expanded += [k for k in post if k.startswith(tid + ".") and not k.startswith("__import__")]
            else:
                expanded.append(tid)
        per = {}
        for tid in sorted(set(expanded)):
            a, b = status_for(tid, pre), status_for(tid, post)
            per[tid] = dict(pre=a, post=b, discriminating=(a in ("FAIL", "ERROR") and b == "ok"),
                            import_only=(a == "IMPORT_ERROR" and b == "ok"))
        n_disc = sum(v["discriminating"] for v in per.values())
        n_imp = sum(v["import_only"] for v in per.values())
        n_no = len(per) - n_disc - n_imp
        verdict = "SCREEN_PASS" if n_disc else ("SCREEN_PASS_IMPORT_ONLY" if n_imp else "SCREEN_FAIL")
        json.dump(dict(issue=issue, verdict=verdict, tests=per), open(os.path.join(out_dir, f"{issue}.json"), "w"), indent=1)
        summary.append(f"| #{issue} | {v1.get(issue, '-')} | {verdict} | {n_disc} | {n_imp} | {n_no} |")
    open(os.path.join(out_dir, "summary.md"), "w").write("\n".join(summary) + "\n")
    print("\n".join(summary))

if __name__ == "__main__":
    main(sys.argv[1])
