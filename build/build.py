#!/usr/bin/env python3
"""Prototype of the Phase 2 renderer: seed-inventory.md -> one self-contained page."""
import re, html, json, collections, pathlib

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
"""State vocabulary, ordered from settled to least settled.

`degraded` and `unoptimized` are both deficits, but they are different problems
and were previously collapsed into one word. `degraded` means the thing fails:
something that is supposed to happen does not, whether it broke or never once
fired. `unoptimized` means the thing does what it was built to do and was simply
never built far enough. Calling the second one "degraded" implied a regression
that never happened, and made 27 rows look like an emergency when 17 of them are
ordinary unfinished work.
"""
STATES = ["stable", "watch", "changing", "planned",
          "unoptimized", "degraded", "undefined", "unknown"]

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
p1_rows = [r for r in rows if "⟐" in r["note"]
            and "Priority ·" in r["note"].split("⟐", 1)[1]]

# ---- stable process ids -----------------------------------------------------
# Votes and comments live in Firestore keyed by these, so they have to survive a
# rebuild. Group + name is the only pair the inventory guarantees to be unique,
# and it stays legible in the exported digest — which matters, because a human
# reads that digest. Renaming a process orphans its votes; the digest reports
# orphans rather than silently dropping them.
def pid(group, name):
    raw = f"{group} {name}"
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower().replace("&", " and ")).strip("-")
    return slug[:120]


for r in rows:
    r["pid"] = pid(r["group"], r["name"])

_dupes = [k for k, n in collections.Counter(r["pid"] for r in rows).items() if n > 1]
if _dupes:
    raise SystemExit(f"duplicate process ids — votes would collide: {_dupes}")


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

# Colour flags a deficit and nothing else. The three axes have different ranges
# and opposite polarity — Auto 1-5 and Doc 0-3 are better when high, Impact 1-5
# is worse when high — so a hand-written table of which digits to tint had to be
# read against three different scales to check, and the printed key claimed
# "1 = worst" while the Impact column coloured 5.
#
# So it is derived instead. Each scale declares its range and which end is the
# deficit; severity is the position along that scale normalised to 0-1, and the
# same two thresholds apply to all three. Adding a scale, or changing a range,
# cannot now produce a column that is coloured on a different rule from its
# neighbours — and the key on the page is generated from this, so it cannot
# describe something the table is not doing.
SCALES = {
    "a": {"label": "Auto",   "lo": 1, "hi": 5, "worst": "low"},
    "d": {"label": "Doc",    "lo": 0, "hi": 3, "worst": "low"},
    "i": {"label": "Impact", "lo": 1, "hi": 5, "worst": "high"},
}
CRIT, WARN = 0.80, 0.55


def deficit(axis, v):
    """How far this value sits toward the bad end of its own scale, 0.0-1.0."""
    s = SCALES[axis]
    frac = (int(v) - s["lo"]) / (s["hi"] - s["lo"])
    return 1 - frac if s["worst"] == "low" else frac


def band(axis, v):
    d = deficit(axis, v)
    return "crit" if d >= CRIT else "warn" if d >= WARN else "ok"


SEV = {ax: {str(v): band(ax, v)
            for v in range(s["lo"], s["hi"] + 1) if band(ax, v) != "ok"}
       for ax, s in SCALES.items()}

# On a phone the table becomes a stack of cards and the column headers go away,
# which would leave three bare digits meaning nothing. Each score cell carries
# its own label so CSS can put it back with ::before at narrow widths.
AXIS_LABEL = {"a": "Auto", "d": "Doc", "i": "Impact"}


def score_cell(axis, v):
    cls = SEV[axis].get(v, "q" if not v.isdigit() else "ok")
    return (f'<td class="s sc-{cls}" data-l="{AXIS_LABEL[axis]}">'
            f'{html.escape(v)}</td>')

# Optional fields, each introduced by its own sigil so the note stays one cell
# and rows that omit a field cost nothing. Order in the source is by convention
# description ◷reviewed ⚙code ⟐strategy ‖docs, but parsing does not
# depend on that order.
SIGILS = {"◷": "reviewed", "⚙": "code", "⚠": "raised",
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
    # Only rows a person actually confirmed carry a line. How much is unverified
    # is reported once, in the inventory header, rather than stamped on ninety-odd
    # rows as a reproach.
    if p.get("reviewed"):
        out += f'<span class="res meta"><b>Reviewed</b> {md(p["reviewed"])}</span>'
    return out

# ---- automation ranking ----------------------------------------------------
# Membership is a separate question from order, and it used to be neither: the
# only filter was score > 0, and since nothing in the registry is A5 the term
# (5 - A) is never zero, so 186 of 187 processes "made" the list. A ranking that
# contains everything is a sorted inventory, not a shortlist.
#
# A row now has to have something actually wrong with it:
#   - a named deficit (degraded or unoptimized) always keeps its place, or
#   - it is not yet both automated and documented, and it matters enough that
#     fixing it is worth someone's week.
# Automated *and* documented is the definition of done here — A4 is "automated,
# humans handle exceptions" and D2 is "current SOP exists" — so those rows are
# finished, not merely un-started. And an I1 or I2 annoyance is a real thing to
# improve one day, but it is not what "where should effort go next" is asking.
FINISHED_A, FINISHED_D, WORTH_IT_I = 4, 2, 3


def needs_work(r):
    if r["state"] in ("degraded", "unoptimized"):
        return True
    if not (r["a"].isdigit() and r["i"].isdigit()):
        return False
    if int(r["a"]) >= FINISHED_A and r["d"].isdigit() and int(r["d"]) >= FINISHED_D:
        return False
    return int(r["i"]) >= WORTH_IT_I


ranked = []
for r in rows:
    if needs_work(r) and r["a"].isdigit() and r["i"].isdigit():
        score = int(r["i"]) * (5 - int(r["a"]))
        if score > 0:
            ranked.append((score, int(r["i"]), r))

n_settled = N - len(ranked)
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
      <div class="tile bad"><span class="num">{st_tot['degraded']}</span><span class="lbl">Failing now</span><span class="sub">Something that should happen does not — nobody currently fixing</span></div>
      <div class="tile unopt"><span class="num">{st_tot['unoptimized']}</span><span class="lbl">Never built out</span><span class="sub">Works as far as it goes; the work was just never finished</span></div>
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

# The rank rows carry their base score as data so the client can re-sort them
# once votes load, without a second copy of the arithmetic living in JS.
rank_html = []
for n, (score, _, r) in enumerate(top, 1):
    extra = "" if n <= SHOWN else " rank-extra"
    rank_html.append(f"""      <div class="rank-row{extra}" data-pid="{r['pid']}" data-base="{score}" data-rank="{n}"{'' if n <= SHOWN else ' hidden'}><div class="n">{n:02d}</div>
        <div class="what"><b>{md(r['name'])}</b><em>{md(plain_note(r['note']))}</em>
        <span class="grp">{html.escape(r['group'])}</span>
        <div class="vote" data-pid="{r['pid']}" hidden>
          <button type="button" class="vt up" data-v="1" aria-label="More important than ranked">&#9650;<span class="c">0</span></button>
          <button type="button" class="vt down" data-v="-1" aria-label="Less important than ranked">&#9660;<span class="c">0</span></button>
          <button type="button" class="vt say" aria-label="Comment on this process">Comment</button>
          <span class="movecue"></span>
        </div></div>
        <div class="score"><span class="final">{score}</span><small>I{r['i']} &times; A{r['a']}<span class="adj"></span></small></div></div>""")

tables = []
for g, rs in by_group.items():
    c = collections.Counter(r["state"] for r in rs)
    blurb = f'<p class="tnote">{md(blurbs[g])}</p>' if g in blurbs else ""
    body = "".join(
        f"""<tr data-pid="{r['pid']}"><td class="p">{md(r['name'])}"""
        f"""<button type="button" class="rowsay" data-pid="{r['pid']}" """
        f"""aria-label="Comment on {html.escape(r['name'], quote=True)}">Comment</button></td>"""
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
n_reviewed = sum(1 for f in fields if f.get("reviewed"))
n_code     = sum(1 for f in fields if f.get("code"))
n_never    = N - n_reviewed

# The comment panel lets someone pick any process, not just one they can see on
# the current tab, so it needs the full list. Emitted as JSON rather than scraped
# from the DOM because the inventory tab is filtered in place.
manifest = json.dumps(
    [{"pid": r["pid"], "name": re.sub(r"[*`]", "", r["name"]),
      "group": r["group"], "state": r["state"]}
     for r in sorted(rows, key=lambda r: (r["group"], r["name"]))],
    ensure_ascii=False, separators=(",", ":"))

# The key used to be hand-written and said "1 — worst on that axis", which is
# true for Auto and Doc and wrong for Impact, where 5 is the bad end. Generated
# from SCALES it shows the actual digits each column tints.
key_bits = []
for _ax, _s in SCALES.items():
    _vals = sorted((v for v in range(_s["lo"], _s["hi"] + 1) if band(_ax, v) != "ok"),
                   key=lambda v: -deficit(_ax, v))
    _chips = "".join(f'<i class="k-{band(_ax, v)}">{v}</i>' for v in _vals)
    key_bits.append(f'<span><b>{_s["label"]}</b>{_chips}</span>')
scorekey = "".join(key_bits)

page = TPL.read_text()
for key, val in [("TILES", tiles), ("LEGEND", legend), ("BOARD", "\n".join(board)),
                 ("NRES", str(nres)), ("NGROUPS", str(len(by_group))),
                 ("NAUTO", str(n_auto)), ("NMANUAL", str(n_manual)),
                 ("NMANUALUNDOC", str(n_manual_undoc)), ("ND3", str(n_d3)),
                 ("NFLOORED", str(n_floored)),
                 ("NREVIEWED", str(n_reviewed)), ("NCODE", str(n_code)),
                 ("NNEVER", str(n_never)), ("NRANK", str(len(top))), ("NSHOWN", str(SHOWN)),
                 ("NMORE", str(max(0, len(top) - SHOWN))), ("RAISED", raised_html),
                 ("MANIFEST", manifest), ("SCOREKEY", scorekey),
                 ("NSETTLED", str(n_settled)),
                 ("NRAISED", str(len(raised))),
                 ("RANK", "\n".join(rank_html)), ("TABLES", "\n".join(tables)),
                 ("UNRANK", unrank_html), ("INFLUX", influx), ("N", str(N)),
                 ("NCHANGING", str(st_tot["changing"])), ("NWATCH", str(st_tot["watch"])),
                 ("CHANGELOAD", str(change_load)), ("CANTSAY", str(cant_say)),
                 ("DEGRADED", str(st_tot["degraded"])), ("UNOPT", str(st_tot["unoptimized"])),
                 ("DEFICIT", str(st_tot["degraded"] + st_tot["unoptimized"])),
                 ("UNDEF", str(st_tot["undefined"])),
                 ("STABLE", str(st_tot["stable"])), ("PLANNED", str(planned)), ("WITHSTRAT", str(with_strat)), ("NP1", str(len(p1_rows)))]:
    page = page.replace("{{" + key + "}}", val)
left = re.findall(r"\{\{[A-Z]+\}\}", page)
if left:
    raise SystemExit(f"unrendered placeholders: {sorted(set(left))}")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
print(f"resource-linked rows: {nres}; D2 floor applied to {n_floored} code-run rows")
print(f"coverage — reviewed {n_reviewed}/{N}, code {n_code}/{N}")
print(f"wrote {OUT} — {N} processes, {len(tables)} groups, change load {change_load}, can't-say {cant_say}")
