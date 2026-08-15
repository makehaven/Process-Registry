# MakeHaven Process Registry

A standing map of every operational process at MakeHaven — what it is, how
manual it is, how well documented, how much it costs us when it breaks, and
whether it is changing right now.

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
on it* (10 processes), nor *this was never built far enough* (17).

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
public/index.html        build output, gitignored
public/participate.js    sign-in, voting and comments (source, committed)
public/registry-config.js  deployment config — OAuth client id goes here
firestore.rules          who may vote, comment and read the comment inbox
build/digest.py          exports votes and comments for review
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

Public and readable with no account. Signing in with a MakeHaven account adds
voting and comments — see below.

## How it stays current

Updating this is a **side effect of loops that already run**, never a separate
discipline. That is the whole design: two earlier attempts at this same idea
died because they needed someone to remember them.

| Loop | What it does here | When |
|---|---|---|
| **pantheon-deploy** — close-out | Mark affected processes `changing`; add rows for processes the work revealed | Staging a feature |
| **pantheon-deploy** — after live | Flip shipped processes to `watch` with what to watch for | Every release |
| **weekly-triage** | Mark `degraded` when the pulse finds something actually failing; close watches whose window passed clean | Weekly, only on real signal |
| **digest review** | Read what staff and members said and voted; apply what holds up | Whenever the digest is non-empty |
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

**States:** `stable` · `changing` · `watch` · `planned` · `unoptimized` ·
`degraded` · `undefined` · `unknown`

`degraded` and `unoptimized` are both deficits and are not the same problem.
**`degraded` means it fails** — something that is supposed to happen does not,
whether it broke or never once fired. **`unoptimized` means it does what it was
built to do and was never built further.** The distinction matters because a
single word made 27 rows read as an emergency when 17 of them are ordinary
unfinished work, and because only one of the two is a reason to drop everything.

## Participation

The registry is a description of other people's work, written mostly by one
person. That is its biggest weakness, and the participation layer exists to
attack it directly.

Anyone with a MakeHaven account — staff, board or member — can sign in and:

The **Next** tab ranks on three inputs, all of them shown on the row so the
order can be argued with:

| Input | What it is | Weight |
|---|---|---|
| Arithmetic | impact × how manual it still is | base, 1–20 |
| The plan | P1/P2 from `data/strategies.csv`, matched by strategy name | +4 / +1 |
| The room | net votes from staff and members | ±5 |

A P1 also earns a place on the tab regardless of its scores, because that is
what the board choosing it meant. `strategies.csv` is read at build time rather
than copied into rows, so when the plan is finalised — it is heading for a
shorter priority list — replacing that one file re-ranks everything.

- **Vote a row up or down on the Next tab.** The base score is arithmetic
  (impact × how manual something still is). Net votes move it by up to ±5, which
  is enough to lift a row several places but not enough for a few early clicks to
  bury a safety process nobody voted on. Both halves stay visible on the row, so
  the ranking can be argued with rather than just distrusted.
- **Comment on any process** — this is wrong, we changed it, something is
  missing, wrong priority, or added context.
- **Read what everyone else said.** Comments are visible to any signed-in
  account, shown above the form on the process they are about. A suggestion box
  nobody can see into produces the silence it was built to fix, and it makes
  people file the same note five times. Because the whole membership can read
  them, no document stores an email address — `uid` resolves to the Drupal
  account when someone needs following up.

Identity comes from Drupal through the `makerspace_firebase_auth` bridge
(OAuth2 PKCE → Firebase custom token), so a vote carries a real account rather
than a typed-in name, and one person gets one vote per process structurally
rather than by promise.

**Nothing written by participants edits the registry.** Votes and comments live
in Firestore; `build/digest.py` exports them to `data/feedback-digest.md`, and a
person decides what is actually true before editing `data/inventory.md` by hand.
Letting anyone with an account rewrite the record directly would make the
registry a thing whoever clicked last owns.

The digest calls out two things specifically: **contested** rows where people
voted in both directions — disagreements worth a conversation, not an edit — and
**orphaned** ids where a vote points at a process that has since been renamed.

Setup is in [SETUP.md](SETUP.md) §6. Until the OAuth client id is filled in, the
page renders exactly as it did before with sign-in hidden.
