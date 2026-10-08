# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du système visuel, des tokens de design et des principes mathématiques de la vidéo de référence `lKqtgjU14TGobAjN.mp4` (*CLAUDE / MOTION REEL '26* - *Every keyframe written in code*). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP).

---

## 1. Archétype Visuel & Philosophie

L'esthétique du film repose sur une synthèse entre trois univers :
1. **Éditorial Suisse & Typographie Brutaliste** : Grands corps de texte en grotesque géométrique compacte (*Inter Tight Display* / *Neue Haas Grotesk*), hiérarchie typographique millimétrée, titraille massive en majuscules avec tracking négatif serré, et contraste absolu entre fond crème chaud et noir charbon profond.
2. **HUD Technique & Télémétrie Caméra (Computer Vision / Viewfinder)** : Cadre d'instrumentation permanent à quatre cornières `[ ]`, running timecode frame-accurate au millième (`TC 00:00:SS:FF`), jauges d'état par discipline, grille de repère à trame de points (*polka dot matrix* 48px), et barres de progression horizontales indexées sur la timeline.
3. **Identité Anthropic / Claude épurée** : Palette chromatique signature combinant le papier ivoire chaud (`#EBE7DB`) et la terre cuite industrielle (*Claude Terracotta / Coral* `#C5593C`). Démonstration didactique de principes d'animation purs (les 12 principes de Disney réinterprétés par le code : squash & stretch, morphing vectoriel, courbes d'asservissement d'easing, et construction géométrique de marque).

Le style rejette tout ornement superflu (aucun dégradé violet générique, aucun effet néon artificiel). Chaque pixel répond à une fonction géométrique, typographique ou analytique explicite.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-primary-cream` | `#EBE7DB` | Fond principal papier ivoire chaud omniprésent | Normal |
| `accent-terracotta` | `#C5593C` | Accent primaire : balle, fond plein cinétique, courbes d'easing, astérisque Claude, curseur | Normal |
| `accent-terracotta-dark` | `#A8452B` | Ombre portée de la balle, facettes inclinées du morphing | Normal / Multiply |
| `accent-terracotta-soft` | `#E0876E` | Onde de choc circulaire (onde radar), reflets intermédiaires | Normal / Screen |
| `text-primary-charcoal` | `#1C1917` | Typographie principale, titres massifs, barres du graphique, cornières HUD | Normal |
| `text-secondary-muted` | `#8A877E` | Métadonnées HUD, libellés secondaires, sous-titres techniques | Normal |
| `watermark-tan` | `#DFD9CC` | Filigranes géants d'arrière-plan ("RHYTHM", "DEPTH") | Normal (opacité 0.20 sur fond crème) |
| `grid-dot-color` | `#C5C0B3` | Points de la matrice de fond (diamètre 3px, pas 48px) | Normal (opacité 0.35) |
| `card-surface-white` | `#FAF8F5` | Face avant des fiches d'easing dans le carrousel 3D | Normal |
| `hud-baseline` | `rgba(28, 25, 23, 0.20)` | Ligne de sol continue et axes de repère | Normal |

### 2.2. Stack Typographique & Règles d'Usage

Le film met en scène deux familles typographiques complémentaires :

1. **Grotesque Géométrique Compacte / Heavy Display** (ex: *Inter Tight Display*, *Neue Haas Grotesk*, *Söhne Breit*) :
   - Usage : Titres massifs en kinetic typography ("EVERY", "FRAME", "IS A", "DECISION.", "CLAUDE", "EASE IS EMOTION."), filigranes de fond ("RHYTHM", "DEPTH").
   - Graisse : `Black` (900) ou `Heavy` (800), majuscules obligatoires.
   - Paramètres CSS :
     - Titres cinétiques : `font-size: 200px; font-weight: 900; letter-spacing: -0.04em; line-height: 0.9;`
     - Filigranes de fond : `font-size: 300px; font-weight: 900; letter-spacing: +0.02em; color: #DFD9CC;`
     - Titre "CLAUDE" : `font-size: 266px; font-weight: 900; letter-spacing: -0.03em; line-height: 1.0; color: #1C1917;`
     - "EASE IS EMOTION." : `font-size: 72px; font-weight: 900; letter-spacing: -0.02em;` avec "EMOTION." coloré en `#C5593C`.

2. **Monospace Technique / Code HUD** (ex: *Geist Mono*, *JetBrains Mono*, *SF Mono*) :
   - Usage : Repères de visée HUD, timecode (`TC 00:00:SS:FF`), labels d'onglets (`01 / SQUASH & STRETCH`), odomètre numérique (`0` à `450`), équations et noms d'easing (`expo.out`, `back.out(1.6)`), sous-titre dactylographié (`MOTION DESIGNER · REEL 2026`), et métadonnées techniques.
   - Graisse : `Regular` (400) et `Medium` (500), majuscules sur les labels HUD, minuscules sur les identifiants de code.
   - Paramètres CSS :
     - Timecode & Cornières : `font-size: 16px; font-weight: 500; letter-spacing: +0.06em;`
     - Compteur de frames géant : `font-size: 180px; font-weight: 700; letter-spacing: -0.03em;`
     - Sous-titre machine à écrire : `font-size: 36px; font-weight: 500; letter-spacing: +0.08em;`
     - Tagline de pied de page : `font-size: 22px; font-weight: 500; letter-spacing: +0.06em;`

---

## 3. Grille, Cadrage & Viewfinder HUD

### 3.1. Résolution & Espacement
- **Résolution native** : `1920x1080` (format 16:9), cadencée à **30.0 fps** progressifs (durée totale : 452 frames = 15.061 secondes).
- **Marges de visée (Viewfinder Bounds)** : Marge périphérique constante de **40px** sur tous les bords.
  - Coin supérieur gauche : `(X: 40, Y: 40)`
  - Coin supérieur droit : `(X: 1880, Y: 40)`
  - Coin inférieur gauche : `(X: 40, Y: 1040)`
  - Coin inférieur droit : `(X: 1880, Y: 1040)`
- **Cornières de cadrage (Corner Brackets)** :
  - Tracé en équerre à angle droit : épaisseur de trait `2px`, longueur de chaque branche `20px`, couleur `#1C1917`.

### 3.2. Grille Matricielle Modulaire (Modular Dot Grid)
- Trame orthogonale régulière de points couvrant tout l'espace intérieur du viewport.
- **Pas de la grille (Pitch)** : **48px $\times$ 48px** exacts ($1920 / 48 = 40$ colonnes, $1080 / 48 = 22.5$ rangées).
- **Géométrie des points** : Disque plein de rayon $r = 1.5px$ (diamètre 3px), couleur `#C5C0B3` (`rgba(28, 25, 23, 0.20)`).
- Rôle technique : Fournit un repère cartésien permanent et sert de matrice nodale active lors de la transition vers la scène 02.

### 3.3. Architecture du HUD Permanent (Scene Graph Global)
Le HUD forme une surcouche de niveau Z supérieur (`Z-Index: 100`) immuable tout au long du film :
- **Bandeau Supérieur (Y = 64px)** :
  - Flanc gauche (`X = 40px`) : Puce pleine `●` suivie de `CLAUDE / MOTION REEL '26`.
  - Flanc droit (`X = 1700px`) : Libellé `TC` suivi du timecode frame-accurate au format `00:00:SS:FF` mis à jour à chaque frame.
- **Bandeau Inférieur (Y = 1010px à 1030px)** :
  - Libellé d'état gauche (`X = 40px, Y = 1010px`) : Numéro et intitulé de la discipline active (`01 / SQUASH & STRETCH`, etc.).
  - Libellé technique droit (`X = 1680px, Y = 1010px`) : `1920x1080 · 30 FPS`.
  - Ligne de sol continue (`Y = 1030px`) : Tracé horizontal de $X = 40px$ à $X = 1880px$ (épaisseur 1px, `#C5C0B3`).
  - Jauge de progression locale : Segment noir d'épaisseur 3px superposé à la ligne de sol, partant de $X = 40px$ et s'allongeant proportionnellement à l'avancement de la discipline active ($0\%$ à $100\%$).

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Métriques Temporelles Clés
- **Tempo musical** : **129.2 BPM** (~130 BPM électro-glitch).
- **Durée d'un temps (Beat)** : `0.4644 seconde` = **13.93 frames** à 30 fps (~14 frames).
- **Durée d'une mesure (Bar 4/4)** : `1.858 seconde` = **55.73 frames** à 30 fps (~56 frames).
- **Totalité de la timeline** : Exactement **8 mesures complètes 4/4** (446 frames) + **6 frames d'extinction/hold** = **452 frames**.

Chaque discipline occupe une fenêtre temporelle rigoureusement indexée sur les mesures musicales :
- **Discipline 01** (`SQUASH & STRETCH`) : Mesures 1 et 2 (Frames 0 à 100).
- **Discipline 02** (`SHAPE & RHYTHM`) : Mesures 3 et première moitié de la mesure 4 (Frames 101 à 180).
- **Discipline 03** (`DATA IN MOTION`) : Deuxième moitié de la mesure 4 et mesure 5 (Frames 181 à 270).
- **Discipline 04** (`DEPTH & EASE`) : Mesures 6 et première moitié de la mesure 7 (Frames 271 à 360).
- **Discipline 05** (`IDENTITY`) : Deuxième moitié de la mesure 7 et mesure 8 (Frames 361 à 452).

### 4.2. Profils Mathématiques d'Easing

L'animation met en pratique quatre fonctions de transfert canoniques :

1. **Exponential Decay Out (`expo.out`)** :
   $$f(t) = 1 - 2^{-10t} \quad \text{pour } t \in [0, 1]$$
   - Caractéristique : Vélocité initiale explosive (80% de la course parcourue sur les 25% premiers du temps), atterrissage asymptotique infiniment doux sans aucun dépassement (*overshoot*).
   - Utilisation : Arrivée des mots en kinetic typography, course du curseur, étalonnage de la courbe de référence dans la scène 03.

2. **Damped Harmonic Oscillator (Squash & Stretch Spring)** :
   $$y(t) = y_{rest} + A \cdot e^{-\zeta \omega_n t} \cos\left(\omega_d t + \phi\right)$$
   - Paramètres : $\zeta = 0.45$ (sous-amorti), $\omega_n = 18 \text{ rad/s}$.
   - Règle de conservation volumétrique : $s_x(t) \cdot s_y(t) = 1.0$. Lors de l'écrasement sur le sol, $s_y = 0.38 \implies s_x = \frac{1}{0.38} \approx 2.63$.

3. **Power 4 Smooth In-Out (`power4.inOut`)** :
   $$f(t) = \begin{cases} 8 t^4 & \text{si } t < 0.5 \\ 1 - 8 (1 - t)^4 & \text{si } t \ge 0.5 \end{cases}$$
   - Utilisation : Balayage du volet biseauté de transition entre les scènes 02 et 03, rotation cyclique du carrousel 3D.

4. **Linear Drift (`linear`)** :
   $$f(t) = t$$
   - Utilisation : Progression du timecode, rotation continue du champ vectoriel de bâtonnets, droite de comparaison dans la scène 03.

---

## 5. Pipeline de Post-Processing & Finition Visuelle

Pour assurer un rendu identique à l'export Remotion ou WebGL :
1. **Grain de Papier Organique** : Bruit monochromatique à haute fréquence (taille de grain 1px, opacité 3.5%, blend mode `overlay`) appliqué sur le calque de fond `#EBE7DB` pour simuler le grain d'un papier à dessin texturé et éliminer tout banding de compression.
2. **Ombres de Contact Dynamiques** : Les ombres au sol sous la balle et sous les éléments reposent sur une ellipse floutée (`filter: blur(4px)`), dont l'opacité ($0.15 \to 0.65$) et la largeur ($40px \to 180px$) sont inversement proportionnelles à la hauteur de l'objet au-dessus de la ligne de sol.
3. **Motion Blur Mathématique** : Calibré à un angle d'obturateur virtuel de $180^\circ$ (équivalent $1/60s$ à 30fps) uniquement sur les déplacements dont la vitesse dépasse $800px/s$ (chute de la balle, balayage du volet de transition).
