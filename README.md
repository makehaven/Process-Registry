# MakeHaven Process Registry

A standing map of every operational process at MakeHaven — what it is, who owns
it, how manual it is, how well documented, how much it costs us when it breaks,
and whether it is changing right now.

**Live:** `process.makehaven.org` — see [SETUP.md](SETUP.md) to publish
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
  MAINTAIN lifecycle. 74 processes carry the strategy ID acting on them, with its
  priority and work type; they do not absorb the sheet. It is edited by
  committees in Google Sheets and should stay that way. Its *numbers* — hours,
  year sequencing — are a live draft and are deliberately not reproduced here;
  what the registry builds on is the set of strategies and their priorities.
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
build/sweep.py           what changed in the website repo, and which rows it touches
build/questions.py       generates a question round from the registry's weak spots
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

Firebase Hosting at `process.makehaven.org`, matching the pattern already used by
`Voicemail-Tool`, `Phonebank-Tool` and `Sponsorship-Tool`. Config is committed
(`firebase.json`, `.firebaserc`, `.github/workflows/deploy.yml`); the project,
domain and CI secret are not yet created.

**One-time setup instructions: [SETUP.md](SETUP.md).**

Once wired, editing is: change `data/inventory.md`, commit, push. The Action
builds and redeploys in about a minute.

Public, read-only, no auth.

## How it stays current

Updating this is a **side effect of loops that already run**, never a separate
discipline. That is the whole design: two earlier attempts at this same idea
died because they needed someone to remember them.

| Loop | What it does here | When |
|---|---|---|
| **pantheon-deploy** — close-out | Mark affected processes `changing`; add rows for processes the work revealed | Staging a feature |
| **pantheon-deploy** — after live | Flip shipped processes to `watch` with what to watch for | Every release |
| **weekly-triage** | Mark `degraded` when the pulse finds something; close watches whose window passed clean | Weekly, only on real signal |
| **cycle-review** | Resolve expired watches, add processes the cycle revealed, re-check the `degraded` list, sanity-check change load | Biweekly |
| **flow-check** | A flow walk maps one-to-one onto processes — mark or close accordingly | Per flow |
| **security-audit** | Confirmed findings that leave a process unreliable → `degraded`, pointing at the ledger | Quarterly |

All of them defer to the **`process-registry` skill** in the website repo
(`.claude/skills/process-registry/`) rather than restating the how-to.

**The bar for touching it: did this work change how a process runs, or reveal
something about one?** If not, say so and move on. A registry edit on every
loop regardless of signal is exactly the ritual that killed the predecessors.

Expect the inventory to keep growing. The initial rounds mapped what could be
seen from the codebase, the strategic plan, the dashboards and two rounds of
questions; the processes nobody thought to mention surface later, usually
through triage or a flow walk.

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
