# 01. Direction Artistique & Design System Technique

Ce document formalise l'intégralité du langage visuel et technique de la vidéo `minchoi-check-out.mp4` (vidéo de présentation / manifesto de la marque *Hypergentik*, créée par Min Choi / @minchoi). Il est conçu pour être directement ingéré par des agents de fabrication logicielle (Remotion, WebGL/Three.js, SVG/GSAP, Canvas 2D).

---

## 1. Archétype Visuel & Philosophie

L'esthétique du film repose sur un équilibre rigoureux entre trois registres :
1. **Dark Cybernetic Minimalism / Terminal Hacker** : Fond noir abyssal, trame alvéolaire hexagonale en filigrane sombre, typographie monospace de console avec curseur bloc clignotant, interfaces filaires néon.
2. **Neo-Brutalist Tech Editorial** : Typographies grotesques suisses géantes en graisse Bold/Medium avec tracking ultra-serré (`-0.03em`), composition asymétrique dense, contrastes binaires tranchés sans dégradés mous.
3. **Hyper-Luminescent Toxic Green Accent** : Une couleur signature omniprésente, un vert néon acide hyper-saturé (`#5DFF26` / `#83FF6B`) qui évoque la luminescence du phosphore P1 des vieux tubes cathodiques, détourné ici dans un contexte d'ingénierie logicielle et d'agents autonomes de pointe.

Le film culmine sur une inversion chromatique brutale (la séquence *Green Climax* à 00:53) où l'espace passe du noir d'encre à un plein écran vert fluorescent aveuglant, brisant la monotonie des présentations tech traditionnelles.

---

## 2. Design Tokens (Spécifications Précises)

### 2.1. Palette Chromatique

| Token Name | Hex Code | Rôle & Usage | Mode de Fusion (Blend Mode) |
|---|---|---|---|
| `bg-void` | `#050505` / `#060405` | Fond noir cosmique omniprésent | Normal |
| `bg-hex-dark` | `#080D08` / `#0B120B` | Teinte de fond subtilement teintée de vert dans les zones illuminées | Normal |
| `grid-hex-stroke` | `rgba(93, 255, 38, 0.08)` / `#111811` | Lignes de la trame alvéolaire hexagonale d'arrière-plan | Normal |
| `accent-toxic-green` | `#5DFF26` / `#6AFF3C` | Vert néon signature : verbes clés, badges de section `01`, `02`, `03`, astérisque | Normal / Additif (`screen`) |
| `accent-green-core` | `#C4FF93` / `#E2FFBF` | Cœur ultra-lumineux des nœuds du tesseract et faisceau laser central | Additif (`screen` / `lighter`) |
| `accent-green-glow` | `rgba(93, 255, 38, 0.40)` | Halo diffus (bloom) autour des éléments vectoriels et 3D | Additif (`lighter`) |
| `climax-green-bg` | `#5DFF26` / `#6AFF3C` | Fond plein vert de la séquence choc (00:53 - 00:58) | Normal |
| `climax-hex-pattern` | `#55E820` / `#4BD818` | Trame alvéolaire sur fond plein vert | Multiply |
| `climax-text-black` | `#000000` / `#050505` | Typographie noire pure sur le fond vert fluo | Normal |
| `text-primary` | `#FFFFFF` | Typographie principale, titres majeurs, verbes d'action | Normal |
| `text-secondary` | `#8E929B` / `#A1A1AA` | Données secondaires, métadonnées, sous-titres descriptifs | Normal |
| `surface-card-dark` | `rgba(13, 17, 14, 0.85)` | Fond translucide des panneaux d'interface et cartes d'état | Normal |
| `border-card-green` | `rgba(93, 255, 38, 0.35)` | Liserés et bordures filaires des cartes et fenêtres UI | Additif / Normal |
| `portal-warm-amber` | `#FF944D` / `#FFB366` | Coucher de soleil / aurore du portail mobile (chaleur humaine) | Normal |
| `portal-aurora-cyan` | `#00E5FF` / `#00FFCC` | Reflets des aurores boréales dans le carrousel 3D | Additif (`screen`) |

### 2.2. Typographie & Rôles

Le système typographique repose sur trois familles rigoureusement hiérarchisées :

1. **Grotesque Suisse Contemporaine (Display & Titres)** :
   - Famille recommandée : *Inter Tight Display*, *Neue Haas Grotesk*, ou *Geist Sans*.
   - Rôle : Titres manifestes monumentaux (`Making something good is still hard.`, `Built faster. Built like it still matters.`, `Humans, with better tools.`).
   - Caractéristiques :
     - Poids : `Bold` (700) et `Medium` (500).
     - Approche (letter-spacing) : Ultra-serrée (`-0.035em` à `-0.04em`).
     - Hauteur de ligne : Très dense (`line-height: 1.05` à `1.10`).
     - Traitement : Blanc pur (`#FFFFFF`) avec accentuation d'un mot ou d'un segment clé en vert néon (`#5DFF26`).

2. **Monospace Technique (Terminal & Prompts)** :
   - Famille recommandée : *Geist Mono*, *SF Mono*, ou *JetBrains Mono*.
   - Rôle : Lignes d'introduction et d'antithèse dactylographiées (`AI has made it remarkably easy...`, `It can generate code.`, `import const reconcile = agent(...)`).
   - Caractéristiques :
     - Poids : `Regular` (400) et `Medium` (500).
     - Curseur terminal : Bloc plein vert (`width: 0.55em`, `height: 1.1em`, background `#5DFF26`) avec clignotement franc à 2 Hz.
     - Espacement : `letter-spacing: 0.00em` sur le code, `+0.02em` sur les prompts.

3. **Logotype Spécialisé (*Hypergentik Custom*)** :
   - Rôle : Logotype `hypergentik*` apparaissant en clôture.
   - Particularités graphiques des glyphes :
     - Lettre `r` stylisée en angle droit minimaliste (rappelant un gamma minuscule `г`).
     - Point sur le `i` matérialisé par un carré vert néon parfait (`#5DFF26`).
     - Astérisque terminal à six branches arrondies, doté d'un chanfrein 3D et d'une luminescence dynamique.

---

## 3. Grille, Cadrage & Caméra

- **Résolution native** : 1920x1080 (16:9), cadencée à 60.0 fps constants.
- **Trame alvéolaire d'arrière-plan (Honeycomb Grid)** :
  - Rayon de cellule : 28px (diamètre circonscrit 56px, apothème ~24.2px).
  - Épaisseur de contour : `1px` avec opacité modulée selon la distance à la source lumineuse centrale.
  - Bascule spatiale : Le plan hexagonal est statique en 2D sur les plans manifestes, mais bascule en sol isométrique infini (`pitch: -65deg`, perspective 1000px) lors de l'apparition des panneaux logiciels (00:24).
- **Caméra & Mouvements spatiaux** :
  - **Plans 2D éditoriaux** : Caméra centrée avec dérive microscopique (subtle drift de 0.2% par seconde).
  - **Espace 3D orbital** : Orbite continue autour du tesseract 4D et de l'astérisque.
  - **Tunnel Hyperspace (00:36 - 00:40)** : Travelling avant à vitesse exponentielle (dolly-in à travers 5 anneaux hexagonaux concentriques) avec étirement relativiste des étoiles en traînées lumineuses (star streaks de ratio longueur/largeur jusqu'à 25:1).

---

## 4. Rythme, Easing & Grille Audio-Visuelle

### 4.1. Paramètres Temporels
- **Tempo musical exact** : **120.0 BPM**.
- **Durée par temps (Beat)** : `0.500 seconde` = **30.0 frames** à 60 fps.
- **Durée par mesure (Bar 4/4)** : `2.000 secondes` = **120.0 frames** à 60 fps.
- **Structure métrique** : Exactement 33 mesures musicales complètes réparties sur les 66.11 secondes du film.
- **Alignement temporel** : Tous les événements majeurs (cuts de scène, flashs, bascules de texte) sont calés à l'unité de frame près sur le premier temps de chaque mesure (frame 0, 480, 960, 1440, 1920, 2400, 3120, 3480).

### 4.2. Courbes d'Easing Clés

Les animations cinétiques du projet obéissent à trois équations mathématiques normalisées :

1. **Hyperbolic Snap-In (Expo Out)** :
   - Formule : `cubic-bezier(0.16, 1, 0.3, 1)` ou $f(t) = 1 - 2^{-10t}$.
   - Usage : Arrivée des blocs de texte imposants et montée verticale des interfaces.
   - Propriété : 85% de la course est accomplie en seulement 8 frames (0.13s), les 15% restants s'amortissent élégamment sur 22 frames.

2. **Inertial Spring Snap-Back** :
   - Paramètres physiques : `stiffness: 180, damping: 22, mass: 1.0`.
   - Usage : Stabilisation des cartes d'états `[✓]` le long du faisceau laser et recentrage de l'astérisque.
   - Propriété : Léger dépassement de consigne (overshoot de ~8%) suivi d'une stabilisation critique sans oscillation parasite.

3. **Linear Dimensional Drift** :
   - Formule : `linear`.
   - Usage : Rotation permanente de l'hypercube 4D dans les plans SO(4), défilement du champ d'étoiles et balayage de la ligne de scan laser.

---

## 5. Pipeline de Post-Processing & Effets Shader

Pour reproduire la patine organique et cybernétique à l'exportation :

1. **Selective Bloom (Glow Néon)** :
   - Seuil de luminance : `threshold = 0.72`.
   - Rayon de flou gaussien : `radius = 32px`.
   - Intensité additive : `intensity = 1.45`.
   - Cibles exclusives : Arêtes du tesseract, cœur de l'astérisque, faisceau laser vert, badges d'état cochés.

2. **Cosmic Dust & Bokeh (Profondeur de champ)** :
   - Émetteur de 400 particules blanches et vertes flottant dans l'espace 3D ($Z \in [-500, 500]$).
   - Flou de défocalisation gaussien inversement proportionnel à la distance au plan focal ($Z = 0$).

3. **Subtle CRT Scanlines & Micro-Aberration** :
   - Trame horizontale de scanlines 1px tous les 3px avec opacité de `3.5%`.
   - Aberration chromatique radiale : décalage des canaux Rouge/Bleu de 1.5px sur les bords du viewport, montant brièvement à 4.0px lors des impacts de kicks majeurs.

4. **Hexagonal Cellular Dissolve (Wipe)** :
   - Shader de transition opérant sur une grille de coordonnées hexagonales axiales $(q, r)$.
   - Seuil d'activation gouverné par un balayage linéaire combiné à un bruit de simplex 2D pour créer un front d'onde cellulaire organique à 00:58.
