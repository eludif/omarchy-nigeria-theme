# Omarchy Nigeria

An Omarchy theme in Nigeria's green and white, with 20 high-resolution photographs of Nigerian places, each credited to the person who took it. Designed for a blog-led release around 1 October.

![Omarchy Nigeria desktop](preview.png)

## Install

```bash
omarchy theme install https://github.com/eludif/omarchy-nigeria-theme
```

This installs and applies the theme as `nigeria`. To work from a local copy of this repository instead:

```bash
mkdir -p ~/.config/omarchy/themes
cp -r -n . ~/.config/omarchy/themes/nigeria
omarchy theme set nigeria
```

Use a fresh destination for the first local install. For a photo per workspace with photographer credits, and the lock screen, see [Extras](#extras).

## Design

Soft green surfaces (`#1A2A22`), off-white text (`#DCE7DF`), and emerald accents (`#39D98A`). The terminal palette follows Everforest's approach to long reading sessions: a softened base, body text around 12:1 rather than a glaring pure white, and distinct hues at similar brightness, so errors, warnings, strings and comments stay easy to tell apart. Focused windows get an emerald / white / emerald border, like the flag; unfocused borders almost disappear.

The theme also ships its own bar, launcher, notification and lock-screen colours (`shell.toml`) and the green Yaru icon set. Omarchy builds a matching Claude Code theme from the palette; pick **Omarchy** with `/theme` in Claude Code. These are design choices inspired by the flag, not a claim about official colour specifications.

## Wallpapers

Twenty photographs, nineteen of them 4K or larger: the National Theatre, Carter Bridge, the Civic Centre and the coastline in Lagos; the National Mosque and the City Gate in Abuja; Zuma Rock at dusk; the Obudu Plateau and the hills of Ngel Nyaki; the Emir's Palace in Dutse; Gidan Makama and Coronation Hall in Kano; the creeks of Port Harcourt; mosques, waterfalls and savannah in the north; and more.

**[Meet the photographers](CREDITS.md).** Each has a section with their name, a link to more of their work, and the story of the place. Their names also appear on the desktop and lock screen whenever their photograph is showing, and each file is named after its photographer, so `omarchy theme bg current` tells you whose picture you are looking at.

The Abuja City Gate is cropped from a portrait original, 3153 pixels wide, so it looks softer than the rest on screens wider than that. Depending on your monitor's shape, the very wide photographs may lose a little at the sides and the 3:2 and 4:3 ones a little at the top and bottom.

To add a photograph: put a 4K landscape original in `backgrounds/` as `NN-place-by-photographer.jpg`, add its entry to [credits.json](credits.json), and run `python3 extras/build-credits.py` to rebuild the credits page.

## Extras

### Photo Walls plugin

```bash
omarchy plugin add https://github.com/eludif/omarchy-photo-walls --enable
```

[Photo Walls](https://github.com/eludif/omarchy-photo-walls) turns the twenty photographs into a living gallery:

- **A photo per workspace.** Every workspace keeps its own photograph. Switching swaps it instantly, so you land on a different place in Nigeria.
- **Fresh every 15 minutes.** The photos are dealt out again, with a gentle cross-fade.
- **One click for another.** A picture icon in the bar gives the current workspace a new photo. Hover it to see who took the one on screen.
- **Photographers credited.** A pill in the bottom-left corner of the desktop names the place and the photographer. Click it to open their profile.

It reads this theme's `credits.json` and does nothing under themes without one. Update it with `omarchy plugin update eludif.photo-walls`.

### Lock screen

![Omarchy Nigeria lock screen](preview-unlock.png)

In the style of the omarchy.org homepage: the current wallpaper, sharp and lightly graded toward the theme's greens, with the Omarchy pixel wordmark set straight into it in green, white and green, an **NG** badge, and a compact password field in the proportions of the site's buttons. Dim pixels sit around the edges, with small clusters twinkling on and off as they do on the site. The photographer is credited in the corner.

Only the lock's visuals change. It is a fresh clone of Omarchy's current lock plugin, and password checking, failure messages and fingerprint support are untouched. The styling switches on only while the active theme ships `lock-emblem.svg`, so other themes keep the stock lock screen.

Because it replaces the program that checks your password, it is a deliberate, separate step. Run it while unlocked:

```bash
git clone https://github.com/eludif/omarchy-nigeria-theme
bash omarchy-nigeria-theme/extras/install-local.sh    # or --replace if you already have a custom lock clone
```

Preview it without locking (click to dismiss):

```bash
omarchy-shell lock preview
```

To go back to Omarchy's own lock screen, run `omarchy plugin disable "$USER.lock"`, then `omarchy restart shell` while unlocked. When Omarchy updates its lock, re-run the installer with `--replace` to pick up the new version. The lock artwork is generated by `extras/make-lock-art.py`.

## Nigeria 66 identity

The anniversary artwork for 66 years of independence (1 October 2026) is in [identity/nigeria-66.svg](identity/nigeria-66.svg), ready for the blog and release graphics.

## Project status

Reading-tuned palette, flag-style focus borders, shell styling, 20 credited high-resolution wallpapers, random rotation, the desktop photo credit, and the Omarchy Nigeria lock screen. The lock has been checked in preview on a 5K display; a real lock and unlock with password and fingerprint still needs checking before public release. See [the brief](docs/brief.md) and [blog draft](docs/blog-draft.md).

## Licence

The theme configuration, scripts and documentation are released under the MIT licence ([LICENSE](LICENSE)). The photographs keep their own licences, listed in [CREDITS.md](CREDITS.md).
