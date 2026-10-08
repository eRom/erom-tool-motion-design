# 02. Découpage Technique Chronologique Intégral

Découpage plan par plan de la vidéo de référence `2Dz1vf5VhJw5zC4D.mp4` (15.061 secondes, 904 frames à 60.0 fps, 144.0 BPM).
L'ensemble des déclencheurs audio, transitions, vecteurs de mouvement et piles de calques sont quantifiés pour une implémentation directe sous Remotion, Three.js ou Canvas 2D.

---

## 1. Vue d'Ensemble des 9 Mesures (Timeline Principale)

| Mesure | Plage de Frames | Timecode (60fps) | Scène / Label HUD | Couleur de Fond | Focus Technique Principal |
|---|---|---|---|---|---|
| **Bar 1** | 0 - 99 | `00:00:00 - 00:01:39` | Intro / Calibrage | `#05080D` | Grille cartésienne, point oscillant, onde harmonique stationnaire |
| **Bar 2** | 100 - 199 | `00:01:40 - 00:03:19` | `SCENE 01 / 07` (`IDENTITY / TYPE`) | `#FA4E20` | Split reveal de titrage, cursive serif, transition iris noir exponentielle |
| **Bar 3** | 200 - 299 | `00:03:20 - 00:04:59` | `SCENE 02 / 07` (`3D / MOGRAPH`) | Dégradé sombre radial | Matrice 3D de 20x20 cubes ondulants, sphère chromée PBR et anneaux orbitaux |
| **Bar 4** | 300 - 399 | `00:05:00 - 00:06:39` | `SCENE 03 / 07` (`KINETIC TYPOGRAPHY`) | Crème / Noir / Bleu / Corail | 4 beats staccato de 25 frames : masque inversé, défilement filaire, bandes tranchées, arc SVG |
| **Bar 5** | 400 - 499 | `00:06:40 - 00:08:19` | `SCENE 04 / 07` (`DATA / INFOGRAPHICS`) | `#F1F1E7` | Jauge circulaire 78%, compteur +312%, barchart 12 mois, courbe de tendance 4.7k |
| **Bar 6** | 500 - 599 | `00:08:20 - 00:09:59` | `SCENE 05 / 07` (`GENERATIVE / PARTICLES`) | `#05080D` | 2 400 particules vectorielles, transition Curl Noise vers phyllotaxie dorée 137.508° |
| **Bar 7** | 600 - 699 | `00:10:00 - 00:11:39` | `SCENE 06 / 07` (`UI / PRODUCT MOTION`) | `#3B5DFD` dégradé | Fenêtre modale Render Queue, curseur souris, toggle, bouton mute en progress bar, toast |
| **Bar 8** | 700 - 799 | `00:11:40 - 00:13:19` | `SCENE 07 / 07` (`SHAPE / LIQUID`) | `#FA4E20` | Métaballes fluides en fusion/scission et Superformula 2D interpolée m=0.00 à 8.00 |
| **Bar 9** | 800 - 903 | `00:13:20 - 00:15:03` | OUTRO (`0 KEYFRAMES DRAGGED`) | `#05080D` | Carte de résolution finale, alignement de puce corail, typographie programmatique |

---

## 2. Découpage Plan par Plan Frame-Accurate

### Bar 1 : Frames 0 à 99 (00:00:00 à 00:01:39) - Intro & Calibrage Harmonique
- **Audio Cue / Beat** : Drone basse fréquence (45 Hz) + crépitements télémétriques, suivi d'un riser ascendant en bruit blanc filtré de la frame 85 à 99.
- **Transition Entrante** : Fade-in direct depuis noir total (`#05080D`) en 10 frames.
- **Effets & Mouvements Clés** :
  - `f=0 - 15` : Allumage des réticules de cadrage aux 4 coins et des croix centrales.
  - `f=15 - 84` : Génération d'une corde vibrante horizontale au centre de l'écran ($y = 540$). L'onde sinusoïdale stationnaire superpose 3 harmoniques avec une amplitude modulée de 0 à 28px. Au centre, une puce corail `#FA4E20` oscille verticalement en phase avec le ventre de l'onde.
  - `f=85 - 99` : L'onde subit un étirement vertical exponentiel ($Scale_y : 1 \rightarrow 80$), transformant la ligne en un rectangle blanc incandescent qui remplit tout le cadre à la frame 99.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond noir nocturne `#05080D`
  - `Z1` : Grille cartésienne millimétrée (`rgba(255, 255, 255, 0.08)`)
  - `Z2` : Onde sinusoïdale vectorielle (stroke blanc 1.5px)
  - `Z3` : Puce centrale corail (`#FA4E20`, rayon 6px)
  - `Z4` : Cartouche de titrage discret `claude / motion reel -`
- **Observation Technique** : La saturation lumineuse de la frame 99 sert de masque de découpe additif naturel pour accueillir le fond corail de la mesure suivante sans sensation de raccord brutal.

---

### Bar 2 : Frames 100 à 199 (00:01:40 à 00:03:19) - Scene 01 : IDENTITY / TYPE
- **Audio Cue / Beat** : Premier drop percussion majeure (Kick lourd + Snare percutant) à la frame 100 exacte.
- **Transition Entrante** : Cut franc post-flash sur aplat corail `#FA4E20`.
- **HUD dynamique** :
  - En haut à droite : `SCENE 01 / 07` (apparition instantanée).
  - En bas à gauche : Désembrouillage de caractères aléatoires (text scramble) vers `IDENTITY / TYPE` de la frame 100 à 118.
  - En bas à droite : Métronome calé sur le temps 1 (`■□□□`), timecode démarrant à `00:00:01:40`.
- **Effets & Mouvements Clés** :
  - `f=100 - 125` : Titre monumental `CLAUDE.` en lettres capitales blanches (Neue Haas Grotesk Bold, corps 160px). Le mot apparaît par un masque de fente horizontale (la moitié haute glisse de -40px vers le bas, la moitié basse de +40px vers le haut, fusion parfaite à f=125).
  - `f=120 - 150` : Sous-titre cursif noir `motion designer` (Serif Italique) glissant en diagonale descendante ($\Delta x = +30\text{px}, \Delta y = +20\text{px}$, opacité $0 \rightarrow 1$).
  - `f=185 - 199` : Le point final noir `.` du mot `CLAUDE.` subit une expansion radiale exponentielle ($Scale : 1 \rightarrow 150$), formant un iris noir qui engloutit l'intégralité du viewport.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond corail d'impact `#FA4E20`
  - `Z1` : Repères de visée et réticules télémétriques
  - `Z2` : Titre vectoriel `CLAUDE` (blanc `#FFFFFF`)
  - `Z3` : Cursive `motion designer` (noir `#060910`)
  - `Z4` : Point final de ponctuation (masque d'iris circulaire noir)
  - `Z5` : HUD de bordure (coins de cadrage, timecode, métronome)
- **Observation Technique** : Le centre de l'iris d'occlusion est calé exactement sur le barycentre du point de ponctuation `(x: 1380, y: 540)`.

---

### Bar 3 : Frames 200 à 299 (00:03:20 à 00:04:59) - Scene 02 : 3D / MOGRAPH
- **Audio Cue / Beat** : Kick à f=200, Snare à f=225, Kick à f=250, Snare à f=275. Filtre de synthétiseur ouvert.
- **Transition Entrante** : Sortie de l'iris noir vers le canevas WebGL 3D.
- **HUD dynamique** :
  - `SCENE 02 / 07` en haut à droite.
  - Désembrouillage textuel vers `3D / MOGRAPH` en bas à gauche.
  - Métronome et timecode incrémentés en continu.
- **Effets & Mouvements Clés** :
  - `f=200 - 299` : Nappe isométrique de $20 \times 20$ prismes rectangulaires arrondis (400 meshes instanciés). Chaque prisme oscille verticalement selon une fonction d'onde radiale :
    $$y_{i,j}(t) = A \cdot \sin\left(\omega t - k \sqrt{x_i^2 + z_j^2}\right)$$
  - Dégradé de couleur interpolé selon l'élévation $y$ : de violet profond (`#6C3BAA`) au niveau bas jusqu'à saumon corail (`#FF8A65`) au sommet des crêtes.
  - Au centre de la nappe, une sphère chromée spéculaire (roughness 0.05, metalness 0.95) flotte avec 2 anneaux orbitaux filaires inclinés de 35° et 65° tournant en sens inverses.
  - Caméra virtuelle Three.js en travelling d'orbite continue (pitch 45°, rotation yaw de 20° sur 100 frames).
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond 3D noir avec vignettage radial sombre
  - `Z1` : Scène Three.js (InstancedMesh de 400 cubes, sphère miroir, anneaux orbitaux)
  - `Z2` : HUD vectoriel 2D en surimpression
- **Observation Technique** : Nécessite l'usage d'un `InstancedMesh` à matrice de transformation unique pour garantir une cadence sans à-coup à 60 fps.

---

### Bar 4 : Frames 300 à 399 (00:05:00 à 00:06:39) - Scene 03 : KINETIC TYPOGRAPHY
- **Audio Cue / Beat** : 4 percussions sèches (claps/snaps) synchronisées au frame près sur les 4 temps (frames 300, 325, 350, 375).
- **Transition Entrante** : Cut direct à haute énergie sur chaque temps.
- **HUD dynamique** :
  - `SCENE 03 / 07` en haut à droite.
  - Désembrouillage textuel vers `KINETIC TYPOGRAPHY` en bas à gauche.
- **Découpage des 4 Temps (25 frames chacun)** :
  1. **Beat 1 (Frames 300 - 324)** :
     - Fond crème `#F1F1E7`.
     - Mot géant plein `EVERY` centré, noir `#060910`, lettrage majuscule ultra-bold.
     - Échelle entrant avec un amorti sec : $Scale : 0.92 \rightarrow 1.00$ en 4 frames.
  2. **Beat 2 (Frames 325 - 349)** :
     - Fond noir profond `#05080D`.
     - Mot central `SINGLE` en corail `#FA4E20` plein.
     - 4 rangées horizontales de répétition du mot `SINGLE` en contour vectoriel creux (stroke blanc 1.5px, fond transparent) défilant à l'horizontale en parallaxe (les rangées impaires vers la gauche, les paires vers la droite à $v = \pm 8\text{px/frame}$).
  3. **Beat 3 (Frames 350 - 374)** :
     - Fond bleu cobalt électrique `#314CFF`.
     - Mot blanc `FRAME` inséré dans une boîte de visée rectangulaire technique `[ FRAME ]`.
     - Mention des labels de capture : `1920 x 1080` et `60 FPS`.
     - Tranchage horizontal du mot en 5 bandes alternées avec micro-translations saccadées ($\Delta x \in [-12\text{px}, +12\text{px}]$) simulant un décalage de balayage CRT.
  4. **Beat 4 (Frames 375 - 399)** :
     - Fond corail `#FA4E20`.
     - Mot en bas-de-casse cursif noir `on purpose.` (Serif Italique).
     - Rature vectorielle dynamique : un arc de cercle noir balaie le mot de gauche à droite via une animation de tracé `stroke-dashoffset` complétée en 15 frames.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Arrière-plans chromatiques alternés (Crème $\rightarrow$ Noir $\rightarrow$ Bleu $\rightarrow$ Corail)
  - `Z1` : Éléments typographiques secondaires et bandes découpées
  - `Z2` : Mot principal du beat courant
  - `Z3` : HUD télémétrique
- **Observation Technique** : Aucun fondu ni transition intermédiaire. Chaque cut intervient précisément sur les multiples de 25 frames pour une synchronisation musicale absolue.

---

### Bar 5 : Frames 400 à 499 (00:06:40 à 00:08:19) - Scene 04 : DATA / INFOGRAPHICS
- **Audio Cue / Beat** : Bips électroniques haute fréquence, cliquetis d'odomètre numérique en roulement.
- **Transition Entrante** : Cut franc vers fond crème minéral `#F1F1E7`.
- **HUD dynamique** :
  - `SCENE 04 / 07` en haut à droite.
  - Désembrouillage textuel vers `DATA / INFOGRAPHICS` en bas à gauche.
- **Effets & Mouvements Clés** :
  - Déploiement simultané d'un tableau de bord de télémétrie à 4 quadrants :
    1. **Quadrant Supérieur Gauche (Jauge de Rétention)** : Jauge circulaire animée de $0^\circ$ à $280^\circ$ représentant `78% RETENTION`. L'arc de cercle noir épais se trace de f=400 à f=445 via `stroke-dashoffset`.
    2. **Quadrant Supérieur Droit (Compteur de Croissance)** : Odomètre à défilement rapide démarrant à `+100.0%` pour se stabiliser à `+312.4%` à la frame 460 avec un chiffre d'accentuation en corail.
    3. **Quadrant Inférieur Gauche (Barchart Mensuel)** : 12 colonnes verticales représentant les mois de Janvier à Décembre (`J` à `D`). Les 11 premières colonnes sont noires; la 12e colonne (`D`) grandit jusqu'à 100% de la hauteur et vire au corail `#FA4E20` avec un badge `PEAK`.
    4. **Quadrant Inférieur Droit (Courbe Vectorielle)** : Tracé d'une courbe spline continue bleue (`#314CFF`) traversant le quadrant de bas en haut et se terminant sur une bulle de métrique `↑ 4.7k`.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond crème `#F1F1E7`
  - `Z1` : Grille cartésienne fine grise (`rgba(0, 0, 0, 0.08)`)
  - `Z2` : Barres de données et arcs de cercle
  - `Z3` : Labels textuels monospace et valeurs numériques
  - `Z4` : Badges d'accentuation corail et bleue
  - `Z5` : HUD télémétrique
- **Observation Technique** : Toutes les interpolations numériques exploitent une fonction de lissage exponentiel pour ralentir subtilement sur les 10 dernières frames de la mesure.

---

### Bar 6 : Frames 500 à 599 (00:08:20 à 00:09:59) - Scene 05 : GENERATIVE / PARTICLES
- **Audio Cue / Beat** : Souffle de balayage granulaire stéréo + harmoniques cristallines.
- **Transition Entrante** : Cut direct vers fond noir abyssal `#05080D`.
- **HUD dynamique** :
  - `SCENE 05 / 07` en haut à droite.
  - Désembrouillage textuel vers `GENERATIVE / PARTICLES` en bas à gauche.
- **Effets & Mouvements Clés** :
  - `f=500 - 540` : Émission et brassage chaotique de 2 400 particules vectorielles sous l'action d'un champ de force de Curl Noise tridimensionnel. Les particules sont réparties en trois teintes : 70% blanc (`#FFFFFF`), 20% corail (`#FA4E20`) et 10% cyan (`#2EE9D8`).
  - `f=541 - 599` : Transition de phase par attraction gravitationnelle vers le centre. Les 2 400 particules se rangent selon la spirale de phyllotaxie à angle d'or :
    $$r_i = c \sqrt{i}, \quad \theta_i = i \times 137.508^\circ \quad (i \in [1, 2400])$$
  - Affichage de données mathématiques en surimpression : compteur incrémental `n = 2,400` et constante `φ = 137.508°`.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond noir `#05080D`
  - `Z1` : Champ de particules Canvas / WebGL (2 400 segments avec traînées directionnelles)
  - `Z2` : Réticules et constantes mathématiques vectorielles
  - `Z3` : HUD télémétrique
- **Observation Technique** : La transition du chaos vers l'ordre géométrique se fait par interpolation linéaire pondérée des coordonnées de chaque particule entre son état turbulent et sa position cible polaire.

---

### Bar 7 : Frames 600 à 699 (00:10:00 à 00:11:39) - Scene 06 : UI / PRODUCT MOTION
- **Audio Cue / Beat** : Bruit de déplacement de curseur, clic mécanique souris à la frame 632, bruit de calcul, carillon aigu de complétion à la frame 675.
- **Transition Entrante** : Fondu en 4 frames vers fond dégradé bleu cobalt `#3B5DFD`.
- **HUD dynamique** :
  - `SCENE 06 / 07` en haut à droite.
  - Désembrouillage textuel vers `UI / PRODUCT MOTION` en bas à gauche.
- **Effets & Mouvements Clés** :
  - `f=600 - 620` : Apparition au centre d'une carte modale glassmorphism (`bg: rgba(241, 241, 231, 0.95)`, blur: 20px, ombrage doux) intitulée `Render queue (900 frames)`.
  - `f=615 - 635` : Un curseur de souris vectoriel noir entre depuis le coin inférieur droit, glisse vers le toggle `Motion blur` et clique dessus à la frame 632 (passage du toggle à l'état actif orange).
  - `f=636 - 650` : Le curseur descend sur le bouton principal `Render ▶` et effectue un second clic à la frame 648.
  - `f=650 - 675` : Le bouton `Render` se transforme instantanément en une jauge de progression horizontale : le texte bascule en `Rendering... 83%` puis atteint `100%`.
  - `f=675 - 699` : Déclenchement d'un toast de confirmation éjecté sous la fenêtre avec rebond élastique :
    `✔ 900 frames rendered • 00:15.00 • 60 FPS • 0 DROPPED`.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond cobalt dégradé `#3B5DFD`
  - `Z1` : HUD télémétrique
  - `Z2` : Carte modale UI glassmorphism
  - `Z3` : Curseur de souris vectoriel
  - `Z4` : Toast de confirmation terminal
- **Observation Technique** : La trajectoire du pointeur de souris suit une courbe de Bézier quadratique naturelle ralentie à l'approche de la cible pour reproduire fidèlement l'inertie humaine.

---

### Bar 8 : Frames 700 à 799 (00:11:40 à 00:13:19) - Scene 07 : SHAPE / LIQUID
- **Audio Cue / Beat** : Effet de succion organique liquide, résonance de basse en glissando descendant, reprise percussive intense.
- **Transition Entrante** : Cut franc vers fond corail `#FA4E20`.
- **HUD dynamique** :
  - `SCENE 07 / 07` en haut à droite.
  - Désembrouillage textuel vers `SHAPE / LIQUID` en bas à gauche.
- **Effets & Mouvements Clés** :
  - `f=700 - 750` : Métaballes 2D noires liquides composées de 7 disques orbitaux en fusion et scission permanentes. Les disques se rapprochent et forment des ponts de matière fluide.
  - `f=740 - 785` : L'enveloppe extérieure de la forme fluide est prise en charge par l'équation de la Superformula 2D de Gielis. Le paramètre de symétrie $m$ s'anime continûment de `0.00` à `8.00`, faisant muter la masse liquide en un polygone régulier aux lobes symétriques parfaits.
  - Formule télémétrique affichée en monospace à gauche : `r(θ) = superformula(m=6.40, n1=1.0)`.
  - `f=785 - 799` : Effondrement gravitationnel instantané : l'étoile se rétracte en 14 frames vers son centre jusqu'à devenir un unique disque noir dense de rayon 8px.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond corail `#FA4E20`
  - `Z1` : Équation télémétrique en blanc transparent
  - `Z2` : Calque de rendu liquide noir (Filtre SVG `feColorMatrix` + Superformula)
  - `Z3` : HUD télémétrique
- **Observation Technique** : L'implémentation repose sur une combinaison de filtres SVG `feGaussianBlur` et `feColorMatrix` pour générer les ponts métaballes sans coût de calcul shader.

---

### Bar 9 : Frames 800 à 903 (00:13:20 à 00:15:03) - OUTRO : Carte de Résolution Finale
- **Audio Cue / Beat** : Dernier impact sub-bass massif à la frame 800, suivi d'une traînée de réverbération s'éteignant jusqu'à la frame 904.
- **Transition Entrante** : Cut franc vers fond noir carbone `#05080D`.
- **HUD dynamique** :
  - Réticules et bordures HUD masqués pour laisser place à la carte de titrage finale épurée.
- **Effets & Mouvements Clés** :
  - `f=800 - 820` : Le point noir issu de la scène précédente réapparaît au centre en orange-corail incandescent `#EC5230` ($x=960, y=540$).
  - `f=821 - 845` : La puce corail translate horizontalement vers la gauche ($x: 960 \rightarrow 720$) pour venir se positionner exactement comme puce d'ancrage devant le nom `Claude`.
  - `f=830 - 860` : Révélation typographique :
    - Titre principal : `Claude` (Grotesque Bold blanc) avec sous-titre cursif `motion designer` (Serif Italique).
    - Filet horizontal de démarcation vectorielle de 1px (`rgba(255, 255, 255, 0.2)`).
    - Signature cinétique en majuscules corail : `EVERY FRAME, ON PURPOSE.`
  - `f=850 - 903` : Mention programmatique terminale en bas d'écran :
    `MADE ENTIRELY IN CODE - REACT • REMOTION • THREE.JS - 0 KEYFRAMES DRAGGED`.
- **Pile de Calques (Z-Index)** :
  - `Z0` : Fond noir `#05080D`
  - `Z1` : Puce corail d'ancrage `#EC5230`
  - `Z2` : Titrage `Claude motion designer`
  - `Z3` : Filet de séparation et sous-titre `EVERY FRAME, ON PURPOSE.`
  - `Z4` : Signature technique basse
- **Observation Technique** : L'animation se fige totalement à partir de la frame 860, maintenant une stabilité visuelle complète pendant 44 frames (près d'une seconde) pour ancrer le message final dans la rétine du spectateur.
