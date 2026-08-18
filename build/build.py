#!/usr/bin/env python3
"""Prototype of the Phase 2 renderer: seed-inventory.md -> one self-contained page."""
import re, sys, html, json, collections, pathlib

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

`broken` and `optimizable` are both deficits, but they are different problems
and were previously collapsed into one word. `broken` means the thing fails:
something that is supposed to happen does not, whether it broke or never once
fired. `optimizable` means the thing does what it was built to do and was simply
never built to its end goal. Collapsing the second into the first implied a
regression that never happened, and made 27 rows look like an emergency when 17
of them are ordinary unfinished work.

These words are the whole vocabulary — the tiles on the front page use them
verbatim rather than a friendlier synonym. They used to differ ("Failing now"
over `degraded`, "Never built out" over `unoptimized`), which meant the number a
reader saw on the front page named a state they could not then find, because the
inventory filter matches the row text and the row said something else.

`optimizable` is deliberately narrow: the thing runs and was never built to its
end goal. It does not mean "could be improved" — read that way it would cover
nearly all 188 rows and the count would stop carrying information. A row where
nothing exists yet is `planned`, not `optimizable`.

`idea` is weaker than `planned` and the distinction is commitment. `planned` is
a confirmed intention — someone has said we will do this. `idea` is under
consideration: a brainstorm, a research question, a maybe. It exists so that
maybes have somewhere to live without being overstated as commitments, and it is
deliberately inert — excluded from the Next ranking and the change load, because
a thing nobody has committed to cannot be urgent.
"""
STATES = ["stable", "watch", "changing", "planned", "idea",
          "optimizable", "broken", "undefined", "unknown"]

# Front-page tiles and inventory badges must name a state identically or the
# filter cannot find what the tile is counting; TILE_COPY keeps the gloss beside
# the word instead of replacing it.
TILE_COPY = {
    "broken":      "Something that should happen does not — nobody currently fixing",
    "optimizable": "Runs, but was never built to its end goal — not merely improvable",
}

# ---- parse -----------------------------------------------------------------
rows, group, blurbs, cur_blurb = [], None, {}, []
for ln in SRC.read_text().split("\n"):
    m = re.match(r"^## (.+)$", ln)
    if m:
        t = m.group(1).strip()
        group = None if any(k in t for k in SKIP_H2) else t
        cur_blurb = []
        continue
    # Group blurbs wrap across source lines like all prose here, so accumulate
    # from the opening underscore to the closing one. The old single-line test
    # meant every wrapped blurb silently never rendered.
    if group and (cur_blurb or ln.startswith("_")):
        cur_blurb.append(ln)
        if ln.endswith("_"):
            blurbs[group] = " ".join(cur_blurb).strip("_")
            cur_blurb = []
        continue
    if group and ln.startswith("| "):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) == 6 and c[1] != "A" and not set(c[1]) <= set("-: "):
            rows.append(dict(group=group, name=c[0], a=c[1], d=c[2], i=c[3],
                             state=c[4], note=c[5]))

# ---- state vocabulary guard -------------------------------------------------
# A state word outside STATES parses fine and then vanishes: it is missing from
# the legend and the group bars (both of which loop over STATES), it has no
# `.pill` rule so the badge renders unstyled, and the recent-changes scanner
# filters on the same set so edits to the row are invisible there too. Two rows
# spent several days as `degraded` — a word this vocabulary retired — before
# anyone noticed the counts no longer summed to N. Failing the build is the only
# way that stays noticed.
_bad = sorted({r["state"] for r in rows} - set(STATES))
if _bad:
    for w in _bad:
        for r in rows:
            if r["state"] == w:
                print(f"  {w!r}: {r['group']} / {r['name']}", file=sys.stderr)
    sys.exit(f"inventory.md uses state(s) not in the vocabulary: {_bad}\n"
             f"Valid states: {STATES}\n"
             "Either re-score those rows or add the word to STATES, TILE_COPY "
             "if it needs a gloss, and a .pill/--s- rule in build/shell.html.")

# ---- documentation floor ----------------------------------------------------
# A process that runs as code has a maintained implementation, and that
# implementation is a current description of what happens — better than most
# SOPs, because it cannot drift from the behaviour it defines. Such rows are
# floored at D3. Applied here rather than edited into inventory.md so the raw
# assessment stays intact and the rule is visible and reversible in one place.
# The floor stops at D3: D4 needs a second person to have worked from it.
#
# It requires a named module, not just an A4 score. Half the rows this rule used
# to raise (13 of 26) named no module anywhere — so "the implementation is the
# description" was asserting a description that nothing in the registry pointed
# at. Comped / sliding-scale / sponsored memberships was one of them: A4 because
# the join form is automated, floored to "a durable description exists" when the
# eligibility policy is written down nowhere. An A4 score says a process runs
# itself; only a module says where to read what it does.
n_floored = 0
for r in rows:
    if (r["a"].isdigit() and int(r["a"]) >= 4 and "⚙" in r["note"]
            and r["d"].isdigit() and int(r["d"]) < 3):
        r["d"], r["d_floored"] = "3", True
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

# How a row's score got to where it is belongs to the registry's own history, not
# to the process. A reader meeting a row for the first time wants to know what the
# thing is and where it stands; "Corrected from `unknown`", "Upgraded from
# `degraded`" and "Corrected twice" all describe edits to this file instead. The
# source keeps the full text — the audit trail is real and worth having — and only
# the rendered page is cleaned.
PROVENANCE = re.compile(
    r"""^(?:Corrected|Upgraded|Downgraded|Re-?scored|Revised|Reclassified)
         (?:\s+(?:from|to)\s*`[^`]*`)?          # ...from `unknown`
         (?:\s*(?:twice|\d+\s*times))?          # ...twice
         (?:\s*to\s+a\s+named\s+weak\s+point)?
      """, re.X | re.I)


def strip_history(note):
    """Drop drafting provenance while keeping any substantive clause riding along.

    "**Corrected from `unknown` — better automated than assumed.** Instructors
    submit hours..." keeps the judgement and the description, losing only the
    fact that this cell used to read `unknown`.
    """
    def fix(m):
        rest = PROVENANCE.sub("", m.group(1)).lstrip(" .,;—-")
        return f"**{rest[0].upper()}{rest[1:]}**" if rest else ""
    note = re.sub(r"\*\*([^*]*?)\*\*",
                  lambda m: fix(m) if PROVENANCE.match(m.group(1)) else m.group(0), note)
    # The same sentence unbolded, and the roadmap boilerplate that only restates
    # the `planned` badge sitting next to it.
    note = PROVENANCE.sub("", note)
    note = re.sub(r"Confirmed by JR as an intention we have not started\s*—\s*"
                  r"a roadmap item, not a broken process\.?", "", note)
    note = re.sub(r"\s*\*?\(JR,\s*round\s*\d\)\*?", "", note)
    note = re.sub(r"^[\s.,;—-]+", "", note)
    note = re.sub(r"\s{2,}", " ", note)
    note = re.sub(r"\s+([.,])", r"\1", note).strip()
    return note[0].upper() + note[1:] if note else note

# Colour flags a deficit and nothing else, and only two of the three axes carry
# one. Auto and Doc are deficit scales and they run the same way — low is bad —
# so a single sentence covers both: the two lowest values are flagged, red for
# the worse of the two. The reader never has to know that the ranges differ.
#
# Impact used to be in that set and should not have been. I5 is "safety, legal
# or existential": that is how much a process matters, not something wrong with
# it, and needs_work() below already treats it as the multiplier on urgency
# rather than the fault. Tinting it made a well-run safety process show a red
# cell, and put "fix this" and "this matters" in the same visual channel while
# the key above the table claimed colour meant a deficit and nothing else. It
# also forced the key to explain itself with "whichever end of the scale they
# sit at", and to print 1 2 under one column and 5 4 under the next.
#
# So Impact is marked by weight instead: I4 and I5 sit in full-strength ink, and
# the alarm palette is left to mean exactly one thing. Both markings are derived
# from the table below rather than hand-written, and the key on the page is
# generated from the same source, so it cannot describe something the table is
# not doing.
# Auto and Doc now share a range as well as a direction. Doc used to run 0-3
# against Auto's 1-5, so the same position on the two scales meant different
# things and the printed key had to name different digits for each column. On a
# common 1-5 they flag the same two values and the rule collapses to one line.
# The top band was the part that had to be invented rather than relabelled, and
# it is defined to mirror A5: A5 is "runs itself and tells us when it fails",
# D5 is "documented and we would know if it went stale". Both are empty today.
SCALES = {
    "a": {"label": "Auto",   "lo": 1, "hi": 5, "mark": "deficit"},
    "d": {"label": "Doc",    "lo": 1, "hi": 5, "mark": "deficit"},
    "i": {"label": "Impact", "lo": 1, "hi": 5, "mark": "weight"},
}
CRIT, WARN = 0.80, 0.55

DEFICIT_AXES = [ax for ax, s in SCALES.items() if s["mark"] == "deficit"]


def _frac(axis, v):
    """Where this value sits in its own range: 0.0 at the low end, 1.0 at the high."""
    s = SCALES[axis]
    return (int(v) - s["lo"]) / (s["hi"] - s["lo"])


def deficit(axis, v):
    """How far this value sits toward the bad end of a deficit scale, 0.0-1.0.

    Only meaningful for the axes in DEFICIT_AXES, which are all low-is-bad.
    """
    return 1 - _frac(axis, v)


def band(axis, v):
    """The class a value earns: severity on a deficit scale, emphasis on Impact."""
    if SCALES[axis]["mark"] == "weight":
        return "hi" if _frac(axis, v) >= WARN else "ok"
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
          "⟐": "strategy", "‖": "docs", "◊": "drafted", "▦": "measure",
          "⧉": "standards"}

# ---- the Standards of Excellence as a lens ----------------------------------
# ⧉ carries the standards a process implements, from the crosswalk
# (docs/STANDARDS_CROSSWALK.md). Framework metadata is snapshotted into
# data/standards.json by build/standards_sync.py — the build never reads the
# sibling repo, so CI works from a bare clone. `S055*` means the standard as
# written does not reach what the process does; `P3` is a proposed standard from
# the gaps doc that does not exist yet.
STD = json.loads((pathlib.Path(__file__).resolve().parents[1]
                  / "data" / "standards.json").read_text())
STD_BY_ID = {s["id"]: s for s in STD["standards"]}
STD_DOMAINS = STD["domains"]

# ---- the KPI dashboard as a measurement pointer ------------------------------
# ▦ carries the id(s) of the strategic-plan KPI a process moves, resolved here to
# the dashboard section that charts it. A link, deliberately not an embedded
# number: the registry shows maturity, not current health — dashboards own the
# live value, and the dashboard needs a login anyway. What the link buys in both
# directions: "this broken process — here is the number it damages", and (via the
# printed coverage stat) "which KPIs have no process pointed at them".
# Ids and labels mirror makerspace_dashboard's kpis.yml; sections are its tab ids.
DASHBOARD = "https://www.makehaven.org/makerspace-dashboard"
KPI = {
    # governance
    "kpi_board_ethnic_diversity":        ("governance", "Board Ethnic Diversity (% BIPOC)"),
    "kpi_board_gender_diversity":        ("governance", "Board Gender Diversity (% Female/Non-binary)"),
    # finance
    "kpi_reserve_funds_months":          ("finance", "Reserve Funds (Months of Operating Expense)"),
    "kpi_earned_income_sustaining_core": ("finance", "Earned Income Sustaining Core %"),
    "kpi_member_revenue_quarterly":      ("finance", "Member Revenue (Quarterly)"),
    "kpi_net_income_program_lines":      ("finance", "Net Income (Program Lines)"),
    "kpi_member_lifetime_value_projected": ("finance", "Member Lifetime Value (Projected)"),
    "kpi_revenue_per_member_index":      ("finance", "Revenue vs Expense Index (per member)"),
    "kpi_monthly_revenue_at_risk":       ("finance", "Monthly Revenue at Risk ($)"),
    "kpi_payment_resolution_rate":       ("finance", "Payment Resolution Rate %"),
    # infrastructure
    "kpi_member_satisfaction_equipment": ("infrastructure", "Member Satisfaction (Equipment)"),
    "kpi_equipment_uptime_rate":         ("infrastructure", "Equipment Uptime Rate %"),
    "kpi_active_maintenance_load":       ("infrastructure", "Active Maintenance Load"),
    "kpi_storage_occupancy":             ("infrastructure", "Storage Occupancy %"),
    "kpi_equipment_investment":          ("infrastructure", "Value of Equipment Added ($)"),
    "kpi_adherence_to_shop_budget":      ("infrastructure", "Adherence to Shop Budget"),
    # outreach
    "kpi_total_new_member_signups":      ("outreach", "Total New Member Signups"),
    "kpi_total_first_time_workshop_participants": ("outreach", "First Time Workshop Participants"),
    "kpi_total_new_recurring_revenue":   ("outreach", "New Recurring Membership Revenue (Monthly)"),
    "kpi_tours":                         ("outreach", "Total Tours (12 month)"),
    "kpi_tours_to_member_conversion":    ("outreach", "Tours to Member Conversion %"),
    "kpi_guest_waiver_to_member_conversion": ("outreach", "Guest Waiver to Member Conversion %"),
    "kpi_event_participant_to_member_conversion": ("outreach", "Event Participant to Member Conversion %"),
    # retention
    "kpi_total_active_members":          ("retention", "Total Active Members"),
    "kpi_first_year_member_retention":   ("retention", "First Year Member Retention %"),
    "kpi_member_post_12_month_retention": ("retention", "Member (Post-12mo) Retention %"),
    "kpi_member_nps":                    ("retention", "Member Net Promoter Score"),
    "kpi_active_participation":          ("retention", "Active Participation %"),
    "kpi_new_member_first_badge_28_days": ("retention", "New Member First Badge (28 days) %"),
    "kpi_members_at_risk_share":         ("retention", "Members At-Risk %"),
    "kpi_membership_diversity_bipoc":    ("retention", "Membership Diversity (% BIPOC)"),
    # education
    "kpi_workshop_attendees":            ("education", "Workshop Attendees"),
    "kpi_workshop_capacity_utilization": ("education", "Workshop Capacity Utilization %"),
    "kpi_program_capacity_utilization":  ("education", "Program Capacity Utilization %"),
    "kpi_workshop_program_capacity_utilization": ("education", "Workshop + Program Capacity Utilization %"),
    "kpi_education_nps":                 ("education", "Education Net Promoter Score"),
    "kpi_workshop_participants_bipoc":   ("education", "% Workshop Participants (BIPOC)"),
    "kpi_active_instructors_bipoc":      ("education", "% Active Instructors (BIPOC)"),
    "kpi_net_income_education":          ("education", "Net Income (Education Program)"),
    # entrepreneurship
    "kpi_incubator_workspace_occupancy": ("entrepreneurship", "Incubator Workspace Occupancy %"),
    "kpi_active_incubator_ventures":     ("entrepreneurship", "Active Incubator Ventures"),
    "kpi_entrepreneurship_event_participation": ("entrepreneurship", "Entrepreneurship Events Participants"),
    # development
    "kpi_recurring_donors_count":        ("development", "Recurring Donors"),
    "kpi_annual_corporate_sponsorships": ("development", "$ Annual Corporate Sponsorships"),
    "kpi_grant_pipeline_count":          ("development", "Grants Submitted (YTD)"),
    "kpi_grant_win_ratio":               ("development", "Grant Win Ratio %"),
    "kpi_donor_retention_rate":          ("development", "Donor Retention Rate %"),
    "kpi_donor_upgrades_count":          ("development", "Donor Upgrades"),
    # dei
    "kpi_retention_poc":                 ("dei", "Retention POC %"),
    "kpi_active_participation_bipoc":    ("dei", "Active Participation % (BIPOC)"),
    "kpi_active_participation_female_nb": ("dei", "Active Participation % (Female/Non-binary)"),
}
unknown_kpis = []      # typos surface in the build output, like unmatched strategies
used_kpis = set()

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
    """Prose and warnings visible; provenance folded behind one line.

    A row's sentence and anything a person raised about it stay in plain sight.
    The rest — which module, which strategy, which documents, when reviewed —
    is provenance: essential when you are working on the row, noise when you are
    scanning 188 of them. It collapses into a <details> whose summary names what
    is inside, so "is anything written down?" is still answerable without a
    click even though the links themselves take one.
    """
    p = parse_note(raw)
    out = md(p["note"])
    if p.get("raised"):
        out += f'<span class="res raised"><b>Raised</b>{md(p["raised"])}</span>'

    folded, labels = [], []
    if p.get("code"):
        folded.append(f'<span class="res code"><b>Code</b>{code_links(p["code"])}</span>')
        labels.append("Code")
    if p.get("strategy"):
        folded.append(f'<span class="res strat"><b>Strategy</b>{md(p["strategy"])}</span>')
        labels.append("Strategy")
    if p.get("docs"):
        folded.append(f'<span class="res"><b>Docs</b>{md(p["docs"])}</span>')
        labels.append("Docs")
    if p.get("measure"):
        links = []
        for k in [x.strip() for x in p["measure"].split(",") if x.strip()]:
            if k in KPI:
                sec, label = KPI[k]
                used_kpis.add(k)
                links.append(f'<a href="{DASHBOARD}/{sec}" target="_blank" '
                             f'rel="noopener">{html.escape(label)}</a>')
            else:
                unknown_kpis.append(k)
                links.append(f'<code>{html.escape(k)}</code>')
        folded.append(f'<span class="res kpi"><b>Measured by</b>{" · ".join(links)}'
                      f' <i class="staffnote">— dashboard (staff)</i></span>')
        labels.append("Measured")
    # Only rows a person actually confirmed carry a line. How much is unverified
    # is reported once, in the inventory header, rather than stamped on ninety-odd
    # rows as a reproach.
    if p.get("reviewed"):
        folded.append(f'<span class="res meta"><b>Reviewed</b> {md(p["reviewed"])}</span>')
        labels.append("Reviewed")
    # A description written from the row's name, module and strategy rather than
    # by someone who runs the process. This is a separate claim from `reviewed`,
    # which on several of these rows is true of the state and scores but was never
    # true of the prose — those rows had no prose at all. Marked per row because
    # the sentence reads exactly like a confirmed one otherwise. It stays outside
    # the fold: a caveat on the sentence belongs next to the sentence.
    if p.get("drafted"):
        out += (f'<span class="res draft"><b>Description inferred</b> '
                f'{md(p["drafted"])} — not confirmed by anyone who runs it</span>')
    if p.get("standards"):
        folded.append(f'<span class="res std"><b>Standards</b>'
                      f'{html.escape(p["standards"])}</span>')
        labels.append("Standards")
    if folded:
        out += (f'<details class="rowmeta"><summary>{" · ".join(labels)}</summary>'
                f'{"".join(folded)}</details>')
    return out

# ---- the strategic plan as a ranking input ----------------------------------
# The plan already assigns each strategy a P1/P2 priority, and 76 rows already
# name the strategy acting on them, but the two never met: the ranking was pure
# arithmetic and would happily put a P1 commitment below an unprioritised row.
# A registry that ignores what the board committed to is at odds with the plan
# it is supposed to serve.
#
# strategies.csv is therefore read at build time rather than baked into the
# inventory. The plan is a live draft heading for a shorter priority list, so
# when it changes the update is one file swap and a rebuild — no row edits.
STRAT_CSV = SRC.with_name("strategies.csv")
PLAN_BOOST = {"P1": 4, "P2": 1}


def _norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


strategies = {}
if STRAT_CSV.exists():
    import csv
    with STRAT_CSV.open(newline="") as fh:
        for _r in csv.DictReader(fh):
            strategies[_norm(_r["Strategy Title"])] = {
                "title": _r["Strategy Title"].strip(),
                "priority": _r["Priority"].strip(),
                "work": _r["Next Work Type"].strip(),
            }


def strategy_of(r):
    """The plan entry acting on this process, or None."""
    f = parse_note(r["note"]).get("strategy")
    if not f:
        return None
    # Rows read "Priority · Some Strategy — building next"; the prefix and the
    # trailing work-type clause are presentation, the title is the key.
    title = re.sub(r"^Priority\s*·\s*", "", f)
    title = re.sub(r"\s*—\s*.*$", "", title).strip()
    return strategies.get(_norm(title))


for r in rows:
    r["strat"] = strategy_of(r)
    r["plan_boost"] = PLAN_BOOST.get(r["strat"]["priority"], 0) if r["strat"] else 0

n_strat_matched = sum(1 for r in rows if r["strat"])
n_p1 = sum(1 for r in rows if r["strat"] and r["strat"]["priority"] == "P1")
n_unmatched = sum(1 for r in rows if not r["strat"] and "⟐" in r["note"])

# ---- automation ranking ----------------------------------------------------
# Membership is a separate question from order, and it used to be neither: the
# only filter was score > 0, and since nothing in the registry is A5 the term
# (5 - A) is never zero, so 186 of 187 processes "made" the list. A ranking that
# contains everything is a sorted inventory, not a shortlist.
#
# A row now has to have something actually wrong with it:
#   - a named deficit (broken or optimizable) always keeps its place, or
#   - it is not yet both automated and documented, and it matters enough that
#     fixing it is worth someone's week.
# Automated *and* documented is the definition of done here — A4 is "automated,
# humans handle exceptions" and D3 is "current SOP exists" — so those rows are
# finished, not merely un-started. And an I1 or I2 annoyance is a real thing to
# improve one day, but it is not what "where should effort go next" is asking.
FINISHED_A, FINISHED_D, WORTH_IT_I = 4, 3, 3


def needs_work(r):
    # An idea is not work owed — nobody committed to it, so it cannot be ranked
    # against things that are failing or promised. It waits in the inventory.
    if r["state"] == "idea":
        return False
    if r["state"] in ("broken", "optimizable"):
        return True
    # A P1 commitment belongs on the list whatever its scores say — that is what
    # the board choosing it means.
    if r["plan_boost"] >= PLAN_BOOST["P1"]:
        return True
    if not (r["a"].isdigit() and r["i"].isdigit()):
        return False
    if int(r["a"]) >= FINISHED_A and r["d"].isdigit() and int(r["d"]) >= FINISHED_D:
        return False
    return int(r["i"]) >= WORTH_IT_I


ranked = []
for r in rows:
    if needs_work(r) and r["a"].isdigit() and r["i"].isdigit():
        base = int(r["i"]) * (5 - int(r["a"]))
        if base > 0:
            r["base"] = base
            ranked.append((base + r["plan_boost"], int(r["i"]), r))

n_settled = N - len(ranked)
ranked.sort(key=lambda t: (-t[0], -t[1], t[2]["name"]))
# Ten, not thirty. A ranked list is a request for attention, and the request has
# to be answerable in one meeting — "here are the ten, argue about the order" is
# a conversation; thirty is homework. The rest stay one click away rather than
# truncated silently. (Cut from 30 after a strategic-planning consultant's
# review: the team needs consensus on what comes first, and a shorter list is
# how a page asks for that.)
SHOWN = 10
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

# ---- standards tab ----------------------------------------------------------
# The registry cannot score a standard — the assessment tool owns that. What it
# can do is the drill-down the tool cannot: for each standard, which processes
# implement it and what state they are in, which is the concrete answer to
# "what would we actually have to change to reach the next level?" A standard
# whose implementing rows are broken or unwritten (D0–D1) cannot honestly score
# 2 ("written, assigned, consistently implemented, evidenced") no matter what an
# assessor hopes — those rows are the work list, and this tab names them.
std_rows = collections.defaultdict(list)   # S-id -> [(row, stretch?)]
prop_rows = collections.defaultdict(list)  # proposed P-id -> [row]
for r in rows:
    spec = parse_note(r["note"]).get("standards")
    if not spec:
        continue
    for tok in spec.split():
        sid = tok.rstrip("*")
        if sid in STD_BY_ID:
            std_rows[sid].append((r, tok.endswith("*")))
        elif re.fullmatch(r"P\d+", sid):
            prop_rows[sid].append(r)

def std_blockers(pairs):
    """The rows that hold a standard below level 2, and why."""
    out = []
    for r, _ in pairs:
        why = []
        if r["state"] == "broken":
            why.append("broken")
        elif r["state"] in ("undefined", "unknown"):
            why.append(r["state"])
        if r["d"].isdigit() and int(r["d"]) < 2:
            why.append(f"nothing written (D{r['d']})")
        if why:
            out.append((r, " and ".join(why)))
    return out

std_sections, n_std_covered = [], len(std_rows)
for dcode in "123456ABCDE":
    dom_ids = [s["id"] for s in STD["standards"] if s["domain"] == dcode]
    covered = [i for i in dom_ids if i in std_rows]
    if not covered:
        continue
    orphans = [i for i in dom_ids if i not in std_rows]
    blocks = []
    for sid in covered:
        s = STD_BY_ID[sid]
        pairs = sorted(std_rows[sid], key=lambda p: (p[0]["state"] != "broken", p[0]["name"]))
        chips = " ".join(
            f'<span class="std-proc{" stretch" if stretch else ""}">'
            f'<span class="pill {r["state"]}">{r["state"]}</span>{md(r["name"])}'
            f'<i>D{html.escape(r["d"])}</i></span>' for r, stretch in pairs)
        badges = f'tier {s["tier"]}' + (" · critical" if s["critical"] else "")
        up = std_blockers(pairs)
        up_html = ""
        if up:
            items = " · ".join(f'{md(r["name"])} <i>({why})</i>' for r, why in up)
            up_html = f'<div class="std-up"><b>To move up</b>{items}</div>'
        blocks.append(f"""      <div class="std-row" id="std-{sid}">
        <div class="std-head"><code>{sid}</code><span class="std-badges">{badges}</span>
          <p>{html.escape(s["statement"])}</p></div>
        <div class="std-procs">{chips}</div>
        {up_html}</div>""")
    orphan_html = ""
    if orphans:
        orphan_html = (f'<p class="std-orphans">Not yet mapped to any process: '
                       f'{" ".join(f"<code>{i}</code>" for i in orphans)} — either a real '
                       f'underinvestment or a standard that does not apply here. '
                       f'Each is worth one honest sentence.</p>')
    std_sections.append(f"""  <section>
    <h2>{html.escape(STD_DOMAINS[dcode])}</h2>
    <div class="std-list">
{chr(10).join(blocks)}
    </div>
{orphan_html}
  </section>""")

if prop_rows:
    pb = []
    for pid_, prs in sorted(prop_rows.items(), key=lambda kv: int(kv[0][1:])):
        chips = " ".join(
            f'<span class="std-proc"><span class="pill {r["state"]}">{r["state"]}</span>'
            f'{md(r["name"])}</span>' for r in sorted(prs, key=lambda r: r["name"]))
        pb.append(f"""      <div class="std-row"><div class="std-head"><code>{pid_}</code>
        <span class="std-badges">proposed</span></div><div class="std-procs">{chips}</div></div>""")
    std_sections.append(f"""  <section>
    <h2>Proposed standards</h2>
    <p class="sec-note">Processes the crosswalk found that no standard reaches — the registry's
      contribution back to the framework. Definitions live in <code>STANDARDS_GAPS.md</code>
      in the Makerspace-Standards repo.</p>
    <div class="std-list">
{chr(10).join(pb)}
    </div>
  </section>""")

standards_html = "\n".join(std_sections)
n_std_stretch = sum(1 for pairs in std_rows.values() for _, st in pairs if st)

# ---- recently finished ------------------------------------------------------
# The other half of a change board. The page is fluent about what is wrong and
# what is moving, and silent about what got done — which reads as "look how much
# is unresolved" to the exact people being asked to resolve it. Finishing is the
# thing the team is being asked to value ("stabilize", in their own word), so the
# page should say it out loud. Derived from this file's own git history rather
# than a new field: the inventory already records every state change as an edit.
def state_transitions(days=30):
    """(name, old_state, new_state, date) for rows whose state changed in git."""
    import subprocess
    root = pathlib.Path(__file__).resolve().parents[1]
    try:
        log = subprocess.run(
            ["git", "log", f"--since={days} days ago", "--format=@@%as",
             "-p", "--unified=0", "--", "data/inventory.md"],
            capture_output=True, text=True, cwd=root, timeout=30).stdout
    except Exception:
        return []          # no git (tarball build): the section simply absents itself

    valid = set(STATES)
    def row_state(line):
        cells = [c.strip() for c in line.split("|")]
        # ['', name, a, d, i, state, note, ''] — only a real row has a state word
        if len(cells) >= 7 and cells[5] in valid and cells[1] not in ("Process", ""):
            return cells[1].strip("*"), cells[5]
        return None

    out, seen, date = [], set(), ""
    removed, added = {}, {}
    def flush():
        for name, new in added.items():
            old = removed.get(name)
            if old and old != new and name not in seen:
                seen.add(name)               # newest-first log → first hit wins
                out.append((name, old, new, date))
        removed.clear(); added.clear()

    for line in log.splitlines():
        # Commit marker is "@@<date>"; hunk headers are "@@ -n,m" with a space.
        if line.startswith("@@") and not line.startswith("@@ "):
            flush(); date = line[2:]
        elif line.startswith("-|"):
            rs = row_state(line[1:])
            if rs: removed[rs[0]] = rs[1]
        elif line.startswith("+|"):
            rs = row_state(line[1:])
            if rs: added[rs[0]] = rs[1]
    flush()
    return out

# A win is reaching stable, or ceasing to be broken — the two transitions worth
# announcing. changing→watch is progress too, but it is already visible in flux.
wins = [(n, o, s, d) for (n, o, s, d) in state_transitions(30)
        if s == "stable" or (o == "broken" and s != "broken")]
if wins:
    win_rows = "".join(
        f"""      <div class="flux-row"><div><span class="pill {s}">{s}</span></div>
        <div class="what"><b>{html.escape(n)}</b></div>
        <div class="n">was <span class="pill {o}" style="padding:1px 5px">{o}</span> until {d}</div></div>"""
        for n, o, s, d in wins[:8])
    wins_html = f"""  <section>
    <h2>Recently finished</h2>
    <p class="sec-note"><strong>{len(wins)} process{"es" if len(wins) != 1 else ""} reached
      <span class="pill stable" style="padding:1px 5px">stable</span> or stopped being
      <span class="pill broken" style="padding:1px 5px">broken</span> in the last 30 days.</strong>
      Read this list first: it is the point of all the others.</p>
    <div class="flux">
{win_rows}
    </div>
  </section>"""
else:
    wins_html = ""

# ---- in flux right now ------------------------------------------------------
flux = [r for r in rows if r["state"] in ("changing", "watch")]
flux.sort(key=lambda r: (r["state"] != "changing", r["group"], r["name"]))
# data-pid on the row, button inside it: paintCommentCounts() walks [data-pid]
# and paints any .rowsay beneath, so this picks up counts with no client change.
# This is the tab built for the board and staff conversation, which is exactly
# where someone reading a row wants to say something about it — asked for in the
# registry's own comments, 2026-08-15.
influx = "".join(
    f"""      <div class="flux-row" data-pid="{r['pid']}"><div><span class="pill {r['state']}">{r['state']}</span></div>
        <div class="what"><b>{md(r['name'])}</b><span class="grp">{html.escape(r['group'])}</span>
        <button type="button" class="rowsay" data-pid="{r['pid']}" """
    f"""aria-label="Comment on {html.escape(r['name'], quote=True)}">Comment</button></div>
        <div class="n">{md(plain_note(r['note']))}</div></div>""" for r in flux)

# ---- fragments -------------------------------------------------------------
# Every tile that counts a single state is an anchor carrying that state's exact
# word, so clicking it lands in the inventory already filtered to the rows it was
# counting. Before, the tiles named states the inventory did not use, so a reader
# who saw "11 failing now" had nothing to type to find those eleven rows.
# "In flux" spans two states and "Processes mapped" is the whole set, so those
# two stay plain divs rather than pretending to a filter they cannot express.
# The tile used to be labelled "Still unknown", which reads as "there is a row
# scored `unknown`" — and there is not; it counts `undefined` + `unknown`, two
# different claims. When only one of them is non-zero the tile says which, and
# filters the inventory to it, so the number on the front page and the rows
# behind it are the same thing.
_gap = [(s, st_tot[s]) for s in ("undefined", "unknown") if st_tot[s]]
_gap_sub = ("Nobody can currently say what the process is"
            if len(_gap) != 1 else
            {"undefined": "The process has no defined shape yet — this is a decision nobody has made",
             "unknown": "It runs, but we cannot characterise it — ask the person who does it"}[_gap[0][0]])
_gap_lbl = _gap[0][0].title() if len(_gap) == 1 else "No agreed shape"
gap_tile = (
    f'<a class="tile gap" href="#inventory" data-filter="state:{_gap[0][0]}">'
    f'<span class="num">{cant_say}</span><span class="lbl">{_gap_lbl}</span>'
    f'<span class="sub">{_gap_sub}</span></a>'
    if len(_gap) == 1 else
    f'<div class="tile gap"><span class="num">{cant_say}</span>'
    f'<span class="lbl">{_gap_lbl}</span><span class="sub">{_gap_sub}</span></div>')

tiles = f"""
      <div class="tile"><span class="num">{N}</span><span class="lbl">Processes mapped</span><span class="sub">Across 13 groups · {st_tot['stable']} running normally</span></div>
      <a class="tile bad" href="#inventory" data-filter="state:broken"><span class="num">{st_tot['broken']}</span><span class="lbl">Broken</span><span class="sub">{TILE_COPY['broken']}</span></a>
      <a class="tile unopt" href="#inventory" data-filter="state:optimizable"><span class="num">{st_tot['optimizable']}</span><span class="lbl">Optimizable</span><span class="sub">{TILE_COPY['optimizable']}</span></a>
      <div class="tile accent"><span class="num">{change_load}</span><span class="lbl">In flux</span><span class="sub">{st_tot['watch']} being watched, {st_tot['changing']} actively changing</span></div>
      <a class="tile plan" href="#inventory" data-filter="state:planned"><span class="num">{planned}</span><span class="lbl">Planned</span><span class="sub">Not started — intentions on the roadmap, not failures</span></a>
      {gap_tile}"""

legend = "".join(
    f'<span><i class="swatch" style="background:var(--s-{s})"></i>{s.title()} {st_tot[s]}</span>'
    for s in STATES if st_tot[s])

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
def plan_chip(r):
    """The plan's own priority on the row, so a boost is never invisible."""
    st = r["strat"]
    if not st:
        return ""
    cls = "p1" if st["priority"] == "P1" else "p2"
    # No "Plan" label on the chip: a P2 strategy whose next work type is PLAN
    # rendered as "Plan P2 Plan". The priority and the work type carry it, and
    # the full strategy name lives in the tooltip.
    tip = f'{st["title"]} · {st["work"].title()} next'
    return (f'<span class="plan {cls}" title="{html.escape(tip, quote=True)}">'
            f'<b>{html.escape(st["priority"])}</b>'
            f'<i>{html.escape(st["work"].title())}</i></span>')


rank_html = []
for n, (score, _, r) in enumerate(top, 1):
    extra = "" if n <= SHOWN else " rank-extra"
    boost = f'<span class="plan-adj">+{r["plan_boost"]}</span>' if r["plan_boost"] else ""
    # The policy or procedure behind a row is most useful precisely here. This is
    # the tab where the room argues about what to do next, and "is anything even
    # written down?" is half that argument — a question the inventory answers two
    # tabs away. Same field as the inventory's Docs line, same links.
    rdocs = parse_note(r["note"]).get("docs")
    docs_html = f'<span class="rdocs"><b>Docs</b>{md(rdocs)}</span>' if rdocs else ""
    rank_html.append(f"""      <div class="rank-row{extra}" data-pid="{r['pid']}" data-base="{r['base']}" data-plan="{r['plan_boost']}" data-rank="{n}"{'' if n <= SHOWN else ' hidden'}><div class="n">{n:02d}</div>
        <div class="what"><b>{md(r['name'])}</b><em>{md(plain_note(r['note']))}</em>
        <span class="grp">{html.escape(r['group'])}{plan_chip(r)}</span>{docs_html}
        <div class="vote" data-pid="{r['pid']}" hidden>
          <button type="button" class="vt up" data-v="1" aria-label="More important than ranked">&#9650;<span class="c">0</span></button>
          <button type="button" class="vt down" data-v="-1" aria-label="Less important than ranked">&#9660;<span class="c">0</span></button>
          <button type="button" class="vt say" aria-label="Comment on this process">Comment</button>
          <span class="movecue"></span>
        </div></div>
        <div class="score"><span class="final">{score}</span><small>I{r['i']} &times; A{r['a']}{boost}<span class="adj"></span></small></div></div>""")

tables = []
for g, rs in by_group.items():
    c = collections.Counter(r["state"] for r in rs)
    blurb = f'<p class="tnote">{md(blurbs[g])}</p>' if g in blurbs else ""
    body = "".join(
        # data-state carries the state as data rather than as prose to be matched.
        # A text search for "broken" also hits three rows that use the word in a
        # note — a broken item, a broken clause — so a tile counting 11 would land
        # the reader on 14. `state:` queries read this attribute instead.
        f"""<tr data-pid="{r['pid']}" data-state="{r['state']}"><td class="p">{md(r['name'])}"""
        f"""<button type="button" class="rowsay" data-pid="{r['pid']}" """
        f"""aria-label="Comment on {html.escape(r['name'], quote=True)}">Comment</button></td>"""
        f"""{score_cell('a', r['a'])}{score_cell('d', r['d'])}{score_cell('i', r['i'])}"""
        f"""<td><span class="pill {r['state']}">{r['state']}</span></td>"""
        f"""<td class="n">{note_cell(r['note'])}</td></tr>""" for r in rs)
    counts = " · ".join(f"{c[s]} {s}" for s in STATES if c[s])
    # data-group is what the "just my area" select matches against.
    tables.append(f"""      <div class="tblwrap" data-group="{html.escape(g, quote=True)}">
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
# A4 says a process runs itself; only a named module says where to read what it
# does. The gap between these two is what the documentation floor now respects.
n_auto_nocode = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) >= 4
                    and "⚙" not in r["note"])
n_auto_code   = n_auto - n_auto_nocode
n_manual = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) <= 2)
n_manual_undoc = sum(1 for r in rows if r["a"].isdigit() and int(r["a"]) <= 2
                     and r["d"].isdigit() and int(r["d"]) <= 2)
# The "proven by a second person" band, D3 before the scales were aligned.
n_d3 = sum(1 for r in rows if r["d"] == "4")

# The A4 -> A5 claim is generated rather than written, because the sentence that
# used to sit here argued from two incidents that no row in this file records —
# one of them a "door-sync outage" that was a UniFi add-on sync error and not an
# access-control failure at all. An unsourced anecdote cannot be checked against
# the data and so survives every rewrite; a sentence computed from the data goes
# stale loudly, the first time someone earns an A5.
n_a4 = sum(1 for r in rows if r["a"] == "4")
n_a5 = sum(1 for r in rows if r["a"] == "5")
if n_a5 == 0:
    a5gap = (f"<strong>{n_a4} processes run themselves and not one of them tells us "
             f"when it stops.</strong> A5 is empty.")
else:
    a5gap = (f"<strong>{n_a4} processes run themselves; {n_a5} also tell us when they "
             f"stop.</strong>")

fields = [parse_note(r["note"]) for r in rows]
n_reviewed = sum(1 for f in fields if f.get("reviewed"))
n_drafted  = sum(1 for f in fields if f.get("drafted"))
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

# ---- question manifest ------------------------------------------------------
# The question rounds are what took this registry from guesses to a map, and
# they were run as documents passed to one person. Embedding the current round
# in the page lets anyone signed in answer one question when they have a minute
# — the same interview, spread across the people who actually run the processes.
# qid is stable across rebuilds (process + category) so an answered question
# stays answered; the wording can improve without resetting the round.
import hashlib, sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).parent))
import questions as _qgen
_name2pid = {re.sub(r"[*`]", "", r["name"]).strip(): r["pid"] for r in rows}
# The whole round, not a top-20 slice. The slice existed when the only place a
# question could be answered was one card in the comment bubble, where more than
# a handful was pointless. The Questions tab shows the round as a list you work
# down in a sitting, so truncating it would only hide questions nobody can then
# reach — and the tail is where the never-verified high-impact rows sit.
_qs = _qgen.questions(_qgen.load())
qmanifest = json.dumps(
    [{"qid": hashlib.md5(f"{proc}|{cat}".encode()).hexdigest()[:10],
      "pid": _name2pid.get(proc), "process": proc, "cat": cat, "q": q, "why": why}
     for pri, cat, proc, q, why in _qs],
    ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

# The key used to be hand-written and said "1 — worst on that axis", which is
# true for Auto and Doc and wrong for Impact, where 5 is the bad end. Generated
# from SCALES it shows the actual digits each column tints — and now that only
# the two deficit axes are tinted, it is two entries reading the same way rather
# than three that had to be checked against three different scales.
key_bits = []
for _ax in DEFICIT_AXES:
    _s = SCALES[_ax]
    _vals = sorted((v for v in range(_s["lo"], _s["hi"] + 1) if band(_ax, v) != "ok"),
                   key=lambda v: -deficit(_ax, v))
    _chips = "".join(f'<i class="k-{band(_ax, v)}">{v}</i>' for v in _vals)
    key_bits.append(f'<span><b>{_s["label"]}</b>{_chips}</span>')
scorekey = "".join(key_bits)

page = TPL.read_text()
for key, val in [("TILES", tiles), ("LEGEND", legend), ("BOARD", "\n".join(board)),
                 ("NRES", str(nres)), ("NGROUPS", str(len(by_group))),
                 ("NAUTO", str(n_auto)), ("NMANUAL", str(n_manual)), ("A5GAP", a5gap),
                 ("NAUTONOCODE", str(n_auto_nocode)), ("NAUTOCODE", str(n_auto_code)),
                 ("NMANUALUNDOC", str(n_manual_undoc)), ("ND3", str(n_d3)),
                 ("NFLOORED", str(n_floored)),
                 ("NREVIEWED", str(n_reviewed)), ("NCODE", str(n_code)),
                 ("NNEVER", str(n_never)), ("NRANK", str(len(top))), ("NSHOWN", str(SHOWN)),
                 ("NMORE", str(max(0, len(top) - SHOWN))), ("RAISED", raised_html),
                 ("MANIFEST", manifest), ("QUESTIONS", qmanifest),
                 ("NQUESTIONS", str(len(_qs))),
                 ("SCOREKEY", scorekey),
                 ("NSETTLED", str(n_settled)), ("NP1ROWS", str(n_p1)),
                 ("NSTRAT", str(n_strat_matched)),
                 ("NRAISED", str(len(raised))),
                 ("RANK", "\n".join(rank_html)), ("TABLES", "\n".join(tables)),
                 ("UNRANK", unrank_html), ("INFLUX", influx), ("N", str(N)),
                 ("WINS", wins_html),
                 ("STANDARDS", standards_html), ("NSTD", str(n_std_covered)),
                 ("NSTDSTRETCH", str(n_std_stretch)),
                 ("NSTDTOTAL", str(len(STD_BY_ID))),
                 ("GROUPOPTS", "\n".join(
                     f'        <option value="{html.escape(g, quote=True)}">{html.escape(g)}</option>'
                     for g in by_group)),
                 ("NCHANGING", str(st_tot["changing"])), ("NWATCH", str(st_tot["watch"])),
                 ("CHANGELOAD", str(change_load)), ("CANTSAY", str(cant_say)),
                 ("DEGRADED", str(st_tot["broken"])), ("UNOPT", str(st_tot["optimizable"])),
                 ("DEFICIT", str(st_tot["broken"] + st_tot["optimizable"])),
                 ("UNDEF", str(st_tot["undefined"])),
                 ("STABLE", str(st_tot["stable"])), ("PLANNED", str(planned)), ("WITHSTRAT", str(with_strat)), ("NP1", str(len(p1_rows)))]:
    page = page.replace("{{" + key + "}}", val)
left = re.findall(r"\{\{[A-Z]+\}\}", page)
if left:
    raise SystemExit(f"unrendered placeholders: {sorted(set(left))}")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
print(f"resource-linked rows: {nres}; D3 floor applied to {n_floored} rows "
      f"that run as code and name the module")
print(f"coverage — reviewed {n_reviewed}/{N}, code {n_code}/{N}, "
      f"descriptions inferred {n_drafted}/{N}")
print(f"plan — {n_strat_matched} rows matched a strategy ({n_p1} P1), {n_unmatched} named a strategy not in strategies.csv")
n_std_blocked = sum(1 for pairs in std_rows.values() if std_blockers(pairs))
print(f"standards — {n_std_covered}/{len(STD_BY_ID)} mapped to a process; "
      f"{n_std_blocked} held below level 2 by a broken or unwritten row; "
      f"{len(prop_rows)} proposed standards carry rows")
n_measured = sum(1 for f in fields if f.get("measure"))
orphan_kpis = sorted(set(KPI) - used_kpis)
print(f"kpi — {n_measured} rows name the KPI they move; "
      f"{len(orphan_kpis)} of {len(KPI)} KPIs have no process pointed at them"
      + (f"; UNKNOWN ids: {sorted(set(unknown_kpis))}" if unknown_kpis else ""))
print(f"wrote {OUT} — {N} processes, {len(tables)} groups, change load {change_load}, can't-say {cant_say}")
print(f"questions — {len(_qs)} in the round across "
      f"{len({q[2] for q in _qs})} processes")
