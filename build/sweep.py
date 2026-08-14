#!/usr/bin/env python3
"""Retrospective sweep: what changed in the website repo, and which processes does it touch?

The registry is normally updated as a side effect of work happening. This is the
other direction — for when nobody updated it for a while and you want to catch up.

It reports; it never edits. Mapping a commit to a process is a judgement call and
the output is a worklist for a human (or a session) to walk, not a patch.

    python3 build/sweep.py                 # since the recorded watermark
    python3 build/sweep.py --since 3.weeks # or an explicit git revision/date
    python3 build/sweep.py --set-watermark # record HEAD as swept, after acting

Rows are matched through their ⚙ code field, so a row only appears here if
someone attached its module. Rows without ⚙ are invisible to the sweep — that
gap is reported too, because it is the thing that limits this tool.
"""
import argparse, collections, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "inventory.md"
WATERMARK = ROOT / "data" / "sweep-watermark.txt"
WEBSITE = pathlib.Path.home() / "development" / "makehaven-website"
MODULE_ROOT = "web/modules/custom/"


def git(*args, repo=WEBSITE):
    out = subprocess.run(["git", "-C", str(repo), *args],
                         capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out.stdout


def load_rows():
    """Registry rows plus the modules each one claims."""
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
        code = ""
        if "⚙" in c[5]:
            code = re.split(r"[⚠⟐‖]", c[5].split("⚙", 1)[1])[0]
        rows.append(dict(group=group, name=re.sub(r"\*", "", c[0]).strip(),
                         state=c[4],
                         modules=[m.strip() for m in code.split(",") if m.strip()]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="git revision or date; defaults to the watermark")
    ap.add_argument("--set-watermark", action="store_true",
                    help="record the website repo's HEAD as swept and exit")
    args = ap.parse_args()

    if not WEBSITE.exists():
        sys.exit(f"website repo not found at {WEBSITE}")
    head = git("rev-parse", "HEAD").strip()

    if args.set_watermark:
        WATERMARK.write_text(head + "\n")
        print(f"watermark set to {head[:12]}")
        return

    since = args.since
    if not since and WATERMARK.exists():
        since = WATERMARK.read_text().strip().split()[0]
    if not since:
        since = "3.months"

    rev = f"{since}..HEAD" if re.fullmatch(r"[0-9a-f]{7,40}", since) else None
    log_args = ["log", "--no-merges", "--name-only", "--format=%x00%H%x1f%an%x1f%ad%x1f%s",
                "--date=short"]
    log_args += [rev] if rev else [f"--since={since}"]
    raw = git(*log_args)

    commits = []
    for chunk in raw.split("\x00"):
        if not chunk.strip():
            continue
        header, _, files = chunk.partition("\n")
        sha, author, date, subject = header.split("\x1f")
        touched = [f for f in files.split("\n") if f.strip()]
        commits.append(dict(sha=sha, author=author, date=date, subject=subject,
                            files=touched))

    rows = load_rows()
    by_module = collections.defaultdict(list)
    for r in rows:
        for m in r["modules"]:
            by_module[m].append(r)

    # which modules were touched, and by what
    mod_commits = collections.defaultdict(list)
    for c in commits:
        for f in c["files"]:
            if f.startswith(MODULE_ROOT):
                mod = f[len(MODULE_ROOT):].split("/")[0]
                if c not in mod_commits[mod]:
                    mod_commits[mod].append(c)

    span = f"{since}..HEAD" if rev else f"last {since}"
    print(f"Sweep of {WEBSITE.name} — {span}")
    print(f"{len(commits)} commits, {len(mod_commits)} custom modules touched\n")

    matched = {m: v for m, v in mod_commits.items() if m in by_module}
    unmatched = {m: v for m, v in mod_commits.items() if m not in by_module}

    if matched:
        print("=" * 72)
        print("PROCESSES TO REVIEW — a module they claim has changed")
        print("=" * 72)
        for mod, cs in sorted(matched.items(), key=lambda kv: -len(kv[1])):
            print(f"\n  {mod}  ({len(cs)} commit{'s' if len(cs) > 1 else ''})")
            for c in cs[:4]:
                print(f"      {c['date']} {c['sha'][:8]} {c['subject'][:64]}")
            if len(cs) > 4:
                print(f"      … {len(cs) - 4} more")
            for r in by_module[mod]:
                print(f"    -> {r['name']}  [{r['state']}]  ({r['group']})")
    else:
        print("No touched module maps to a registry row.\n")

    if unmatched:
        print("\n" + "=" * 72)
        print("TOUCHED BUT UNMAPPED — no row claims these; add ⚙ or add a process")
        print("=" * 72)
        for mod, cs in sorted(unmatched.items(), key=lambda kv: -len(kv[1])):
            print(f"  {mod:44} {len(cs):3} commit{'s' if len(cs) > 1 else ''}"
                  f"  (last: {cs[0]['subject'][:40]})")

    n_code = sum(1 for r in rows if r["modules"])
    print("\n" + "-" * 72)
    print(f"Coverage: {n_code}/{len(rows)} rows carry ⚙ code. The other "
          f"{len(rows) - n_code} cannot be reached by this sweep.")
    print(f"After acting:  python3 build/sweep.py --set-watermark   "
          f"(would record {head[:12]})")


if __name__ == "__main__":
    main()
