---
name: motion-context
description: "Point d'entrée de toute création de motion design : vidéo animée, teaser, intro, générique, clip, reel, kinetic typography, motion graphics, démo produit animée. Vérifie que HyperFrames et Remotion sont prêts, puis apporte ce qu'ils n'ont pas : références de vidéos décortiquées, génération d'images (Seedream, Nanobanana), images libres (Pixabay), musique (Lyria), bruitages (Sonniss). À charger avant `/hyperframes:hyperframes` dès que Romain veut fabriquer une vidéo, même sans dire « motion design »."
---

# Motion Context

HyperFrames fabrique le motion : composition, animation, rendu. Cette skill ne le remplace pas. Elle vérifie qu'il est là, puis apporte la matière qu'il n'a pas : des références pour l'œil et des outils externes pour les images, la musique et les bruitages.

## 1. Vérifier les plugins

Deux plugins sont requis : `hyperframes@hyperframes` et `remotion@remotion`. Un plugin installé mais désactivé ne sert à rien : il faut les deux, installé **et** activé.

Premier test, sans commande : les skills de la session. Si `hyperframes:hyperframes` et `remotion:remotion-best-practices` figurent dans la liste des skills disponibles, les deux plugins sont actifs. Passer à l'étape 2.

Sinon, diagnostiquer :

```bash
claude plugin list 2>&1 | grep -A3 -E 'hyperframes@|remotion@'
```

| Ce qui sort | Quoi faire |
|---|---|
| Rien pour un plugin | Pas installé. `claude plugin marketplace add heygen-com/hyperframes` puis `claude plugin install hyperframes@hyperframes` (Remotion : `remotion-dev/claude-code-plugin`, `remotion@remotion`) |
| `Status: ✘ disabled` | Installé mais coupé. `claude plugin enable hyperframes@hyperframes` (ou `remotion@remotion`) |
| `Status: ✔ enabled` mais skills absentes de la session | Activé après le lancement de la session. Il faut relancer Claude Code |

Installer ou activer un plugin change la config de Romain : lui donner la commande et attendre son accord, ne pas la lancer d'office. Sans HyperFrames, s'arrêter là : rien ne peut être rendu.

## 2. Passer la main à HyperFrames

`/hyperframes:hyperframes` est le point d'entrée obligatoire de toute vidéo : il choisit le bon workflow (motion graphics court, explainer, clip musical, lancement produit…). HyperFrames est le framework par défaut. Remotion ne sert que si Romain le demande explicitement pour ce livrable.

Les sections suivantes sont des ressources à injecter dans ce workflow, au moment où il en a besoin : références pendant la direction artistique, images et sons pendant la fabrication.

## 3. Références

`${CLAUDE_PLUGIN_ROOT}/shared/references/INDEX.md` liste 14 vidéos de motion design décortiquées, par famille, avec durée, tempo et ce qui distingue chacune. Le lire d'abord, puis seulement le `01_GLOBAL_DA_AND_SYSTEM.md` des 1 à 3 candidats proches de l'intention.

Chaque dossier contient :
- `01_GLOBAL_DA_AND_SYSTEM.md` : direction artistique et design tokens
- `02_CHRONOLOGICAL_BREAKDOWN.md` : découpage plan par plan
- `03_FABRICATION_BLUEPRINTS.md` : recettes de code et algorithmes de reproduction
- `04_AUDIO_AND_SOUND_DESIGN.md` : cartographie audio et sound design

N'ancre pas ton motion design précisément sur un exemple : ce sont juste des exemples.

Tu peux aussi chercher des références sur Internet librement (builtin `WebSearch`, plugin `tavily:*`). Tu peux faire ce que tu penses exprimer le mieux visuellement, y compris des motion graphics abstraits.

## 4. Outils externes

### Génération d'images

1. **Seedream 5.0 Pro** (ByteDance via OpenRouter)

C'est le choix idéal si vous intégrez du texte ou des éléments d'interface graphiques complexes dans vos plans. Il excelle dans le rendu de texte précis à plus de 99 % et gère la séparation en calques (Layers), ce qui est parfait pour importer des éléments isolés dans une composition. Le coût est fixe à l'utilisation (0,045 $ à 0,09 $ par image).
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Seedream-5.0-Pro-image-gen.md`

2. **Google Nanobanana 2.1** (Google)

Ce modèle est redoutable pour sa vitesse et son contrôle itératif ultra-rapide. Il est idéal pour générer des arrière-plans fluides ou des textures abstraites à la volée (0,02 $ à 0,03 $ par image).
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Nanobanana-2.1-image-gen.md`

### Bibliothèque d'images libres de droits

Pixabay.com : l'API la plus permissive pour un agent.
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Pixabay.md`

### Bruitages (SFX)

Banque Sonniss GDC 2024 : 609 WAV libres de droits sur Google Drive (`gdrive:sound-fx/GDC2024/`), en complément de la bibliothèque SFX de HyperFrames (`/hyperframes:media-use`). Recherche, téléchargement et pose dans la composition : skill `sonniss-catalog-audio-fx`. Chaque bruitage devient une piste `<audio>` HyperFrames, mixée au rendu avec la musique.

### Voix (Gemini TTS)

Voix off, narration, dialogue à plusieurs personnages : skill `gemini-vocal-generator`. Elle crée des voix sur mesure depuis une description (voice design), synthétise un texte ou un dialogue en WAV, et le pose comme piste `<audio>` dans la composition. Pour une voix off simple avec une voix prête, `/hyperframes:media-use` suffit aussi et donne en prime le minutage des mots pour les sous-titres.

### Musique (Google)

Lyria 3.5 et Lyria 3 Clip, la suite de modèles de génération musicale de Google, accessible via l'API Gemini. Lyria 3.5 génère un son stéréo de haute qualité à 44,1 kHz à partir de textes ou d'images. Ces modèles offrent une cohérence structurelle, incluant les voix, les paroles synchronisées et les arrangements instrumentaux complets.
ModelID `lyria-3-5` et `lyria-3-clip-preview` vérifiés le lundi 28 septembre 2026 sur `https://aistudio.google.com`.
Voir `${CLAUDE_PLUGIN_ROOT}/shared/docs-tools/Lyria-prompt-guide.md`

1. **Lyria 3.5**
   - ModelID : `lyria-3-5`
   - Usage : musique longue
   - Durée : quelques minutes (pilotable par le prompt)
   - Sortie : MP3, 0,10 $ par génération

2. **Lyria 3 Clip**
   - ModelID : `lyria-3-clip-preview`
   - Usage : clips courts, boucles, previews
   - Durée : 30 secondes
   - Sortie : MP3, 0,06 $ par génération

La musique générée se pose dans la composition comme piste `<audio>` marquée `data-timeline-role="music"`. C'est elle que `npx hyperframes beats` analyse pour caler les animations et les bruitages sur les temps.
