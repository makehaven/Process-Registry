#!/usr/bin/env python3
"""Pull participation out of Firestore into a digest a human or an AI can act on.

The registry's source of truth is data/inventory.md, edited by hand. Votes and
comments never write back to it — that would let anyone with an account silently
rewrite the record. Instead this exports what people said into one markdown file,
and a person (or Claude, working from it) decides what changes.

    python3 build/digest.py                 # everything not yet reviewed
    python3 build/digest.py --all           # including already-reviewed
    python3 build/digest.py --mark-reviewed # flip the exported comments to reviewed

Auth is the caller's own gcloud credentials, so running this requires being a
project member — there is no service-account key checked in anywhere.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

PROJECT = "makehaven-process-registry"
BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "feedback-digest.md"
INVENTORY = ROOT / "data" / "inventory.md"

KIND_LABEL = {
    "correction": "Says this is wrong",
    "changed": "Says they changed it",
    "missing": "Says something is missing",
    "priority": "Disagrees with the priority",
    "context": "Adds context",
}


HINT = (f"You need gcloud signed in as an account with Firestore access on\n"
        f"{PROJECT} — that is the MakeHaven Google account, not a personal one:\n\n"
        f"    gcloud auth login jrlogan@makehaven.org\n\n"
        f"The Firebase CLI keeps its own separate login, so being signed in to\n"
        f"`firebase` is not enough for the Firestore REST API.")


def token(account: str | None) -> str:
    cmd = ["gcloud", "auth", "print-access-token"]
    if account:
        cmd.append(f"--account={account}")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("gcloud not found — install the Google Cloud CLI.\n\n" + HINT)
    except subprocess.CalledProcessError as e:
        sys.exit(f"Could not get an access token.\n{e.stderr.strip()}\n\n" + HINT)
    return out.stdout.strip()


def untyped(value: dict):
    """Firestore REST wraps every scalar in a type tag; unwrap back to Python."""
    if "nullValue" in value:
        return None
    for k in ("stringValue", "booleanValue"):
        if k in value:
            return value[k]
    if "integerValue" in value:
        return int(value["integerValue"])
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "timestampValue" in value:
        return value["timestampValue"]
    if "arrayValue" in value:
        return [untyped(v) for v in value["arrayValue"].get("values", [])]
    if "mapValue" in value:
        return {k: untyped(v) for k, v in value["mapValue"].get("fields", {}).items()}
    return None


def fetch(collection: str, bearer: str) -> list[dict]:
    """Read a whole collection, following pagination."""
    docs, page = [], None
    while True:
        url = f"{BASE}/{collection}?pageSize=300" + (f"&pageToken={page}" if page else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {bearer}"})
        try:
            with urllib.request.urlopen(req) as r:
                body = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                sys.exit(f"Permission denied reading `{collection}`.\n\n" + HINT)
            sys.exit(f"Firestore returned {e.code} for `{collection}`: {e.read()[:400].decode()}")
        for d in body.get("documents", []):
            row = {k: untyped(v) for k, v in d.get("fields", {}).items()}
            row["_name"] = d["name"]
            row["_id"] = d["name"].rsplit("/", 1)[-1]
            docs.append(row)
        page = body.get("nextPageToken")
        if not page:
            return docs


def mark_reviewed(ids: list[str], bearer: str) -> None:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for doc_id in ids:
        url = (f"{BASE}/feedback/{doc_id}"
               f"?updateMask.fieldPaths=status&updateMask.fieldPaths=reviewedAt")
        payload = json.dumps({"fields": {
            "status": {"stringValue": "reviewed"},
            "reviewedAt": {"stringValue": now},
        }}).encode()
        req = urllib.request.Request(url, data=payload, method="PATCH", headers={
            "Authorization": f"Bearer {bearer}", "Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            print(f"  ! could not mark {doc_id}: {e.code}", file=sys.stderr)
    print(f"marked {len(ids)} comments reviewed")


def known_processes() -> dict[str, str]:
    """pid -> current name, derived the same way build.py derives it.

    build.py writes the page as a side effect of import, so it cannot be reused
    as a module without refactoring it. The slug rule is duplicated here instead;
    if it ever changes in build.py it has to change here too, and the "Orphaned"
    section of the digest is what will notice if it does not.
    """
    group, out = None, {}
    for ln in INVENTORY.read_text().split("\n"):
        m = re.match(r"^## (.+)$", ln)
        if m:
            t = m.group(1).strip()
            group = None if any(k in t for k in (
                "How to read", "The strategic plan", "What v2", "What v3",
                "What the seed", "The resource layer", "Where this draft",
                "Suggested agenda")) else t
            continue
        if group and ln.startswith("| "):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) == 6 and c[1] != "A" and not set(c[1]) <= set("-: "):
                raw = f"{group} {c[0]}"
                slug = re.sub(r"[^a-z0-9]+", "-", raw.lower().replace("&", " and ")).strip("-")
                out[slug[:120]] = re.sub(r"[*`]", "", c[0])
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true",
                    help="include comments already marked reviewed")
    ap.add_argument("--mark-reviewed", action="store_true",
                    help="after writing the digest, flip the exported comments to reviewed")
    ap.add_argument("--account", default=None,
                    help="gcloud account to authenticate as "
                         "(default: whichever gcloud is currently using)")
    args = ap.parse_args()

    bearer = token(args.account)
    feedback = fetch("feedback", bearer)
    votes = fetch("votes", bearer)
    known = known_processes()

    fresh = [f for f in feedback if args.all or f.get("status") == "new"]
    fresh.sort(key=lambda f: f.get("createdAt") or "")

    # ---- vote tallies -------------------------------------------------------
    tally: dict[str, dict] = collections.defaultdict(
        lambda: {"up": 0, "down": 0, "voters": []})
    for v in votes:
        pid = v.get("processId")
        if not pid:
            continue
        t = tally[pid]
        t["up" if v.get("value") == 1 else "down"] += 1
        t["voters"].append((v.get("name") or "?", v.get("value")))

    ranked = sorted(tally.items(), key=lambda kv: (
        -(kv[1]["up"] - kv[1]["down"]), -kv[1]["up"], kv[0]))

    orphans = sorted(set(tally) - set(known))
    orphan_comments = sorted({f["processId"] for f in feedback
                              if f.get("processId") and f["processId"] not in known})

    # ---- write --------------------------------------------------------------
    now = datetime.datetime.now(datetime.timezone.utc)
    L: list[str] = []
    add = L.append
    add(f"# Participation digest — {now:%Y-%m-%d}")
    add("")
    add(f"_Exported from Firestore (`{PROJECT}`) at {now:%Y-%m-%d %H:%M} UTC. "
        f"{len(fresh)} comment(s) {'in total' if args.all else 'awaiting review'}, "
        f"{len(votes)} vote(s) across {len(tally)} process(es)._")
    add("")
    add("**This file is an input, not a source of truth.** Nothing here has been applied to")
    add("`data/inventory.md`. Read it, decide what is actually true, and edit the inventory by")
    add("hand — a vote is a signal about priority, and a comment is a claim that still needs")
    add("checking against the system it describes.")
    add("")

    if not fresh and not votes:
        add("## Nothing yet")
        add("")
        add("No votes and no comments. If the page has been live for a while, that is itself")
        add("worth knowing — check that sign-in actually works before concluding people are quiet.")

    # comments
    if fresh:
        add("---")
        add("")
        add("## Comments")
        add("")
        by_pid = collections.defaultdict(list)
        for f in fresh:
            by_pid[f.get("processId") or "__general__"].append(f)
        for pid in sorted(by_pid, key=lambda k: (k == "__general__", known.get(k, k))):
            items = by_pid[pid]
            if pid == "__general__":
                add("### The registry as a whole / missing processes")
            else:
                name = known.get(pid)
                add(f"### {name or pid}" + ("" if name else "  ⚠️ *no longer in the inventory*"))
                if name:
                    add("")
                    add(f"<sub>`{pid}` · {items[0].get('group') or '—'} · "
                        f"currently `{items[0].get('state') or '?'}`</sub>")
            add("")
            for f in items:
                who = f.get("name") or "Unknown"
                roles = ", ".join(f.get("roles") or []) or "no role claims"
                when = (f.get("createdAt") or "")[:16].replace("T", " ")
                add(f"- **{KIND_LABEL.get(f.get('kind'), f.get('kind'))}** — "
                    f"{who} ({roles}), {when}")
                for para in (f.get("text") or "").strip().split("\n"):
                    if para.strip():
                        add(f"  > {para.strip()}")
                add("")

    # votes
    if ranked:
        add("---")
        add("")
        add("## Votes on the Next ranking")
        add("")
        add("Net is up minus down. The page caps the effect at ±5 regardless of how large net")
        add("gets, so a wide margin here means agreement, not extra weight.")
        add("")
        add("| Process | Up | Down | Net | Who |")
        add("|---|---:|---:|---:|---|")
        for pid, t in ranked:
            name = known.get(pid) or f"`{pid}` ⚠️ gone"
            voters = ", ".join(f"{n}{'▲' if v == 1 else '▼'}" for n, v in
                               sorted(t["voters"], key=lambda x: (-x[1], x[0])))
            add(f"| {name} | {t['up']} | {t['down']} | "
                f"{t['up'] - t['down']:+d} | {voters} |")
        add("")

        # The most useful thing in the whole file: where people disagree with us.
        contested = [(p, t) for p, t in ranked if t["up"] and t["down"]]
        if contested:
            add("### Contested")
            add("")
            add("Rows with votes in both directions — these are the disagreements worth a")
            add("conversation rather than an edit.")
            add("")
            for pid, t in contested:
                add(f"- **{known.get(pid) or pid}** — {t['up']} up, {t['down']} down")
            add("")

    if orphans or orphan_comments:
        add("---")
        add("")
        add("## Orphaned")
        add("")
        add("Votes or comments pointing at a process id that is no longer in the inventory —")
        add("almost always because the row was renamed. Rename it back, or migrate the")
        add("documents; leaving them here means the participation is silently discarded.")
        add("")
        for pid in sorted(set(orphans) | set(orphan_comments)):
            add(f"- `{pid}`")
        add("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n")
    print(f"wrote {OUT} — {len(fresh)} comment(s), {len(votes)} vote(s), "
          f"{len(tally)} process(es) voted on")
    if orphans or orphan_comments:
        print(f"  ! {len(set(orphans) | set(orphan_comments))} orphaned process id(s) — see digest")

    if args.mark_reviewed and fresh:
        mark_reviewed([f["_id"] for f in fresh], bearer)


if __name__ == "__main__":
    main()
