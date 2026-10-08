# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `gLl6GZWastLVE2fr.mp4` (*Claude Motion Reel 2026*) sous l'angle exclusif du montage cinématique et de l'asservissement visuel. Il détaille comment le sound design minimaliste, précis et ultra-percussif pilote la génération de chaque frame du code.

---

## 1. Structure Rythmique & Synchronisation Image

La bande sonore est un morceau IDM / Minimal Bass percutant cadencé à **128.0 BPM exact**. Chaque mesure musicale de 4 temps constitue un bloc thématique autonome de 112.5 frames (1.875 seconde).

| Élément Percussif | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse Sub)**<br>(Temps 1 de chaque mesure) | **Cuts de mesure majeurs et impacts de masse** :<br>- Déclencheurs des changements d'univers visuel (noir -> rouge -> noir -> crème -> bleu -> jaune -> noir -> crème)<br>- Impulsion de scale caméra et de l'atome corail central (`scale: 1.15 -> 1.0` en 6 frames)<br>- Initialisation des cycles du métronome HUD (`BEAT ■□□□`) | `const kickImpulse = 1 + 0.15 * Math.exp(-progress * 5);` |
| **Snare / Rimshot Aigu**<br>(Temps 2 et 4) | **Scissions géométriques et transitions de matière** :<br>- Division cellulaire de l'atome (Bar 1, Beat 2)<br>- Explosion cinétique plein écran sur le mot "EVERY" (Bar 2, Beat 2)<br>- Éclatement de la rosace en grille cartésienne (Bar 4, Beat 2)<br>- **Match cut terminal** : ancrage du point rouge sur le logo `Claude.` (Bar 8, Beat 2) | `const isSnapFrame = (frame % framesPerBeat) < 2;` |
| **Hi-Hats & Shuffles (16th notes)**<br>(Croches et doubles-croches) | **Télémétrie et micro-rotations continues** :<br>- Défilement des compteurs de frame `FRAME XXXX / 0900`<br>- Pas angulaires de la boîte filaire `ROT 090.0°` (Bar 3)<br>- Vitesse orbitale des anneaux de texte (Bar 7) | `const rotationAngle = (frame * speed) % 360;` |
| **Sub-Bass Drone (35 - 55 Hz)** | **Profondeur spatiale et volume 3D** :<br>- Soutien continu des séquences immersives 3D (Bar 5 champ de particules, Bar 6 ruban) | Modulation de l'amplitude Z des particules en WebGL. |

---

## 2. Typologie des SFX (Sound Effects Métier)

Le paysage sonore évite le bruitisme orchestral pour privilégier des textures électroniques ultra-courtes, nettes et chirurgicales, parfaitement calibrées pour le motion design graphique.

### 2.1. Whooshes (Balayages Stéréo & Inertie)
- **Usage** : Souligner les trajectoires vectorielles à haute vélocité et les déploiements de bandes de texte.
- **Occurrences clés** :
  - `00:09.38 - 00:10.32` (Bar 6) : **Whip-whoosh stéréo dynamique** accompagnant l'accélération du ruban tubulaire sur sa spline de Bézier à travers l'écran jaune.
  - `00:11.26 - 00:11.72` (Bar 7) : Whoosh horizontal court calé sur le jaillissement du bandeau ticker initial vers la gauche.
- **Règle de montage** : Le front montant du whoosh commence 3 frames en amont de l'accélération pour donner une sensation physique d'aspiration d'air.

### 2.2. Risers & Pitch-Sweeps (Tension & Accélération)
- **Usage** : Construire l'élan cinétique avant les déflagrations graphiques.
- **Occurrences clés** :
  - `00:02.82` (Bar 2, Beat 3) : Balayage de fréquence montant très court (FM sweep) menant au verrouillage de la boîte de visée `[FRAME]`.
  - `00:12.65` (Bar 7, Beat 4) : Riser d'harmoniques montantes accélérant la rotation orbitale des 4 anneaux de texte concentriques juste avant l'expansion en iris blanc/crème.

### 2.3. Impacts & Sub-Drops (Ancrage & Masse)
- **Usage** : Sceller une transition ou donner un poids physique irréversible à un élément graphique.
- **Occurrences clés** :
  - `00:02.35` (Bar 2, Beat 2) : **Drop d'impact plein écran** : le snare saturé s'accompagne d'une onde sub-bass lorsque l'écran entier vire au rouge corail `#EB4432` avec le mot "EVERY".
  - `00:10.32` (Bar 6, Beat 3) : **Snap métallique aigu** au moment exact où le ruban boucle sur lui-même et projette l'éclat d'épines noires (spikes).
  - `00:13.60` (Bar 8, Beat 2) : **Impact sec de clôture** : le plus fort pic acoustique du film (`Peak = 0.838`), un rimshot mat et autoritaire au moment où l'atome corail se fige pour devenir le point terminal du logotype `Claude.`.

### 2.4. Glitches & Bleeps Télémétriques (HUD & Code)
- **Usage** : Renforcer l'identité "généré par le code" en matérialisant chaque calcul d'interpolation.
- **Occurrences clés** :
  - `00:00.00 - 00:01.87` (Bar 1) : Bips de métronome d'une netteté clinique sur chaque quart de mesure, synchronisés sur l'affichage `BEAT ■□□□`.
  - `00:03.76 - 00:05.62` (Bar 3) : Chirps FM discrets et harmoniques modulées lors du passage de l'angle à `090.0°` et du morphing en triangle/fleur.
  - `00:07.51 - 00:09.37` (Bar 5) : Carillon de fréquences cristallines aiguës (8 à 12 kHz) flottant au-dessus de la basse modulaire pour traduire la dispersion du nuage de points 3D.

### 2.5. Foley Matériel & Mécanique (Tactile)
- **Usage** : Humaniser la rigueur numérique par des micro-bruitages physiques.
- **Occurrences clés** :
  - `00:05.63` (Bar 4, Beat 1) : Léger froissement / souffle de texture papier à l'ouverture du fond crème `#F4EFE6`.
  - `00:06.10` (Bar 4, Beat 2) : Bruitage de dispersion de billes ou de particules légères quand la rosace de Fibonacci éclate en grille de points.
  - `00:14.53 - 00:15.00` (Bar 8, Beat 4) : **Dactylographie mécanique fine** : cliquetis d'écriture rapide accompagnant le déroulé du texte technique `900 FRAMES • 60 FPS • 128 BPM • WRITTEN ENTIRELY IN CODE`.

---

## 3. Gestion du Vide, Silences & Suspension (Hang Time)

La puissance rythmique du film repose sur un contraste dynamique extrême entre les sections :

```
Énergie RMS par Mesure (44.1 kHz) :
Bar 1 (Intro minimale) : 0.0550  ■
Bar 2 (Explosion Typo) : 0.2581  ■■■■■ (x4.7 d'énergie !)
Bar 3 (Morphing)       : 0.2253  ■■■■
Bar 4 (Phyllotaxie)    : 0.2356  ■■■■
Bar 5 (Nuage 3D)       : 0.2235  ■■■■
Bar 6 (Ruban)          : 0.2395  ■■■■
Bar 7 (Anneaux Ticker) : 0.1991  ■■■
Bar 8 (Logo & Fin)     : 0.1759  ■■■
```

### 3.1. Le Vide d'Amorce (Frames 0 à 27, `00:00.00 - 00:00.46`)
- **Mécanisme** : Niveau sonore quasi nul (`RMS = 0.000`), seuls les repères graphiques s'arment en silence.
- **Rôle** : Créer l'attente télémétrique avant que le premier point corail n'apparaisse sur le Beat 2.

### 3.2. Le Saut de Dynamique Bar 1 -> Bar 2 (`00:01.87`)
- **Mécanisme** : Passage instantané sans transition d'un univers feutré (`RMS = 0.055`) au déluge sonore complet (`RMS = 0.258`).
- **Effet visuel** : L'impact sur la rétine est décuplé par la surprise acoustique. La musique "explose" au moment exact où la typographie sature l'espace.

### 3.3. La Suspension Pré-Logo (Frame 815, `00:13.58`)
- **Mécanisme** : Léger creux transitoire d'une fraction de seconde avant le Beat 2 de la Bar 8.
- **Effet visuel** : L'iris crème finit de s'ouvrir dans un souffle feutré, créant la suspension indispensable qui prépare le coup de rimshot sec figeant le logo `Claude.`.

---

## 4. Tableau Synoptique Audio -> Image (Beat-par-Beat)

| Mesure / Beat | Timestamp (Frames @ 60fps) | Événement Sonore Dominant | Action Graphique Asservie | Paramètre Code Déclenché |
|---|---|---|---|---|
| **Bar 1, Beat 1** | `00:00.00` (f 00) | Thud sourd + silence ambiant | Réticule central `+` qui s'arme | Opacité HUD `0 -> 1` |
| **Bar 1, Beat 2** | `00:00.47` (f 28) | Woodblock percussif net | **Apparition de l'atome corail** | `scale: 1.3 -> 1.0` en 6 frames |
| **Bar 1, Beat 3** | `00:00.93` (f 56) | Clic stéréo net | Scission cellulaire en 2 points à 45° | Calcul rayon polaire `r=48px` |
| **Bar 1, Beat 4** | `00:01.40` (f 84) | Double chirp numérique | Déploiement orbital en 4 puis 8 points | Rotation angulaire linéaire |
| **Bar 2, Beat 1** | `00:01.88` (f 113) | Kick lourd d'attaque | Anneau télescopique + masque "E" | Déclenchement masque SVG |
| **Bar 2, Beat 2** | `00:02.35` (f 141) | **Snare drop massif + sub** | **Fond rouge plein + typo "EVERY"** | Inversion chromatique globale |
| **Bar 2, Beat 3** | `00:02.82` (f 169) | FM pitch sweep court | Cadre de visée `[FRAME]` + glitch RGB | Décalage RGB 6px sur 5 frames |
| **Bar 2, Beat 4** | `00:03.28` (f 197) | Snare syncopé | Ombre portée dure 3D à 45° | Drop-shadow nette `offset: 12px` |
| **Bar 3, Beat 1** | `00:03.76` (f 226) | Cut kick franc | Retour fond noir + boîte filaire active | Reset position et label `ROT 003.5°` |
| **Bar 3, Beat 2** | `00:04.22` (f 253) | Snare régulier | Onde de choc circulaire concentrique | Propagation rayon d'onde `0 -> 400px` |
| **Bar 3, Beat 3** | `00:04.68` (f 281) | Kick + chirp FM | Morphing en carré cobalt + ghosting | Interpolation p-norme + rotation 90° |
| **Bar 3, Beat 4** | `00:05.15` (f 309) | Snare de relance | Morphing en fleur ambre à 4 lobes | Formule 4 lobes + rotation 240° |
| **Bar 4, Beat 1** | `00:05.63` (f 338) | Rimshot sec + souffle papier | **Cut sur papier crème + rosace d'or** | Tracé points angle d'or $137.5^\circ$ |
| **Bar 4, Beat 2** | `00:06.10` (f 366) | Snare blast + scatter foley | Éclatement des points en grille cartésienne | Morphing radial `delayFactor` |
| **Bar 4, Beat 3** | `00:06.57` (f 394) | Kick percutant | Balayage d'onde colonne rouge corail | Écart $dx$ et élévation $dy$ |
| **Bar 4, Beat 4** | `00:07.03` (f 422) | Snare de transition | Onde sinusoïdale continue bidimensionnelle | Champ d'ondes mathématique |
| **Bar 5, Beat 1** | `00:07.51` (f 451) | Sub drone lourd + carillon aigu | **Cut vers bleu cobalt + terrain 3D** | Initialisation mesh Three.js |
| **Bar 5, Beat 2** | `00:07.97` (f 478) | Snare + arpège de synthé | Repliement en sphère de Fibonacci | Morphing positions $P_1 \to P_2$ |
| **Bar 5, Beat 3** | `00:08.43` (f 506) | Kick sub | Évidement et aplatissement en tore 3D | Morphing positions $P_2 \to P_3$ |
| **Bar 5, Beat 4** | `00:08.90` (f 534) | Snare de transition | Cristallisation sur les 12 arêtes du cube | Morphing positions $P_3 \to P_4$ |
| **Bar 6, Beat 1** | `00:09.38` (f 563) | Kick d'impact + ouverture filtre | **Cut jaune vif + jaillissement ruban** | Tracé spline Bézier multicouche |
| **Bar 6, Beat 2** | `00:09.85` (f 591) | Whoosh stéréo violent | Accélération en courbe S avec motion blur | `strokeDashoffset` rapide |
| **Bar 6, Beat 3** | `00:10.32` (f 619) | **Snap métallique perçant** | **Boucle sur soi-même + éclat d'épines** | Burst radial de pointes triangulaires |
| **Bar 6, Beat 4** | `00:10.78` (f 647) | Snare de relance | Éjection balistique hors du cadre droit | Vélocité terminale > 2500 px/s |
| **Bar 7, Beat 1** | `00:11.26` (f 676) | Cut kick sec | Cut noir carbone + bandeau ticker gauche | Défilement texte 8px/frame |
| **Bar 7, Beat 2** | `00:11.72` (f 703) | Snare syncopé | Déploiement en 4 tickers alternés | 4 pistes horizontales inversées |
| **Bar 7, Beat 3** | `00:12.18` (f 731) | Kick d'impulsion | **Enroulement polaire en 4 anneaux** | Transformation cartésien $\to$ polaire |
| **Bar 7, Beat 4** | `00:12.65` (f 759) | Riser harmonique accéléré | Accélération orbitale x3 + pulsation atome | Multiplicateur de vitesse angulaire |
| **Bar 8, Beat 1** | `00:13.13` (f 788) | Sub-bass dive feutré | Expansion en iris crème plein écran | Rayon masque circulaire $0 \to 1200\text{px}$ |
| **Bar 8, Beat 2** | `00:13.60` (f 816) | **Rimshot mat sec (Pic max 0.838)** | **Match cut du point sur `Claude.`** | Verrouillage position baseline |
| **Bar 8, Beat 3** | `00:14.07` (f 844) | Kick doux de conclusion | Apparition du sous-titre `MOTION DESIGNER` | Fade-in opacité monospace |
| **Bar 8, Beat 4** | `00:14.53` (f 872) | Dactylographie mécanique rapide | Déroulé du crédit technique d'ingénierie | Caractères par pas de 2 frames |
| **Fin (f 900)** | `00:15.00` (f 900) | Extinction réverbérée naturelle | Arrêt sur image parfait | Figeage total des compteurs |
