# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, graphique et cinématique de la vidéo `chTkL3ZwF5yuxh8G.mp4` (titre officiel : *Crew in the Dark* / *Every Frame Is Code* - production Septembre 2026). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas 2D).

---

## 1. Archétype Visuel & Philosophie

L'esthétique de *Crew in the Dark* incarne le manifeste de la nouvelle ère du motion design généré par code et orchestré par agents IA ("Zero After Effects"). Le film articule trois registres visuels distincts :

1. **Terminal d'Agent IA & Télémétrie Chirurgicale** :
   - Invites de commande interactives (`* > make it dynamic`, `* > it was`), curseurs blocs clignotants, arborescences de répertoires (`~/crew-in-the-dark · zsh`), fenêtres terminales sombres.
   - Échantillonnage de probabilités de tokens (`P(next) · context`, `dynamic: 0.62`, `cinematic: 0.21`, `beautiful: 0.09`, `top-p 0.95`, `400K tokens`).
   - Bribes de code réel imprimées directement sur des rubans de pellicule 35mm (syntaxe GSAP `power4.out`, `path.getPointAtLength`, `code.render({ fps: 30 })`).

2. **Satire du Motion Design Générique vs Multi-Agent Crew** :
   - Dérision des modèles "One prompt, one shot" : un tapis infini en perspective 3D composé de centaines de cartes arrondies identiques arborant le dégradé néo-violet stéréotypé de l'IA commerciale, toutes estampillées `Seamless` ou `SAME`.
   - Modélisation du workflow multi-agent en boîtes filaires 3D luminescentes : `REFERENCE-BREAKER`, `STORYBOARDER`, `BUILDER`, `FILM-REVIEWER`, interconnectées en réseau de nœuds stellaire autour du symbole astérisque d'Anthropic.

3. **Bureaucratie Tactile & Métacinéma** :
   - Fiches de catalogue d'exposition et formulaires de revue (`FORM 7-A`, `FORM 4-C`), feuilles quadrillées ou lignées à marge rouge.
   - Claquage mécanique de tampons encreurs d'alerte (`P0`), ratures au feutre noir de censure, ciseaux virtuels découpant le texte sur ligne pointillée ("HARD CUT").
   - Clôture métacinématographique : plateau de théâtre sombre aux rideaux de velours rouge, projecteur conique volumétrique braqué sur une chaise de réalisateur pliante (`YOU`), et clap de cinéma 3D (`PROD: CREW IN THE DARK`, `DIRECTOR: YOU`).

Le traitement colorimétrique refuse les néons criards sans intention : il ancre un fond noir carbone chaud texturé de grain argentique, dynamisé par un orange braise incandescent (`#FF5533`), avec des contrepoints sur papier crème administratif (`#EDE8DF`) et le violet générique parodié (`#5B42D6`).

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-charcoal` | `#0E0E10` | Fond noir carbone prédominant sur 85% des plans | Normal |
| `bg-surface-terminal` | `#161618` | Fenêtre terminale Claude, boîte de dialogue prompt | Normal |
| `bg-card-dark` | `#1E1C1B` | Cartes du fil social Twitter/X en perspective | Normal |
| `accent-ember` | `#FF5533` | Accent principal : étincelle, rails actifs, mot-clé `CREW`, curseur | Normal / Additif (`screen`) |
| `accent-ember-glow` | `#FF7744` | Halo volumétrique de l'étincelle et reflets de bloom | Additif (`screen` / `lighter`) |
| `accent-ember-dim` | `#99331F` | Tracés secondaires inactifs, graduations polaires discrètes | Normal |
| `text-primary` | `#FFFFFF` | Typographie principale plein fer en kinetic typo | Normal |
| `text-offwhite` | `#F2EFEA` | Couleur nominale des mots en animation GSAP (`tl.set`) | Normal |
| `text-muted` | `#737378` | Données télémétriques secondaires, labels HUD, timecodes | Normal |
| `generic-card-grad-start` | `#2E1E6B` | Teinte basse du dégradé générique parodié (bleu-indigo nuit) | Normal |
| `generic-card-grad-mid` | `#5B42D6` | Teinte médiane du dégradé générique (violet néo-IA) | Normal |
| `generic-card-grad-end` | `#43B0FF` | Teinte haute du dégradé générique (cyan électrique) | Normal |
| `paper-cream` | `#EDE8DF` | Fond des formulaires administratifs (FORM 7-A, FORM 4-C) | Normal |
| `paper-grid-line` | `#DDD8CE` | Quadrillage millimétré et lignes de bloc-notes | Normal |
| `paper-ink-black` | `#1A1A1A` | Typographie dactylographiée imprimée sur papier | Normal / Multiply |
| `stamp-red` | `#D6453D` | Tampon encreur mécanique `P0`, ligne rouge de coupe, marge | Multiply / Normal |
| `hud-grid` | `rgba(255, 255, 255, 0.08)` | Grille cartésienne 3D de fond et repères de perspective | Normal |
| `hud-axis` | `rgba(255, 255, 255, 0.22)` | Axes polaires, graduations d'angle, réticules | Normal |
| `theater-curtain-red` | `#3D1418` | Velours sombre des rideaux de théâtre latéraux | Normal |

### 2.2. Stack Typographique

Le film fait dialoguer quatre familles typographiques rigoureusement typées :

1. **Grotesque Brutaliste Monumentale** (ex: *Neue Haas Grotesk Display*, *Inter Display 900*, *Druk Wide*) :
   - Usage : Titres massifs en kinetic typography ("WOKE UP", "EVERY FRAME IS CODE", "ZERO AFTER EFFECTS", "ONE PROMPT", "EVERYBODY'S THE SAME", "IT'S A CREW", "FIND A REFERENCE", "HARD CUT", "ROLL IT AGAIN").
   - Poids : `Black` (900) et `Bold` (700), systématiquement en capitales.
   - Traitement : Plein blanc optique (`#FFFFFF`) avec accentuation d'un mot-clé en orange braise incandescent (`#FF5533`), tracking resserré (`letter-spacing: -0.03em`).

2. **Monospace Terminal & Télémétrie** (ex: *JetBrains Mono*, *SF Mono*, *Geist Mono*) :
   - Usage : Commandes shell (`$ ffmpeg -i ref.mp4 ...`), prompts interactifs (`* > make it dynamic`), fenêtres de logits (`P(next) · dynamic 0.62`), métadonnées HUD (`TC 00:00:28:21`, `FPS 30`, `FRAME 0366`, `TAKE 03`).
   - Poids : `Regular` (400) et `Medium` (500).
   - Traitement : Chasse fixe stricte, espacement normal (`letter-spacing: 0em`), blocs de prompt surlignés d'un curseur rectangulaire plein (`width: 12px`, `height: 22px`).

3. **Typewriter Administrative & Formulaires** (ex: *Courier Prime*, *Prestige Elite*) :
   - Usage : Titres de sections formulaires (`EXHIBITION CATALOGUE · MOTION WORKS 2026`, `FORM 7-A · ENTRY NO. 016 LOCKED`, `FORM 4-C · CREW REVIEW`), items de checklist dactylographiés.
   - Poids : `Bold` (700) et `Regular` (400).
   - Traitement : Encre noire mate sur papier crème (`#1A1A1A` sur `#EDE8DF`), avec barres de censure noires opaques (`height: 14px`).

4. **Cursive Néon & Serif d'Auteur** (ex: *Snell Roundhand*, *Autography*, *Bickham Script Pro*) :
   - Usage : Contrepoints ironiques et artistiques contrastant avec la brutalité géométrique : le mot *"art"* dans le formulaire FORM 7-A, et le mot *"director"* dans la scène de théâtre.
   - Poids : `Medium` cursif fluide.
   - Traitement : Tracé cursif souple avec halo lumineux néon (`drop-shadow: 0 0 12px #FF5533`).

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : **1280x720** (ratio 16:9 cinématographique standard web).
- **Framerate** : **30.0 fps** constants (3503 frames au total sur 116.757 secondes).
- **Repères de Cadrage & HUD Viewfinder** :
  - Timecode frame-accurate affiché dans les coins (`TC 00:00:18:29`).
  - Métadonnées techniques incrustées : `FPS 30`, `TAKE 01/02/03`, `RENDER PASS 02`, `HOLD 1.00 S`, `SELECT B`.
  - Repères polaires et cartésiens : coordonnées affichées (`ANGLE 138° · R 2.00`, point central `(0,0)`).
- **Système de Caméra Virtuelle** :
  - **Plans 2D Centrés** : Caméra frontale avec zooms avant modérés (0.7x à 1.2x) et secousses d'impact (screen shakes) sur les coups de grosse caisse.
  - **Plans 3D Isométriques & Plongées** :
    - Nappe infinie de cartes déclinée avec un angle de pitch à 60° et un point de fuite central bas.
    - Défilement vertical du fil social montant vers le spectateur avec profondeur de champ (DoF) progressive.
    - Trou noir gravitationnel : déformation non-linéaire radiale du plan cartésien 2D aspirant la matière vers un rayon critique `R_s`.

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels & Découpage Métrique
- **Tempo musical** : **123.05 BPM** (rythme synthpop / electronic mid-tempo).
- **Durée par temps (Beat)** : `0.4876 seconde` = **14.63 frames** à 30 fps.
- **Durée par mesure (Bar 4/4)** : `1.950 seconde` = **58.51 frames** à 30 fps.
- **Durée par section de 4 mesures (Phrase)** : `7.80 secondes` = **234.0 frames** à 30 fps.
- **Durée par bloc de 8 mesures (Couplet / Refrain)** : `15.60 secondes` = **468.1 frames** à 30 fps.

### 4.2. Courbes d'Easing Clés

Les animations cinématiques suivent quatre modèles mathématiques rigoureux :

1. **Snap-in Expo (Expo Out)** :
   - Formule : `y = 1 - Math.pow(2, -10 * t)`
   - CSS / GSAP : `cubic-bezier(0.16, 1, 0.3, 1)` ou `ease: "expo.out"`
   - Usage : Arrivée en translation Z rapide des mots géants (de `z: -400px` à `z: 0px` en 12 frames), claquage des cartes d'interface.

2. **Power4 Out (Cinematic Settle)** :
   - Formule : `y = 1 - Math.pow(1 - t, 4)`
   - GSAP : `ease: "power4.out"`, durée nominale de 0.42s (~13 frames).
   - Usage : Glissement horizontal des mots de kinetic typography et calage des positions de texte.

3. **Linear Spline Travel (Traceur Vélocité Constante)** :
   - Formule : `distance = velocity * t`
   - Usage : Tête d'étincelle naviguant le long des tracés SVG (`path.getPointAtLength(progress * totalLength)`), cercles polaires trigonométriques.

4. **Spring Overshoot (Impact Physique de Tampon)** :
   - Paramètres physiques : `mass: 1, stiffness: 240, damping: 14`
   - Usage : Frappe du tampon `P0` sur `FORM 4-C`, avec overshoot d'échelle de 12% et rebond résiduel amorti sur 8 frames.

---

## 5. Pipeline de Post-Processing & Effets Shader

Pour reproduire le rendu visuel exact à l'export dans un pipeline de fabrication :

1. **Grain 35mm Argentique (Film Grain Shader)** :
   - Bruit de sel et poivre monochrome généré par shader WebGL (ou calque SVG feTurbulence), opacité 6% à 8%, avec actualisation stochastique à chaque frame pour éviter la fixité numérique.
2. **Bloom & Glow Incandescent (Dual-Pass Gaussian Blur)** :
   - Seuil de luminance : `0.70`. Rayon de flou : 24px en passe large, 6px en passe concentrée.
   - Appliqué sur l'étincelle (`#FF5533`), la tête de traceur et les mots braise.
3. **Vignettage Radial Chaud** :
   - Masque dégradé radial inversé : centre clair avec légère dominante chaude (ambre), coins assombris à 55% d'opacité vers `#0E0E10`.
4. **Aberration Chromatique Impulsionnelle** :
   - Décalage séparé des canaux RVB : Canal Rouge décalé de `+2.5px` en X, Canal Bleu de `-2.5px` en X lors des cuts francs et des impacts percussifs, amorti en 4 frames.
