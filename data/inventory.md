# Process Inventory — v10 (fully characterised)

_Drafted 2026-08-14. **v2** added the two strategic-plan drafts, the
`makerspace_dashboard` sections and chart builders, and the entrepreneurship
stack. **v3** added the sibling app repos, the resource layer absorbed from
`makehaven.org/operations`, and four corrections from JR. **v4** adds eight
processes found by testing the inventory against the CT Makerspace Network
**Standards of Excellence** self-assessment. **v5 applies JR's answers to the
round-1 question set — 69 rows re-scored, two major corrections verified against
the database.** **v10 (2026-08-18) adds six processes found by sweeping the
website's custom modules against this file and measuring each survivor on live:
equipment & area reservation, member printing, the Slack membership lifecycle
sync, scheduled job execution, the member-facing AI assistants and the member
file bucket.** Still not reviewed by staff beyond JR._

**Roughly half the inventory is now answered rather than guessed.** Rows carrying
"Corrected from" in their notes come from JR directly; the rest are still
inferred from the codebase, dashboards, strategic plans, app repos, operations
doc and Standards of Excellence. Read "Where this draft is weakest" before
trusting an un-annotated number.

## How to read it

- **A** = automation, A1 tribal → A5 autonomous + monitored
- **D** = documentation, D1 nothing written → D5 proven and kept current.
  Runs 1–5 like **A**, and the two are read the same way: same number, same
  distance from finished. D5 mirrors A5 — A5 tells us when it stops, D5 tells us
  when it has gone stale. Both are empty today.
- **I** = impact when it fails, I1 annoyance → I5 safety/legal/existential
- **State** = `stable` · `changing` · `watch` · `planned` · `idea` ·
  `optimizable` · `broken` · `undefined` · `unknown`
- `idea` sits below `planned`, and the line between them is commitment.
  `planned` means someone has said *we will do this*; `idea` means *we are
  considering this* — a brainstorm, a research question, a maybe. Ideas are
  deliberately inert: they never enter the Next ranking or the change load,
  because a thing nobody has committed to cannot be urgent. Promoting one to
  `planned` is a decision, and should be recorded as one.
- `broken` and `optimizable` are both deficits and are not the same problem.
  **`broken` means it fails** — something that is supposed to happen does not,
  whether it broke or never once fired. **`optimizable` means it does what it was
  built to do and was never built to its end goal.** Do not use `broken` for work
  that was simply never finished; that was the error this vocabulary corrects.
- `optimizable` is narrow. Almost anything here could be improved — reserve it for
  a process with an end state someone can name that was never reached. If nothing
  exists to improve yet, the state is `planned`.
- **◊** marks a description written from the row's name, module and strategy
  rather than by someone who runs the process. It is a separate claim from **◷**,
  which records that a person confirmed the state and scores. Replacing a drafted
  sentence with a real one means deleting the ◊ field.
- **?** in a score column = genuinely unknown. Do not guess it in review — ask the
  person who does it. `undefined` means the *process* has no defined shape;
  `unknown` means it runs but we cannot currently characterise it.
- **▦** names the strategic-plan KPI(s) this process moves, by their ids in the
  dashboard's `kpis.yml`. The build resolves them to a link to the dashboard
  section that charts them — a pointer, never an embedded number, because the
  registry shows maturity and dashboards own current health. The build also
  reports which KPIs have *no* process pointed at them, which is the list of
  numbers the plan tracks that nothing here claims to move.

Full scale definitions are in `plan.md`. There is deliberately no owner field:
most work here is collaborative or automated — the optimization and digitization
is often done by JR or by AI, while the person who tests it and says whether it
actually works is someone else — so one name per process described neither role
honestly. `◷ reviewed` records that a person confirmed the row, which is the
accountability that turned out to be real.

---

## The strategic plan already asked for this

The two working-draft strategic plans make this track's case better than the
track does. Three passages, quoted:

> **Lever strategy #1:** "Systematize, stabilize, and […]: website, systems,
> operations to lay the groundwork for growth, innovation, responsiveness
> [move past start-up style]"

> **Facilities & Operations, Year 1 Strategy #5 — 200 hours budgeted:**
> "Establish and conduct a regular, consistent process for reviewing,
> improving, and stabilizing operational systems and procedures."

> **Governance — Leadership and Succession Planning:** "Document key staff processes and responsibilities to
> support operational stability during leadership changes."

And, in a margin comment on the AI-automation strategy, a reviewer wrote:

> "It might be worth doing an audit of the current systems first to make sure
> they're actually efficient before bringing in AI. That way, we're improving
> the process itself, not just automating around any existing issues."

That comment is this registry, requested by name, before it existed. This track
is not a side project — it is Year 1 Strategy #5, and it is the prerequisite the
reviewer put on Infrastructure — AI-Driven Automation and Member Support.

### The number that makes the ranking matter

**Corrected 2026-08-14 against the live planning sheet.** I previously put the
Year 1 ask at "roughly 3,300 hours" by summing inline estimates in the narrative
plan. The working Hours sheet is authoritative and lower:

| | hours |
|---|---:|
| 4.0 FTE × 40h × 52w | 8,320 |
| Less 90% keeping the lights on | −7,520 |
| **Available for strategy, Year 1** | **800** |
| **Estimated for the Year 1 strategy list** | **1,480** |
| **To postpone, reduce, delete or hire against** | **680** |

So the real figure is **1.85× oversubscribed with 680 hours to find**, not 4×.
That is a materially more solvable problem, and the sheet is already solving it —
strategies 8, 10, 11, 16 and 17 are struck as redundant, 18b is cut from 100
hours to 50, and the safety programme carries the note "remove if no hours?".

The registry's job here is narrow and useful: **when something has to be cut, an
impact × manual-effort ranking over a real inventory is a better basis than
whichever strategy has the loudest advocate.** The 680 hours has to come from
somewhere.

### Alignment with the strategy sequence sheet

The strategy sheet carries a work-type lifecycle staff already use. The registry
should adopt that vocabulary rather than invent a parallel one:

| Strategy sheet work type | Registry state |
|---|---|
| PLAN | `planned` |
| DEVELOP | `changing` |
| GROW | `changing` |
| REFINE | `watch` |
| MAINTAIN | `stable` |
| — *(no equivalent)* | **`optimizable`** |
| — *(no equivalent)* | **`broken`** |
| — *(before the sheet begins)* | **`idea`** |

**Those last two rows are the point.** The strategy sheet is entirely
forward-looking: every state describes work someone intends to do. It has no way
to say *this is broken right now and nobody is on it* (10 processes), nor *this
was never built far enough and no strategy is pointed at it* (17). The two
systems are complementary rather than duplicative, and that gap is the clearest
justification for the registry existing alongside the plan.

Each process therefore carries the strategy that acts on it, named as the plan names it, rather than
absorbing the strategy sheet. That makes two questions answerable that neither
system can answer alone: *which processes does this strategy touch?* and — more
useful for the 680-hour problem — *which of our broken and optimizable
processes has no strategy pointed at it?*

### Group → strategic goal mapping

Each process carries a `strategic_goal` field so the board can read the registry
rolled up by the plan's structure while staff read it by operational group.
DEI is a cross-cutting **tag**, not a group — matching the plan's own note that
"DEI strategies [are] integrated in other sections."

| Registry group | Strategic goal | Committee / dashboard |
|---|---|---|
| Education & Instruction | 1 Program | Education |
| Entrepreneurship | 1 Program | Entrepreneurship |
| Facilities & Equipment | 2 Facilities & Operations | Infrastructure |
| Access & Safety | 2 Facilities & Operations | Infrastructure |
| Lending, Storage & Store | 2 Facilities & Ops / 5 Financial | Operations |
| Membership & Billing | 3 Membership | Retention / Finance |
| Member Experience & Retention | 3 Membership | Retention |
| Outreach & Recruitment | 4 Visibility & Outreach | Outreach |
| Communications | 4 Visibility & Outreach | Outreach |
| Finance & Accounting | 5 Financial strength | Finance |
| Development & Fundraising | 5 Financial strength | Development |
| Governance & People | 6 Organizational effectiveness | Governance |
| Platform & Meta | 6 Organizational effectiveness | Infrastructure |

---

## The resource layer — answering the bus-factor question

**Yes, the registry should carry links, and there is already a document doing
this job to absorb rather than replace.** `makehaven.org/operations` redirects
to a Google Doc that opens: *"a compilation of key organizational documents…
1) A reference for future staff of the organization 2) a convenient way to
share."* It holds **~70 real policy, procedure, agreement and job-description
links** — bylaws, conflict of interest, whistleblower, safety program, hazard
bands, membership agreement, member warning and termination, storage ticketing,
donation acknowledgement, LAI scoring sheet, every staff job description.

That is the existing answer to the bus-factor question and the direct ancestor
of this registry. It is also `broken`, for reasons the registry structurally
fixes:

| The operations doc | The registry |
|---|---|
| A flat list of documents | Documents attached to the process that uses them |
| No dates — cannot tell current from abandoned | `reviewed` date and doc staleness derived from file mtime |
| No owner per document | Owner and backup per process |
| At least one broken link (Workspace Use Agreement) | Link-checkable in the build |
| Back half is an unrelated makerspace field-trip photo log | Scoped to operations |
| Nothing says whether the document is *followed* | A/D/I scores say exactly that |

**40 of the 186 rows now carry `Docs` links** pulled from it. The remaining
~30 operations-doc links are background, reference material, or belong to
processes the session will add. Two things fell out of doing this that no
other source surfaced: **member conduct & discipline** (warning and termination
procedures exist as documents; whether they are followed or logged is unknown)
and **harassment & conduct complaints** (public policy, invisible intake). Both
are I5. Both were missing from v2 entirely.

The schema field is `resources:` — a list of `{label, url}` — and the honest
version of D0–D3 depends on it: *"a current SOP exists"* is a claim you can only
check against a link.

---

## What v3 changed

Four corrections and one new source, all from JR:

1. **UniFi is an add-on to access control, not its own system.** Its row is
   gone; the fact now lives as a note on access-control hardware operations,
   with the standing reminder that UniFi sync errors are not a door outage.
2. **Access control is split in two, and tool access is the bigger problem.**
   *Door access control* (building entry) and **tool access control
   (interlocks)** are now separate rows. Tool access is `degraded` at I5 — per
   JR, the biggest thing not working, with repeated bug-and-redeploy cycles.
   Both share a root cause the architecture plan already names: every tap
   depends on Drupal being reachable, and *"we have repeatedly hit this failure
   mode."* The local-primary rearchitecture is drafted and pre-implementation —
   which makes it the highest-value item in the whole inventory.
3. **Incident reporting is not undefined.** The intake exists at
   `/safety-concern-and-accident-report-form` and covers injuries, illnesses and
   near misses. The gap is the back half: reviewed by "a committee of the board
   and potentially others," with no response time, no escalation, and no
   notification to the reporter. Re-scored A3/D1, `degraded` — a genuinely
   different and more actionable finding than "we have no process."
4. **The sibling app repos added five processes** — see below.

### What the app repos revealed

| App | Added / changed |
|---|---|
| Voicemail-Tool + `makerspace_voice` | **Inbound phone & voicemail triage** — live but inert (mock mode, no number bought). Who answers the phone today is undocumented |
| Phonebank-Tool + `makerspace_phonebank` | **Member phonebank campaigns** — a built tool whose operating cadence is undocumented |
| Inventory-App | **Physical inventory count** — SPA exists, README is literally "Readme TODO later", no count cadence |
| `time-report` | **ED time reporting to board** — new Aug 2026. Also the only real source for the `effort_hrs_month` field this registry lacks |
| Grant-Researcher | Sharpens an existing row: a full discovery-and-scoring app is deployed **and 0 grants were submitted YTD against a goal of 12.** The tool is not the bottleneck |
| Governance-Dance | A board-governance app — agendas, committee chairs, attendance, board demographics for grants, self-assessment — covering perhaps six of the `undefined` Governance rows. Whether it is *in use at MakeHaven* is the question for the session |

The Governance-Dance find is the sharpest of these: several Governance rows may
be closer to solved than the registry says, or may be a built tool nobody
adopted. Those are opposite conclusions and only staff can say which.

---

## What v2 changed

The v1 seed had 94 processes and four near-empty groups. Adding the strategic
plan and the dashboards roughly doubled it, and the additions are not evenly
spread:

- **Two entirely new groups** — Entrepreneurship (11) and Development &
  Fundraising (11) — neither of which appeared in v1 at all, despite
  Entrepreneurship having four custom modules and a dashboard section, and
  Development having its own committee, dashboard, and five strategic objectives.
- **Governance & People went from 6 rows to 17.** Board recruitment,
  nomination, onboarding, self-assessment, minutes retention, policy review,
  succession, the governance archive, volunteer role tracking, staff
  onboarding — all real, all recurring, essentially none of them defined.
- **Outreach went from 0 rows to 13.** v1 folded outreach into Communications
  and lost the entire conversion funnel: tours, guest waivers, workshop
  participants, referrals, ambassadors.
- **Facilities gained the things members actually complain about** — building
  maintenance and landlord liaison, tool downtime tracking, the safety program.

The pattern in v1 holds and got sharper: **the repo sees code, the strategic
plan sees intent, and neither sees the recurring human work.** It took both
sources plus the dashboards to find the second half of the list.

---

## What the seed shows

**186 processes across 13 groups.**

| | v4 (guessed) | round 1 | round 2 | round 3 |
|---|---:|---:|---:|---:|
| `stable` | 40 | 86 | 116 | **118** |
| `unoptimized` | — | — | — | **17** |
| `degraded` | 28 | 31 | 27 | **10** |
| `watch` | 12 | 13 | 13 | 13 |
| `changing` | 8 | 11 | 14 | 14 |
| `planned` | — | — | 14 | 14 |
| `undefined` | 56 | 31 | 2 | **1** |
| `unknown` | 42 | 14 | 0 | **0** |

**Uncharacterised went 98 → 45 → 2 → 1.** Both of the last two turned out to be
*mis-scored rather than unknown*, which is the pattern that has held throughout:

- **Facilitator six-month renewal** is genuinely running. `webform_10645` shows
  two clean campaigns a year — Feb 2025 (40), Jul–Aug 2025 (33), Jan 2026 (31),
  Jul–Aug 2026 (38) — against 54 facilitators. What is missing is not the
  process but **a field to hold a term date**, which is the concrete reason it
  cannot be automated.
- **Board succession** is defined in the bylaws: director resignation, removal,
  vacancies, one-year officer terms with interim vacancies fillable until the
  next annual meeting, and staggered three-year director terms.

What survived was hiding inside the second one: **executive succession and
emergency authority**. The bylaws cover governance continuity; nothing covers
operational continuity. That row is now the single highest-impact undefined
process in the registry, and splitting it out is what made it visible.

**A new state, `planned`, carries 14 rows.** These are intentions we have not
started — an ambassador programme, planned giving, peer benchmarking — which
earlier drafts were unfairly counting as broken processes. Separating *not
started* from *running badly* is the single biggest improvement to the fairness
of this page, and it was JR's triage that made it possible.

- **Most of what looked missing was documentation, not practice.** 116 of 186
  processes run normally. Almost everything that moved out of `undefined` went
  straight to `stable` — it existed, it worked, it just wasn't written anywhere
  a new person could find it. **The gap at MakeHaven is legibility, not
  competence** — a different and far more tractable problem than the v4 page
  implied.
- **The registry now contains the documentation, not just a score for it.**
  Answers gathered while scoring became the `description` on each row, with
  `description_source` recording who said it and when. For most processes that
  paragraph *is* the D2 artefact.
- **Biggest single artefact produced:** the renewal, insurance and compliance
  calendar — nine recurring items with months, brokers, carriers and filing
  numbers — now at `docs/ops/RENEWAL_CALENDAR.md`. It lived entirely in one
  person's head until 2026-08-14.
- **Change load is 24 processes, not a percentage.** The percentage fell from v1 only
  because the denominator doubled. Until the inventory stabilises, **track the
  count, not the ratio** — the ratio keeps moving for reasons that have nothing
  to do with how much is actually changing.
- **`degraded` split into `degraded` and `unoptimized`, 27 → 10 + 17.** The
  single word was doing two jobs and implied a regression that mostly had not
  happened. Only 10 processes actually fail — the interlock controller locking
  up, the instructor acknowledgement that never fires, $565/month of storage
  billing that never reconciles. The other 17 — planned giving, board–member
  engagement, guest-waiver follow-up — do what they were built to do and were
  never built further. That is ordinary unfinished work, and calling it
  degraded made the page read as an emergency it is not.
- **23 rows have no automation score**, and 16 are I5 (safety, legal, or
  existential). Three are both — unrankable and highest-impact: youth & school
  custodial partnerships, insurance/lease/compliance renewals, and backup &
  disaster recovery. (Incident reporting left this list in v3 — see below.)
- **Tool access control is the single most consequential `degraded` row**:
  I5, actively broken, and sharing a root cause with the door.
- **Roughly half the strategic plan's Year 1 strategies are requests to build a
  process that does not exist yet.** The registry's `undefined` rows and the
  plan's Year 1 list are substantially the same list, viewed from opposite ends.
  That is the strongest structural argument for the registry: it is the
  strategic plan's operational ledger, not a parallel document.
- **The KPI baselines confirm the gaps rather than contradicting them.**
  Equipment uptime baseline: `na` — not measured. Grants submitted YTD: `0`
  against a goal of 12. Incubator occupancy and active ventures: `TBD`.
  Entrepreneurship events: 23 participants against a goal of 300. Where the
  registry says `undefined`, the KPI table usually says `na`, `TBD`, or `0`.
- **Guest waiver → member conversion is 2.4%** against a 5% goal, on 218 waivers
  a year. Tours convert at 32%. Nobody owns the gap between those two numbers,
  and the automated follow-up that would close it is a Year 1 strategy.
- **Tool downtime tracking has already been tried and failed.** From JR's own
  margin note: *"I tried putting together an entire tracking system for when
  tools were down and it did not get traction, there were a lot of exceptions."*
  That is the single most useful row in the inventory — a documented failed
  attempt with a stated cause. Any new attempt starts from it.
- **The DEI committee has no active members**, per a margin exchange, while DEI
  objectives are cross-referenced from five other sections. A cross-cutting
  concern with no one to cut across.

---

## Education & Instruction

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Instructor recruitment funnel | 3 | 2 | 3 | optimizable | Menu consolidation shipped 08-12, **reverted 08-13** after staff objection. No CiviCRM link on instructor interest ⟐ Diverse Instructors and Inclusive Marketing — scaling next ▦ kpi_active_instructors_bipoc ⧉ P3 |
| Instructor proposal review | 3 | 2 | 3 | watch | `/admin/education` console — the half that survived the rollback ⧉ P3 |
| Instructor agreement signing | 2 | 2 | 3 | changing | Now staff-sent; orientation video + quiz switched off. 2 quiz questions contradict our own docs ‖ [Instructor Agreement](https://docs.google.com/document/d/1yd48GRRl0vHfPRcHiC-GEWXssXxcl0210_ps7qiyrC4/edit) ⧉ P3 S008 |
| Instructor interest acknowledgement | 4 | 1 | 3 | watch | **Fixed live 2026-08-13, re-verified against live 2026-08-17.** `webform_497`'s acknowledgement handler addressed `[…values:e_mail_address:raw]` while the element is `e_mail_address_25`, so it resolved empty and Webform declined to send — for every submission the form has ever taken. The token is now correct on live and both handlers fire. **A re-scored 1 → 4 in one step**: the old 1 scored the outcome (no acknowledgement ever arrived), not the mechanism, which was always an automatic Webform email with one wrong character. Two things the fix does not cover — the 129 people who submitted and heard nothing have still not been told, and the form *requires* topic images, machines and consumables, so a guest speaker offering a talk cannot submit it honestly ⧉ P3 |
| Instructor development & peer observation | 1 | 1 | 3 | planned | A way for instructors to keep improving after they start teaching — peers sitting in on classes and feeding back to the instructor. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Instructor Development and Diversity Pipeline — building next ⧉ S058 P3 |
| Instructor evaluation & coaching | 2 | 2 | 3 | optimizable | The education manager reviews evaluations as they arrive, but JR: "we can do much better to aggregate, and actually to get people to do the evaluations." Both halves — response rate and trend analysis — are weak ⟐ Quality Assurance and Continuous Improvement — planning next ⧉ S058 P3 |
| Class scheduling & publishing | 2 | 2 | 4 | changing | **Corrected from `unknown`.** The education manager engages a contractor who schedules. JR has self-serve scheduling in the pipeline, particularly for repeat instructors ◷ 2026-08-14 ⟐ Data-Driven and Automated Learning Systems — building next ‖ [Class Proposal Form](https://www.makehaven.org/Propose-a-class) ⧉ P3 |
| Class registration | 4 | ? | 4 | stable | CiviCRM ▦ kpi_workshop_attendees ⧉ P3 |
| Class promotion / seat fill | 4 | 2 | 3 | watch | Targeted empty-seats email still unbuilt ⟐ Personalized Engagement Tools — building next |
| Event capacity marketing | 4 | 2 | 2 | stable | Early Bird / Flash Sale ⚙ makehaven_event_capacity |
| Class attendance marking | 2 | 1 | 3 | watch | **Discovered 2026-08-17 by the weekly pulse — nobody had a row for it.** Recording who actually turned up to a class, which is what separates a registration from an attendance and feeds the education KPIs and the post-class follow-up. The purpose-built instructor path — the "Take attendance" screen in `instructor_companion` — is a **hard fatal and has never worked**: `AttendanceForm::buildForm()` calls `$this->entityTypeManager()`, which `FormBase` does not provide, so every instructor who clicks it gets a white screen. Six real attempts in the retained log window. It is not wholly unmarked, because staff can set participant status by hand in CiviCRM: over the last 30 days **12 marked Attended and 2 No-show against 110 still sitting at Registered**, so the fallback runs but rarely. **Fix staged 2026-08-17 (`instructor_companion` 19bae63), deploy pending** — the form now injects the entity type manager it was calling as a helper, verified locally by building and submitting against a real past class. **The fix reached live on 2026-08-20 and the fatal is gone** — live `composer.lock` pins `19bae637`, and the last `AttendanceForm::entityTypeManager()` error in live watchdog is 2026-08-18, before the deploy. **The outcome has not moved:** over the 30 days to 2026-08-20, **119 Registered against 12 Attended and 2 No-show** — the same ratio as before the fix. So the dead tool was never the whole problem; nothing prompts an instructor to open the screen, and the post-class reminder does not ask for attendance. Watching whether the unmarked count falls now that the form works; if it has not by mid-September, the next move is a prompt, not a repair. Scored A2 rather than A3 because the tooling half is dead and the surviving path is a human editing CiviCRM records, and D1 because nothing describes that fallback ⚙ instructor_companion ⧉ P3 |
| Class evaluation collection | 4 | 3 | 2 | watch | Applied live 08-11. NPS 76.4 but plan notes "low response rate for number of potential respondents" ‖ [Workshop Evaluation](https://docs.google.com/document/d/1mux1xU0hIU4tbtnHNygGNPVg7ge7XRjFkI4doj_Yiso/edit) ▦ kpi_education_nps ⧉ S057 S058 |
| Workshop fill-rate management | 3 | 2 | 4 | stable | The education manager watches fill rates; undersubscribed classes get automatic promotion in the newsletter, with automatic discounting intended later. 55% weighted fill against an 80% goal. *(JR, round 2)* ◷ 2026-08-14 ▦ kpi_workshop_capacity_utilization |
| Instructor stipend payment | 4 | 2 | 3 | stable | **Corrected from `unknown` — better automated than assumed.** Instructors submit hours on the instructor dashboard after class; those import to Xero/Melio and staff approve. JR: still being refined, but working ◷ 2026-08-14 ‖ [Instructor Agreement](https://docs.google.com/document/d/1yd48GRRl0vHfPRcHiC-GEWXssXxcl0210_ps7qiyrC4/edit) ⧉ P3 S046* |
| GEMS cohort management | 2 | 2 | 3 | stable | **Corrected from `unknown` — running now**, with details in the event listing ◷ 2026-08-14 ⟐ GEMs and Introductory Program Expansion — scaling next ⧉ S054 S056 |
| Badge quiz authoring | 2 | 2 | 3 | stable | **Corrected from `unknown`.** Mostly written by the shop manager, with a badge-quality report used to find problems — and acknowledged work to do there ◷ 2026-08-14 ⚠ Staff, 2026-08-14 — part of the badge-earning flow, which staff see as a major driver of retention and a strong candidate for review soon ⚙ assign_badge_from_quiz,quiz_notifications ‖ [Badge quality report (staff)](https://www.makehaven.org/admin/reports/badge-quality) · [Tool Orientation Checklists](https://drive.google.com/drive/folders/1JN7rJd1z_8lQed-syIrGxgQnkehl7qj2) ⧉ S022 S026 |
| Badge grant from quiz | 4 | 2 | 4 | stable | Auto-grants at 100% ⚠ Staff, 2026-08-14 — part of the badge-earning flow, which staff see as a major driver of retention and a strong candidate for review soon ⚙ assign_badge_from_quiz ⟐ Digital Badging and Workforce Pathways — scaling next ⧉ S022 |
| Badge checkout appointment | 4 | 2 | 4 | broken | A member books a one-to-one slot with a badger to be checked out on a tool and earn the badge. Runs automatically; a fault that broke the 60-minute slot length was fixed in July 2026. **Cancelling a booking has never returned the slot to the pool** — reported by staff 2026-08-19 (feedback sid 20312) and confirmed in code and data by the 2026-08-20 cycle review. The availability view carries exactly one cancellation filter and it reads `field_reservation_cancellation`, a vestigial field from the older reservation content type that **none of the 914 cancelled appointments on live carry**; all 914 stay published and keep their slot blocked. The booking form's JavaScript builds its list of taken slots straight from that view, so the lost capacity is invisible rather than merely cosmetic. Volume is steady rather than dramatic — about 31 cancellations per 30 days — which is why it went unnoticed for so long. **Fix staged 2026-08-20 (config only: the view now filters `field_appointment_status != canceled`), deploy pending**; verified against the real view query, which excludes the cancelled node and still blocks scheduled ones. Noted while fixing and not shipped: the view still pages at 15 rows sorted newest-first, so a facilitator with more than 15 appointments may not have every reserved slot rendered ◊ 2026-08-15 ⚙ appointment_facilitator,appointment_enhancements ⚠ Staff, 2026-08-14 — part of the badge-earning flow, which staff see as a major driver of retention and a strong candidate for review soon ⧉ S022 |
| Facilitator scheduling | 4 | 2 | 3 | stable | Sets and publishes which facilitators are covering which shifts, driven by the facilitator modules rather than a manual rota. ◊ 2026-08-15 ⚙ facilitator_api,facilitator_display,appointment_facilitator ‖ [Facilitator Training](https://docs.google.com/presentation/d/1jBctIZ_C1ntcK_Azp6i2lBER0UCNn4xTbYhdh0QxIME/edit) ⧉ S050 S051 S028 |
| Facilitator 6-month renewal | 2 | 2 | 3 | changing | **Corrected from `undefined` — it runs, and the data proves the cadence.** `webform_10645` "Current Facilitator Application Update" shows two clear campaigns a year: Feb 2025 (40), Jul–Aug 2025 (33), Jan 2026 (31), Jul–Aug 2026 (38) — against 54 facilitators, roughly a 60–75 per cent response each cycle. The six-month term is real and is actually being run. **What is missing is not the process but somewhere to put the answer: the coordinator profile has no term start or end field** (availability, capacity, email, focus, hours, on-request, requirements, scheduled hours — and nothing else), which is the concrete reason renewal cannot be reminded, rostered or offboarded automatically. Two dead forms should be archived: `webform_1680` "Current Facilitator Reapplication", last used Feb 2019, and `webform_8242` "Facilitator Evaluation", last used Aug 2023. *(Verified against the database, 2026-08-14)* **A track opened 08-11 now builds exactly the missing piece** — term fields, renewal reminders, onboarding and offboarding — which is why this row reads `changing` rather than `stable`. **Refined 2026-08-20 by the cycle review, and it makes the missing piece smaller than stated above.** The claim that there is nowhere to put a term stands — there is no term field — but the *recurrence already carries most of one*: `field_coordinator_hours` is a Smart Date field, all 70 facilitators have a weekly rule (7,744 instance rows, 72 rules, 6 rows with no rule at all), and the rule records a term **start** for everyone. A term **end** exists for 13 of 72 — `UNTIL=<date>` on 12, `COUNT=99` on one — while **59 (82%) are `unlimited`, running forward with no end at all**, which is the honest reason renewal cannot be rostered automatically today. So the Phase 0 question is narrower than "add term fields": require an `UNTIL` when hours are entered and the recurrence becomes authoritative, or add separate fields and accept two sources of truth for data that already drives live scheduling. **Do not add fields before that is decided with Kate.** ◷ 2026-08-14 ⚙ appointment_facilitator ⟐ Volunteer Pathways and Member Committees — scaling next ‖ [Community Facilitator Program](https://www.makehaven.org/community-animator-program) · [Facilitator Training](https://docs.google.com/presentation/d/1jBctIZ_C1ntcK_Azp6i2lBER0UCNn4xTbYhdh0QxIME/edit) ⧉ S051 S023* |
| On-request badger matching | 3 | 2 | 2 | stable | When no scheduled checkout slot suits a member, they request one and are matched to an available badger. Live since August 2026. ◊ 2026-08-15 ⚙ appointment_on_request ⧉ S050 S030 |
| Youth & school custodial partnerships | 2 | 3 | 5 | stable | **Materially lower risk than v3 assumed.** Minors attend as guests of their own guardians, or through school partnerships where **the school's instructor supervises — MakeHaven is not the custodian**. Youth safety policies are published. Standards module B still applies, but the screening burden largely sits with partners ⟐ Youth and School Collaboration — scaling next ‖ [Youth safety policies](https://www.makehaven.org/makehaven-youth-safety-policies) · [TurnBridge Youth Access MOU](https://docs.google.com/document/d/1VSmWqgyx-czRHzeCf12hh9PErIc7562RzAh3gTa2qGg/edit) · [BOE Sewing Program MOU](https://docs.google.com/document/d/1hCqDZTXjwF2nU_9cUZ2FKgiq0FLQilyYjH4AgiJa2Qc/edit) ⧉ S066 S067 S068 S069 S059 |
| Peer benchmarking (annual) | 1 | 1 | 2 | planned | An annual comparison of MakeHaven against similar makerspaces — membership, pricing, programming — to test our own numbers against the field. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Quality Assurance and Continuous Improvement — planning next ⧉ S084 |
| Public credential transcript (Open Badges) | 1 | 1 | 2 | planned | An opt-in shareable transcript of a member's badges and certifications, mapped to the Open Badges standard so credentials mean something outside the building. On the website master roadmap; groundwork shipped as the member public profile MVP. ◊ 2026-08-16 ⟐ Digital Badging and Workforce Pathways — scaling next |

## Entrepreneurship

_New group in v2. Four custom modules and a dashboard section exist; the
operating processes around them mostly do not._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Entrepreneur goal capture at signup | 4 | 2 | 3 | stable | `field_member_goal` — inventor / entrepreneur / seller. **46% of new members** identify this way ⧉ S054 |
| Entrepreneur dashboard & nudges | 4 | 2 | 2 | watch | `makerspace_entrepreneur_dashboard`. Member half was invisible (soft-launch block placed in the admin theme); fixed live 08-09 ⚙ makerspace_entrepreneur_dashboard |
| Entrepreneurship AI support assistant | 4 | 2 | 2 | stable | Early, experimental, explicitly non-critical and optional per JR. Worth watching against the tool-chatbot precedent rather than investing further yet ⚙ makerspace_ai_entrepreneur_support ⧉ P2 |
| Nexus platform bridge | 3 | 2 | 2 | stable | Experimental and used at a very light level, with hopes for future development. Members ticking entrepreneur goals should be invited into Nexus, but that path is underdeveloped and underused ⚙ entrepreneur_nexus_bridge ⧉ S059 |
| Incubator workspace intake & graduation | 2 | 2 | 3 | stable | **Intake corrected from `undefined`**: applicants apply and the director decides, with live availability published. **Graduation remains undefined** — nothing defines when a venture should move on ⟐ Incubator Workspace Program — scaling next ‖ [Workspaces](https://www.makehaven.org/workspaces) ▦ kpi_incubator_workspace_occupancy,kpi_active_incubator_ventures ⧉ S071 S072 S073 |
| Entrepreneurship milestone tracking | 1 | 1 | 3 | planned | Not started. Signup goal data is used for grant reporting and occasional outreach filtering, but no milestone tracking exists. *(JR, round 2)* ◷ 2026-08-14 ⟐ Metrics and Ecosystem Tracking — building next ⧉ S074 |
| Mentor & advisor matching | 1 | 1 | 3 | planned | Tried and abandoned: "it just did not work well, we would need to do redesign from ground up." A prior attempt exists as evidence, so any restart should begin from why it failed. *(JR, round 2)* ◷ 2026-08-14 ⟐ Entrepreneurship Coordination and Network Building — scaling next |
| Entrepreneurship events programming | 2 | 1 | 3 | optimizable | **23 participants against a 300 goal.** The gap is 13× ⟐ Entrepreneurship Events and Community Education — scaling next ▦ kpi_entrepreneurship_event_participation ⧉ S054 |
| Cohort programs (Ecolab-style) | 1 | 1 | 3 | planned | Running entrepreneurship support as fixed-intake cohorts rather than continuous enrolment, on the model of the Ecolab program. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Cohort-Based Entrepreneurship Programs — planning next ⧉ S074 |
| "Made at MakeHaven" marketplace | 1 | 1 | 2 | stable | Runs at a very light level: a Slack channel where members share design files. Nothing resembling the retail or pop-up presence in the strategic plan. *(JR, round 2)* ◷ 2026-08-14 ⟐ Maker Marketplace and Retail Presence — planning next ⧉ S071 |
| Ecosystem partner data alignment | 1 | 1 | 2 | planned | Actively being worked on — shared data standards with ClimateHaven, Collab and the Community Foundation. *(JR, round 2)* ◷ 2026-08-14 ⟐ Makerspace Network Integration and Collaboration — scaling next ⧉ S059 P2 |
| Opportunity relay (commissions, gigs & job posts) | 2 | 2 | 2 | changing | Outside people call or email wanting something made, or share a job opening; staff relay it to members by hand-pasting into Slack `#jobs`. An intake form has existed for four years with nothing downstream of it. A track opened 08-13 closes the loop — intake → light review → automatic post → auto-expiry — deliberately leaving member-to-member posts alone. ◊ 2026-08-16 ‖ [Opportunity Board track](https://github.com/makehaven/makehaven-website/tree/master/conductor/tracks/opportunity_board_20260813) |
| Venture business profiles & support logging | 1 | 1 | 2 | idea | Business profiles for incubated ventures plus a CiviCRM workflow logging every support touch, so grant applications draw on recorded data rather than recollection. Roadmap backlog; would carry the milestone tracking the dashboard had to retire. ◊ 2026-08-16 ⟐ Metrics and Ecosystem Tracking — building next |

## Facilities & Equipment

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Tool acquisition & commissioning | 2 | 2 | 3 | stable | **Corrected from `undefined`.** Budget first, then the member wishlist, then consultation with area experts; final call sits with the shop manager and executive director ◷ 2026-08-14 ‖ [Asset inventory](https://www.makehaven.org/asset/inventory) · [Asset Disposal Policy](https://docs.google.com/document/d/1D5d7KUBJr8kXA6f1ShQME3BPIrHW7ClzXyQ2wUS63Fc/edit) · [Wishes](https://www.makehaven.org/wishes) ▦ kpi_equipment_investment ⧉ S032 S015 P6 |
| Tool downtime & repair tracking | 3 | 2 | 4 | watch | **Major correction — v2 and v3 called this a failed attempt; it is live.** `asset_log_entry` holds 117 records and members report faults that feed the KPIs, with a tool-quality report checking configuration. The earlier "did not get traction" note was historical. **New concern from the data: logging has fallen off a cliff** — roughly 29/month across April–June, then 5 in July and 3 so far in August. Either faults dropped or reporting did, and those need different responses ‖ [Asset maintenance queue (staff)](https://www.makehaven.org/admin/content/asset-maintenance) · [Tool quality report (staff)](https://www.makehaven.org/admin/reports/tool-quality) ▦ kpi_equipment_uptime_rate,kpi_active_maintenance_load ⧉ S033 S034 |
| Preventive maintenance schedule | 2 | 2 | 4 | changing | **Corrected from `undefined`.** The shop manager keeps a spreadsheet of recurring tasks for the shop tech. Intent is to formalise it into `/tasks`; extending it to members is gated on first building a way to certify who is competent to repair what ◷ 2026-08-14 ⟐ Tool Maintenance and Replacement Planning — building next ⧉ S034 |
| Equipment depreciation & replacement planning | 2 | 2 | 3 | optimizable | **Currently driven by the CPA, not by us.** Once a year they ask what was acquired over $1,000 and what was disposed of. Additions are recorded in the site's equipment inventory. JR wants this connected to actual asset lifetimes so replacement is forecast rather than discovered. *(JR, round 2)* ◷ 2026-08-14 ⟐ Tool Maintenance and Replacement Planning — building next ‖ [Asset inventory](https://www.makehaven.org/asset/inventory) ⧉ S039 |
| Shop budget adherence | 2 | 2 | 3 | stable | **Corrected from `unknown`.** A shop budget line exists; the shop manager works within it and the executive director and finance committee monitor. *(JR, round 2)* ◷ 2026-08-14 ▦ kpi_adherence_to_shop_budget ⧉ S040 |
| Consumable restock | 3 | 2 | 2 | stable | **Corrected from `undefined`.** Store material pages let members flag an item as out; QR codes in the space feed a webform to the operations manager; store inventory has reorder thresholds. **Remaining gap: the free supplies out in the space have no system at all** ◷ 2026-08-14 ⧉ S013 |
| Physical inventory count | 4 | 2 | 3 | stable | **Corrected from `unknown`.** Used every month; JR reports staff like it and consider it well developed ◷ 2026-08-14 ‖ [Asset inventory](https://www.makehaven.org/asset/inventory) ⧉ S032 S038 |
| Equipment & area reservation | 4 | 2 | 3 | changing | **Added 2026-08-18 by a sweep of the custom modules — the registry had no row for it, and by volume it is one of the most-used member-facing systems we run.** Members book a machine or a whole area for a window of time; the booking checks conflicts up and down the asset hierarchy (holding "Laser Area" warns about an existing booking on "Laser 1", and booking "Laser 1" is refused while the area is held), enforces a per-asset maximum duration and minimum advance window, and lets staff override an ancestor conflict rather than be blocked by it. **2,893 reservations to date, 166 in the last 30 days from 64 distinct members; across 90 days 424 confirmed against 61 cancelled** (13% cancelled). The gap is documentation, not function: the hierarchy rules and the time limits live only in the module and in field values on each asset node, so a member refused a slot is not told which parent booking refused it, and nothing written says who may reserve what, for how long, or what happens to a no-show. **Badge authorization staged 2026-08-20 (e9a6721, deploy pending):** until now the booking checked role access but never badges, so a member holding only a Door badge could self-book the $70k water jet — 6 of 226 personal reservations on badge-required tools since launch were made by members without the badge. The gate refuses those, exempting staff and the supervised checkout itself; watch for legitimate bookings being blocked, and soften via `badge_gate_mode` rather than reverting ⚙ makerspace_reservations ⧉ S032 |
| Member printing (SavaPage) | 4 | 2 | 2 | stable | **Added 2026-08-18 by the module sweep.** Members print through SavaPage on an on-site print server: clicking "Open Printing" provisions a SavaPage account just-in-time, mints a one-time SSO token through a bridge service reached over a Cloudflare tunnel, and hands the member into the print queue with no second password. Balances are topped up at `/savapage/topup` through a Stripe-backed page on the bridge. **31 launches by 11 distinct members across the nine days of retained log, every one successful, no errors.** Two things want a decision rather than an assumption. **The membership gate the module was built with is switched off on live at both levers** — `require_active_membership` is `false` and `access savapage printing` is granted to `authenticated` rather than to `member` — so the role, pause and payment-failed checks never run and any registered account can open printing; the practical control is the SavaPage balance, which starts at $0. And the top-up money moves through the print server's own Stripe rather than the site's, so it sits outside the Stripe → Xero reconciliation this registry already tracks ⚙ savapage_auth |
| 24/7 self-access operation | 4 | 3 | 2 | stable | **Reframed — there is no opening or closing.** The space is 24/7 and unstaffed, with RFID access and the rules carried by the membership agreement. Standards S017 still wants explicit lone-work and after-hours protocols, which is a narrower ask than "document open and close" ‖ [Membership agreement](https://www.makehaven.org/membership-agreement) ⧉ S017 P1 |
| Cleaning & shop upkeep | 2 | 3 | 2 | stable | **Corrected from `undefined`.** Contracted to a member under a signed contract ◷ 2026-08-14 ‖ [Woodshop Dust Mitigation](https://docs.google.com/document/d/1s-zby2Ouw8b-R8NkKgpu-e1oUXxSRr4G4PYiDV8q1So/edit) ⧉ S036 |
| Building maintenance & landlord liaison | 2 | 2 | 4 | stable | **Better than v4 implied.** The landlord, Steven Bernblum, is himself a MakeHaven member; contact is by direct phone or text, by email, or through the ManageBuilding portal. Shop manager leads and the executive director escalates. The friction is responsiveness — a request typically needs a text and a reminder or two — not a missing channel. *(JR, round 2)* ◷ 2026-08-14 ‖ [ManageBuilding portal](https://bernblum.managebuilding.com/) · [Landlord (member profile)](https://www.makehaven.org/users/steven-bernblum) ⧉ P7 S035 |
| Safety program review & drills | 2 | 3 | 5 | stable | **Corrected from `undefined`.** The Safety Program Summary plus tool hazard levels are the core, with the rest embedded in the badging system and the membership agreement. **Emergency drills remain unaddressed** — Standards S011/S019 want them plus a trend review ◷ 2026-08-14 ⟐ Comprehensive Safety Program — refining next ‖ [Safety Program Summary](https://docs.google.com/document/d/1Zy8JqWkn_ZLyhUPM8tqK5jepFVNQe_Yy7pwtSbIulqg/edit) · [Hazard Bands](https://docs.google.com/drawings/d/1y85LYQM3PWhqW8MazO6iGBF_QF1YoJohnGUK3m89k7Y/edit) · [Safety Signage](https://drive.google.com/drive/folders/19JDhOYJorRwjviIgCVV0gH1jNEUO9e5M) ⧉ S011* S019 |
| Incident & near-miss reporting | 2 | 3 | 5 | stable | **Corrected twice.** Members and staff report incidents and near misses through an online form. The Safety & Accessibility committee reviews submissions **quarterly**, and reports reach a standing list of staff and volunteers. Real gaps are narrower — paper forms are re-keyed into the online form by hand, and the reporter is never told what happened ‖ [Report form](https://www.makehaven.org/safety-concern-and-accident-report-form) · [Safety Program Summary](https://docs.google.com/document/d/1Zy8JqWkn_ZLyhUPM8tqK5jepFVNQe_Yy7pwtSbIulqg/edit) · [Emergency resources](https://docs.google.com/document/d/1pm7AKcYorVGmJa5HbqGpVDIG8Jy9Ab4fbV8rq4YCrJA/edit) ⧉ S016* |
| Accessibility / ADA audit | 2 | 2 | 4 | stable | **Corrected from `undefined`.** A second annual walk-through by the same committee covers accessibility. JR: the audit happens, but there is no defined **review-and-improvement loop** after it ◷ 2026-08-14 ⟐ Accessibility and Inclusive Design — scaling next ⧉ S055* |
| Insurance / lease / compliance renewals | 2 | 3 | 5 | stable | **Now fully documented — the single biggest bus-factor win of this exercise.** Nine recurring items across insurance (General Liability + Umbrella in February, D&O in April, Workers' Comp in October, all through Wellstone), the 770 Chapel St lease, and compliance filings (CT annual report in March, CPA review April–June, Form 990 extended to November, CT charitable solicitation, board COI disclosures in July). Every one is still triggered by an inbound email rather than a calendar, which is how the 990 was late in 2025. Written up in full at `docs/ops/RENEWAL_CALENDAR.md`. *(JR, round 2)* ◷ 2026-08-14 ⧉ S001 S018 S043 |
| Sustainable operations practices | 1 | 1 | 2 | planned | What the organisation itself does about waste, energy and materials in the shops, as distinct from what members are asked to do. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Sustainable Operations Practices — planning next ⧉ S020 |
| Chemical inventory & SDS access | 2 | 3 | 5 | stable | **Corrected from `undefined`.** Dedicated flammables cabinets, a printed SDS binder for commonly-used chemicals, a published air-quality usage policy, and air monitors verifying conditions. JR notes the binder is due a review ◷ 2026-08-14 ‖ [Air quality policy](https://www.makehaven.org/air) ⧉ S013 |
| Lockout / tagout of unsafe equipment | 3 | 2 | 5 | stable | **Corrected from `undefined`.** Anyone may place a warning sign; staff apply physical cord locks; every tool page carries a report-issue button. Remote lockout is designed but **blocked on tool access control being fixed** ◷ 2026-08-14 ⧉ S033 |
| Routine shop inspection walk-through | 2 | 2 | 4 | stable | **Corrected from `undefined`.** The Safety & Accessibility committee walks the shop once a year for general safety ◷ 2026-08-14 ⧉ S036 |
| Hazardous & material waste disposal | 2 | 3 | 4 | stable | **Corrected from `degraded` — it is a stated policy, not an oversight.** The membership agreement places responsibility on members to remove what they bring in. Standards S020 still expects an organisation-side procedure for anything generated by our own operations. *(JR, round 2)* ◷ 2026-08-14 ‖ [Membership agreement](https://www.makehaven.org/membership-agreement) ⧉ S020 |
| Equipment satisfaction micro-feedback | 1 | 1 | 2 | idea | Lightweight prompts — a QR code on the machine, a one-click "how was this tool?" after a badge-logged use — feeding the equipment-satisfaction number now collected only by occasional surveys. Three variants sketched in the website TODO; none started. ◊ 2026-08-16 ▦ kpi_member_satisfaction_equipment |

## Access & Safety

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Door access control (building entry) | 4 | 3 | 5 | broken | Works day to day, but **every badge tap depends on Drupal being reachable** — "when the website is down or the internet is out, nothing opens. We have repeatedly hit this failure mode." The local-primary rearchitecture is drafted (2026-04-14) and pre-implementation. Instructors on billing pause were silently refused at the door until 08-14 ⚙ access_request,access_unifi_bridge,unifi_access_sync ⟐ Secure and Collaborative Digital Infrastructure — building next ‖ [Access Control Documentation](https://docs.google.com/document/d/1lDw-kVj9gYE433tGsU--1r5DV75IaIqgF3DDI9JIYyg/edit) ⧉ S023* P1 |
| **Tool access control (interlocks)** | 2 | 2 | 5 | broken | **The most consequential finding in the registry.** The microcontroller locks up after a couple of days and the bug has not been found. **The workaround — trusting members to use only tools they have been signed off on — has been the operating reality for almost two years.** So tool authorisation is currently a social control, not a technical one, and the remote-lockout capability that would take an unsafe tool out of service depends on the same system. *(JR, round 2)* ◷ 2026-08-14 ‖ [Access Control Documentation](https://docs.google.com/document/d/1lDw-kVj9gYE433tGsU--1r5DV75IaIqgF3DDI9JIYyg/edit) · [Hardware repo](https://crice009.github.io/toolauth-hardware/) · [Tool Orientation Checklists](https://drive.google.com/drive/folders/1JN7rJd1z_8lQed-syIrGxgQnkehl7qj2) · [CNC Use Policy](https://docs.google.com/document/d/1ujsuRdkSmYLTDe2e_SV2WYsd_ACVnWDZv27CD99bToU/edit) ⧉ S015 S022 S023 |
| Access-control hardware operations | 4 | 3 | 5 | stable | Home-built ESP32 plus Home Assistant. **Vincent, Corey and Lior** hold the knowledge, and a documentation site is linked from the GitHub repository in the MakeHaven org account — GitHub has been the key recovery tool more than once. UniFi Access is an add-on to this, not a parallel system. *(JR, round 2)* ◷ 2026-08-14 ⚙ access_control_api_logger,access_unifi_bridge ‖ [Access Control Hardware](https://crice009.github.io/toolauth-hardware/) · [System in action (video)](https://www.youtube.com/watch?v=OjUBacrdoow) ⧉ S037 S035 |
| Event visitor passes | 4 | 2 | 2 | stable | QR / PIN for registrants, via the UniFi add-on ⚙ event_access_unifi ⧉ S027 |
| Access request approval | 3 | 2 | 3 | stable | A member asks for access to a tool or area they are not yet cleared for, and staff approve or decline it. ◊ 2026-08-15 ⚙ access_request ⧉ S023 |
| Guest & waiver handling | 3 | 2 | 5 | stable | A guest signs the waiver, it is stored in the system, and they are offered the option to join the email list. JR believes this works. **That is the whole process — there is no follow-up sequence**, which is the likeliest explanation for 2.4% conversion against a 5% goal on 218 waivers a year. *(JR, round 2)* ◷ 2026-08-14 ‖ [Waivers](https://www.makehaven.org/waivers) ⧉ S027 |
| Member T&C re-acceptance gate | 4 | 2 | 4 | watch | **Discovered 2026-08-15 by measuring it — nobody had a row for it.** When the waiver is revised, every member is locked out of the whole site at next login until they re-accept. It runs unattended but tells nobody when it fails, so failure surfaces only as a member complaining to staff. Over five days of live logs **21 of 35 clients that reached the gate never submitted it**, and **615 of 862 active members are still behind the v7 gate**. Three prior fixes all patched the session lock; the lock was never the fault — the accept page gave no instruction on arrival, put the first actionable control ~3 screens down, and made Confirm a silent no-op when any of five required boxes was unticked. Fix shipped live 2026-08-15 (`makerspace_legal_gate`, plus the accept page moved to the scroll-box style): an instruction callout on arrival, a jump link to the boxes, and native validation replaced by an in-page error naming the box still unticked. **Watching**: whether the 187 accounts still behind the gate now clear it, and whether staff stop hearing about it. It still tells nobody when it fails, which is why A stays 4 rather than 5. D scored low deliberately: a README now describes it, but nobody has yet worked from it unaided ⚠ Kate Cebik, 2026-08-15 — members repeatedly stuck and blocked from doing anything ⚙ makerspace_legal_gate ⟐ Website and Onboarding Optimization — refining next |
| Tool issue reporting | 4 | 2 | 3 | stable | Webform to Slack ⧉ S016 S033 |
| Tool status communication | 4 | 2 | 3 | stable | Tells members when a tool goes out of service and when it returns; status changes post to Slack automatically. ◊ 2026-08-15 ⚙ asset_status,slack_asset_status_change ⧉ S033 P8 |
| API endpoint security | 3 | 3 | 5 | broken | Open critical finding (SEC-001): `access_control_api_logger`'s `/api/v0/*` routes are all `_access: 'TRUE'` with no caller auth, exposing the door grant-or-deny decision, member name/UUID/status/photo, and the full badge catalog to anyone on the internet. **Re-verified 2026-08-20:** an anonymous `GET /api/v0/permissions/list` still returns HTTP 200 with the whole catalog. The real fix is blocked on hardware — the ESP32/Home-Assistant readers are live consumers and must send the new auth before we enforce it. **The unblocking task is small and nobody is on it: find the readers' egress IP**, which would let us restrict `/api/v0/*` at the Pantheon edge today with no firmware change. The module logs no caller IP, so it has to come from Pantheon's nginx logs. Full finding and remediation tracks in the security ledger ⚙ access_control_api_logger ‖ [Security audit ledger](https://github.com/makehaven/makehaven-website/blob/master/docs/ops/SECURITY_AUDIT.md) ⧉ P2 S037 |

## Lending, Storage & Store

_Grouped together because the plan treats them as one thing —
Program and Product Line Monitoring:
"evaluate major program areas (store, lending library, membership, courses,
storage, and workspaces) for cost recovery and mission alignment."_

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Borrower onboarding | 4 | 2 | 2 | stable | Role assigned on webform submission ⚙ lending_library_borrower_role ⧉ S062 |
| Loan checkout | 4 | 3 | 3 | stable | Module carries its own docs ⚙ lending_library ⧉ S062 S063 |
| Loan return | 4 | 3 | 3 | stable | Closing out a lending-library loan — the item is checked back in and the member's hold released. ◊ 2026-08-15 ⚙ lending_library ⧉ S064 |
| Overdue late fee | 4 | 2 | 4 | watch | The double-charge fix shipped live 2026-08-14, but the **refunds it was supposed to enable are silently failing**. Two refund attempts on 2026-08-15 (transactions 4851, 4857) were rejected by Stripe: the `rk_live_` restricted key in use lacks `charge_write`, so the site logged an attempt and no money moved. **Resolved by 2026-08-18 and verified against Stripe 2026-08-20: the key was granted `charge_write`, and all three refunds then went through the site's own form** — transaction 4851 ($30.00) and 4857 ($5.00) at 23:07/23:08 UTC on 08-18, plus 4866 ($5.00) at 23:14, each matched by a `succeeded` refund object in Stripe. Nobody is out of pocket, and there has been no refund failure since. **The reason this row is `watch` and not `stable`** is the pattern rather than the incident: this was the **second** scope missing from that key discovered by a production failure — the store tab pilot hit the same key missing `Customers:Write` — and both times a member hit the hole before we did. The key's scopes still want auditing against every Stripe write path in one pass rather than being widened one outage at a time; until that happens, assume a third scope is missing somewhere nobody has exercised yet. Found by the 2026-08-17 weekly pulse. *(A 2026-08-20 re-check first recorded this as still broken by searching watchdog for errors and finding no newer ones; searching for successes instead showed the refunds had gone through three days earlier. Absence of new failures is not evidence of a fix.)* ⚙ lending_library,mh_stripe ⧉ S063 S024 |
| Damage deposit | 3 | 2 | 3 | stable | Taking and releasing a deposit against damage to a borrowed item. Runs, but nothing is written down and no module implements it. ◊ 2026-08-15 ⧉ S063 |
| Battery tracking | 3 | 2 | 2 | stable | Knowing which tool batteries exist, where they are, and whether they still hold a charge. ◊ 2026-08-15 ⧉ S064 |
| Missing / lost item handling | 3 | 1 | 3 | watch | **Guard shipped and verified present on live 2026-08-17.** Reporting an item missing from the issue form is now blocked when it is on loan to someone else, and points staff at the admin Mark Missing flow, which keeps the loan attached instead of silently closing it and orphaning the battery. What remains is the detection side: the `borrowed_or_missing_without_borrower` integrity check conflates "borrowed without a borrower" (a real fault) with "missing without a borrower" (usually expected), and reads as failing because of a stale write-off backlog nobody has triaged — so the one instrument pointed at this process cannot currently tell a fault from housekeeping ⚙ lending_library ⧉ S065 |
| Item repair & retirement | 2 | 2 | 2 | stable | A broken library item is removed from circulation. JR's intent is for lending fees to eventually fund replacement, which they do not today. *(JR, round 2)* ◷ 2026-08-14 ⧉ S064 S065 |
| Librarian role administration | ? | 1 | 2 | optimizable | Granting a new librarian has been open for weeks ⧉ S050 S051 |
| Lending budget review | 3 | 2 | 2 | stable | Periodic check of what the lending library is spending on replacements, additions and losses against what it has. ◊ 2026-08-15 ⧉ S065 |
| Storage assignment | 3 | 2 | 3 | stable | Assigning member storage space and working the waiting list when it is full, under the published storage policy. ◊ 2026-08-15 ‖ [Storage Policy](https://www.makehaven.org/storage) · [Storage ticketing](https://docs.google.com/document/d/1GNGAhenJNU_GsO86tsB6_4jQJ2zuh4FHYYODaGKkMBo/edit) ▦ kpi_storage_occupancy ⧉ S079 S080 |
| Storage billing | 3 | 2 | 4 | changing | **Worse than v4 recorded.** A re-audit against live Stripe on 2026-08-14 found **24 active assignments, roughly $565/month uncollected** — not the 7 and ~$225 previously logged. Seven were never linked and seventeen point at dead, cancelled or expired subscriptions. This is ongoing rather than legacy (two failed this week) and the root cause is that nothing feeds subscription state back: there is no webhook or cron reconciliation and the status field was never created. No member has been over-billed. *(JR, round 2)* ◷ 2026-08-14 **Update 2026-08-15:** the feedback loop now exists — `storage_manager` c185556 shipped live with the two status fields that were never created, a weekly reconciliation against the Stripe API, and a digest to staff. Its first read-only run on live reproduced the audit exactly: **$565.00/mo across 24 assignments**, 175 of 255 healthy, of which 11 are automatically repairable and 13 need a person. **Nothing has been charged yet and that is deliberate** — auto-repair ships off so a human reviews the list before any member's card is touched. A moves 2 → 3: detection is now automatic, collection is not. ⚙ storage_manager ⧉ S041* S024 S082 |
| Store purchase | 3 | 2 | 3 | watch | Member plywood complaint 08-17 confirmed `/store` rendered only classic-PayPal buttons (now behind a PayPal auth wall; sales 168/mo Apr → 28 by mid-Aug) with zero links to the tab/Stripe checkout. Fix shipped live 2026-08-20 (config-only): every buy button on /store, material pages and related-supplies blocks now routes to `/store/checkout-item/{nid}` with a guest-PayPal fallback. **Verified on live 2026-08-20 — the staged config is deployed** (the local-vs-live config diff no longer contains it). **One day of data, too early to call:** in-product transactions ran 43 in July and 57 so far in August, and the day after the deploy carried 6 against a recent daily median of 2. Re-measure the PayPal-vs-Stripe split and tab uptake in the week to 2026-08-27 before moving this to `stable`. ◷ 2026-08-17 ⧉ S041 S001* |
| Store member tab collection | 4 | 3 | 3 | watch | Pilot live 08-03; live key lacks a write scope so default-promotion no-ops ⚙ makerspace_material_store ⧉ S041 |
| Store inventory restock & reorder | 3 | 2 | 2 | stable | Some materials priced at $0.01/unit — any unit cap becomes a silent spend limit ⧉ S041 |
| Line-of-business profitability review | 2 | 2 | 4 | stable | **Corrected from `undefined` — the finance committee has actually done this**, breaking results down by line of business. It is laborious, and work is ongoing to make Xero produce it more directly. *(JR, round 2)* ◷ 2026-08-14 ⟐ Program and Product Line Monitoring — refining next ⧉ S043 S061 |

## Membership & Billing

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Join / signup flow | 3 | 3 | 4 | changing | UX overhaul staged across four repos, deploy pending ⟐ Website and Onboarding Optimization — refining next ‖ [New Member procedure](https://docs.google.com/document/d/1wqWk57i_w1WSEKry2u6wqH0543BVp7ADuqR1mVXbTwI/edit) · [Membership Agreement](https://docs.google.com/document/d/1SAmCthMaj_2ZGspNhtc-a9yC5STRHbmXJHujEiKD6Rk/edit) ▦ kpi_total_new_member_signups ⧉ S021 S024 |
| Email validation at signup | 4 | 2 | 3 | watch | **Fixed and live 2026-08-18** (`makerspace_email_guard`). Scope had been recorded as unmeasured; it was not small. Across the CRM's 1,393 distinct email domains, **114 resolve to nothing at all** (no MX, no A, no AAAA), covering **173 contacts, 62 with no Drupal account** — people who got a contact record, have heard nothing from us since, and read as no-shows rather than broken signups — plus **120 Drupal accounts** on a dead domain. Dead domains are now blocked at the register form, every webform, and **CiviCRM's own event registration**, which is where most of these actually came from and which no Drupal form alter can see. Live typosquats (`gamil.com`, `oulook.com`) are only *suggested*, never blocked, because `gmx.com`, `aim.com` and `qq.com` are real domains members use and sit just as close to a big provider. Fails open if DNS is unreachable, so an outage cannot stop signups. **Watching two things:** that nobody reports a legitimate address being refused (the tell is a "skipped the deliverability check" warning in watchdog — none at deploy), and that the weekly cron re-scan keeps the report honest. A4 not A5: it runs unattended and logs, but nothing tells a human unprompted. The backward-looking cleanup of the 62 is a separate open task and needs a person, not code. **Watch check 2026-08-20 (two days in, holding but too early to close):** across the 12 days watchdog retains, the module has logged exactly one line — the weekly re-scan notice on 2026-08-18 — and **zero "skipped the deliverability check" warnings**, which is the stated tell for over-blocking. The re-scan has only fired once, so its cadence is asserted rather than demonstrated; re-check after the next two Mondays before moving this to `stable` ⚙ makerspace_email_guard ⧉ S021 |
| Payment setup | 4 | 2 | 4 | stable | Chargebee portal ⚙ chargebee_portal ⧉ S024 S041 |
| Membership status sync | 4 | 2 | 4 | broken | **Corrected from `stable` on 2026-08-20 by measuring it.** The webhook matches a member by `field_user_chargebee_id` and *drops* the plan write when no account carries that ID yet — no queue, no retry. In one 12-day log window **14 of 16** "No user found for Chargebee ID" warnings resolved to accounts that exist now, most created the same day. The miss is permanent because only `subscription_created`/`_updated`/`_reactivated` write the plan; renewals and payments do not, so a member who simply renews is never repaired. It surfaced as members reading **"Unassigned"** on the membership snapshot: **9 active members, 8 of them genuinely paying**, about **$340/month** absent from MRR because the finance queries treat "no plan row" as "not a Chargebee member". **The 8 were repaired by hand on live 2026-08-20** (2 were not linked to Chargebee at all and had their customer ID set; one owned two customer records and was linked to the live one), taking Unassigned 9 → 2. Stays `broken` because the *mechanism* is unchanged on live: the fix — a daily `PlanReconciler` cron sweep that re-derives from Chargebee, plus `chargebee:reconcile-plans` — is **staged, deploy pending** (`chargebee_fetch_data` 528e9a5, confirmed still on neither test nor live as of 2026-08-20). Move to `watch` after it deploys and confirm the sweep reports 0 repaired. The two members still Unassigned have no Chargebee record at all and need a person, not code ⚙ chargebee_status_sync,chargebee_fetch_data ⧉ S023 S024 |
| Dunning / payment recovery | 3 | 3 | 4 | changing | Chasing failed and lapsed membership payments before they turn into cancellations. A first phase went live in April 2026. **2026-08-20: staff review (Kate/Christina) found the Intervention Performance page untrustworthy, and they were right** — the outreach log auto-records wins (member pays → back-attributed `payment_updated` row) but never losses: a member whose subscription cancels mid-recovery drops out of the snapshots with no row, so Confirmed Cancel read 0 for everyone since 2026-04-20 (28 real departures unrecorded; 17 had Christina's outreach within 30 days). Fix staged (`makerspace_member_success` 79c45cf): departures now auto-log a back-attributed `confirmed_cancel`, an `ms:backfill-cancellations` command repairs the gap, the resolution-rate card gained a names drill-down, and the Full Contact Log export now actually exports the log. Move to `watch` after deploy + backfill; verify Kate/Christina accept the corrected numbers ◊ 2026-08-20 ▦ kpi_payment_resolution_rate,kpi_monthly_revenue_at_risk ⚙ makerspace_member_success ⧉ S024 |
| Cancellation & offboarding | 4 | 2 | 3 | stable | **Corrected from `unknown` — this is one of the better-automated flows we have.** Member cancels in Chargebee; the sync module removes the member role, which removes door access; the cancellation reason is captured and synced to Drupal/CiviCRM. A failed payment routes to dunning and then the member-success queue instead ◷ 2026-08-14 ‖ [Member success dashboard (staff)](https://www.makehaven.org/admin/makerspace/member-success/dashboard) ⧉ S023 S024 |
| Member conduct & discipline | 2 | 3 | 5 | stable | **Corrected from `degraded`.** The executive director decides, following a written guide. The member may appeal to the board chair, who either lets the decision stand or takes it to the board to consider overruling. Low volume, clear escalation path; the weak point is that records live in a spreadsheet rather than the CRM. *(JR, round 2)* ◷ 2026-08-14 ‖ [Member warning](https://docs.google.com/document/d/18BfXtbSVDhe6hm5WxYurEMN5S_KBA_cIf0hlt0YeD_M/edit) · [Member termination](https://docs.google.com/document/d/1LFao9lQ1r8iDtby6iT54-LqLoo6TQnGaMv75__3KNCs/edit) · [Discipline guide](https://docs.google.com/spreadsheets/d/1Hs65Eg6k71zvtbIcsAXfEE36wz-Eujy5pSyeX563NeI/edit) ⧉ S025 |
| Exit survey & ending-reason capture | 4 | 2 | 4 | stable | **Corrected from `degraded`.** Reason is captured at cancellation in Chargebee and flows through to the profile, so it is automatic rather than a survey anyone has to chase ◷ 2026-08-14 ⧉ S057 |
| Rejoin / recapture campaign | 2 | 1 | 3 | stable | Runs: a contractor does outreach and rejoin buttons exist in the product. What has not happened recently is any larger marketing push to lapsed members. *(JR, round 2)* ◷ 2026-08-14 ⟐ Priority · Rejoin and Recapture Pathways — planning next |
| Comped / sliding-scale / sponsored memberships | 4 | 2 | 3 | stable | **Corrected from `unknown`.** Applicants self-certify on the join form with an online signature — no approval queue by design. **The intake is automated; the policy behind it is not written down.** There is an application form and a pricing policy, but nothing states who qualifies, what the sliding scale actually is, or how a scholarship differs from a comp — so the decision rests on whoever is asked. JR, 2026-08-15: no documented process exists for this ◷ 2026-08-14 ⟐ Sliding Scale Scholarships and Financial Flexibility — refining next ‖ [Scholarship application](https://www.makehaven.org/makehaven-scholarship-application) · [Pricing Policy](https://docs.google.com/document/d/10mGYDuvO_J4AAgWRHIXb3WEO1dU2OQKCnxm2w_0JYpk/edit) ⧉ P4 S024 S055 |
| Stripe customer linkage | 2 | 2 | 3 | optimizable | 656 unlinked; field only written by manual backfills ⚙ mh_stripe ⧉ S041 |
| Membership pricing review | 2 | 3 | 4 | stable | **Corrected from `unknown`.** Board policy sets an annual inflation-linked default; the executive director holds the authority to apply it ◷ 2026-08-14 ⟐ Sustainable and Equitable Membership Revenue — scaling next ‖ [Pricing Policy](https://docs.google.com/document/d/10mGYDuvO_J4AAgWRHIXb3WEO1dU2OQKCnxm2w_0JYpk/edit) ⧉ S024 S043 |
| Workspace rental agreement | 4 | 3 | 3 | watch | Signing flow live 07-29; retire gate live 08-12 ⚙ workspace_rental ‖ [Workspace Use Agreement (link broken in source)](https://docs.google.com/document/d/1AShT2j-Cc24Q0cxVqJLD8OxZ9V9erV2kCCfyYk49K0c/edit) · [Workspaces](https://www.makehaven.org/workspaces) ⧉ S079 S082 |
| Workspace rental billing | 2 | 2 | 3 | stable | **Corrected from `undefined`, and verified: 14 of 15 workspaces now carry a price** — Kate filled them. Many tenants are paying, invoiced through Xero today, with migration to the in-product system intended later. *(JR, round 2)* ◷ 2026-08-14 ⚙ workspace_rental ‖ [Workspaces](https://www.makehaven.org/workspaces) ⧉ S041 S079 |
| Denied-entry rejoin follow-up | 1 | 1 | 2 | idea | When the door denies someone with no active membership, nothing follows; the sketch is an automatic email/SMS explaining why, with a mobile rejoin link and quiet-hour rules. Would give the rejoin campaign a trigger instead of a list. ◊ 2026-08-16 |

## Member Experience & Retention

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Onboarding nudge / stalled-join recovery | 4 | 3 | 3 | watch | Live 08-11, profile-step only. Efficacy unproven — before widening, 0 of 5 nudged progressed. **08-17: widening to the full funnel (video/quiz/schedule) staged, deploy pending** — triggered by Glenn Bair stalling at the video step with no automated email; watch post-deploy whether video-stuck members progress ⟐ Priority · Structured Onboarding and Early Engagement — refining next |
| Orientation scheduling | 3 | 2 | 3 | stable | Calendly. A webhook outage lost Apr–Jun records; orientations never backfilled ‖ [Orientation video / process](https://www.makehaven.org/orientation-video) ⧉ S021 |
| First-badge-in-28-days promotion | 3 | 2 | 4 | optimizable | **Measured but not managed** — JR: "now just measured and we work against it." 67% against an 80% goal. Current experiment: sending a free GEMS course to members who appear stuck. *(JR, round 2)* ◷ 2026-08-14 ⚠ Staff, 2026-08-14 — part of the badge-earning flow, which staff see as a major driver of retention and a strong candidate for review soon ▦ kpi_new_member_first_badge_28_days |
| Interest capture + Slack invite | 4 | 2 | 2 | watch | Captures someone who registers interest in joining and invites them into Slack automatically. Live since August 2026 and still being watched. ◊ 2026-08-15 |
| Member success outreach queue | 3 | 3 | 3 | changing | A worklist of members for staff to reach out to — newly joined, gone quiet, or at risk of leaving. **08-17: Kate proved the recovery side was hiding its targets (4 named members, 7 total); episode-reset policy (new payment failure re-opens files, Kate-confirmed) + Chargebee write-off flag clearing + cron CiviCRM backfill (Christina-work visibility) + template 166/167 repair all STAGED, deploy pending** ◊ 2026-08-15 ⚙ makerspace_member_success |
| At-risk early-warning detection | 4 | 3 | 4 | stable | Year 1 list marks this "(done, improve?)" — the one strategy already built ⟐ Priority · Early Engagement Monitoring — building next ▦ kpi_members_at_risk_share |
| Retention intervention tracking | 3 | 2 | 3 | stable | A contractor works the at-risk queue using member-success module data. Whether interventions actually change outcomes is charted but not, as far as we can tell, acted on. *(JR, round 2)* ◷ 2026-08-14 ⟐ Data-Driven Retention Tracking — building next |
| New-member 3-month survey | 1 | 1 | 3 | planned | Asking members three months in how joining has actually gone, while it is recent enough to act on. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⧉ S057 |
| New-member gatherings & peer intros | 2 | 2 | 2 | stable | **Split result.** Social events and meetups genuinely happen and are frequent. The **mentorship programme fell apart and is dormant** — that half is the gap, not the social half ⟐ New Member Gatherings and Peer Introductions — building next ⧉ S030 S056 |
| Interest-based member groups | 1 | 1 | 2 | stable | Runs loosely through Slack channels and meetups rather than as a supported programme with stipends. *(JR, round 2)* ◷ 2026-08-14 ⚙ interests_civi_bridge ⟐ Interest-Based Groups — scaling next ⧉ S056 |
| Member recognition & awards | 1 | 1 | 2 | changing | In the works, and has been for a long time — the awards concept keeps being picked up and put down. *(JR, round 2)* ◷ 2026-08-14 ⟐ Community Events and Member Recognition — scaling next ⧉ S053 |
| NPS & satisfaction survey | 2 | 2 | 3 | stable | Member surveys carrying NPS have run for years. JR wants the process integrated into the site and automatic rather than periodic and manual — and flags it as something to check back in on ‖ [2023 Member Survey](https://docs.google.com/document/d/1BHuenfGNNegj1PIDFYOxBacPq6gGpOcBUcKeG2t_Lvw/edit) ▦ kpi_member_nps ⧉ S057 |
| Community Wishlist | 4 | 2 | 2 | stable | **Corrected from `undefined` — it exists and runs.** Members submit and vote; it also feeds the tool-acquisition process as the step after budget ◷ 2026-08-14 ⟐ Transparency Feedback and Dashboards — building next ‖ [Wishes](https://www.makehaven.org/wishes) ⧉ S057 S039 |
| Deferred profile field capture | 3 | 2 | 2 | watch | **Re-measured 2026-08-17 and it was three things, not one — and the biggest was not a capture problem at all.** Discovery recovered once it moved to the thank-you interest picker (8 of 15 recent profiles, against 0 of the preceding 10). Bio has a capture moment now too (the Slack intro banner) but has still produced nothing. **The third part was a lock:** emergency contact name, emergency contact phone and preferred phone were all `required` on `profile.main`, so **115 of 858 active members (13.4%) could not save *any* profile edit** — not a bio, not a headshot — until they supplied an emergency contact nobody had ever asked them for. That is what dead-ended every "you can fill this in later" path, and it was routinely misreported as "the bio field is required" (bio is not required). **Fixed live 2026-08-18**: the requirement now applies on the join path only, so new members are still asked while established members get a prompt and a one-purpose form at `/membership/emergency-contact` instead of a wall. **Watching the number**: 115 at deploy — if it does not fall, the passive banner is not enough and the answer is an email, not another form tweak. That is the same lesson the discovery fix taught: a deferred field needs an *active* capture moment or it is not collected ⚙ profile_membership,interests_civi_bridge,slack_member_sync ⧉ S054 |
| Member file bucket | 4 | 2 | 1 | stable | **Added 2026-08-18 by the module sweep.** A deliberately short-lived file drop at `/bucket` for moving files between a member's own device and a shop computer: members upload, the list is public, downloading streams the file and marks it used, and cron deletes it — a 48-hour TTL and immediate deletion after first download, 50 MB cap, dangerous extensions blocked. The public listing is intentional and disclosed on the page itself ("Anyone on the internet can see the files uploaded here"), which is also the only documentation this process has — for a service this small, nothing separate is worth keeping current ⚙ bucket |
| Member feedback triage | 3 | 3 | 3 | stable | A well-documented A3 — worth copying as a pattern ⟐ Centralized Feedback and Engagement System — refining next ⧉ S057 S061 |
| Quarterly close-the-loop reporting | 1 | 1 | 3 | planned | Telling members each quarter what changed because of the feedback they gave. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Culture of Listening and Recognition — scaling next ⧉ S061 S060 |
| Year in review | 4 | 2 | 1 | stable | A personal end-of-year summary for each member — what they made, learned and attended. ◊ 2026-08-15 ⚙ makerspace_member_year_review ⧉ S060 |

## Outreach & Recruitment

_The conversion funnel: getting people who are not yet members in the door and
across the line — tours, waivers, follow-ups, campaigns. The line against
Communications is the audience: if it exists to convert outsiders, it is here;
if it is a standing channel talking to people we already have, it is
Communications. v1 folded the two together and lost the whole funnel, which is
why they are deliberately separate._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Tour booking & delivery | 3 | 2 | 4 | stable | **Corrected from `unknown`.** All staff sit on a published tour schedule. JR is considering moving tours to a volunteer corps, which would change both the capacity and the training need ◷ 2026-08-14 ‖ [Tour booking](https://www.makehaven.org/tour) ▦ kpi_tours ⧉ S027 |
| Tour follow-up & conversion | 2 | 2 | 4 | optimizable | Conversion-Focused Marketing and Follow-Ups wants automated personalised follow-up. Currently manual or absent ▦ kpi_tours_to_member_conversion |
| Guest waiver → member conversion | 1 | 1 | 3 | optimizable | **2.4% against a 5% goal** on 218 waivers. No defined follow-up at all ▦ kpi_guest_waiver_to_member_conversion ⧉ S027 |
| Workshop participant → member conversion | 2 | 1 | 4 | optimizable | JR: it *should* send an email and re-invite attendees, but that needs verifying and is undeveloped either way. 6.4% conversion against a 10% goal, and the strategic plan carries its own note that this is not properly measured. *(JR, round 2)* ◷ 2026-08-14 ⟐ Conversion-Focused Marketing and Follow-Ups — planning next ▦ kpi_event_participant_to_member_conversion |
| Discovery source capture | 3 | 2 | 2 | stable | "How you heard" is collected and discussed in the outreach and marketing committee. Self-reported, so treated as directional rather than reliable. *(JR, round 2)* ◷ 2026-08-14 ⧉ S054 |
| Referral / bring-a-friend | 2 | 2 | 3 | optimizable | **Corrected from `unknown` — it runs, but by hand.** Members do refer; JR names it explicitly as an area for technical process improvement ◷ 2026-08-14 ⟐ Member Referral and Ambassador Programs — scaling next ‖ [Referral program](https://www.makehaven.org/member-referral-program) |
| Ambassador program | 1 | 1 | 3 | planned | A named group of members who bring people in and welcome them once they arrive, with some recognition for doing it. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Member Referral and Ambassador Programs — scaling next ⧉ S050 |
| Community tabling & partner events | 2 | 1 | 2 | stable | Staffing a MakeHaven table at community and partner events to reach people who have not heard of us. It runs, but how it is planned and staffed is not written down anywhere. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Community Tabling and Partner Events — scaling next ⧉ S059 |
| Community partnership development | 2 | 1 | 3 | stable | Confirmed running, though without a defined pipeline or count. *(JR, round 2)* ◷ 2026-08-14 ⟐ Partner Outreach and Sponsored Access Programs — planning next ⧉ S059 |
| Media relations & press kit | 1 | 1 | 2 | planned | A maintained press kit and a habit of pitching stories, so coverage is sought rather than waited for. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Earned Media and Public Relations — planning next |
| Neighborhood & postcard campaigns | 2 | 2 | 2 | stable | Run as experiments rather than on a schedule — planned ad hoc rather than triggered. *(JR, round 2)* ◷ 2026-08-14 ⟐ Priority · Neighborhood Apartment and Regional Outreach — planning next |
| Paid digital advertising & retargeting | 1 | 3 | 3 | changing | 250 hrs budgeted. Ad Grant campaign launch-ready, blocked on account access ⟐ Paid Digital Advertising and Retargeting — planning next |
| Lead / inquiry handling | 2 | 2 | 3 | optimizable | **Corrected from `unknown` to a named weak point.** `info@` lands in a shared Google inbox answered mostly by Kate, and staff struggle to keep up with the volume ◷ 2026-08-14 ⧉ P8 |
| Member phonebank campaigns | 3 | 2 | 3 | stable | **Corrected from `unknown`.** Used once for a fundraising experiment, well received, and planned for the next phonathon. Occasional-use by design rather than neglected ◷ 2026-08-14 |

## Communications

_The standing channels — newsletter, digest, Slack, the site, the phone — and
the hygiene that keeps them working. These speak to everyone we already have;
anything built to convert outsiders lives in Outreach & Recruitment. The two
overlap at the newsletter and social media, which serve both audiences: those
sit here because the channel outlives any one campaign._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Weekly digest | 5 | 3 | 3 | watch | **The W34 send stalled and nothing caught it.** On 2026-08-19 a 892-recipient batch sat for 4h45m with zero delivered, blocking every other CiviMail behind it. It left no error to find: PHP's `max_execution_time` *killed* the send rather than it throwing, so every error-log-based monitor we had was structurally blind to it. Resolved by raising `mailerBatchLimit` 0 → 100 so the batch fits inside the execution ceiling — a CiviCRM setting, not Drupal config, so it does **not** travel with `drush cim` and must be set on any environment that will send at scale. Alerting shipped live 2026-08-20 (`makerspace_digest_scheduler` 7ad888c): two checks on every cron tick — a running job whose delivered count stops moving, and a schedule whose window passed with no mailing created at all, the failure that leaves no row and no job to find. Alerts reach Slack, `staff@makehaven.org` and watchdog. The same release fixed an ordering bug that had recorded no run-state for W31–W34, so status had been reading a month stale. **A moves 4 → 5**: failure now reaches a human who was not looking for it. **Watching**: the 2026-08-26 send, and whether the missed-send check stays quiet on live rather than crying wolf ⚙ makerspace_digest_scheduler ⧉ P8 |
| Monthly newsletter | 2 | 2 | 3 | changing | Mailchimp retirement in flight ⧉ P8 |
| Mailing list / smart group hygiene | 3 | 2 | 3 | watch | **Verified against live 2026-08-17: the three repairs are holding.** All the mailing feeders are smart, all rebuilt their caches within the hour, and every audience has grown since the 2026-08-06 fix (Monthly 7,373 → 7,484, Weekly 876 → 946). The reason this kept recurring was never the groups themselves but that **nothing was watching** — each freeze was found by hand, months late. Two checks were added to `scripts/workflow-health.sh` on 2026-08-17 to close that: one for a smart group whose cache stops rebuilding, one for a group fed by an automated write path that has gone quiet. The second immediately named a real outstanding case the audit had left behind — the Guest Waiver webform's group-add has been dead for 145 days, harmless only because that audience is now activity-driven. Leaves `watch` when a freeze is caught by the check rather than by a person ⧉ P8 |
| Slack announcements | 4 | 2 | 2 | stable | Tasks, events, asset status ⧉ P8 |
| Slack membership lifecycle sync | 4 | 2 | 3 | broken | **Added 2026-08-18 by the module sweep, and it is failing.** The module matches members to Slack by email, stores the Slack user id on the profile, emails a workspace invite to members not yet in Slack, retries on cron until they join or hit the attempt cap, syncs interest channels (#woodshop, #electronics) from stated interests, and — the part that is broken — adds people to the members broadcast channel when the member role is granted and **removes them when it is revoked**. **Every removal attempt in the retained window has failed: 24 `restricted_action` rejections from Slack, the most recent 2026-08-21 01:24 UTC** — it is failing daily, not historically. Slack returns `restricted_action` on `conversations.kick` for one of two reasons, and we have not yet established which: a workspace preference limiting who may remove people from public channels, or the target channel being #general, which no bot can ever kick from. **Identify channel `C0AUFPLUR5G` first** — the answer decides whether this is a settings change or a redesign. Two more failed as `invalid_arguments` — a Slack *handle* stored on the profile where a `U…` user id is required. Joining works, leaving does not, so people keep member-channel access after their membership ends ⚙ slack_member_sync ⧉ S024 |
| Website content publishing | 2 | 1 | 2 | stable | Any staff member can publish; there is no editorial calendar. JR wants to step up blog and announcement output, which would also feed the developing automatic newsletter |
| SEO & analytics instrumentation | 4 | 3 | 2 | watch | Live 08-09. Tag wiring is implicit and fragile |
| Inbound phone & voicemail triage | 1 | 1 | 3 | changing | **Moved from `optimizable` — work is landing, not merely wished for.** JR: "this is a weak point." Calls go to a Google voicemail box that often sits unanswered for a long time because of staff capacity. The voice AI routing track shipped its Phase 1 foundation live on 08-07, inert behind config; the Voicemail-Tool is written and pre-launch, awaiting a Twilio number ◷ 2026-08-14 ⚙ makerspace_voice ⧉ P8 |
| Impact storytelling & member spotlights | 1 | 1 | 2 | planned | Publishing member stories on a regular cadence to show what the space makes possible. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⧉ S060 |
| Annual report & impact reporting | 2 | 2 | 3 | stable | **Corrected from `undefined`.** The annual member meeting is presented and recorded, and a PDF of that deck serves as the annual report when one is requested. Standards S060 wants finances, participation, outcomes *and setbacks* — worth checking the deck against that ◷ 2026-08-14 ⧉ S060 S042 |

## Finance & Accounting

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Contractor payment → Xero bill | 4 | 2 | 4 | watch | Duplicate-bill fix pushed, deploy pending; no real double-pays occurred. Covers member reimbursements as well as contractor hours. Two more fixes staged 2026-08-15 off a member complaint: the "My Payment Requests" list showed neither the amount nor the hours, so you could see you had filed something but not what you were owed; and the request title — which `SyncManager` sends to Xero as the **bill line description** — was being blanked by every background save, because the label pattern rendered access-controlled fields as the anonymous account cron runs as. 290 of 307 requests had lost theirs, and those bills are already in Xero carrying the damage. **Both shipped live 2026-08-15** (`xero_bills_sync` ac54dcb): the member list now carries For / Hours / Amount, the label pattern moved to property tokens so background saves stop rewriting titles, and `update_9005` rebuilt all 311 titles on test and live. Verified as a real member, not as an admin — field permissions make those two views differ. **Watching**: that titles survive the next 1st/15th consolidation run, since cron is what erased them before. **Staged 2026-08-18** (`a1748d7`): the free-text "Pay to (Xero contact)" box no longer sits in the middle of every request form for staff — it moves into the collapsed Advanced group and only comes back out when the payee has a business contact recorded. That review found the LLC billing path had been **entirely dormant** since it shipped — no account had a business Xero contact set — and JR recorded the first one the same day (Aaron Monikowski → Glow Worm Ideas, live). Two things surfaced from switching it on: his form save silently failed to land (written via drush instead; cause unidentified, worth chasing if it recurs), and the choice label rendered the raw Xero ContactID, which a second fix resolves to the business name ⚙ xero_bills_sync ⧉ S041 S046* |
| Vendor payment via Melio | 2 | 2 | 4 | optimizable | **Corrected from `broken` — JR, 2026-08-15: "actually working pretty good… we have fixed most issues."** It is not failing, so `broken` was the wrong word; what is left is an end state someone can name and has not been reached, which is what `optimizable` is for. **There is still no periodic sweep** — detection depends on someone happening to check, which is how two payments once sat undelivered. The failure is visible in Xero if someone looks, and responsibility sits with the staff member who initiated the payment to their own contractor, per the procurement policy's budget-line ownership. *(JR, round 2)* ◷ 2026-08-15 ‖ [Procurement policy](https://www.makehaven.org/makehaven-procurement-policy) ⧉ S041 |
| Stripe → Xero reconciliation | 3 | 3 | 4 | stable | **Corrected from `degraded`.** Statements import into Xero, the bookkeeper matches receipts, and unresolved items are worked through in a standing session with the executive director. The known friction is unlabelled PaymentIntents, where the bank feed shows only a charge description and the income line has to be inferred. *(JR, round 2)* ◷ 2026-08-14 ⧉ S041 |
| Monthly financial close | 2 | 3 | 4 | stable | **Corrected from `unknown`.** A contractor does data entry, the executive director handles the harder work, finance committee volunteers assist, and a CPA reviews and prepares the 990 ◷ 2026-08-14 ⟐ Modern and Efficient Financial Infrastructure — refining next ⧉ S040 S041 |
| Budget vs actual review | 2 | 3 | 4 | stable | **Corrected from `unknown`.** The board approves an annual budget and receives regular budget-versus-actual reporting ◷ 2026-08-14 ⧉ S040 |
| Reserve fund management | 2 | 3 | 5 | stable | **Corrected from `unknown`.** Governed by published financial and procurement policies, managed by the executive director. Reserve stands at 2.93 months against a 6-month goal ◷ 2026-08-14 ⟐ Priority · Reserve Development and Investment Strategy — building next ‖ [Financial policies](https://www.makehaven.org/makehaven-financial-policies-and-procedures) · [Procurement policy](https://www.makehaven.org/makehaven-procurement-policy) ⧉ S045 S039 |
| Annual external review / audit | 2 | 3 | 4 | stable | **Corrected from `unknown`.** Completed last year; this year's documents are already with the reviewer ◷ 2026-08-14 ⟐ Policies Review and Audit Cycle — building next ‖ [Filing requirements & procedures](https://docs.google.com/document/d/1utOZLoGWzUXXe0hS3D7jt1YPEMKZ93yD1ztQedEaF0k/edit) ⧉ S044 |
| Financial policy maintenance | 2 | 3 | 3 | stable | **Corrected from `undefined`** — both policies are published and current ◷ 2026-08-14 ⟐ Policies Review and Audit Cycle — building next ‖ [Financial policies](https://www.makehaven.org/makehaven-financial-policies-and-procedures) · [Procurement policy](https://www.makehaven.org/makehaven-procurement-policy) ⧉ S041 P9 |
| Financial dashboards & board briefings | 2 | 2 | 3 | stable | The executive director prepares the board packet from Xero, working documents and the KPI dashboard ⟐ Financial Dashboards and Transparency Tools — building next ⧉ S040 S043 |
| Donation processing | 3 | 2 | 3 | stable | **Corrected from `unknown`.** The acknowledgement procedure is followed. Some manual steps are deliberate — handwritten notes on cards — and JR sees room to automate acknowledgements for smaller donations while keeping the personal touch for larger ones. *(JR, round 2)* ◷ 2026-08-14 ‖ [Donation Acknowledgement Procedure](https://docs.google.com/document/d/1Xd3CkHtjPSUSQdXktw2MZ3chxBd8uEiyPMwyFzphnMc/edit) ⧉ S042 |

## Development & Fundraising

_New group in v2. Has a committee, a dashboard, and five strategic objectives;
had zero rows in v1._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Annual appeals (spring + year-end) | 2 | 2 | 4 | stable | **Corrected from `unknown`.** Run by the Resource Development committee with Kate as staff lead ◷ 2026-08-14 ⟐ Two Annual Appeals — maintaining ‖ [Fundraising Plan](https://docs.google.com/document/d/1ehYHyPDqcll_xW0tpcqhJt237GxUi7VjD3-Gvqd5BBo/edit) ⧉ S042 |
| Recurring giving program | 2 | 2 | 3 | stable | Owned by Kate with the resource development committee; 39 recurring donors against a 60 goal. *(JR, round 2)* ◷ 2026-08-14 ⟐ Recurring Giving Program — refining next ▦ kpi_recurring_donors_count ⧉ S042 |
| Major donor LAI qualification & pipeline | 3 | 2 | 4 | changing | Sponsorship-Tool implements LAI scoring and a pipeline board; 3 tasks from done ⟐ Priority · LAI Qualification and Pipeline — scaling next ‖ [LAI Scoring Sheet](https://docs.google.com/document/d/1pn_sc4nKokRn0hxEPdSOVGvQuD3bHXWsQzCSihxSs5A/edit) ⧉ S042 P2 |
| Major donor stewardship cadence | 2 | 2 | 4 | stable | **Corrected from `undefined`.** Staff steward major donors and the board is sometimes involved. JR: the system could be built out — cadence is not yet systematic ◷ 2026-08-14 ⟐ Stewardship Cadence — planning next ▦ kpi_donor_retention_rate ⧉ S042 |
| Corporate sponsorship solicitation & renewal | 2 | 3 | 4 | watch | Tier ladder + benefit matrix live 08-09; round 3 staged. $7,916 against a $25,000 goal ⟐ Priority · Sponsorship Plan Materials and Recognition — building next ‖ [Sponsorship Levels](https://docs.google.com/document/d/1M2m3-Yj7wuhvFAC5yPaY79NjOV_O-_IdYyfkJhtaX9E/edit) · [Example Sponsor Letter](https://docs.google.com/document/d/1H3U11lrA-jERoDLlV6aJ70zt2IgZQjyE0dhrBWlsZ6A/edit) ▦ kpi_annual_corporate_sponsorships ⧉ S042 |
| Sponsor recognition & benefit fulfilment | 2 | 2 | 3 | stable | Kate leads, shared with the executive director for sponsor relationships. *(JR, round 2)* ◷ 2026-08-14 ⟐ Sponsorship Program Leadership — building next ⧉ S042 |
| Grant pipeline & deadline tracking | 3 | 2 | 4 | stable | **Major correction, now verified against the database. JR was right and the KPI is wrong.** `civicrm_value_funding_7` holds 46 records; **6 have 2026 due dates and 5 of those 6 carry a submitted link**. So roughly five grants were submitted this year, not zero. The win ratio KPI is fine (12 won of 34 decided = 35%, reported 32%), so this is one broken metric, not a broken dashboard. **The pipeline has no `submitted` status at all** — it runs researching → waiting → won/lost/abandoned — so "submitted" is inferred from a link field and the period is keyed off the due date. That inference is what fails ⟐ Priority · Integrated CRM and Calendar Tracking — scaling next ▦ kpi_grant_pipeline_count ⧉ S042 S001 |
| Grant outcome recording | 3 | 2 | 3 | stable | Recorded in CiviCRM by Kate and the executive director; win ratio 12 of 34 decided. *(JR, round 2)* ◷ 2026-08-14 ▦ kpi_grant_win_ratio ⧉ S042 |
| Donor data hygiene in CRM | 2 | 2 | 3 | stable | **Kate owns donor data quality** and does most of the checking, shared with the executive director for major donors and sponsors. *(JR, round 2)* ◷ 2026-08-14 ⟐ CRM and Pipeline Management — building next ⧉ P2 |
| Case statement maintenance | 1 | 1 | 2 | planned | Keeping a current case for support — why a funder should give — instead of writing one under deadline for each ask. Nothing built. Confirmed by JR as an intention we have not started — a roadmap item, not a broken process. *(JR, round 2)* ◊ 2026-08-15 ◷ 2026-08-14 ⟐ Rotating Case Statements — planning next ⧉ S007 |
| Planned giving / bequest program | 1 | 1 | 2 | optimizable | A page exists but there is no cultivation activity behind it — present in form, dormant in practice. *(JR, round 2)* ◷ 2026-08-14 ⟐ Planned Giving Quiet Build — planning next ⧉ S042 P6 |

## Governance & People

_6 rows in v1, 17 here. This is where the strategic plan added the most, and
where almost nothing is defined._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Board recruitment matrix & sourcing | 2 | 2 | 4 | stable | **Corrected from `undefined`.** A webform is sent to candidates to collect skills and demographic information, which feeds the matrix used to build the slate. *(JR, round 2)* ◷ 2026-08-14 ⟐ Strategic Board Recruitment — maintaining ‖ [Board Skill & Demographic Matrix](https://docs.google.com/document/d/1PEZszopG0dXW9gUtas5myG1Ps_sRzhTtKC8LScWg4Do/edit) · [Board roster](https://www.makehaven.org/team) ▦ kpi_board_ethnic_diversity,kpi_board_gender_diversity ⧉ S003 |
| Board nomination & election | 2 | 2 | 4 | stable | **Corrected from `unknown`.** The governance committee discusses; nominations arrive through a website form; candidates are assessed against the skills matrix; the committee talks with the strongest, assembles a slate, and the board passes it. *(JR, round 2)* ◷ 2026-08-14 ⟐ Inclusive Nomination and Onboarding — maintaining ⧉ S002 S003 |
| Board onboarding | 2 | 2 | 3 | stable | **Corrected from `undefined`.** A new director receives a one-hour orientation presentation with Q&A. *(JR, round 2)* ◷ 2026-08-14 ⟐ Board Governance Development — building next ‖ [Board orientation slides](https://docs.google.com/presentation/d/1S-zx_82MFvUkyZ1Yw-Mjjnu2segRcwHGAr0MgZr9b8I/edit) · [Expectations for Board Members](https://docs.google.com/document/d/1DS9-Av-3Y8HBOX79xtD0s5rw7OVLNOyaAjUY1DGMN90/edit) ⧉ S003* S010 |
| Board self-assessment (annual) | 2 | 2 | 3 | changing | In progress now via a board survey, after a long gap ‖ [Board survey (staff)](https://www.makehaven.org/survey/board) ⧉ S010 |
| Board & committee minutes retention | 2 | 2 | 4 | stable | Board meets quarterly plus committees; approved minutes retained in Google Drive. Candidate for Governance-Dance if that app is adopted ‖ [Board roster](https://www.makehaven.org/team) ⧉ S004 S006 |
| Governance policy annual review | 2 | 3 | 5 | stable | Conflict-of-interest policy published; the policy set is indexed in the operations doc ⟐ Governance Model and Policy Review — refining next ‖ [Conflict of interest](https://www.makehaven.org/conflict-interest-policy) · [Operations index](https://www.makehaven.org/operations) · [Bylaws](https://docs.google.com/document/d/1yhU7K5EpKeP6KRXCDboMOiFOrT6bd5vA5Dcippb694g/edit) · [Whistleblower Policy](https://docs.google.com/document/d/1XF4N91TwuxkHUsOLHZ7QZEn8t755kPxO6qtczERSiyU/edit) ⧉ S006 P9 |
| Committee charters & effectiveness | 2 | 2 | 3 | stable | **Correction: the DEI committee is active and meeting** — v2's "no active members" is stale. Committee structure is published. **Real remaining gap, in JR's words: no reliable way to track who is actually on each committee** — the clearest use case for Governance-Dance ‖ [Committee structure](https://www.makehaven.org/volunteer-leadership-structure) ⧉ S002* S004 |
| Governance archive / institutional memory | 1 | 2 | 3 | planned | Partly served by Google Drive and the operations index today, but nothing purpose-built. JR wants something stronger — possibly Governance-Dance, possibly a dedicated continuity tool. *(JR, round 2)* ◷ 2026-08-14 ⟐ Knowledge Transfer and Governance Archive — building next ⧉ S006 P9 |
| Board officer & director succession | 2 | 3 | 4 | stable | **Split out of the old succession row — and it turns out to be defined, in the bylaws.** Section 2.4 covers director resignation, 2.5 removal, 2.6 vacancies (fillable by the directors at any meeting), and 3.7 officer resignation and removal. Officers serve one-year terms and **"interim vacancies may be filled by the Board of Directors to serve until the next annual meeting"**. Directors serve staggered three-year terms with roughly a third expiring each year, so continuity is structural rather than ad hoc. *(Verified against the bylaws, 2026-08-14)* ⟐ Leadership and Succession Planning — planning next ‖ [Bylaws](https://docs.google.com/document/d/1yhU7K5EpKeP6KRXCDboMOiFOrT6bd5vA5Dcippb694g/edit) ⧉ S002 S009 |
| Executive succession & emergency authority | 1 | 1 | 5 | undefined | **The real gap, now isolated.** The bylaws handle *governance* continuity; nothing handles *operational* continuity. If the executive director were suddenly unavailable there is no documented answer to who signs, who approves payments, who holds the vendor and landlord relationships, or who assumes day-to-day authority — JR: "not really, we should work on this." The partial mitigations are real but incidental: system access is distributed and recoverable through the org email account, and a **MakeHaven System and Data Access Agreement** form has captured 21 submissions since May 2025. Standards S009 asks for succession and emergency authority to be documented **and tested** — we have neither. **This is now the highest-impact undefined process in the registry.** ⟐ Leadership and Succession Planning — planning next ⧉ S009 |
| Staff onboarding / offboarding | 1 | 2 | 3 | stable | **Reframed.** The same four staff have been in post for years, so this rarely fires; when it does, the executive director spends substantial one-to-one time. **JR's own redirect is the useful finding: the real onboarding gap is instructors and volunteers, not staff** — and those are far higher-volume. *(JR, round 2)* ◷ 2026-08-14 ‖ [Personnel Policy](https://docs.google.com/document/d/1G70oyO5qSCDrjqVkLztEoLJyAbQzYs85QZJx_h3Snt0/edit) · [Staff Responsibilities Map](https://docs.google.com/drawings/d/1w8iB6siS0NJh0tNlZ0A3myBtsTayvzGYybzU_qRA8OQ/edit) ⧉ S046 S047 |
| Staff development, benefits & wellbeing | 2 | 3 | 3 | stable | Annual evaluations happen and job descriptions are reviewed at the same time; both live in Google Drive ⟐ Staff Retention Efficiency and Operational Continuity — refining next ‖ [Employee Evaluation](https://docs.google.com/document/d/1hm2Tl-jVQSOHfMhyDOjz4SCHxcOkS-BgGO7vZW4gR50/edit) · [Personnel Policy](https://docs.google.com/document/d/1G70oyO5qSCDrjqVkLztEoLJyAbQzYs85QZJx_h3Snt0/edit) ⧉ S048 |
| Staffing plan & role clarity | 1 | 2 | 4 | optimizable | JR: "not really formally… I feel like we have it but not in one place." Individual job descriptions exist and are reviewed at annual evaluations; the org-level plan does not exist as a single artefact. *(JR, round 2)* ◷ 2026-08-14 ‖ [Staff Responsibilities Map](https://docs.google.com/drawings/d/1w8iB6siS0NJh0tNlZ0A3myBtsTayvzGYybzU_qRA8OQ/edit) ⧉ S049 S046 |
| Volunteer pathway, roles & recognition | 2 | 2 | 3 | stable | **Corrected from `undefined`.** Roughly **75+ titled volunteers** across facilitators, shop techs, the lending librarian, ambassadors, board and committee members. Structure is published; the gap is a single maintained roster ◷ 2026-08-14 ⟐ Volunteer Pathways and Member Committees — scaling next ‖ [Volunteer structure](https://www.makehaven.org/volunteer-leadership-structure) · [Intern Program](https://www.makehaven.org/intern-program) · [New Member Ambassador](https://docs.google.com/document/d/1XKOOxTMI4VJH66fhmKHbuVxwsz4eo_xgdWBQ4e_tBZc/edit) ⧉ S050 S051 S052 S053 |
| Annual member meeting | 2 | 2 | 3 | stable | Held with a recorded presentation; the PDF of that deck doubles as the annual report when one is requested ⟐ Transparent Communication and Shared Leadership — building next ⧉ S002 S060 P5 |
| ED time reporting to board | 2 | 3 | 2 | changing | New Aug 2026, from a 5-day pilot. **Also the only real source for the `effort_hrs_month` field this registry is missing** — worth wiring the two together rather than estimating twice ⧉ S048 |
| Harassment & conduct complaints | 3 | 3 | 5 | stable | **Corrected from `unknown`.** Intake is a Google Form — chosen deliberately for privacy control rather than the site's own webforms — which emails staff, who act immediately. Gap: no case record or tracking beyond the mailbox ◷ 2026-08-14 ‖ [Harassment policy](https://www.makehaven.org/harassment) ⧉ S025 S047 S006 |
| Board–member engagement | 1 | 1 | 3 | optimizable | A member comment states the board "fails every transparency test I can think of"; JR's reply agrees a stronger feedback loop is needed ⟐ Board Interaction with Members — scaling next ‖ [Expectations for Board Members](https://docs.google.com/document/d/1DS9-Av-3Y8HBOX79xtD0s5rw7OVLNOyaAjUY1DGMN90/edit) · [Board roster](https://www.makehaven.org/team) ⧉ P5 |
| DEI review (inclusion, accessibility, affordability) | 2 | 2 | 3 | stable | The DEI committee is active again and the accessibility walk-through runs annually alongside the safety one ⟐ Inclusive Representation and Accessibility Review — refining next ‖ [Committee structure](https://www.makehaven.org/volunteer-leadership-structure) ⧉ S055 S057 |
| Records retention & filings calendar | 1 | 2 | 5 | optimizable | Filings are now documented in the renewal calendar, but **JR confirms there is no retention rule of any kind yet — "need to establish."** That blocks the Standards three-years-of-evidence test and leaves no defined answer to what we keep, for how long, or where. *(JR, round 2)* ◷ 2026-08-14 ‖ [Filing requirements & procedures](https://docs.google.com/document/d/1utOZLoGWzUXXe0hS3D7jt1YPEMKZ93yD1ztQedEaF0k/edit) ⧉ S006 S001 |
| Nondiscrimination & accommodation requests | 3 | 2 | 4 | stable | **Corrected from `undefined`.** Requests go to the shop manager and director, and there is a dedicated accessibility-issue intake alongside the general concern pipeline. *(JR, round 2)* ◷ 2026-08-14 ⟐ Adaptive Tools Training and Representation — building next ‖ [Accessibility issue form](https://www.makehaven.org/accessibility-issue) ⧉ S055 |
| Member IP rights | 2 | 3 | 3 | stable | **Corrected — a policy does exist.** The membership agreement states members keep their own IP, which satisfies Standards S008. *(JR, round 2)* ◷ 2026-08-14 ‖ [Membership agreement](https://www.makehaven.org/membership-agreement) ⧉ S008 |
| Demographic data collection & reporting | 4 | 3 | 3 | stable | Lives in CiviCRM since Dec 2025; dashboards converted 07-10 ▦ kpi_membership_diversity_bipoc ⧉ S054 S057 P2 |

## Platform & Meta

_How we change everything else._

| Process | A | D | I | State | Notes |
|---|---|---|---|---|---|
| Feature planning | 2 | 3 | 3 | stable | Tracks carry a premise and kill criteria since 07-09 |
| Deploy pipeline | 4 | 4 | 4 | stable | **The model for what stable looks like.** An SOP others have run, a wizard that enforces it, a ground-truth state file ⧉ S037 |
| Config reconciliation | 3 | 3 | 4 | stable | Known gotcha: it deletes committed staged config ⧉ S037 |
| Security audit | 3 | 3 | 5 | stable | Quarterly. Four of six dimensions never run ⧉ P2 |
| Weekly pulse triage | 3 | 3 | 2 | stable | The weekly pass over incoming signals — tickets, reports and alerts — deciding what gets attention that week. ◊ 2026-08-15 ⧉ S037 |
| Cycle review | 2 | 3 | 3 | stable | Replaced a 950-line improvement pipeline that was fully specified and never ran once |
| Backup & disaster recovery | 3 | 3 | 5 | stable | Three systems hold essentially everything: **Google Drive** (Google for Education) for documents, **Pantheon** for the website with its own robust backups, and **GitHub** for code — which has repeatedly been the actual recovery tool. UniFi cameras are a fourth, lesser store. Each vendor carries its own recovery documentation, and JR has performed real restores. What is missing is a MakeHaven-side runbook saying which to restore in what order. *(JR, round 2)* ◷ 2026-08-14 ⟐ Secure and Collaborative Digital Infrastructure — building next ⧉ S035 S037 |
| Scheduled job execution | 4 | 1 | 4 | optimizable | **Added 2026-08-18 by the module sweep — almost everything that runs on a timer rides on this and nothing had a row for it.** 57 registered jobs run under Ultimate Cron behind an hourly external trigger: the Chargebee status sync, the UniFi access sync, the Xero bill sync, the Slack member sync, the weekly digest, the monthly membership snapshot and the rest. It works — `system_cron` completed 24 passes on every full day in the retained window. What is missing is anything watching it. **The launcher logs "No free threads available for launching jobs" roughly 57 times a day, every day** (554 across nine days). That is invocations arriving while a pass is still running rather than the hourly pass being lost, but it means a real stall would look exactly like the noise we have learned to ignore. Separately `makerspace_ai_tool_context_cron` has sat disabled since 2026-07-08 and nothing reported it. The end state someone can name: a job that misses its own window tells a person, instead of a person noticing ⧉ S037 |
| Production error monitoring | 2 | 2 | 4 | optimizable | **Added 2026-08-20 by the cycle review — three separate rows already carried a "we could not see it fail" finding and nothing named the underlying process.** How anyone learns that production is broken. In practice: the weekly pulse reads the watchdog trend, `scripts/daily_log_triage.py` runs a pass, and a handful of modules alert into Slack. The signal it all rests on is badly degraded. **Over the 12 days watchdog retains, 355,028 of ~410,000 rows are a single warning** — `Theme hook %hook not found.`, the known search_api shutdown-phase flood whose 2026-08-03 fix missed `site_content` and never stopped, at roughly 29,600 a day. Add 32,315 debug-level `access_display` rows for a service account and the bot-driven 404s below, and **real errors are about 0.2% of the log**: 533 CiviCRM, 552 UniFi, 130 geocoding, the rest in single digits. Two consequences, one obvious and one not: triage means reading past a wall of noise, and the volume is itself a database write load on a site with standing performance complaints. **The pattern this row exists to name:** the W34 digest stall left no error at all because PHP killed the send rather than it throwing, so every error-log-based check was structurally blind; the late-fee refunds were first re-recorded as still broken because a search for new failures found none, when a search for successes showed they had gone through. Absence of errors is not evidence of health, and nothing here is built to know the difference. Scored A2 because a human starts every pass, D2 because the pulse and workflow-health docs describe it, I4 because the failures it misses are billing and delivery ones ‖ [Workflow health](https://github.com/makehaven/makehaven-website/blob/master/docs/ops/WORKFLOW_HEALTH.md) · [Pulse log](https://github.com/makehaven/makehaven-website/blob/master/docs/ops/PULSE_LOG.md) ⧉ S037 |
| Hostile traffic filtering | 2 | 1 | 3 | optimizable | **Added 2026-08-20 by the cycle review.** Keeping automated and hostile traffic off the site. Monitoring exists — the Pantheon traffic overage is checked weekly in `workflow-health.sh` — but nothing filters anything: there is no edge rule, WAF or rate limit, so every scanner request is served by PHP. The measurable cost is not just bandwidth. **Bots hitting registration URLs for events that do not exist produced 444 CiviCRM fatal errors in 12 days**, one URL (`/civicrm/event/register?id=765`) accounting for 358 of them and still firing; each is a full CiviCRM bootstrap that ends in a crash. The referrers are spoofed (`bing.org`, `google.org`, `baidu.org` — note `.org`), so this is not a broken internal link to chase. The 404 log agrees: the top paths are `/.env`, `/api/.env`, `/graphql` and a WordPress plugin exploit probe, at 100–230 hits each, alongside 52,930 access-denied and 36,087 not-found rows in the same window. **`optimizable` rather than `planned`** because the watching half runs and the acting half was never built — the named next step is an edge layer, which also happens to be the only near-term way to restrict the unauthenticated door API (see *API endpoint security*) ⧉ S037 |
| Member-facing AI assistants | 4 | 2 | 2 | optimizable | **Added 2026-08-18 by the module sweep.** Two grounded chatbots are live: a member navigator that routes people to the right page for membership, resources, tools and projects, and a tool-page assistant that injects the live node data for whichever tool you are reading so the answers are about that machine. Both are link-first with a guard that strips invented URLs — it fired 4 times in the retained window, which is the point of having it. Context injection ran 325 times in nine days, but **the AI request log records only one to five actual conversations a day through August 2026**: built, live, and barely used. The named end state is the curated knowledge layer these are meant to read from. **Measured properly for the first time 2026-08-20 by the cycle review, and three things changed the picture.** (1) **Answers were never being recorded at all.** `ai_logging` writes `output_text` from the provider's raw output and the OpenAI chat provider leaves it empty — every chat row on live is literally `{}`, so the AI oversight console has been showing blank replies and answer quality was unmeasurable except when a member happened to ask a follow-up and the previous turn came back as conversation history. Which assistant answered and which user asked were not recorded either. Fix staged 2026-08-20 (`makerspace_ai_tool_context` 6a34121): the answer, a refusal flag, the assistant id and the uid now go into the log's `extra_data`. (2) **The quality problem is concentrated and countable.** Of the navigator conversations where the member sent a second turn, roughly **70% followed the assistant saying "I'm not sure" or "I don't know"** — the follow-up is usually a member re-asking after a failure, not deepening a good answer. Asked how to submit a meetup it pointed at the CiviCRM event browser; the member replied *"The answer is makehaven.org/meetup — learn that"* and it said "I'm not sure" again. (3) **The demand is wayfinding, not tool expertise.** 24 navigator questions since 2026-07-01 cluster into five intents — room and door access (7), membership change (4), booking and facilitator hours (4), stuck in onboarding (3), profile editing (2) — while the tool-page assistant, which is on every tool and badge page for members and anonymous visitors alike, draws about three questions a month. **The reach gap is the actionable half:** the navigator is placed on six path patterns (`/resources*`, `/my-membership*`, `/badges`, `/user/*`) and none of `/access-request`, `/appointments` or the onboarding pages are among them, so a member sitting on the page where the question arises has nothing to ask. Nobody has ever rated an answer — the feedback table has 8 rows and has not moved since 2026-07-16. Separately, "Red", the anonymous recruitment assistant built to answer prospective-member questions without login, is **switched off** on the theme anonymous visitors actually get while still enabled in a theme the site does not use ⚙ makerspace_ai_tool_context,makerspace_member_navigator |
| Admin access & systems register | 2 | 2 | 4 | changing | **Upgraded from `degraded` — a register has been started.** Access is genuinely distributed (Pantheon with Terence and Yan, Chargebee/Stripe with Kate, Xero with the treasurer, Home Assistant with Vincent, Corey and Lior, Firebase under an org account, domain under org email) and everything is recoverable by taking control of the ED's work email. Finishing the started document closes the largest remaining bus-factor gap. *(JR, round 2)* A **MakeHaven System and Data Access Agreement** webform has also been capturing who holds what since May 2025 (21 submissions) — a better foundation than the draft document alone suggested. ◷ 2026-08-14 ⟐ Secure and Collaborative Digital Infrastructure — building next ‖ [Systems register (draft)](https://docs.google.com/document/d/18B7Oxe8kvQCvrex1dLNuhUiMWqXN-r7yzE-QwXHxe2Q/edit) ⧉ S037 S009 |
| Local development environment | 2 | 3 | 2 | stable | Documented and repeatedly repaired |
| Preview / staff testing | 4 | 3 | 2 | stable | Sandbox site for extended staff testing |
| Policy & procedure document index | 1 | 2 | 4 | changing | The operations doc is the current answer and it is drifting. JR wants something stronger — possibly folded into Governance-Dance, possibly its own continuity tool. **That decision is now live rather than hypothetical**, because this registry is starting to do part of the job. *(JR, round 2)* ◷ 2026-08-14 ‖ [Operations index](https://www.makehaven.org/operations) · [Staff tools hub (staff)](https://www.makehaven.org/staff-tools) ⧉ P9 S006 |
| Process registry maintenance | 1 | 3 | 3 | changing | This document. It belongs in its own inventory, and it starts at A1 ⟐ AI-Driven Automation and Member Support — building next ⧉ P9 |
| Curated knowledge & Q&A layer | 1 | 1 | 3 | planned | A maintained knowledge layer — curated answers, indexed tool manuals — feeding site search, member support and the AI assistants, so answers come from one reviewed source instead of scattered pages. Named a high-priority initiative on the website master roadmap; no track yet. ◊ 2026-08-16 |
| Makerspace Collective API integration | 1 | 1 | 2 | idea | Aligning MakeHaven's success metrics with the national makerspace collective's data aggregator — standardised measurement and collective grant power. Roadmap status: research. Related to but distinct from ecosystem partner data alignment, which is local. ◊ 2026-08-16 |
| Screen & display fleet upkeep | 3 | 2 | 2 | watch | The Raspberry Pi displays around the shop run, but each is hand-built: no standard image, setup knowledge tribal. Two things changed in August 2026. The fleet was **inventoried** — six screens, their routes, refresh intervals and failure modes, written up at `docs/ops/DISPLAYS.md`, which is why D moves 1 → 2. And a **shared self-heal runtime** shipped live 2026-08-20 (`makerspace_kiosk`, first consumer `access_display`): the boards now poll with backoff, show a status chip carrying a ticking clock and a liveness dot, and reload themselves when a feed goes stale instead of sitting there looking healthy. That last part is the real fix — the member faces board **failed silently**, because its fetch errors were swallowed and its grid is append-only, so a dead feed rendered identically to a live one. A moves 2 → 3: recovery is automated, provisioning is still by hand. **Watching**: whether the chip reads green on the physical screens (still unconfirmed by a person at the hardware), and whether the remaining consumers — `facilitator_display`, `makerspace_screen_slideshow`, `makehaven_tasks` — get moved onto the shared runtime. ◊ 2026-08-16 ⚙ makerspace_kiosk,access_display,makerspace_screen_slideshow ‖ [Display fleet](https://github.com/MakeHaven/makehaven-website/blob/master/docs/ops/DISPLAYS.md) |

---

## Where this draft is weakest

1. **Facilities, Governance and staff/HR are still largely inferred.** v2 knows
   what the strategic plan *wants* those processes to be. It still does not know
   what actually happens today. A plan saying "conduct annual drills" is not
   evidence that drills happen.
2. **Documentation scores are the least reliable column.** "An SOP file exists"
   is not D3 "current," and nothing here is verified D4.
3. **Effort in staff hours is absent** — the field that would most improve the
   automation ranking. The strategic plan's Year 1 hour estimates are the best
   available proxy and are only a forecast, not a measurement.
4. **Granularity is unvalidated and now visibly uneven.** Lending gets ten rows;
   "space opening / closing" gets one. That is an artefact of where documentation
   exists, not of where the work is.
5. **Some rows may be aspirations, not processes.** "Planned giving programme"
   and "Made at MakeHaven marketplace" are strategic intentions with no current
   operation. The registry needs to distinguish *a process running badly* from
   *a process that does not exist yet* — `undefined` currently conflates them.
   Worth a sixth state, or a `planned: true` flag, before Phase 1.

---

## Suggested agenda for the Phase 0 session

1. **Argue with the groups first** (15 min). Thirteen groups. Confirm the
   group → strategic-goal mapping, since that is what makes the board view work.
2. **Separate aspiration from operation** (20 min). Walk the `undefined` rows
   and split them: *should be running and isn't* vs *not started, and that's
   fine.* Weakness 5 above.
3. **Fill Facilities and Governance from life, not from the plan** (45 min).
   What actually happens when a tool breaks, when the building floods, when a
   board seat opens. Only staff can supply this.
4. **Calibrate on ten rows** (30 min). Where two people disagree, fix the *scale
   wording*, not the score.
5. **Assign owners** (30 min). Rows where nobody can name an owner are the
   finding.
6. **Do not score the whole list in the room.** Owners score their own rows;
   the AI maintenance pass keeps the derived fields current afterward.
