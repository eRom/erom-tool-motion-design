![erom-motion-design](assets/plugin.png)

# erom-motion-design

Plugin Claude Code. Boîte à outils de motion design : références décortiquées de vidéos marquantes, guides des générateurs d'images et de musique, banque de bruitages Sonniss, pour aller au-delà des limites de HyperFrames.

## Installation

```
/plugin marketplace add eRom/erom-marketplace
/plugin install erom-motion-design@erom-marketplace
```

## Prérequis

- Plugins `hyperframes` et `remotion` : ce plugin les complète, il ne les remplace pas.
- `bun` et `ffmpeg` pour chercher et mixer les bruitages.
- `rclone` avec un remote `gdrive:` qui donne accès à `sound-fx/GDC2024/`.
- Clés d'API en variables d'environnement, selon les outils utilisés : `GEMINI_API_KEY` (Nanobanana, Lyria), `PIXABAY_API_KEY`, une clé OpenRouter (Seedream).

## Les skills

| Skill | Invocation | Ce qu'elle fait |
|---|---|---|
| `motion-context` | `/erom-motion-design:motion-context` | Pose le contexte d'une création : références décortiquées, générateurs d'images (Seedream, Nanobanana), musique (Lyria), images libres (Pixabay), bruitages. |
| `sonniss-catalog-audio-fx` | `/erom-motion-design:sonniss-catalog-audio-fx` | Cherche des bruitages dans la banque Sonniss GDC 2024 (609 WAV), les télécharge et les mixe à la musique. |

## Licence

MIT, Romain Ecarnot.
