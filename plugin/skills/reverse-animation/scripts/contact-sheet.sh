#!/usr/bin/env bash
# Planche-contact d'une fenêtre de vidéo : images à cadence fixe, en grille, lecture gauche->droite puis haut->bas.
# Imprime sur stdout la table case -> horodatage (ms), parce que le ffmpeg de Homebrew n'a pas drawtext.
#
# Usage : contact-sheet.sh <vidéo> <début_s> <fin_s> <sortie.jpg> [fps=20] [colonnes=5] [largeur_case=360]
set -euo pipefail

if [ $# -lt 4 ]; then
  echo 'usage : contact-sheet.sh <vidéo> <début_s> <fin_s> <sortie.jpg> [fps=20] [colonnes=5] [largeur_case=360]' >&2
  exit 2
fi
command -v ffmpeg >/dev/null || { echo 'contact-sheet: ffmpeg absent (brew install ffmpeg)' >&2; exit 1; }

video="$1"; start="$2"; end="$3"; out="$4"
fps="${5:-20}"; cols="${6:-5}"; width="${7:-360}"

count=$(awk -v s="$start" -v e="$end" -v f="$fps" 'BEGIN { n = int((e - s) * f + 0.5); print (n < 1 ? 1 : n) }')
if [ "$count" -gt 60 ]; then
  echo "contact-sheet: ${count} images, au-delà de 60 la planche devient illisible : réduis la fenêtre ou le fps" >&2
  exit 2
fi
rows=$(( (count + cols - 1) / cols ))

ffmpeg -y -loglevel error -ss "$start" -t "$(awk -v s="$start" -v e="$end" 'BEGIN { print e - s }')" -i "$video" \
  -vf "fps=${fps},scale=${width}:-2,tile=${cols}x${rows}:padding=4:color=0x808080" \
  -frames:v 1 -q:v 3 "$out"

echo "planche : $out (${cols}x${rows}, ${count} images, pas de $(awk -v f="$fps" 'BEGIN { printf "%.1f", 1000 / f }') ms)"
awk -v s="$start" -v f="$fps" -v n="$count" -v c="$cols" 'BEGIN {
  for (i = 0; i < n; i++) printf "case %d (ligne %d, col %d) : t = %d ms\n", i + 1, int(i / c) + 1, i % c + 1, (s + i / f) * 1000 + 0.5
}'
