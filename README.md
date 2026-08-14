# MakeHaven Process Registry

A standing map of every operational process at MakeHaven — what it is, who owns
it, how manual it is, how well documented, how much it costs us when it breaks,
and whether it is changing right now.

**Live:** `process.makehaven.org` *(not yet published — see Deploy)*
**Track:** `makehaven-website/conductor/tracks/process_stabilization_20260814/`

---

## Why this is its own repo

It began inside the Drupal site's planning directory, which was the wrong home
for three reasons:

1. **Different release cycle.** Nothing here needs to ride Pantheon's deploy
   train, and coupling it there means a process-description typo waits for a
   site deploy.
2. **Different audience.** The output is read by board, staff and members, and
   potentially by other makerspaces — the CT Makerspace Network Standards of
   Excellence work is explicitly collaborative.
3. **It stopped being about the website.** Of 186 processes, well under half
   touch Drupal at all. Facilities, governance, finance and fundraising have no
   code behind them, and those are exactly the ones the registry exists to make
   legible.

## What it is and is not

**Is:** the standing map of processes and their current state. The canonical
short description of each. Links to the policy and procedure documents behind
them.

**Is not:**

- **A strategy tracker.** The five-year strategy sequence lives in its own
  spreadsheet with owners, priorities and a PLAN → DEVELOP → GROW → REFINE →
  MAINTAIN lifecycle. Processes carry `strategy_ids` pointing at it; they do not
  absorb it. The strategy sheet is edited by committees in Google Sheets and
  should stay that way.
- **A task or project system.** Conductor tracks own that.
- **A documentation platform.** Descriptions are a paragraph. Anything longer
  becomes a document in `docs/` or an external link.
- **Live operational monitoring.** The registry shows *maturity*, not *current
  health*. Dashboards own that.

The one thing it supplies that nothing else does: the strategy sheet is entirely
forward-looking and has no state meaning *this is broken right now and nobody is
on it*. That is 27 of our 186 processes.

## Layout

```
data/inventory.md        the registry itself — the source of truth
build/build.py           renderer: inventory.md -> public/index.html
build/shell.html         page template (CSS, prose sections, {{PLACEHOLDERS}})
docs/                    documents spun out of the registry when a description
                         outgrew a paragraph (e.g. RENEWAL_CALENDAR.md)
questions/               archived question rounds with answers inline — the raw
                         record behind every description. Append-only.
public/                  build output, gitignored
```

## Build

```bash
python3 build/build.py     # writes public/index.html
```

No dependencies beyond the Python standard library. The output is a single
self-contained HTML file.

## Deploy

Not wired up yet. Intended shape, matching the pattern already used by
`Voicemail-Tool`, `Phonebank-Tool` and `Sponsorship-Tool`:

- Firebase Hosting, custom domain `process.makehaven.org`
- GitHub Action on push to `main`: run the build, deploy `public/`
- **Public, read-only, no auth.** Fields marked staff-only are stripped at build
  time before anything is published.

## Conventions

- **Answers are the documentation.** Each process carries a description of two
  to five sentences plus `description_source` recording who said it and when.
  For most processes that paragraph *is* the written artefact the Standards of
  Excellence "Operational" level asks for.
- **Never overwrite a human assertion with an inference.** The AI maintenance
  pass may propose changes with cited evidence; it may not conclude. Three
  separate times during the seeding rounds, a gap inferred from missing
  documentation turned out not to exist.
- **The pass may not create or delete processes** — only update fields.
  Otherwise the inventory drifts toward whatever is easy to measure.
- **Scores move one step per pass.** A1 → A4 in a single commit is a symptom.

## Scales

| | Automation | Documentation | Impact |
|---|---|---|---|
| 1 / 0 | Tribal — lives in someone's head | Nothing written | Internal annoyance |
| 2 / 1 | Documented, executed by hand | Informal notes | Staff time, minor friction |
| 3 / 2 | Assisted — tooling helps, human drives | Current SOP exists | Member experience or revenue |
| 4 / 3 | Automated, humans handle exceptions | Proven — someone else has run it from the doc | Significant revenue, trust, data |
| 5 / — | Autonomous **and tells us when it fails** | — | Safety, legal, existential |

Documentation deliberately matches the CT Makerspace Network Standards of
Excellence 0–3 evidence scale, so a maintained registry produces that
self-assessment as a by-product.

**States:** `stable` · `changing` · `watch` · `planned` · `degraded` ·
`undefined` · `unknown`
