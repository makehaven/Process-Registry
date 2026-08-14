# Round 1 Questions — reducing `undefined` and `unknown`

_2026-08-14. For JR. 90 of 186 rows are `undefined` or `unknown`; these questions
target them in rough order of leverage._

## How to answer

**Answer by number, skip freely, and be terse.** "Q14 — nobody, never happens"
is a complete and useful answer. Where I have guessed, the guess is in
*italics* — confirming or correcting it takes two words.

Sections **U** and **A** are the high-leverage ones; if you only do those,
roughly half the unknowns resolve. Sections B–H can come later or in pieces.

Three answer shapes recur:

- **A-score** — A1 tribal / A2 documented, done by hand / A3 tooling helps, human
  drives each one / A4 runs itself, humans handle exceptions / A5 runs itself and
  tells us when it breaks
- **Owner** — a name. "Nobody" is a real and important answer.
- **Real / aspiration** — is this a thing we do badly, or a thing we have never
  started? The registry currently conflates them.

---

## U — Unlock questions (each resolves many rows at once)

**U1. Staff and contractors, right now.** Name, title, paid/volunteer, and the
two or three things each person owns end to end. This single answer fills
roughly forty owner fields and lets me infer a lot of A-scores.

JR: We have almst everyone in our CRM database. our main volunteers are faciliators. I have moved our contractors, mostly instructors to use the dashboard that is starting and there is a nice intergration to xero so the hours are paid. Still working on refining buit it is working.

**U2. Which of these does anyone actually use, and how often?** For each:
*daily / weekly / monthly / rarely / never / never launched.*

| Tool | My guess |
|---|---|
| Governance-Dance (board governance app) | Never used, just now developed as experiment |
| Inventory-App | Used every month, staff love it well developed |
| Phonebank-Tool | Used once for fundraisr expeiment, well liked future potentioal use at next phonathon |
| Grant-Researcher | Activly using shoudl show sevearl grants submitted to it, liked to civicrm |
| Sponsorship-Tool | IN use but just starting, still in development but bones are there, hired contractor to do outreach |
| Entrepreneurship Nexus | Experimental, usign on very light level with hope of future development |
| Entrepreneur AI support assistant | Early expeimental non critical, optinal |
| Voicemail-Tool | Just created this week, pre launch, plan to use |
| Tool-expert chatbot | Lunached on limited basis, woudl like to see more development in feedback loop. |

**U3. The recurring calendar.** What genuinely happens on a fixed schedule?
Daily / weekly / monthly / quarterly / annually. Anything on this list that
isn't already in the registry is a process I've missed entirely.

**U4. Open and close.** Is the space staffed, and during what hours? What
happens at open and at close, who does it, and is any of it written down?
(Standards S017 asks for opening, closing, lone-work, impairment and
after-hours protocols — I found none.)

JR: space is 24 hours, not staffed we trust our memebrs and use RFID access. Should all be on about page and in https://www.makehaven.org/membership-agreement

**U5. Committees.** Which exist on paper, which actually meet, and who chairs
each? I know the DEI committee has no active members; I don't know about the
others. 

JR: we have commiteees here: https://www.makehaven.org/volunteer-leadership-structure DEI is now active and meeting. I could use a system (maybe governance dance to keep better track of who is actually on each)

**U6. Standards of Excellence profile.** The workbook's Profile sheet is
unfilled, so every conditional module defaults to "No" — which currently
switches off four modules that plainly apply to MakeHaven. Confirm:

JR: standards of excillence is in development and i hope to collaborate with other makerspaces on it.

| Profile question | Sheet says | Should it be? |
|---|---|---|
| Lends tools for off-site use? | No | *Yes — the lending library* |
| Serves minors under 18? | No | *Yes? — not as members, but several programs in partnerships with schools* |
| Supports business incubation or production? | YEs | *Yes — incubator workspaces, try to develop programs to support produict development* |
| Hosts repair cafés or salvage programs? | No | *Yes? — Repair Fair, Precious Plastic* We are doing a little we had a big grant to do more but it got canceled by trump, so now we do what we can. We have preciious plastics equipment |
| Rents desks, studios, bays, or storage? | No | *Yes — storage + workspace rentals* yes we are active in doing this. |
| At least 3 years of retained records? | No | we dont yet have a retention policy. Somthign to do |

Fixing this takes applicable standards from 52 to roughly 75, and four of the
five extension modules are ones we'd currently score badly on.

---

## A — Safety, insurance and continuity (highest impact — I5 rows)

**A1.** Insurance and lease renewals: who handles them, what month do they fall,
and is there any reminder mechanism or is it memory? Broker name?

JR: I as executive director handle these. I woudl like to develop some app or software that checks timing. There are lots of other reporting requiremetns for the state (annaul report, fundiraising license ans so on) All basicly i get an email and then I renew. But it would be better to be more proactive, maybe eventually AI can help to do filings (or draft) and we can be intentional about collecting that data as we go.

**A2.** Has anyone **ever restored** from a backup — Pantheon, CiviCRM, the
local access-control box, or the Firebase projects? A backup nobody has
restored from is a hope, not a process.

JR: Yes, I have doen restores. also built lcoal coplies on machienes and had other people do the same.

**A3.** Besides you, who can administer Drupal/Pantheon, CiviCRM, Chargebee,
Stripe, Xero, the Firebase projects, Home Assistant, and the domain registrar?
Per service if it varies. This is the bus-factor question in its purest form.

JR: Terence our board member and Yan have access to panteheon and have setup clones of site. Kate is admin on chargebee and stripe. Kevin (tresuer on xero), Firebase I think is just me but using my makehaven accoount so could be accessed and reset by org. Home assistant is Vincent (shop tech volunteer and corey). Domain login via org email. There are different answers but all shoudl be reoverabe from peopel or by taking cotrol of my work email.

**A4.** Incident reports: roughly how many in the last 12 months? Which board
committee reviews them, how quickly, and does the reporter ever hear back?

JR: We have a safety and accessablity committee (we shoudl think about accessablity review and imrpovement processs) We review quarterly at our meetings. We have paper copies (that we input to the online form) the submitted concerns got to a list of volunteers and staff who review at the quarterly meeting.

**A5.** Safety program: is there a written plan beyond the Safety Program
Summary doc? Have emergency drills ever been run? When was the plan last
reviewed?

JR: The summary doc, and the tool levels is the main thing. Other stuff is embeded in the badging system and membership agreement.

**A6.** Chemical inventory and SDS access — does either exist? *(Standards S013,
Tier 1 critical. I found nothing.)*

JR: we have special cabnets and we have a binder with the stuff printed we most often use (although could be reviewed). Our usage policy is at makehaven.org/air we have air montors to verify air conditions.

**A7.** How is an unsafe tool taken out of service today, and what has to happen
before it comes back? Is there a physical lockout, or is it a sign and an
honour system? *(Standards S033, Tier 1 critical.)*

JR: we have signs that anyone can put on a tool. There are buttons on every tool page to also report an issue. We have locks that go on cords to lock out tools (implemented by staff). When the access control system for tools is back we can lock those tools out remotly. 

**A8.** Is there any routine walk-through inspection of the shop — egress,
guards, ventilation, housekeeping? *(S036.)*

JR: Yes, the safety and accessablity comimttee does one walk through each year for general safety. They do another for accessablity. 

**A9.** Hazardous waste and paint/solvent disposal: what actually happens, and
who arranges it?

JR: This we just tell membrs to take care of it themselves. Probably somthing to look at.

**A10.** Are there minors on site at present, under which MOUs, and is anyone
background-screened? *(Standards module B applies if yes.)*

JR: As guests of guardians, yes. Also partnership with schools like St.martain depors but they have a instructor from teh school supervising so we are not custodians of students.

---

## B — Facilities and equipment

**B1.** Preventive maintenance: does any PM schedule exist, or is it
run-to-failure with tasks raised when something breaks?

JR: Sort of. Our shop manager made a list of tasks for the shop tech in a spreadsheet. This was gign to maybe be formalized into /tasks but that is a work in progress. We would like to empower members, but only do so for people who are techncially able which means building out a system to regulat who can repair. 

**B2.** The previous tool-downtime tracking attempt — what actually killed it?
Too many exceptions to model, nobody entering data, or no one reading the
output? This determines whether a second attempt is worth anything.

JR: I thoght we were activly using it at https://www.makehaven.org/admin/content/asset-maintenance Members can report and that data feeds into oru kpis. We also have https://www.makehaven.org/admin/reports/tool-quality to make sure things are setup right.

**B3.** Who calls the landlord about elevators, HVAC, flooding and leaks? Is
there any log or ticket trail, or is it phone calls?

JR: This is both shop manager and executive director. Mostly shop manager but if things dont happen its director. This is pretty informal. Landlord is in 80s and on site and forgetfull. So its a challange. They did create a system for submitting tickets which is ok, but they normally need a text message and a remidner or two.

**B4.** Consumables: who notices something has run out, and who buys it?

JR: the store material pages allow members to metnion somethign is out. Some materials in space also have qre codes where theis can be metnioned that goes to a webform and tells the operation manager to reorder. Also there is a inventory of store and threholds to reoder. This syustem could be refined. The "free" supplies that are out in the space could benfit from more of a system possibly. 

**B5.** Tool acquisition: who decides what to buy, on what basis, and who
commissions it, writes the SOP, and creates the badge?

JR: There is the overall budget first. THen there is the wishlist. After that we talk to the area experts. The final decision is between shop manager and executive director. 

**B6.** Cleaning: staff, contractor, volunteers, or members?

JR: we have a contract who is a member. We have a signed corntract.

**B7.** Is there an asset register with location, status and a responsible lead
per major tool? *(S032, Tier 1 critical.)* I know `asset_status` exists — does
it actually carry a named lead per tool?

JR: Yes. many of these answers can be found from the tools at https://www.makehaven.org/staff-tools In this case its http://makehaven.org/asset/inventory

---

## C — Governance and people

**C1.** Board: how many voting directors, how often does it meet, are approved
minutes retained, and where do they live?

JR: Updatd at https://www.makehaven.org/team Meet quarterly. plus committees. Yes minutes are in google drive. Maybe eventually in board dance.

**C2.** Conflict-of-interest annual disclosure — when was it last collected?
Bylaws and policies — when last reviewed?

JR: Yes at: https://www.makehaven.org/conflict-interest-policy Policies are documented in /operations

**C3.** Has a board self-assessment ever been completed?

JR: Its been a while we are workign on one now. https://www.makehaven.org/survey/board

**C4.** Who prepares the board packet, how far ahead, and from what sources?

JR: Its me as executive director. From Xero, my own google docs  and the /kpi report.

**C5.** Is there any written succession or emergency-authority plan — for the
board and for you specifically?

JR: Not really we should work on this.

**C6.** Staff: current job descriptions? Employee handbook? Do annual
evaluations happen? *(S046–S048.)*

JR: yes we do annual evenuation and review the job descriptions then. They are in google drive.

**C7.** Who files the 990 and the state registrations, and when are they due?

JR: I do it as director with help of CPA who does review. We did exetention so I think OCtober. I was late last year and got fined. 

**C8.** Titled volunteers: roughly how many, and who keeps the list?

JR: Facililitators, shop techs, lending librarien, Ambasitors, board members, committeee members. maybe 75+

**C9.** Member discipline: roughly how many warnings and terminations in the
last 12 months, who decides, and is anything logged?

JR: Not sure in the last months. Started trying to add to civicrm. Was working out of spread sheet. Its not many but it is important. This sia good candidate for a app that is on its own but connected to crm system so its easy to send and track dicipline.

**C10.** Harassment complaints: where does one go, who investigates, and is
there a record? *(A public policy exists; the intake is invisible.)*

JR: It goes to http://makehaven.org/harassment a google form so we have more privacy contorl. We get an email and try to act on it right away. 

---

## D — Membership and member experience

**D1.** When a member quits, what actually happens — door badge, storage,
Slack, CiviCRM, Chargebee? Is any of it automatic?

JR: They get directed to Chargebee. They cancel there. THe sync module then removes the member role and that changes their door access. THey are asked in chargebee the reason and that snycs to drupal/crm. If the payment just failes they go to dunning. Then the member success process. https://www.makehaven.org/admin/makerspace/member-success/dashboard

**D2.** Does an exit survey exist? Roughly what share of leavers complete it?

JR: Yes, it goes from chargeee to profile. Check there or KPIs for number.

**D3.** Comped, sliding-scale and scholarship memberships: roughly how many, and
who approves each?

JR: people fillin the join form and self certify with a online signature.

**D4.** When were prices last changed, and who decides?

JR: Board has polciy we now change by default each year related to inflation. Executive director has authroity.

**D5.** Is the member NPS survey a real recurring thing, or was 89.0 a one-off?

JR: yes we have done surveys to members with NPS for years. tryign to make that process mroe intergrated to site and autmatic, somthing i should cehck back in on.

**D6.** Does anything happen for new members socially — gatherings, peer
intros, mentorship — or is that entirely aspirational right now?

JR: yes lots of social events and meetups. but old mentorship program fell apart and is dorment. 

**D7.** Community Wishlist — does this exist in any form today?

JR: Yes please look at /wishes

---

## E — Education

**E1.** Who schedules classes, how far ahead, and how is the calendar decided —
instructor availability, demand, or ad hoc?

JR: Education manager hires a contractor silas that does it now. I have in pipline to make it as self serve (particularly for repeat instructrors) as possible 

**E2.** Instructor stipends: how does an instructor actually get paid, and who
approves it?

JR: After the class on the instructror dashboard they submit their hours. THat gets imported to xero/meilio and staff approve.

**E3.** Is GEMS running right now? Who runs it?

JR: Yes, check the event listing it has the detials.

**E4.** Who writes badge quizzes, and who checks them? *(Two agreement-quiz
questions currently contradict our own docs.)*

JR: Mostly our shop manager. We have a badge quality reprot and work to do there: https://www.makehaven.org/admin/reports/badge-quality

**E5.** Does anyone review class evaluation trends, or do they accumulate
unread?

JR: Education manager says they review when we get them but I think we cna do much better to aggrigate and actually to get people todo the evaluations.

**E6.** Which youth/school partnerships are active this year?

JR: I would havbe to check is a number of them. We follow these policies https://www.makehaven.org/makehaven-youth-safety-policies

---

## F — Entrepreneurship

**F1.** How many incubator desks/bays exist, how many are occupied, and who
decides who gets one?

JR: THey apply. Director decieds by application. Go to /workspaces to see our workspaces and avaiblity.

**F2.** Is there anyone playing the entrepreneurship-coordinator role today,
even informally?

JR: I do as director but dont have time for it. I would love to have volunteers and or a contractor do more to growth the program.

**F3.** Is any cohort programme running, or is that entirely dormant?

JR: THere are not enterprenur cohors now. 

**F4.** Does anything happen when a member ticks "inventor" or "entrepreneur" at
signup — 46% of joins do — beyond the dashboard nudge?

JR: Not a lot. The system is developing that they are invited to larger enterprenur nexus that shoudl connect them to other resources but that is under developed and under used at this point. We also might search and filter by that to reach out when we do craft markets and so on. I use that data for grants.

---

## G — Finance and development

**G1.** Is "0 grants submitted YTD" accurate? Who writes grants now?

JR: Thats wrong. we did submit and should be in Civicrm and in KPI data. 

**G2.** Did the spring and year-end appeals run in 2025, and who ran them?

JR: Resource development commitete and Kate as staff lead

**G3.** Roughly how many $1,000+ donors are there, and who stewards them?

JR: You can see in reports and civicrm. And staff do, we can build that system a bit we do sometimes involve board.

**G4.** Monthly close: who does the bookkeeping, on what cadence, and who
reviews it?

JR: Contractror does entery, Execytive director does harder work. Finance commitee volunteers help with harder things. Then we have CPA for review and 990.

**G5.** Does the board approve an annual budget, and does it see budget-vs-actual
regularly? *(S040, Tier 1 critical.)*

JR: Yes they do an annual budget and I have reports regularly on budget actual progress.

**G6.** When was the last independent financial review or audit, and is one
legally required at our revenue level?

JR: Last year. and all our docs are with them for this year review.

**G7.** Who manages the reserve, and is there a written investment policy?

We have a finance policy and executive director manages: https://www.makehaven.org/makehaven-procurement-policy https://www.makehaven.org/makehaven-financial-policies-and-procedures

**G8.** Are financial duties separated at all — receipts, payments, payroll,
reconciliation — or does that all run through one or two people? *(S041, Tier 1
critical.)*

JR: Most of them are with executive director and checked by finance committee. Operations manager has access to most too. Somthing we can continue to develop.

---

## H — Outreach and communications

**H1.** Who gives tours, how are they booked, and roughly how many per week?

JR: alls taff on on tour schedule /tour We are thinking about making this somethign more volunteer core does.

**H2.** After a guest signs a waiver, does *anything* happen? (2.4% convert
against a 5% goal, on 218 waivers.)

JR: It shoudl go into CRM, and put on email list. Need to check.

**H3.** Does the referral programme actually run? Roughly how many referrals a
year, and is the incentive paid?

JR: Yes, peopel refer, but this is a area for techncial process improvement its a bit manual now.

**H4.** Is there an ambassador programme in any form today?

JR: not really just an idea. and some regular volunteers. 

**H5.** Who answers the phone right now, and who monitors info@

JR: this is a weak point. mostly it goes to google voicemail box and often unanswerd for long time becuase of staff capacity Thats why working on app to help. Info goes to google shared inbox and mostly answered by kate. Looking for ways to make better since staff struggle to keep up.

**H6.** Who publishes website content, and is there any editorial calendar?

JR: anyone on staff can. No calendar. Want to step up blog and annoucements that can also feed the automatic newsletter (new developing initative.)

**H7.** Has an annual report ever been produced? When was the last one?

JR: thaere is an annual memeber meeting that has a powerpoint and presnetation recorded. We have used a PDF of that presnetation as annual report when asked.

---

## What I'll do with the answers

Update the seed inventory, re-score the affected rows, and republish. Anything
that turns out to be a process I've missed entirely gets added; anything that
turns out to be aspiration rather than operation gets flagged `planned` so the
page stops reading as an indictment.

Rows you can't answer are also a result — "nobody knows" is exactly what the
bus-factor view is for.
