---
name: motion-context
description: "Donne des contextes et des instructions pour la création de motion design. Triggers: Motion Design"
---

# Motion Context

Vérifie si les plugins `hyperframes@hyperframes`, `remotion@remotion` et `erom-image@erom-marketplace` sont installés et disponibles.

## References 

Le dossier `${CLAUDE_PLUGIN_ROOT}/shared/references/` contient plusieurs _démos_ de motion design marquants.
Chaque sous-dossier est décomposé de : 
- 01_GLOBAL_DA_AND_SYSTEM.md : **Direction Artistique & Design Tokens** 
- 02_CHRONOLOGICAL_BREAKDOWN.md : **Découpage Plan-par-Plan Exhaustif**
- 03_FABRICATION_BLUEPRINTS.md : **Recettes de Code & Algorithmes de Reproduction**
- 04_AUDIO_AND_SOUND_DESIGN.md : **Cartographie Audio & Sound Design (SFX)**

N'ancre pas ton motion design précisement sur un exemple, c'est juste des exemples.

## Tools disponibles

Tu peux utiliser Internet librement pour aller chercher des références. Tu peux regarder du motion design (builtin `WebSearch`, plugin `tavily:*`) Tu peux faire vraiment ce que tu penses pouvoir le mieux exprimer visuellement, y compris des motion graphics abstraits.

### Plugins Claude Code

Tu as accès aux plugins suivants : 
- Plugin `hyperframes`
- Plugin `remotion`

### Image Generation

1. Seedream 5.0 Pro (ByteDance via OpenRouter)

C’est le choix idéal si vous intégrez du texte ou des éléments d'interface graphiques complexes dans vos plans. Il excelle dans le rendu de texte précis à plus de 99% et gère la séparation en calques (Layers), ce qui est parfait pour importer des éléments isolés dans Remotion. Le coût est fixe à l'utilisation ($0,045 à $0,09 par image).
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Seedream-5.0-Pro-image-gen.md`

2. Google Nanobana 2.1 (Google)

Ce modèle est redoutable pour sa vitesse et son contrôle itératif ultra-rapide. Il est idéal pour générer des arrière-plans fluides ou des textures abstraites à la volée ($0,02  à $0,03 par image).
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Nanobanana-2.1-image-gen.md`

### Bibliothèque d'images libre de droit

Pixabay.com : API la plus permissive pour un agent.
See `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Pixabay.md`

### Bruitages (SFX)

Banque Sonniss GDC 2024 : 609 WAV libres de droits sur Google Drive (`gdrive:sound-fx/GDC2024/`). Recherche, téléchargement et mix avec la musique : skill `sonniss-catalog-audio-fx` (`${CLAUDE_PLUGIN_ROOT}/skills/sonniss-catalog-audio-fx/SKILL.md`). Rappel : `motion render` n'embarque qu'une piste son, les bruitages doivent être mixés dans `assets/mix.wav`.

### Music (Google)

Lyria 3.5 & Lyria 3 Clip, la suite de modèles de génération musicale de Google, accessible via l'API Gemini. Grâce à Lyria 3.5, vous pouvez générer un son stéréo de haute qualité à 44,1 kHz à partir de textes ou d'images. Ces modèles offrent une cohérence structurelle, incluant les voix, les paroles synchronisées et les arrangements instrumentaux complets.
ModelID: `lyria-3-5` et `lyria-3-clip-preview` verifiés lundi 28 sept sur `https://aistudio.google.com`.
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Lyria-prompt-guide.md`

1. Lyria 3.5

- ModelID: `lyria-3-5`
- Best use: Long-form music generation
- Duration: A couple of minutes (controllable using prompt)
- Output: MP3, $0,10/generation

2. Lyria 3 Clip

- ModelID: `lyria-3-clip-preview`
- Best use: Short clips, loops, previews
- Duration: 30 seconds
- Output: MP3, $0,06/generation
