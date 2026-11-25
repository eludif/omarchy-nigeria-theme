#!/usr/bin/env python3
"""Rebuild CREDITS.md and docs/gallery/ from credits.json.

credits.json is the single list of wallpapers: the desktop photo-credit pill,
the lock screen and this page all read it. To add a photograph, put the file in
backgrounds/ as NN-place-by-photographer.jpg, add its entry to credits.json, and
run:  python3 extras/build-credits.py
Requires ImageMagick (`magick`) for the gallery previews.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
credits = json.loads((ROOT / "credits.json").read_text())
gallery = ROOT / "docs" / "gallery"
gallery.mkdir(parents=True, exist_ok=True)

missing = [name for name in credits if not (ROOT / "backgrounds" / name).is_file()]
uncredited = sorted(p.name for p in (ROOT / "backgrounds").iterdir() if p.is_file() and p.name not in credits)
if missing or uncredited:
    raise SystemExit(f"credits.json and backgrounds/ disagree. Missing files: {missing}; uncredited files: {uncredited}")

for stale in gallery.iterdir():
    if stale.name not in credits:
        stale.unlink()
for name in credits:
    target = gallery / name
    if not target.exists():
        subprocess.run(["magick", str(ROOT / "backgrounds" / name), "-resize", "1200x", "-strip", "-quality", "82", str(target)], check=True)

photographers = sorted({c["photographer"] for c in credits.values()}, key=str.lower)
lines = [
    "# The photographers",
    "",
    f"Every wallpaper in this theme exists because someone stood in a particular place in Nigeria, at a particular moment, and took the picture. This page is for the {len(photographers)} photographers behind these {len(credits)} images.",
    "",
    "Their names also appear on your desktop and lock screen whenever their photograph is showing. Click the name on the desktop to visit their profile. If you enjoy one of these photographs, go and look at the rest of their work.",
    "",
    "The files in `backgrounds/` are the photographers' originals, unchanged except where a section says it was cropped. The previews on this page are smaller copies.",
    "",
    "**Photographers:** " + ", ".join(photographers),
    "",
]
for name, c in credits.items():
    lines += [
        "---",
        "",
        f"## {c['place']}",
        "",
        f"![{c['place']}](docs/gallery/{name})",
        "",
        f"**{c['photographer']}** · [see more of their work]({c['profile']})",
        "",
        c["note"],
        "",
        f"`backgrounds/{name}` · {c['size']} · [source]({c['source']}) · [{c['licence']}]({c['licence_url']})",
        "",
    ]
lines += [
    "---",
    "",
    "## Using and sharing these photographs",
    "",
    "- **Pexels photographs** are under the [Pexels License](https://www.pexels.com/license/): free to use and modify. Credit is not required, but we give it gladly. The licence does not allow selling unaltered copies, or putting the photos on other stock-photo or wallpaper platforms.",
    "- **Wikimedia Commons photographs** are under Creative Commons BY-SA. When you share them, keep the photographer's name, the source link and the licence link. If you change one, say what you changed and share it under the same licence.",
    "- None of the photographers is represented as endorsing this theme.",
    "",
    "## Add your photograph",
    "",
    "Have a photograph of a Nigerian place you love? Contributions are welcome. Please send a landscape original of at least 3840 × 2160, the place, when you took it, how you would like to be credited, a link to your work, and a licence that allows redistribution. Your photo will get its own section on this page, and your name on every desktop that shows it.",
    "",
]
(ROOT / "CREDITS.md").write_text("\n".join(lines))
print(f"CREDITS.md: {len(credits)} photographs by {len(photographers)} photographers")
