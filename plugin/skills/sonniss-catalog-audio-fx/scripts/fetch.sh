#!/usr/bin/env bash
# Télécharge un ou plusieurs sons de la banque dans <scène>/assets/sfx/.
# Usage : fetch.sh <dossier de scène> "<chemin Drive tel que donné par search.ts>" [chemin…]
set -euo pipefail

REMOTE="gdrive:sound-fx/GDC2024"

if [ $# -lt 2 ]; then
  echo "usage: fetch.sh <scene_dir> <drive_path> [drive_path…]" >&2
  exit 2
fi

scene_dir="$1"
shift
[ -n "$scene_dir" ] || { echo "scene_dir vide" >&2; exit 2; }
dest="$scene_dir/assets/sfx"
mkdir -p "$dest"

for path in "$@"; do
  rclone copyto "$REMOTE/$path" "$dest/$(basename "$path")"
  echo "ok  $dest/$(basename "$path")"
done
