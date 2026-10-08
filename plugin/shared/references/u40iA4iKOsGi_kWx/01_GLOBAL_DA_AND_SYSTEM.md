# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, graphique et technique de la vidéo `u40iA4iKOsGi_kWx.mp4` (Showreel / Manifeste méta-pédagogique du motion designer Claude). Il fournit les spécifications d'ingénierie nécessaires pour une réimplémentation logicielle fidèle sous Remotion, Canvas 2D, WebGL/Three.js et SVG.

---

## 1. Archétype Visuel & Philosophie

L'identité visuelle fusionne trois univers graphiques complémentaires :
1. **Atelier de Motion Design & Décomposition Didactique** : Esthétique "Behind-The-Scenes" exposant les rouages de l'animation. Trajectoires d'arcs en pointillés, fantômes stroboscopiques (onion-skinning), repères de bounding box, courbes d'interpolation de Bézier éditables et annotations manuscrites au feutre d'animateur (bleu de crayon de rough et rouge de correction).
2. **Interface Technique (HUD & Motion Tool UI)** : Simulation permanente d'une interface logicielle d'animation (hybride After Effects, Figma et Rive). Scrubber de timeline dynamique en bas d'écran avec keyframes losanges, aiguille de lecture en translation continue, timecode frame-accurate affiché au millième en haut à droite, et curseur de souris vectoriel opérant les poignées d'animation.
3. **Kinetic Typography Contemporaine & Brutalisme Éditorial** : Typographie grotesque monumentale ultra-condensée en capitales, occupant l'espace optique, rythmée par des transformations physiques littérales (rebond à stacking Z, étirement élastique horizontal, rotation 3D sur l'axe Y, snap instantané sans amorti).

L'équilibre chromatique repose sur une alternance nette de deux états de fond (fond clair albâtre `#F2F2F4` vs fond sombre asphalte `#121316`), ponctuée par deux teintes d'accentuation pures : un bleu cobalt électrique `#1E6BFF` et un rouge corail dynamique `#FF334B`.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Code Hex / RGBA | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-light` | `#F2F2F4` | Fond albâtre des chapitres clairs (spacing, easing, hello) | Normal |
| `bg-dark` | `#121316` | Fond asphalte profond des chapitres sombres (type wordplay, follow-through, anticipation) | Normal |
| `accent-blue` | `#1E6BFF` | Couleur de marque : balle héroïque, mot STRETCH, scrubber actif, particules en tête, annotations d'accentuation | Normal / Additif (`screen`) |
| `accent-red` | `#FF334B` | Couleur de rupture : annotation "squash!", mot "SNAP", texte barré "linear = robotic", repères d'alignement | Normal |
| `text-dark-primary` | `#111215` | Typographie principale et tracés majeurs sur fond clair | Normal |
| `text-dark-secondary` | `#6E7079` | Métadonnées secondaires, axes du repère d'animation sur fond clair | Normal |
| `text-light-primary` | `#FFFFFF` | Typographie monumentale et éléments géométriques sur fond sombre | Normal |
| `text-light-secondary` | `#8C8E96` | Timecode en haut à droite, graduations radiales sur fond sombre | Normal |
| `grid-dot-light` | `#D8D8DC` | Micro-points de grille cartésienne sur fond clair (pitch 40px) | Normal |
| `grid-dot-dark` | `#23252B` | Micro-points de grille cartésienne sur fond sombre (pitch 40px) | Normal |
| `hud-track-light` | `rgba(0, 0, 0, 0.08)` | Rail horizontal de la timeline inférieure sur fond clair | Normal |
| `hud-track-dark` | `rgba(255, 255, 255, 0.12)` | Rail horizontal de la timeline inférieure sur fond sombre | Normal |
| `hud-needle` | `#1E6BFF` / `#FFFFFF` | Curseur triangulaire et tête de lecture de la timeline | Normal |
| `hud-keyframe-diamond` | `#8C8E96` | Losanges de keyframes positionnés aux divisions de mesure sur la timeline | Normal |

### 2.2. Stack Typographique

Le système orchestre trois familles typographiques aux rôles strictement cloisonnés :

1. **Grotesque Monumentale Ultra-Condensée** (*Druk Condensed Super*, *Tungsten Bold*, ou *Anton*) :
   - Usage : Titres massifs en kinetic typography ("I MAKE THINGS MOVE.", "BOUNCE", "STRETCH", "SPIN", "SNAP", "MOTION DESIGNER CLAUDE.").
   - Poids : `Black` (900) ou `Ultra-Bold`, majuscules intégrales obligatoires.
   - Propriétés CSS : `letter-spacing: -0.02em`, `line-height: 0.82`, `text-transform: uppercase`.
   - Traitement : Plein monochrome (`#FFFFFF` ou `#111215`), teinté (`#1E6BFF`, `#FF334B`), ou découpé en tranches pour les décompositions 3D.

2. **Monospace HUD & Métriques Techniques** (*JetBrains Mono*, *SF Mono*, *Space Mono*) :
   - Usage : Timecode supérieur droit (`00:00:SS:FF`), labels d'axes ("position", "time"), pourcentage radial ("0%" à "100%"), annotations numériques d'espacement ("stagger: 45ms").
   - Poids : `Regular` (400) et `Medium` (500).
   - Propriétés CSS : `letter-spacing: 0.04em`, `font-variant-numeric: tabular-nums`.

3. **Cursive Organique / Feutre d'Animateur** (*Caveat*, *Nanum Pen Script*, ou tracés vectoriels SVG calligraphiés) :
   - Usage : Annotations critiques de principes d'animation ("slow in, slow out", "squash!", "stretch", "overlap", "gravity-ish", "elastic", "no ease. on purpose.", "linear = robotic", "ease in-out [check]", "spacing!", "follow-through", "anticipation", "open to new projects").
   - Poids : Aspect tracé feutre fin à moyen (épaisseur de trait variable entre 2px et 3.5px).
   - Couleur : Exclusivement `#1E6BFF` (bleu d'animateur) ou `#FF334B` (rouge correctif).

---

## 3. Grille, Cadrage & Caméra

### 3.1. Résolution & Espacement
- Résolution nominale : 1920x1080 pixels (ratio 16:9).
- Framerate : 30.00 fps (1 frame = 33.333 ms).
- Grille de fond : Matrice orthogonale de points réguliers de rayon 1.5px espacés de 40px en X et en Y. Les points sont alignés au centre de la composition `(960, 540)`.

### 3.2. Éléments Fixes d'Interface (Overlay HUD)
- **Timecode supérieur droit** :
  - Position de l'ancre : `top: 44px`, `right: 64px`.
  - Format : `00:00:SS:FF` (SS = secondes, FF = frames de 00 à 29).
  - Typographie : Monospace semi-condensée 18px.
  - Comportement : Incrémentation synchrone frame par frame sans lissage.
- **Barre de Timeline inférieure (Scrubber)** :
  - Position : `bottom: 40px`, centré horizontalement, largeur : 1760px (marge latérale de 80px).
  - Hauteur du rail : 2px.
  - Losanges de keyframes : 5 repères en losange de 8x8px fixés à des positions clés proportionnelles aux chapitres.
  - Tête de lecture (Needle) : Triangle inversé de base 10px et hauteur 8px, avec ligne verticale indicatrice de 14px, avançant linéairement de `x: 0%` à `x: 100%` sur l'ensemble des 452 frames.
  - Étiquette de chapitre : Texte cursif flottant 20px au-dessus de la tête de lecture, commutant à chaque changement de section (`spacing` -> `type` -> `easing` -> `follow-through` -> `anticipation` -> `hello`).

### 3.3. Espace Tridimensionnel & Caméra
- Les séquences 1, 2, 4 et 6 opèrent dans un espace 2D orthographique pur.
- La séquence 3 ("SPIN") applique une perspective CSS locale `perspective(1200px)` avec point de fuite au centre du mot `(960, 540)`.
- La séquence 5 ("follow-through") opère une bascule de caméra virtuelle avec une rotation en tangage (pitch) de -35 degrés sur l'axe X, conférant à la grille de particules une profondeur fuyante vers l'horizon avant de se contracter au centre.

---

## 4. Rythme, Easing & Physique Mathématique

### 4.1. Métriques Temporelles (Tempo Audio : 129.2 BPM)
- Cadence vidéo : 30.00 fps.
- Durée d'un temps (beat à la noire) : `60 / 129.2 = 0.4644 s` = **13.93 frames** (~14 frames).
- Durée d'une demi-mesure (2 temps) : `0.9288 s` = **27.86 frames** (~28 frames).
- Durée d'une mesure complète (bar 4/4) : `1.8576 s` = **55.73 frames** (~56 frames).
- Durée totale : 15.061 secondes = **452 frames** (exactement 8 mesures musicales complètes et 5 frames de résonance).

### 4.2. Profils d'Interpolation (Easing & Springs)

1. **Rebond Gravitationnel (Bouncing Ball)** :
   - Descente : Accélération polynomiale `y(t) = y_start + g * t^2`. Vitesse maximale à l'impact.
   - Remontée : Décélération inverse `y(t) = y_floor - (v0 * t - 0.5 * g * t^2)`.
   - Squash à l'impact : Conservation de volume 2D `scaleX = 1 + s`, `scaleY = 1 / scaleX`. À l'impact, `scaleX = 1.45`, `scaleY = 0.69`.
   - Stretch en vol : À vitesse maximale, `scaleY = 1.35`, `scaleX = 0.74` orienté le long du vecteur tangent de la trajectoire.

2. **Cubic Bézier Universel "Ease In-Out"** :
   - Fonction : `cubic-bezier(0.42, 0.0, 0.58, 1.0)`.
   - Utilisé pour le déplacement fluide du curseur de souris, les volets de transition de fond et l'interpolation du dial radial.

3. **Snap Instantané (Zero Ease)** :
   - Profil : `steps(1, end)` ou `cubic-bezier(0.0, 0.0, 0.05, 1.0)` avec temps de montée de 2 frames (66 ms).
   - Aucun rebond, aucun dépassement d'amorti (undershoot/overshoot) : impact mécanique sec.

4. **Ressort Élastique (Spring Physics - Mot "STRETCH")** :
   - Masse : `m = 1.0`
   - Raideur (stiffness) : `k = 240.0`
   - Amortissement (damping) : `c = 15.0`
   - Réponse : Oscillation amortie sur 18 frames avec 2 dépassements perceptibles.

---

## 5. Post-Processing & Finition Optique

- **Vignettage Périphérique Doux** :
  - Dégradé radial neutre : `radial-gradient(ellipse at center, transparent 60%, rgba(0, 0, 0, 0.07) 100%)`.
  - Atténue subtilement les bords sans assombrir la composition.
- **Grain Argentique Subliminal** :
  - Bruit 2D fractal généré dynamiquement à 30 fps, opacité 2.0% à 3.0%, mode de fusion `overlay`.
  - Évite le banding dans les dégradés d'implosion et donne une texture tactile aux aplats de couleur.
- **Motion Blur Directionnel (Vector Blur)** :
  - Simulé sur le mot "STRETCH" et lors de la rotation de "SPIN".
  - Échantillonnage de 5 sous-frames réparties le long du vecteur de vélocité angulaire ou linéaire avec opacité décroissante (`[0.35, 0.25, 0.18, 0.12, 0.10]`).
