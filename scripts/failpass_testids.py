#!/usr/bin/env python3
"""Plan v1.2 item F4: derive the exact test IDs a fixing PR adds or modifies.

Screen 5a (v1) ran whole test modules and recorded the module exit code, so "fails
before the fix" could be satisfied by an ImportError. v2 runs the specific tests the
PR touched, by Django test ID (app.tests.module.Class.test_method), verbose, at the
first parent and at the merge commit, and records a verdict per test.

This script computes the IDs mechanically: for every test file in the PR diff, the
new-file-side line numbers of every added or changed hunk are mapped to the enclosing
test method at the merge commit (ast). Output: data/failpass_matrix_v2.json, one entry
per selected ticket: {issue, pr, merge, test_files, test_ids}.

Requires: full netbox clone at FG_UPSTREAM (default /tmp/netbox-up).
"""
import ast, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM = os.environ.get("FG_UPSTREAM", "/tmp/netbox-up")

def sh(args):
    return subprocess.run(args, cwd=UPSTREAM, capture_output=True, text=True, check=True).stdout

def module_of(path):
    p = path[len("netbox/"):-3].replace("/", ".")
    return p

def method_ranges(src):
    """[(start, end, 'Class.test_x')] for every test method in the file."""
    out = []
    tree = ast.parse(src)
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        for fn in [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test")]:
            out.append((fn.lineno, fn.end_lineno, f"{cls.name}.{fn.name}"))
    return out

def changed_new_lines(merge, path):
    """New-file-side line numbers touched by the PR in this file (from -U0 hunk headers)."""
    lines = set()
    d = sh(["git", "diff", "-U0", merge + "^", merge, "--", path])
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", d, flags=re.M):
        start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        if count == 0:   # pure deletion: attribute to the line after the deletion point
            lines.add(start + 1)
        else:
            lines.update(range(start, start + count))
    return lines

def main():
    rows = []
    for line in open(os.path.join(ROOT, "preregistration", "selected_tickets.md"), encoding="utf-8-sig"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*#(\d+)\s*\|\s*(\d+)\s*\|.*?\|\s*([0-9a-f]{40})\s*\|", line)
        if not m:
            continue
        issue, pr, merge = int(m.group(2)), int(m.group(3)), m.group(4)
        files = [f for f in sh(["git", "diff", "--name-only", merge + "^", merge]).split() if f]
        tests = [f for f in files if "/tests/" in f and f.endswith(".py") and f.startswith("netbox/")]
        ids = []
        for f in tests:
            try:
                src = sh(["git", "show", f"{merge}:{f}"])
            except subprocess.CalledProcessError:
                continue   # deleted by the PR
            ranges = method_ranges(src)
            touched = changed_new_lines(merge, f)
            mod = module_of(f)
            hit = sorted({name for (s, e, name) in ranges if any(s <= l <= e for l in touched)})
            if not hit and touched:
                # changes outside any test method (fixtures, setUpTestData, imports): run the whole module
                hit = ["*"]
            ids += [f"{mod}.{h}" if h != "*" else mod for h in hit]
        rows.append(dict(issue=issue, pr=pr, merge=merge, test_files=tests, test_ids=ids))
        print(f"#{issue}: {len(ids)} ids  {ids[:4]}{' ...' if len(ids) > 4 else ''}")
    json.dump(rows, open(os.path.join(ROOT, "data", "failpass_matrix_v2.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
