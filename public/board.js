/**
 * "What's next" — the one ranked board for all MakeHaven work.
 *
 * Drupal is the system of record (board items are feedback_ledger nodes; wishes
 * are wish nodes) and hands over raw signals at /api/work-board. This file is
 * the ONLY place those signals become a rank, so the weights can be argued
 * about and re-tuned in one commit without a Drupal deploy. The board shows
 * the reasons behind every position, because a rank nobody can see the inputs
 * to is a rank nobody trusts.
 *
 * Design and the reasoning behind the weights: makehaven-website
 * docs/ops/WORK_SYSTEM.md.
 */

/** How many queued items get promoted into "Next up" by score (pins come on
 *  top of this). Small on purpose: "next" that holds 30 things means nothing. */
export const NEXT_UP_SIZE = 8;

/** Unlinked wishes shown in their own section, most-voted first. */
export const WISH_PREVIEW = 8;

export const WEIGHTS = {
  report: 3,        // per submission folded into the item
  important: 2,     // per ▲ (Drupal flag or registry vote)
  wishVotesSqrt: 2, // × √(votes across linked wishes) — 300 votes must not bury everything
  urgent: 10,       // blocks members, money or safety
  brokenProcess: 5, // the item's process is recorded as broken
  agePer4Weeks: 1,  // old things rise slowly…
  ageCap: 6,        // …but not forever
};

const DAY = 86400000;

/**
 * Score one item and say why. Pure: takes the feed item, the wish lookup, the
 * registry's ▲ count for it, and the process manifest.
 */
export function scoreItem(item, { wishById, votes = 0, processById, now = Date.now() }) {
  const reasons = [];
  let score = 0;

  const reports = Math.max(1, item.reports || 1);
  score += WEIGHTS.report * reports;
  reasons.push(reports === 1 ? "1 report" : `${reports} reports`);

  const marks = (item.important || 0) + votes;
  if (marks) {
    score += WEIGHTS.important * marks;
    reasons.push(`▲ ${marks}`);
  }

  const wishVotes = (item.wishes || [])
    .reduce((n, id) => n + ((wishById.get(id) || {}).votes || 0), 0);
  if (wishVotes) {
    score += WEIGHTS.wishVotesSqrt * Math.sqrt(wishVotes);
    reasons.push(`${wishVotes} wish vote${wishVotes === 1 ? "" : "s"}`);
  }

  if (item.urgent) {
    score += WEIGHTS.urgent;
    reasons.push("blocks members, money or safety");
  }

  const proc = item.process ? processById.get(item.process) : null;
  if (proc && proc.state === "broken") {
    score += WEIGHTS.brokenProcess;
    reasons.push("its process is broken");
  }

  const reported = Date.parse(item.reported || "");
  if (!Number.isNaN(reported)) {
    const weeks = Math.floor((now - reported) / (7 * DAY));
    const bump = Math.min(WEIGHTS.ageCap, Math.floor(weeks / 4) * WEIGHTS.agePer4Weeks);
    score += bump;
    if (weeks >= 4) reasons.push(`open ${weeks} weeks`);
  }

  return { score: Math.round(score * 10) / 10, reasons };
}

/**
 * Sort every item into its lane. Returns { now, next, queued, looking, wishes }.
 *  - now:     in_progress, by score
 *  - next:    pinned items first, then the top NEXT_UP_SIZE queued by score
 *  - queued:  the rest of `planned`, by score
 *  - looking: received / reviewing / needs_info, by score
 *  - wishes:  wishes no item claims yet, by votes
 */
export function buildLanes(feed, { itemVotes = new Map(), processes = [], now = Date.now() } = {}) {
  const wishById = new Map((feed.wishes || []).map((w) => [w.nid, w]));
  const processById = new Map(processes.map((p) => [p.pid, p]));

  const scored = (feed.items || []).map((item) => ({
    ...item,
    ...scoreItem(item, { wishById, votes: itemVotes.get(item.nid) || 0, processById, now }),
    linkedWishes: (item.wishes || []).map((id) => wishById.get(id)).filter(Boolean),
    processRow: item.process ? processById.get(item.process) || null : null,
  }));
  const byScore = (a, b) => b.score - a.score || String(a.reported).localeCompare(String(b.reported));

  const lanes = { now: [], next: [], queued: [], looking: [], wishes: [] };
  const queued = [];
  for (const it of scored) {
    if (it.status === "in_progress") lanes.now.push(it);
    else if (it.pinned) lanes.next.push(it);
    else if (it.status === "planned") queued.push(it);
    else lanes.looking.push(it);
  }
  lanes.now.sort(byScore);
  lanes.next.sort(byScore);
  queued.sort(byScore);
  lanes.next.push(...queued.slice(0, NEXT_UP_SIZE));
  lanes.queued = queued.slice(NEXT_UP_SIZE);
  lanes.looking.sort(byScore);

  lanes.wishes = (feed.wishes || [])
    .filter((w) => !w.item)
    .sort((a, b) => b.votes - a.votes || String(b.created).localeCompare(String(a.created)));
  return lanes;
}

/** Open items grouped by registry process id — for the process panel. */
export function itemsByProcess(feed) {
  const out = new Map();
  for (const it of feed.items || []) {
    if (!it.process) continue;
    if (!out.has(it.process)) out.set(it.process, []);
    out.get(it.process).push(it);
  }
  return out;
}

/* ------------------------------------------------------------------ render */

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === "class") n.className = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat()) {
    if (k == null || k === false) continue;
    n.appendChild(typeof k === "string" ? document.createTextNode(k) : k);
  }
  return n;
}

function itemRow(it, n, ctx) {
  const mine = ctx.myVotes.has(it.nid);
  const vote = el("button", {
    type: "button",
    class: `wb-vote${mine ? " on" : ""}`,
    "aria-pressed": mine ? "true" : "false",
    title: mine ? "Remove your ▲" : "This matters to me — move it up",
    onclick: async (e) => {
      e.currentTarget.disabled = true;
      try { await ctx.toggleVote(it.nid); } finally { ctx.rerender(); }
    },
  }, mine ? "▲ Marked" : "▲ Important");

  const meta = [
    el("span", { class: "wb-status" }, it.status_label),
    it.area_label ? el("span", { class: "grp" }, it.area_label) : null,
  ];
  const links = [
    el("a", { href: it.url, target: "_blank", rel: "noopener" }, "Details"),
  ];
  for (const w of it.linkedWishes) {
    links.push(el("a", { href: w.url, target: "_blank", rel: "noopener" }, `Wish: ${w.title}`));
  }
  if (it.processRow) {
    links.push(el("a", { href: `?p=${encodeURIComponent(it.process)}#inventory` }, `Process: ${it.processRow.name}`));
  }

  return el("li", { class: "rank-row wb-row" },
    el("span", { class: "n" }, String(n)),
    el("div", { class: "what" },
      el("b", {}, it.title),
      it.pinned ? el("span", { class: "wb-pin" }, `Pinned${it.pin_reason ? ` — ${it.pin_reason}` : ""}`) : null,
      it.note ? el("em", {}, it.note) : null,
      el("span", { class: "wb-why" }, it.reasons.join(" · ")),
      el("span", { class: "wb-meta" }, meta, " ", links),
    ),
    el("div", { class: "score" }, String(it.score), el("small", {}, "score"), vote),
  );
}

function lane(title, lead, items, ctx, { open = true, start = 1 } = {}) {
  if (!items.length) return null;
  const list = el("ol", { class: "rank wb-list" }, items.map((it, i) => itemRow(it, start + i, ctx)));
  const body = [el("p", { class: "wb-lead" }, lead), list];
  if (open) {
    return el("section", { class: "wb-lane" }, el("h2", {}, title, el("span", { class: "c" }, ` ${items.length}`)), body);
  }
  return el("section", { class: "wb-lane" },
    el("details", {}, el("summary", {}, el("h2", {}, title, el("span", { class: "c" }, ` ${items.length}`))), body));
}

function wishLane(wishes, feed) {
  if (!wishes.length) return null;
  const shown = wishes.slice(0, WISH_PREVIEW);
  return el("section", { class: "wb-lane" },
    el("h2", {}, "Member wishes waiting for a look", el("span", { class: "c" }, ` ${wishes.length}`)),
    el("p", { class: "wb-lead" },
      "Ideas members posted on the website that nobody has turned into a piece of work yet. ",
      "Votes count: when staff pick one up it joins the board above with its votes. ",
      el("a", { href: feed.wish_url, target: "_blank", rel: "noopener" }, "Post a wish"), "."),
    el("ul", { class: "rank wb-list" }, shown.map((w) =>
      el("li", { class: "rank-row wb-row" },
        el("span", { class: "n" }, "♡"),
        el("div", { class: "what" },
          el("a", { href: w.url, target: "_blank", rel: "noopener" }, el("b", {}, w.title)),
          el("span", { class: "wb-meta" },
            el("span", { class: "wb-status" }, w.status_label),
            w.type_label ? el("span", { class: "grp" }, w.type_label) : null)),
        el("div", { class: "score" }, String(w.votes), el("small", {}, w.votes === 1 ? "vote" : "votes"))))),
    wishes.length > shown.length
      ? el("p", { class: "wb-lead" }, el("a", { href: feed.wish_url.replace(/\/node\/add\/wish$/, "/wishes/top"), target: "_blank", rel: "noopener" },
          `All ${wishes.length} open wishes →`))
      : null);
}

/**
 * Render the board into `root`. ctx = { feed, processes, itemVotes: Map nid→n,
 * myVotes: Set nid, toggleVote(nid), rerender() }.
 */
export function renderBoard(root, ctx) {
  const lanes = buildLanes(ctx.feed, { itemVotes: ctx.itemVotes, processes: ctx.processes });
  root.textContent = "";
  let n = 1;
  const add = (node, count) => { if (node) root.appendChild(node); n += count; };

  add(lane("Being worked on now", "Someone has this in hand.", lanes.now, ctx, { start: n }), lanes.now.length);
  add(lane("Next up",
    `What gets picked up next: anything staff pinned, then the ${NEXT_UP_SIZE} highest-scoring queued items. ` +
    "The score adds up reports, ▲ marks, wish votes, urgency and how long it has waited — the reasons are under each item.",
    lanes.next, ctx, { start: n }), lanes.next.length);
  add(lane("Queued", "Decided we will do it, not yet scheduled. Mark ▲ on the ones that matter to you and they move up.",
    lanes.queued, ctx, { open: false, start: n }), lanes.queued.length);
  add(lane("Being looked at", "Logged and under review — not decided yet.",
    lanes.looking, ctx, { open: false, start: n }), lanes.looking.length);
  add(wishLane(lanes.wishes, ctx.feed), 0);

  root.appendChild(el("p", { class: "wb-foot" },
    "Something missing or wrong? ",
    el("a", { href: ctx.feed.report_url, target: "_blank", rel: "noopener" }, "Tell us"),
    " · ",
    el("a", { href: ctx.feed.board_mine_url, target: "_blank", rel: "noopener" }, "The things you reported"),
    ` · Updated ${new Date(ctx.feed.generated).toLocaleString()}`));

  const count = document.getElementById("wbtab-count");
  if (count) count.textContent = String(lanes.now.length + lanes.next.length);
}
