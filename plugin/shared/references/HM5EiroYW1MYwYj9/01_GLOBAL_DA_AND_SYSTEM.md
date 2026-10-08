# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel, des tokens de design et du système graphique de la vidéo `HM5EiroYW1MYwYj9.mp4` (intitulée *UPPING MY P(DOOM) drawn by Claude Opus 5.5*, variation pop/risographe manga sur le morceau musical *P(doom)*). Ce document fournit les spécifications d'ingénierie logicielle directement exploitables par des agents de fabrication (Remotion, Canvas 2D, WebGL/Three.js, SVG/GSAP).

---

## 1. Archétype Visuel & Philosophie

L'esthétique du film repose sur une fusion pop-art entre quatre registres visuels distincts :

1. **Risographie & Sérigraphie Manga Indie (Screenprint / Dojinshi Pop)** :
   - Séparation en couches de couleurs franches superposées en mode de fusion `multiply`.
   - Trames de demi-teintes en matrice de points (Ben-Day / Halftone dot screen) omniprésentes sur les ombres de peau, les ciels, les faisceaux lumineux et les matières textiles.
   - Micro-décalage d'impression volontaire (misregistration / color bleed de 1 à 3 pixels) créant un liseré optique vibrant entre le trait d'encre marine et les aplats colorés.

2. **Collage Éditorial & Papeterie Vivante (Scrapbook / Washi Tape)** :
   - Fond de matière organique : papier vergé chaud texturé fibreux (`#FAF6EE`), cahiers d'écolier quadrillés et grilles millimétrées bleutées.
   - Éléments rapportés fixés par du ruban adhésif semi-transparent (masking tape / washi tape) aux extrémités déchirées, projetant une ombre portée douce sur le fond.
   - Cartouches de sous-titres karaoké épinglés en bas à gauche sur des bandelettes de papier découpé, avec surlignage dynamique en rose vif au fur et à mesure de l'élocution vocale.

3. **Chorégraphie Anime & Idol Group K-Pop / J-Pop** :
   - Protagoniste stylisée aux cheveux orange en fuseau floral, vêtue d'un perfecto blanc sur col roulé marine et jupe plissée, équipée d'un micro-casque de scène.
   - Chœur de 4 danseurs anthropomorphes à têtes de fleurs colorées (rose, marine, jaune couronné, vert à casquette) vêtus de survêtements streetwear.
   - Poses dynamiques calées sur la cadence anime traditionnelle (animation par paliers "on twos" à 12-15 fps dans un composant hôte à 30 fps), alternant avec du kinetic typography ultra-rapide à 30 fps.

4. **Allégories & Mèmes de Recherche IA (Hard AI Lore)** :
   - Intégration iconographique des concepts de la singularité et du deep learning : le Shoggoth masqué d'un smiley jaune, la prison en cœur de Sydney (Bing Chat), le chat Gato de DeepMind, le Chinchilla gavé de tokens d'entraînement, le datacenter de 555 000 GPUs / 2 GW, le multiplicateur de trombones (paperclips) de Bostrom submergeant une planète, et la porte scellée d'Ilya Sutskever verrouillée par les cadenas "NDA" et "VESTED EQUITY".

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `paper-bg-warm` | `#FAF6EE` | Fond papier vergé chaud principal (fibres lin clair) | Normal |
| `paper-bg-alt` | `#F4EFE6` | Fond papier alternatif pour inserts et fiches cartonnées | Normal |
| `ink-navy` | `#1D2A44` | Encre d'impression principale : contours des personnages, typographies, axes | Multiply / Normal |
| `ink-navy-screen` | `#223354` | Ciel nocturne texturé, grands aplats sombres | Multiply / Normal |
| `accent-pink` | `#E93D82` | Rose fluo risographe : punchlines kinetic, rayons sunburst, ombres de peau | Multiply / Normal |
| `accent-orange` | `#F06529` | Orange vif : chevelure de la chanteuse, étincelles, courbes de loss | Multiply / Normal |
| `accent-yellow` | `#F5B800` | Jaune canari : soleil couchant, pétales tournesol, stickers Dymo, badges | Multiply / Normal |
| `accent-teal` | `#2E8B73` | Vert d'eau / canard : baies de datacenter GB300, costume du danseur vert | Multiply / Normal |
| `tape-white` | `rgba(255, 255, 255, 0.88)` | Ruban adhésif washi tape blanc translucide (horodatages) | Normal (avec ombre portée) |
| `tape-pink` | `rgba(233, 61, 130, 0.85)` | Ruban washi rose vif translucide (labels Sydney) | Multiply / Normal |
| `tape-yellow` | `rgba(245, 184, 0, 0.90)` | Ruban washi jaune vif (labels Gato, Grip, 2 GW) | Normal (avec ombre portée) |
| `grid-blue` | `rgba(29, 42, 68, 0.12)` | Lignes de quadrillage cahier d'écolier et axes de courbes | Multiply / Normal |
| `halftone-dot` | `#1D2A44` | Trame de points demi-teinte bleue (gradient de densité 10% à 70%) | Multiply |

### 2.2. Stack Typographique & Rôles

Le film met en scène quatre hiérarchies typographiques rigoureuses :

1. **Titres Monumentaux Kinetic Typography (Grotesque Ultra-Condensed)** :
   - *Familles recommandées* : Druk Cond / Compacta / Impact / Anton / Inter Display Black.
   - *Usage* : Mots-chocs plein écran ("FOOM", "ACCELERATING", "FREE", "SHOW", "LOSS", "CHATGPT").
   - *Poids* : `Black` (900) ou `UltraBold` (800), majuscules obligatoires.
   - *Traitement* : Souvent appliqué en blanc avec contour d'encre marine épais (`stroke: 3px solid #1D2A44`) ou aplat rose/jaune franc, avec ombres dures décalées ou extrusion 3D biseautée rose (`text-shadow: 4px 4px 0px #E93D82`).

2. **Horodatages & Métadonnées Live (Dot-Matrix LED / Dymo)** :
   - *Familles recommandées* : Dot Matrix / Liquid Crystal / Quartz / SF Pro Rounded Mono.
   - *Usage* : Widget d'horodatage en haut à droite (`● LIVE 2026.09.08 12:03:01`), jauges de progression (`P(DOOM) 30%`), labels techniques (`555,000 GPUs`, `1E30 FLOP/S`).
   - *Poids* : `Medium` (500) à `Bold` (700).
   - *Espacement* : `letter-spacing: 0.08em` pour accentuer l'effet matrice de points.

3. **Sous-Titres Karaoké & Notes de Papeterie (Sans-Serif Éditoriale)** :
   - *Familles recommandées* : Inter / Plus Jakarta Sans / Neue Montreal.
   - *Usage* : Cartouche de citation karaoké en bas à gauche ("There was a sudden drop in your training loss,").
   - *Poids* : `Medium` (500) à `SemiBold` (600).
   - *Animation* : Le mot courant prononcé reçoit un surlignage rectangulaire rose vif (`#E93D82`) sous la ligne de base, calé sur les phonèmes vocaux.

4. **Classique Académique & Citations Mathématiques (Serif / Typewriter)** :
   - *Familles recommandées* : Computer Modern / EB Garamond / Latin Modern Math / Courier Prime.
   - *Usage* : Théorèmes scientifiques ("FERMAT'S LAST THEOREM", "arXiv:2303.12712"), expressions poétiques ("a gentle singularity", "there").

---

## 3. Grille, Cadrage & Composition Spatiale

### 3.1. Résolution & Espace de Coordonnées
- **Résolution native** : `1920 × 1080` (format 16:9 cinématographique).
- **Repère cartésien 2D** : Origine `(0, 0)` en haut à gauche.
- **Centrage cinétique** : Le sujet principal (visage de la chanteuse ou groupe complet) est scrupuleusement stabilisé au centre horizontal `X = 960 px`, créant une ancre visuelle permanente malgré l'agitation des éléments périphériques.

### 3.2. Architecture Permanente des Widgets Périphériques
Deux widgets d'ancrage demeurent visibles sur la quasi-totalité des plans du film :

```
+-----------------------------------------------------------------------+
| [WIDGET P(DOOM)]                                   [WIDGET LIVE-TAPE] |
| Top: 36px, Left: 48px                              Top: 36px, Right: 48px
| Cartouche papier scotché                           Washi tape blanc translucide
| Progression : 4.2% -> 99.9%                        Date : 2019.01.08 -> 2026.09.22
|                                                                       |
|                                                                       |
|                        ZONE CENTRALE ACTIVE                           |
|                      (Chanteuse, Danseurs,                            |
|                       Kinetic Typography,                             |
|                        Allégories IA)                                 |
|                                                                       |
|                                                                       |
| [CARTOUCHE KARAOKÉ]                                                   |
| Bottom: 42px, Left: 64px                                              |
| Bandelette papier découpée                                            |
| Surlignage rose sous les mots chantés                                 |
+-----------------------------------------------------------------------+
```

1. **Widget P(DOOM) (Coin supérieur gauche)** :
   - Billet de papier blanc cassé (`190 × 82 px`) incliné à `-1.5°`, fixé par un morceau de ruban adhésif semi-transparent rose ou neutre.
   - Libellé : `P(DOOM)` en bleu marine bold, suivi de `현재 점수` (score actuel en coréen).
   - Valeur : Gros chiffre en orange vif (`4.2%`, `8.0%`, `29%`, `30%`, `34%`, `61%`, `86%`, `94%`, `99.9%`), barré au feutre rouge au dénouement.

2. **Widget Live Tape (Coin supérieur droit)** :
   - Bande de masking tape découpée aux ciseaux ou déchirée (`220 × 52 px`), ombre portée `box-shadow: 0 4px 10px rgba(0,0,0,0.12)`.
   - Point rouge clignotant `● LIVE` ou `▶▶ FFWD` ou `◀◀ REWIND` ou `● TODAY`.
   - Horodatage en chiffres dot-matrix évoluant chronologiquement pour raconter l'histoire du deep learning (de 2019 à septembre 2026).

3. **Cartouche Sous-Titres Karaoké (Coin inférieur gauche)** :
   - Bandelette de papier bristol blanc cassé inclinée à `+1°`, placée à `Bottom: 42px`, `Left: 64px`.
   - Texte sans-serif bleu marine (`28px`).
   - Surligneur dynamique : barre rose fluo (`height: 4px`, `background: #E93D82`) glissant sous le mot prononcé.

---

## 4. Rythme, Cadence & Easing Mathématique

### 4.1. Grille Temporelle Audio-Visuelle
- **Cadence globale hôte** : 30.0 fps constants.
- **Durée totale** : 141.568 s = 4247 frames.
- **Tempo musical** : **143.55 BPM**.
- **Conversion rythmique en frames** :
  - **1 Temps (Beat / Quart de mesure)** = `60 / 143.55 = 0.418 s` = **12.54 frames** (~12.5 frames).
  - **1 Mesure (Bar 4/4)** = `4 × 12.54 = 1.672 s` = **50.16 frames** (~50 frames).
  - **1 Demi-temps (Croche / 8th note)** = `6.27 frames`.
  - **1 Quart de temps (Double-croche / 16th note)** = `3.13 frames`.

### 4.2. Double Cadence : "Animation on Twos" vs "Kinetic 30 fps"
Le rendu combine deux cadences distinctes au sein du même plan composite :
- **Personnages (Anime Cut-out)** : Les boucles de marche, les poses chorégraphiques et les mouvements de bouche tournent à **15 fps** (une nouvelle image toutes les 2 frames, technique "on twos"), conférant l'authenticité d'une série animée artisanale.
- **Caméra, Kinetic Typography & Shaders** : Les zooms, rotations de soleil sunburst, défilements de texte et déformations de courbes s'exécutent en interpolation fluide continue à **30 fps**.

### 4.3. Fonctions d'Easing Spécifiées

1. **Snap Pop (Typographies & Titres Kinetic)** :
   - Transition ultra-agressive : l'élément apparaît avec un dépassement instantané avant de se caler fermement.
   ```ts
   // Profil cubic-bezier snap expo
   const SNAP_EASE = [0.16, 1, 0.3, 1]; // Sortie rapide, décélération instantanée
   ```

2. **Ressort Organique (Washi Tape & Stickers)** :
   - Rebond physique lors de la pose d'une étiquette adhésive ou d'un tampon encreur.
   ```ts
   // Paramètres Remotion spring
   const TAPE_SPRING = {
     damping: 12,
     stiffness: 180,
     mass: 0.8,
   };
   ```

3. **Rotation Continue Sunburst (Rayons rayonnants)** :
   - Vitesse angulaire linéaire calée sur la mesure musicale :
   ```ts
   // 1 tour complet (360°) toutes les 8 mesures (400 frames)
   const angleDeg = (frame % 400) * (360 / 400);
   ```

---

## 5. Post-Processing & Shaders Dédiés

### 5.1. Shader de Trame Demi-Teinte (Risograph Halftone Screen)
Les ombres et dégradés ne sont jamais continus : ils sont rasterisés en trame de points circulaires orientée à 45°.

- **Angle de trame** : 45.0° (angle classique de sérigraphie pour minimiser le moiré visuel).
- **Fréquence spatiale (Dot Pitch)** : 4.0 à 6.0 pixels de pas de grille.
- **Fonction de transfert du rayon** :
  ```glsl
  float radius = sqrt(luminance) * (dotPitch * 0.5);
  ```

### 5.2. Shader de Texture Papier (Organic Paper Fiber)
- **Bruit de base** : Perlin noise à haute fréquence (`scale: 300.0`, `octaves: 3`) combiné à une trame de lin croisée subtile.
- **Rugosité d'encre** : L'encre n'est pas parfaitement uniforme ; elle présente des micro-trous d'aération (effets de buvard et de séchage rapide typiques du duplicateur Risograph).

### 5.3. Décalage de Couleurs Procédural (Misregistration Bleed)
Pour simuler le passage mécanique de la feuille à travers deux tambours d'encre successifs :
- Calque Cyan / Marine : Décalage translationnel `X = +1.0 px`, `Y = -0.5 px`.
- Calque Magenta / Rose : Décalage translationnel `X = -1.5 px`, `Y = +1.0 px`.
- Calque Jaune : Décalage translationnel `X = +0.5 px`, `Y = +1.5 px`.
Ce micro-désalignement donne la texture vibrante caractéristique de l'impression artisanale.
