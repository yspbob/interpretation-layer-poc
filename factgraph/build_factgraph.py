#!/usr/bin/env python3
"""M-013 Phase 1: deterministic fact-graph extraction over NetBox at T0.

No LLM anywhere. Inputs: the working tree at T0 (ea4c205) and git history
(ancestors of T0 only, guaranteed by the detached checkout). Output: SQLite
fact graph (factgraph.db) with provenance on every row.

Facts extracted:
  modules      : every Python module under netbox/, with LOC, class/function counts
  symbols      : top-level classes and functions per module
  imports      : module-to-module internal import edges (ast-based, fully static)
  subsystems   : Django apps (top-level packages) with roll-up stats
  churn        : per-module commit count, author count, first/last commit date (<= T0)
  tests        : test modules, their test-class/method counts, and which internal
                 modules they import (test topology)
  entrypoints  : management commands, urls modules, api modules, signal receivers
"""
import ast, os, sqlite3, subprocess, sys, hashlib, json

REPO = "/home/claude/poc_netbox"
PKG_ROOT = os.path.join(REPO, "netbox")   # the Django project package dir
DB = "/home/claude/poc/factgraph/factgraph.db"
T0 = "ea4c205a37baa3e58e6e481158c15c6154cceeff"

def sh(args, cwd=REPO):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True).stdout

# ---------- guardrail: confirm HEAD is T0 ----------
head = sh(["git", "rev-parse", "HEAD"]).strip()
assert head == T0, f"HEAD {head} is not T0"

# ---------- walk modules ----------
mods = {}        # relpath -> dict
sym_rows = []
imp_raw = []     # (src_mod, imported_module_string, lineno)

def mod_name(relpath):
    p = relpath[:-3] if relpath.endswith(".py") else relpath
    p = p.replace(os.sep, ".")
    return p[:-9] if p.endswith(".__init__") else p

py_files = []
for root, dirs, files in os.walk(PKG_ROOT):
    dirs[:] = sorted(d for d in dirs if d not in ("node_modules", ".git", "__pycache__"))
    for f in sorted(files):
        if f.endswith(".py"):
            py_files.append(os.path.relpath(os.path.join(root, f), REPO))

for rel in py_files:
    full = os.path.join(REPO, rel)
    src = open(full, encoding="utf-8", errors="replace").read()
    loc = src.count("\n") + 1
    name = mod_name(os.path.relpath(full, PKG_ROOT))
    try:
        tree = ast.parse(src)
    except SyntaxError:
        mods[rel] = dict(module=name, loc=loc, classes=0, functions=0, parse="SYNTAX_ERROR")
        continue
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    mods[rel] = dict(module=name, loc=loc, classes=len(classes), functions=len(funcs), parse="OK")
    for c in classes:
        bases = ",".join(ast.unparse(b) for b in c.bases)[:200]
        sym_rows.append((name, "class", c.name, c.lineno, bases, rel))
    for fn in funcs:
        sym_rows.append((name, "function", fn.name, fn.lineno, "", rel))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imp_raw.append((name, a.name, node.lineno, rel))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:   # relative import -> resolve against pkg
                base = name.split(".")
                base = base[: len(base) - node.level] if not rel.endswith("__init__.py") else base[: len(base) - node.level + 1]
                target = ".".join(base + ([node.module] if node.module else []))
            else:
                target = node.module or ""
            imp_raw.append((name, target, node.lineno, rel))

internal_prefixes = tuple(sorted({m["module"].split(".")[0] for m in mods.values()}))
mod_by_name = {m["module"]: rel for rel, m in mods.items()}

def resolve_internal(target):
    """Longest-prefix match of an imported dotted path to a known module."""
    if not target or not target.startswith(internal_prefixes):
        return None
    parts = target.split(".")
    while parts:
        cand = ".".join(parts)
        if cand in mod_by_name:
            return cand
        parts.pop()
    return None

imp_rows = []
for src_mod, target, lineno, rel in imp_raw:
    resolved = resolve_internal(target)
    if resolved and resolved != src_mod:
        imp_rows.append((src_mod, resolved, target, lineno, rel))

# ---------- churn & authorship (ancestors of T0 only; per-path exact, matches the audit command) ----------
churn = {}
for rel in py_files:
    out = sh(["git", "log", "--format=%an|%ad", "--date=short", T0, "--", rel])
    if not out.strip():
        continue
    authors = set(); dates = []
    for line in out.splitlines():
        an, ad = line.rsplit("|", 1)
        authors.add(an); dates.append(ad)
    churn[rel] = dict(commits=len(dates), authors=authors, first=min(dates), last=max(dates))

# ---------- assemble DB ----------
os.makedirs(os.path.dirname(DB), exist_ok=True)
if os.path.exists(DB):
    os.remove(DB)
db = sqlite3.connect(DB)
db.executescript("""
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE modules(module TEXT PRIMARY KEY, path TEXT, loc INT, classes INT, functions INT,
                     parse TEXT, subsystem TEXT, is_test INT, is_migration INT, is_data INT);
CREATE TABLE symbols(module TEXT, kind TEXT, name TEXT, lineno INT, bases TEXT, path TEXT);
CREATE TABLE imports(src TEXT, dst TEXT, raw TEXT, lineno INT, path TEXT);
CREATE TABLE churn(path TEXT PRIMARY KEY, module TEXT, commits INT, authors INT,
                   first_commit TEXT, last_commit TEXT);
CREATE TABLE subsystems(subsystem TEXT PRIMARY KEY, modules INT, loc_code INT, loc_data INT, test_modules INT);
CREATE TABLE entrypoints(kind TEXT, module TEXT, detail TEXT, path TEXT);
""")

def subsystem_of(name):
    parts = name.split(".")
    if parts[0] == "netbox" and len(parts) > 1:
        return parts[0] if len(parts) == 1 else (parts[1] if os.path.isdir(os.path.join(PKG_ROOT, parts[0], parts[1])) else parts[0])
    return parts[0]

for rel, m in sorted(mods.items()):
    name = m["module"]
    sub = name.split(".")[0]
    is_test = 1 if (".tests" in name or name.rsplit(".", 1)[-1].startswith("test")) else 0
    is_mig = 1 if ".migrations." in name else 0
    is_data = 1 if (m["loc"] > 2000 and m["classes"] == 0 and m["functions"] == 0) else 0
    db.execute("INSERT INTO modules VALUES(?,?,?,?,?,?,?,?,?,?)",
               (name, rel, m["loc"], m["classes"], m["functions"], m["parse"], sub, is_test, is_mig, is_data))
db.executemany("INSERT INTO symbols VALUES(?,?,?,?,?,?)", sorted(sym_rows))
db.executemany("INSERT INTO imports VALUES(?,?,?,?,?)", sorted(set(imp_rows)))
for path, d in sorted(churn.items()):
    rel = path
    name = mod_name(rel[len("netbox/"):]) if rel.startswith("netbox/") else rel
    db.execute("INSERT OR REPLACE INTO churn VALUES(?,?,?,?,?,?)",
               (rel, name, d["commits"], len(d["authors"]), d["first"], d["last"]))

# entrypoints
for name, rel in sorted(mod_by_name.items()):
    leaf = name.rsplit(".", 1)[-1]
    if ".management.commands." in name:
        db.execute("INSERT INTO entrypoints VALUES(?,?,?,?)", ("management_command", name, leaf, rel))
    if leaf == "urls":
        db.execute("INSERT INTO entrypoints VALUES(?,?,?,?)", ("urls", name, "", rel))
    if ".api." in name and leaf in ("views", "viewsets"):
        db.execute("INSERT INTO entrypoints VALUES(?,?,?,?)", ("api_views", name, "", rel))
    if leaf == "signals":
        db.execute("INSERT INTO entrypoints VALUES(?,?,?,?)", ("signals", name, "", rel))

# subsystems roll-up
for (sub,) in db.execute("SELECT DISTINCT subsystem FROM modules ORDER BY 1"):
    n, loc_code = db.execute("SELECT COUNT(*), SUM(loc) FROM modules WHERE subsystem=? AND is_migration=0 AND is_data=0", (sub,)).fetchone()
    loc_data = db.execute("SELECT COALESCE(SUM(loc),0) FROM modules WHERE subsystem=? AND is_data=1", (sub,)).fetchone()[0]
    t = db.execute("SELECT COUNT(*) FROM modules WHERE subsystem=? AND is_test=1", (sub,)).fetchone()[0]
    db.execute("INSERT INTO subsystems VALUES(?,?,?,?,?)", (sub, n, loc_code, loc_data, t))

db.execute("INSERT INTO meta VALUES('t0', ?)", (T0,))
db.execute("INSERT INTO meta VALUES('repo', 'yspbob/netbox (fork of netbox-community/netbox)')")
db.execute("INSERT INTO meta VALUES('extractor', 'ast+gitlog deterministic v1, no LLM')")
db.execute("INSERT INTO meta VALUES('python', sys.version)" if False else "INSERT INTO meta VALUES('python', ?)", (sys.version.split()[0],))
db.commit()

# summary
print("modules:", db.execute("SELECT COUNT(*) FROM modules").fetchone()[0])
print("  non-migration:", db.execute("SELECT COUNT(*) FROM modules WHERE is_migration=0").fetchone()[0])
print("  tests:", db.execute("SELECT COUNT(*) FROM modules WHERE is_test=1").fetchone()[0])
print("symbols:", db.execute("SELECT COUNT(*) FROM symbols").fetchone()[0])
print("import edges:", db.execute("SELECT COUNT(*) FROM imports").fetchone()[0])
print("churn rows:", db.execute("SELECT COUNT(*) FROM churn").fetchone()[0])
print("entrypoints:", db.execute("SELECT COUNT(*) FROM entrypoints").fetchone()[0])
print("subsystems:", db.execute("SELECT COUNT(*) FROM subsystems").fetchone()[0])
for row in db.execute("SELECT subsystem, modules, loc_code, loc_data, test_modules FROM subsystems ORDER BY loc_code DESC LIMIT 12"):
    print("  ", row)
print("data modules:", db.execute("SELECT COUNT(*) FROM modules WHERE is_data=1").fetchone()[0])
h = hashlib.sha256(open(DB, "rb").read()).hexdigest()
print("db sha256:", h[:16])
