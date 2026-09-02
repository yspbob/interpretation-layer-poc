#!/usr/bin/env python3
"""Plan v1.2 item F5: per-ticket fact graphs and the staleness table.

For each of the 25 selected tickets, check out the pre-fix commit (FIRST parent of
the fixing PR's merge commit), run the deterministic v2 extractor there, and diff
the result against the frozen T0 store. No LLM. Each parent commit contains nothing
of its own ticket's fix, so nothing here leaks a solution.

Outputs (committed):
  factgraph/per_ticket/<issue>.json   compact diff vs T0: modules/symbols/edges/model_refs
                                      added and removed, survival rates, touched modules
                                      absent from T0. Source for the change note and the
                                      stale-evidence flags (Phase 5).
  data/staleness.md, data/staleness.json   the staleness covariate table.

The full per-ticket stores are not committed (25 x ~1.2 MB, reproducible in ~25 min
with this script); set FG_KEEP_STORES=1 to keep them under factgraph/per_ticket/stores/.

Requires: a full clone of netbox at FG_UPSTREAM (default /tmp/netbox-up) containing all
merge commits; the extractor factgraph/build_factgraph.py; git.
"""
import json, os, re, sqlite3, subprocess, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UPSTREAM = os.environ.get("FG_UPSTREAM", "/tmp/netbox-up")
T0_DB = os.path.join(HERE, "factgraph.db")
T0 = "ea4c205a37baa3e58e6e481158c15c6154cceeff"
OUT_DIR = os.path.join(HERE, "per_ticket")
KEEP = os.environ.get("FG_KEEP_STORES") == "1"

def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True).stdout

def load_sets(db_path):
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    return dict(
        modules=set(r[0] for r in db.execute("SELECT module FROM modules")),
        symbols=set(db.execute("SELECT module, kind, name FROM symbols")),
        edges=set(db.execute("SELECT DISTINCT src, dst FROM imports")),
        model_refs=set(db.execute("SELECT module, class, field, kind, raw FROM model_refs")),
        tests=set(r[0] for r in db.execute("SELECT module FROM modules WHERE is_test=1")),
    )

def tickets():
    rows = []
    for line in open(os.path.join(ROOT, "preregistration", "selected_tickets.md"), encoding="utf-8-sig"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*#(\d+)\s*\|\s*(\d+)\s*\|\s*([\d-]+)\s*\|\s*([\d-]+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([0-9a-f]{40})\s*\|", line)
        if m:
            rows.append(dict(seq=int(m.group(1)), issue=int(m.group(2)), pr=int(m.group(3)),
                             merged=m.group(5), files=int(m.group(6)), merge=m.group(8)))
    assert len(rows) == 25, len(rows)
    return rows

def mod_of(path):
    if not path.startswith("netbox/") or not path.endswith(".py"):
        return None
    p = path[len("netbox/"):-3].replace("/", ".")
    return p[:-9] if p.endswith(".__init__") else p

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = load_sets(T0_DB)
    t0_nontest = {m for m in t0["modules"] if m not in t0["tests"]}
    table = []
    for t in tickets():
        parent = sh(["git", "rev-parse", t["merge"] + "^"], cwd=UPSTREAM).strip()   # first parent
        parent_date = sh(["git", "log", "-1", "--format=%cs", parent], cwd=UPSTREAM).strip()
        changed = [p for p in sh(["git", "diff", "--name-only", parent, t["merge"]], cwd=UPSTREAM).split() if p]
        touched = sorted({m for m in (mod_of(p) for p in changed) if m and ".tests" not in m and ".migrations." not in m})
        wt = tempfile.mkdtemp(prefix=f"fg_{t['issue']}_")
        sh(["git", "worktree", "add", "-f", "--detach", wt, parent], cwd=UPSTREAM)
        store = os.path.join(OUT_DIR, "stores", f"{t['issue']}.db") if KEEP else os.path.join(wt, "fg.db")
        os.makedirs(os.path.dirname(store), exist_ok=True)
        env = dict(os.environ, FG_REPO=wt, FG_DB=store, FG_T0=parent)
        subprocess.run([sys.executable, os.path.join(HERE, "build_factgraph.py")], env=env, check=True,
                       stdout=subprocess.DEVNULL)
        cur = load_sets(store)
        sh(["git", "worktree", "remove", "--force", wt], cwd=UPSTREAM)
        if not KEEP:
            shutil.rmtree(wt, ignore_errors=True)
        d = dict(issue=t["issue"], pr=t["pr"], merge=t["merge"], parent=parent, parent_date=parent_date,
                 t0=T0, months_after_t0=round((_days(parent_date) - _days("2025-06-27")) / 30.44, 1))
        for k in ("modules", "symbols", "edges", "model_refs"):
            a, b = t0[k], cur[k]
            d[k] = dict(t0=len(a), at_checkout=len(b), survived=len(a & b), removed=len(a - b), added=len(b - a),
                        survival=round(len(a & b) / len(a), 4))
            d[k + "_removed"] = sorted(map(list, a - b)) if k != "modules" else sorted(a - b)
            d[k + "_added"] = sorted(map(list, b - a)) if k != "modules" else sorted(b - a)
        d["touched_modules"] = touched
        d["touched_absent_from_t0"] = [m for m in touched if m not in t0["modules"]]
        te = {e for e in t0["edges"] if e[0] in touched}; ts = {s for s in t0["symbols"] if s[0] in touched}
        d["touched_edge_survival"] = round(len(te & cur["edges"]) / len(te), 4) if te else None
        d["touched_symbol_survival"] = round(len(ts & cur["symbols"]) / len(ts), 4) if ts else None
        json.dump(d, open(os.path.join(OUT_DIR, f"{t['issue']}.json"), "w"), indent=1)
        table.append(dict(seq=t["seq"], issue=t["issue"], parent=parent[:9], parent_date=parent_date,
                          months_after_t0=d["months_after_t0"],
                          mod_surv=d["modules"]["survival"], sym_surv=d["symbols"]["survival"],
                          edge_surv=d["edges"]["survival"], ref_surv=d["model_refs"]["survival"],
                          mods_added=d["modules"]["added"], edges_added=d["edges"]["added"],
                          touched=len(touched), touched_absent=len(d["touched_absent_from_t0"]),
                          touched_edge_surv=d["touched_edge_survival"], touched_sym_surv=d["touched_symbol_survival"]))
        print(f"#{t['issue']} parent {parent[:9]} ({parent_date}) +{d['modules']['added']} modules "
              f"+{d['edges']['added']} edges sym_surv={d['symbols']['survival']:.3f} "
              f"touched={len(touched)} absent={len(d['touched_absent_from_t0'])}", flush=True)
    json.dump(table, open(os.path.join(ROOT, "data", "staleness.json"), "w"), indent=1)
    write_md(table)

def _days(s):
    import datetime
    return datetime.date.fromisoformat(s).toordinal()

def write_md(table):
    n_absent = sum(1 for r in table if r["touched_absent"])
    lines = ["# Corpus staleness per ticket (plan v1.2, F5)", "",
             "The LLM-drafted corpus is frozen at T0 (`ea4c205`, 27 Jun 2025). Each row compares the deterministic "
             "fact graph rebuilt at the ticket's pre-fix checkout (first parent of the merge commit) with the T0 store. "
             "Survival = fraction of T0 facts still true at the checkout. Added = facts at the checkout the T0 map does "
             "not contain. Touched = non-test, non-migration modules the reference fix changed; absent = touched modules "
             "that do not exist at T0. Generated by `factgraph/build_per_ticket.py`; no LLM.", "",
             "| # | Issue | Checkout | Months after T0 | Module surv. | Symbol surv. | Edge surv. | Ref surv. | Modules added | Edges added | Touched | Touched absent from T0 | Touched edge surv. | Touched symbol surv. |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in table:
        f = lambda v: "n/a" if v is None else f"{v:.3f}"
        lines.append(f"| {r['seq']} | #{r['issue']} | `{r['parent']}` {r['parent_date']} | {r['months_after_t0']} | "
                     f"{f(r['mod_surv'])} | {f(r['sym_surv'])} | {f(r['edge_surv'])} | {f(r['ref_surv'])} | {r['mods_added']} | "
                     f"{r['edges_added']} | {r['touched']} | {r['touched_absent']} | {f(r['touched_edge_surv'])} | {f(r['touched_sym_surv'])} |")
    import statistics
    lines += ["", f"Summary: median symbol survival {statistics.median(r['sym_surv'] for r in table):.3f}; "
              f"median edge survival {statistics.median(r['edge_surv'] for r in table):.3f}; "
              f"tickets touching at least one module absent from T0: {n_absent} of {len(table)}; "
              f"maximum staleness {max(r['months_after_t0'] for r in table)} months.",
              "", "Use in Phase 5: (1) covariate in the exploratory analysis, expected to attenuate the effect; "
              "(2) source of the per-subsystem change note served beside the corpus; (3) source of the per-claim "
              "stale-evidence flags (a claim whose cited module, symbol or edge is in the removed set at the ticket's checkout)."]
    open(os.path.join(ROOT, "data", "staleness.md"), "w").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
