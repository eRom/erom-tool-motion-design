# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel et technique de la vidéo `juiGldW_-J9pBs0s.mp4` (vidéo de lancement spéculative et motion showcase : *Claude Opus 5.5 - The world's most intelligent model* par Anthropic). Il fournit à des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas 2D) l'ensemble des tokens, règles géométriques, physiques d'animation et shaders nécessaires pour recréer l'œuvre à l'identique.

---

## 1. Archétype Visuel & Philosophie

L'esthétique de la vidéo incarne le **Humanist High-Tech / Editorial Brutalism** caractéristique de l'identité de marque d'Anthropic, poussé ici à une dynamique cinétique extrême :

1. **Dualité Sombre / Papier Écru (Dark Mode vs Parchment Light Mode)** :
   - Un fond sombre chaud et organique (noir suie teinté d'ombre brûlée `#0A0907` à cœur radial sépia `#281B13`), parsemé de micro-poussières flottantes en apesanteur (bokeh 3D).
   - Des respirations lumineuses brutales sur fond papier crème texturé (`#F1EEE5`), évoquant des carnets d'édition, des formulaires de bureau ou l'interface de lecture épurée de Claude.

2. **Typographie Hybride : Rigueur Grotesque & Sensibilité Éditoriale** :
   - Association systématique et millimétrée entre un **Grotesque ultra-lourd** (bâton géométrique, majuscules et bas-de-casse massifs) pour les verbes d'action et les annonces de puissance.
   - Un **Serif italique chaud et raffiné** (style éditorial littéraire) pour les compléments d'objet, apportant une humanité littéraire contrastant avec la brutalité technologique.
   - Un **Monospace d'ingénierie chirurgical** pour les compteurs, les chemins de fichiers, les invites de commande et les métadonnées télémétriques.

3. **Traitement Optique Analogique & Chaleur Cinématographique** :
   - Rejet total du néon cyberpunk violet ou du bleu corporate aseptisé.
   - Dominante terracotta / corail chaud / saumon (`#CC7152` / `#DE6B48`), halo de bloom doux et diffusion anamorphique horizontale (streak flare cinématographique).
   - Séparation chromatique anaglyphe (RGB chromatic aberration split de 2px à 8px) sur les transitoires percussifs et les cuts staccato.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-dark-base` | `#070604` | Fond sombre profond en périphérie et coins d'écran | Normal |
| `bg-dark-radial` | `#281B13` | Cœur du dégradé radial sombre chaud (ambiance lumineuse) | Normal |
| `bg-paper-light` | `#F1EEE5` | Fond crème papier (scènes mascotte pixel et résultats clients) | Normal |
| `bg-paper-vignette`| `#97978F` | Vignettage périphérique diffus sur fond papier | Multiply |
| `accent-terracotta`| `#CC7152` | Couleur emblématique Anthropic : astérisque, badges, titres serif | Normal / Screen |
| `accent-coral-glow`| `#E99372` / `#F08C69` | Cœur incandescent de l'astérisque, halos et lens flare | Additif (`screen` / `lighter`) |
| `accent-light-peach`| `#F6C4B2` | Variantes claires de curseurs, bulles de prompt et surbrillance | Normal |
| `text-primary-dark`| `#F3EFE6` | Typographie principale sur fond sombre (ivoire optique) | Normal |
| `text-secondary-dark`| `#8E8A82` | Métadonnées, chemins UNIX, sources en bas d'écran | Normal |
| `text-primary-light`| `#11120C` | Typographie principale et yeux de la mascotte sur fond crème | Normal / Multiply |
| `card-surface-dark`| `rgba(30, 24, 20, 0.75)` | Cartes de benchmarks, fenêtres terminales, conteneurs HUD | Normal / Backdrop-filter blur |
| `card-border-warm` | `rgba(204, 113, 82, 0.25)`| Liseré des cartes en verre sombre et séparateurs | Normal / Screen |
| `rgb-split-red` | `#FF2A2A` | Frange rouge de l'aberration chromatique anaglyphe | Screen / Lighten |
| `rgb-split-cyan` | `#00E5FF` | Frange cyan de l'aberration chromatique anaglyphe | Screen / Lighten |

### 2.2. Stack Typographique & Rôles

Le système s'articule autour de quatre familles rigoureusement typées :

1. **Display Grotesque Géométrique Massif** (*Favorit*, *Styrene A*, *Neue Haas Grotesk Bold*) :
   - **Usage** : Titres monumentaux ("From question", "Opus 5.5", "Operates", "Builds", "Catches errors", "Refactors.", "Designs.", "Works solo.", "Your whole project", "#1 IN THE WORLD").
   - **Graisse** : `Bold` (700) à `Black` (900).
   - **Letter-spacing** : `-0.03em` à `-0.04em` (tracking très serré pour un impact compact).
   - **Casse** : Title Case pour les annonces majeures, Majuscules strictes pour les badges records.

2. **Editorial Serif Italique Raffiné** (*Canela Italic*, *Editorial New Italic*, *Tiempos Headline Light Italic*) :
   - **Usage** : Segments poétiques ou narratifs contrastés ("to finished work.", "your computer.", "in the terminal.", "For hours.", "in memory.", "At once.", "Writes clearly.", "No fluff.").
   - **Graisse** : `Regular Italic` (400i) ou `Light Italic` (300i).
   - **Couleur** : Systématiquement teinté en `accent-terracotta` (`#CC7152`), créant la signature visuelle du film.
   - **Letter-spacing** : `0em` à `-0.01em`.

3. **Monospace d'Ingénierie & Télémétrie** (*Berkeley Mono*, *JetBrains Mono*, *SF Mono*) :
   - **Usage** : Invites de commande (`> claude --model`), télémétrie de prompt (`PROMPT 02 / 13`), arborescence de fichiers, code Rust/Python, horloge d'autonomie (`UNSUPERVISED 15:56h`), mentions de sources.
   - **Graisse** : `Medium` (500) et `Regular` (400).
   - **Letter-spacing** : `+0.04em` sur les étiquettes en capitales, `0em` sur les blocs de code.

4. **Script Cursive Manuscrite Organique** (*Claude Brand Script* / *Reenie Beanie*) :
   - **Usage** : Signature manuscrite de marque "Claude" survolant le titre monumental "Opus 5.5" (00:20 et 01:09).
   - **Positionnement** : Décalé vers le haut-gauche, angle d'inclinaison de -5°.

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : 1920x1080 (16:9), cadencée à **60.0 fps** stricts.
- **Grille de composition** :
  - Composition asymétrique 40/60 : Le texte d'annonce occupe le tiers gauche de l'écran ($X \in [120\text{px}, 720\text{px}]$), tandis que la démonstration interactive (fenêtre Mac, graphique, carrousel) occupe les deux tiers droits ($X \in [760\text{px}, 1800\text{px}]$).
  - Ligne de repère télémétrique en bas d'écran : filet fin de 1px (`rgba(255, 255, 255, 0.15)`) à $Y = 1010\text{px}$, ancré à gauche par le libellé d'étape (ex: `PROMPT 02 / 13`, `CUSTOMER RESULTS • 03 / 06`).
- **Caméra & Transformations 3D** :
  - **Perspective spatiale** : Les fenêtres d'application (Terminal, Browser ERP, Editeur de code, Vue mémoire) sont projetées en CSS 3D avec une perspective de `1200px`, une rotation `rotateY(-12deg)` et `rotateX(4deg)`, conférant une profondeur physique tangible.
  - **Caméra Fly-through (Vortex)** : Translation en $Z$ de $+1500\text{px}$ à $-4000\text{px}$ à travers les anneaux de tokens lors de la phase d'accélération (00:11 - 00:20).
  - **Micro-secousses (Camera Shakes)** : Déplacements aléatoires de 2px à 5px sur l'axe $X/Y$ synchronisés sur les transitoires de kick et les chutes de cartes.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels
- **Tempo musical** : **89.1 BPM** (Groove hip-hop syncopé avec kicks lourds, claps nets et chops vocaux).
- **Durée par temps (Beat)** : `0.6734 seconde` = **40.4 frames** à 60 fps.
- **Durée par demi-temps (8th note)** : `0.3367 seconde` = **20.2 frames** à 60 fps.
- **Durée par mesure (Bar - 4/4)** : `2.694 secondes` = **161.6 frames** à 60 fps.
- **Fréquence des coupes rapides** :
  - Carrousel des prompts (00:05 - 00:11) : Coupes calées sur les demi-temps (toutes les 20 à 25 frames).
  - Smash cuts cinétiques (00:34 - 00:37) : Coupes franches tous les 1 temps musical (40 frames).

### 4.2. Courbes d'Easing Clés

1. **Snap & Heavy Settle (Power 4 Out)** :
   - Formule : `cubic-bezier(0.12, 1, 0.22, 1)`.
   - Utilisation : Arrivée des cartes de démonstration depuis la droite, apparition de la typographie monumentale.
   - Dynamique : Parcours de 85% de la distance en 6 frames, stabilisation feutrée sur les 18 frames restantes.

2. **Damped Spring (Ressort Physique)** :
   - Paramètres : `mass: 1.0, stiffness: 280, damping: 20`.
   - Utilisation : Rebond des badges `RECORD`, claquage des cartes Kanban, saut de la mascotte pixel sur le slider de pensée.
   - Comportement : Dépassement (overshoot) d'environ 8% avec extinction rapide des oscillations en 12 frames.

3. **Keplerian Orbital Decay (Rotation Accélérée)** :
   - Formule : $\theta(t) = \theta_0 + \omega_0 \cdot t + \frac{1}{2}\alpha \cdot t^2$.
   - Utilisation : Rotation des anneaux de tokens dans le vortex d'accrétion (00:11 - 00:20).

---

## 5. Pipeline de Post-Processing & Effets Shader

Pour reproduire la patine organique caractéristique du film :

1. **Lueur & Bloom Gaussien (Glow Shader)** :
   - Rendu additif (`screen` ou `lighter`) avec flou à deux passes :
     - Rayon interne chaud : $\sigma_1 = 8\text{px}$, intensité $0.8$, teinte `#F08C69`.
     - Rayon externe diffus : $\sigma_2 = 48\text{px}$, intensité $0.35$, teinte `#CC7152`.

2. **Faisceau Anamorphique Horizontal (Streak Flare)** :
   - Ligne lumineuse continue traversant l'écran sur l'axe central $Y = 540\text{px}$.
   - Décroissance exponentielle verticale : $I(y) = I_0 \cdot \exp(-|y - y_0| / 1.5\text{px})$.
   - Largeur : Étirement horizontal infini avec atténuation douce aux extrémités gauche/droite via un masque alpha linéaire.

3. **Aberration Chromatique Anaglyphe (RGB Channel Separation)** :
   - Séparation des canaux lors des impacts :
     - Décalage canal Rouge : $(-d_x, 0)$ avec $d_x \in [3\text{px}, 8\text{px}]$.
     - Décalage canal Cyan (Vert + Bleu) : $(+d_x, 0)$.
   - Décroissance exponentielle rapide : $d_x(t) = d_{\max} \cdot \exp(-t / 0.15\text{s})$.

4. **Grain de Film 35mm & Poussières Dynamiques (Film Grain & Dust)** :
   - Bruit monochromatique animé régénéré à 60 fps avec opacité de $4\%$ en mode `overlay`.
   - Particules de poussières flottantes (30 à 60 sprites circulaires flous de diamètre 1px à 3px, opacité 15% à 40%, dérivant selon un bruit de Perlin 2D).
