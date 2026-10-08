# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du système visuel, des tokens de design et des principes mathématiques de la vidéo de référence `Ug6RUqJ59vKTsnPX.mp4` (*CLAUDE / MOTION REEL - 2026* - *15 Seconds · Every Frame Written in Code*). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de la vidéo repose sur une collision maîtrisée entre trois univers stylistiques :

1. **Éditorial Brutaliste & Typographie Hybride** : Confrontation radicale entre une typographie grotesque ultra-lourde en capitales compactes (*Neue Haas Grotesk / Inter Tight Display / Druk Wide*) et un serif italique fluide d'inspiration Didone/Bodoni à fort contraste de plein et délié (*Playfair / Instrument Serif*). Rejet de tout ornement gratuit : les mots occupent l'espace comme des blocs architecturaux.
2. **HUD Télémétrique & Instrumentation Caméra (Computer Vision / Viewfinder)** : Cadre d'instrumentation permanent à quatre cornières d'angle `[ ]`, running timecode à la cadence native (`00:00:SS:FF`), moniteur de tempo (`128 BPM`), compteur de mesures interactif (`■□□□ BAR X/8`), indicateur de framerate (`60 FPS`), et annotations télémétriques de simulation (`SPRING F=2.6 ζ=0.30`, `TRUCHET x 153`, `VERTICES 576 · FOCAL 1400`).
3. **Didactique Algorithmique & Rendu Procédural Pur** : Chaque plan illustre un chapitre fondamental de l'ingénierie visuelle (01 Identity, 02 Easing, 03 Morphing, 04 Systems, 05 Depth, 06 Kinetic Type, 07 Fin). L'animation ne triche jamais : les trajectoires, courbes d'asservissement, déformations de ressorts, pavages et projections 3D sont calculés mathématiquement à chaque photogramme.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-dark-onyx` | `#0F0F11` | Fond sombre principal (Scènes 01, 04, 05, 06 fin) | Normal |
| `accent-vermilion` | `#F04B38` | Rouge-orange signature Claude / Anthropic (Fond Scènes 01.2 & 07, accent dots, curves) | Normal |
| `bg-cream-paper` | `#F2EFE6` | Fond ivoire / papier chaud (Scène 02 Easing, Scène 06 flash) | Normal |
| `accent-cobalt-electric` | `#302FF5` | Bleu royal saturé (Fond Scène 03 Morphing, balle Easing 02 & 05, flash Scène 06) | Normal |
| `accent-lime-chartreuse` | `#E3FF44` | Jaune-vert acide électrique (Fond Scène 06 "NEVER") | Normal |
| `text-dark-charcoal` | `#090806` | Titres géants "CLAUDE" sur fond rouge, "NEVER" sur fond lime, balle linear | Normal |
| `text-light-cream` | `#F2EFE6` | Textes et formes blanches sur fonds sombre, cobalt et rouge | Normal |
| `hud-wire-light` | `#EAEAEC` | Cornières de cadrage et labels télémétriques sur fonds sombres | Normal |
| `hud-wire-dark` | `#1C1917` | Cornières de cadrage et labels télémétriques sur fond crème et fond lime | Normal |
| `trail-geometry-ghost` | `rgba(240, 75, 56, 0.25)` | Lignes de fuite et sillages géométriques pendant le morphing | Screen / Additive |
| `shockwave-bloom` | `rgba(255, 230, 200, 0.85)` | Halo lumineux de l'onde de choc circulaire (Scène 07) | Screen / Additive |

### 2.2. Stack Typographique & Règles d'Usage

Trois familles typographiques strictement cloisonnées par rôle :

1. **Grotesque Brutaliste / Heavy Display** (ex: *Inter Tight Display*, *Neue Haas Grotesk*, *Druk Wide*) :
   - Usage : Titres massifs "CLAUDE", "NEVER", "LINEAR."
   - Graisse : `Black` (900) ou `Heavy` (800), majuscules obligatoires.
   - Paramètres CSS :
     - "CLAUDE" (Scène 01.2) : `font-size: 260px; font-weight: 900; letter-spacing: -0.03em; line-height: 0.9;`
     - "NEVER" (Scène 06) : `font-size: 220px; font-weight: 900; letter-spacing: -0.02em;`
     - "LINEAR." (Scène 06) : `font-size: 240px; font-weight: 900; letter-spacing: -0.04em;`
     - Titre final "CLAUDE" (Scène 07) : `font-size: 240px; font-weight: 900; letter-spacing: -0.03em;`
   - Déformation cinétique (Scène 01.2) : Modulation asymétrique de la largeur des glyphes (variable font `wdth` ou matrice `scaleX(1.8)` sur le "C" et `scaleX(0.7)` sur "LAUDE").

2. **Serif Éditorial Italique / Contrast Display** (ex: *Playfair Display Italic*, *Instrument Serif Italic*, *Ogg*) :
   - Usage : Sous-titre signature `motion designer`, titre de démonstration `Six ways to get from A to B.`
   - Graisse : `Regular` (400) ou `Medium` (500), minuscules calligraphiées avec empattements nets et ligatures.
   - Paramètres CSS :
     - `motion designer` : `font-size: 110px; font-style: italic; font-weight: 400; letter-spacing: -0.01em;`
     - `Six ways to get from A to B.` : `font-size: 68px; font-style: italic; font-weight: 400; letter-spacing: -0.01em;`

3. **Monospace Technique / HUD Télémétrique** (ex: *Geist Mono*, *JetBrains Mono*, *SF Mono*) :
   - Usage : Viewfinder HUD, timecode, BPM, barre de mesure, noms d'easings (`01 linear`, etc.), étiquettes télémétriques de transformation, footer technique.
   - Graisse : `Regular` (400) et `Medium` (500), majuscules pour les métadonnées, chiffres tabulaires (`font-variant-numeric: tabular-nums`).
   - Paramètres CSS :
     - HUD Timecode & Status : `font-size: 14px; font-weight: 500; letter-spacing: +0.08em;`
     - Easing Labels : `font-size: 20px; font-weight: 500; letter-spacing: +0.04em;`
     - Footer Final : `font-size: 14px; font-weight: 500; letter-spacing: +0.10em;`

---

## 3. Grille, Cadrage & Viewfinder HUD

### 3.1. Résolution & Cadence Native
- **Résolution native** : `1920x1080` (format 16:9).
- **Framerate exact** : **60.0 fps** progressifs (durée totale : 904 frames = 15.061 secondes).
- **Marges de visée (Viewfinder Inset)** : Retrait périphérique uniforme de **44px** sur les 4 bordures.
  - Coin supérieur gauche : `(X: 44, Y: 44)`
  - Coin supérieur droit : `(X: 1876, Y: 44)`
  - Coin inférieur gauche : `(X: 44, Y: 1036)`
  - Coin inférieur droit : `(X: 1876, Y: 1036)`
- **Cornières de cadrage (Corner Brackets)** :
  - Angle droit d'épaisseur `2px`.
  - Branche horizontale : `20px`.
  - Branche verticale : `20px`.

### 3.2. Architecture du HUD Permanent (Scene Graph Superposé)
Le HUD constitue une surcouche télémétrique persistante (`Z-Index: 100`) :
- **Coin Supérieur Gauche (`X = 44px, Y = 68px`)** :
  - Libellé fixe : `CLAUDE` suivi d'une marge puis `MOTION REEL - 2026`.
- **Coin Supérieur Droit (`X = 1720px, Y = 68px`)** :
  - Indicateur de chapitre actif (ex: `01 - IDENTITY`, `02 - EASING`, `03 - MORPHING`, `04 - SYSTEMS`, `05 - DEPTH`, `06 - KINETIC TYPE`, `07 - FIN`).
- **Coin Inférieur Gauche (`X = 44px, Y = 932px`)** :
  - Running Timecode frame-accurate au format `00:00:SS:FF` (s'incrémente de `00:00:00:00` à `00:00:15:00`).
  - Libellé de cadence : `60 FPS` positionné à $X = 136px$.
  - Ligne de repère horizontale fine à $Y = 972px$ (longueur variable selon la section).
- **Coin Inférieur Droit (`X = 1620px, Y = 932px`)** :
  - Indicateur de tempo : `128 BPM`.
  - Matrice des 4 temps de la mesure : 4 carrés de $6 \times 6px$ espacés de $4px$ (`■□□□` sur le temps 1, `□■□□` sur le temps 2, `□□■□` sur le temps 3, `□□□■` sur le temps 4).
  - Numéro de mesure en cours : `BAR X/8` (s'incrémente de `BAR 1/8` à `BAR 8/8`).

---

## 4. Rythme, Grille Audio-Visuelle & Easing Mathématique

### 4.1. Structure Métrique & Subdivision Temporelle
- **Tempo musical** : **128.0 BPM** exact (tempo techno / electro minimaliste).
- **Durée d'un temps (Quarter Note / Beat)** :
  $$T_{beat} = \frac{60}{128} = 0.46875 \text{ secondes} = 28.125 \text{ frames à 60 fps}$$
- **Durée d'une demi-pulsation (Eighth Note / Croche)** :
  $$T_{half} = 0.234375 \text{ secondes} = 14.0625 \text{ frames}$$
- **Durée d'une mesure (Bar 4/4)** :
  $$T_{bar} = 4 \times 0.46875 = 1.875 \text{ secondes} = 112.5 \text{ frames}$$
- **Totalité de la timeline** : Exactement **8 mesures 4/4** ($8 \times 1.875s = 15.000s = 900 \text{ frames}$) + 4 frames d'extinction finale = **904 frames**.

| Chapitre | Mesure Musicale | Plage Temporelle (s) | Plage de Frames (@ 60fps) | Durée (frames) |
|---|---|---|---|---|
| **01 - IDENTITY (Part 1)** | Bar 1/8 | `00:00.000 - 00:01.875` | Frames 0 à 112 | 113 |
| **01 - IDENTITY (Part 2)** | Bar 2/8 | `00:01.875 - 00:03.750` | Frames 113 à 225 | 113 |
| **02 - EASING** | Bar 3/8 | `00:03.750 - 00:05.625` | Frames 226 à 337 | 112 |
| **03 - MORPHING** | Bar 4/8 | `00:05.625 - 00:07.500` | Frames 338 à 450 | 113 |
| **04 - SYSTEMS** | Bar 5/8 | `00:07.500 - 00:09.375` | Frames 451 à 562 | 112 |
| **05 - DEPTH** | Bar 6/8 | `00:09.375 - 00:11.250` | Frames 563 à 675 | 113 |
| **06 - KINETIC TYPE** | Bar 7/8 | `00:11.250 - 00:13.125` | Frames 676 à 787 | 112 |
| **07 - FIN** | Bar 8/8 | `00:13.125 - 00:15.061` | Frames 788 à 904 | 117 |

### 4.2. Profils d'Easing & Définitions Mathématiques
Le film constitue une encyclopédie visuelle des courbes d'interpolation d'animation :

1. **Linear** :
   $$f(t) = t$$
2. **Ease-In-Out (Cubic)** :
   $$f(t) = \begin{cases} 4t^3 & \text{si } t < 0.5 \\ 1 - \frac{(-2t + 2)^3}{2} & \text{si } t \ge 0.5 \end{cases}$$
3. **Expo-Out** :
   $$f(t) = \begin{cases} 0 & \text{si } t = 0 \\ 1 - 2^{-10t} & \text{si } t > 0 \end{cases}$$
4. **Back-Out ($s = 1.70158$)** :
   $$f(t) = 1 + (s + 1)(t - 1)^3 + s(t - 1)^2$$
5. **Elastic-Out** :
   $$f(t) = 2^{-10t} \cdot \sin\left(\frac{(t \cdot 10 - 0.75) \cdot 2\pi}{3}\right) + 1$$
6. **Bounce-Out** :
   $$f(t) = \text{rebonds paraboliques successifs amortis}$$
7. **Simulation de Ressort Harmonique (Spring Physics)** :
   - Fréquence propre : $F = 2.6 \text{ Hz}$
   - Taux d'amortissement : $\zeta = 0.30$ (sous-amorti vif avec oscillation de rebond)
   - Équation différentielle : $\ddot{x} + 2\zeta \omega_n \dot{x} + \omega_n^2 x = 0$ avec $\omega_n = 2\pi F \approx 16.336 \text{ rad/s}$.

---

## 5. Post-Processing & Traitements de Surface

1. **Grain de Pellicule Numérique (Monochromatic Film Grain)** :
   - Bruit gaussien monochrome très fin superposé en incrustation (`blend-mode: overlay`, opacité $3.5\%$).
   - Permet de casser le banding sur les aplats rouge vermillon et cobalt.
2. **Aberration Chromatique & RGB Split** (Scène 06 "NEVER LINEAR.") :
   - Séparation des canaux rouge et cyan : décalage horizontal de $\Delta X = \pm 3px$ à $\pm 6px$ sur les bordures de fort contraste.
3. **Motion Blur Directionnel & Écho Stroboscopique** :
   - Sur les typographies cinétiques rapides et les balles en accélération : étirement géométrique selon le vecteur vitesse ($v_x, v_y$) couplé à un estompage d'écho en 4 passes d'opacité décroissante ($100\%, 60\%, 35\%, 15\%$).
4. **Iris Shockwave & Bloom Spectral** (Scène 07) :
   - Onde de choc circulaire en expansion radiale ultra-rapide ($R(t) = 0 \to 1200px$ en 14 frames).
   - Anneau externe avec dispersion chromatique prismatique (halo dégradé jaune $\to$ rose $\to$ cyan).
