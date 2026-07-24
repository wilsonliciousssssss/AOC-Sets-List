# ΑΩ Collective — Set List

A public website for sharing your upcoming gig playlists. Alpha Omega Collective
branding (ink + lime/channels, sharp corners, Syne / Fraunces / Space Mono / Inter,
pixel-glitch ΑΩ). The homepage lists every gig as a channel-coloured card; each card
opens that gig's full set sheet (tracks, keys, BPM, energy curve, Camelot wheel).

**The whole point:** to add a gig, you just **upload its `.html` file into `/sets`**.
The homepage finds it and builds the card automatically — no manifest to edit, no
build step to run.

---

## What's in here

```
index.html            ← the homepage (auto-lists every gig). Nothing to edit.
sets/
  set-5.html          ← your first gig (Set 5 — The Long Way Home)
  _TEMPLATE.html      ← blank starting point. Copy this for a new gig.
                         (files starting with "_" are ignored by the homepage)
gigs.json             ← optional fallback list (see "Fallback" below)
.nojekyll             ← tells GitHub Pages to serve files as-is
README.md             ← this file
HOW-TO-ADD-A-GIG.md   ← the 30-second version
```

---

## One-time setup — publish it (public)

1. Create a new **public** repo on GitHub. Suggested name: **`gigs`**.
   (Public + Pages = your friends can open it. No private data lives here.)
2. Upload **everything in this folder** to the repo (drag the files into the
   GitHub "Add file → Upload files" box, or push with git).
3. Repo **Settings → Pages** → *Source: Deploy from a branch* → **main / (root)** → Save.
4. Wait ~1 minute. Your site is live at:

   **https://<your-username>.github.io/gigs/**

   For you that's: **https://wilsonliciousssssss.github.io/gigs/**

That's it. Share that link.

> The homepage auto-detects the username/repo from the URL, so if you name the repo
> something other than `gigs`, it still works — no code change needed. (If you ever
> serve it from an unusual setup, you can hard-set `OWNER_OVERRIDE` / `REPO_OVERRIDE`
> at the top of the `<script>` in `index.html`.)

---

## Adding a gig (every time)

**Fast path — GitHub website, no tools:**

1. Make the set sheet. Easiest: use your **dj-set-preparation** skill to generate a
   sheet, styled in this same Collective theme. Or copy `sets/_TEMPLATE.html`.
2. In the sheet, edit the two things that matter:
   - the **`AO-GIG`** comment block near the top (title, venue, city, date, channel,
     tracks, bpmRange, duration, vibes) — this is what the homepage card reads;
   - the **`SET` object** in the `<script>` (the tracklist / phases / notes) — this
     is what the full sheet shows.
3. Name the file clearly, e.g. `set-6.html`, and **upload it into the `sets/` folder**
   on GitHub (open the `sets` folder → *Add file → Upload files*).
4. Refresh the homepage — the new gig appears. Upcoming gigs sort by date; once a
   gig's date passes it moves to **Past Sets** on its own.

`channel` picks the card colour: `lime` · `cobalt` · `orange` · `magenta` · `teal` · `violet`.
If you leave it out, the homepage assigns one automatically.

---

## Fallback (how it stays reliable)

The homepage tries three things, in order, so it always shows something:

1. **GitHub API** — lists `/sets` live. This is the "just upload the file" magic and
   is what runs on your public site.
2. **`gigs.json`** — if the API is ever unavailable, it reads this list of filenames
   instead. Only needed as a backup; if you rely on it, add each new file's name here.
3. **Inline seed** — if the page is opened as a local file (double-click, offline),
   it shows the seed baked into `index.html` so you still see a preview.

For a normal public repo you never touch #2 or #3 — #1 handles everything.

---

*Alpha Omega Collective · one system, many channels.*
