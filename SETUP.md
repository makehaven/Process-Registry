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
| Spun-out documents | `docs/` — currently the renewal calendar |
| Answer archive | `questions/` — append-only, never edited after the fact |
| Track and rationale | `makehaven-website/conductor/tracks/process_stabilization_20260814/plan.md` |
