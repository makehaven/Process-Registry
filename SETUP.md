# Setup — GitHub, Firebase and the domain

Everything in this file is a one-time task for JR. The repo is committed and
builds cleanly; these steps put it on the internet at
`process.makehaven.org`.

Rough time: 20–30 minutes, most of it waiting for DNS.

---

## 1. Push to GitHub — ✅ done

`origin` is `github.com/makehaven/Process-Registry`, default branch **`master`**
(the deploy workflow has been corrected to match — thanks).

Just push whatever is local:

```bash
cd ~/development/Process-Registry
git push -u origin master
```

---

## 2. Create the Firebase project

Console → **Add project** → name it `makehaven-process-registry`.

The project ID must match what's already in `.firebaserc` and the deploy
workflow. If Firebase appends a suffix (it does when the name is taken), update
both files to the actual ID:

- `.firebaserc` → `projects.default`
- `.github/workflows/deploy.yml` → `projectId:`

Then enable Hosting: **Build → Hosting → Get started**. Skip the CLI walkthrough
it offers; `firebase.json` already exists here.

Google Analytics is not needed. Decline it.

---

## 3. First deploy from your machine

Confirms the config before wiring CI:

```bash
cd ~/development/Process-Registry
python3 build/build.py          # writes public/index.html
npx firebase-tools login        # if not already authenticated
npx firebase-tools deploy --only hosting
```

That should print a `web.app` URL. Open it and check the page renders — this is
the same output you've been reviewing, so it should look identical.

---

## 4. Point the domain

Firebase Console → **Hosting → Add custom domain** → `process.makehaven.org`.

Firebase will give you either a TXT record (to verify ownership) or two A
records. Add them wherever `makehaven.org` DNS lives — same place you'd manage
records for the other subdomains.

Certificate provisioning takes anywhere from 15 minutes to a few hours. The
console shows progress; there's nothing to do but wait.

**Note:** `makehaven.org` currently has subdomains on Firebase already
(`sponsorship`, `phonebank`), so this is a path you've walked before — the DNS
provider and process will be familiar.

---

## 5. Wire up automatic deploys

So that editing `data/inventory.md` and pushing republishes the site.

```bash
cd ~/development/Process-Registry
npx firebase-tools init hosting:github
```

It will ask to authorise the GitHub repo, then create a service account and
store it as the `FIREBASE_SERVICE_ACCOUNT` secret. When it offers to overwrite
the existing workflow file, **say no** — `.github/workflows/deploy.yml` is
already written and includes a build-output check the generated one lacks.

If the secret name it creates differs (it sometimes appends the project ID),
update the `firebaseServiceAccount:` line in the workflow to match.

Test it:

```bash
git commit --allow-empty -m "Test deploy"
git push origin master
```

Watch the run under the repo's **Actions** tab.

---

## 6. Participation — sign-in, votes and comments

This is the only remaining setup that is not already done in code. The page ships
with participation **switched off**: `OAUTH_CLIENT_ID` in
`public/registry-config.js` is empty, so the sign-in control stays hidden and
visitors see the registry exactly as before. Filling that value in is what turns
it on.

Already done, nothing to do:

- Firestore database `(default)` in `makehaven-process-registry` (nam5)
- Security rules written and deployed — `firestore.rules`
- Firebase web app registered; its config is in `public/registry-config.js`
- The client — `public/participate.js`

### 6a. Register the app with the Drupal bridge — ✅ config committed

The `makerspace_firebase_auth` module is already generic and **already live** —
`/api/firebase-token/process_registry` answers 403 rather than 404, which means
the route exists and only the app registration was missing. No Drupal code
change was needed.

Committed in `makehaven-website` (local only — **not pushed**, because master
there is 14 commits ahead of Pantheon already and pushing deploys to dev):

| File | What |
|---|---|
| `config/makerspace_firebase_auth.settings.yml` | the `process_registry` app entry |
| `config/simple_oauth.oauth2_scope.process_registry.yml` | the OAuth scope, granted to `authenticated` |
| `web/sites/default/services.yml` | `https://process.makehaven.org` in the CORS allow-list |

It follows `grant_research` in reading the key from a **Pantheon secret** rather
than a `private://` upload, so the credential never sits in the filesystem:

```yaml
process_registry:
  project_id: makehaven-process-registry
  service_account_key: 'secret://process_registry_sa_json'
```

The claim rules only decide **who can triage comments**. Voting, commenting and
reading what others said need nothing beyond a signed-in account, which is why
the scope is granted to `authenticated` rather than a named role, and why there
is no `board` role anywhere in this.

**What is left here:** push that repo, deploy, and `drush cim`.

### 6b. Set the Pantheon secret

The service-account key has been generated and is at
`process-registry-sa.json` in this session's scratchpad. **Do not commit it.**

```bash
terminus secret:site:set <site>.live process_registry_sa_json \
  "$(cat process-registry-sa.json)" --scope=web
```

Note that `terminus remote:drush` and `terminus secret:*` could not be run from
this machine — `appserver.<id>.drush.in` does not resolve here, though the git
remote does. Run these where terminus works.

If the key ever needs replacing:
`gcloud iam service-accounts keys create out.json --iam-account=firebase-adminsdk-fbsvc@makehaven-process-registry.iam.gserviceaccount.com`

### 6c. Create the OAuth consumer — ✅ done

At `/admin/config/services/consumer`, add a consumer:

| Field | Value |
|---|---|
| Label | Process Registry |
| Client ID | `process_registry` — you type this; it is not generated |
| Redirect URI | `https://process.makehaven.org/` |
| Scopes | `process_registry` — already created by the config in 6a |
| Confidential | **no** — this is a public PKCE client, no secret |

The CORS entry is already in the committed `services.yml`, so there is nothing
to add there.

A consumer has to be created here rather than in config because consumers are
content entities, not configuration — that is the one part of this that cannot
be committed.

### 6d. Turn it on — ✅ done

The consumer's **client id** is `process_registry`, set in
`public/registry-config.js`:

```js
export const OAUTH_CLIENT_ID = "process_registry";
```

Note this is a value you choose, not one Drupal generates: on `consumers` 1.x
`client_id` is a required text field, "an arbitrary unique field, like a machine
name". It is the same string as `FIREBASE_APP_ID` and the OAuth scope on purpose.

It is **not** a secret and does not belong in GitHub secrets — it is a public
PKCE client id served to every visitor, and the deploy workflow does no
substitution anyway: it builds `index.html` and ships `public/` verbatim.

Verified against the live site before committing: `/oauth/authorize` with this
client id and `https://process.makehaven.org/` as the redirect URI returns a 302
to the login page, while an unknown client id or a wrong redirect URI returns
`401 invalid_client`.

### 6e. Check it

Open `process.makehaven.org`, sign in, and confirm four things: the arrows on
the **Next** tab move a row and the score shows `+n` beside the formula; a
**Comment** button appears on inventory rows; the pill at bottom right opens the
panel; and after filing one comment, re-opening the panel shows it back with
your name on it. If sign-in reports *"not registered with the Drupal Firebase
bridge yet"*, the config from 6a has not been deployed and imported yet; if it
reports a 500, the Pantheon secret from 6b is missing or malformed.

If the page still says *"participation is not configured for this deployment
yet"* after the deploy is live, that is your browser holding a cached
`registry-config.js` — hard-reload (Ctrl/Cmd+Shift+R). Check what the server is
actually sending before believing the page:

```bash
curl -s https://process.makehaven.org/registry-config.js | grep OAUTH_CLIENT_ID
```

The `headers` block in `firebase.json` exists for this. It originally scoped the
short max-age to `**/*.html`, which never matched anything: `cleanUrls` 301s
`/index.html` to `/`, so the only path a browser requests is `/`, and every file
— HTML and JS alike — fell through to Firebase's default one-hour cache. The
rules now key on `/` and `**/*.js`, and the JS is `max-age=0, must-revalidate`
because these files are unversioned and one of them decides whether sign-in
exists at all. A revalidation on a 2 KB file is cheap; an hour of stale auth
config is not.

---

## 7. Reading what people said

Votes and comments never write back to `data/inventory.md`. Anyone with an
account can vote, so letting that edit the record directly would mean the
registry could be rewritten by whoever clicked last. Instead they are exported
and a person decides:

```bash
gcloud auth login jrlogan@makehaven.org   # once; the personal gmail account has no access
python3 build/digest.py                   # writes data/feedback-digest.md
```

The digest groups comments by process, tallies the votes, and calls out two
things worth looking at directly: **contested** rows where people voted in both
directions, and **orphaned** ids where a vote points at a process that has since
been renamed. Hand it to Claude with the inventory, or read it yourself, then
edit `data/inventory.md` by hand and push.

Once the changes are in, `python3 build/digest.py --mark-reviewed` clears the
queue so the next run only shows what is new.

`data/feedback-digest.md` is gitignored — it is a working file, and it contains
names and unverified claims about people's work.

---

## After it's live

**Editing is now: change `data/inventory.md`, commit, push.** The site rebuilds
and redeploys in about a minute. No local build needed.

Three things worth doing in the first week:

1. **Show it at a staff or board meeting.** One of the kill criteria is "not
   referenced in a board or staff meeting within two cycles of publication." The
   *In flux right now* section is the one built for that conversation.
2. **Decide what the public version shows.** Six links are marked `(staff)` and
   currently render for everyone as labelled links to admin pages — they 403 for
   anonymous visitors, so nothing leaks, but they do advertise internal URLs.
   If that bothers you, the build should strip them; say the word and I'll add
   it.
3. **Delegate round 3.** The remaining questions are better answered by the shop
   manager, Kate, and the education manager than by you. Part 4 of
   `questions/questions-round-2.md` maps who should get what.

## Where things live now

| | |
|---|---|
| Registry data | `data/inventory.md` — the source of truth |
| Renderer | `build/build.py`, `build/shell.html` |
| Participation client | `public/participate.js`, `public/registry-config.js` |
| Firestore rules | `firestore.rules` — deploy with `firebase deploy --only firestore:rules` |
| Feedback export | `build/digest.py` → `data/feedback-digest.md` (gitignored) |
| Spun-out documents | `docs/` — currently the renewal calendar |
| Answer archive | `questions/` — append-only, never edited after the fact |
| Track and rationale | `makehaven-website/conductor/tracks/process_stabilization_20260814/plan.md` |
