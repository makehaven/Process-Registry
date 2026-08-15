# Standards ↔ Process crosswalk

Maps every row in `data/inventory.md` to the CT Makerspace Network **Standards of
Excellence** standards it implements, and vice versa.

**Draft, 2026-08-14. Not yet reviewed. Nothing in the inventory has been edited.**

## Why both directions matter

- **Standard → processes** answers *"what would we actually have to change to
  move S023 from 1 to 2?"* — the drill-down the standards tool cannot do alone.
- **Process → standards** answers *"is this broken row anybody's problem
  outside MakeHaven?"* — and, where the answer is no, whether that is because
  the process is ours alone or because **the standards are missing something**.

The second direction is what produced `STANDARDS_GAPS.md` in the
`Makerspace-Standards` repo.

## Notation

| | |
|---|---|
| `S023` | implements that standard |
| `S055*` | implements it, but the standard as written does not reach what this process does — see gaps doc |
| `P1`–`P9` | **proposed** standard that does not exist yet — see gaps doc |
| `— exec` | deliberately not a standards concern: business execution, growth, marketing |
| `— impl` | implementation detail sitting beneath a standard listed on another row |

`— exec` is not a criticism of the row. Roughly a third of the inventory is how
MakeHaven grows and competes, which is none of the network's business. Marking
it explicitly is what keeps the standards from trying to absorb the registry.

## Proposed sigil for `data/inventory.md`

If this is adopted, standards references join the existing row conventions as a
third segment, after strategy (`⟐`) and before docs (`‖`):

```
| Process name | A | D | I | state | description ⟐ strategy · WORKTYPE ⧉ S023 S015 ‖ docs |
```

`⧉` for standards. Order: `⟐` → `⧉` → `‖`.

---

## Education & Instruction

| Process | Standards | Note |
|---|---|---|
| Instructor recruitment funnel | **P3** | No standard governs who is allowed to teach |
| Instructor proposal review | **P3** | — |
| Instructor agreement signing | **P3** · S008 | Agreement carries IP terms |
| Instructor interest acknowledgement | — exec | — |
| Instructor development & peer observation | S058 · **P3** | S058 covers pedagogy, not instructor qualification |
| Instructor evaluation & coaching | S058 · **P3** | — |
| Class scheduling & publishing | **P3** | — |
| Class registration | **P3** | — |
| Class promotion / seat fill | — exec | — |
| Event capacity marketing | — exec | — |
| Class evaluation collection | S057 · S058 | — |
| Workshop fill-rate management | — exec | — |
| Instructor stipend payment | **P3** · S046* | Staff module never activates for contractor-only spaces |
| GEMS cohort management | S054 · S056 | — |
| Badge quiz authoring | S022 · S026 | — |
| Badge grant from quiz | S022 | — |
| Badge checkout appointment | S022 | — |
| Facilitator scheduling | S050 · S051 · S028 | — |
| Facilitator 6-month renewal | S051 · S023* | S023 requires suspension, never expiry — the missing term-date field |
| On-request badger matching | S050 · S030 | — |
| Youth & school custodial partnerships | S066 · S067 · S068 · S069 · S059 | — |
| Peer benchmarking (annual) | S084 | — |

## Entrepreneurship

| Process | Standards | Note |
|---|---|---|
| Entrepreneur goal capture at signup | S054 | — |
| Entrepreneur dashboard & nudges | — exec | — |
| Entrepreneurship AI support assistant | **P2** | Member-facing AI has no standard; watch rather than write one yet |
| Nexus platform bridge | S059 | — |
| Incubator workspace intake & graduation | S071 · S072 · S073 | Graduation still undefined |
| Entrepreneurship milestone tracking | S074 | — |
| Mentor & advisor matching | — exec | — |
| Entrepreneurship events programming | S054 | — |
| Cohort programs (Ecolab-style) | S074 | — |
| "Made at MakeHaven" marketplace | S071 | Commercial-use policy governs it |
| Ecosystem partner data alignment | S059 · **P2** | Sharing member data with partners |

## Facilities & Equipment

| Process | Standards | Note |
|---|---|---|
| Tool acquisition & commissioning | S032 · S015 · **P6** | No standard gates a new tool going live before an SOP exists |
| Tool downtime & repair tracking | S033 · S034 | — |
| Preventive maintenance schedule | S034 | — |
| Equipment depreciation & replacement planning | S039 | — |
| Shop budget adherence | S040 | — |
| Consumable restock | S013 | Only the hazardous subset is covered |
| Physical inventory count | S032 · S038 | — |
| 24/7 self-access operation | S017 · **P1** | S017 is one non-critical clause under an entire operating model |
| Cleaning & shop upkeep | S036 | — |
| Building maintenance & landlord liaison | **P7** · S035 | S035 backs up the lease; nothing addresses occupancy or permits |
| Safety program review & drills | S011* · S019 | No standard requires the drill to be *practised* |
| Incident & near-miss reporting | S016* | S016 does not require telling the reporter what happened |
| Accessibility / ADA audit | S055* | S055 is policy-level; no physical audit or improvement loop |
| Insurance / lease / compliance renewals | S001 · S018 · S043 | — |
| Sustainable operations practices | S020 | — |
| Chemical inventory & SDS access | S013 | — |
| Lockout / tagout of unsafe equipment | S033 | Remote lockout blocked on tool access control |
| Routine shop inspection walk-through | S036 | — |
| Hazardous & material waste disposal | S020 | — |

## Access & Safety

| Process | Standards | Note |
|---|---|---|
| Door access control (building entry) | S023* · **P1** | No standard asks what happens when the access system is unreachable |
| Tool access control (interlocks) | S015 · S022 · S023 | Standards catch this correctly — it would score low, and should |
| Access-control hardware operations | S037 · S035 | — |
| Event visitor passes | S027 | — |
| Access request approval | S023 | — |
| Guest & waiver handling | S027 | — |
| Tool issue reporting | S016 · S033 | — |
| Tool status communication | S033 · **P8** | — |
| API endpoint security | **P2** · S037 | S037 is continuity, not protection of personal data |

## Lending, Storage & Store

| Process | Standards | Note |
|---|---|---|
| Borrower onboarding | S062 | — |
| Loan checkout | S062 · S063 | — |
| Loan return | S064 | — |
| Overdue late fee | S063 · S024 | — |
| Damage deposit | S063 | — |
| Battery tracking | S064 | Lithium storage/charging risk is implicit at best |
| Missing / lost item handling | S065 | — |
| Item repair & retirement | S064 · S065 | — |
| Librarian role administration | S050 · S051 | — |
| Lending budget review | S065 | — |
| Storage assignment | S079 · S080 | Rentals module covers storage |
| Storage billing | S041* · S024 · S082 | Nothing reconciles entitlement against payment |
| Store purchase | S041 · S001* | Retail sales tax sits inside "required filings" |
| Store member tab collection | S041 | — |
| Store inventory restock & reorder | S041 | — |
| Line-of-business profitability review | S043 · S061 | Core has no equivalent of S074/S083 subsidy review |

## Membership & Billing

| Process | Standards | Note |
|---|---|---|
| Join / signup flow | S021 · S024 | — |
| Email validation at signup | — impl | Under S021 |
| Payment setup | S024 · S041 | — |
| Membership status sync | S023 · S024 | — |
| Dunning / payment recovery | S024 | — |
| Cancellation & offboarding | S023 · S024 | Access revocation on cancel — the strongest control we have |
| Member conduct & discipline | S025 | — |
| Exit survey & ending-reason capture | S057 | — |
| Rejoin / recapture campaign | — exec | — |
| Comped / sliding-scale / sponsored memberships | **P4** · S024 · S055 | The app collects need-based dues as a metric with no standard behind it |
| Stripe customer linkage | S041 | — |
| Membership pricing review | S024 · S043 | — |
| Workspace rental agreement | S079 · S082 | — |
| Workspace rental billing | S041 · S079 | — |

## Member Experience & Retention

| Process | Standards | Note |
|---|---|---|
| Onboarding nudge / stalled-join recovery | — exec | — |
| Orientation scheduling | S021 | — |
| First-badge-in-28-days promotion | — exec | — |
| Interest capture + Slack invite | — exec | — |
| Member success outreach queue | — exec | — |
| At-risk early-warning detection | — exec | — |
| Retention intervention tracking | — exec | — |
| New-member 3-month survey | S057 | — |
| New-member gatherings & peer intros | S030 · S056 | — |
| Interest-based member groups | S056 | — |
| Member recognition & awards | S053 | S053 covers volunteers only |
| NPS & satisfaction survey | S057 | — |
| Community Wishlist | S057 · S039 | — |
| Deferred profile field capture | S054 | — |
| Member feedback triage | S057 · S061 | The A3 worth copying |
| Quarterly close-the-loop reporting | S061 · S060 | — |
| Year in review | S060 | — |

## Outreach & Recruitment

Almost entirely `— exec`. This group is the clearest demonstration that the
registry is the larger of the two documents and should stay that way.

| Process | Standards | Note |
|---|---|---|
| Tour booking & delivery | S027 | Visitor boundaries apply |
| Tour follow-up & conversion | — exec | — |
| Guest waiver → member conversion | S027 | Waiver half only; the conversion half is exec |
| Workshop participant → member conversion | — exec | — |
| Discovery source capture | S054 | — |
| Referral / bring-a-friend | — exec | — |
| Ambassador program | S050 | Volunteer roles once it exists |
| Community tabling & partner events | S059 | — |
| Community partnership development | S059 | — |
| Media relations & press kit | — exec | — |
| Neighborhood & postcard campaigns | — exec | — |
| Paid digital advertising & retargeting | — exec | — |
| Lead / inquiry handling | **P8** | Can the public reach a responsible person? |
| Member phonebank campaigns | — exec | — |

## Communications

| Process | Standards | Note |
|---|---|---|
| Weekly digest | **P8** | — |
| Monthly newsletter | **P8** | — |
| Mailing list / smart group hygiene | **P8** | Silently frozen feeder groups = cannot reach members |
| Slack announcements | **P8** | — |
| Website content publishing | — exec | — |
| SEO & analytics instrumentation | — exec | — |
| Inbound phone & voicemail triage | **P8** | — |
| Impact storytelling & member spotlights | S060 | — |
| Annual report & impact reporting | S060 · S042 | S060 wants setbacks too — check the deck |

## Finance & Accounting

Best-covered group in the inventory. S040–S045 map almost one to one.

| Process | Standards | Note |
|---|---|---|
| Contractor payment → Xero bill | S041 · S046* | — |
| Vendor payment via Melio | S041 | No periodic sweep — a control-design point under S041 |
| Stripe → Xero reconciliation | S041 | — |
| Monthly financial close | S040 · S041 | — |
| Budget vs actual review | S040 | — |
| Reserve fund management | S045 · S039 | 2.93 months against a 6-month goal |
| Annual external review / audit | S044 | — |
| Financial policy maintenance | S041 · **P9** | — |
| Financial dashboards & board briefings | S040 · S043 | — |
| Donation processing | S042 | — |

## Development & Fundraising

| Process | Standards | Note |
|---|---|---|
| Annual appeals (spring + year-end) | S042 | — |
| Recurring giving program | S042 | — |
| Major donor LAI qualification & pipeline | S042 · **P2** | LAI scoring is sensitive personal data |
| Major donor stewardship cadence | S042 | — |
| Corporate sponsorship solicitation & renewal | S042 | — |
| Sponsor recognition & benefit fulfilment | S042 | — |
| Grant pipeline & deadline tracking | S042 · S001 | — |
| Grant outcome recording | S042 | — |
| Donor data hygiene in CRM | **P2** | — |
| Case statement maintenance | S007 | — |
| Planned giving / bequest program | S042 · **P6** | Bequests of equipment are the acceptance problem in its sharpest form |

## Governance & People

| Process | Standards | Note |
|---|---|---|
| Board recruitment matrix & sourcing | S003 | — |
| Board nomination & election | S002 · S003 | — |
| Board onboarding | S003* · S010 | No standard requires director orientation |
| Board self-assessment (annual) | S010 | — |
| Board & committee minutes retention | S004 · S006 | — |
| Governance policy annual review | S006 · **P9** | — |
| Committee charters & effectiveness | S002* · S004 | Committees are how volunteer-led spaces actually govern |
| Governance archive / institutional memory | S006 · **P9** | — |
| Board officer & director succession | S002 · S009 | Defined in the bylaws |
| Executive succession & emergency authority | S009 | **The standard found the biggest gap we have** |
| Staff onboarding / offboarding | S046 · S047 | — |
| Staff development, benefits & wellbeing | S048 | — |
| Staffing plan & role clarity | S049 · S046 | — |
| Volunteer pathway, roles & recognition | S050 · S051 · S052 · S053 | 75+ titled volunteers, no single roster |
| Annual member meeting | S002 · S060 · **P5** | — |
| ED time reporting to board | S048 | Also the source for the registry's missing `effort_hrs_month` |
| Harassment & conduct complaints | S025 · S047 · S006 | — |
| Board–member engagement | **P5** | "Fails every transparency test I can think of" — no standard reaches this |
| DEI review (inclusion, accessibility, affordability) | S055 · S057 | — |
| Records retention & filings calendar | S006 · S001 | Blocks the three-year evidence test |
| Nondiscrimination & accommodation requests | S055 | — |
| Member IP rights | S008 | — |
| Demographic data collection & reporting | S054 · S057 · **P2** | — |

## Platform & Meta

| Process | Standards | Note |
|---|---|---|
| Feature planning | — exec | — |
| Deploy pipeline | S037 | The A4/D4 model row — what "proven" documentation looks like |
| Config reconciliation | S037 | — |
| Security audit | **P2** | The quarterly audit exists; no standard asks for it |
| Weekly pulse triage | S037 | — |
| Cycle review | — exec | — |
| Backup & disaster recovery | S035 · S037 | Missing the order-of-restore runbook |
| Admin access & systems register | S037 · S009 | — |
| Local development environment | — exec | — |
| Preview / staff testing | — exec | — |
| Policy & procedure document index | **P9** · S006 | — |
| Process registry maintenance | **P9** | This document's own parent |

---

## Reverse index: standards with thin or absent process coverage

Not standards gaps — **MakeHaven** gaps, surfaced by running the crosswalk
backwards. These are standards with no process, or only a partial one.

| Standard | | Coverage |
|---|---|---|
| S026 | Credential quality review, equivalency | **No process.** Badge quiz authoring is adjacent; no review cycle, no equivalency rule for members arriving with outside training |
| S031 | Public-access data reviewed annually | **No process.** Guest waivers are captured and never analysed |
| S045 | Multi-year forecast, adverse scenarios | Partial — reserve is managed, no scenario analysis |
| S049 | Workforce review: pay equity, single-person dependencies | **No process.** The bus-factor question the registry keeps hitting has no owner |
| S052 | Volunteer backup coverage, handoffs | **No process** against 75+ titled volunteers |
| S053 | Annual volunteer workload/burnout/succession review | **No process** |
| S061 | Evaluation findings demonstrably change decisions | Planned only (quarterly close-the-loop) |
| S065 · S070 · S074 · S078 · S083 | Module-level annual reviews | None run as a defined process |

### The pattern in that table

Of the 18 tier-3 standards — the ones that gate **Exemplary** — we can match a
real MakeHaven process to roughly half, and most of those are partial. The
recurring shape is *"three annual reviews of X"*, and **nobody has a process for
doing an annual review of anything.** The reviews that do happen (safety
walk-through, accessibility walk-through, board self-assessment) are calendar
events without a defined findings-to-closure loop.

Read alongside the retention finding — no retention rule of any kind, which
blocks the three-year evidence test outright — the practical conclusion is that
Exemplary is currently unreachable for the most systems-mature space in the
network, and not because of the substance of any individual standard. That is a
framework calibration question, raised in `STANDARDS_GAPS.md`.
