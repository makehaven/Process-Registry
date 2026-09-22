# Obligations Register

_Drafted 2026-09-21 from `docs/RENEWAL_CALENDAR.md` (JR, 2026-08-14) plus a sweep
of the `jrlogan@makehaven.org` mailbox and the `makehaven-website` repository.
Owner: Executive Director. Review annually, and after any filing._

**Process registry:** `insurance_compliance.renewals`, `governance.records_retention`,
`finance.contractor_payments`, `finance.staff_reimbursement`

The renewal calendar answered *what recurs*. This answers the three questions a
successor actually has in front of them: **when is it due, what proves it was
done last time, and what breaks if it slips.** Every row carries evidence or
says plainly that it has none.

---

## How to read it

- **Cadence** — the real cycle, not the aspiration.
- **Due** — the statutory or contractual date. Where the old calendar carried a
  *target* date that differed from the real one, the real one is here and the
  discrepancy is called out.
- **Start work** — the day the working period opens. Most obligations have a
  window of preparation and then a hard date; the calendar carries both, so a
  reminder arrives when there is still time to act, not when the date lands.
- **Evidence** — the artefact that proves the last cycle closed. "None found"
  means exactly that: the mailbox sweep found no confirmation, which is not the
  same as it not having happened.
- **State** — `current` · `due-soon` · `at-risk` · `unresolved` · `unverified`

`at-risk` means the deadline is reachable but something is in the way.
`unresolved` means a cycle appears to have been missed and the consequence has
already landed.

---

## At a glance

| Start work | Hard due | Item | Cadence | Owner | State |
|---|---|---|---|---|---|
| same day | 1st & 15th | Contractor payment approval & pay run | Semimonthly | ED | current |
| now | Sep 28 | Check Xero↔Gusto connection (Gusto says reconnect) | One-off | ED | due-soon |
| Sep 7 | Oct 7 | Workers' Compensation renewal | Annual | ED | due-soon |
| on receipt | ~30 days after | Workers' Comp premium audit — staff-time form | Annual, after term ends | ED | unverified |
| Oct 1 | Nov 1 | Declaration of Personal Property (New Haven) | Annual | ED | unverified |
| Sep 1 | Nov 15 | IRS Form 990 (extended) | Annual | ED + CPA | at-risk |
| Nov 16 | Nov 30 | CT Charitable Solicitation renewal | Annual | ED | at-risk |
| Dec 15 | Dec 31 | Q4 staff reimbursement form | Quarterly | Staff → ED | current |
| Dec 1 | Jan 31 | Contractor 1099-NEC issuance | Annual | ED | **at-risk** |
| Jan 5 | Jan 23 | Gusto form mailing order (precedes the IRS date) | Annual | ED | current |
| Jan 1 | Feb | General Liability & Umbrella renewal → COI to landlord | Annual | ED | current |
| Mar 1 | Mar 22 | CT Secretary of the State Annual Report | Annual | ED | **date corrected** |
| Mar 1 | Apr | Directors & Officers renewal | Annual | ED | current |
| Mar 15 | Apr–Jun | CPA financial review | Annual | ED + Treasurer | at-risk |
| Apr 15 | May 15 | IRS Form 8868 extension | Annual | ED + CPA | current |
| on receipt | Jun | CT Cultural District annual report | Annual | ED | unverified |
| Jun 15 | Jul | Board conflict-of-interest disclosures | Annual | President / ED | unverified |
| Sep 1, 2029 | Nov 1, 2029 | Quadrennial Tax Exempt Application (M-3) | Every 4 years | ED | **unresolved** |
| ongoing | Annual | Facility lease review | Annual | ED | changing |

---

## 1. The two that are already automated

These are the ones most likely to be misunderstood by a successor, because the
software does part of the job and it is not obvious which part.

### Contractor payment approval and pay run
- **Cadence:** semimonthly, 1st and 15th
- **What the software does:** contractors log hours through the timesheet form.
  Each becomes a `payment_request` entity held as a **draft**. Drupal cron on
  the 1st and 15th consolidates all drafts into **one Xero bill per contractor**
  (`xero_bills_sync`, `auto_consolidate: true`,
  `consolidation_schedule: semimonthly`). A catch-up pass re-runs any period
  cron missed, so a skipped day does not silently drop hours.
- **What a person must do:** approve the consolidated bills in Xero, then pay
  through Melio. Nothing pays itself.
  - Approval queue: `go.xero.com/app/!VMz7W/bills/list/awaiting-approval`
  - Payment queue: `go.xero.com/app/!VMz7W/bills/list/awaiting-payment`
- **Failure mode to watch:** `immediate_contractor_sync` and `auto_consolidate`
  must never both be on. Together they create duplicate Xero bills. The settings
  form warns about this; the warning is the only guard.
- **Who can pay:** payment scheduling in Melio is not limited to the ED. Kate
  Cebik and Ashley Zdeb have both scheduled contractor payments, and Ashley has
  added a delivery method for a payee. Whether that is intended is a control
  question for the finance committee, not a bug.
- **Check by 28 September 2026:** Gusto emailed on 15 September asking
  MakeHaven to **reconnect Xero to Gusto**. JR's understanding is that the two
  are already connected, and that may be right — but the notice usually means
  the authorisation token lapsed and the sync has quietly stopped. It is a
  two-minute check in Gusto's integrations settings. That sync carries wages,
  taxes, reimbursements and contractor payments into the ledger, which is the
  payroll half of the 1099 reconciliation.
- **Consequence of slipping:** contractors are not paid. Reputational and, past
  a point, a wage-claim exposure for anyone misclassified.
- **Downstream:** this feeds the 1099 obligation below. Melio and Xero issue
  them, which is why contractor onboarding into both systems matters.

### Quarterly staff reimbursement form
- **Cadence:** quarterly
- **What it is:** webform `webform_26999`, *Quarterly Health, Commuter and other
  Reimbursement Request*. A wizard covering health benefit, commuter and other
  reimbursements. Submissions email `jrlogan@makehaven.org`.
- **Standing setup it assumes:** each staff member has a recurring automatic
  premium reimbursement already configured, and a personal Drive receipts
  folder. The form asks whether the recurring amount covers the full benefit and
  branches on the answer. **If a staff member's premium changes, the ED must be
  emailed separately so the recurring amount is adjusted** — the form says so but
  does not enforce it.
- **Failure mode to watch:** the receipts-folder links are hardcoded per person
  in the form body. A staffing change requires editing the webform, and there is
  nothing that makes that visible when someone joins or leaves.
- **Consequence of slipping:** staff are under-reimbursed for a benefit they are
  owed, and the health benefit's substantiation record thins out, which is what
  makes it non-taxable.

---

## 2. Tax and regulatory filings

### CT Secretary of the State Annual Report
- **Due: 22 March.** ⚠️ The renewal calendar said "target 26 March". That is
  wrong and it has cost two consecutive years.
  - 2025: missed. Past-due notice 21 April 2025, filed 5 May 2025.
  - 2026: filed 26 March 2026 — four days late, exactly the date the calendar
    said to aim for.
- **Where:** Business.CT.gov, Business Services Division. ALEI `1066239`. $50.
- **Evidence:** filing 0013848474 confirmed 26 March 2026; filing 0013019998
  confirmed 5 May 2025.
- **Lead:** the state emails at 30 days, 14 days and on the day. File on the
  first notice.
- **Consequence:** administrative dissolution if left long enough.

### IRS Form 8868 extension
- **Due: 15 May.** Filed electronically by the CPA. This is the control that
  prevents the 990 penalty and it is not optional paperwork.
- **Evidence:** 2025 tax year extension **accepted by the IRS 28 April 2026**
  (Wolters Kluwer acknowledgment, via ZZSCPA). The 2024 tax year extension was
  *not* filed, which is what produced the late 990 and the fine.
- **Watch:** two "review and sign your extension" reminders went unread in
  April 2026. The extension was accepted regardless, but do not rely on that.

### IRS Form 990
- **Due: 15 May statutory, 15 November extended.**
- **State: at-risk.** The extension is in place, so the date is reachable. What
  is not in place is the work behind it. The CPA issued the 2025 review request
  list on 1 July 2026. JR's follow-up to Keith Sullivan on 28 August 2026 about
  bookkeeping help has no reply in the mailbox.
- **Prepared by:** ZZSCPA. **Signed by:** Board Treasurer.
- **Evidence:** 2024 990 filed June 2025 (late, fine incurred). 2023 990
  finalised 5 November 2024.
- **Ignore:** `myfilingservices.com` sends reminders claiming MakeHaven must
  file a **990-N e-Postcard**. This is a commercial solicitation, not the IRS,
  and it is wrong — MakeHaven files a full 990. Do not act on it.

### CT Charitable Solicitation (Public Charity) renewal
- **Due: 30 November.** ⚠️ The renewal calendar said "annually, per the state
  portal schedule". The date is fixed and it is 30 November.
- **Registration:** CHR.0067264. Fee $50. `elicense.ct.gov`, user ID `MakeHaven`.
  The one-time Fast Track PIN is in the renewal notice emailed to
  `admin@makehaven.org` on 10 July 2026; it is deliberately not recorded here.
- **Dependency that makes this tight:** renewal requires the current year's 990
  to be **already filed with the IRS**. The 990 is on extension to 15 November.
  That is fifteen days of slack between the two, every year the extension is used.
- **Also required:** gross revenue between $500K and $1M means attesting to an
  independent review by a CPA. Financial documents are no longer submitted but
  must be retained three years in case of a DCP audit — which is a second reason
  the missing records-retention policy matters.
- **History:** this **lapsed in 2024**. Past-due notice 18 December 2024,
  reinstated 30 December 2024. A lapse blocks state and municipal grant
  applications and public fundraising.
- **Evidence:** certificate issued 15 December 2025 for the current term.
- **Watch:** every notice goes to `admin@makehaven.org`, not to JR directly.

### Quadrennial Tax Exempt Application (M-3) — **unresolved**
- **Cadence:** every four years. Last cycle 2025. Next 2029.
- **Due:** 1 November of the quadrennial year, to the town assessor, under
  CGS 12-81(7)(10)(11) and 12-87a.
- **What appears to have happened:** the CPA warned on 22 October 2025 that M-3
  was due 1 November. On 19 November 2025 Ingrid Lavado-Ponce of the New Haven
  assessor's office wrote about account UID `017402`, noted a zero-asset
  Declaration of Personal Property had been filed, and asked directly whether
  the quadrennial had been filed. **That email is unread and no reply exists in
  the mailbox.** On 1 July 2026 the New Haven Tax Collector was added to Webster
  Bank bill pay.
- **Reading:** the exemption was not renewed, so the city assessed the personal
  property. This is the most likely origin of the property tax bill.
- **Next action:** contact the assessor about a late filing or appeal before
  treating the bill as settled. This obligation was absent from the renewal
  calendar entirely.
- **What it needs when filed:** the assessor's letter, the IRS 501(c)
  determination letter, current bylaws or charter, an itemised list of property
  owned or leased in New Haven, a signed front page of the most recent 990, and
  evidence of compensation paid to officers, directors and employees.

### Declaration of Personal Property
- **Due: 1 November, every year** — separate from the quadrennial, and also
  absent from the renewal calendar.
- **Where:** New Haven assessor, account UID `017402`.
- **Note:** a zero-asset filing was submitted for 2025. Whether that is correct
  depends on the exemption being in force, which is the unresolved item above.

### Contractor 1099-NEC issuance — **needs work before January 2027**
- **Due:** file with the IRS and furnish to recipients by **31 January**. In
  2026 the furnish date fell on **2 February** because of the weekend.
- **Threshold:** $600 or more paid to a contractor in the calendar year, counted
  **across every payment method**, not per platform.

**⚠️ Tax year 2026 is split across two payment systems and neither one can see
the other.**

Contractors were paid through **Gusto** into at least 18 May 2026, and through
**Melio via Xero** from at least 7 July 2026 onward. The changeover sits
somewhere in between; the exact boundary is worth confirming from the ledger.

Each platform issues 1099-NECs only for what **it** paid. A contractor who
received $400 through Gusto and $400 through Melio has been paid $800, which is
over the threshold, and **neither platform will issue a form**, because each
sees only its own half. MakeHaven is the payer and carries the obligation
regardless of what the software does.

**What the annual work actually is, in order:**
1. Pull total 2026 payments per contractor from **both** Gusto and Melio/Xero
   and add them together. The Xero ledger is the one place both can be
   reconciled, since Gusto syncs into it.
2. Identify everyone at $600 or more in aggregate.
3. Check which of those already receive a form from one platform, and which
   need one issued manually or corrected.
4. Confirm a **W-9 with a TIN** is on file for each. In Melio this is collected
   when the contractor "finalizes their receiving method" — the step that blocks
   payment until done. Anyone paid outside that flow may have no W-9 at all.
5. Distribute, and order any platform mailing well before the deadline.

**Gusto's internal deadlines run earlier than the IRS one.** In 2026: forms
available 20 January, **mailing orders due 23 January**, distribution deadline
2 February. Miss the mailing order date and distribution becomes a manual job.

**Also watch:** staff who are paid both as W-2 employees and as contractors for
separate work appear in both systems. Confirm each payment is coded to the right
relationship before the totals are trusted.

- **Evidence:** 2025 forms were produced through Gusto, which covered both
  employees and contractors that year. **2026 has no single source and no
  completed process.** This is the first year the split exists.

---

## 3. Insurance

Broker for all three: **Wellstone Insurance** — Kathleen Daleb,
`kdaleb@wellstoneins.com`, (860) 286-7772.

### Workers' Compensation — **due in days**
- **Renews:** 7 October. Carrier **The Hartford**.
- **2026 renewal:** sent by the broker 14 August 2026 for the 10/7/2026–10/7/2027
  term, limits $500,000 / $500,000 / $500,000. **Unread for five weeks.** JR's
  own daily digest flagged it on 7 and 10 September.
- **On renewal:** review projected payroll, and confirm uncompensated board
  members and officers are excluded via signed CT Workers' Compensation
  Commission forms, or they attract unnecessary premium.
- **Liberty Mutual, resolved as far as mail allows:** it withdraws a premium
  on the **7th of every month**, and sent renewal documents to
  `admin@makehaven.org` on 8 August 2026. A monthly installment on the 7th
  matches this policy's term, so Liberty Mutual is most likely the **current**
  Workers' Comp carrier and The Hartford quote from Wellstone is the renewal.
  Confirm with the broker which one is in force after 7 October, and whether
  the Liberty Mutual auto-pay needs to be stopped.

### Workers' Compensation premium audit — the annual staff-time form
- **Cadence:** once a year, after the policy term ends. The carrier sends a
  payroll audit form asking for actual wages by classification for the expired
  term; the premium is then trued up against the estimate.
- **When:** typically within a couple of months after 7 October. Due roughly
  30 days after it arrives. No copy of the form was found in the mailbox
  sweep; this row exists because JR does it every year.
- **Prepare:** Gusto payroll summary for the term, contractor payments (some
  carriers count uninsured contractors as payroll), and the officer exclusion
  forms.
- **Consequence:** an estimated audit at the carrier's number, usually higher,
  and possible cancellation if ignored.

### General Liability & Commercial Umbrella
- **Renews:** February (Feb–Feb term). Carrier **Philadelphia Insurance (PHLY)**.
- **On renewal:** issue an updated Certificate of Insurance naming
  **770 Chapel Street, LLC** as additional insured. This is a lease obligation,
  not a courtesy.
- **Open coverage gap:** an absolute sexual-misconduct exclusion runs across the
  policies. In February 2026 the board decided to write the policy and put
  practices in place first, then seek the coverage. That decision has no owner
  or date attached to it.

### Directors & Officers / Management Liability
- **Renews:** April (Apr–Apr term).
- **Evidence:** renewed policy received 22 May 2026 and circulated to the board.

---

## 4. Governance and financial

### CPA financial review
- **Window:** April–June. Request list late April, draft mid-June.
- **Vendor:** Zackin Zimyeski Sullivan CPA LLC — Keith Sullivan, Emma West
  (`ewest@zzscpa.com`), Anthony Sinopoli.
- **2025 review:** request list issued 1 July 2026, later than the stated window.
  Still open as of this writing.
- **Prepare:** prior-year bank statements, 1099s, board minutes, fixed asset
  additions and disposals, payroll summaries, adjusting journal entries.
- **Feeds:** the 990, and the attestation on the charity renewal.

### Board conflict-of-interest disclosures
- **Collected:** July, and on onboarding for new directors.
- **Signed at:** `makehaven.org/conflict-interest-policy`.

### Facility lease review
- **Cadence:** annual review / lease term. Landlord 770 Chapel Street, LLC
  (Bernblum), also a member. Maintenance via phone, text, or the
  [ManageBuilding portal](https://bernblum.managebuilding.com/).
- **State: changing.** A lease negotiation is live as of September 2026, with
  outside counsel at MacDermid Reynolds & Glissman engaged on a limited scope
  covering the CPI sticking point.

### CT Cultural District annual report
- **Cadence:** annual, reminders arrive around June.
- **Evidence:** none found. Three reminders in June 2026 are unread. Confirm
  whether this is an obligation MakeHaven carries or one carried by the district.

---

## Known gaps

- **No records-retention policy exists.** It is a Standards of Excellence
  requirement in its own right, it blocks the three-years-of-evidence test for
  the top recognition level, and the DCP charity renewal now assumes three years
  of retained financials.
- **Compliance mail is split across two mailboxes.** The charity renewal and the
  assessor's quadrennial question both went only to `admin@makehaven.org`. The
  daily unread digest reads `jrlogan@makehaven.org`. The two most time-critical
  items of 2026 were invisible to the tool built to catch them.
- **No reminder mechanism with lead times.** Every item above is still triggered
  by an inbound email from the vendor or agency. Two of those emails have now
  been sitting unread past the point where acting on them was easy.
- **No evidence store.** Several rows say "none found" only because confirmations
  live in a mailbox rather than in one place a successor can open.
