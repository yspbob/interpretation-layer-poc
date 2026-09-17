import json, random, re, html, sys
batchfile, seed, out, title = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
T0="ea4c205a37baa3e58e6e481158c15c6154cceeff"; BLOB=f"https://github.com/netbox-community/netbox/blob/{T0}/"
CIT=re.compile(r"\[(fg|code):([^\]]+)\]")
subs=json.load(open(batchfile)); slices={s:json.load(open(f"slices/{s}.json")) for s in subs}
claims=[]
for s in subs:
    for fn in ("map.md","patterns.md","adrs.md"):
        for i,line in enumerate(open(f"corpus/{s}/{fn}"),1):
            t=line.rstrip("\n"); st=t.strip()
            if not st or st.startswith("#") or CIT.sub("",st).strip(" -*|")=="": continue
            if CIT.search(t): claims.append((s,fn,i,t))
rnd=random.Random(seed); sample=rnd.sample(claims,20); sample.sort()
def fgrow(s,ref):
    for k,v in slices[s].items():
        if isinstance(v,list):
            for r in v:
                if r.get("id")==ref: return r
    return slices[s]["summary"] if ref==f"subsystems:{s}" else None
def snippet(p,a,b):
    lines=open(f"/home/claude/screen/t0_src/{p}",encoding="utf-8",errors="replace").read().split("\n")[a-1:b]
    return "\n".join(f"{a+j:>5}  {l}" for j,l in enumerate(lines))
def render_fg(s,ref):
    r=fgrow(s,ref); kind=ref.split(":")[0]
    if not r: return '<div class="ev"><span class="btn muted">graph row not found</span></div>'
    p=r.get("path")
    if kind=="symbols":
        a=r["lineno"]; return f'<div class="ev"><a class="btn" href="{BLOB}{p}#L{a}" target="_blank" rel="noopener">{html.escape(p)}:{a}</a><div class="note">Graph row: {r["kind"]} <b>{html.escape(r["name"])}</b>, bases {html.escape(r.get("bases") or "none")}</div><pre>{html.escape(snippet(p,a,a+2))}</pre></div>'
    if kind=="imports":
        a=r["lineno"]; return f'<div class="ev"><a class="btn" href="{BLOB}{p}#L{a}" target="_blank" rel="noopener">{html.escape(p)}:{a}</a><div class="note">Graph row: {html.escape(r["src"])} imports {html.escape(r["dst"])}</div><pre>{html.escape(snippet(p,a,a))}</pre></div>'
    if kind=="model_refs":
        a=r["lineno"]; return f'<div class="ev"><a class="btn" href="{BLOB}{p}#L{a}-L{a+3}" target="_blank" rel="noopener">{html.escape(p)}:{a}</a><div class="note">Graph row: {html.escape(r["class"])}.{html.escape(r["field"])} {html.escape(r["kind"])} refers to {html.escape(r["raw"])}</div><pre>{html.escape(snippet(p,a,a+3))}</pre></div>'
    if kind=="modules":
        return f'<div class="ev"><a class="btn" href="{BLOB}{p}" target="_blank" rel="noopener">{html.escape(p)}</a><div class="note">Graph row: module {html.escape(r["module"])}, {r["loc"]} lines (store count), {r["classes"]} classes, {r["functions"]} functions{", test module" if r.get("is_test") else ""}{", migration" if r.get("is_migration") else ""}</div></div>'
    if kind=="churn":
        return f'<div class="ev"><a class="btn" href="https://github.com/netbox-community/netbox/commits/{T0}/{p}" target="_blank" rel="noopener">history of {html.escape(p)}</a><div class="note">Graph row: {r["commits"]} commits, {r["authors"]} authors, {r["first_commit"]} to {r["last_commit"]}</div></div>'
    if kind=="entrypoints":
        return f'<div class="ev"><a class="btn" href="{BLOB}{p}" target="_blank" rel="noopener">{html.escape(p)}</a><div class="note">Graph row: entry point of kind {html.escape(r["kind"])} (the file runs without being called directly)</div></div>'
    return f'<div class="ev"><span class="btn muted">subsystem summary</span><div class="note">{html.escape(json.dumps(r))}</div></div>'
cards=[]
for n,(s,fn,ln,t) in enumerate(sample,1):
    text=CIT.sub("",t).strip(); ev=[]
    for kind,ref in CIT.findall(t):
        if kind=="code":
            m=re.match(r"^([\w./\-]+):(\d+)(?:-(\d+))?$",ref.strip()); p,a,b=m.group(1),int(m.group(2)),int(m.group(3) or m.group(2))
            ev.append(f'<div class="ev"><a class="btn" href="{BLOB}{p}#L{a}-L{b}" target="_blank" rel="noopener">{html.escape(p)}:{a}{"-"+str(b) if b!=a else ""}</a><pre>{html.escape(snippet(p,a,min(b,a+11)))}{"" if b-a<12 else chr(10)+"  ... (range continues to line "+str(b)+")"}</pre></div>')
        else: ev.append(render_fg(s,ref.strip()))
    cards.append(f'''<article class="claim" id="c{n}"><div class="num">{n}</div><div class="main"><div class="src">{s} / {fn} line {ln}</div><div class="text">{html.escape(text)}</div>{"".join(ev)}</div><div class="side"><label class="tick"><input type="radio" name="v{n}" value="yes" data-id="{n}"> supported</label><label class="tick"><input type="radio" name="v{n}" value="no" data-id="{n}"> not supported</label><label class="tick"><input type="radio" name="v{n}" value="unsure" data-id="{n}"> unsure (partly)</label></div></article>''')
page=f'''<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#F6F7F4;--ink:#1D2622;--mute:#5B6660;--line:#D9DED9;--card:#FFFFFF;--acc:#1F6F63;--acc-ink:#FFFFFF;--code:#EEF1EE}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#131816;--ink:#E6EBE7;--mute:#9AA69F;--line:#2B3430;--card:#1B2220;--acc:#5FB8A8;--acc-ink:#0F1513;--code:#232C28}}}}
:root[data-theme="dark"]{{--bg:#131816;--ink:#E6EBE7;--mute:#9AA69F;--line:#2B3430;--card:#1B2220;--acc:#5FB8A8;--acc-ink:#0F1513;--code:#232C28}}
body{{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:15px;line-height:1.5;padding-inline:16px;padding-block:24px 64px}}
.wrap{{max-width:960px;margin:0 auto}} h1{{font-size:26px;font-weight:600;margin:0 0 6px}} p{{margin:0 0 10px}} .how{{color:var(--mute)}}
.claim{{display:grid;grid-template-columns:34px 1fr 150px;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:10px}}
.num{{font-family:"IBM Plex Mono",monospace;color:var(--mute)}} .src{{font-size:12px;color:var(--mute);letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px}}
.text{{font-weight:500;margin-bottom:8px}} .ev{{margin-top:8px}} .note{{font-size:13px;color:var(--mute);margin-top:4px}}
pre{{background:var(--code);border-radius:6px;padding:8px 10px;font-family:"IBM Plex Mono",monospace;font-size:12px;overflow-x:auto;margin:6px 0 0;white-space:pre}}
.btn{{display:inline-block;background:var(--acc);color:var(--acc-ink);text-decoration:none;padding:5px 10px;border-radius:6px;font-size:13px;font-weight:500}} .btn.muted{{background:var(--code);color:var(--mute)}}
.side{{display:flex;flex-direction:column;gap:6px}} .tick{{font-size:13px;display:flex;gap:6px;align-items:center}}
.summary{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}} .tile{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px;min-width:110px}} .tile b{{font-size:20px;display:block}} .tile span{{color:var(--mute);font-size:13px}}
@media (max-width:640px){{.claim{{grid-template-columns:28px 1fr}}.side{{grid-column:2;flex-direction:row;flex-wrap:wrap}}}}
</style>
<div class="wrap"><h1>{title}</h1>
<p>Twenty claims drawn at random (seed {seed}) from the {len(claims)} cited claims in this batch of the draft corpus at T0 <code>ea4c205</code>. Under each claim is the evidence it cites, shown inline and linked to the pinned source. The mechanical check already confirmed every citation exists; your judgement is whether the evidence supports what the sentence says. Mark each one, then tell Munin the tally.</p>
<div class="summary"><div class="tile"><b id="yes">0</b><span>supported</span></div><div class="tile"><b id="no">0</b><span>not supported</span></div><div class="tile"><b id="unsure">0</b><span>unsure</span></div></div>
{"".join(cards)}
</div>
<script>(function(){{var key='{out}';function load(){{try{{return JSON.parse(localStorage.getItem(key)||'{{}}')}}catch(e){{return {{}}}}}}function save(o){{try{{localStorage.setItem(key,JSON.stringify(o))}}catch(e){{}}}}
var st=load();function tally(){{var c={{yes:0,no:0,unsure:0}};Object.values(st).forEach(function(v){{c[v]=(c[v]||0)+1}});['yes','no','unsure'].forEach(function(k){{document.getElementById(k).textContent=c[k]}})}}
document.querySelectorAll('.tick input').forEach(function(r){{if(st[r.dataset.id]===r.value)r.checked=true;r.addEventListener('change',function(){{st[r.dataset.id]=r.value;save(st);tally()}})}});tally();}})();</script>
'''
open(out+".html","w").write(page); json.dump(sample,open(out+".json","w"),indent=1); print(len(claims),len(page))
