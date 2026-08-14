#!/usr/bin/env python3
"""Generate an interview from the registry's own weak spots.

The question rounds are what took this from guesses to a map, and they worked
because they asked about what was actually uncertain rather than working down a
fixed list. This regenerates that: it reads the current data, ranks what is
least trustworthy, and writes a question set worth someone's time.

It never invents an answer and never edits the inventory. Output goes to
questions/ as a new round, which is append-only.

    python3 build/questions.py              # print to stdout
    python3 build/questions.py --write      # write questions/questions-round-N.md
    python3 build/questions.py --limit 25   # how many questions (default 20)

Ranking favours questions whose answer would change something: high impact
first, then processes nobody can currently characterise, then claims that were
inferred and never confirmed by a person.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "inventory.md"
QDIR = ROOT / "questions"
SIGILS = "⚑◷⚙⚠⟐‖"


def load():
    rows, group = [], None
    for ln in SRC.read_text().split("\n"):
        m = re.match(r"^## (.+)$", ln)
        if m:
            group = m.group(1).strip()
            continue
        if not ln.startswith("| "):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) != 6 or c[1] == "A" or set(c[1]) <= set("-: "):
            continue
        note = c[5]
        f = {}
        for sig, key in zip(SIGILS, ["owner", "reviewed", "code", "raised", "strategy", "docs"]):
            if sig in note:
                f[key] = re.split(f"[{SIGILS}]", note.split(sig, 1)[1])[0].strip()
        rows.append(dict(group=group, name=re.sub(r"\*", "", c[0]).strip(),
                         a=c[1], d=c[2], i=c[3], state=c[4],
                         prose=re.split(f"[{SIGILS}]", note)[0].strip(), **f))
    return rows


def impact(r):
    return int(r["i"]) if r["i"].isdigit() else 3


def questions(rows):
    """(priority, category, process, question, why) — highest priority first."""
    out = []
    for r in rows:
        i, nm = impact(r), r["name"]
        base = i * 10

        if r["state"] in ("undefined", "unknown"):
            out.append((base + 40, "Uncharacterised", nm,
                        f"What actually happens when this runs — who does it, and in what order?",
                        f"State is `{r['state']}` at impact I{i}. Nobody can currently describe it."))
        elif r["state"] == "degraded":
            out.append((base + 30, "Degraded", nm,
                        "Is this still broken, and is anyone on it now?",
                        f"Marked degraded at I{i}. Degraded with nobody assigned is the "
                        "registry's main finding — confirm it is still true."))

        if not r.get("reviewed") and i >= 4:
            out.append((base + 25, "Never verified", nm,
                        f"Is this description accurate? — \"{r['prose'][:110]}\"",
                        f"I{i} and no person has ever confirmed it. Inferred from the "
                        "codebase or the plan, never checked."))

        if not r.get("owner") and i >= 4:
            out.append((base + 20, "No owner", nm,
                        "Who owns this, and who covers it when they are away?",
                        f"I{i} with no named owner. If it fails, there is no one to call."))

        if r["a"].isdigit() and int(r["a"]) <= 2 and r["d"] in ("0", "1") and i >= 3:
            out.append((base + 15, "Manual and unwritten", nm,
                        "If the person who does this left tomorrow, what would break, "
                        "and what would someone need to pick it up?",
                        f"A{r['a']} with D{r['d']} at I{i} — a human does every step and "
                        "nothing is written down."))

        if r.get("raised") and r["state"] == "stable":
            out.append((base + 35, "Flagged by staff", nm,
                        "What specifically should change here, and what would better look like?",
                        f"Someone raised this: {r['raised'][:90]}"))

    out.sort(key=lambda t: (-t[0], t[2]))
    # one question per process — the highest-priority angle
    seen, uniq = set(), []
    for q in out:
        if q[2] in seen:
            continue
        seen.add(q[2])
        uniq.append(q)
    return uniq


def render(qs, rows):
    n = 1
    while (QDIR / f"questions-round-{n}.md").exists():
        n += 1
    L = [f"# Questions — round {n}", "",
         "Generated from the registry's own weak spots by `build/questions.py`, "
         "ranked so the answers that would change the most come first.", "",
         "**Answer inline under each question.** Anything left blank stays unknown, "
         "which is a valid outcome — a guess recorded as fact is worse. When applying "
         "answers, stamp `◷ <date>` on the rows a person confirmed.", ""]
    cur = None
    for pri, cat, proc, q, why in qs:
        if cat != cur:
            L += [f"## {cat}", ""]
            cur = cat
        L += [f"### {proc}", "", f"**{q}**", "", f"_Why asked: {why}_", "", "> ", ""]
    L += ["---", "",
          f"_{len(qs)} questions across {len({q[2] for q in qs})} processes, "
          f"from {len(rows)} rows._"]
    return "\n".join(L), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    rows = load()
    qs = questions(rows)[:a.limit]
    if not qs:
        sys.exit("Nothing worth asking — no uncharacterised, degraded, "
                 "unverified or unowned high-impact rows.")
    text, n = render(qs, rows)
    if a.write:
        QDIR.mkdir(exist_ok=True)
        p = QDIR / f"questions-round-{n}.md"
        p.write_text(text + "\n")
        print(f"wrote {p.relative_to(ROOT)} — {len(qs)} questions")
    else:
        print(text)


if __name__ == "__main__":
    main()
