# Alpha Omega Collective — Gig Playlists

### ▶ Live site: **https://wilsonliciousssssss.github.io/AOC-Sets-List/**

*Signal over noise.* — by **DJ7 · Wilsonlicioussss**

---

Hey — I'm Wilson, and this is where I share the playlists from my gigs.

Every set I play out, I lay down here as an interactive **set sheet**: not just a list
of songs, but the whole journey — the order I played them, the keys, the tempos, and
the way the energy rises and falls across the night. If you caught one of my sets and
wanted to know "what *was* that track," or you just like following a set like a story
from the first record to the last, this is for you. Open the site, pick a gig, and dig in.

## What you'll find

- **Every gig as a full set sheet.** The complete tracklist in the exact order I played
  it, split into phases — warm-up, the builds, the peaks, the breather, the comedown.
- **The energy journey, drawn out.** A live energy curve for the whole set. Hover it (or
  drag your finger on mobile) and the track at that moment pops up — title, artist, BPM
  and key.
- **Hear it before you dig for it.** Every track has a ▶ preview button for a quick
  listen, plus one-tap links straight to it on **Spotify** and **Apple Music**.
- **For the DJs.** Camelot keys, BPMs, harmonic-mixing notes and my transition cues for
  each track — the invisible stuff behind a set that actually flows.
- **Made for your phone.** It reads great in your hand, and you can add it to your home
  screen and open it like an app.

New sets land here whenever I play out, so check back.

## Follow along

If a set connected with you, a follow is the best support — come say hi and tell me what
you found:

- **Instagram** — https://www.instagram.com/wilsonlicioussss/
- **Blog** — https://harbingermsc.blogspot.com/

---

## For the curious — how this is built

This is a single, self-contained static site — no tracking, no ads, no sign-up. It's
built with the **Alpha Omega Collective** design system (ink, lime, sharp edges — *freedom
in colour, discipline in structure*) and hosted free on GitHub Pages. Each set sheet is
its own standalone HTML file; the previews resolve live from the public iTunes catalogue,
so there are no keys or accounts anywhere in here.

The homepage builds itself. Every set sheet lives in the [`sets/`](./sets) folder, and a
GitHub Action re-scans that folder on every push and regenerates the index — so a new gig
appears on the site on its own, no page-editing by hand.

**Adding a gig (for me / future me):** drop the set-sheet HTML into `sets/`, commit, push.
Done. Optionally prefix the filename with a date (`2026-08-15-neon-rooftop.html`) or add
a `date:`/`venue:` line inside the sheet to date and label the card.

**Run or host it yourself:** clone the repo, then either open `index.html` after running
`python build_gigs.py`, or serve the folder (`python -m http.server`) and visit
`localhost`. To publish your own copy: push it to a GitHub repo and set **Settings → Pages
→ Source: GitHub Actions**. Mine lives at
`https://wilsonliciousssssss.github.io/AOC-Sets-List/`.

---

Made with **Alpha Omega Collective** — *Signal over noise.*
