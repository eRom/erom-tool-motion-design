# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel et technique de la vidéo `PRWfsEy-zcoo2ao_.mp4` (titre : *Clawd - Dual Mode / One Clawd, Every Mode*). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas 2D).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de cette vidéo fusionne trois registres stylistiques majeurs :

1. **Pop 3D Toy-Brutalism & Mascot Design** :
   - Le personnage central "Clawd" (la mascotte officielle inspirée de l'identité Anthropic/Claude) est traité comme un jouet de designer en vinyle / plastique mat (finition soft-touch, arêtes chanfreinées, géométrie cubique arrondie, yeux carrés laqués noirs avec reflet spéculaire).
   - Finitions matérielles tactiles : argile / plastique doux sans rugosité excessive, éclairage studio 3 points doux avec occlusion ambiante marquée et ombres de contact au sol.

2. **Anime Action & Shōnen Dynamic Framing** :
   - Lignes de vitesse radiales (manga speed lines / sunbursts).
   - Plans d'impact négatifs / monochromes inversés à très fort contraste avant chaque révélation de scène (flash de tension dramatique de 4 à 5 frames).
   - Caméra dynamique : zooms brusques (punch zooms), tremblements d'impact (screen shakes), légères aberrations chromatiques sur les bords et focale courte (effet grand angle dynamique 24mm - 35mm).

3. **Graphic Novel & Comic Pop-Art (Dual-Tone)** :
   - Écran divisé à 45 degrés séparant l'univers "analogique / pastel chaleureux" de l'univers "numérique / dark cyber".
   - Motifs de trame en demi-teintes (Ben-Day halftone dots pattern) sur les aplats sombres.
   - Typographie cinétique monumentale en bas de cadre : lettres majuscules condensées extra-bold avec contours noirs massifs (stroke de 3 à 4px) et ombres portées nettes et bloquées (hard block shadows sans flou).

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `mascot-body-terracotta` | `#EF7E54` | Corps cubique principal de Clawd (terracotta Claude) | Normal |
| `mascot-body-dark` | `#C85B32` | Face ombrée et dessous des pattes de la mascotte | Normal |
| `mascot-eye-black` | `#1A1A1A` | Yeux carrés et bouche/expressions | Normal |
| `mascot-specular-white` | `#FFFFFF` | Reflet spéculaire blanc sur le coin haut-gauche des yeux | Normal |
| `bg-cream-paper` | `#F0EADE` | Fond crème chaud de l'univers analogique (demi-écran gauche) | Normal |
| `bg-navy-cyber` | `#0B2559` | Fond bleu nuit profond de l'univers digital (demi-écran droit) | Normal |
| `halftone-dot-navy` | `#07193D` | Points de trame Ben-Day sur le demi-écran bleu | Multiply |
| `accent-cyan-hologram` | `#00E5FF` | Version holographique de Clawd, oreillettes cyber, badges | Additif (`screen`) |
| `accent-cyan-glow` | `#33F0FF` | Halo lumineux des écrans HUD et anneaux de lévitation | Additif (`screen`) |
| `mode-code-green` | `#39FF14` | Vert néon Matrix, typographie "12 AGENTS", checkmarks | Normal / Screen |
| `mode-code-bg` | `#021408` | Fond sombre verdâtre de la chambre de hackers | Normal |
| `mode-write-purple` | `#3D348B` | Fond royal indigo de la scène scribe "FULL REWRITE" | Normal |
| `mode-write-stamp-red` | `#E63946` | Tampon encreur rouge "THE END" | Multiply |
| `mode-research-pink` | `#E6007A` | Fond rose fuchsia vif de la scène "847 TABS" | Normal |
| `mode-research-gold` | `#F9C74F` | Tranches des livres, badge de compteur d'onglets | Normal |
| `mode-debug-maroon` | `#4A151B` | Fond bordeaux brûlé de la scène "KILL IT WITH FIRE" | Normal |
| `mode-debug-flame-orange`| `#FF6B00` | Flammes volumétriques, lueurs de déflagration | Additif (`screen`) |
| `mode-analyze-indigo` | `#14122B` | Fond cosmique sombre de la scène "ALL THE DATA" | Normal |
| `mode-analyze-bar-yellow`| `#F7C844` | Colonnes 3D du diagramme en bâtons | Normal |
| `mode-analyze-bar-cyan` | `#56CFE1` | Colonnes secondaires et sol quadrillé néon | Normal |
| `mode-design-white` | `#F8F9FA` | Sol et murs du studio d'artiste "MASTERPIECE" | Normal |
| `paint-magenta` | `#FF007F` | Ruban de peinture 3D, éclaboussures liquides | Normal |
| `paint-lemon-yellow` | `#FFD166` | Ruban de peinture 3D cintré | Normal |
| `paint-azure-blue` | `#00B4D8` | Rouleau de peinture géant et trainée liquide | Normal |
| `paint-emerald-green` | `#06D6A0` | Bande de peinture au sol | Normal |
| `text-title-white` | `#FFFFFF` | Corps des textes cinétiques principaux | Normal |
| `text-stroke-black` | `#1A1A1A` | Contour extérieur épais des titrages (3px à 4px) | Normal |
| `text-shadow-black` | `rgba(0, 0, 0, 0.85)` | Ombre portée bloquée décalée vers le bas-droite | Normal |

### 2.2. Typographie & Traitements Graphiques

Le film utilise trois niveaux typographiques très stricts :

1. **Titrage Cinétique Principal (Action Punch)** :
   - Exemples : `"CLAWD"`, `"DUAL MODE"`, `"12 AGENTS"`, `"FULL REWRITE"`, `"847 TABS"`, `"KILL IT WITH FIRE"`, `"ALL THE DATA"`, `"MASTERPIECE"`, `"CODE"`, `"THE END"`.
   - Famille : Sans-serif condensée ultra-grasse (ex: *Bebas Neue*, *Druk Wide Condensed*, *Anton*, *Impact*).
   - Style : Majuscules obligatoires, inclinaison dynamique (oblique / faux-italique à -6° sur l'axe X).
   - Rendu CSS / SVG :
     ```css
     font-family: 'Bebas Neue', 'Anton', sans-serif;
     font-weight: 900;
     text-transform: uppercase;
     letter-spacing: 0.02em;
     transform: skewX(-6deg);
     -webkit-text-stroke: 4px #1A1A1A;
     paint-order: stroke fill;
     filter: drop-shadow(6px 6px 0px #1A1A1A);
     ```

2. **Métadonnées de Chapitrage & Statut (Sub-Labels)** :
   - Exemples : `"01 / 06 • CODE"`, `"02 / 06 • WRITE"`, `"tabs: 847"`, `"one Clawd • every mode"`.
   - Famille : Grotesque technique ou Monospace (ex: *JetBrains Mono*, *Inter Display Bold*).
   - Style : Poids Medium ou Bold, majuscules pour les chapitres, minuscules pour les badges d'interface, espacement étendu (`letter-spacing: 0.08em`).
   - Placement : Toujours ancré au-dessus du titrage principal à 48px de la marge inférieure gauche.

3. **Interface Moniteur & Écrans HUD 3D** :
   - Exemples : `orchestrator - 12 agents`, `agent-01`, `agents 08/12 > running`, `✓ ALL 847 CLOSED`.
   - Famille : Monospace pur (ex: *SF Mono*, *JetBrains Mono*, *Fira Code*).
   - Style : Alignement gauche, syntaxe type terminal de code avec coloration syntaxique (mots-clés verts, variables cyan, booléens orangers).

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : 1920x1080 (16:9), cadencée à 30.0 fps constants.
- **Durée totale** : 51.243 secondes (1537 frames).
- **Repères spatiaux et composition** :
  - La zone d'action 3D principale est rigoureusement inscrite dans un carré central 1080x1080.
  - La mascotte Clawd est positionnée au tiers inférieur vertical (axe Y = 620px), ancrée sur le plancher du décor.
  - Les titrages cinétiques occupent le coin inférieur gauche (marge X: 96px, marge Y: 96px du bas).
  - Les badges de statut (ex: `tabs: 847`) occupent le coin supérieur droit (marge X: 96px, marge Y: 80px du haut).
- **Paramètres de Caméra 3D** :
  - Type : Perspective Camera (Three.js / Blender).
  - Champ de vision (FOV) : 42 degrés pour les scènes de bureau (rendu studio posé), basculant à 65 degrés (grand angle dynamique) lors des séquences d'action (DEBUG flamethrower et speed lines zoom).
  - Position standard : `x: 0, y: 1.8, z: 5.2`, cible orientée vers le torse de la mascotte `x: 0, y: 0.8, z: 0`.
  - Mouvements :
    - Punch Zoom : Avancée instantanée de Z: 5.2 à Z: 3.1 sur 6 frames avec amorti exponentiel.
    - Camera Shake : Bruit pseudo-aléatoire sur X et Y d'une amplitude de ±8px lors des impacts de kicks et tirs de flammes.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels & Découpage Musical

- **Tempo musical mesuré** : **152.0 BPM** (tempo électro-pop rapide, calé au métronome).
- **Durée par temps (Beat - noire)** : `0.3947 seconde` = **11.84 frames** à 30 fps (arrondi standard à 12 frames par alternance 12 / 12 / 12 / 11 frames).
- **Durée par demi-mesure (2 temps)** : `0.7895 seconde` = **23.68 frames** (~24 frames).
- **Durée par mesure complète (Bar 4/4)** : `1.5789 seconde` = **47.37 frames** (~47.4 frames).
- **Bloc standard de scène (2 mesures = 8 temps)** : `3.158 secondes` = **94.7 frames** (~95-96 frames).
- **Bloc étendu de scène (4 mesures = 16 temps)** : `6.316 secondes` = **189.5 frames** (~190-192 frames).

### 4.2. Profils Mathématiques d'Easing

Toutes les animations obéissent à quatre courbes normalisées :

1. **Pop Punch-In (Entrée des Titres & Éléments UI)** :
   - Fonction : Amorti élastique avec léger rebond (overshoot).
   - Formule : `cubic-bezier(0.175, 0.885, 0.32, 1.275)` sur 12 frames (0.4s).
   - Comportement : Scale passe de 0.2 à 1.08 en 8 frames, puis se stabilise à 1.0 en 4 frames.

2. **Snappy Slide-Up (Textes et Cartouches)** :
   - Fonction : Décélération violente.
   - Formule : `cubic-bezier(0.16, 1, 0.3, 1)` (Expo Out).
   - Comportement : 85% de la translation verticale parcourue dans les 4 premières frames.

3. **Manga Speed Line Punch (Transitions Flash)** :
   - Fonction : Flash instantané (1 frame) suivi d'un zoom linéaire sur 4 frames (`linear`), puis cut sec.

4. **Wiggle & Floating Idle (Mascotte et Cartes en lévitation)** :
   - Formule : `Math.sin(time * frequency) * amplitude`.
   - Paramètres pour la mascotte : `frequency: 2.5 rad/s`, `amplitude: 0.05m en Y`, rotation subtile de ±1.5° sur Z.

---

## 5. Pipeline de Post-Processing & Shaders

Pour reproduire fidèlement l'ambiance visuelle du film lors d'une génération par code :

1. **Halftone Dot Pattern (Demi-teintes Comic)** :
   - Appliqué sur le côté droit de l'écran en mode DUAL.
   - Fréquence de la trame : 1 point tous les 16px sur une grille orientée à 45°.
   - Taille des points modulée par la luminance : rayon de 2px dans les ombres à 7px dans les hautes lumières.

2. **Anime Radial Speed Lines Shader** :
   - Généré procéduralement via un calcul polaire `atan2(y - cy, x - cx)`.
   - Bruit unidimensionnel en angle échantillonné à haute fréquence, seuillé pour produire des traits acérés convergeant vers le centre de gravité de Clawd.
   - Alpha modulé radialement : centre dégagé (rayon 180px), opacité maximale en périphérie (bords d'écran).

3. **Chromatic Aberration (Séparation RVB)** :
   - Décalage radial des canaux rouge et bleu proportionnel à la distance au centre :
     `offset = pow(distance_from_center, 2.0) * 0.008`.
   - Visible particulièrement lors de la scène 05 (ANALYZE) et lors des explosions de flammes.

4. **Bloom & Glow Écran** :
   - Seuil de luminance : `threshold: 0.82`, rayon de diffusion : `24px`, intensité : `1.4`.
   - Utilisé sur les néons Matrix verts, les flammes orange, et les lentilles des lunettes de Clawd.
