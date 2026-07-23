# Alpha Omega Collective — Gig Playlists

A web app for sharing my gig playlists. Each set I play out lives here as a
read-from-the-booth **set sheet** (tracklist, keys, BPM, energy arc). The
homepage indexes every set automatically — I drop a file in, the site updates
itself.

**Signal over noise.** By DJ7 · Wilsonlicioussss.

---

## The workflow (what you do per gig)

1. Prep the set sheet HTML (the file Claude gives you — a self-contained page).
2. Put it in the **`sets/`** folder.
3. Commit & push.

That's the whole job. On push, a GitHub Action re-scans `sets/`, rebuilds the
index, and redeploys. The new gig appears on the homepage on its own — you never
edit `index.html`.

> Prefer clicking over the command line? On github.com, open the `sets/` folder →
> **Add file → Upload files** → drag the HTML in → **Commit changes**. Same result.

### Optional: set the gig date

The date on each card is auto-detected, in this order:

1. A `date: "YYYY-MM-DD"` line inside the set sheet's `SET` object (add `venue: "…"` too if you like), **or**
2. A date prefix on the filename — `2026-08-15-neon-rooftop.html` → *15 Aug 2026*.

With neither, the gig still lists fine (shows **Date TBA**, sorts after dated
sets). Newest date shows first.

---

## One-time setup (≈ 5 minutes)

You only do this once, to get the site live.

1. **Create a repo** on GitHub — e.g. `gig-playlists`. Public if you want friends
   to see it.
2. **Upload this whole folder** to the repo root (so `index.html` sits at the top
   level), commit to the `main` branch. Via CLI:
   ```bash
   git init && git add . && git commit -m "Alpha Omega gig playlists"
   git branch -M main
   git remote add origin https://github.com/<you>/gig-playlists.git
   git push -u origin main
   ```
3. **Turn on Pages with Actions:** repo **Settings → Pages → Build and deployment
   → Source: `GitHub Actions`**. (Not "Deploy from a branch" — this site builds
   itself.)
4. Push once (or **Actions** tab → run **Build & Deploy**). When it's green, your
   site is live at:
   ```
   https://<you>.github.io/gig-playlists/
   ```
   Share that link. Friends can open it on any phone and even **Add to Home
   Screen** to install it like an app (offline-ready).

---

## What's in here

```
index.html                  the homepage (auto-renders the gig grid; don't edit)
sets/                        ← DROP NEW SET SHEETS HERE
  set-5.html                 example: Set 5 — "The Long Way Home" (28 tracks)
build_gigs.py                scans sets/ → writes assets/gigs.js (the index)
assets/gigs.js               AUTO-GENERATED index (don't edit by hand)
assets/icons/                the ΑΩ app icons
tokens.css                   Alpha Omega Collective design tokens (source of truth)
app.webmanifest              installable-app config (PWA)
sw.js                        offline caching
.github/workflows/deploy.yml the auto-build-and-deploy Action
```

---

## Preview locally (optional)

Because the homepage loads `assets/gigs.js`, serve the folder rather than
double-clicking, so everything resolves:

```bash
python build_gigs.py        # refresh the index after adding a set
python -m http.server 8080  # then open http://localhost:8080
```

The committed `assets/gigs.js` also makes the page work when opened directly in
most browsers — but the Action is the source of truth once it's live.

---

## How the auto-index works

`build_gigs.py` reads the `SET` object inside each `sets/*.html` and pulls out
the title, subtitle, vibe tags, track count, BPM range, core key, length and
peak count — then writes them into `assets/gigs.js`. The homepage reads that file
and draws one card per gig, with search + vibe filters. No database, no server,
no build step for you to run — the Action handles it.

---

Made with **Alpha Omega Collective** — *Signal over noise.*
