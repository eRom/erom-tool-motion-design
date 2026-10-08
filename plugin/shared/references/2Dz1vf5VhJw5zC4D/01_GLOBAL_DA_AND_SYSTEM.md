# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, structurel et mathématique de la vidéo de référence `2Dz1vf5VhJw5zC4D.mp4`. Conçu pour une ingestion directe par des agents de fabrication logicielle (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP), il fait abstraction de tout commentaire subjectif pour ne retenir que des paramètres rigoureusement quantifiés.

---

## 1. Archétype Visuel & Philosophie

L'esthétique de la vidéo relève du **Brutalisme Éditorial & Télémétrie Logicielle (Creative Tool HUD)** :
1. **Précision Mécanique & Télémétrie Temps Réel** : Présence permanente d'un affichage tête haute (HUD) intégrant un timecode frame-accurate au 60e de seconde, un métronome visuel 4 temps asservi au BPM, des réticules de cadrage et un cartouche de scène dynamique.
2. **Brutalisme Typographique Suisse & Contrapuntal Serif** : Affrontement permanent entre des blocs grotesques massifs ultra-condensés (poids Black, majuscules serrées) et une typographie serif cursivo-éditoriale d'une grande fluidité.
3. **Palette d'Impact Haute Saturation** : Opposition binaire entre un noir carbone abyssal (`#05080D`), un blanc cassé minéral (`#F1F1E7`), un orange-corail de signalisation (`#FA4E20`) et un bleu cobalt électrique (`#314CFF`). Aucun dégradé pastel flou : aplats nets, masques francs ou transitions mathématiques pures.
4. **Cinématique 100% Procédurale** : Zéro interpolation approximative à la main. Tous les mouvements dérivent de fonctions trigonométriques, d'algorithmes génératifs (phyllotaxie, bruit de Curl, superformula de Gielis) ou de profils de ressort amortis.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-dark` | `#05080D` | Fond principal nocturne (Intro, Scene 03/Beat 2, Scene 05, Outro) | Normal |
| `bg-coral` | `#FA4E20` | Fond d'impact chaud (Scene 01, Scene 03/Beat 4, Scene 07) | Normal |
| `bg-cream` | `#F1F1E7` | Fond papier minéral (Scene 03/Beat 1, Scene 04, Modal UI Scene 06) | Normal |
| `bg-blue` | `#314CFF` | Fond cobalt électrique (Scene 03/Beat 3, fond d'ambiance Scene 06) | Normal |
| `accent-orange` | `#EC5230` | Puce conductrice, curseur HUD, indicateurs d'accentuation | Normal / Additif (`screen`) |
| `accent-purple` | `#6C3BAA` | Nuance basse du dégradé des prismes 3D (Scene 02) | Normal |
| `accent-salmon` | `#FF8A65` | Nuance haute du dégradé des prismes 3D (Scene 02) | Normal |
| `accent-cyan` | `#2EE9D8` | Particules vectorielles haute énergie (Scene 05) | Additif (`screen`) |
| `text-white` | `#FFFFFF` | Typographie principale sur fond sombre ou corail | Normal |
| `text-dark` | `#060910` | Typographie principale sur fond crème | Normal |
| `text-muted` | `rgba(255, 255, 255, 0.45)` | Labels télémétriques inactifs, repères millimétrés | Normal |
| `grid-line-dark` | `rgba(255, 255, 255, 0.08)` | Lignes de repère cartésiennes sur fond sombre | Normal |
| `grid-line-light` | `rgba(0, 0, 0, 0.08)` | Lignes de repère cartésiennes sur fond crème | Multiply |

### 2.2. Typographie & Rôles

Le système s'articule autour de trois registres typographiques stricts :

1. **Grotesque Monumentale Ultra-Bold** (Équivalents recommandés : *Druk Wide Bold*, *Neue Haas Grotesk Black*, *Clash Display 700*) :
   - **Usage** : Titrages cinétiques principaux (`CLAUDE.`, `EVERY`, `SINGLE`, `FRAME`, `Render queue`, `EVERY FRAME, ON PURPOSE.`).
   - **Casse & Poids** : Majuscules systématiques (`uppercase`), poids 800-900.
   - **Tracking** : `-0.04em` à `-0.06em` (lettrage très resserré pour un impact monobloc).
   - **Traitements** : Alternance entre aplats pleins (`#FFFFFF` ou `#060910`) et contours vectoriels creux (`fill: transparent; stroke: 2px currentColor;`).

2. **Serif Éditoriale Italique** (Équivalents recommandés : *Playfair Display Italic*, *Editorial New Italic*, *EB Garamond Italic*) :
   - **Usage** : Contrepoint organique et humain (`motion designer`, `on purpose.`).
   - **Casse & Poids** : Bas-de-casse (`lowercase`), poids 400 Italic.
   - **Tracking** : `-0.01em` à `0.00em`.
   - **Alignement** : Souvent positionné en sous-titre décalé avec soulignement cursif ou traversant.

3. **Monospace Télémétrique Tabulaire** (Équivalents recommandés : *SF Mono Regular*, *JetBrains Mono*, *Geist Mono*) :
   - **Usage** : Données d'affichage HUD, timecode, métronome, métadonnées techniques (`SCENE 01 / 07`, `1920 x 1080`, `60 FPS`, `0 DROPPED`, `r(θ) = superformula`, `n = 2,400`, `φ = 137.508°`).
   - **Propriété essentielle** : `font-variant-numeric: tabular-nums` (largeur constante par glyphe pour éviter tout sautillement du timecode).
   - **Casse & Poids** : Majuscules, poids 400 à 500, taille 11px à 13px (sur base 1080p).
   - **Tracking** : `+0.05em` à `+0.12em`.

---

## 3. Grille, Cadrage & Système de Coordonnées

- **Résolution canevas** : `1920 x 1080 px` (Ratio 16:9 standard).
- **Zone sécurisée de titrage (Action Safe Zone)** : `padding: 48px 64px` (invariable tout au long des 15 secondes).
- **Repères Viewfinder permanents** :
  - Coins de visée en L (`⌜ ⌝ ⌞ ⌟`) tracés en traits de 1px, longueur 16px, marge interne 48px du bord de l'écran.
  - Croix réticulaires centrales `+` de 8px de large positionnées sur les intersections de tiers `(640, 360)`, `(1280, 360)`, `(640, 720)`, `(1280, 720)`.
- **Cartouches d'angle HUD (Invariables en position)** :
  - **Coin supérieur droit** : Indicateur de chapitre `SCENE 0X / 07` (ancré à `top: 48px; right: 64px;`).
  - **Coin inférieur gauche** : Catégorie technique avec effet de désembrouillage (`top: 1016px; left: 64px;`).
  - **Coin inférieur droit** : Métronome 4 temps + Timecode `00:00:SS:FF` (ancré à `top: 1016px; right: 64px;`).

---

## 4. Rythme, Horloge & Équations de Timing

- **Cadence vidéo** : `60.0 fps` (exactement 60 frames par seconde de temps universel).
- **Tempo musical** : **144.0 BPM** (détecté à 72.0 BPM demi-mesure).
- **Durée élémentaire d'un temps (Beat)** :
  $$\text{Frames par temps} = \frac{60 \times 60}{144} = 25.0 \text{ frames (soit 416.67 ms)}$$
- **Durée d'une mesure (Bar 4/4)** :
  $$\text{Frames par mesure} = 4 \times 25.0 = 100.0 \text{ frames (soit 1.6667 s)}$$
- **Découpage global** : 9 mesures de 100 frames = 900 frames d'animation active + 4 frames d'extinction acoustique (total 904 frames / 15.061 s).

### Profils d'Amortissement & Easing

1. **Snap Mécanique / Perforation (Kinetic Typo & HUD Cuts)** :
   - Transition instantanée en 1 frame (cut pur) ou profil exponentiel rapide :
   ```css
   cubic-bezier(0.16, 1, 0.3, 1) /* easeOutExpo */
   ```
2. **Rebond Ressort Amorti (Pop-in de modale, toggles UI)** :
   - Spécification Spring Remotion / Framer Motion :
   ```typescript
   { mass: 0.8, stiffness: 220, damping: 18 }
   ```
3. **Ondulation Continue Harmonique (Scène 3D cubes, ondes sinusoidales)** :
   - Fonction oscillatoire pure sans discontinuité :
   $$y(t) = A \cdot \sin(2\pi f t + \phi)$$

---

## 5. Post-Processing & Texturation

Bien que le graphisme soit vectoriel et numérique, une chaîne de post-traitement subtile élimine la platitude informatique :

1. **Grain Monochrome Subtil** :
   - Bruit gaussien uniforme généré en shader ou calque SVG `feTurbulence`.
   - Opacité globale : `0.035` (3.5%).
   - Mode de fusion : `overlay` ou `soft-light`.
2. **Aberration Chromatique Périmétrique** :
   - Décalage radial des canaux R et B proportionnel au carré de la distance au centre :
   $$\Delta r = k \cdot (x^2 + y^2)$$
   - Valeur crête en bord d'écran : `2.5 px` maximum (imperceptible au centre, légère frange rouge/cyan sur les bords extrêmes).
3. **Motion Blur Quantifié (Directionnel)** :
   - Utilisé exclusivement sur les translations haute vélocité (bandes cinétiques Scene 03, cartes de transition) : shutter angle virtuel fixé à `180°` (soit une pondération sur 3 frames adjacentes).
