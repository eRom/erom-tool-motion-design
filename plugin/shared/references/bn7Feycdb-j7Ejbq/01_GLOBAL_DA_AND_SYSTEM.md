# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, géométrique et cinématique de la vidéo `bn7Feycdb-j7Ejbq.mp4` (titre officiel : *UPPING MY P(DOOM) - MADEWITHV DnB REMIX*, moteur graphique : *pdoom-video by Mexicat (MIT)*, remix Drum & Bass par *madewithv*, voix pop Claude par *deckard / @slimer48484*, paroles par *osmarks, MusicPerson & EleutherAI Discord*).

Ce dossier de spécification est calibré pour être ingéré directement par des agents codeurs autonomes (Three.js/WebGL, GLSL shaders, Remotion, Canvas 2D, SVG).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de cette version constitue une réinterprétation radicale de la vidéo originelle de Mexica :
1. **Y2K Liquid Chrome & Specular Refraction** : Les typographies massives et symboles clés sont traités en métal liquide chromé 3D avec biseautage prononcé, reflets d'environnement iridescents (dégradés dynamiques cyan-violet-blanc) et scintillements d'étoiles spéculaires à quatre branches (*glints*) sur les arrêtes vives.
2. **Cyber-Rave & Dark Cosmic Violet** : Le noir d'encre académique de l'original cède la place à un vide spatial violet profond (`#07070F` à `#141318`), zébré d'auras électriques néon pourpre/magenta (`#8C5ABC`, `#9D4EDD`) et de faisceaux d'accélération hyperspatiale.
3. **Double Système Typographique Plein / Filaire (Ghost Overlays)** : Chaque mot-clé en typographie chromée pleine est systématiquement doublé ou précédé par son double en filaire technique (`stroke: 1.5px`, fill transparent), créant une sensation de wireframe CAO sous-jacent.
4. **Télémétrie HUD Continue & Tickers Périphériques** : Deux bandeaux horizontaux de texte en micro-monospace (`UPPING MY P(DOOM) - MADEWITHV`) défilent en continu en bordure d'écran (y = 28px et y = 1052px), tandis qu'un compteur de risque existentiel en bas à droite (`P(DOOM) 2.5%` jusqu'à `NaN`) cadence mathématiquement l'escalade de la vidéo.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-midnight-void` | `#07070F` | Fond principal violet-noir cosmique | Normal |
| `bg-elevated-surface` | `#141318` | Cartouches HUD, sous-couches de panneaux et boîtes terminal | Normal |
| `bg-glitch-deep` | `#221040` | Fond saturé lors des phases de saturation stroboscopique et glitch | Normal / Addition |
| `chrome-specular-white` | `#F0F9FE` | Crêtes de reflets et points de brillance spéculaire des textes 3D | Additif (`screen` / `lighter`) |
| `chrome-iridescent-cyan` | `#86ADCE` / `#67D4E8` | Reflets de Fresnel froids sur le biseau chromé | Normal / Overlay |
| `chrome-iridescent-purple` | `#C4A7E7` / `#D8B4FE` | Teinte zénithale et reflets chauds sur les surfaces métalliques | Normal / Screen |
| `chrome-shadow-deep` | `#1C1E2A` / `#2A2640` | Creux de biseau et ombrage interne des glyphes métalliques | Normal |
| `accent-neon-violet` | `#8C5ABC` / `#9D4EDD` | Auras électriques, ondes de choc, décharges d'énergie, bordures HUD | Screen / Lighter |
| `accent-electric-cyan` | `#48CAE4` / `#00F5D4` | Réticules télémétriques, pointeurs de visée, tags de statut | Normal |
| `accent-alert-crimson` | `#EF4444` / `#F43F5E` | Alertes de rupture de sécurité (`SAFETY CHECK PASSED / NOT HELD`) | Normal |
| `wireframe-stroke` | `rgba(147, 129, 255, 0.45)` | Tracés vectoriels des lettres fantômes et maillages isométriques | Normal |
| `ticker-text-lavender` | `#9381FF` / `#A78BFA` | Micro-monospace des bandeaux de défilement supérieur et inférieur | Normal |
| `text-primary-white` | `#FFFFFF` | Typographie principale plein texte, sous-titres karaoké, libellés | Normal |
| `text-secondary-slate` | `#7E7B9A` / `#94A3B8` | Métadonnées secondaires, numéros d'étapes, labels d'axes (`STEP 42000`) | Normal |
| `grid-axis-line` | `rgba(168, 85, 247, 0.18)` | Lignes d'axes cartésiens et séparateurs de sections | Normal |

### 2.2. Typographie & Rôles

Le film orchestre quatre registres typographiques stricts :

1. **Display Monumentale Grotesque 3D (Chrome Hero)** (ex: *Druk Wide Heavy*, *Neue Haas Grotesk 900*, *Syne Extra Bold*) :
   - Usage : Mots clés majeurs au centre de l'impact sonore (`SPARKS`, `LOSS`, `THE FUTURE GOES`, `LIES`, `EYES`, `OMEGA`, `ASKEW`, `ILYA`).
   - Poids : `Black` (900), casse majuscule exclusive.
   - Traitement : Extrusion 3D (profondeur z = 18px à 40px), biseau à 45 degrés avec shader matcap iridescent et reflets lumineux spéculaires à 4 branches.

2. **Filaire Technique Fantôme (Ghost Wireframe Display)** :
   - Usage : Doublure des mots clés, placée directement derrière ou décalée en profondeur Z, et typographies secondaires de fond (`AGI`, `DOOM`, `STABLE`, `WHAT DID`).
   - Traitement : `fill: transparent`, `stroke: 1.5px rgba(147, 129, 255, 0.45)`, géométrie vectorielle apparente.

3. **Monospace Télémétrique & HUD** (ex: *JetBrains Mono*, *SF Mono*, *Space Mono*) :
   - Usage : Compteur permanent `P(DOOM) 2.5%` -> `NaN`, coordonnées, étapes d'optimisation (`STEP 186358`, `LOSS 0.0398`), couches d'attention (`LAYER 01 - ATTN + MLP`), labels de tokens BERT (`[mask]`, `@batch`, `[cls]`, `[sep]`).
   - Poids : `Regular` (400) et `Medium` (500).
   - Espacement : `letter-spacing: +0.06em`.

4. **Micro-Monospace des Tickers (Bordures)** :
   - Usage : Tickers continus supérieur (`y = 28px`) et inférieur (`y = 1052px`).
   - Poids : `Semi-Bold` (600), taille `11px`, `letter-spacing: 0.18em`.
   - Contenu répété : `UPPING MY P(DOOM) - MADEWITHV - UPPING MY P(DOOM) - MADEWITHV`.

5. **Sans-Serif Épurée Cartel** (ex: *Inter*, *Helvetica Neue Regular*) :
   - Usage unique : Cartouche minimaliste central `We'll never know.` (03:12 / 11520f) sur plaque noire rectangulaire compacte.

---

## 3. Grille, Cadrage & Composition

- **Résolution native** : 1920x1080 (16:9), cadencée à 60.0 fps constants.
- **Bandeaux Tickers (Safe Margins)** :
  - Bandeau haut : `y = 0px` à `y = 52px`. Ligne de défilement centrée à `y = 28px`.
  - Bandeau bas : `y = 1028px` à `y = 1080px`. Ligne de défilement centrée à `y = 1052px`.
  - Zone utile d'animation libre : `1920x976px` (de `y = 52px` à `y = 1028px`).
- **Ancrages Télémétriques Fixes** :
  - **Module P(DOOM)** (Coin inférieur droit) :
    - Label `P(DOOM)` à `x = 1650px`, `y = 905px`, font monospace 12px, couleur `#7E7B9A`.
    - Valeur chiffrée (ex: `12.9%`, `61.8%`, `NaN`) à `x = 1650px`, `y = 935px`, font monospace bold 28px, couleur `#FFFFFF`.
    - Ligne de progression horizontale de 200px sous la valeur, remplie proportionnellement de `#8C5ABC`.
  - **Module Sous-titres Karaoké** :
    - Ancrage en bas au centre (`y = 940px`), alignement gauche ou centré.
    - Style : Texte blanc avec traitement chrome atténué, mots chantés s'allumant en blanc plein.
  - **Module Métadonnées Haut-Gauche / Haut-Droite** :
    - Statuts d'exécution (`TRAINING RUN - LOSS`, `STATUS: RUNNING`, `ETA: CALCULATING`) calés à `x = 60px` et `x = 1580px`, `y = 80px`.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels Drum & Bass

Le montage et l'animation sont verrouillés sur un tempo Drum & Bass rigoureusement mesuré :
- **Tempo musical** : **172.26 BPM** (~172.3 BPM).
- **Durée d'un temps (Beat)** : `0.3483 seconde` = **20.90 frames** à 60 fps.
- **Durée d'une mesure (Bar 4/4)** : `1.3932 seconde` = **83.60 frames** à 60 fps.
- **Durée d'une croche (8th note)** : `0.1741 seconde` = **10.45 frames** à 60 fps.
- **Durée d'une double-croche (16th note breakbeat)** : `0.0871 seconde` = **5.22 frames** à 60 fps.

### 4.2. Courbes d'Easing Clés

Les mouvements obéissent à trois profils cinématiques chiffrés :

1. **DnB Snap & Settle (Expo Out Agressif)** :
   - Formule : `cubic-bezier(0.05, 0.9, 0.1, 1.0)`.
   - Utilisation : Arrivée des mots monumentaux en kinetic typo sur chaque snare et kick.
   - Comportement : 85% de la course parcourue en 4 frames (66ms), décélération abrupte sur les 10 frames suivantes.

2. **Sub-Bass Spring Rebound** :
   - Paramètres ressort : `mass: 0.8, stiffness: 320, damping: 14`.
   - Utilisation : Échelle caméra sur les drops de batterie et secousses d'impact des blocs de sécurité.
   - Comportement : Overshoot de 12% avec 2 oscillations ultra-serrées (cycle complet en 8 frames).

3. **Hyper-Speed Linear Conveyor** :
   - Easing : `linear`.
   - Utilisation : Translation des rubans tickers haut/bas (défilement régulier de 3.5px par frame), défilement du tunnel de cristaux et de la ligne de barrières de sécurité.

---

## 5. Post-Processing & Pipeline Shaders

Le rendu visuel s'appuie sur une chaîne de 5 passes de post-traitement en temps réel :

1. **Passe MatCap & Fresnel Iridescent (Matériau 3D)** :
   - Texture d'environnement hémisphérique combinant blanc froid, cyan électrique et pourpre profond.
   - Facteur de Fresnel : `F = F0 + (1.0 - F0) * pow(1.0 - dot(N, V), 3.5)` injectant du cyan `#67D4E8` et du magenta `#D8B4FE` sur les normales tangentes.
2. **Passe Glint Spéculaire (Cross Flare)** :
   - Détection des pixels de luminance > 0.92 sur les géométries 3D.
   - Génération d'étoiles spéculaires à 4 branches orientées à 45 degrés avec décroissance exponentielle.
3. **Passe Bloom Volumétrique (UnrealBloomPass)** :
   - Résolution : 1920x1080.
   - Paramètres : `strength: 1.15`, `radius: 0.75`, `threshold: 0.62`.
4. **Passe Aberration Chromatique & Dispersion Radiale** :
   - Décalage RVB : Repos à 1.5px dans les coins ; pics d'impulsion à 8px - 14px sur les coups de caisse claire (snare) et impacts majeurs.
5. **Passe Glitch & Tranches CRT (Scanline Slice Jitter)** :
   - Découpage stochastique en bandes horizontales de 4px à 24px de hauteur avec décalage horizontal aléatoire (`dx = [-35px, +35px]`) actif lors des drops et des transitions d'accélération exponentielle.
