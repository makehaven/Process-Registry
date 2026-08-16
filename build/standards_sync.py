#!/usr/bin/env python3
"""Snapshot the Standards of Excellence framework into data/standards.json.

The framework lives in the Makerspace-Standards repo (a sibling checkout, still
in draft) as a JS constant inside the self-contained assessment app. The registry
build cannot depend on that checkout existing — CI builds in a bare clone — so
this script copies the data in, and the JSON is committed. Re-run it whenever
the framework changes; the build reads only the JSON.

    python3 build/standards_sync.py
"""
import json, pathlib, re, sys

APP = pathlib.Path.home() / "development" / "Makerspace-Standards" / "app" / "index.html"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "standards.json"

if not APP.exists():
    sys.exit(f"not found: {APP} — clone Makerspace-Standards beside this repo")

h = APP.read_text()

m = re.search(r"const STANDARDS = \[(.*?)\n\];", h, re.S)
if not m:
    sys.exit("could not find `const STANDARDS` in the app")
standards = []
for row in re.finditer(
        r'\{ id:"(S\d+)",\s*d:"([^"]+)",\s*m:"([^"]+)",\s*t:(\d+),\s*c:(true|false),\s*'
        r's:"((?:[^"\\]|\\.)*)",\s*e:"((?:[^"\\]|\\.)*)"', m.group(1)):
    sid, d, mod, t, c, s, e = row.groups()
    standards.append({"id": sid, "domain": d, "module": mod, "tier": int(t),
                      "critical": c == "true",
                      "statement": s.replace('\\"', '"'),
                      "evidence": e.replace('\\"', '"')})

m = re.search(r"DOMAINS = \[(.*?)\n\]", h, re.S)
domains = dict(re.findall(r'code: "([^"]+)", name: "([^"]+)"', m.group(1))) if m else {}

if len(standards) < 50 or not domains:
    sys.exit(f"parse looks wrong: {len(standards)} standards, {len(domains)} domains")

OUT.write_text(json.dumps({"source": "Makerspace-Standards app/index.html (draft framework)",
                           "domains": domains, "standards": standards},
                          indent=1, ensure_ascii=False) + "\n")
print(f"wrote {OUT.name}: {len(standards)} standards, {len(domains)} domains")
