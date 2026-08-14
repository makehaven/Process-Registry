#!/usr/bin/env python3
"""Prototype of the Phase 2 renderer: seed-inventory.md -> one self-contained page."""
import re, html, collections, pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "data" / "inventory.md"
TPL = pathlib.Path(__file__).with_name("shell.html")
OUT = pathlib.Path(__file__).resolve().parents[1] / "public" / "index.html"
REPO = "https://github.com/makehaven/makehaven-website/tree/master"

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

# ---- documentation floor ----------------------------------------------------
# A process that runs as code (A4+) has a maintained implementation, and that
# implementation is a current description of what happens — better than most
# SOPs, because it cannot drift from the behaviour it defines. Such rows are
# floored at D2. Applied here rather than edited into inventory.md so the raw
# assessment stays intact and the rule is visible and reversible in one place.
# The floor stops at D2: D3 needs a second person to have worked from it.
n_floored = 0
for r in rows:
    if r["a"].isdigit() and int(r["a"]) >= 4 and r["d"].isdigit() and int(r["d"]) < 2:
        r["d"], r["d_floored"] = "2", True
        n_floored += 1

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

def strip_history(note):
    """Drop drafting provenance ("Corrected from `unknown`.", "(JR, round 2)")
    while keeping any substantive clause that was riding along with it. The
    source file keeps the full text; only the rendered page is cleaned."""
    def fix(m):
        rest = re.sub(r"^Corrected from\s*`[^`]*`(\s*to a named weak point)?", "", m.group(1))
        rest = rest.lstrip(" .,;—-")
        return f"**{rest[0].upper()}{rest[1:]}**" if rest else ""
    note = re.sub(r"\*\*(Corrected from[^*]*?)\*\*", fix, note)
    note = re.sub(r"\s*\*?\(JR,\s*round\s*\d\)\*?", "", note)
    note = re.sub(r"^[\s.,;—-]+", "", note)
    note = re.sub(r"\s{2,}", " ", note)
    note = re.sub(r"\s+([.,])", r"\1", note).strip()
    return note[0].upper() + note[1:] if note else note

# Severity of each score, so the digit can carry a status colour. The digit is
# always rendered, so colour is redundant encoding rather than the only signal.
SEV = {"a": {"1": "crit", "2": "warn", "3": "mid", "4": "good", "5": "good"},
       "d": {"0": "crit", "1": "warn", "2": "good", "3": "good"},
       "i": {"5": "crit", "4": "warn", "3": "mid", "2": "low", "1": "low"}}

def score_cell(axis, v):
    return f'<td class="s sc-{SEV[axis].get(v, "q")}">{html.escape(v)}</td>'

# Optional fields, each introduced by its own sigil so the note stays one cell
# and rows that omit a field cost nothing. Order in the source is by convention
# description ⚑owner ◷reviewed ⚙code ⟐strategy ‖docs, but parsing does not
# depend on that order.
SIGILS = {"⚑": "owner", "◷": "reviewed", "⚙": "code", "⚠": "raised",
          "⟐": "strategy", "‖": "docs"}

def parse_note(raw):
    """Split a note cell into its prose and whichever optional fields it carries."""
    parts, cur, buf = {}, "note", []
    for ch in raw:
        if ch in SIGILS:
            parts[cur] = "".join(buf).strip()
            cur, buf = SIGILS[ch], []
        else:
            buf.append(ch)
    parts[cur] = "".join(buf).strip()
    parts["note"] = strip_history(parts.get("note", ""))
    return parts

def plain_note(raw):
    """Just the prose: no optional fields, no drafting history."""
    return parse_note(raw)["note"]

def code_links(spec):
    """Module names -> links to the module directory on GitHub."""
    out = []
    for m in [x.strip() for x in spec.split(",") if x.strip()]:
        out.append(f'<a href="{REPO}/web/modules/custom/{m}" target="_blank" '
                   f'rel="noopener"><code>{html.escape(m)}</code></a>')
    return " · ".join(out)

def note_cell(raw):
    """Prose first, then each optional field as its own labelled line."""
    p = parse_note(raw)
    out = md(p["note"])
    if p.get("raised"):
        out += f'<span class="res raised"><b>Raised</b>{md(p["raised"])}</span>'
    if p.get("code"):
        out += f'<span class="res code"><b>Code</b>{code_links(p["code"])}</span>'
    if p.get("strategy"):
        out += f'<span class="res strat"><b>Strategy</b>{md(p["strategy"])}</span>'
    if p.get("docs"):
        out += f'<span class="res"><b>Docs</b>{md(p["docs"])}</span>'
    meta = []
    if p.get("owner"):
        meta.append(f'<b>Owner</b> {md(p["owner"])}')
    meta.append(f'<b>Reviewed</b> {md(p["reviewed"])}' if p.get("reviewed")
                else '<b>Reviewed</b> <i class="never">never</i>')
    out += f'<span class="res meta">{" · ".join(meta)}</span>'
    return out

# ---- automation ranking ----------------------------------------------------
ranked = []
for r in rows:
    if r["a"].isdigit() and r["i"].isdigit():
        score = int(r["i"]) * (5 - int(r["a"]))
        if score > 0:
            ranked.append((score, int(r["i"]), r))
ranked.sort(key=lambda t: (-t[0], -t[1], t[2]["name"]))
# A dedicated tab has room for more than a dozen. Show 30 and keep the rest
# one click away rather than truncating silently.
SHOWN = 30
top = ranked

unrankable = [r for r in rows if r["i"] == "5" and not r["a"].isdigit()]

# ---- raised by people -------------------------------------------------------
# The ranking is a formula and cannot know what staff have noticed. Rows
# carrying ⚠ were flagged by a person; they belong next to the ranking, not
# inside it, because they are judgement rather than arithmetic.
raised = [(r, parse_note(r["note"])) for r in rows]
raised = [(r, f) for r, f in raised if f.get("raised")]
raised.sort(key=lambda t: (t[0]["group"], t[0]["name"]))
if raised:
    items = "".join(
        f"""      <div class="raise-row">
        <div class="what"><b>{md(r['name'])}</b><span class="grp">{html.escape(r['group'])}</span></div>
        <div class="n">{md(f['raised'])}</div>
        <div class="st"><span class="pill {r['state']}">{r['state']}</span></div></div>"""
        for r, f in raised)
    raised_html = f"""  <section>
    <h2>Raised by people</h2>
    <p class="sec-note">
      The ranking above is arithmetic — impact multiplied by how manual something still is.
      It cannot know what staff have noticed. These {len(raised)} were flagged by a person, and
      that is a different and often better signal.
    </p>
    <div class="raised">
{items}
    </div>
  </section>"""
else:
    raised_html = ""

# ---- in flux right now ------------------------------------------------------
flux = [r for r in rows if r["state"] in ("changing", "watch")]
flux.sort(key=lambda r: (r["state"] != "changing", r["group"], r["name"]))
influx = "".join(
    f"""      <div class="flux-row"><div><span class="pill {r['state']}">{r['state']}</span></div>
        <div class="what"><b>{md(r['name'])}</b><span class="grp">{html.escape(r['group'])}</span></div>
        <div class="n">{md(plain_note(r['note']))}</div></div>""" for r in flux)

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
    extra = "" if n <= SHOWN else " rank-extra"
    rank_html.append(f"""      <div class="rank-row{extra}"{'' if n <= SHOWN else ' hidden'}><div class="n">{n:02d}</div>
        <div class="what"><b>{md(r['name'])}</b><em>{md(plain_note(r['note']))}</em>
        <span class="grp">{html.escape(r['group'])}</span></div>
        <div class="score">{score}<small>I{r['i']} × A{r['a']}</small></div></div>""")

tables = []
for g, rs in by_group.items():
    c = collections.Counter(r["state"] for r in rs)
    blurb = f'<p class="tnote">{md(blurbs[g])}</p>' if g in blurbs else ""
    body = "".join(
        f"""<tr><td class="p">{md(r['name'])}</td>"""
        f"""{score_cell('a', r['a'])}{score_cell('d', r['d'])}{score_cell('i', r['i'])}"""
        f"""<td><span class="pill {r['state']}">{r['state']}</span></td>"""
        f"""<td class="n">{note_cell(r['note'])}</td></tr>""" for r in rs)
    counts = " · ".join(f"{c[s]} {s}" for s in STATES if c[s])
    tables.append(f"""      <div class="tblwrap">
        {blurb}<table>
          <caption>{html.escape(g)} <span>{len(rs)} processes · {GOAL[g]}</span><b>{counts}</b></caption>
          <thead><tr><th>Process</th><th>Auto</th><th>Doc</th><th>Impact</th><th>State</th><th>Notes</th></tr></thead>
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
n_auto   = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) >= 4)
n_manual = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) <= 2)
n_manual_undoc = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) <= 2
                     and r["d"].isdigit() and int(r["d"]) <= 1)
n_d3 = sum(1 for r in rows if r["d"] == "3")
fields = [parse_note(r["note"]) for r in rows]
n_owner    = sum(1 for f in fields if f.get("owner"))
n_reviewed = sum(1 for f in fields if f.get("reviewed"))
n_code     = sum(1 for f in fields if f.get("code"))
n_never    = N - n_reviewed

page = TPL.read_text()
for key, val in [("TILES", tiles), ("LEGEND", legend), ("BOARD", "\n".join(board)),
                 ("NRES", str(nres)), ("NGROUPS", str(len(by_group))),
                 ("NAUTO", str(n_auto)), ("NMANUAL", str(n_manual)),
                 ("NMANUALUNDOC", str(n_manual_undoc)), ("ND3", str(n_d3)),
                 ("NFLOORED", str(n_floored)), ("NOWNER", str(n_owner)),
                 ("NREVIEWED", str(n_reviewed)), ("NCODE", str(n_code)),
                 ("NNEVER", str(n_never)), ("NRANK", str(len(top))), ("NSHOWN", str(SHOWN)),
                 ("NMORE", str(max(0, len(top) - SHOWN))), ("RAISED", raised_html),
                 ("NRAISED", str(len(raised))),
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
print(f"resource-linked rows: {nres}; D2 floor applied to {n_floored} code-run rows")
print(f"coverage — owner {n_owner}/{N}, reviewed {n_reviewed}/{N}, code {n_code}/{N}")
print(f"wrote {OUT} — {N} processes, {len(tables)} groups, change load {change_load}, can't-say {cant_say}")
