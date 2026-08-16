# Plans sweep — 2026-08-16

A review of every planning document in `makehaven-website` against the registry,
asking one question per source: *does this add a process, modify one, or is it
not a process at all?* Run once; worth re-running when the master roadmap is
next reconciled (last: 2026-07-08).

**Sources scanned:** `conductor/master_roadmap.md`, `conductor/plan.md`,
`TODO.md` (147 lines, including the staff-feedback and chat-history backlogs),
all 23 `conductor/tracks/*/plan.md`, and the four `docs/*PLAN*.md` documents.

**Commitment vocabulary used below,** matching the registry's states:
a *track* is committed work (`changing` when active), a *roadmap initiative*
is a confirmed intention (`planned`), and a *TODO idea or research item* is
exactly that (`idea` — the state created for this sweep).

---

## Added to the registry (8 rows, all ◊ drafted, none reviewed)

| Row | Group | State | Source and commitment |
|---|---|---|---|
| Opportunity relay (commissions, gigs & job posts) | Entrepreneurship | `changing` | **A running process the registry had missed** — staff hand-paste outside requests into `#jobs` today; `opportunity_board_20260813` is active |
| Curated knowledge & Q&A layer | Platform & Meta | `planned` | Master roadmap initiative, priority High, no track yet |
| Public credential transcript (Open Badges) | Education & Instruction | `planned` | Roadmap initiative, Medium; member-public-profile MVP already shipped as groundwork |
| Venture business profiles & support logging | Entrepreneurship | `idea` | Roadmap backlog + TODO; would restore the retired `kpi_milestones_achieved` |
| Makerspace Collective API integration | Platform & Meta | `idea` | Roadmap status Research, priority Low |
| Equipment satisfaction micro-feedback | Facilities & Equipment | `idea` | Three variants sketched in TODO ("*Idea:*", verbatim); links the orphan KPI `kpi_member_satisfaction_equipment` |
| Denied-entry rejoin follow-up | Membership & Billing | `idea` | TODO section with defined scope (templates, quiet hours); no commitment |
| Screen & display fleet upkeep | Platform & Meta | `optimizable` | Displays run today, hand-built each time; TODO names the end state (standard image, provisioning script, docs) |

## Modified (2 rows)

- **Inbound phone & voicemail triage** `optimizable` → `changing` — the
  `voice_ai_routing` track shipped its Phase 1 foundation live 2026-08-07
  (inert behind config), and the Voicemail-Tool awaits a Twilio number. Work is
  landing, not merely wished for.
- **Facilitator 6-month renewal** `stable` → `changing` —
  `facilitator_lifecycle_20260811` builds exactly the gap the row documents
  (term fields, reminders, offboarding).

## Already covered — no change needed

Tracks whose process already has a row in the right state:
`monthly_newsletter` → *Monthly newsletter* (changing) ·
`member_awards` → *Member recognition & awards* (changing) ·
`new_member_onboarding_recovery` → *Onboarding nudge* (watch) ·
`workspace_rental_system` → the two workspace rows ·
`recovery_dunning_urgency` → *Dunning / payment recovery* ·
`sponsorship_research_tool` → *Major donor LAI qualification & pipeline* ·
`appointment_on_request` → *On-request badger matching* ·
`process_stabilization` → *Process registry maintenance* ·
`standard_event_lifecycle` + `event_management_ecosystem` → act on *Class
scheduling & publishing* (already `changing`) ·
`tool_expert_chatbot` → parked 07-08 at near-zero usage; the registry already
cites it as the cautionary precedent.

## Deliberately not added

- **Product features, not operational processes:** area-of-interest term hubs,
  project-path onboarding, tool favorites, member public profile, D11 theme
  aesthetics. The registry maps how the organisation runs, not what the website
  offers; a feature earns a row only when operating it becomes somebody's job.
- **One-time tasks:** card-serial migration, D7 Projects migration, CiviCRM
  non-prod email safety, the ghost-tool-charge repair, the chat-history bug
  backlog. Tasks belong to tracks and TODO, not to a standing process map.
- **Enhancements to existing rows, noted here rather than duplicated:**
  referral-tracking re-implementation (acts on *Referral / bring-a-friend*),
  post-appointment feedback automation (acts on *Class evaluation collection* /
  facilitator feedback), quiz standardisation and advanced badges (act on
  *Badge quiz authoring*), menu-architecture audit (acts on *Website content
  publishing* at most).

## What the sweep says about the sources

The website repo's planning surface is in better shape than the phrase "various
levels of commitment" suggests: the master roadmap already distinguishes
Active / Planning / Backlog / Research, and it reconciles against tracks. The
real gaps this sweep found were the two blind spots the registry now closes —
a running manual process nobody had inventoried (the `#jobs` relay), and
brainstorms living in a TODO where they read, misleadingly, like commitments.
The `idea` state exists so the second kind has an honest home.
