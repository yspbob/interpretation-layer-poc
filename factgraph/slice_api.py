#!/usr/bin/env python3
"""M-013 Phase 1: slice API over the fact graph. Read-only, deterministic.
The Phase 2 drafting pipeline and the Phase 4 MCP server consume ONLY these calls."""
import sqlite3, json, os

DB = os.environ.get("FG_DB", "/home/claude/poc/factgraph/factgraph.db")

def _db():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c

def meta():
    return {k: v for k, v in _db().execute("SELECT key, value FROM meta")}

def subsystem_summary():
    return [dict(r) for r in _db().execute(
        "SELECT * FROM subsystems ORDER BY loc_code DESC")]

def module_page(module):
    db = _db()
    m = db.execute("SELECT * FROM modules WHERE module=?", (module,)).fetchone()
    if not m: return None
    return {
        "module": dict(m),
        "symbols": [dict(r) for r in db.execute(
            "SELECT kind,name,lineno,bases FROM symbols WHERE module=? ORDER BY lineno", (module,))],
        "imports": [dict(r) for r in db.execute(
            "SELECT dst,raw,lineno FROM imports WHERE src=? ORDER BY lineno", (module,))],
        "imported_by": [r["src"] for r in db.execute(
            "SELECT DISTINCT src FROM imports WHERE dst=? ORDER BY src", (module,))],
        "churn": dict(db.execute("SELECT * FROM churn WHERE module=?", (module,)).fetchone() or {}),
        "tested_by": [r["src"] for r in db.execute(
            "SELECT DISTINCT i.src FROM imports i JOIN modules t ON i.src=t.module "
            "WHERE i.dst=? AND t.is_test=1 ORDER BY i.src", (module,))],
    }

def dependencies(module, direction="out"):
    q = ("SELECT DISTINCT dst AS m FROM imports WHERE src=?" if direction == "out"
         else "SELECT DISTINCT src AS m FROM imports WHERE dst=?")
    return [r["m"] for r in _db().execute(q + " ORDER BY m", (module,))]

def cross_subsystem_edges(subsystem=None):
    q = ("SELECT i.src, i.dst, a.subsystem AS from_sub, b.subsystem AS to_sub, i.path, i.lineno "
         "FROM imports i JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module "
         "WHERE a.subsystem != b.subsystem")
    args = ()
    if subsystem:
        q += " AND (a.subsystem=? OR b.subsystem=?)"; args = (subsystem, subsystem)
    return [dict(r) for r in _db().execute(q + " ORDER BY i.src, i.dst", args)]

def churn_top(n=20):
    return [dict(r) for r in _db().execute(
        "SELECT * FROM churn ORDER BY commits DESC LIMIT ?", (n,))]

def model_refs(module=None, cross_app_only=False):
    """v2: Django string-reference edges (FK/M2M/O2O/GenericRelation targets, apps.get_model)."""
    q = "SELECT * FROM model_refs"; conds = []; args = []
    if module: conds.append("module=?"); args.append(module)
    if cross_app_only: conds.append("cross_app=1")
    if conds: q += " WHERE " + " AND ".join(conds)
    return [dict(r) for r in _db().execute(q + " ORDER BY module, lineno", args)]

def cross_app_model_edges(app=None):
    """v2: app-to-app coupling via string references, aggregated (from_app, to_app, count)."""
    q = ("SELECT substr(module,1,instr(module,'.')-1) AS from_app, ref_app AS to_app, COUNT(*) AS c "
         "FROM model_refs WHERE cross_app=1")
    args = ()
    if app: q += " AND (substr(module,1,instr(module,'.')-1)=? OR ref_app=?)"; args = (app, app)
    return [dict(r) for r in _db().execute(q + " GROUP BY 1,2 ORDER BY c DESC", args)]

def entrypoints(kind=None):
    q = "SELECT * FROM entrypoints"
    args = ()
    if kind: q += " WHERE kind=?"; args = (kind,)
    return [dict(r) for r in _db().execute(q + " ORDER BY kind, module", args)]

if __name__ == "__main__":
    print(json.dumps(meta(), indent=1))
    print(json.dumps(subsystem_summary()[:3], indent=1))
    print(json.dumps(module_page("dcim.models")["module"], indent=1))
    print("dcim.models imported_by count:", len(module_page("dcim.models")["imported_by"]))
    print("cross-app model edges (top 5):", json.dumps(cross_app_model_edges()[:5]))
