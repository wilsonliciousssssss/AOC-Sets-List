#!/usr/bin/env python3
"""
build_gigs.py  —  Alpha Omega Collective · Gig Playlists  ·  auto-indexer.

WHAT IT DOES
  Scans every set sheet in  sets/*.html  and writes a single manifest
  assets/gigs.js  (window.GIGS = [...]). The landing page (index.html) reads
  that manifest and renders one card per gig. Nothing on the homepage is
  hand-written — drop a new set sheet into sets/ and re-run this (the GitHub
  Action does it for you on every push).

THE ONLY THING YOU DO PER GIG
  Put the set sheet HTML into  sets/  and push. That's it.

  Optional niceties (all auto-detected, none required):
    • Name the file with a date prefix to set the gig date + ordering:
          2026-08-15-neon-rooftop.html   ->  15 Aug 2026
      (accepts  YYYY-MM-DD  then  -  or  _  then any slug)
    • Or add a line inside the SET object of the sheet:
          date: "2026-08-15",
          venue: "Neon Rooftop, KL",
      These win over the filename if present.

  With neither, the gig still lists fine (date shows as "Date TBA" and it
  sorts after dated gigs, by filename).

USAGE
    python build_gigs.py            # writes assets/gigs.js
    python build_gigs.py --check    # verify only, non-zero exit if a sheet is unreadable

No third-party packages. Python 3.8+.
"""
from __future__ import annotations
import json, os, re, sys, html
from datetime import datetime, timezone

HERE   = os.path.dirname(os.path.abspath(__file__))
SETS   = os.path.join(HERE, "sets")
ASSETS = os.path.join(HERE, "assets")
OUT    = os.path.join(ASSETS, "gigs.js")

DATE_IN_NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[-_]?(.*)$")
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _str_field(src: str, key: str):
    """Pull  key: "value"  out of the SET object (first match).
    Handles unquoted JS keys (title:) and JSON-quoted keys ("title":)."""
    m = re.search(r'(?:"|\b)' + re.escape(key) + r'"?\s*:\s*"((?:[^"\\]|\\.)*)"', src)
    if not m:
        return None
    val = m.group(1)
    # unescape common JS string escapes WITHOUT touching UTF-8 bytes
    val = re.sub(r'\\(["\\/])', r"\1", val)
    val = val.replace("\\n", " ").replace("\\t", " ")
    return html.unescape(val).strip()


def _num_field(src: str, key: str):
    m = re.search(r'(?:"|\b)' + re.escape(key) + r'"?\s*:\s*(\d+)', src)
    return int(m.group(1)) if m else None


def _extract_set_block(txt: str) -> str:
    """Return just the SET = { ... } object text (best-effort brace match)."""
    i = txt.find("const SET")
    if i < 0:
        i = txt.find("SET =")
    if i < 0:
        return txt
    brace = txt.find("{", i)
    if brace < 0:
        return txt
    depth, j, in_str, esc = 0, brace, None, False
    while j < len(txt):
        c = txt[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in "\"'":
                in_str = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return txt[brace:j + 1]
        j += 1
    return txt[brace:]


def _vibes(src: str):
    m = re.search(r'(?:"|\b)vibes"?\s*:\s*\[([^\]]*)\]', src)
    if not m:
        return []
    return [html.unescape(v.strip()) for v in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))]


def _tracks_block(setblock: str) -> str:
    m = re.search(r'(?:"|\b)tracks"?\s*:\s*\[', setblock)
    if not m:
        return ""
    start = m.end() - 1
    depth, j = 0, start
    while j < len(setblock):
        if setblock[j] == "[":
            depth += 1
        elif setblock[j] == "]":
            depth -= 1
            if depth == 0:
                return setblock[start:j + 1]
        j += 1
    return setblock[start:]


def parse_sheet(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    setblock = _extract_set_block(txt)
    tracks = _tracks_block(setblock)
    # gig-level fields live BEFORE the phases[] / tracks[] arrays; slice there so
    # keys like `time` (which also appears inside every phase) aren't mis-read.
    head = re.split(r'(?:"|\b)phases"?\s*:', setblock, 1)[0]

    n_tracks = len(re.findall(r'\{\s*"?n"?\s*:\s*\d+', tracks))
    apexes   = len(re.findall(r'"?tag"?\s*:\s*"apex"', tracks))
    bpms     = [int(x) for x in re.findall(r'(?:"|\b)bpm"?\s*:\s*(\d+)', tracks)]

    fname = os.path.basename(path)
    stem  = os.path.splitext(fname)[0]

    # date: SET.date wins, else filename prefix, else none
    iso = _str_field(head, "date")
    dm = DATE_IN_NAME.match(stem)
    if not iso and dm:
        iso = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}"

    date_label, sort_key = "Date TBA", "0000-00-00"
    if iso and re.match(r"^\d{4}-\d{2}-\d{2}$", iso):
        try:
            y, mo, d = (int(p) for p in iso.split("-"))
            date_label = f"{d:02d} {MONTHS[mo]} {y}"
            sort_key = iso
        except (ValueError, IndexError):
            pass

    title = _str_field(head, "title") or stem.replace("-", " ").title()

    return {
        "file": f"sets/{fname}",
        "title": title,
        "subtitle": _str_field(head, "subtitle") or "",
        "kicker": _str_field(head, "kicker") or "",
        "venue": _str_field(head, "venue") or "",
        "time": _str_field(head, "time") or "",
        "date": date_label,
        "iso": sort_key,
        "length": _str_field(head, "totalLength") or "",
        "coreKey": _str_field(head, "coreKey") or "",
        "bpmStart": _num_field(head, "start"),
        "bpmPeak": _num_field(head, "peak"),
        "bpmMin": min(bpms) if bpms else None,
        "bpmMax": max(bpms) if bpms else None,
        "tracks": n_tracks,
        "peaks": apexes,
        "vibes": _vibes(head),
    }


def main() -> int:
    check_only = "--check" in sys.argv
    if not os.path.isdir(SETS):
        print(f"ERROR: no sets/ folder at {SETS}", file=sys.stderr)
        return 2

    # skip files starting with "_" (e.g. _TEMPLATE.html) — they aren't gigs
    files = sorted(f for f in os.listdir(SETS)
                   if f.lower().endswith(".html") and not f.startswith("_"))
    gigs, errors = [], []
    for f in files:
        try:
            gigs.append(parse_sheet(os.path.join(SETS, f)))
        except Exception as e:  # noqa: BLE001 - report, don't crash the whole build
            errors.append((f, str(e)))

    # newest first; undated (iso 0000-00-00) fall to the bottom, then by title
    gigs.sort(key=lambda g: (g["iso"], g["title"]), reverse=True)

    for f, e in errors:
        print(f"WARN  could not parse {f}: {e}", file=sys.stderr)

    if check_only:
        print(f"OK  {len(gigs)} gig(s) parse cleanly; {len(errors)} error(s).")
        return 1 if errors else 0

    payload = {
        "gigs": gigs,
        "meta": {
            "count": len(gigs),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        },
    }
    os.makedirs(ASSETS, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* AUTO-GENERATED by build_gigs.py — do not edit by hand. */\n")
        f.write("window.GIGS = ")
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write(";\n")

    print(f"OK  indexed {len(gigs)} gig(s) -> {os.path.relpath(OUT, HERE)}")
    for g in gigs:
        print(f"    · {g['date']:>12}  {g['title']}  ({g['tracks']} tracks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
