# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, des tokens graphiques et des règles d'ingénierie cinématique de la vidéo `gLl6GZWastLVE2fr.mp4` (*Claude Motion Reel 2026*). Il est conçu pour être directement exploité par des agents de fabrication logicielle (Remotion, WebGL/Three.js, Canvas 2D, SVG).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de l'œuvre résulte d'un dialogue millimétré entre trois univers :
1. **Brutalisme Typographique Suisse** : Titrages monumentaux à graisse maximale, compositions asymétriques rigoureuses, grille cartésienne stricte et alternance radicale entre aplats pleins et tracés filaires (*outlined*).
2. **HUD Télémétrique de Monitoring de Code** : Encadrement viewfinder technique permanent, métadonnées temps réel incrustées à l'écran (compteur de frame `F0000`, mesure `BAR 1/8`, cadence `128 BPM`, métronome visuel `BEAT ■□□□`, indicateurs angulaires `ROT 090.0°`). L'animation s'affirme comme un artefact généré et piloté exclusivement par le code.
3. **Identité Éditoriale Contrastée & Atome Cinématique** : Un atome graphique unique, le disque rouge corail (`#EB4432`), traverse l'intégralité des 900 frames. Il se divise, se métamorphose en carré puis fleur, génère des champs d'ondes et des nuages 3D, pour finalement venir s'immobiliser et servir de point de ponctuation terminal au logotype à empattements `Claude.`.

Le film évite les artifices décoratifs superflus. Chaque transition est un impact physique franc synchronisé à la frame près sur la grille musicale à 128 BPM.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

La chromatique fonctionne par blocs mesurés, passant d'un noir carbone minimaliste à des fonds primaires saturés (crème papier, bleu cobalt, jaune ambre) reliés par le rouge terracotta signature.

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-dark` | `#0F0F11` | Noir carbone mat profond (Bars 1, 2 partiel, 3, 7) | Normal |
| `bg-cream` | `#F4EFE6` | Papier crème texturé chaleureux (Bars 4, 8) | Normal |
| `bg-blue` | `#2644EB` | Bleu cobalt électrique saturé (Bar 5 champ 3D) | Normal |
| `bg-yellow` | `#F5CE38` | Jaune bouton d'or haute visibilité (Bar 6 ruban) | Normal |
| `accent-coral` | `#EB4432` | Rouge terracotta signature Claude : point focal, onde, ruban, logo final | Normal |
| `accent-blue` | `#3854F5` | Bleu morphing intermédiaire (Bar 3) | Normal |
| `accent-yellow` | `#F6CB35` | Jaune ambre morphing fleur (Bar 3) | Normal |
| `text-white` | `#FFFFFF` | Typographie principale et repères HUD sur fond sombre | Normal |
| `text-black` | `#0F0F11` | Typographie et éléments graphiques sur fond clair | Normal |
| `hud-muted-light` | `rgba(255, 255, 255, 0.45)` | Repères télémétriques, coins de visée sur fond sombre | Normal |
| `hud-muted-dark` | `rgba(15, 15, 17, 0.45)` | Repères télémétriques, coins de visée sur fond clair | Normal |
| `hud-line-dim` | `rgba(255, 255, 255, 0.15)` | Cercles en pointillés, réticules inactifs | Normal |
| `chromatic-red` | `#FF0033` | Canal rouge du glitch d'impact (Bar 2) | Screen / Additive |
| `chromatic-cyan` | `#00FFFF` | Canal cyan du glitch d'impact (Bar 2) | Screen / Additive |

### 2.2. Stack Typographique

Trois familles typographiques sont orchestrées avec une séparation stricte des rôles :

1. **Grotesque Compacte Monumentale** (ex: *Druk Wide*, *Founders Grotesk X-Condensed / Bold*, *Neue Haas Grotesk 900*) :
   - Usage : Titrages cinétiques ("EVERY", "FRAME", "ON BEAT") et bandeaux défilants infinis (tickers horizontaux de la Bar 7).
   - Traitement : Majuscules obligatoires. Alternance entre remplissage blanc plein (`#FFFFFF`), remplissage noir (`#0F0F11`) et contour pur (`stroke: 2px #FFFFFF`, `fill: transparent`).
   - Métriques : `letter-spacing: -0.02em` sur les mots d'impact, `line-height: 0.9`.

2. **Serif Éditoriale Transitionnelle** (ex: *Claude Serif*, *Romie*, *Caslon Display*) :
   - Usage : Logotype signature `Claude.` apparaissant à la Bar 8.
   - Traitement : Fort contraste pleins/déliés, empattements biseautés affûtés, casse minuscule avec capitale initiale.
   - Point final : Remplacé visuellement par l'atome cinématique `accent-coral` (`#EB4432`).

3. **Monospace Télémétrique HUD** (ex: *JetBrains Mono*, *SF Mono*, *Space Mono*) :
   - Usage : HUD persistant supérieur et inférieur, compteurs de frame, coordonnées d'angle (`ROT 090.0°`), métriques de forme (`SHAPE SQUARE`), sous-titre `MOTION DESIGNER`.
   - Poids : Regular (400) et Bold (700).
   - Métriques : `letter-spacing: +0.05em`, chiffres tabulaires obligatoires (`font-variant-numeric: tabular-nums`).

---

## 3. Grille, Cadrage & Composition

- **Résolution native** : 1920x1080 (16:9), cadencée à 60.0 fps constants.
- **Zone utile & Viewfinder framing** :
  - 4 repères de coin `[ ]` en filets vectoriels de 1.5px d'épaisseur situés à 36px des bords externes.
  - Dimensions de chaque coin : branches de 18px horizontalement et verticalement.
- **HUD Supérieur (Y = 56px)** :
  - Gauche : `CLAUDE MOTION REEL 2026` (Monospace 14px, opacité 70%).
  - Droite : `BAR X/8  128 BPM` (Monospace 14px bold, synchronisé sur l'index de mesure en cours).
- **HUD Inférieur (Y = 1024px)** :
  - Gauche : Métronome visuel à 4 temps `BEAT ■□□□`, `BEAT □■□□`, `BEAT □□■□`, `BEAT □□□■`.
  - Droite : Compteur frame-accurate `FRAME XXXX / 0900` au format 4 chiffres avec zéros non significatifs.
- **Centre d'Origine Géométrique** :
  - Coordonnée universelle `(960, 540)` : point de convergence et d'émission de l'atome corail, des divisions orbitales, des ondes de phyllotaxie et des anneaux polaires.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels & Métriques Rythmiques

L'ensemble de la timeline est verrouillé mathématiquement sur le tempo musical :
- **Tempo musical** : **128.0 BPM** exact.
- **Durée par temps (Beat)** : `60 / 128 = 0.46875 seconde` = **28.125 frames** à 60 fps.
- **Durée par mesure (Bar 4/4)** : `4 * 28.125 = 112.5 frames` (1.875 seconde).
- **Durée totale (8 mesures)** : `8 * 112.5 = 900 frames` (15.000 secondes pile).

Tous les changements de plan majeurs (cuts de scène) surviennent strictement sur le beat 1 de chaque mesure (offsets de 112.5 frames). Les événements secondaires (divisions géométriques, pulsations, impulsions d'ondes) surviennent sur les beats 2, 3 et 4.

### 4.2. Profils d'Easing Mathématiques

1. **Snap & Settle (Expo Out Brutal)** :
   - Fonction : `cubic-bezier(0.16, 1, 0.3, 1)` ou `t => 1 - Math.pow(2, -10 * t)`.
   - Utilisation : Arrivée des mots kinetic typo, morphing des formes polygonales (Bar 3), déploiement des anneaux de ticker (Bar 7).
   - Dynamique : 80% du déplacement est complété en 4 frames (66ms), les 20% restants s'amortissent sur 14 frames.

2. **Impulsion Sinusoïdale Transitoire (Beat Pulse)** :
   - Formule : `scale(1 + 0.15 * Math.exp(-decay * t) * Math.sin(freq * t))` sur chaque front de beat.
   - Utilisation : Soubresauts des compteurs HUD, pulsations de l'atome corail, ondes de choc de la grille.

3. **Mouvement Continu Linéaire (Linear Flow)** :
   - Fonction : `linear`.
   - Utilisation : Défilement horizontal des tickers de texte, rotation orbitale des anneaux concentriques, balayage de la courbe de Bézier du ruban.

---

## 5. Pipeline de Post-Processing & Rendu

1. **Grain Argentique Subtil** :
   - Shading de bruit monochrome appliqué en surimpression globale (blend mode `overlay`, opacité 4%).
   - Fréquence temporelle : renouvelé toutes les 2 frames pour conserver une granularité fine sans scintillement agressif.
2. **Aberration Chromatique d'Impact** :
   - Décalage radial RGB activé uniquement sur les impacts de kick violents (notamment Bar 2, frames 141 et 169).
   - Déplacement du canal rouge de `+6px` sur X et du canal cyan de `-6px` sur X, s'estompant en 5 frames.
3. **Ghosting / Traînée de Rémanence (Motion Trails)** :
   - Sur les formes morphing en rotation rapide (Bar 3) et sur le ruban (Bar 6) : accumulation de 3 à 5 échantillons temporels retardés de 1 frame avec décroissance exponentielle d'opacité (`0.4`, `0.2`, `0.1`, `0.05`).
