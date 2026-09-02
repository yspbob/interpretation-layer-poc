#!/usr/bin/env python3
"""M-013 status page generator, v2 (plan v1.2, section 6).

Deterministic assembly from committed artifacts only:
  statuspage/state.json            every hand-stated fact (phases, cards, Gate 1 scores, texts)
  factgraph/factgraph.db           the map (v2: imports + model_refs)
  statuspage/tickets.json          from preregistration/selected_tickets.md via extract_tickets.py
  data/staleness.json              per-ticket staleness (build_per_ticket.py)
  data/name_coupling.json          hidden-test name coupling (name_coupling.py)
  statuspage/overviews.json        LLM-written one-line ticket overviews, labelled on the page
Nothing on the page is typed into this file. Presentation only: no pipeline stage reads it.
The footer carries the source commit the generator ran on, so deployment lag is visible.
Run from anywhere: paths are resolved relative to the repository root.
"""
import sqlite3, json, math, html, datetime, os, subprocess, textwrap, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
DB = P("factgraph", "factgraph.db")
OUT = P("docs", "index.html")
GENERATED = datetime.date.today().isoformat()
SRC_COMMIT = os.environ.get("FG_SRC_COMMIT") or subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "uncommitted"
FG_SHA = hashlib.sha256(open(DB, "rb").read()).hexdigest()[:16]
import sys; sys.path.insert(0, P("factgraph"))
from rowhash import table_hashes, store_hash
ROWHASH = store_hash(table_hashes(DB))[:16]

NAVY = "#24425f"; NAVY_D = "#16293c"; INK = "#1d2530"; MUT = "#5b6570"
GOOD = "#1a7f37"; WARN = "#b45309"; PEND = "#6b7280"; LINE = "#d8dce1"
BG = "#f7f7f5"; CARD = "#ffffff"; WIP = "#fff4e5"

S = json.load(open(P("statuspage", "state.json")))
db = sqlite3.connect(DB); db.row_factory = sqlite3.Row
meta = {k: v for k, v in db.execute("SELECT key, value FROM meta")}
T0 = meta["t0"][:7]
tickets = json.load(open(P("statuspage", "tickets.json")))
stale = {r["issue"]: r for r in json.load(open(P("data", "staleness.json")))} if os.path.exists(P("data", "staleness.json")) else {}
coupling = {r["issue"]: r for r in json.load(open(P("data", "name_coupling.json")))} if os.path.exists(P("data", "name_coupling.json")) else {}

subs = [dict(r) for r in db.execute("SELECT * FROM subsystems ORDER BY loc_code DESC")]
counts = dict(
    modules=db.execute("SELECT COUNT(*) FROM modules").fetchone()[0],
    symbols=db.execute("SELECT COUNT(*) FROM symbols").fetchone()[0],
    imports=db.execute("SELECT COUNT(*) FROM imports").fetchone()[0],
    edges=db.execute("SELECT COUNT(*) FROM (SELECT DISTINCT src,dst FROM imports)").fetchone()[0],
    refs=db.execute("SELECT COUNT(*) FROM model_refs").fetchone()[0],
    refs_cross=db.execute("SELECT COUNT(*) FROM model_refs WHERE cross_app=1").fetchone()[0],
    subsystems=db.execute("SELECT COUNT(*) FROM subsystems").fetchone()[0],
    loc_total=db.execute("SELECT SUM(loc) FROM modules").fetchone()[0],
    loc_code=db.execute("SELECT SUM(loc) FROM modules WHERE is_migration=0 AND is_data=0").fetchone()[0],
    loc_data=db.execute("SELECT COALESCE(SUM(loc),0) FROM modules WHERE is_data=1").fetchone()[0],
    loc_mig=db.execute("SELECT COALESCE(SUM(loc),0) FROM modules WHERE is_migration=1").fetchone()[0],
)
sub_edges = {}
for r in db.execute("""SELECT a.subsystem s1, b.subsystem s2, COUNT(*) c FROM imports i
    JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module
    WHERE a.subsystem!=b.subsystem GROUP BY 1,2"""):
    sub_edges[(r["s1"], r["s2"])] = r["c"]
ref_edges = [dict(r) for r in db.execute("""SELECT substr(module,1,instr(module,'.')-1) a, ref_app b, COUNT(*) c
    FROM model_refs WHERE cross_app=1 GROUP BY 1,2 ORDER BY c DESC LIMIT 15""")]

drill = {}
for s in subs:
    mods = [dict(r) for r in db.execute("""
      SELECT m.module, m.loc, m.classes, m.functions,
        (SELECT COUNT(DISTINCT src) FROM imports WHERE dst=m.module) fan_in,
        (SELECT COUNT(DISTINCT dst) FROM imports WHERE src=m.module) fan_out,
        COALESCE(c.commits,0) commits, COALESCE(c.authors,0) authors
      FROM modules m LEFT JOIN churn c ON c.module=m.module
      WHERE m.subsystem=? AND m.is_migration=0 AND m.is_data=0
      ORDER BY fan_in DESC, m.loc DESC LIMIT 12""", (s["subsystem"],))]
    outs = [dict(r) for r in db.execute("""SELECT b.subsystem sub, COUNT(*) c FROM imports i
        JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module
        WHERE a.subsystem=? AND b.subsystem!=? GROUP BY 1 ORDER BY c DESC LIMIT 6""", (s["subsystem"], s["subsystem"]))]
    ins_ = [dict(r) for r in db.execute("""SELECT a.subsystem sub, COUNT(*) c FROM imports i
        JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module
        WHERE b.subsystem=? AND a.subsystem!=? GROUP BY 1 ORDER BY c DESC LIMIT 6""", (s["subsystem"], s["subsystem"]))]
    refs_out = [dict(r) for r in db.execute("""SELECT ref_app sub, COUNT(*) c FROM model_refs
        WHERE cross_app=1 AND substr(module,1,instr(module,'.')-1)=? GROUP BY 1 ORDER BY c DESC LIMIT 6""", (s["subsystem"],))]
    drill[s["subsystem"]] = dict(stats=s, top_modules=mods, imports_out=outs, imported_in=ins_, refs_out=refs_out)

# ---------------- subsystem dependency SVG ----------------
W, H, CX, CY, R = 860, 640, 430, 320, 245
big = [s for s in subs if s["loc_code"] >= 500]
n = len(big); pos = {}
for i, s in enumerate(big):
    a = -math.pi / 2 + 2 * math.pi * i / n
    pos[s["subsystem"]] = (CX + R * math.cos(a), CY + R * math.sin(a))
maxloc = max(s["loc_code"] for s in big)
edges_svg = []
for (s1, s2), c in sorted(sub_edges.items(), key=lambda kv: kv[1]):
    if s1 not in pos or s2 not in pos or c < 3: continue
    x1, y1 = pos[s1]; x2, y2 = pos[s2]
    mx, my = (x1 + x2) / 2 + (CX - (x1 + x2) / 2) * 0.35, (y1 + y2) / 2 + (CY - (y1 + y2) / 2) * 0.35
    w = 0.6 + math.log2(c); op = min(0.12 + c / 200, 0.55)
    edges_svg.append(f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" '
                     f'stroke="{NAVY}" stroke-width="{w:.1f}" opacity="{op:.2f}" class="edge"/>')
nodes_svg = []
for s in big:
    x, y = pos[s["subsystem"]]
    r = 10 + 22 * math.sqrt(s["loc_code"] / maxloc)
    ly = y + r + 16 if y >= CY else y - r - 8
    nodes_svg.append(
        f'<g class="node" data-sub="{s["subsystem"]}" style="cursor:pointer">'
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{NAVY}" opacity="0.88" stroke="#fff" stroke-width="2"/>'
        f'<text x="{x:.0f}" y="{ly:.0f}" text-anchor="middle" class="nlabel">{s["subsystem"]}</text>'
        f'<text x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle" class="nnum">{s["loc_code"]//1000}k</text></g>')
dep_svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Subsystem dependency graph">'
           + "".join(edges_svg) + "".join(nodes_svg) + "</svg>")
edge_table = sorted(((s1, s2, c) for (s1, s2), c in sub_edges.items()), key=lambda t: -t[2])[:15]

# ---------------- pipeline SVG ----------------
phases = S["phases"]
PW = 1180; seg = PW / len(phases); pipe = []
for i, ph in enumerate(phases):
    x = seg * i + seg / 2; st = ph["status"]
    col = GOOD if st == "done" else (WARN if st == "active" else "#aeb6bf")
    icon = "&#10003;" if st == "done" else ("&#9654;" if st == "active" else "")
    if i < len(phases) - 1:
        pipe.append(f'<line x1="{x+42:.0f}" y1="70" x2="{x+seg-42:.0f}" y2="70" stroke="{LINE}" stroke-width="2.5"/>')
    pipe.append(f'<circle cx="{x:.0f}" cy="70" r="26" fill="{col}" opacity="{1 if st!="pending" else 0.55}"/>'
                f'<text x="{x:.0f}" y="63" text-anchor="middle" class="pnum">{ph["num"]}</text>'
                f'<text x="{x:.0f}" y="80" text-anchor="middle" class="picon">{icon}</text>'
                f'<text x="{x:.0f}" y="118" text-anchor="middle" class="pname">{html.escape(ph["name"])}</text>'
                f'<text x="{x:.0f}" y="140" text-anchor="middle" class="pgate">{html.escape(ph["gate"])}</text>')
    for j, wline in enumerate(textwrap.wrap(ph["meaning"], 24)[:3]):
        pipe.append(f'<text x="{x:.0f}" y="{158+j*14}" text-anchor="middle" class="pmean">{html.escape(wline)}</text>')
    for j, wline in enumerate(textwrap.wrap(ph["note"], 24)[:2]):
        pipe.append(f'<text x="{x:.0f}" y="{206+j*14}" text-anchor="middle" class="pnote" fill="{col}">{html.escape(wline)}</text>')
pipe_svg = f'<svg viewBox="0 0 {PW} 240" role="img" aria-label="POC pipeline: phases and gates">' + "".join(pipe) + "</svg>"

# ---------------- honesty cards ----------------
LAB = {"green": "HOLDS", "amber": "OPEN", "grey": "NOT YET TESTABLE"}
rag_html = "".join(
    f'<div class="rag {c["state"]}"><span class="dot"></span><b>{html.escape(c["title"])}</b>'
    f'<span class="raglab">{LAB[c["state"]]}</span><p>{html.escape(c["text"])}</p>'
    f'<p class="src">Source: {html.escape(c["source"])}</p></div>' for c in S["honesty_cards"])

# ---------------- Gate 1 ----------------
g1 = S["gate1"]; crit = g1["criteria"]; scores = g1["scores"]
sel_rows = "".join(
    f'<tr><td>{i+1}. {html.escape(c)}</td>' + "".join(
        f'<td class="{ "hi" if scores[k][i]==max(scores[x][i] for x in scores) else "" }">{scores[k][i]}</td>'
        for k in scores) + "</tr>" for i, c in enumerate(crit))
sel_totals = "<tr class='tot'><td>Total / 35</td>" + "".join(f"<td>{sum(v)}</td>" for v in scores.values()) + "</tr>"

# ---------------- subsystem bars ----------------
mx = subs[0]["loc_code"]
bars = "".join(
    f'<div class="brow"><span class="blab">{s["subsystem"]}</span>'
    f'<div class="btrack"><div class="bfill" style="width:{100*s["loc_code"]/mx:.1f}%"></div></div>'
    f'<span class="bval">{s["loc_code"]:,}</span>'
    + (f'<span class="bdata">+{s["loc_data"]:,} data</span>' if s["loc_data"] else "")
    + f'<span class="btests">{s["test_modules"]} test mod.</span></div>'
    for s in subs if s["loc_code"] >= 500)

# ---------------- tickets ----------------
tick_rows = []
for t in tickets:
    subs_badges = " ".join(f'<span class="badge">{s}</span>' for s in t["subsystems"])
    files_li = "".join(f"<li><code>{html.escape(f)}</code></li>" for f in t["files_list"])
    st = stale.get(t["issue"]); cp = coupling.get(t["issue"])
    stale_line = (f"Map staleness for this ticket: checkout is {st['months_after_t0']} months after T0; "
                  f"{st['mods_added']} modules and {st['edges_added']} import edges exist here that the map does not know; "
                  f"{st['touched_absent']} of the {st['touched']} modules the fix touched are absent from the map."
                  if st else "Map staleness: table pending (data/staleness.json).")
    if cp:
        coup_line = ("Hidden tests demand the maintainers' names: " + ", ".join(f"<code>{html.escape(s)}</code>" for s in cp["coupled_symbols"])
                     if cp["coupled"] else "Hidden tests do not depend on names the fix invented.")
    else:
        coup_line = "Name coupling: table pending."
    tick_rows.append(f"""
<details class="ticket"><summary>
  <span class="tno">{t["seq"]}</span>
  <span class="ttitle">{html.escape(t["title"])}</span>
  <span class="tmeta"><a href="{t["issue_url"]}">#{t["issue"]}</a> &middot; <a href="{t["pr_url"]}">PR {t["pr"]}</a>
  &middot; merged {t["merged"]} &middot; {t["files"]} files &middot; <span class="ok">{t["audit"]}</span>{' &middot; <span class="warnb">names</span>' if cp and cp["coupled"] else ''}</span>
</summary>
<div class="tbody"><p class="ovw"><span class="llm">AI-written summary</span> {html.escape(t["overview"])}</p>
<p class="subsline">Subsystems touched: {subs_badges}</p>
<p class="subsline">{stale_line}</p>
<p class="subsline">{coup_line}</p>
<p class="fileshead">Files in the fixing PR (first parent <code>{t["parent"][:9]}</code> to merge <code>{t["commit"][:9]}</code>):</p><ul class="files">{files_li}</ul></div>
</details>""")
tickets_html = "".join(tick_rows)
n_coupled = sum(1 for c in coupling.values() if c["coupled"])
stale_summary = ""
if stale:
    import statistics
    stale_summary = (f"Across the 25 tickets: median symbol survival {statistics.median(r['sym_surv'] for r in stale.values()):.1%}, "
                     f"median import-edge survival {statistics.median(r['edge_surv'] for r in stale.values()):.1%}, "
                     f"{sum(1 for r in stale.values() if r['touched_absent'])} tickets touch a module the map has never seen, "
                     f"maximum staleness {max(r['months_after_t0'] for r in stale.values())} months. Full table: data/staleness.md.")

# ---------------- Gate 2: audit samples rendered for the owner ----------------
def parse_audit(path):
    """Rows of a markdown audit table: | # | fact | command | must appear | result |"""
    rows = []
    if not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) >= 4 and cells[0].isdigit():
            has_window = len(cells) >= 6
            rows.append(dict(n=cells[0], fact=cells[1], cmd=cells[2].replace("\\|", "|"), must=cells[3],
                             window=cells[4].replace("\\|", "|") if has_window else "",
                             result=(cells[5] if has_window else (cells[4] if len(cells) > 4 else ""))))
    return rows

import urllib.parse
REPO = S.get("repo", "yspbob/interpretation-layer-poc")
def issue_link(title, body, label="decision"):
    q = urllib.parse.urlencode({"title": title, "body": body, "labels": label})
    return f"https://github.com/{REPO}/issues/new?{q}"

def md_inline(t):
    t = html.escape(t)
    import re as _re
    return _re.sub(r"`([^`]*)`", r"<code>\1</code>", t)

def audit_table(rows, key):
    if not rows:
        return "<p class=\"small\">Not yet transferred to this repository.</p>"
    def window_html(w):
        if not w: return "<span class=\"small\">(run the command)</span>"
        lines = [md_inline(x) for x in w.split("<br>")]
        return "<div class=\"win\">" + "<br>".join(lines) + "</div>"
    body = "".join(
        f"<tr><td>{r['n']}</td><td>{md_inline(r['fact'])}</td><td>{window_html(r['window'])}<code class=\"cmd\">{html.escape(r['cmd'].strip('`'))}</code></td>"
        f"<td>{md_inline(r['must'])}</td><td class=\"verdict\">"
        + (html.escape(r['result']) if r['result'] else
           f"<label><input type=radio name=\"{key}_{r['n']}\" value=PASS> pass</label> <label><input type=radio name=\"{key}_{r['n']}\" value=FAIL> fail</label>")
        + "</td></tr>" for r in rows)
    return (f"<table class=\"audit\" data-key=\"{key}\"><tr><th>#</th><th>What the map claims</th><th>The frozen code at T0 (and the command that prints it)</th><th>Must appear</th><th>Your verdict</th></tr>{body}</table>")

audit32 = audit_table(parse_audit(P("preregistration", "gate_reports", "audit_sample_32.md")), "a32")
audit8 = audit_table(parse_audit(P("factgraph", "audit_sample_model_refs.md")), "a8")

# ---------------- decisions owed by the owner ----------------
dec_cards = []
for d in S.get("decisions", []):
    body = (f"Decision: {d['title']}\n\nSource file: {d['file']}\n\nOptions: {d['options']}\n"
            f"Current: {d['default'] or 'none recorded'}\n\nMy decision:\n\n(edit here, then submit)\n")
    link = issue_link(f"[decision:{d['id']}] {d['title']}", body)
    dec_cards.append(
        f'<div class="dec"><b>{html.escape(d["title"])}</b>'
        f'<p>{html.escape(d["what"])}</p>'
        f'<p class="small">Options: {html.escape(d["options"])}' + (f' &middot; Current: <b>{html.escape(d["default"])}</b>' if d["default"] else "") +
        f' &middot; File: <code>{html.escape(d["file"])}</code></p>'
        + ("" if d["id"] == "gate2" else f'<a class="btn" target="_blank" rel="noopener" href="{html.escape(link)}">Record decision on GitHub</a>')
        + "</div>")
decisions_html = "".join(dec_cards)
gate2_issue_base = issue_link("[decision:gate2] Gate 2 verdicts", "PLACEHOLDER")

drill_json = json.dumps(drill)
css = open(P("statuspage", "style.css")).read()

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interpretation Layer POC: status and evidence</title>
<style>{css}</style></head><body>
<div class="wip"><b>Work in progress.</b> {html.escape(S["wip_banner"])}</div>
<header><div class="wrap">
<h1>Interpretation Layer POC: status and evidence</h1>
<div class="byline">A live test of the interpretation layer proposed in <a href="https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html">the AI Engineering Playbook</a> (section 4), run on a real public codebase &middot; <a href="https://www.linkedin.com/in/yaroslavpavolotsky">Yaroslav Pavolotskyi</a> &middot; pre-registered experiment, plan {html.escape(S["plan"]["version"])} &middot; <a href="https://github.com/yspbob/interpretation-layer-poc">artifacts published as they are produced</a></div>
</div></header><div class="wrap">

<div class="card"><p><b>What this is.</b> The playbook argues that before an AI coding agent touches a large codebase, it should be handed a curated, checked knowledge base about that codebase: what the parts are, how they depend on each other, and which decisions are already settled. The playbook calls this the interpretation layer, and it is the one part of the book not yet proven anywhere. This experiment builds that layer for NetBox, a real open-source project, then measures the same AI agent fixing 25 real tickets from NetBox's history four ways: with the knowledge base plugged in or not, and with the maintainers' own hand-written agent guide present or not. Every rule, ticket and threshold is committed to the public repository before the results exist, so the outcome cannot be steered after the fact. The results ship whichever way they land. The plan itself, its amendment history and three rounds of independent methodological review are in the repository under <code>preregistration/</code>.</p></div>

<div class="statebar">
<div class="state"><b>Current state</b>{html.escape(S["current_state"])}</div>
<div class="state"><b>Awaiting the owner</b>{html.escape(S["awaiting_owner"])}</div>
<div class="state green"><b>Hypothesis under test</b>{html.escape(S["hypothesis"])}</div>
</div>

<h2>Decisions waiting for the owner</h2>
<p class="small">{html.escape(S.get("decisions_intro",""))}</p>
<div class="decgrid">{decisions_html}</div>

<h2>What keeps this honest</h2>
<p class="small">An experiment like this is easy to rig by accident, and easier on purpose. Each card names one way it could be rigged, and the control that prevents it. Green means the control holds today, amber means work is still owed or a limit is being measured rather than removed, grey means it cannot be tested until a later stage. Each card names the committed file it is derived from.</p>
<div class="raggrid">{rag_html}</div>

<h2>The seven stages</h2>
<div class="card">{pipe_svg}</div>

<h2>Why NetBox: choosing the codebase (Gate 1)</h2>
<div class="card">
<p class="small">{html.escape(g1["narrative"])}</p>
<table><tr><th>Criterion</th>{"".join(f"<th>{html.escape(k)}</th>" for k in scores)}</tr>{sel_rows}{sel_totals}</table>
<p class="small">{html.escape(g1["why"])} Ratified at Gate 1 ({html.escape(g1["ruling"])}).</p>
</div>

<h2>The frozen copy</h2>
<div class="card">
<p class="small">The experiment runs on a fork of <a href="https://github.com/netbox-community/netbox">netbox-community/netbox</a>, frozen at commit <code>{T0}</code> of 27 June 2025. That commit, called T0 throughout, is the parent of the earliest of the 25 fixes, so nothing in the frozen copy knows about any of them. Counted by script from that snapshot: {counts["modules"]:,} Python modules holding {counts["loc_total"]:,} lines ({counts["loc_code"]:,} code, {counts["loc_data"]:,} static data, {counts["loc_mig"]:,} migrations), {counts["symbols"]:,} top-level classes and functions, {counts["imports"]:,} import statements between modules ({counts["edges"]:,} distinct module-to-module edges), {counts["refs"]:,} string model references of which {counts["refs_cross"]:,} cross an app boundary, {counts["subsystems"]} subsystems. Counting rule: {html.escape(S["loc_rule"])}</p>
{bars}
<p class="small">Code lines per subsystem, with migrations and static data excluded. One subsystem, extras, additionally carries {counts["loc_data"]//1000}k lines of static reference data; the map flags it as data so the drafting stage cannot mistake it for logic. The agent files NetBox added for AI coding tools in 2026 are not in this snapshot (it predates them) and are stripped from every later checkout by the harness.</p>
</div>

<h2>The map: how the subsystems depend on each other</h2>
<div class="card">
<p class="small">Each circle is one subsystem, and the bigger the circle, the more code it holds. A line means one subsystem imports from another, and the thicker the line, the more import statements cross between them (pairs with fewer than three are left out to reduce noise). Click a circle to see its busiest modules and what it depends on. Django also couples apps without an import, through string references such as <code>ForeignKey('ipam.VLAN')</code>; those edges are in the second table and in the click-through detail.</p>
{dep_svg}
<details><summary class="small">Table view: top 15 cross-subsystem import dependencies</summary>
<table><tr><th>From</th><th>To</th><th>Import statements</th></tr>
{"".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in edge_table)}
</table></details>
<details><summary class="small">Table view: top 15 cross-app string model references (the edges imports cannot see)</summary>
<table><tr><th>From app</th><th>To app</th><th>References</th></tr>
{"".join(f"<tr><td>{r['a']}</td><td>{r['b']}</td><td>{r['c']}</td></tr>" for r in ref_edges)}
</table></details>
</div>

<h2>Check the map yourself (Gate 2)</h2>
<div class="card">
<p class="small"><b>What this is for.</b> The map was built by script, so the question at Gate 2 is not "is the map true" but "does the script extract what it says it extracts". The owner answers that by checking a random sample of the map's claims against the frozen code. Each row below is one claim, the exact command that shows the relevant lines of the frozen copy, and what must be visible in those lines. If it is there, the row passes; if not, it fails and the extractor has a bug. The samples were drawn at random with a fixed seed (recorded in each file) so the rows could not be chosen to flatter the extractor. With 32 rows and no failures, the extractor's per-fact error rate is below about 9% at 95% confidence (the "rule of three"); the 8 supplementary rows cover the second edge kind added on 3 Sep 2026.</p>
<p class="small"><b>How to run a check.</b> In a clone of NetBox (upstream or the fork), paste the command. <code>git show ea4c205:&lt;path&gt;</code> prints the file exactly as it was at T0, and <code>sed -n 'A,Bp'</code> cuts out lines A to B. Compare what prints with the "must appear" column.</p>
<h3 class="small">The 32-fact sample (import graph, symbols, churn, entry points)</h3>
{audit32}
<h3 class="small">The 8-fact supplement (string model references, added 3 Sep 2026)</h3>
{audit8}
<p><a class="btn" id="gate2btn" href="#" target="_blank" rel="noopener">Submit Gate 2 verdicts on GitHub</a> <span class="small" id="gate2note">Tick pass or fail on every row first; the button opens a pre-filled issue with your verdicts.</span></p>
<p class="small">Sources: <code>preregistration/gate_reports/audit_sample_32.md</code>, <code>factgraph/audit_sample_model_refs.md</code>. Verdicts are recorded by editing the "Result" column of those files; the page reflects them at the next regeneration.</p>
</div>

<h2>The 25 evaluation tickets</h2>
<p class="small">{html.escape(S["ticket_selection_text"])} {html.escape(stale_summary)} Name coupling: {n_coupled} of 25 tickets have hidden tests that import a name the fix invented (data/name_coupling.md). The one-line summaries are AI-written from the issue text and labelled as such; they are not part of the map.</p>
{tickets_html}

<footer>Generated {GENERATED} from source commit <code>{SRC_COMMIT}</code> by <code>statuspage/generate_status_page.py</code>, reading only committed artifacts: <code>statuspage/state.json</code>, <code>factgraph/factgraph.db</code> (file sha256 {FG_SHA}&hellip;, row hash {ROWHASH}&hellip;), <code>statuspage/tickets.json</code>, <code>data/staleness.json</code>, <code>data/name_coupling.json</code>. This page is presentation only. No pipeline stage reads it, and the stage that drafts the knowledge base never sees the ticket list above. The plan ({html.escape(S["plan"]["version"])}, ratified {S["plan"]["ratified"]}), its history and the review rounds live in <code>preregistration/</code>; the final write-up will label everything here as one codebase under lab conditions, not production evidence.</footer>
</div>
<div id="drill"><span class="close" onclick="this.parentNode.style.display='none'">&times;</span><div id="drillbody"></div></div>
<script>
var GATE2_BASE = {json.dumps(gate2_issue_base)};
document.getElementById('gate2btn').addEventListener('click', function(ev){{
  var rows = document.querySelectorAll('table.audit tr'); var lines = []; var missing = 0;
  document.querySelectorAll('table.audit').forEach(function(t){{
    var key = t.getAttribute('data-key');
    t.querySelectorAll('tr').forEach(function(tr){{
      var n = tr.children[0] && tr.children[0].textContent.trim(); if(!n || !/^\d+$/.test(n)) return;
      var sel = tr.querySelector('input[type=radio]:checked');
      var fixed = tr.querySelector('td.verdict') && !tr.querySelector('input[type=radio]') ? tr.querySelector('td.verdict').textContent.trim() : null;
      var v = sel ? sel.value : (fixed || 'NOT CHECKED'); if(v==='NOT CHECKED') missing++;
      lines.push((key==='a32'?'32-fact':'8-fact') + ' row ' + n + ': ' + v);
    }});
  }});
  var body = 'Gate 2 verdicts, submitted from the status page.\\n\\n' + lines.join('\\n') + '\\n\\nRows not checked: ' + missing + '\\n\\nNotes:\\n';
  this.href = GATE2_BASE.replace('PLACEHOLDER', encodeURIComponent(body));
}});
var DRILL = {drill_json};
document.querySelectorAll('.node').forEach(function(n){{
  n.addEventListener('click', function(){{
    var s = n.getAttribute('data-sub'); var d = DRILL[s]; if(!d) return;
    var h = '<h3>' + s + ': ' + d.stats.loc_code.toLocaleString() + ' code lines, ' + d.stats.modules + ' modules, ' + d.stats.test_modules + ' test modules</h3>';
    h += '<p class="small">Imports from: ' + (d.imports_out.map(function(o){{return o.sub + ' (' + o.c + ')';}}).join(', ') || 'nothing internal') + ' &middot; Imported by: ' + (d.imported_in.map(function(o){{return o.sub + ' (' + o.c + ')';}}).join(', ') || 'nothing internal') + ' &middot; String model references to: ' + (d.refs_out.map(function(o){{return o.sub + ' (' + o.c + ')';}}).join(', ') || 'none') + '</p>';
    h += '<table><tr><th>Module (top by fan-in)</th><th>LOC</th><th>Fan-in</th><th>Fan-out</th><th>Commits</th><th>Authors</th></tr>';
    d.top_modules.forEach(function(m){{ h += '<tr><td><code>' + m.module + '</code></td><td>' + m.loc + '</td><td>' + m.fan_in + '</td><td>' + m.fan_out + '</td><td>' + m.commits + '</td><td>' + m.authors + '</td></tr>'; }});
    h += '</table>';
    document.getElementById('drillbody').innerHTML = h;
    document.getElementById('drill').style.display = 'block';
  }});
}});
</script></body></html>"""
# make every section after the state bar collapsible; the first two stay open
import re as _re
def _wrap(m):
    title = m.group(1); body = m.group(2)
    open_attr = " open" if title.startswith(("What keeps this honest", "Decisions")) else ""
    return f'<details class="sec"{open_attr}><summary><h2>{title}</h2></summary>{body}</details>'
page = _re.sub(r"<h2>(.*?)</h2>(.*?)(?=<details class=\"sec\"|<h2>|<footer>)", _wrap, page, flags=_re.S)
open(OUT, "w").write(page)
print("written", OUT, len(page), "bytes; source commit", SRC_COMMIT, "; store", FG_SHA, "rowhash", ROWHASH)
