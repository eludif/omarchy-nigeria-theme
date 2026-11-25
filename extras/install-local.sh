#!/bin/bash
# Optional Omarchy Nigeria lock screen.
# Run from anywhere, while unlocked, after `omarchy theme set nigeria`.
#   --replace   move an existing, unrelated lock clone to the backup folder first
#
# The photo per workspace, the 15-minute re-deal and the desktop photo credit
# are a separate plugin:  omarchy plugin add https://github.com/eludif/omarchy-photo-walls --enable
set -euo pipefail
project=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
backup="$HOME/.local/state/nigeria-theme/backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup"
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

# Earlier versions installed the wallpaper extras as scripts, services and a key
# binding. The Photo Walls plugin replaces them, so move what is left into the backup.
units="$HOME/.config/systemd/user"
for unit in nigeria-workspace-walls.service nigeria-city-rotation.timer nigeria-city-rotation.service; do
  if [[ -e $units/$unit ]]; then
    systemctl --user disable --now "$unit" >/dev/null 2>&1 || true
    mv "$units/$unit" "$backup/"
  fi
done
for script in nigeria-workspace-walls nigeria-rotate-city; do
  if [[ -e $HOME/.local/bin/$script ]]; then mv "$HOME/.local/bin/$script" "$backup/"; fi
done
systemctl --user daemon-reload
bindings="$HOME/.config/hypr/bindings.lua"
if [[ -f $bindings ]] && grep -q "nigeria-workspace-walls next" "$bindings"; then
  cp -a "$bindings" "$backup/bindings.lua"
  sed -i '/-- Omarchy Nigeria: new random wallpaper for this workspace/d; /nigeria-workspace-walls next/d' "$bindings"
  hyprctl reload >/dev/null 2>&1 || true
fi
if [[ -e $HOME/.config/omarchy/plugins/nigeria.photo-credit ]]; then
  omarchy plugin disable nigeria.photo-credit >/dev/null 2>&1 || true
  mv "$HOME/.config/omarchy/plugins/nigeria.photo-credit" "$backup/"
fi

omarchy restart shell
printf 'Backup saved to %s\n' "$backup"
echo "For a photo per workspace and photographer credits on the desktop, also run:"
echo "  omarchy plugin add https://github.com/eludif/omarchy-photo-walls --enable"
