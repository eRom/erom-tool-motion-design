# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel et technique de la vidéo `NZmVCE0HQqbmkf0i.mp4` (MIRR. - *Cała firma budowlana w jednym miejscu*, solution d'exploitation et d'intelligence de gestion pour entreprises du bâtiment). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas 2D).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de MIRR. incarne le **B2B Industrial High-End / Dark Modernity** :
1. **Dark UI Chirurgicale & Contrastes Luminescents** : Rejet absolu du dark-mode terne ou des dégradés violets génériques. La scène baigne dans un noir charbon profond (`#050507`), sur lequel tranche une surface sombre technique (`#111111`) illuminée par des accents néon menthe/cyan (`#6FD7CB`), ambre (`#C6AE3C`) et carmin (`#EF4141`).
2. **Dense B2B Operational Clarity** : Chaque écran présente des données de production réalistes (devis métré au m², factures fournisseurs NIP, pointage d'ouvriers à la seconde près, TVA, marge brute de chantier en temps réel). L'animation valorise la précision comptable et l'immédiateté de l'action.
3. **Collision Physique 2D / 3D Isométrique** : Les interfaces plates (tableaux, formulaires, messagerie) s'élèvent et pivotent dans un espace 3D avec perspective calibrée (DoF, motion blur cinétique, ombres portées douces, reflets spéculaires discrets), conférant un poids matériel tangible aux artefacts logiciels.
4. **Le Noyau Conducteur (The Core)** : Une pastille luminescente cyan (`#6FD7CB`) fait office de fil conducteur narratif et physique. Elle sert tour à tour de pointeur d'alerte, de moteur d'attraction gravitationnelle, d'avatar de pensée de l'agent IA, de centre orbital et enfin de point final (`.`) du logo de marque.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-void` | `#030303` / `#050507` | Fond noir charbon profond, vignetté en périphérie | Normal |
| `bg-surface-elevated` | `#111111` / `#16181D` | Cartouches de cards, conteneurs Kanban, modales de prompt | Normal |
| `surface-border-subtle` | `rgba(255, 255, 255, 0.08)` | Bordures fines de conteneurs UI (1px solid) | Normal |
| `accent-teal-primary` | `#6FD7CB` | Accent maître : pastille noyau, bouton CTA, marges positives, focus border | Normal / Additif (`screen`) |
| `accent-teal-glow` | `rgba(111, 215, 203, 0.35)` | Halo de bloom et lueur d'élévation sur cartes actives et CTA | Additif (`screen` / `lighter`) |
| `accent-red-alert` | `#EF4141` | Bouton STOP pointeuse, liseré créances impayées, tag PRZEGRANE | Normal |
| `accent-amber-warning` | `#C6AE3C` | Liseré dettes fournisseurs (`PRZETERMINOWANE ZOBOWIĄZANIA`) | Normal |
| `accent-green-success` | `#4B9370` / `#22C55E` | Badge statut ouvrier `PRACUJE`, cartouche `WYGRANE 12` | Normal |
| `text-primary` | `#FFFFFF` | Typographie principale, titres majeurs, KPI cardinaux | Normal |
| `text-secondary` | `#8F94A0` | Métadonnées HUD, sous-titres, dates, chiffrage passif | Normal |
| `text-tertiary` | `#525660` | Graduations de dates secondaires, labels de colonnes inactives | Normal |
| `paper-invoice-bg` | `#F1EEE5` | Fond de document facture papier et devis imprimé | Normal |
| `paper-ink-dark` | `#1A1D20` | Texte et filets imprimés sur documents administratifs | Normal / Multiply |

### 2.2. Typographie & Stack Font

Le système typographique repose sur une stricte hiérarchie fonctionnelle :

1. **Titres Monumentaux & Identité (Neo-Grotesque Géométrique)** :
   - Familles recommandées : *Inter Display*, *Geist*, *Neue Haas Grotesk Bold*.
   - Usage : Titre de marque `MIRR.`, titres de modules (`PULPIT`, `ZAPYTANIA`, `FINANSE`), accroches cinétiques (`Piszesz po ludzku.`, `Ekipa klika Start i Stop.`, `Cała firma budowlana w jednym miejscu.`).
   - Caractéristiques : Graisse `Black` (900) et `Bold` (700), tracking serré (`-0.03em`), minuscules à double-étage.

2. **Chiffres Tabulaires & Données Métier (Technical Monospace with Dotted Zero)** :
   - Familles recommandées : *JetBrains Mono*, *Geist Mono*.
   - Usage : Compteurs de marge (`+42%`, `30,1%`), montants financiers (`237 058,54 zł`, `91 830,00 zł`), chronomètres d'équipe (`6:16:42`, `8:30:00`), surfaces et ratios (`180 m²`, `165 zł`).
   - Traitement : Chiffres à largeur fixe (`font-variant-numeric: tabular-nums`), zéro doté d'un point central (`0̇`), ponctuation monétaire fine.

3. **Micro-HUD & Télémétrie Opérationnelle (Micro Monospace Tracké)** :
   - Familles recommandées : *JetBrains Mono Medium*, *SF Mono*.
   - Usage : Cartouche de timeline inférieur gauche (`01 —— PULPIT`, `08 —— CZAS PRACY EKIPY`), étiquettes de contexte (`PONIEDZIAŁEK · 21:47 · FIRMA BUDOWLANA`), badges système (`KSEF`, `MAIL`, `ZDJĘCIE`).
   - Traitement : `text-transform: uppercase`, taille `10px - 12px`, `letter-spacing: +0.08em` à `+0.12em`.

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : 1280x720 (16:9), cadencée à 60.0 fps constants (2927 frames totales).
- **Repères de Cadrage & HUD Anchor** :
  - Coin inférieur gauche (`x: 40px, y: 680px`) : Indicateur de chapitre persistant avec tiret cadratin (`## —— NOM DU MODULE`) ou compteur séquentiel (`01 / 04 SPRAWY`, `01 / 08`).
  - Coin inférieur droit (`x: 1240px, y: 680px`, aligné à droite) : Compteurs d'étapes d'introduction.
- **Cinématique de Caméra & Perspective 3D** :
  - **Plan 2D Orthographique** : Réservé aux micro-moments de concentration (l'invitation naturelle de l'agent 00:20, les flash-cuts staccato 00:38).
  - **Perspective Isométrique Dynamique (Tilt 3D)** :
    - `perspective: 1200px`.
    - Rotation combinée : `rotateX(15deg)` à `25deg` (plongée) et `rotateY(-5deg)` à `-12deg` (légère bascule latérale).
    - Caméra en travelling continu (slow push-in ou dolly-in) avec un amorti exponentiel pour maintenir une tension cinétique constante.
  - **Motion Blur Calibré** : Obturateur à 180° (shutter angle 180°), actif lors des whip-pans horizontaux et des projections de cartes.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels & Calibrage BPM

- **Tempo musical exact** : **129.2 BPM**.
- **Durée par temps (Beat)** : `0.4644 seconde` = **27.86 frames** à 60 fps.
- **Durée par mesure (Bar 4/4)** : `1.858 seconde` = **111.46 frames** à 60 fps.
- **Grille de Découpage Fonctionnel** : Chaque module métier (Dashboard, Kanban, Devis, Factures, Agent, Telegram, Timers) s'étale sur une plage rigoureusement calibrée de **2 mesures complètes** (~222 frames / ~3.7 secondes), respectant une respiration musicale de métronome.

### 4.2. Profils Mathématiques d'Easing

1. **Snap & Settle (Expo Out)** :
   - CSS : `cubic-bezier(0.16, 1, 0.3, 1)`.
   - Utilisation : Entrées des blocs typographiques, cartes de KPI, arrivée des écrans après whip-pan.
   - Comportement : 75% du déplacement absorbé en 5 frames, stabilisation soyeuse sur les 15 frames suivantes.

2. **Damped Spring (Ressort Critique)** :
   - Paramètres physiques : `mass: 1.0, stiffness: 180, damping: 14`.
   - Utilisation : Déplacement de la pastille cyan d'un quadrant à l'autre dans l'intro, élévation de la carte prospect `Jakub Kowalski` dans le Kanban.
   - Comportement : Léger dépassement (overshoot 8%) avant calage précis.

3. **Linear Velocity / Continuous Spin** :
   - Easing : `linear`.
   - Utilisation : Rotation des chiffres de chronomètres, balayage vertical du rayon laser OCR, révolution orbitale des 6 pastilles satellites autour du noyau MIRR.

---

## 5. Pipeline de Post-Processing & Effets Shader

Pour reproduire fidèlement le rendu à l'exportation :

1. **Bloom Luminescent Additif** :
   - Seuil (Threshold) : `0.75`.
   - Rayon : `18px - 28px`.
   - Application sélective : Pastille cyan `#6FD7CB`, pourcentage géant `+42%`, chiffres du chronomètre validé, bouton CTA `ZAŁÓŻ KONTO →`.
2. **Grain Subtil de Surface** :
   - Bruit monochrome procédural (1px, opacité 3.5% à 4.5%, blend-mode `overlay`) pour conférer une texture physique et masquer les artefacts de compression sur aplats sombres.
3. **Vignettage Optique Cinématographique** :
   - Dégradé radial doux depuis `rgba(0,0,0,0)` à 55% du centre jusqu'à `rgba(0,0,0,0.65)` dans les quatre coins.
4. **Flou de Profondeur (Depth of Field / Tilt-Shift)** :
   - Flou gaussien progressif (`blur(0px)` au point focal jusqu'à `blur(8px)` en arrière-plan) accentuant l'effet de maquette 3D sur les tables et tableaux Kanban.
