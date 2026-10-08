# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel et technique de la vidéo `pleometrix-mexica.mp4` (titre original : *P(doom)* / *Sparks of AGI* par Mexica / @pleometrix). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas2D).

---

## 1. Archétype Visuel & Philosophie

L'esthétique repose sur une collision maîtrisée entre trois registres :
1. **Academic Sci-Fi / Hard AI Research** : Tracés TikZ, diagrammes de réseaux de neurones (MLP, Transformers), paysages de perte (loss landscapes), métriques d'entraînement (`loss (log)`, `P(doom)`, `top-p`, `sampled tokens`).
2. **Post-Cyberpunk HUD & Computer Vision** : Bounding boxes de détection d'objets (style YOLO/OpenCV), réticules de visée, tags de confiance, repères de cadrage caméra `[ ]`, oscilloscope CRT.
3. **Bureaucratie & Typographie Vintage** : Formulaires administratifs ("FORM 7-B", "DEPT. OF REASONABLE ASSURANCES"), tampons encreurs claqués au ressort, compteurs mécaniques kilométriques (odomètre à rouleaux), typographies machine à écrire.

Le traitement refuse le clinquant des néons violets génériques : il privilégie un contraste brut, chirurgical, noir charbon et blanc optique, dynamisé par un orange industriel haute visibilité (International Orange / OSHA safety orange).

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-primary` | `#0A0A0C` | Fond noir charbon profond omniprésent | Normal |
| `bg-surface-elevated` | `#141418` | Cartouches de code, blocs Transformer, barres de statut | Normal |
| `accent-orange` | `#FF4400` / `#FF3B00` | Accent principal : mots clés, tracés actifs, étincelle, P(doom) | Normal / Additif (`screen`) |
| `accent-orange-glow` | `#FF6600` | Halo lumineux d'étincelle et glow de bloom | Additif (`screen` / `lighter`) |
| `text-primary` | `#FFFFFF` | Typographie principale, titres massifs, repères forts | Normal |
| `text-secondary` | `#99999F` | Données secondaires, métadonnées HUD, code TikZ inactif | Normal |
| `grid-line` | `rgba(255, 255, 255, 0.07)` | Grille cartésienne 2D, repères millimétrés | Normal |
| `grid-axis` | `rgba(255, 255, 255, 0.20)` | Axes X/Y principaux, graduations chiffrées | Normal |
| `paper-bg` | `#F2EFE9` | Fond papier vintage (scène FORM 7-B et schéma Von Neumann) | Normal |
| `paper-ink-black` | `#1A1A1A` | Texte imprimé machine à écrire sur papier | Normal / Multiply |
| `stamp-red` | `#E6391F` | Encre rouge dégradée du tampon "SAFE ENOUGH" | Multiply |

### 2.2. Typographie & Rôles

Le film orchestre quatre familles typographiques distinctes :

1. **Grotesque Géométrique Compacte / Brutaliste** (ex: *Neue Haas Grotesk*, *Inter Tight Display*, *Druk*) :
   - Usage : Titres monumentaux en kinetic typography ("AGI", "MY", "TRANSFORMERS", "POST-CHINCHILLA", "UPPIN'").
   - Poids : `Black` (900) ou `Bold` (700), majuscules obligatoires.
   - Traitement : Alternance entre plein coloré (`#FF4400`), blanc plein (`#FFFFFF`) et contour filaire creux (`stroke: 2px solid white`, fill transparent).

2. **Monospace Technique / Code** (ex: *JetBrains Mono*, *SF Mono*, *Roboto Mono*) :
   - Usage : Code TikZ, invites de commande ("draw a unicorn in TikZ"), valeurs numériques, labels de bounding boxes (`t-00:03.96`, `ckpt 3`, `P(doom) 0.04`).
   - Poids : `Regular` (400) et `Medium` (500).
   - Espacement : `letter-spacing: -0.02em` sur les blocs de code, `+0.05em` sur les labels HUD.

3. **Typewriter Mécanique** (ex: *Courier Prime*, *Prestige Elite*, *OCR-B*) :
   - Usage : Formulaire administratif FORM 7-B ("That was safe enough, we reckon").
   - Traitement : Chasse fixe crénelée, léger bleed d'encre sur les contours.

4. **Serif Classique / Académique** (ex: *Times New Roman*, *EB Garamond Italic*) :
   - Usage : Éléments poétiques ou théoriques contrastés ("The Omega Point's coming soon", variable mathématique `b l u e s`).

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : 1280x720 (16:9), cadencée à 60.0 fps constants.
- **Viewfinder framing** : Dans 90% des plans, quatre coins de visée `[ ]` en traits fins (`1px`, `#FFFFFF` à 40% d'opacité) délimitent la zone utile à 24px des bords.
- **Grille de repère** : Grille orthogonale 2D (pas de 40px) avec des graduations d'axes cartésiens (-3, -2, -1, 0, 1, 2, 3) qui basculent en perspective 3D isométrique ou en déformation topologique non-linéaire selon la narration.
- **Caméra** :
  - Plans 2D : Caméra fixe avec légers micro-secousses (shakes) sur les transitoires audio.
  - Plans 3D : Plongées à 45 degrés sur paysages de perte et tunnels d'accrétion (effet trou noir), avec rolling shutter / motion blur calibré à un angle de 180 degrés (obturateur standard 1/120s à 60fps).

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels
- **Tempo musical** : **129.2 BPM** (~130 BPM).
- **Durée par temps (Beat)** : `0.464 seconde` = **27.8 frames** à 60 fps.
- **Durée par mesure (Bar - 4/4)** : `1.858 seconde` = **111.4 frames** à 60 fps.
- **Résolution d'accrochage** : Toutes les entrées typographiques majeures et les cuts de caméra tombent rigoureusement sur le kick (temps 1) ou la caisse claire / snare (temps 2 et 4).

### 4.2. Courbes d'Easing Clés

Les courbes d'animation obéissent à trois profils mathématiques stricts :

1. **Snap & Settle (Expo Out)** :
   - CSS : `cubic-bezier(0.16, 1, 0.3, 1)` ou `easeOutExpo`.
   - Utilisation : Arrivée des mots en kinetic typography, zoom de caméra brusque.
   - Comportement : Vitesse initiale extrême (80% du déplacement en 4 frames), décélération douce sur les 12 frames suivantes.

2. **Elastic Snap-Back (Spring)** :
   - Physique : `mass: 1, stiffness: 220, damping: 15`.
   - Utilisation : Frappe du tampon "SAFE ENOUGH", rebond des cadres de détection.
   - Comportement : Overshoot de 10% à 15% avant stabilisation en 3 oscillations rapides.

3. **Linear Constant Motion** :
   - Easing : `linear`.
   - Utilisation : Translation de la tête chercheuse / étincelle le long des tracés SVG, défilement des barres verticales de prison, compteurs rotatifs.

---

## 5. Pipeline de Post-Processing & Effets Shader

Pour reproduire fidèlement l'ambiance à l'export :
1. **Bloom / Additive Glow** : Rayon de 12px à 24px avec seuil (threshold) à `0.85`, appliqué sélectivement sur l'étincelle orange (`#FF4400`) et les textes haute intensité.
2. **Grain de film argentique** : Bruit monochrome fin (taille 1px, intensité 4% à 6%, blend mode `overlay`) sur toute la timeline pour casser le côté "vectoriel clinique".
3. **Aberration Chromatique dynamique** : Séparation RVB (décalage horizontal de -2px sur le rouge, +2px sur le bleu) déclenchée en impulsion d'une durée de 3 à 5 frames sur les impacts audio majeurs (drops, kicks massifs).
4. **Vignettage optique** : Assombrissement radial doux partant de 70% du centre jusqu'à 0.4 d'opacité noire aux angles.
