#!/usr/bin/env bash
# Télécharge un ou plusieurs sons de la banque dans <projet>/assets/sfx/.
# Usage : fetch.sh <projet HyperFrames> "<chemin Drive tel que donné par search.ts>" [chemin…]
set -euo pipefail

REMOTE="gdrive:sound-fx/GDC2024"

if [ $# -lt 2 ]; then
  echo "usage: fetch.sh <project_dir> <drive_path> [drive_path…]" >&2
  exit 2
fi

project_dir="$1"
shift
[ -n "$project_dir" ] || { echo "project_dir vide" >&2; exit 2; }
dest="$project_dir/assets/sfx"
mkdir -p "$dest"

for path in "$@"; do
  rclone copyto "$REMOTE/$path" "$dest/$(basename "$path")"
  echo "ok  $dest/$(basename "$path")"
done
