#!/usr/bin/env python3
"""Render data/obligations.yaml -> public/obligations/index.html.

The page answers three questions for the Executive Director and for whoever
comes next: what is due, what proves the last cycle closed, and what breaks if
it slips. Dates are computed from the register every build, so the page is
never older than the last deploy.

Run:   python3 build/obligations.py
Test:  OBLIGATIONS_TODAY=2026-09-22 python3 build/obligations.py
"""
import datetime as dt
import html
import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "obligations.yaml"
OUT = ROOT / "public" / "obligations" / "index.html"

LANES = [("tax", "Tax & filings"), ("insurance", "Insurance"), ("money", "Money & people")]
SOON_DAYS = 30
WINDOW_BEFORE = 21          # days of the timeline to the left of today
WINDOW_AFTER = 365

# ---------------------------------------------------------------- dates


def today() -> dt.date:
    env = os.environ.get("OBLIGATIONS_TODAY")
    return dt.date.fromisoformat(env) if env else dt.date.today()


def add_years(d: dt.date, n: int) -> dt.date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:            # 29 Feb
        return d.replace(year=d.year + n, day=28)


def annual_next(mm: int, dd: int, base: dt.date) -> dt.date:
    cand = dt.date(base.year, mm, dd)
    return cand if cand >= base else dt.date(base.year + 1, mm, dd)


def quarter_end_next(base: dt.date) -> dt.date:
    for m in (3, 6, 9, 12):
        last = (dt.date(base.year, m % 12 + 1, 1) - dt.timedelta(days=1)) if m < 12 \
            else dt.date(base.year, 12, 31)
        if last >= base:
            return last
    return dt.date(base.year + 1, 3, 31)


def semimonthly_dates(start: dt.date, end: dt.date):
    d = dt.date(start.year, start.month, 1)
    while d <= end:
        for day in (1, 15):
            x = d.replace(day=day)
            if start <= x <= end:
                yield x
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)


def resolve(item: dict, base: dt.date) -> dict:
    """Attach next_due, start, approx, overdue_since to a register item."""
    cad, due = item["cadence"], item.get("due")
    nxt, approx, since = None, False, None
    if cad == "annual":
        if isinstance(due, str) and due.startswith("~"):
            nxt, approx = annual_next(int(due[1:]), 15, base), True
        else:
            mm, dd = (int(p) for p in str(due).split("-"))
            nxt = annual_next(mm, dd, base)
    elif cad == "once":
        nxt = dt.date.fromisoformat(str(due))
        if nxt < base:
            since = nxt
    elif cad == "every-4-years":
        last = dt.date.fromisoformat(str(due))
        if item.get("state") == "unresolved":
            since = last
        nxt = add_years(last, 4)
    elif cad == "semimonthly":
        nxt = next(semimonthly_dates(base, base + dt.timedelta(days=40)))
    elif cad == "quarterly":
        nxt = quarter_end_next(base)
    start = (nxt - dt.timedelta(days=int(item.get("start_days", 0)))) if nxt else None
    out = dict(item)
    out.update(next_due=nxt, start=start, approx=approx, overdue_since=since)
    return out


def derived_state(it: dict, base: dt.date) -> str:
    if it["overdue_since"] or it["state"] == "unresolved":
        return "risk"
    if it["state"] == "at-risk":
        return "risk"
    if it["next_due"] and (it["next_due"] - base).days <= SOON_DAYS and it["cadence"] != "semimonthly":
        return "soon"
    return {"current": "ok", "unverified": "none", "changing": "info"}.get(it["state"], "none")


# ---------------------------------------------------------------- rendering helpers

E = html.escape


def fmt(d: dt.date | None, approx=False) -> str:
    if d is None:
        return "—"
    return (d.strftime("~%b %Y") if approx else d.strftime("%-d %b %Y"))


def rel(d: dt.date | None, base: dt.date) -> str:
    if d is None:
        return ""
    n = (d - base).days
    if n < 0:
        return f"{-n} days ago"
    if n == 0:
        return "today"
    if n == 1:
        return "tomorrow"
    return f"in {n} days"


PILL = {"ok": "Current", "soon": "Due soon", "risk": "At risk", "none": "No evidence",
        "info": "Changing", "auto": "Prepared"}


def pill(kind: str, label: str | None = None) -> str:
    return f'<span class="pill p-{kind}">{E(label or PILL[kind])}</span>'


# ---------------------------------------------------------------- timeline


def timeline(items: list[dict], base: dt.date) -> str:
    for it in items:
        it.setdefault("short", SHORT.get(it["id"], it["name"]))
    x0, x1, w = 90.0, 1090.0, 1000.0
    t0 = base - dt.timedelta(days=WINDOW_BEFORE)
    t1 = base + dt.timedelta(days=WINDOW_AFTER)
    span = (t1 - t0).days

    def X(d: dt.date) -> float:
        return x0 + w * (d - t0).days / span

    lane_y = {"tax": 100, "insurance": 180, "money": 255}
    parts = []

    # month grid
    d = dt.date(t0.year, t0.month, 1)
    while d <= t1:
        if d >= t0:
            x = X(d)
            q = ' q' if d.month in (1, 4, 7, 10) else ''
            parts.append(f'<line class="tick{q}" x1="{x:.1f}" y1="26" x2="{x:.1f}" y2="272"/>')
            lbl = d.strftime("%b %y") if (d.month == 1 or d == dt.date(t0.year, t0.month, 1)) else d.strftime("%b")
            parts.append(f'<text class="mo" x="{x + 4:.1f}" y="18">{lbl}</text>')
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)

    for key, label in LANES:
        y = lane_y[key]
        parts.append(f'<line class="lane" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>')
        parts.append(f'<text class="lanelbl" x="0" y="{y + 4}">{E(label)}</text>')

    tx = X(base)
    parts.append(f'<line class="today-line" x1="{tx:.1f}" y1="30" x2="{tx:.1f}" y2="272"/>')
    parts.append(f'<text class="today-lbl" x="{tx + 5:.1f}" y="36">Today</text>')

    # semimonthly rings
    for it in items:
        if it["cadence"] == "semimonthly":
            y = lane_y[it["group"]]
            for d in semimonthly_dates(base, t1):
                parts.append(f'<circle class="repeat" cx="{X(d):.1f}" cy="{y}" r="4"/>')
            parts.append(f'<text class="ev sub" x="{(x0 + x1) / 2:.0f}" y="{y + 27}" text-anchor="middle">'
                         f'◦ {E(it["name"].lower())}, 1st and 15th — prepared by the site, signed off in Xero</text>')

    # dots with collision-aware labels, per lane
    for key, _ in LANES:
        y = lane_y[key]
        lane_items = []
        for it in items:
            if it["group"] != key or it["cadence"] in ("semimonthly", "ongoing"):
                continue
            if it["overdue_since"]:
                lane_items.append((x0, it, True))
            elif it["next_due"] and t0 <= it["next_due"] <= t1:
                lane_items.append((X(it["next_due"]), it, False))
        lane_items.sort(key=lambda t: t[0])
        last = {"up": -1e9, "down": -1e9}
        for x, it, overdue in lane_items:
            k = derived_state(it, base)
            r = 6 if k in ("risk", "soon") else 5.5
            parts.append(f'<circle class="d-{k}" cx="{x:.1f}" cy="{y}" r="{r}"/>')
            slot = "up" if (x - last["up"]) >= (x - last["down"]) else "down"
            lx = max(x, last[slot] + 100)
            if lx != x:
                parts.append(f'<line class="lead" x1="{x:.1f}" y1="{y}" x2="{lx:.1f}" '
                             f'y2="{y - 22 if slot == "up" else y + 16}"/>')
            last[slot] = lx
            ny, sy = (y - 40, y - 28) if slot == "up" else (y + 24, y + 36)
            if overdue:
                sub = f"since {it['overdue_since'].strftime('%b %Y')}"
            else:
                sub = it["next_due"].strftime("~%b" if it["approx"] else "%b %-d")
                if it.get("start") and it["start"] > base:
                    sub += f" · start {it['start'].strftime('%b %-d')}"
            anchor = "end" if overdue else "middle"
            lx_txt = x0 - 38 if overdue else lx
            parts.append(f'<text class="ev" x="{lx_txt:.1f}" y="{ny}" text-anchor="{anchor}">{E(it.get("short", it["name"]))}</text>')
            parts.append(f'<text class="ev sub" x="{lx_txt:.1f}" y="{sy}" text-anchor="{anchor}">{E(sub)}</text>')

    return ('<svg viewBox="0 0 1120 300" role="img" aria-label="Twelve-month timeline of obligations in three lanes">'
            + "".join(parts) + "</svg>")


SHORT = {
    "contractor-approvals": "Contractor approvals", "gusto-xero-check": "Xero↔Gusto check",
    "workers-comp": "Workers' Comp", "workers-comp-audit": "WC premium audit",
    "personal-property": "Personal property", "form-990": "Form 990",
    "charity-renewal": "Charity renewal", "q-reimbursement": "Staff reimbursements",
    "gusto-mailing": "Gusto mailing cutoff", "form-1099": "1099-NEC",
    "gl-umbrella": "Liability & umbrella", "sots-annual-report": "State annual report",
    "d-and-o": "D&O", "cpa-review": "CPA review", "form-8868": "8868 extension",
    "cultural-district": "Cultural District", "board-coi": "Board conflict-of-interest",
    "m3-quadrennial": "M-3 exemption", "lease-review": "Lease",
}



# ---------------------------------------------------------------- page


def render(items: list[dict], base: dt.date) -> str:
    for it in items:
        it["short"] = SHORT.get(it["id"], it["name"])

    overdue = [i for i in items if i["overdue_since"] or i["state"] == "unresolved"]
    soon = [i for i in items if i["next_due"] and 0 <= (i["next_due"] - base).days <= SOON_DAYS
            and i["cadence"] != "semimonthly"]
    noev = [i for i in items if not i.get("evidence")]

    def names(xs, n=4):
        s = ", ".join(i["short"] for i in xs[:n])
        return s + (f", +{len(xs) - n} more" if len(xs) > n else "")

    # register table
    rows = []
    for key, label in LANES:
        rows.append(f'<tr class="grp"><td colspan="5">{E(label)}</td></tr>')
        lane = sorted((i for i in items if i["group"] == key),
                      key=lambda i: (i["overdue_since"] or i["next_due"] or dt.date.max))
        for it in lane:
            k = derived_state(it, base)
            due_txt = ("1st &amp; 15th" if it["cadence"] == "semimonthly" else
                       "ongoing" if it["cadence"] == "ongoing" else
                       E(fmt(it["overdue_since"] or it["next_due"], it["approx"])))
            sub = E(rel(it["overdue_since"] or it["next_due"], base)) if it["next_due"] else ""
            p = pill("auto") if it.get("auto") else pill(k, {"none": "Unverified"}.get(k) if it["state"] == "unverified" else
                                                       ("Unresolved" if it["state"] == "unresolved" else None))
            ev = f'<td class="ev">{E(it["evidence"])}</td>' if it.get("evidence") else '<td class="ev miss">None found</td>'
            rows.append(
                f'<tr><td class="due">{due_txt}<span>{sub}</span></td>'
                f'<td class="name"><b>{E(it["name"])}</b><span>{E(it.get("note", ""))}</span></td>'
                f'<td>{p}</td>{ev}<td>{E(it.get("if_slips", ""))}</td></tr>')

    def q(kind, n, what, detail):
        return (f'<div class="q-{kind}"><b>{n}</b><span>{E(what)}</span>'
                f'<em>{E(detail) if detail else "Nothing."}</em></div>')

    return TEMPLATE.format(
        asof=E(base.strftime("%a %-d %b %Y")),
        n=len(items),
        q_over=q("risk", len(overdue), "overdue or unresolved", names(overdue)),
        q_soon=q("soon", len(soon), f"due in the next {SOON_DAYS} days", names(soon)),
        q_noev=q("none", len(noev), "no evidence the last cycle closed", names(noev, 5)),
        timeline=timeline(items, base),
        rows="".join(rows),
    )


TEMPLATE = r"""<!DOCTYPE html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Obligations — MakeHaven</title>
<meta name="description" content="What is due, what proves it was done, and what breaks if it slips. Rendered from the obligations register.">
<style>
  :root {{
    --paper:#f5f4f1; --surface:#ffffff; --sunken:#eceae6;
    --ink:#191619; --ink-2:#4b4642; --ink-3:#7d766e;
    --rule:#dcd8d1; --rule-2:#c6c1b8; --crimson:#8b1919;
    --ok:#3d6b52; --ok-bg:#e5efe8; --soon:#9c6a0c; --soon-bg:#f6ecd8;
    --risk:#a01f1f; --risk-bg:#f6e3e3; --info:#2d5b87; --info-bg:#e2ebf4;
    --auto:#7d5a91; --auto-bg:#efe8f3; --none:#6b6560; --none-bg:#e9e6e2;
    --sans: ui-sans-serif, system-ui, "Helvetica Neue", Helvetica, Arial, sans-serif;
    --mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
    --maxw: 1180px;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --paper:#141316; --surface:#1c1a1e; --sunken:#252227;
      --ink:#eae6e2; --ink-2:#b3ada6; --ink-3:#8b847c;
      --rule:#322e34; --rule-2:#423d45; --crimson:#d96a6a;
      --ok:#7cc39a; --ok-bg:#1e3129; --soon:#dfae52; --soon-bg:#33280f;
      --risk:#e58080; --risk-bg:#38201f; --info:#7bacd8; --info-bg:#1c2b3a;
      --auto:#c0a0d4; --auto-bg:#2c2333; --none:#9a938b; --none-bg:#2a2725;
    }}
  }}
  :root[data-theme="dark"] {{
    --paper:#141316; --surface:#1c1a1e; --sunken:#252227;
    --ink:#eae6e2; --ink-2:#b3ada6; --ink-3:#8b847c;
    --rule:#322e34; --rule-2:#423d45; --crimson:#d96a6a;
    --ok:#7cc39a; --ok-bg:#1e3129; --soon:#dfae52; --soon-bg:#33280f;
    --risk:#e58080; --risk-bg:#38201f; --info:#7bacd8; --info-bg:#1c2b3a;
    --auto:#c0a0d4; --auto-bg:#2c2333; --none:#9a938b; --none-bg:#2a2725;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans);
         font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased; }}
  .wrap {{ max-width:var(--maxw); margin:0 auto; padding-inline:22px; }}
  a {{ color:inherit; }}
  :focus-visible {{ outline:2px solid var(--info); outline-offset:2px; }}
  .masthead {{ border-bottom:2px solid var(--ink); background:var(--surface); }}
  .masthead .wrap {{ display:flex; flex-direction:column; gap:14px; padding-block:30px 22px; }}
  .eyebrow {{ font-family:var(--mono); font-size:11px; letter-spacing:.14em; text-transform:uppercase;
             color:var(--crimson); font-weight:600; display:flex; gap:18px; flex-wrap:wrap; }}
  .eyebrow a {{ color:var(--ink-3); text-decoration:none; font-weight:500; }}
  .eyebrow a:hover {{ color:var(--ink); }}
  h1 {{ margin:0; font-size:clamp(28px,4.4vw,42px); line-height:1.04; letter-spacing:-.025em;
       font-weight:800; text-wrap:balance; max-width:22ch; }}
  .standfirst {{ margin:0; max-width:66ch; color:var(--ink-2); font-size:16.5px; }}
  .meta-line {{ display:flex; flex-wrap:wrap; gap:8px 22px; font-family:var(--mono); font-size:11.5px;
               letter-spacing:.05em; text-transform:uppercase; color:var(--ink-3); }}
  section {{ padding-block:40px 0; }}
  section:last-of-type {{ padding-bottom:60px; }}
  h2 {{ margin:0 0 4px; font-size:12px; font-family:var(--mono); letter-spacing:.15em; text-transform:uppercase;
       font-weight:700; color:var(--ink); padding-bottom:9px; border-bottom:1px solid var(--ink); }}
  .sec-note {{ margin:12px 0 20px; color:var(--ink-2); font-size:14.5px; max-width:74ch; }}
  .sec-note strong {{ color:var(--ink); }}
  .qstrip {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:18px 0 0; }}
  .qstrip div {{ padding:15px 17px; background:var(--surface); border:1px solid var(--rule); border-radius:2px; }}
  .qstrip b {{ font-size:30px; font-weight:750; margin-right:9px; font-variant-numeric:tabular-nums; line-height:1; }}
  .q-risk b {{ color:var(--risk); }} .q-soon b {{ color:var(--soon); }} .q-none b {{ color:var(--none); }}
  .qstrip span {{ font-size:13.5px; color:var(--ink-2); }}
  .qstrip em {{ display:block; margin-top:9px; font-style:normal; font-size:13px; color:var(--ink); }}
  @media (max-width:760px) {{ .qstrip {{ grid-template-columns:1fr; }} }}
  .horizon {{ background:var(--surface); border:1px solid var(--rule); border-radius:2px; padding:14px 8px 6px; overflow-x:auto; }}
  .horizon svg {{ display:block; min-width:760px; width:100%; height:auto; font-family:var(--sans); }}
  .horizon .tick {{ stroke:var(--rule); stroke-width:1; }} .horizon .tick.q {{ stroke:var(--rule-2); }}
  .horizon .lane {{ stroke:var(--rule); stroke-width:1; }}
  .horizon .lead {{ stroke:var(--rule-2); stroke-width:1; }}
  .horizon .mo {{ fill:var(--ink-3); font-family:var(--mono); font-size:10px; letter-spacing:.08em; text-transform:uppercase; }}
  .horizon .lanelbl {{ fill:var(--ink-3); font-family:var(--mono); font-size:10px; letter-spacing:.1em; text-transform:uppercase; font-weight:700; }}
  .horizon .today-line {{ stroke:var(--crimson); stroke-width:1.5; stroke-dasharray:3 3; }}
  .horizon .today-lbl {{ fill:var(--crimson); font-family:var(--mono); font-size:10px; letter-spacing:.1em; font-weight:700; text-transform:uppercase; }}
  .horizon .ev {{ font-size:11.5px; fill:var(--ink); }} .horizon .ev.sub {{ fill:var(--ink-3); font-size:10.5px; }}
  .horizon .d-ok {{ fill:var(--ok); }} .horizon .d-soon {{ fill:var(--soon); }} .horizon .d-risk {{ fill:var(--risk); }}
  .horizon .d-info {{ fill:var(--info); }} .horizon .d-none {{ fill:var(--none); }}
  .horizon .repeat {{ fill:none; stroke:var(--auto); stroke-width:1.5; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:7px 18px; margin:14px 0 0; font-family:var(--mono);
            font-size:10.5px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-2); }}
  .legend span {{ display:inline-flex; align-items:center; gap:7px; }}
  .sw {{ width:10px; height:10px; border-radius:50%; flex:none; display:inline-block; }}
  .tablewrap {{ overflow-x:auto; border:1px solid var(--rule); border-radius:2px; background:var(--surface); }}
  table {{ border-collapse:collapse; width:100%; min-width:820px; font-size:13.5px; }}
  th {{ text-align:left; font-family:var(--mono); font-size:10.5px; letter-spacing:.1em; text-transform:uppercase;
       color:var(--ink-3); font-weight:700; padding:11px 12px; border-bottom:1px solid var(--ink); background:var(--sunken); }}
  td {{ padding:10px 12px; border-bottom:1px solid var(--rule); vertical-align:top; }}
  tr:last-child td {{ border-bottom:0; }}
  td.due {{ font-family:var(--mono); font-variant-numeric:tabular-nums; white-space:nowrap; font-size:12.5px; }}
  td.due span {{ display:block; color:var(--ink-3); font-size:10.5px; }}
  td.name b {{ display:block; font-weight:650; }} td.name span {{ color:var(--ink-3); font-size:12.5px; }}
  .pill {{ display:inline-block; padding:2px 8px; border-radius:2px; font-family:var(--mono); font-size:10px;
          letter-spacing:.1em; text-transform:uppercase; font-weight:700; white-space:nowrap; }}
  .p-ok {{ background:var(--ok-bg); color:var(--ok); }} .p-soon {{ background:var(--soon-bg); color:var(--soon); }}
  .p-risk {{ background:var(--risk-bg); color:var(--risk); }} .p-info {{ background:var(--info-bg); color:var(--info); }}
  .p-auto {{ background:var(--auto-bg); color:var(--auto); }} .p-none {{ background:var(--none-bg); color:var(--none); }}
  td.ev {{ color:var(--ink-2); font-size:12.5px; }} td.ev.miss {{ color:var(--none); font-style:italic; }}
  .grp td {{ background:var(--sunken); font-family:var(--mono); font-size:10.5px; letter-spacing:.12em;
            text-transform:uppercase; color:var(--ink-2); font-weight:700; padding:7px 12px; }}
  .pipe {{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-top:18px; }}
  .stage {{ background:var(--surface); border:1px solid var(--rule); border-radius:2px; padding:13px 14px; }}
  .stage .n {{ font-family:var(--mono); font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--crimson); font-weight:700; }}
  .stage h4 {{ margin:5px 0 6px; font-size:14.5px; }} .stage p {{ margin:0; font-size:12.5px; color:var(--ink-2); }}
  .stage .who {{ display:inline-block; margin-top:9px; font-family:var(--mono); font-size:10px; letter-spacing:.1em;
                text-transform:uppercase; padding:2px 7px; border-radius:2px; }}
  .who.m {{ background:var(--auto-bg); color:var(--auto); }} .who.h {{ background:var(--info-bg); color:var(--info); }}
  .who.x {{ background:var(--none-bg); color:var(--none); }}
  @media (max-width:900px) {{ .pipe {{ grid-template-columns:1fr 1fr; }} }}
  @media (max-width:520px) {{ .pipe {{ grid-template-columns:1fr; }} }}
  .foot {{ margin-top:26px; padding-top:14px; border-top:1px solid var(--rule); color:var(--ink-3); font-size:12.5px; max-width:80ch; }}
  code {{ font-family:var(--mono); font-size:.92em; }}
</style>

<header class="masthead">
  <div class="wrap">
    <div class="eyebrow"><span>MakeHaven · Compliance &amp; recurring obligations</span><a href="/">← Process registry</a></div>
    <h1>What is due, what proves it, who hears if it slips</h1>
    <p class="standfirst">One page for the Executive Director and for whoever comes next. Every row is computed from the obligations register at build time. Credentials and runbook detail live with staff, not on this page.</p>
    <div class="meta-line">
      <span>As of {asof}</span>
      <span>{n} obligations</span>
      <span>Rendered from <code>data/obligations.yaml</code></span>
    </div>
  </div>
</header>

<section><div class="wrap">
  <h2>Start here</h2>
  <div class="qstrip">{q_over}{q_soon}{q_noev}</div>
</div></section>

<section><div class="wrap">
  <h2>The next twelve months</h2>
  <p class="sec-note">Each dot is a due date. <strong>The dashed line is today.</strong> Anything left of it that is not green is late. Where a working window opens before the date, the label says when. Open rings are the twice-monthly contractor approvals, which the site prepares and a person signs off.</p>
  <div class="horizon">{timeline}</div>
  <div class="legend">
    <span><i class="sw" style="background:var(--risk)"></i>at risk / unresolved</span>
    <span><i class="sw" style="background:var(--soon)"></i>due within 30 days</span>
    <span><i class="sw" style="background:var(--ok)"></i>on track, evidence on file</span>
    <span><i class="sw" style="background:var(--none)"></i>no evidence found</span>
    <span><i class="sw" style="background:var(--info)"></i>changing</span>
    <span><i class="sw" style="border:1.5px solid var(--auto)"></i>prepared by software</span>
  </div>
</div></section>

<section><div class="wrap">
  <h2>The register</h2>
  <p class="sec-note">Every obligation, its next real due date, and the artefact that proves the last cycle closed. <strong>"None found" is a fact about the evidence folder, not about the filing.</strong></p>
  <div class="tablewrap"><table>
    <thead><tr><th>Next due</th><th>Obligation</th><th>State</th><th>Last evidence</th><th>If it slips</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div></section>

<section><div class="wrap">
  <h2>How this page is fed</h2>
  <p class="sec-note">Five parts, built in this order. Purple is the machine's job, blue is a person's, grey is not built yet. <strong>The machine never files, pays, or invents an obligation.</strong></p>
  <div class="pipe">
    <div class="stage"><div class="n">1 · Register</div><h4>One record per obligation</h4><p><code>data/obligations.yaml</code> — cadence, owner, evidence, consequence. Edited by pull request.</p><span class="who h">Person edits · built</span></div>
    <div class="stage"><div class="n">2 · Clock</div><h4>Computes next-due, writes calendar events</h4><p>This page's dates are computed at every deploy. Calendar events on "Grants, Reporting and Filing Requirements" are hand-entered for now.</p><span class="who m">Page built · calendar script next</span></div>
    <div class="stage"><div class="n">3 · Watcher</div><h4>Reads both mailboxes, matches senders</h4><p>Due notice → confirms. Acknowledgment → files evidence. Unknown agency → triage queue.</p><span class="who x">Not built</span></div>
    <div class="stage"><div class="n">4 · Escalation</div><h4>Overdue items go to the Treasurer too</h4><p>What survives a personnel gap.</p><span class="who x">Not built</span></div>
    <div class="stage"><div class="n">5 · Checks</div><h4>Two Xero queries</h4><p>1st/15th: bills awaiting approval. December: per-contractor totals from Gusto + Xero for 1099s.</p><span class="who x">Not built</span></div>
  </div>
  <p class="foot">Source: <code>github.com/makehaven/Process-Registry</code> — <code>data/obligations.yaml</code> for the rows, <code>data/obligations.md</code> for history and runbook pointers, <code>build/obligations.py</code> for this page.</p>
</div></section>
"""


def main() -> int:
    base = today()
    raw = yaml.safe_load(SRC.read_text())
    items = [resolve(i, base) for i in raw]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(items, base))
    n_over = sum(1 for i in items if i["overdue_since"] or i["state"] == "unresolved")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(items)} obligations, {n_over} overdue, as of {base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
