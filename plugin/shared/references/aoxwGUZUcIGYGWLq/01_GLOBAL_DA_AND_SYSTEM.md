# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, géométrique et cinématique de la vidéo `aoxwGUZUcIGYGWLq.mp4` (*Claude Motion Reel - Motion Designer*). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, Three.js / WebGL, Canvas 2D, SVG / GSAP).

---

## 1. Archétype Visuel & Philosophie

L'esthétique du film repose sur une démonstration d'ingénierie procédurale pure, résumée par son sous-titre manifeste :  
`15 SECONDS / 450 FRAMES / 0 KEYFRAMES SET BY HAND`.

Le système visuel est articulé autour de trois piliers fondamentaux :

1. **Hardware-Software Neo-Brutalism (Anthropic Identity)** :  
   Une collision calculée entre la matérialité physique (céramique mate, verre laqué, métal brossé, ombres de contact directionnelles) et le minimalisme logiciel radical propre à l'écosystème Claude / Anthropic.
2. **Pulsion Cinématique Binaire & Contraste d'Échelle** :  
   Alternance rythmée entre des environnements d'obscurité totale (`#050505` avec horizon rasant) et des environnements clairs de studio tactile (`#F2ECDE` façon papier Japonais / céramique chaude). Passage sans transition douce de micro-détails (anneaux gyroscopiques millimétrés) à des volumes typographiques monumentaux occupant 90% du cadre.
3. **HUD Télémétrique Temps Réel (Framing & Frame-Accurate Diagnostics)** :  
   Un cadre d'instrumentation permanent qui ancre chaque photogramme dans une rigueur de studio de fabrication : indexation continue du frame counter (`F 001 / 450` à `F 450 / 450`), timecode millisecondes, identification typographique des chapitres (`01 IMPACT` à `06 SIGN-OFF`) et timeline linéaire de progression calée au pixel près sur la durée totale.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-obsidian-dark` | `#050505` | Fond noir charbon profond (Sections 01, 03, 04) | Normal |
| `bg-paper-cream` | `#F2ECDE` | Fond chaud céramique / papier texturé (Sections 05, 06) | Normal |
| `accent-claude-terracotta` | `#EB513F` | Teinte signature Anthropic : sphère motrice, onde voxel, astérisque | Normal |
| `accent-claude-deep` | `#ED3A1F` | Fond uni saturé de la séquence cinétique (Section 02) | Normal |
| `accent-coral-glow` | `#FF6A55` | Halo lumineux (bloom) sur l'anneau gyro et les néons hexagonaux | Additif (`screen` / `lighter`) |
| `text-ink-black` | `#1A1919` | Typographie lourde "CLAUDE", "EVERY", "COUNTS", subtextes | Normal |
| `text-chalk-white` | `#FFFFFF` | Typographie 3D "CLAUDE" (S01), "FRAME" (S02), HUD sur fond sombre | Normal |
| `text-offwhite-warm` | `#EEECE1` | Face avant des lettres "FRAME" et reflets diffus | Normal |
| `metal-chrome-specular` | `#F0F0F2` | Anneaux métalliques du gyroscope, reflets spéculaires | Normal / Additif |
| `metal-chrome-dark` | `#222226` | Tranches et faces d'ombre des anneaux gyroscopiques | Normal |
| `horizon-rim-red` | `#301817` / `#5A1E18` | Dégradé d'horizon rasant et réflexion de sol (Section 01) | Normal / Screen |
| `voxel-inactive` | `#E8E4D8` | Pavés de la grille tactile à l'état de repos (Section 05) | Normal |
| `hud-line-light` | `rgba(255, 255, 255, 0.40)` | Ligne de progression et séparateurs sur fond sombre | Normal |
| `hud-line-dark` | `rgba(26, 25, 25, 0.40)` | Ligne de progression et séparateurs sur fond clair | Normal |

---

### 2.2. Stack Typographique & Rôles

Le film orchestre deux familles typographiques parfaitement hiérarchisées :

1. **Grotesque Géométrique Monumentale / Ultra-Black** (ex: *Neue Haas Grotesk Display Black*, *Druk Wide Bold*, *Integral CF Heavy*, *Syne Extra Bold*) :
   - **Usage** : Titres monumentaux ("CLAUDE" en 3D, "EVERY", "FRAME", "COUNTS", compteurs dynamiques `02.7`, `083`).
   - **Graisse** : `Black` (900) ou `Heavy` (800), majuscules obligatoires, crénage très serré (`letter-spacing: -0.04em`).
   - **Traitements** : 
     - Section 01 : Extrusion 3D blanche avec biseau discret (bevel 1.5px), réflexion au sol.
     - Section 02 : Alternance 2D contrastée (noir d'encre `#1A1919` vs blanc cassé `#EEECE1`) puis extrusion isométrique 3D en bloc compact.
     - Section 06 : Lettrage 3D lourd coulé en céramique noir d'encre avec ombres portées douces sur fond crème.

2. **Monospace Télémétrique & Diagnostic (HUD)** (ex: *JetBrains Mono*, *SF Mono*, *Space Mono*) :
   - **Usage** : Système HUD périphérique permanent ("CLAUDE — MOTION REEL", "©2026", labels de sections "01 IMPACT" -> "06 SIGN-OFF", timecode "00:07 F 008 / 450", mention technique de clôture).
   - **Graisse** : `Medium` (500) et `SemiBold` (600), majuscules.
   - **Espacement** : `letter-spacing: +0.08em` à `+0.12em` pour garantir la lisibilité télémétrique.

3. **Sans-Serif Humaniste / Editorial Bold** (ex: *Favorit*, *Söhne Breit*, *Inter Display*) :
   - **Usage** : Sous-titre "MOTION DESIGNER" en Section 06.
   - **Graisse** : `Bold` (700), espacement ouvert (`letter-spacing: +0.15em`).

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : `1920x1080` (format standard 16:9), cadencée à **30.0 fps constants**.
- **Durée totale** : **450 frames exactes** = 15.00 secondes (suivies de 2 frames techniques de buffer d'export).
- **Structure du Cadrage HUD** :
  - **Marges de sécurité** : `48px` depuis chaque bord du canvas (zone de contenu utile `1824x984`).
  - **Header (Y = 48px)** :
    - Gauche (`x = 48px`) : `CLAUDE — MOTION REEL`
    - Droite (`x = 1872px`, aligné à droite) : `©2026`
  - **Footer (Y = 1032px)** :
    - Gauche (`x = 48px`) : Numéro et nom de section (`01 IMPACT`, `02 KINETIC TYPE`, etc.)
    - Droite (`x = 1872px`, aligné à droite) : Timecode et compteur frame (`MM:SS  F NNN / 450`)
  - **Barre de Défilement Continue (Y = 1040px)** :
    - Ligne fine horizontale de `1px` traversant le bas de l'écran. Une barre de progression pleine se remplit linéairement de gauche à droite de `0%` à `100%` (`progress = frame / 450`).

- **Cinématique des Caméras par Section** :
  - **Section 01 (Impact)** : Caméra 3D perspective frontale rasante (FOV 40°, hauteur `y = 120`, angle de plongée `pitch = -8°`), travelling latéral doux vers la droite, suivi d'un zoom d'interception rapide (dolly-in Z) lorsque la sphère percute l'objectif.
  - **Section 02 (Kinetic Type)** : Caméra orthogonale 2D verrouillée au centre, puis bascule brutale en perspective 3D oblique (rotation `pitch = 18°`, `yaw = -24°`) lors de l'extrusion volumétrique des blocs de lettres.
  - **Section 03 (Form / Gyro)** : Caméra 3D orbitale centrée (distance `z = 650`), rotation continue sur trois axes simultanés, puis plongée zénithale d'alignement avec les axes des tores.
  - **Section 04 (Velocity)** : Caméra axiale alignée au centre du tunnel polygonal (FOV 65°), course ultra-rapide le long de l'axe Z négatif avec roulis continu (`roll Z = frame * 0.08 rad`).
  - **Section 05 (Systems)** : Caméra isométrique axonométrique en plongée (angle de vue `pitch = 52°`, `yaw = 38°`), se redressant progressivement sur les 30 dernières frames pour atteindre une vue orthogonale de dessus à 90°.
  - **Section 06 (Sign-Off)** : Vue quasi zénithale fixe (angle d'élévation `pitch = 82°`), éclairage directionnel simulant un soleil rasant à 45° projetant des ombres douces et allongées vers le bas-droit.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels & Mathématiques
- **Tempo musical** : **120.0 BPM** (période acoustique rigoureusement synchrone avec le framerate 30 fps).
- **Durée par temps (Beat)** : `60 / 120 = 0.500 seconde` = **exactement 15 frames** à 30 fps.
- **Durée par mesure (Bar 4/4)** : `4 * 15 = 60 frames` = **exactement 2.000 secondes**.
- **Quantification des découpages** : Les 6 chapitres sont tous calés sur des multiples entiers de mesures (bars) ou de demi-mesures de 120 BPM :
  - Section 01 : 60 frames (1 mesure de 4 temps)
  - Section 02 : 75 frames (1 mesure + 1 temps)
  - Section 03 : 90 frames (1 mesure et demie / 6 temps)
  - Section 04 : 45 frames (3 temps)
  - Section 05 : 92 frames (~1 mesure et demie)
  - Section 06 : 88 frames (~1 mesure et demie jusqu'à stabilisation finale)

### 4.2. Courbes d'Easing & Physique

Toutes les animations s'appuient sur des modèles physiques ou des fonctions mathématiques explicites sans retouche manuelle :

1. **Rebond Gravitaire & Restitution (Bouncing Ball)** :
   $$\begin{cases} y(t) = y_{\text{floor}} + \frac{1}{2} g t^2 \\ v(t) = -e \cdot v(t) \quad \text{au contact du sol} \quad (e \approx 0.68) \end{cases}$$
2. **Snap & Settle (Exponential Deceleration)** :
   - Profil : `cubic-bezier(0.16, 1, 0.3, 1)` ou amortissement critique `x(t) = 1 - (1 + \omega t) e^{-\omega t}`.
   - Utilisation : Déploiement des lettres 2D, stabilisation de l'astérisque.
3. **Propagation d'Onde Circulaire (Voxel Ripple)** :
   - Équation de hauteur d'un voxel en coordonnée $(x, z)$ :
     $$h(x, z, t) = h_0 + A \cdot \exp\left(-\gamma \cdot (r - v t)^2\right) \cdot \sin(k \cdot r - \omega t)$$
     avec $r = \sqrt{(x - x_0)^2 + (z - z_0)^2}$.
4. **Accélération Exponentielle (Warp Tunnel)** :
   - Vélocité de caméra le long de Z : $v_z(t) = v_0 \cdot \exp(\alpha \cdot t)$.

---

## 5. Pipeline de Post-Processing & Rendu Shader

1. **Motion Blur Vectoriel (Shutter Angle 180°)** :  
   Simulé à 1/60s sur la cadence 30 fps. Les vecteurs de vitesse linéaire de la sphère et la vitesse angulaire de l'astérisque induisent un flou directionnel calculé par pixel shader.
2. **Bloom & Diffuse Glow** :  
   Seuil de luminance (luminance threshold) à `0.85`, rayon de dispersion de `28px`, facteur d'intensité de `0.30`. Appliqué spécifiquement au point d'impact lumineux, à l'anneau rouge du gyroscope et aux arêtes néon du tunnel hexagonal.
3. **Ombres Douces & Occlusion Ambiante (SSAO)** :  
   Rendu des ombres portées au sol en Section 06 avec une source de lumière ponctuelle étendue : pénombre progressive sur les bords (`shadowBlur: 16px`), couleur d'ombre `#1A1919` avec une opacité maximale de `28%`.
4. **Grain de Film Procédural (Organic Micro-Noise)** :  
   Bruit blanc uniforme généré par shader (`intensity: 0.04`), réactualisé à chaque frame, assurant la cohérence texturée entre les scènes 3D pures et les aplats typographiques.
