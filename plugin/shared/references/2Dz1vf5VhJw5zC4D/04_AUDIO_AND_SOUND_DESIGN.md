# 04. Sound Design & Synchronisation Audio-Visuelle

Ce document analyse la bande sonore de la vidéo `2Dz1vf5VhJw5zC4D.mp4` sous l'angle du monteur et de l'ingénieur de motion design. Il explicite la manière dont les événements acoustiques (percussions, risers, bruitages foley et silences) dirigent avec une précision mathématique la cinématique visuelle.

---

## 1. Métriques Acoustiques & Grille Rythmique

L'ensemble de la composition musicale et du mixage sonore est asservi à un tempo rigide et métronomique :

- **Tempo Nominal** : **144.0 BPM** (détecté à 72.0 BPM en demi-mesure).
- **Signature Temporelle** : **4/4** (4 temps par mesure).
- **Durée d'un Temps (Beat)** :
  $$T_{\text{beat}} = \frac{60}{144} = 0.41667 \text{ s} \quad \Longleftrightarrow \quad \mathbf{25\text{ frames exactes à 60 fps}}$$
- **Durée d'une Mesure (Bar)** :
  $$T_{\text{bar}} = 4 \times T_{\text{beat}} = 1.66667 \text{ s} \quad \Longleftrightarrow \quad \mathbf{100\text{ frames exactes à 60 fps}}$$
- **Durée Totale Active** : 9 mesures de 100 frames = 900 frames d'animation + 4 frames de traînée de réverbération finale (904 frames / 15.061 secondes).

### Structure Percussive Électronique par Mesure

Chaque mesure de 100 frames suit une distribution récurrente de frappes de batterie :
- **Temps 1 (Frame 00 de la mesure)** : Kick d'attaque sub-bass (45-60 Hz) à forte vélocité.
- **Temps 2 (Frame 25 de la mesure)** : Snare percutant ou Clap sec (bande 1.2 kHz - 3.5 kHz).
- **Temps 3 (Frame 50 de la mesure)** : Kick de relance médium.
- **Temps 4 (Frame 75 de la mesure)** : Snare de transition avec réverbération courte ou ghost note.
- **Hi-hats / Ride** : Motifs continus en doubles-croches (toutes les 6.25 frames virtuelles, soit alternativement 6 et 7 frames).

---

## 2. Typologie des Effets Sonores (SFX Catalog)

Le design sonore combine six familles d'effets spécialisés :

### 2.1. Sub-Drops & Impacts Basse Fréquence
- **Spectre** : Sinusoïde pure de 60 Hz descendant vers 35 Hz avec compression agressive.
- **Rôle** : Ancrer physiquement les cuts majeurs de transition de scène (Frames 100, 300, 700 et 800).
- **Comportement visuel lié** : Secousse caméra instantanée de 1 frame ou cut optique franc à opacité 100%.

### 2.2. Risers & Balayages Ascendants (Tension Builders)
- **Spectre** : Bruit blanc filtré par passe-bande résonant balayant de 200 Hz à 12 kHz sur 15 frames.
- **Rôle** : Annoncer l'arrivée imminente d'une rupture rythmique (notamment Frames 85-99 avant le titre, et Frames 485-499 avant les particules).
- **Comportement visuel lié** : Élargissement vertical de la fente lumineuse, accélération de la vélocité.

### 2.3. Bleeps Télémétriques & Glitch Numérique (UI Sounds)
- **Spectre** : Ondes carrées et FM courtes (1.5 kHz à 4 kHz), durées d'impulsion de 15 ms à 30 ms.
- **Rôle** : Accompagner le désembrouillage typographique (Text Scramble) du cartouche HUD en bas à gauche de chaque scène, ainsi que le compteur de données de la scène 04.
- **Comportement visuel lié** : Remplacement pseudo-aléatoire des glyphes de texte à chaque frame.

### 2.4. Foley Matériel & Mécanique de Bureau
- **Spectre** : Transitoire haute définition d'un commutateur de souris mécanique (micro-switch Omron, clic à 2.8 kHz).
- **Rôle** : Conférer une réalité physique aux micro-interactions de la scène 06 (Frame 632 : activation du toggle ; Frame 648 : clic du bouton Render).
- **Comportement visuel lié** : Enfoncement de bouton de 2px, bascule colorimétrique du switch.

### 2.5. Chime Harmonique & Carillon de Succès
- **Spectre** : Double tonalité sinusoïdale pure (accords majeurs à 1046 Hz et 1318 Hz) avec decay de 350 ms.
- **Rôle** : Célébrer l'achèvement du rendu vidéo à la Frame 675.
- **Comportement visuel lié** : Éjection du toast de validation sous la fenêtre modale.

### 2.6. Textures Organiques Visqueuses (Liquid Foley)
- **Spectre** : Bruitage de succion liquide et de cavitation sous vide (filtre passe-bas à résonance liquide).
- **Rôle** : Matérialiser l'adhérence et la rupture des ponts de matière entre les métaballes dans la scène 07 (Frames 710-760).
- **Comportement visuel lié** : Déformation de la membrane SVG `feColorMatrix`.

---

## 3. Gestion du Vide, Silences & Suspensions (Hang Time)

L'impact dynamique de la vidéo repose sur des ruptures acoustiques calculées :

1. **La Suspension d'Iris (Frames 185 à 199)** :
   - Alors que la mesure 2 atteint son apogée, le point final de `CLAUDE.` commence son expansion en iris noir géant.
   - À la frame 188, la batterie s'interrompt brutalement. Seul un whoosh d'aspiration étouffé subsiste pendant 12 frames.
   - Ce micro-silence crée un appel d'air dramatique qui décuple l'effet de surprise lors de l'apparition de l'univers 3D à la frame 200.

2. **Le Décrochage Staccato (Frames 300 à 399)** :
   - Suppression complète de la ligne de basse continue sur toute la mesure 4.
   - Réduction de l'accompagnement à quatre coups de percussions isolés espacés de 25 frames, forçant l'œil à focaliser toute son attention sur le rythme binaire des 4 mots (`EVERY`, `SINGLE`, `FRAME`, `on purpose.`).

3. **L'Extinction Post-Drop Finale (Frames 804 à 904)** :
   - Après l'impact massif de la frame 800, toutes les percussions sont définitivement coupées.
   - La traînée de réverbération décroît linéairement pendant 100 frames sans aucune nouvelle pulsation rythmique.
   - Cette immobilité acoustique garantit la lisibilité et l'autorité de la carte de titrage finale.

---

## 4. Tableau Synoptique de Synchronisation Audio -> Image

| Frame(s) | Mesure / Temps | Événement Sonore (Audio Cue) | Action Visuelle Déclenchée | Trigger de Code & Paramètre |
|---|---|---|---|---|
| **0** | Bar 1 / Beat 1 | Hum sub-bass (45 Hz) + Bip d'initialisation | Allumage des réticules de visée Viewfinder | `opacity: 0 -> 1` sur 15 frames |
| **85 - 99** | Bar 1 / Beat 4.4 | Riser ascendant en bruit blanc filtré | Élargissement de l'onde sinusoïdale en bande lumineuse | `scaleY: 1 -> 80` sur f=85..99 |
| **100** | Bar 2 / Beat 1 | **Kick 1 + Snare lourd + Sub-drop** | Cut vers fond corail `#FA4E20` + Début split reveal `CLAUDE.` | `cut: Scene 01`, split reveal `offsetY: 40 -> 0` |
| **100 - 118** | Bar 2 / Beat 1-2 | Train de bleeps UI haute fréquence | Désembrouillage textuel du label `IDENTITY / TYPE` | `scrambleProgress: 0 -> 1` sur 18 frames |
| **185 - 199** | Bar 2 / Beat 4.4 | Coupure batterie + Whoosh d'aspiration | Le point final s'étend en disque noir avalant l'écran | Iris scale `1 -> 150`, occlusion totale à f=199 |
| **200** | Bar 3 / Beat 1 | Reprise du groove synthétique + Kick lourd | Ouverture de la scène 3D de 400 cubes et sphère chromée | Rendu Three.js `WaveGrid3D`, pitch caméra 45° |
| **300** | Bar 4 / Beat 1 | Snap percussif sec #1 | Cut vers fond crème, mot `EVERY` en snap d'échelle | `beatIndex = 0`, scale `0.92 -> 1.0` |
| **325** | Bar 4 / Beat 2 | Snap percussif sec #2 | Cut vers fond noir, mot `SINGLE` + défilement filaire | `beatIndex = 1`, translation $v = \pm 12\text{px/f}$ |
| **350** | Bar 4 / Beat 3 | Snap percussif sec #3 | Cut vers fond bleu, mot `FRAME` découpé en 5 bandes | `beatIndex = 2`, slices offset $\pm 14\text{px}$ |
| **375** | Bar 4 / Beat 4 | Snap percussif sec #4 | Cut vers fond corail, mot `on purpose.` + rature vectorielle | `beatIndex = 3`, `strokeDashoffset: 800 -> 0` |
| **400** | Bar 5 / Beat 1 | Kick lourd + Cliquetis continu d'odomètre | Cut vers fond crème, déploiement du tableau 4 quadrants | Compteur `interpolate(f, [0, 60], [100, 312])` |
| **500** | Bar 6 / Beat 1 | Souffle stéréo granulaire + Bruit blanc | Cut vers fond noir, dispersion de 2 400 particules | Champ Curl Noise initial, dispersion 3D |
| **540** | Bar 6 / Beat 2.6 | Harmonique cristalline ascendante | Convergence des particules vers la spirale de phyllotaxie | Morphing vers $r = c\sqrt{i}$, $\theta = i \cdot 137.508^\circ$ |
| **600** | Bar 7 / Beat 1 | Basse feutrée + Entrée du curseur | Fondu vers bleu cobalt, apparition modale Render Queue | Spring pop-in modale `{ stiffness: 220, damping: 18 }` |
| **632** | Bar 7 / Beat 2.3 | **Clic mécanique de souris #1** | Bascule du toggle `Motion blur` à l'état actif | `motionBlurActive: false -> true` |
| **648** | Bar 7 / Beat 2.9 | **Clic mécanique de souris #2** | Clic sur le bouton `Render ▶`, début de la barre de progression | Mute bouton en barre de progression |
| **675** | Bar 7 / Beat 4 | **Carillon harmonique (Chime de succès)** | Fin de la jauge (100%), éjection vers le bas du toast validé | Toast `translateY: 0 -> 48px` avec rebond |
| **700** | Bar 8 / Beat 1 | Succion organique fluide + Sub-drop | Cut vers fond corail, métaballes liquides noires en fusion | Filtre SVG `feColorMatrix` activé |
| **740** | Bar 8 / Beat 2.6 | Glissando de basse montant | Morphing de la Superformula de Gielis vers polygone régulier | Paramètre $m : 0.00 \rightarrow 8.00$ |
| **785** | Bar 8 / Beat 4.4 | Whoosh d'effondrement rapide | Rétraction de la forme liquide en un unique point noir | Scale polygone `220 -> 8` en 14 frames |
| **800** | Bar 9 / Beat 1 | **Kick final ultra-lourd (Sub 35 Hz)** | Cut vers fond noir, translation de la puce corail | Début séquence Outro, puce $x: 960 \rightarrow 720$ |
| **860 - 903** | Bar 9 / Beat 3.4 | Traînée de réverbération en fade-out pur | Fixité absolue de la carte de signature finale | Gel complet du moteur d'animation jusqu'à l'extinction |
