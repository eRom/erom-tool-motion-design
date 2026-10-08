# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `aoxwGUZUcIGYGWLq.mp4` (*Claude Motion Reel*) sous l'angle du montage et de l'animation procédurale. Il formalise comment chaque impulsion acoustique (percussions, textures électroniques, balayages et silences) justifie, propulse et verrouille l'image pour un moteur de rendu de motion design.

---

## 1. Structure Rythmique & Grille Temporelle

La timeline entière est asservie à un tempo musical métronomique de **120.0 BPM** (mesuré à 120.19 BPM), ce qui produit une correspondance arithmétique exacte avec la cadence d'affichage de **30.0 fps** :

| Grandeur Temporelle | Valeur en Secondes | Équivalent en Frames (@ 30fps) | Rôle & Verrouillage Visuel |
|---|---|---|---|
| **Période d'un temps (Beat)** | `0.500 s` | **15.0 frames** | Fréquence de pas des animations cinétiques et rebonds |
| **Période d'une mesure (Bar 4/4)** | `2.000 s` | **60.0 frames** | Cadence des transitions majeures de chapitres |
| **Demi-temps (Croche / 8th note)** | `0.250 s` | **7.5 frames** | Durée typique des décélérations snap-in (Expo Out) |
| **Quart de temps (Double croche / 16th)** | `0.125 s` | **3.75 frames** | Échelon d'apparition séquentielle lettre par lettre |

### Rôle des Composants Acoustiques comme Déclencheurs (Triggers)

| Composant Audio | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse)**<br>(Temps 1 et 3 / toutes les 30 frames) | **Impacts de masse et compressions d'échelle** :<br>- Frappe au sol de la sphère rouge (F017, F032, F296)<br>- Claquage des mots en kinetic typo ("EVERY", "COUNTS")<br>- Impulsion de secousse caméra (`cameraShake: 3px -> 0px` en 4 frames) | `const kickImpulse = isKick ? Math.exp(-progress * 8) * 0.08 : 0;` |
| **Snare / Clap (Caisse Claire)**<br>(Temps 2 et 4 / toutes les 30 frames) | **Cuts de direction et ruptures de plan** :<br>- Entrée latérale à grande vitesse du mot "FRAME" (F076)<br>- Bascule de la 2D vers l'extrusion 3D (F111)<br>- Alignement coaxial du gyroscope (F211) | `const snapProgress = spring({ frame, config: { damping: 12, stiffness: 220 } });` |
| **Hi-Hats & Percussions Rapides**<br>(Doubles croches) | **Micro-vibrations télémétriques HUD** :<br>- Clignotement imperceptible de la jauge HUD<br>- Vitesse de roulis de la sphère et étirement des speed lines du tunnel | `const jitter = (frame % 4 === 0) ? (Math.random() - 0.5) * 1.5 : 0;` |
| **Textures de Synthèse & Risers** | **Accélération spatiale et expansion de FOV** :<br>- Montée en fréquence pendant la traversée du tunnel hexagonal<br>- Élargissement du champ de vision caméra de 60° à 85° | `camera.fov = 60 + Math.pow(tunnelProgress, 2) * 25;` |

---

## 2. Typologie des SFX (Sound Effects)

Le sound design combine des éléments percussifs électroniques nets, des textures analogiques chaleureuses et des bruits de matière concrète (verre, métal, céramique) reflétant l'identité matérielle de Claude.

### 2.1. Impacts & Sub-Drops (Masse & Gravité)
- **Rôle** : Matérialiser le poids physique de la sphère et la force d'inertie des blocs typographiques.
- **Occurrences clés** :
  - `00:16 (F017)` : **Sub-drop sourd d'ouverture** : la sphère percute le sol noir. La sous-fréquence (45 Hz - 60 Hz) accompagne l'onde de choc circulaire visible au sol.
  - `00:32 (F032)` : **Impact mat de rebond sur le mot "CLAUDE"** : son percutant couplé à une résonance brève de matériau solide.
  - `09:26 (F296)` : **Impact tactile sur lit de picots** : bruit mat de percussion amortie quand la sphère retombe sur les pavés voxels.

### 2.2. Whooshes & Swishes (Vélocité & Traversée)
- **Rôle** : Donner du réalisme physique aux mouvements de caméra brusques et aux translations rapides.
- **Occurrences clés** :
  - `00:56 - 00:59 (F056-F059)` : **Whoosh d'occlusion de lentille** : souffle rapide montant en volume alors que la sphère fonce vers l'objectif et recouvre l'écran.
  - `02:16 (F076)` : **Whip-swish horizontal** : le mot "FRAME" fend l'air depuis la droite avec un balayage stéréo marqué.
  - `04:13 (F133)` : **Zoom-whoosh d'aspiration** : le bloc "EVERY FRAME COUNTS" est aspiré dans la caméra avant l'extinction.
  - `07:16 - 08:27 (F226-F267)` : **Warp rush continu** : texture continue de souffle d'air et de résonance tubulaire simulant la traversée du conduit hexagonal.

### 2.3. Risers & Pitch-Bends (Tension & Accélération)
- **Rôle** : Préparer les ruptures de chapitres et dramatiser les accélérations géométriques.
- **Occurrences clés** :
  - `07:01 - 07:15 (F211-F225)` : Riser harmonique montant progressivement en fréquence pendant l'alignement des trois anneaux du gyroscope, culminant sur l'entrée dans le tunnel à F226.
  - `08:20 - 08:28 (F260-F268)` : Accélération du filtre résonant ouvrant les hautes fréquences jusqu'au flash lumineux blanc à la frame 268.

### 2.4. Foley Tactile & Mécanique (Matérialité)
- **Rôle** : Ancrer la typographie dans un atelier d'usinage ou de typographie de plomb.
- **Occurrences clés** :
  - `12:03 (F363)` : **Son de rotation fluide** : cliquetis doux et feutré d'un gyroscope ou d'un engrenage horloger pendant la rotation sur 360° de l'astérisque.
  - `12:21 - 13:00 (F381-F405)` : **Slam mécanique lettre par lettre** : chaque lettre de "CLAUDE" (C, L, A, U, D, E) produit un clic sourd de stèle qui se dresse ou de touche mécanique pondérée.
  - `13:21 (F411)` : **Roulis de bille de céramique** : frottement très doux de la sphère qui roule sur le fond papier texturé avant de s'arrêter net comme un point de ponctuation.

---

## 3. Gestion du Vide & Silences (Hang Time)

L'efficacité du motion design repose sur la maîtrise des micro-ruptures acoustiques qui précèdent les chocs visuels :

1. **Le Vide Pré-Impact (Frames 001 - 016 / 0.50 s)** :  
   Absence totale de percussions ou d'attaque. Uniquement un silence pesant et un léger bourdonnement sous-jacent. L'impact de la sphère à F017 tire 100% de son punch dramatique de ce vide préalable.
2. **La Rupture de 2 Frames avant le Gyroscope (Frames 133 - 135 / 0.10 s)** :  
   Après l'agression typographique de "EVERY FRAME COUNTS", la piste coupe brutalement toute résonance. Le noir d'écran total coïncide avec un trou d'air acoustique complet, rendant l'apparition du gyroscope à F136 captivante et chirurgicale.
3. **La Respiration au Sortir du Tunnel (Frames 268 - 270 / 0.07 s)** :  
   Au moment où la caméra franchit le seuil du flash blanc/crème, le bruit de vent du tunnel s'arrête net. La transition vers la Section 05 `05 SYSTEMS` se fait dans un paysage sonore plus apaisé, dominé par des textures douces et organiques.

---

## 4. Tableau Synoptique Audio -> Image

| Frame Cible | Temps (s) | Déclencheur Acoustique (Audio Cue) | Action Visuelle Déclenchée | Paramètre Moteur / Trigger Code |
|---|---|---|---|---|
| **F 001** | `00:00` | Silence / Low rumble | Affichage de l'horizon sombre et des repères HUD | `opacity: interpolate(frame, [0, 6], [0, 1])` |
| **F 017** | `00.56` | **Impact 1 (Onset fort)** | Chute et contact de la sphère rouge au sol | `triggerWave(x=0, z=0, radius=54); squash(0.82);` |
| **F 022** | `00.73` | Rebond ascendant | Émergence verticale des lettres "CLAUDE" | `translateY: spring({ mass: 1, stiffness: 200 })` |
| **F 032** | `01.07` | **Kick 01 (Temps fort 120 BPM)** | Sphère heurtant le sommet du "U" | `applyBounce({ obstacle: 'U', velocityY: -4.5 })` |
| **F 056** | `01.87` | Whoosh d'accélération | Sphère fonçant vers la lentille caméra | `scale: Math.exp((frame - 50) * 0.4)` |
| **F 061** | `02.03` | **Kick 03 (Temps fort S02)** | Bascule au rouge uni + mot "EVERY" plein cadre | `setSection('02 KINETIC TYPE'); renderText('EVERY');` |
| **F 076** | `02.53` | **Snare 01 (Attaque caisse claire)** | Snap horizontal du mot "FRAME" | `translateX: interpolate(frame, [76, 82], [800, 0], easeExpo)` |
| **F 090** | `03.00` | **Kick 05** | Montée verticale du mot "COUNTS" | `translateY: interpolate(frame, [90, 96], [300, 0], easeExpo)` |
| **F 111** | `03.70` | Percussion de tension | Extrusion volumétrique 3D du bloc de mots | `extrudeDepth: spring({ stiffness: 180, damping: 14 })` |
| **F 133** | `04.43` | Zoom-whoosh + Coupure son | Bloc plongeant dans l'objectif -> Écran noir | `zoom: interpolate(frame, [132, 134], [1, 8]); blackout();` |
| **F 137** | `04.57` | **Kick 08 (Reprise groove)** | Éveil du gyroscope 3D au centre du noir | `setSection('03 FORM'); startGimbal();` |
| **F 211** | `07.03` | Climax du riser | Alignement coaxial des trois tores du gyroscope | `easeEulerAnglesToZero(); openHexPortal();` |
| **F 226** | `07.53` | **Kick 14 (Début Warp)** | Entrée dans le tunnel hexagonal infini | `setSection('04 VELOCITY'); startTunnelWarp();` |
| **F 268** | `08.93` | Flash d'impact transitoire | Flash blanc optique et bascule au fond crème | `triggerWhiteFlash(); invertHUDToDark();` |
| **F 272** | `09.07` | **Kick 17 (Groove feutré)** | Révélation de la grille voxel isométrique | `setSection('05 SYSTEMS'); renderVoxelGrid();` |
| **F 296** | `09.87` | Impact feutré | Premier rebond de la sphère sur les voxels | `emitVoxelRipple(center, amplitude=45);` |
| **F 331** | `11.03` | Climax mélodique | Cubes s'élevant pour former l'astérisque | `morphToAsteriskPattern(); cameraPitchTo90();` |
| **F 362** | `12.07` | **Kick 23 (Onset S06)** | Astérisque lisse détaché + rotation 360° | `setSection('06 SIGN-OFF'); spin360(asterisk);` |
| **F 381** | `12.70` | Percussions staccato | Lettres "CLAUDE" s'érigeant une par une | `letters.forEach((l, i) => erectLetter(l, delay=i*4));` |
| **F 411** | `13.70` | Bruitage de roulement | Sphère rouge entrant pour faire le point final | `rollInPeriodDot(targetX=1710, targetY=570);` |
| **F 435** | `14.50` | Maintien et extinction | Stabilisation finale à 100%, hold jusqu'à F450 | `freezeAllState(); completeProgressBar();` |
