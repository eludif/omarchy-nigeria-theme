#!/bin/bash
# Optional Omarchy Nigeria extras: the themed lock screen, the desktop photo credit,
# a wallpaper per workspace re-dealt every 15 minutes, and a key for a new photo.
# Run from anywhere, while unlocked, after `omarchy theme set nigeria`.
#   --replace   move an existing, unrelated lock clone to the backup folder first
set -euo pipefail
project=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
backup="$HOME/.local/state/nigeria-theme/backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup" "$HOME/.local/bin" "$HOME/.config/systemd/user"
cp -a "$HOME/.config/omarchy/shell.json" "$backup/shell.json"

# Lock screen: a fresh clone of Omarchy's current lock, restyled (visuals only).
clone="$HOME/.config/omarchy/plugins/${USER}.lock"
if [[ -e $clone ]]; then
  if grep -q "Nigeria theme lock styling" "$clone/LockView.qml" 2>/dev/null; then
    echo "Nigeria lock styling already installed; leaving the lock as it is."
  elif [[ ${1:-} == --replace ]]; then
    mv "$clone" "$backup/${USER}.lock"
    echo "Moved the existing lock clone to $backup/${USER}.lock"
  else
    echo "A lock clone already exists at $clone." >&2
    echo "Re-run with --replace to move it to $backup and install a fresh one." >&2
    exit 1
  fi
fi
if [[ ! -e $clone ]]; then
  omarchy plugin clone omarchy.lock
  python3 "$project/extras/customize-lock.py" "$clone"
fi

# Desktop photo credit: names the photographer of the current wallpaper.
credit="$HOME/.config/omarchy/plugins/nigeria.photo-credit"
if [[ -e $credit ]]; then cp -a "$credit" "$backup/nigeria.photo-credit"; rm -rf "$credit"; fi
cp -a "$project/extras/photo-credit" "$credit"
omarchy-shell shell rescanPlugins >/dev/null 2>&1 || true
omarchy plugin enable nigeria.photo-credit

# A wallpaper per workspace, re-dealt every 15 minutes, while a theme with credits.json is active.
install -m 755 "$project/extras/workspace-walls" "$HOME/.local/bin/nigeria-workspace-walls"
install -m 755 "$project/extras/rotate-city" "$HOME/.local/bin/nigeria-rotate-city"
for unit in nigeria-city-rotation.service nigeria-city-rotation.timer nigeria-workspace-walls.service; do
  if [[ -e "$HOME/.config/systemd/user/$unit" ]]; then
    cp -a "$HOME/.config/systemd/user/$unit" "$backup/$unit"
  fi
  install -m 644 "$project/extras/systemd/$unit" "$HOME/.config/systemd/user/$unit"
done
systemctl --user daemon-reload
systemctl --user enable --now nigeria-city-rotation.timer
systemctl --user enable nigeria-workspace-walls.service
systemctl --user restart nigeria-workspace-walls.service

# Super+Ctrl+Shift+N: a new random photo for the current workspace.
bindings="$HOME/.config/hypr/bindings.lua"
if [[ -f $bindings ]] && ! grep -q "nigeria-workspace-walls next" "$bindings"; then
  cp -a "$bindings" "$backup/bindings.lua"
  printf '\n-- Omarchy Nigeria: new random wallpaper for this workspace\no.bind("SUPER + CTRL + SHIFT + N", "Next Nigeria wallpaper", "%s next")\n' "$HOME/.local/bin/nigeria-workspace-walls" >>"$bindings"
  hyprctl reload >/dev/null 2>&1 || true
fi
omarchy restart shell
printf 'Backup saved to %s\n' "$backup"
