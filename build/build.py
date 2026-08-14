#!/usr/bin/env python3
"""Prototype of the Phase 2 renderer: seed-inventory.md -> one self-contained page."""
import re, html, collections, pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "data" / "inventory.md"
TPL = pathlib.Path(__file__).with_name("shell.html")
OUT = pathlib.Path(__file__).resolve().parents[1] / "public" / "index.html"

SKIP_H2 = ("How to read", "The strategic plan", "What v2", "What v3",
           "What the seed", "The resource layer", "Where this draft",
           "Suggested agenda")

GOAL = {
    "Education & Instruction": "1 Program",
    "Entrepreneurship": "1 Program",
    "Facilities & Equipment": "2 Facilities & Operations",
    "Access & Safety": "2 Facilities & Operations",
    "Lending, Storage & Store": "2 Facilities & Ops / 5 Financial",
    "Membership & Billing": "3 Membership",
    "Member Experience & Retention": "3 Membership",
    "Outreach & Recruitment": "4 Visibility & Outreach",
    "Communications": "4 Visibility & Outreach",
    "Finance & Accounting": "5 Financial strength",
    "Development & Fundraising": "5 Financial strength",
    "Governance & People": "6 Organizational effectiveness",
    "Platform & Meta": "6 Organizational effectiveness",
}
ORDER = list(GOAL)
STATES = ["stable", "watch", "changing", "planned", "degraded", "undefined", "unknown"]

# ---- parse -----------------------------------------------------------------
rows, group, blurbs, cur_blurb = [], None, {}, []
for ln in SRC.read_text().split("\n"):
    m = re.match(r"^## (.+)$", ln)
    if m:
        t = m.group(1).strip()
        group = None if any(k in t for k in SKIP_H2) else t
        cur_blurb = []
        continue
    if group and ln.startswith("_") and ln.endswith("_"):
        blurbs[group] = ln.strip("_")
    if group and ln.startswith("| "):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) == 6 and c[1] != "A" and not set(c[1]) <= set("-: "):
            rows.append(dict(group=group, name=c[0], a=c[1], d=c[2], i=c[3],
                             state=c[4], note=c[5]))

by_group = collections.OrderedDict((g, [r for r in rows if r["group"] == g]) for g in ORDER)
st_tot = collections.Counter(r["state"] for r in rows)
N = len(rows)
change_load = st_tot["watch"] + st_tot["changing"]
cant_say = st_tot["undefined"] + st_tot["unknown"]
planned = st_tot["planned"]
with_strat = sum(1 for r in rows if chr(0x27D0) in r["note"])
p1_rows = [r for r in rows if "\u2605" in r["note"]]

def md(s):
    s = html.escape(s)
    s = re.sub(r"\[(.+?)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

def note_cell(raw):
    """note [⟐ strategies] [‖ docs] — each rendered as its own labelled line."""
    body, _, docs = raw.partition("‖")
    note, _, strat = body.partition("⟐")
    out = md(note.strip())
    if strat.strip():
        out += f'<span class="res strat"><b>Strategy</b>{md(strat.strip())}</span>'
    if docs.strip():
        out += f'<span class="res"><b>Docs</b>{md(docs.strip())}</span>'
    return out

# ---- automation ranking ----------------------------------------------------
ranked = []
for r in rows:
    if r["a"].isdigit() and r["i"].isdigit():
        score = int(r["i"]) * (5 - int(r["a"]))
        if score > 0:
            ranked.append((score, int(r["i"]), r))
ranked.sort(key=lambda t: (-t[0], -t[1], t[2]["name"]))
top = ranked[:12]

unrankable = [r for r in rows if r["i"] == "5" and not r["a"].isdigit()]

# ---- in flux right now ------------------------------------------------------
flux = [r for r in rows if r["state"] in ("changing", "watch")]
flux.sort(key=lambda r: (r["state"] != "changing", r["group"], r["name"]))
influx = "".join(
    f"""      <div class="flux-row"><div><span class="pill {r['state']}">{r['state']}</span></div>
        <div class="what"><b>{md(r['name'])}</b><span class="grp">{html.escape(r['group'])}</span></div>
        <div class="n">{md(r['note'].split(chr(0x2016))[0].split(chr(0x27D0))[0].strip())}</div></div>""" for r in flux)

# ---- fragments -------------------------------------------------------------
tiles = f"""
      <div class="tile"><span class="num">{N}</span><span class="lbl">Processes mapped</span><span class="sub">Across 13 groups · {st_tot['stable']} running normally</span></div>
      <div class="tile bad"><span class="num">{st_tot['degraded']}</span><span class="lbl">Need attention</span><span class="sub">Known broken or unreliable, nobody currently fixing</span></div>
      <div class="tile accent"><span class="num">{change_load}</span><span class="lbl">In flux</span><span class="sub">{st_tot['watch']} being watched, {st_tot['changing']} actively changing</span></div>
      <div class="tile plan"><span class="num">{planned}</span><span class="lbl">Planned, not started</span><span class="sub">Intentions on the roadmap — not failures</span></div>
      <div class="tile gap"><span class="num">{cant_say}</span><span class="lbl">Still unknown</span><span class="sub">No agreed shape yet — ask the person who runs it</span></div>"""

legend = "".join(
    f'<span><i class="swatch" style="background:var(--s-{s})"></i>{s.title()} {st_tot[s]}</span>'
    for s in STATES)

board = []
for g, rs in by_group.items():
    c = collections.Counter(r["state"] for r in rs)
    bars = "".join(f'<i style="flex:{c[s]};background:var(--s-{s})"></i>' for s in STATES if c[s])
    aria = ", ".join(f"{c[s]} {s}" for s in STATES if c[s])
    board.append(f"""      <div class="row-g">
        <div class="gname">{html.escape(g)}</div>
        <div class="bar" role="img" aria-label="{html.escape(g)}: {aria}"><div class="barin">{bars}</div></div>
        <div class="gtot">{len(rs)}</div>
      </div>""")

rank_html = []
for n, (score, _, r) in enumerate(top, 1):
    rank_html.append(f"""      <div class="rank-row"><div class="n">{n:02d}</div>
        <div class="what"><b>{md(r['name'])}</b><em>{md(r['note'].split(chr(0x2016))[0].split(chr(0x27D0))[0].strip())}</em>
        <span class="grp">{html.escape(r['group'])}</span></div>
        <div class="score">{score}<small>I{r['i']} × A{r['a']}</small></div></div>""")

tables = []
for g, rs in by_group.items():
    c = collections.Counter(r["state"] for r in rs)
    blurb = f'<p class="tnote">{md(blurbs[g])}</p>' if g in blurbs else ""
    body = "".join(
        f"""<tr><td class="p">{md(r['name'])}</td>"""
        f"""<td class="s{' q' if not r['a'].isdigit() else (' hi' if r['a']=='1' else '')}">{r['a']}</td>"""
        f"""<td class="s{' q' if not r['d'].isdigit() else (' hi' if r['d']=='0' else '')}">{r['d']}</td>"""
        f"""<td class="s{' q' if not r['i'].isdigit() else (' hi' if r['i']=='5' else '')}">{r['i']}</td>"""
        f"""<td><span class="pill {r['state']}">{r['state']}</span></td>"""
        f"""<td class="n">{note_cell(r['note'])}</td></tr>""" for r in rs)
    counts = " · ".join(f"{c[s]} {s}" for s in STATES if c[s])
    tables.append(f"""      <div class="tblwrap">
        {blurb}<table>
          <caption>{html.escape(g)} <span>{len(rs)} processes · {GOAL[g]}</span><b>{counts}</b></caption>
          <thead><tr><th>Process</th><th>A</th><th>D</th><th>I</th><th>State</th><th>Notes</th></tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>""")

# Rendered only when there is something to show — an empty list under a headline
# claiming unrankable I5 processes exist is worse than no section at all.
if unrankable:
    n_un = len(unrankable)
    word = {1: "One process", 2: "Two processes", 3: "Three processes",
            4: "Four processes"}.get(n_un, f"{n_un} processes")
    items = "".join(f"<li><b>{md(r['name'])}</b> — {md(r['note'])}</li>" for r in unrankable)
    unrank_html = f"""    <div class="unranked">
      <h3>{word} that cannot be ranked at all</h3>
      <p>These carry the highest impact rating on the page — safety, legal, or existential — and
      <strong>no one has scored how manual they are, because no one has described them.</strong>
      An unrankable I5 is worse news than anything in the ranked list above.</p>
      <ul>{items}</ul>
    </div>"""
else:
    unrank_html = ""

nres = sum(1 for r in rows if "‖" in r["note"])

page = TPL.read_text()
for key, val in [("TILES", tiles), ("LEGEND", legend), ("BOARD", "\n".join(board)),
                 ("NRES", str(nres)), ("NGROUPS", str(len(by_group))),
                 ("RANK", "\n".join(rank_html)), ("TABLES", "\n".join(tables)),
                 ("UNRANK", unrank_html), ("INFLUX", influx), ("N", str(N)),
                 ("NCHANGING", str(st_tot["changing"])), ("NWATCH", str(st_tot["watch"])),
                 ("CHANGELOAD", str(change_load)), ("CANTSAY", str(cant_say)),
                 ("DEGRADED", str(st_tot["degraded"])), ("UNDEF", str(st_tot["undefined"])),
                 ("STABLE", str(st_tot["stable"])), ("PLANNED", str(planned)), ("WITHSTRAT", str(with_strat)), ("NP1", str(len(p1_rows)))]:
    page = page.replace("{{" + key + "}}", val)
left = re.findall(r"\{\{[A-Z]+\}\}", page)
if left:
    raise SystemExit(f"unrendered placeholders: {sorted(set(left))}")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
print(f"resource-linked rows: {nres}")
print(f"wrote {OUT} — {N} processes, {len(tables)} groups, change load {change_load}, can't-say {cant_say}")
