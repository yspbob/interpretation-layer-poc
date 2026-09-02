#!/usr/bin/env python3
"""M-013 status page generator. Deterministic assembly from committed artifacts:
factgraph.db, preregistration/selected_tickets.md (via tickets.json), the Gate 1
report data, and labelled LLM-written ticket overviews. Regenerate at every phase.
This page is presentation only: no pipeline stage reads it."""
import sqlite3, json, math, html, datetime

DB = "/home/claude/poc/factgraph/factgraph.db"
TICKETS = "/home/claude/poc/statuspage/tickets.json"
OUT = "/home/claude/poc/statuspage/index.html"
FG_SHA = "f760d315f21396cc"
T0 = "ea4c205"
GENERATED = datetime.date.today().isoformat()

NAVY = "#24425f"; NAVY_D = "#16293c"; INK = "#1d2530"; MUT = "#5b6570"
GOOD = "#1a7f37"; WARN = "#b45309"; PEND = "#6b7280"; LINE = "#d8dce1"
BG = "#f7f7f5"; CARD = "#ffffff"

db = sqlite3.connect(DB); db.row_factory = sqlite3.Row
tickets = json.load(open(TICKETS))
subs = [dict(r) for r in db.execute("SELECT * FROM subsystems ORDER BY loc_code DESC")]
sub_edges = {}
for r in db.execute("""SELECT a.subsystem s1, b.subsystem s2, COUNT(*) c FROM imports i
    JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module
    WHERE a.subsystem!=b.subsystem GROUP BY 1,2"""):
    sub_edges[(r["s1"], r["s2"])] = r["c"]

# drill-down data: per subsystem, top modules by fan-in, with churn
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
        WHERE a.subsystem=? AND b.subsystem!=? GROUP BY 1 ORDER BY c DESC LIMIT 6""",
        (s["subsystem"], s["subsystem"]))]
    ins_ = [dict(r) for r in db.execute("""SELECT a.subsystem sub, COUNT(*) c FROM imports i
        JOIN modules a ON i.src=a.module JOIN modules b ON i.dst=b.module
        WHERE b.subsystem=? AND a.subsystem!=? GROUP BY 1 ORDER BY c DESC LIMIT 6""",
        (s["subsystem"], s["subsystem"]))]
    drill[s["subsystem"]] = dict(stats=s, top_modules=mods, imports_out=outs, imported_in=ins_)

# ---------------- subsystem dependency SVG (circle layout, one hue) ----------------
W, H, CX, CY, R = 860, 640, 430, 320, 245
big = [s for s in subs if s["loc_code"] >= 500]
n = len(big)
pos = {}
for i, s in enumerate(big):
    a = -math.pi / 2 + 2 * math.pi * i / n
    pos[s["subsystem"]] = (CX + R * math.cos(a), CY + R * math.sin(a))
maxloc = max(s["loc_code"] for s in big)
edges_svg = []
for (s1, s2), c in sorted(sub_edges.items(), key=lambda kv: kv[1]):
    if s1 not in pos or s2 not in pos or c < 3: continue
    x1, y1 = pos[s1]; x2, y2 = pos[s2]
    mx, my = (x1 + x2) / 2 + (CX - (x1 + x2) / 2) * 0.35, (y1 + y2) / 2 + (CY - (y1 + y2) / 2) * 0.35
    w = 0.6 + math.log2(c)
    op = min(0.12 + c / 200, 0.55)
    edges_svg.append(f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" '
                     f'stroke="{NAVY}" stroke-width="{w:.1f}" opacity="{op:.2f}" class="edge" data-s1="{s1}" data-s2="{s2}"/>')
nodes_svg = []
for s in big:
    x, y = pos[s["subsystem"]]
    r = 10 + 22 * math.sqrt(s["loc_code"] / maxloc)
    lx = x + (18 + r) * (1 if x >= CX else -1) * 0.0
    anchor = "middle"
    ly = y + r + 16 if y >= CY else y - r - 8
    nodes_svg.append(
        f'<g class="node" data-sub="{s["subsystem"]}" style="cursor:pointer">'
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{NAVY}" opacity="0.88" stroke="#fff" stroke-width="2"/>'
        f'<text x="{x:.0f}" y="{ly:.0f}" text-anchor="{anchor}" class="nlabel">{s["subsystem"]}</text>'
        f'<text x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle" class="nnum">{s["loc_code"]//1000}k</text></g>')
dep_svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Subsystem dependency graph">'
           + "".join(edges_svg) + "".join(nodes_svg) + "</svg>")

edge_table = sorted(((s1, s2, c) for (s1, s2), c in sub_edges.items()), key=lambda t: -t[2])[:15]

# ---------------- pipeline SVG ----------------
phases = [
    ("0", "Pick the codebase", "Gate 1", "choose the project to test on", "done", "PASSED: NetBox, R-247"),
    ("1", "Map the codebase", "Gate 2", "build the map by script, hand-check a sample", "active", "AWAITING OWNER: 32-fact sample filed"),
    ("2", "Draft the knowledge", "Gate 3", "AI drafts the pages, every claim cites the map", "pending", ""),
    ("3", "Check the knowledge", "Gate 4", "second AI from another vendor checks every claim", "pending", ""),
    ("4", "Plug it in", "Gate 5", "connect the knowledge base to the agent, dry run", "pending", ""),
    ("5", "Run the test", "Gate 6", "150 runs: same tickets, with and without", "pending", ""),
    ("6", "Publish", "Publish", "results published whichever way they land", "pending", ""),
]
PW, PH = 1180, 240
seg = PW / len(phases)
pipe = []
for i, (num, name, gate, meaning, st, note) in enumerate(phases):
    x = seg * i + seg / 2
    col = GOOD if st == "done" else (WARN if st == "active" else "#aeb6bf")
    icon = "&#10003;" if st == "done" else ("&#9654;" if st == "active" else "")
    if i < len(phases) - 1:
        pipe.append(f'<line x1="{x+42:.0f}" y1="70" x2="{x+seg-42:.0f}" y2="70" stroke="{LINE}" stroke-width="2.5"/>')
    pipe.append(f'<circle cx="{x:.0f}" cy="70" r="26" fill="{col}" opacity="{1 if st!="pending" else 0.55}"/>'
                f'<text x="{x:.0f}" y="63" text-anchor="middle" class="pnum">{num}</text>'
                f'<text x="{x:.0f}" y="80" text-anchor="middle" class="picon">{icon}</text>'
                f'<text x="{x:.0f}" y="118" text-anchor="middle" class="pname">{name}</text>'
                f'<text x="{x:.0f}" y="140" text-anchor="middle" class="pgate">{gate}</text>')
    for j, wline in enumerate(_w := __import__("textwrap").wrap(meaning, 24)[:3]):
        pipe.append(f'<text x="{x:.0f}" y="{158+j*14}" text-anchor="middle" class="pmean">{html.escape(wline)}</text>')
    if note:
        for j, wline in enumerate(__import__("textwrap").wrap(note, 24)[:2]):
            pipe.append(f'<text x="{x:.0f}" y="{206+j*14}" text-anchor="middle" class="pnote" fill="{col}">{html.escape(wline)}</text>')
pipe_svg = f'<svg viewBox="0 0 {PW} 240" role="img" aria-label="POC pipeline: phases and gates">' + "".join(pipe) + "</svg>"

# ---------------- honesty RAG ----------------
rag = [
    ("green", "No knowledge from the future", "The knowledge base is built from the codebase as it stood in June 2025, before the earliest of the 25 test tickets was fixed. The agent cannot be helped by information that did not exist at the time."),
    ("green", "Tickets picked by rule, not by hand", "The 25 tickets were selected by a written rule, published before the selection ran, so none could be cherry-picked to flatter the result. Both amendments to the rule were made before the freeze, with their timing on record."),
    ("green", "The map contains no AI guesses", "The codebase map is extracted by plain scripts, parsers and git history, with no AI involved: it can be incomplete, but it cannot invent. One extraction bug (renamed files undercounted) was found and fixed before the audit sample was drawn, on record."),
    ("green", "The real NetBox project stays untouched", "Everything runs on a frozen private copy. The only planned contact with the live project is a single documentation offer to its maintainers, and only if they want it."),
    ("amber", "Everything locked before results exist", "The tickets, the selection rule and the freeze point are committed. Three things are still to lock before any scored run: the judge model, the exact instructions both agents receive, and the statistics plan."),
    ("amber", "A human checks the map", "32 facts were drawn at random from the map, each with the exact command that verifies it against the code. Until that hand check passes, the map counts as machine-built and unaudited."),
    ("grey", "Both agents get identical instructions", "The two test runs differ in exactly one thing: whether the knowledge base is plugged in. The instructions are word-for-word the same. Checkable at the stage 4 dry run."),
    ("grey", "The judge is chosen before the verdict", "The second-opinion model that checks the drafted knowledge comes from a different vendor and is named, with its instructions and threshold, before any result exists that it could be picked to favour."),
]
rag_html = "".join(
    f'<div class="rag {c}"><span class="dot"></span><b>{html.escape(t)}</b>'
    f'<span class="raglab">{ {"green":"HOLDS","amber":"OPEN","grey":"NOT YET TESTABLE"}[c] }</span>'
    f'<p>{html.escape(d)}</p></div>' for c, t, d in rag)

# ---------------- repo selection ----------------
crit = ["Size 50-500k LOC", "Activity", "Layered architecture", "Containerised tests",
        "Test-carrying fixes", "Thin architecture docs", "Language tooling"]
scores = {"NetBox": [5,5,5,3,5,4,5], "Paperless-ngx": [5,5,3,5,4,5,4], "Wagtail": [5,5,4,3,3,3,5]}
sel_rows = "".join(
    f'<tr><td>{i+1}. {c}</td>' + "".join(
        f'<td class="{ "hi" if scores[k][i]==max(scores[x][i] for x in scores) else "" }">{scores[k][i]}</td>'
        for k in scores) + "</tr>"
    for i, c in enumerate(crit))
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
sub_count = {}
for t in tickets:
    for s in t["subsystems"]:
        if s in drill: sub_count[s] = sub_count.get(s, 0) + 1
tick_rows = []
for t in tickets:
    subs_badges = " ".join(f'<span class="badge">{s}</span>' for s in t["subsystems"])
    files_li = "".join(f"<li><code>{html.escape(f)}</code></li>" for f in t["files_list"])
    tick_rows.append(f"""
<details class="ticket"><summary>
  <span class="tno">{t["seq"]}</span>
  <span class="ttitle">{html.escape(t["title"])}</span>
  <span class="tmeta"><a href="{t["issue_url"]}">#{t["issue"]}</a> &middot; <a href="{t["pr_url"]}">PR {t["pr"]}</a>
  &middot; merged {t["merged"]} &middot; {t["files"]} files &middot; <span class="ok">MATCH</span></span>
</summary>
<div class="tbody"><p class="ovw"><span class="llm">summary</span> {html.escape(t["overview"])}</p>
<p class="subsline">Subsystems touched: {subs_badges}</p>
<p class="fileshead">Files in the fixing PR (merge {t["commit"][:9]}):</p><ul class="files">{files_li}</ul></div>
</details>""")
tickets_html = "".join(tick_rows)

drill_json = json.dumps(drill)

# ---------------- page ----------------
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interpretation Layer POC: status and evidence</title>
<style>
body{{margin:0;background:{BG};color:{INK};font:15px/1.55 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}}
a{{color:{NAVY};}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 20px 60px}}
header{{background:{NAVY_D};color:#fff;padding:26px 0 22px;margin-bottom:26px}}
header .wrap{{padding-bottom:0}}
h1{{margin:0;font-size:26px;font-weight:650}}
.byline{{color:#b8c4d0;font-size:13.5px;margin-top:6px}}
.byline a{{color:#dce6f0}}
h2{{font-size:19px;margin:38px 0 12px;color:{NAVY_D};border-bottom:2px solid {NAVY_D};padding-bottom:6px}}
.card{{background:{CARD};border:1px solid {LINE};border-radius:8px;padding:18px 20px;margin:14px 0}}
.statebar{{display:flex;gap:14px;flex-wrap:wrap;align-items:stretch}}
.state{{flex:1 1 260px;background:{CARD};border:1px solid {LINE};border-left:5px solid {WARN};border-radius:8px;padding:14px 16px}}
.state.green{{border-left-color:{GOOD}}}
.state b{{display:block;font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;color:{MUT};margin-bottom:4px}}
.raggrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:12px}}
.rag{{background:{CARD};border:1px solid {LINE};border-radius:8px;padding:12px 14px;font-size:13.5px}}
.rag p{{margin:6px 0 0;color:{MUT};font-size:12.8px}}
.rag .dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px}}
.rag.green .dot{{background:{GOOD}}} .rag.amber .dot{{background:{WARN}}} .rag.grey .dot{{background:{PEND}}}
.raglab{{float:right;font-size:11px;letter-spacing:.05em;color:{MUT}}}
.rag.green .raglab{{color:{GOOD}}} .rag.amber .raglab{{color:{WARN}}}
svg{{max-width:100%;height:auto;display:block;margin:0 auto}}
.pnum{{font:600 13px sans-serif;fill:#fff}} .picon{{font:11px sans-serif;fill:#fff}}
.pname{{font:600 13.5px sans-serif;fill:{INK}}} .pgate{{font:600 11.5px sans-serif;fill:{NAVY};letter-spacing:.04em}}
.pmean{{font:11.5px sans-serif;fill:{MUT}}} .pnote{{font:600 11px sans-serif}}
.nlabel{{font:600 13px sans-serif;fill:{INK}}} .nnum{{font:600 11px sans-serif;fill:#fff}}
.node:hover circle{{opacity:1}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}
th,td{{padding:7px 10px;text-align:left;border-bottom:1px solid {LINE}}}
th{{background:{NAVY_D};color:#fff;font-weight:600}}
td.hi{{font-weight:700;color:{NAVY}}}
tr.tot td{{font-weight:700;border-top:2px solid {NAVY_D}}}
.brow{{display:flex;align-items:center;gap:10px;margin:5px 0;font-size:13px}}
.blab{{width:105px;text-align:right;color:{INK};font-weight:600}}
.btrack{{flex:1;background:#e8eaed;border-radius:4px;height:16px;position:relative}}
.bfill{{background:{NAVY};height:16px;border-radius:4px}}
.bval{{width:60px;text-align:right;font-variant-numeric:tabular-nums}}
.bdata{{color:{MUT};font-size:12px}} .btests{{color:{MUT};font-size:12px;width:80px}}
.ticket{{background:{CARD};border:1px solid {LINE};border-radius:8px;margin:8px 0;padding:0}}
.ticket summary{{display:flex;gap:12px;align-items:baseline;padding:11px 16px;cursor:pointer;flex-wrap:wrap}}
.ticket summary::-webkit-details-marker{{display:none}}
.tno{{background:{NAVY_D};color:#fff;border-radius:5px;padding:1px 8px;font-size:12.5px;font-weight:600}}
.ttitle{{font-weight:600;flex:1 1 320px}}
.tmeta{{color:{MUT};font-size:12.5px;white-space:nowrap}}
.ok{{color:{GOOD};font-weight:700}}
.tbody{{padding:2px 18px 14px;border-top:1px solid {LINE}}}
.llm{{background:#eef2f7;color:{NAVY};border-radius:4px;padding:1px 6px;font-size:11px;letter-spacing:.03em;text-transform:uppercase}}
.badge{{background:#e8eef5;color:{NAVY_D};border-radius:4px;padding:1px 7px;font-size:12px}}
ul.files{{columns:2;font-size:12.5px;color:{MUT};margin:4px 0}}
.fileshead,.subsline{{font-size:13px;color:{MUT};margin:8px 0 2px}}
#drill{{position:sticky;bottom:0;background:{CARD};border-top:3px solid {NAVY};box-shadow:0 -4px 16px rgba(0,0,0,.08);padding:12px 20px;display:none;max-height:44vh;overflow:auto}}
#drill h3{{margin:0 0 6px;font-size:15px}} #drill .close{{float:right;cursor:pointer;color:{MUT};font-size:18px}}
#drill table{{font-size:12.5px}}
.small{{font-size:12.5px;color:{MUT}}}
footer{{margin-top:44px;padding-top:14px;border-top:1px solid {LINE};font-size:12.5px;color:{MUT}}}
code{{background:#f0f1f3;border-radius:3px;padding:0 4px;font-size:12px}}
</style></head><body>
<header><div class="wrap">
<h1>Interpretation Layer POC: status and evidence</h1>
<div class="byline">A live test of the interpretation layer proposed in <a href="https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html">the AI Engineering Playbook</a> (section 4), run on a real public codebase &middot; <a href="https://www.linkedin.com/in/yaroslavpavolotsky">Yaroslav Pavolotskyi</a> &middot; pre-registered experiment, <a href="https://github.com/yspbob/interpretation-layer-poc">all artifacts public</a></div>
</div></header><div class="wrap">

<div class="card"><p><b>What this is.</b> The playbook argues that before an AI coding agent touches a large codebase, it should be handed a curated, human-checked knowledge base about that codebase: what the parts are, how they depend on each other, and which decisions are already settled. The playbook calls this the interpretation layer, and it is the one part of the book not yet proven anywhere. This experiment builds that layer for NetBox, a real open-source project, then measures the same AI agent fixing 25 real tickets from NetBox's history two ways: with the knowledge base plugged in, and without it. Every rule, ticket and threshold is published before the results exist, so the outcome cannot be steered after the fact. The results ship whichever way they land.</p></div>

<div class="statebar">
<div class="state"><b>Current state</b>Two of the seven stages are done: the codebase is chosen and its map is built. A 32-fact sample of the map is filed for checking. Nothing further has started.</div>
<div class="state"><b>Awaiting the owner</b>One decision is due, and it is mine: hand-checking the 32 sampled facts against the actual code (Gate 2). Nothing else waits on anyone.</div>
<div class="state green"><b>Hypothesis under test</b>An AI agent handed a verified knowledge base about the codebase will produce changes that fit the existing architecture measurably better than the same agent working from the raw code alone.</div>
</div>

<h2>What keeps this honest</h2>
<p class="small">An experiment like this is easy to rig by accident, and easier on purpose. Each card names one way it could be rigged, and the control that prevents it. Green means the control holds today, amber means work is still owed, grey means it cannot be tested until a later stage.</p>
<div class="raggrid">{rag_html}</div>

<h2>The seven stages</h2>
<div class="card">{pipe_svg}</div>

<h2>Why NetBox: choosing the codebase (Gate 1)</h2>
<div class="card">
<p class="small">Eight open-source projects were assessed against the seven criteria in the plan. Five fell out early: saleor was too large, redash is no longer active, directus has licence ambiguity and an unverifiable size, and zulip and Ghost are so well documented already that a generated knowledge base would have little to add. The three finalists were scored 0 to 5 on each criterion:</p>
<table><tr><th>Criterion</th><th>NetBox</th><th>Paperless-ngx</th><th>Wagtail</th></tr>{sel_rows}{sel_totals}</table>
<p class="small">NetBox won on the grounds that matter here. The experiment is about dependency structure, and NetBox has the clearest one, with twelve domain apps importing from a shared core. Its maintainers link nearly every fix back to its issue, which is what makes rule-based ticket selection workable. And it is the only finalist whose size could be verified inside the target band, at 328k lines of Python. Ratified at Gate 1 (R-247, 31 Aug 2026).</p>
</div>

<h2>The frozen copy</h2>
<div class="card">
<p class="small">The experiment runs on a fork of <a href="https://github.com/netbox-community/netbox">netbox-community/netbox</a>, frozen at commit <code>{T0}</code> of 27 June 2025. That commit, called T0 throughout, is the parent of the earliest of the 25 fixes, so nothing in the frozen copy knows about any of them. Counted by script from that snapshot: 965 modules, 4,303 top-level classes and functions, 3,155 import statements between modules, 17 subsystems. Files that carry instructions for AI coding tools are stripped from the copy, so neither test arm gets hidden help.</p>
{bars}
<p class="small">Code lines per subsystem, with migrations and static data excluded. One subsystem, extras, additionally carries 121k lines of static reference data; the map flags it as data so the drafting stage cannot mistake it for logic.</p>
</div>

<h2>The map: how the subsystems depend on each other</h2>
<div class="card">
<p class="small">Each circle is one subsystem, and the bigger the circle, the more code it holds. A line means one subsystem imports from another, and the thicker the line, the more import statements cross between them (pairs with fewer than three are left out to reduce noise). Click a circle to see its busiest modules and what it depends on.</p>
{dep_svg}
<details><summary class="small">Table view: top 15 cross-subsystem dependencies</summary>
<table><tr><th>From</th><th>To</th><th>Import statements</th></tr>
{"".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in edge_table)}
</table></details>
</div>

<h2>The 25 evaluation tickets</h2>
<p class="small">These are 25 real changes from NetBox's history, each a closed issue that the maintainers fixed with tests. In the evaluation, the agent gets each ticket exactly as it stood before the fix existed, and has to produce its own. They were picked by the pre-registered rule, not by hand: the fixing PR had to carry tests, touch at least five files, demonstrably fail those tests before the fix and pass them after, and match the reported symptom under a per-ticket audit. The one-line summaries below are AI-written from the issue text and labelled as such; they are not part of the map.</p>
{tickets_html}

<footer>Generated {GENERATED} by <code>generate_status_page.py</code> from committed artifacts: <code>factgraph.db</code> (sha256 {FG_SHA}…), the pre-registered ticket list, and the Gate 1 report. This page is presentation only. No pipeline stage reads it, and the stage that drafts the knowledge base never sees the ticket list above. The full plan and every ruling live in the project record, and the final write-up will label everything here as one codebase under lab conditions, not production evidence.</footer>
</div>
<div id="drill"><span class="close" onclick="this.parentNode.style.display='none'">&times;</span><div id="drillbody"></div></div>
<script>
var DRILL = {drill_json};
document.querySelectorAll('.node').forEach(function(n){{
  n.addEventListener('click', function(){{
    var s = n.getAttribute('data-sub'); var d = DRILL[s]; if(!d) return;
    var h = '<h3>' + s + ': ' + d.stats.loc_code.toLocaleString() + ' code lines, ' + d.stats.modules + ' modules, ' + d.stats.test_modules + ' test modules</h3>';
    h += '<p class="small">Depends on: ' + (d.imports_out.map(function(o){{return o.sub + ' (' + o.c + ')';}}).join(', ') || 'nothing internal') + ' &middot; Depended on by: ' + (d.imported_in.map(function(o){{return o.sub + ' (' + o.c + ')';}}).join(', ') || 'nothing internal') + '</p>';
    h += '<table><tr><th>Module (top by fan-in)</th><th>LOC</th><th>Fan-in</th><th>Fan-out</th><th>Commits</th><th>Authors</th></tr>';
    d.top_modules.forEach(function(m){{ h += '<tr><td><code>' + m.module + '</code></td><td>' + m.loc + '</td><td>' + m.fan_in + '</td><td>' + m.fan_out + '</td><td>' + m.commits + '</td><td>' + m.authors + '</td></tr>'; }});
    h += '</table>';
    document.getElementById('drillbody').innerHTML = h;
    document.getElementById('drill').style.display = 'block';
  }});
}});
</script></body></html>"""
open(OUT, "w").write(page)
print("written", OUT, len(page), "bytes")
