/**
 * Participation layer: Drupal sign-in, votes on the Next ranking, comments on
 * any process.
 *
 * The registry is a static page rebuilt from data/inventory.md, so nothing here
 * changes what the build produced. Votes and comments live in Firestore and are
 * applied to the DOM after load. If Firebase is unreachable, or the deployment
 * has no OAuth consumer yet, the page stays exactly as built — the ranking still
 * renders, it just does not move. Participation is additive, never load-bearing.
 *
 * Identity comes from Drupal via the makerspace_firebase_auth bridge: OAuth2
 * PKCE against makehaven.org, then a custom token swapped for a Firebase
 * session. That means a vote carries a real account rather than a typed-in name,
 * and Firestore rules can check request.auth.uid without trusting the client.
 */
import {
  DRUPAL_BASE_URL, OAUTH_CLIENT_ID, OAUTH_SCOPE, FIREBASE_APP_ID,
  FIREBASE_CONFIG, VOTE_CAP,
} from "./registry-config.js";

const SDK = "https://www.gstatic.com/firebasejs/12.11.0";

/* ---------------------------------------------------------------- OAuth PKCE */
/* Ported from Sponsorship-Tool/src/auth.ts, which is the working reference for
 * this flow. Kept as plain functions rather than a class because the whole
 * lifecycle here is: log in, hold a token, refresh it once on 401. */

const LS = {
  verifier: "pr.code_verifier",
  access: "pr.access_token",
  refresh: "pr.refresh_token",
  returnTo: "pr.return_to",
};

function randomString(len) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
  const bytes = new Uint8Array(len);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => chars[b % chars.length]).join("");
}

function base64url(buf) {
  let s = "";
  for (const b of new Uint8Array(buf)) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function challengeFor(verifier) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier));
  return base64url(digest);
}

/** The redirect URI has to match the Drupal consumer exactly, so it is derived
 *  from the origin and never carries a query string or hash. */
function redirectUri() {
  return window.location.origin + window.location.pathname;
}

async function login() {
  const verifier = randomString(96);
  sessionStorage.setItem(LS.verifier, verifier);
  // Which tab the user was on, so signing in does not dump them back on Overview.
  sessionStorage.setItem(LS.returnTo, window.location.hash || "");
  const url = new URL(`${DRUPAL_BASE_URL}/oauth/authorize`);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("client_id", OAUTH_CLIENT_ID);
  url.searchParams.set("redirect_uri", redirectUri());
  url.searchParams.set("code_challenge", await challengeFor(verifier));
  url.searchParams.set("code_challenge_method", "S256");
  url.searchParams.set("scope", OAUTH_SCOPE);
  window.location.href = url.toString();
}

async function exchange(params) {
  const res = await fetch(`${DRUPAL_BASE_URL}/oauth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(params).toString(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.error) {
    throw new Error(data.error_description || data.error || `token exchange failed (${res.status})`);
  }
  localStorage.setItem(LS.access, data.access_token);
  if (data.refresh_token) localStorage.setItem(LS.refresh, data.refresh_token);
  return data.access_token;
}

/** Consume ?code= if we have just come back from Drupal. Returns true if this
 *  page load was a login callback, so the caller knows to restore the tab. */
async function completeLoginIfCallback() {
  const url = new URL(window.location.href);
  const code = url.searchParams.get("code");
  if (!code) return false;
  const verifier = sessionStorage.getItem(LS.verifier);
  // Strip the code before anything can go wrong with it — an authorization code
  // left in the address bar gets copied, pasted and shared.
  url.searchParams.delete("code");
  url.searchParams.delete("state");
  const back = sessionStorage.getItem(LS.returnTo) || "";
  history.replaceState({}, "", url.pathname + (url.search === "?" ? "" : url.search) + back);
  sessionStorage.removeItem(LS.verifier);
  sessionStorage.removeItem(LS.returnTo);
  if (!verifier) throw new Error("Login could not be completed — please try again.");
  await exchange({
    grant_type: "authorization_code",
    client_id: OAUTH_CLIENT_ID,
    code,
    redirect_uri: redirectUri(),
    code_verifier: verifier,
  });
  return true;
}

async function refreshAccessToken() {
  const rt = localStorage.getItem(LS.refresh);
  if (!rt) return null;
  try {
    return await exchange({
      grant_type: "refresh_token",
      client_id: OAUTH_CLIENT_ID,
      refresh_token: rt,
    });
  } catch {
    return null;
  }
}

function forgetDrupal() {
  localStorage.removeItem(LS.access);
  localStorage.removeItem(LS.refresh);
}

/* --------------------------------------------------------- Firebase bridging */

const state = {
  fb: null,        // { auth, db, api }
  user: null,      // Firebase user
  profile: null,   // { uid, name, roles, staff }
  votes: new Map(),      // pid -> { up, down, mine }
  comments: new Map(),   // pid ("__general__" for site-wide) -> [comment, …]
  processes: [],
  ready: false,
};

async function loadFirebase() {
  if (state.fb) return state.fb;
  const [app, auth, store] = await Promise.all([
    import(`${SDK}/firebase-app.js`),
    import(`${SDK}/firebase-auth.js`),
    import(`${SDK}/firebase-firestore.js`),
  ]);
  const a = app.initializeApp(FIREBASE_CONFIG);
  state.fb = { auth: auth.getAuth(a), db: store.getFirestore(a), api: { ...auth, ...store } };
  return state.fb;
}

/** Swap the Drupal access token for a Firebase session. One retry after a
 *  refresh, because an expired Drupal token is the ordinary case here — people
 *  leave this page open. */
async function signInToFirebase() {
  let token = localStorage.getItem(LS.access);
  if (!token) return null;

  const fetchCustomToken = async (bearer) =>
    fetch(`${DRUPAL_BASE_URL}/api/firebase-token/${FIREBASE_APP_ID}`, {
      headers: { Authorization: `Bearer ${bearer}` },
    });

  let res = await fetchCustomToken(token);
  if (res.status === 401) {
    token = await refreshAccessToken();
    if (!token) { forgetDrupal(); return null; }
    res = await fetchCustomToken(token);
  }
  if (!res.ok) {
    // 404 means the app is not registered in the bridge yet — a setup step, not
    // a user error, so say so plainly rather than looping on sign-in.
    const detail = res.status === 404
      ? "the registry is not registered with the Drupal Firebase bridge yet"
      : `the sign-in bridge returned ${res.status}`;
    throw new Error(`Could not start a session — ${detail}.`);
  }
  const { token: customToken } = await res.json();
  const { auth, api } = await loadFirebase();
  const cred = await api.signInWithCustomToken(auth, customToken);
  return cred.user;
}

/**
 * Ask Drupal who this is.
 *
 * Nothing in the Firebase session carries a name: the bridge mints role claims
 * and a uid and nothing else, and signInWithCustomToken leaves displayName null
 * because there is no provider profile behind a custom token. Without this every
 * comment files as "Unknown" — for everyone, not just accounts that lack a name —
 * and digest.py has no way to recover the author afterwards.
 *
 * The `profile` scope is already requested at /oauth/authorize and this origin is
 * already in Drupal's CORS allow-list, so this needs no server change. Failure is
 * deliberately silent: an unnamed comment is worth more than a blocked sign-in.
 */
async function drupalDisplayName() {
  const token = localStorage.getItem(LS.access);
  if (!token) return null;
  try {
    const res = await fetch(`${DRUPAL_BASE_URL}/oauth/userinfo`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) return null;
    const info = await res.json();
    return info.name || info.preferred_username || null;
  } catch {
    return null;
  }
}

async function buildProfile(user) {
  const res = await user.getIdTokenResult();
  const c = res.claims || {};
  return {
    uid: user.uid,
    name: c.name || c.display_name || user.displayName
      || (await drupalDisplayName()) || "Unknown",
    // The bridge maps Drupal roles to claims. Which ones exist is deployment
    // config, so read whatever is there rather than hard-coding a list.
    roles: Object.keys(c).filter((k) => c[k] === true && !RESERVED.has(k)).sort(),
    staff: c.staff === true || c.admin === true,
  };
}

const RESERVED = new Set(["email_verified", "iss", "aud", "auth_time", "sub", "iat", "exp", "firebase"]);

/* ------------------------------------------------------------------- storage */

async function loadVotes() {
  const { db, api } = await loadFirebase();
  const snap = await api.getDocs(api.collection(db, "votes"));
  const tally = new Map();
  snap.forEach((d) => {
    const v = d.data();
    if (!v || !v.processId) return;
    const t = tally.get(v.processId) || { up: 0, down: 0, mine: 0 };
    if (v.value === 1) t.up += 1;
    else if (v.value === -1) t.down += 1;
    if (state.profile && v.uid === state.profile.uid) t.mine = v.value;
    tally.set(v.processId, t);
  });
  state.votes = tally;
}

/** One document per person per process, keyed so a second vote overwrites the
 *  first. Nobody can vote twice and changing your mind is a normal edit. */
async function castVote(pid, value) {
  const { db, api } = await loadFirebase();
  const p = state.profile;
  const row = state.processes.find((x) => x.pid === pid);
  const ref = api.doc(db, "votes", `${p.uid}__${pid}`);
  const t = state.votes.get(pid) || { up: 0, down: 0, mine: 0 };

  if (t.mine === value) {           // clicking the same arrow again clears it
    await api.deleteDoc(ref);
    if (value === 1) t.up -= 1; else t.down -= 1;
    t.mine = 0;
  } else {
    await api.setDoc(ref, {
      processId: pid,
      processName: row ? row.name : pid,
      group: row ? row.group : null,
      value,
      uid: p.uid,
      name: p.name,
      roles: p.roles,
      updatedAt: new Date().toISOString(),
    });
    if (t.mine === 1) t.up -= 1;
    if (t.mine === -1) t.down -= 1;
    if (value === 1) t.up += 1; else t.down += 1;
    t.mine = value;
  }
  state.votes.set(pid, t);
  applyVotes();
}

async function sendComment({ pid, kind, text }) {
  const { db, api } = await loadFirebase();
  const p = state.profile;
  const row = pid ? state.processes.find((x) => x.pid === pid) : null;
  const id = `c-${Date.now()}-${randomString(6)}`;
  await api.setDoc(api.doc(db, "feedback", id), {
    id,
    processId: pid || null,
    processName: row ? row.name : null,
    group: row ? row.group : null,
    state: row ? row.state : null,
    kind,
    text: text.trim().slice(0, 4000),
    uid: p.uid,
    name: p.name,
    roles: p.roles,
    status: "new",
    createdAt: new Date().toISOString(),
  });
  await loadComments();
}

/** Comments are readable by every signed-in member, so they are loaded and shown
 *  rather than filed away. A suggestion box nobody can see into gets the silence
 *  it was built to fix. */
async function loadComments() {
  const { db, api } = await loadFirebase();
  const snap = await api.getDocs(api.collection(db, "feedback"));
  const byPid = new Map();
  snap.forEach((d) => {
    const c = d.data();
    if (!c || !c.text) return;
    const key = c.processId || "__general__";
    if (!byPid.has(key)) byPid.set(key, []);
    byPid.get(key).push(c);
  });
  byPid.forEach((list) => list.sort((a, b) =>
    (b.createdAt || "").localeCompare(a.createdAt || "")));
  state.comments = byPid;
  paintCommentCounts();
}

/** A count on the button is what tells someone there is anything to read. */
function paintCommentCounts() {
  document.querySelectorAll("[data-pid]").forEach((el) => {
    const n = (state.comments.get(el.dataset.pid) || []).length;
    el.querySelectorAll(".rowsay, .vt.say").forEach((b) => {
      b.textContent = n ? `Comments ${n}` : "Comment";
      b.classList.toggle("has", n > 0);
    });
  });
}

/* ------------------------------------------------------------------ ranking  */

/**
 * Re-score and re-sort the Next tab.
 *
 * The base score stays visible next to the adjustment so nobody has to guess why
 * a row moved — a participatory ranking that cannot be audited is just a ranking
 * people distrust more slowly.
 */
function applyVotes() {
  const list = document.getElementById("rank-list");
  if (!list) return;
  const rows = Array.from(list.querySelectorAll(".rank-row"));
  if (!rows.length) return;

  // Three inputs, kept separate so the row can show its own arithmetic:
  // the scores, what the strategic plan committed to, and what people voted.
  const scored = rows.map((el) => {
    const pid = el.dataset.pid;
    const base = Number(el.dataset.base);
    const plan = Number(el.dataset.plan) || 0;
    const t = state.votes.get(pid) || { up: 0, down: 0, mine: 0 };
    const net = t.up - t.down;
    const adj = Math.max(-VOTE_CAP, Math.min(VOTE_CAP, net));
    return { el, pid, base, plan, t, adj,
             final: base + plan + adj, was: Number(el.dataset.rank) };
  });

  scored.sort((a, b) =>
    b.final - a.final || b.adj - a.adj || a.was - b.was);

  scored.forEach((s, i) => {
    const now = i + 1;
    s.el.querySelector(".n").textContent = String(now).padStart(2, "0");
    s.el.querySelector(".final").textContent = String(s.final);

    const adjEl = s.el.querySelector(".adj");
    adjEl.textContent = s.adj ? ` ${s.adj > 0 ? "+" : "−"}${Math.abs(s.adj)}` : "";
    adjEl.className = "adj" + (s.adj > 0 ? " up" : s.adj < 0 ? " down" : "");

    const box = s.el.querySelector(".vote");
    if (box) {
      box.hidden = !state.ready;
      box.querySelector(".up .c").textContent = s.t.up;
      box.querySelector(".down .c").textContent = s.t.down;
      box.querySelector(".up").classList.toggle("on", s.t.mine === 1);
      box.querySelector(".down").classList.toggle("on", s.t.mine === -1);
      const cue = box.querySelector(".movecue");
      const delta = s.was - now;
      cue.textContent = delta > 0 ? `moved up ${delta}` : delta < 0 ? `moved down ${-delta}` : "";
    }
    list.appendChild(s.el);   // reorder in place
  });

  reapplyRankTail();
}

/** The build hides everything past the first 30 behind a "show more" button.
 *  After a re-sort the visible set has to be recomputed, or re-ordering would
 *  quietly reveal rows the button still claims are hidden. */
function reapplyRankTail() {
  const list = document.getElementById("rank-list");
  const more = document.getElementById("rank-more");
  if (!list || !more) return;
  const expanded = more.getAttribute("aria-expanded") === "true";
  // How many the build chose to show; kept in one place so the two cannot drift.
  const shown = Number(more.dataset.shown) || 30;
  Array.from(list.querySelectorAll(".rank-row")).forEach((el, i) => {
    const tail = i >= shown;
    el.classList.toggle("rank-extra", tail);
    el.hidden = tail && !expanded;
  });
}

/* ----------------------------------------------------------------------- UI  */

const $ = (id) => document.getElementById(id);

function setAuthBar(status, detail) {
  const bar = $("authbar");
  if (!bar) return;
  bar.dataset.status = status;
  const who = $("authwho");
  const btn = $("authbtn");
  if (status === "in") {
    who.textContent = `${state.profile.name}${state.profile.staff ? " · staff" : ""}`;
    btn.textContent = "Sign out";
  } else if (status === "busy") {
    who.textContent = detail || "Signing in…";
    btn.hidden = true;
  } else if (status === "off") {
    // Configured-off, or the bridge is unreachable. Offering a button that
    // cannot work is worse than offering none, so say why and stop.
    who.textContent = detail || "Participation is not available right now";
    btn.hidden = true;
  } else {
    who.textContent = detail || "Sign in with your MakeHaven account to vote and comment";
    btn.textContent = "Sign in";
    btn.hidden = false;
  }
}

function openPanel(pid) {
  if (!state.ready) { login(); return; }
  const panel = $("fbpanel");
  const sel = $("fbproc");
  sel.value = pid || "";
  $("fbdone").hidden = true;
  $("fbform").hidden = false;
  $("fberr").hidden = true;
  panel.hidden = false;
  $("fbpill").setAttribute("aria-expanded", "true");
  renderThread(sel.value);
  setTimeout(() => $("fbtext").focus(), 40);
}

const KIND_LABEL = {
  correction: "Says this is wrong",
  changed: "Says they changed it",
  missing: "Says something is missing",
  priority: "Disagrees with the priority",
  context: "Adds context",
};

/** What everyone else already said about this process, above the form — so
 *  people answer each other rather than each filing the same note. */
function renderThread(pid) {
  const box = $("fbthread");
  const list = state.comments.get(pid || "__general__") || [];
  box.textContent = "";
  box.hidden = !list.length;
  if (!list.length) return;

  const h = document.createElement("span");
  h.className = "fbl";
  h.textContent = list.length === 1 ? "1 comment so far" : `${list.length} comments so far`;
  box.appendChild(h);

  list.slice(0, 12).forEach((c) => {
    const item = document.createElement("div");
    item.className = "fbc";
    const meta = document.createElement("b");
    meta.textContent = `${c.name || "Unknown"} — ${KIND_LABEL[c.kind] || c.kind}`;
    const when = document.createElement("i");
    when.textContent = (c.createdAt || "").slice(0, 10);
    const body = document.createElement("p");
    body.textContent = c.text;   // textContent, never innerHTML: this is user input
    item.append(meta, when, body);
    box.appendChild(item);
  });

  if (list.length > 12) {
    const more = document.createElement("span");
    more.className = "fbmore";
    more.textContent = `+${list.length - 12} older, in the digest`;
    box.appendChild(more);
  }
}

function closePanel() {
  $("fbpanel").hidden = true;
  $("fbpill").setAttribute("aria-expanded", "false");
}

function wireUI() {
  // Comment affordances only mean something once someone can be identified, so
  // they stay hidden until sign-in resolves.
  document.querySelectorAll(".rowsay").forEach((b) => {
    b.hidden = !state.ready;
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      openPanel(b.dataset.pid);
    });
  });

  document.querySelectorAll(".vote .vt").forEach((b) => {
    b.addEventListener("click", async () => {
      const pid = b.closest(".vote").dataset.pid;
      if (b.classList.contains("say")) { openPanel(pid); return; }
      if (!state.ready) { login(); return; }
      b.disabled = true;
      try { await castVote(pid, Number(b.dataset.v)); }
      catch (err) { console.error(err); alert("Could not save that vote — please try again."); }
      finally { b.disabled = false; }
    });
  });

  $("authbtn").addEventListener("click", async () => {
    if (state.ready) {
      const { auth, api } = await loadFirebase();
      await api.signOut(auth);
      forgetDrupal();
      window.location.reload();
    } else {
      login();
    }
  });

  $("fbpill").addEventListener("click", () => {
    const p = $("fbpanel");
    p.hidden ? openPanel("") : closePanel();
  });
  $("fbx").addEventListener("click", closePanel);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("fbpanel").hidden) closePanel();
  });

  $("fbsend").addEventListener("click", submitComment);
  $("fbproc").addEventListener("change", (e) => renderThread(e.target.value));
  $("fbtext").addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") submitComment();
  });

  // Keep the "show more" button honest after a vote-driven re-sort.
  const more = $("rank-more");
  if (more) more.addEventListener("click", () => setTimeout(reapplyRankTail, 0));
}

async function submitComment() {
  const text = $("fbtext").value.trim();
  const err = $("fberr");
  if (!text) { $("fbtext").focus(); return; }
  const btn = $("fbsend");
  btn.disabled = true;
  btn.textContent = "Sending…";
  try {
    await sendComment({
      pid: $("fbproc").value,
      kind: document.querySelector('input[name="fbkind"]:checked').value,
      text,
    });
    $("fbtext").value = "";
    $("fbform").hidden = true;
    $("fbdone").hidden = false;
    renderThread($("fbproc").value);
    setTimeout(() => { if (!$("fbpanel").hidden) closePanel(); }, 2200);
  } catch (e) {
    console.error(e);
    err.textContent = "Could not save that — check your connection and try again.";
    err.hidden = false;
  } finally {
    btn.disabled = false;
    btn.textContent = "Send";
  }
}

function fillProcessPicker() {
  const sel = $("fbproc");
  const byGroup = new Map();
  state.processes.forEach((p) => {
    if (!byGroup.has(p.group)) byGroup.set(p.group, []);
    byGroup.get(p.group).push(p);
  });
  byGroup.forEach((list, group) => {
    const g = document.createElement("optgroup");
    g.label = group;
    list.forEach((p) => {
      const o = document.createElement("option");
      o.value = p.pid;
      o.textContent = p.name;
      g.appendChild(o);
    });
    sel.appendChild(g);
  });
}

/* ---------------------------------------------------------------------- boot */

async function boot() {
  const dock = $("fbdock");
  state.processes = JSON.parse($("process-manifest").textContent);
  fillProcessPicker();
  wireUI();

  // No consumer configured yet: leave the page exactly as built rather than
  // offering a sign-in button that cannot work.
  if (!OAUTH_CLIENT_ID) {
    setAuthBar("off", "Participation is not configured for this deployment yet");
    return;
  }

  try {
    setAuthBar("busy");
    await completeLoginIfCallback();
    const user = await signInToFirebase();
    if (!user) { setAuthBar("out"); return; }
    state.user = user;
    state.profile = await buildProfile(user);
    state.ready = true;
    setAuthBar("in");
    dock.hidden = false;
    document.body.classList.add("signed-in");
    await Promise.all([loadVotes(), loadComments()]);
    applyVotes();
    document.querySelectorAll(".rowsay").forEach((b) => { b.hidden = false; });
  } catch (e) {
    // An expired session is not an exception — signInToFirebase returns null for
    // that and the bar offers sign-in. Reaching here means something is wrong
    // with the setup or the network, where another sign-in attempt would just
    // fail the same way, so state the reason and let a reload be the retry.
    console.error(e);
    setAuthBar("off", e.message || "Sign-in is unavailable right now");
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  boot();
}
