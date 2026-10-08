# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de la vidéo de référence `Ug6RUqJ59vKTsnPX.mp4` (*CLAUDE / MOTION REEL - 2026*) sous l'angle du monteur et de l'ingénieur motion design. Il explicite comment chaque composant acoustique (pulsation métronomique, foley mécanique, textures numériques et silences calculés) propulse et verrouille l'image à la frame près pour un agent de fabrication logicielle.

---

## 1. Structure Rythmique & Asservissement Percussif

L'intégralité de la composition (15.061s, 904 frames à 60.0 fps) est gouvernée par une signature rythmique 4/4 à **128.0 BPM** exact (tempo techno/électro clinique), articulée en **8 mesures musicales complètes** de 112.5 frames (1.875s) :

| Élément de Percussion | Rôle Moteur sur l'Animation | Déclencheur / Formule de Code |
|---|---|---|
| **Kick (Grosse Caisse Lourde)**<br>(Temps 1 et 3 en beat standard) | **Impacts de Masse & Ruptures de Plan** :<br>- Cut plein écran vers fond rouge "CLAUDE" (Frame 113)<br>- Entrée dans la grille d'easing (Frame 226)<br>- Cut vers le fond cobalt du morphing (Frame 338)<br>- Bascule vers le pavage de Truchet (Frame 451)<br>- Rafale cinétique "LINEAR." (Frame 732)<br>- Éruption d'iris bloom final (Frame 788) | `const isKick = frame % (framesPerBeat * 2) === 0;`<br>`const kickImpact = Math.exp(-decayProgress * 12);` |
| **Snare / Clap Électronique**<br>(Temps 2 et 4) | **Modulations Internes & Transitions de Forme** :<br>- Éclosion de l'astérisque 12 rayons (Frame 28)<br>- Élargissement élastique du "C" de "CLAUDE" (Frame 141)<br>- Lancement des billes d'easing (Frame 254)<br>- Métamorphose Circle $\to$ Triangle (Frame 366)<br>- Déclenchement de la Vague 1 de Truchet (Frame 479)<br>- Flash vers le mot "NEVER" (Frame 704) | `const isSnare = (frame - framesPerBeat) % (framesPerBeat * 2) === 0;` |
| **Hi-Hats & Double-Croches (1/16)**<br>(Pulsation continue à haute cadence) | **Télémétrie HUD, Spacing Ticks & Rotations** :<br>- Incrémentation du running timecode à 60 fps<br>- Impression des ticks de spacing stroboscopique sur les rails (Scène 02)<br>- Vitesse angulaire de révolution du tore et de la sphère 3D ($\omega = 2.4^\circ/\text{frame}$)<br>- Cadence de la matrice de temps `■□□□` dans le HUD | `const tickVisible = frame % 4 === 0;` |
| **Basse Électro-Glitch & Sub-Drone**<br>(Filtre coupe-bas modulé) | **Ondes de Déformation & Trajectoires Continues** :<br>- Ondulation concentrique de l'astérisque central<br>- Front de balayage de Truchet ($v = 48px/\text{frame}$)<br>- Champ de gravité et friction des 40 particules de confettis | `const subWave = Math.sin((frame / 28.125) * Math.PI);` |

---

## 2. Profil Énergétique & Courbe Dynamique RMS

L'analyse spectrale et volumétrique par mesure (RMS mesuré sur signal stéréo 44.1 kHz) révèle une dramaturgie sonore en 4 actes parfaitement architecturée :

```
Niveau RMS
  0.25 |              [B2]   [B3]   [B4]   [B5]                 [B7]
       |             ────── ────── ────── ──────               ──────
  0.20 |                                                      
       |                                                               [B8]
  0.15 |                                                              ──────
       |       [B1]                                     [B6]
  0.10 |      ──────                                   ──────
       |
  0.00 └─────────────────────────────────────────────────────────────
         Mesure 1   Mesure 2 Mesure 3 Mesure 4 Mesure 5 Mesure 6 Mesure 7 Mesure 8
         Intro      Drop     Easing   Morph    Systems  HangTime Climax   Outro
```

- **Mesure 1 (`00:00.00 - 00:01.88`, RMS = 0.0825)** : Introduction atmosphérique, bourdonnement feutré, pose de l'univers visuel.
- **Mesures 2 à 5 (`00:01.88 - 00:09.38`, RMS $\approx$ 0.242)** : Plateau de groove stable à énergie constante (les 4 piliers didactiques : Identité, Easing, Morphing, Systèmes procéduraux).
- **Mesure 6 (`00:09.38 - 00:11.25`, RMS = 0.0841)** : **Breakdown acoustique / Drop de filtre** : Chute de volume de $65\%$, disparition de la batterie, suspension spatiale 3D.
- **Mesure 7 (`00:11.25 - 00:13.12`, RMS = 0.2528)** : **Climax stroboscopique** : Intensité maximale absolue du film, percussions mitraillettes, "NEVER LINEAR."
- **Mesure 8 (`00:13.12 - 00:15.06`, RMS = 0.1348, Peak = 0.8524)** : **Impact cathartique & Extinction** : Pic d'amplitude maximal absolu de toute la timeline à la frame 788 sur le sub-drop, suivi d'une décroissance harmonique douce.

---

## 3. Typologie des SFX (Sound Effects)

### 3.1. Impacts & Sub-Drops (Basses Fréquences 30-80 Hz)
- **Frame 113 (`00:01.88`)** : **Impact Kick Lourd & Sub-Drop 45 Hz** : Coïncide exactement avec le cut vermillon et le snap géant "CLAUDE".
- **Frame 310 (`00:05.15`)** : **Impact Harmonique Cloche & Résonance Sub** : Déclenché lorsque les 6 billes atteignent simultanément la borne B ($X=1700px$).
- **Frame 788 (`00:13.12`)** : **Sub-Drop Titanesque (Peak 0.852)** : Déflagration acoustique majeure accompagnant l'éruption de l'iris bloom et l'expulsion des confettis.

### 3.2. Risers, Sweeps & Whooshes de Transition
- **Frames 84 à 112 (`00:01.40 - 00:01.87`)** : **Riser de Filtre Ascendant** : Montée en fréquence d'un bruit blanc filtré résonant ($200\text{ Hz} \to 8000\text{ Hz}$) pendant la torsion de l'astérisque.
- **Frames 479 à 506 (`00:07.97 - 00:08.42`)** : **Whoosh de Balayage Horizontal** : Souffle d'air stéréo panoramique accompagnant le front d'onde de gauche à droite sur les tuiles de Truchet.
- **Frames 760 à 787 (`00:12.65 - 00:13.10`)** : **Crescendo de Rafale Laser** : Sifflement aigu d'accélération exponentielle précédant le drop final de la mesure 8.

### 3.3. Télémétrie UI, Bips & Digital Clicks
- **Frame 0 (`00:00.00`)** : **Tick d'Initialisation UI** : Micro-clic sec de 12ms marquant l'allumage des cornières de cadrage.
- **Frame 226 (`00:03.75`)** : **Clic d'Ouverture Console** : Déclic mécanique haute fréquence lors du cut vers le fond crème du chapitre 02.
- **Frames 366, 394, 422 (`00:06.10, 00:06.57, 00:07.03`)** : **Bips Harmoniques de Transformation** : Triades de bips électroniques à chaque métamorphose géométrique (Cercle $\to$ Triangle $\to$ Étoile $\to$ Carré).
- **Frame 846 (`00:14.07`)** : **Clic de Verrouillage Mécanique** : Cliquetis de contact lors du tracé du filet horizontal et de l'apparition de la mire centrale `◉`.

### 3.4. Dactylographie & Claviers Mécaniques
- **Frames 141 à 168 (`00:02.35 - 00:02.80`)** : Micro-clics de commutation lors de la déformation de la lettre "C".
- **Frames 846 à 875 (`00:14.07 - 00:14.52`)** : Séquence feutrée de dactylographie accompagnant l'apparition des caractères du footer technique.

---

## 4. Gestion du Vide, Silences & Suspension (Hang Time)

L'efficacité dramatique du film repose sur le contraste entre la saturation percussive et des zones de creux méticuleusement ménagées :

### 4.1. La Suspension d'Apex de la Mesure 6 (Frames 647 à 675, `00:10.78 - 00:11.23`)
- **Phénomène** : À la fin de la démonstration 3D, le tore s'effondre dans le noir. Pendant 28 frames entières (près de $0.5$ seconde), la bande sonore retire tout transitoire percussif. Seul subsiste un silence de plomb avec une traînée de réverbération agonisante.
- **Effet psychologique** : L'oreille s'ouvre, le cerveau anticipe l'impact. Ce silence pré-climax est la condition nécessaire pour que le déchaînement stroboscopique de la Scène 06 produise son effet de choc cinétique maximal.

### 4.2. Le Creux de Pré-Impact de la Frame 784 à 787 (`00:13.07 - 00:13.11`)
- **Phénomène** : 4 frames d'extinction totale (cut sonore absolu) juste avant le coup de kick monstrueux de la frame 788.
- **Principe de dynamique** : Sans ce micro-silence de 66 millisecondes, le cerveau fusionnerait le riser montant avec l'impact du sub-drop, détruisant la sensation de déflagration physique de l'iris bloom.

---

## 5. Tableau Synoptique Audio $\to$ Image (Matrice Déclencheur / Rendu)

| Timestamp (Frame @ 60fps) | Événement Sonore (Audio Cue) | Action Graphique Déclenchée | Paramètre de Code / Trigger Logiciel |
|---|---|---|---|
| `00:00.00` (F0) | Clic d'initiation + bourdonnement sub | Apparition des cornières HUD `[ ]` et du point rouge central | `if (frame === 0) triggerHudBoot();` |
| `00:00.47` (F28) | Snare feutrée + clic métallique | Éclosion radiale des 12 rayons de l'astérisque | `spring({ frame: frame - 28, config: { damping: 12 } });` |
| `00:00.93` (F56) | Hi-hat étincelant + nappe montante | Déploiement et rotation du texte courbe sur tracé | `textPathRotation = (frame - 56) * 0.75;` |
| `00:01.40` (F84) | Riser de filtre ascendant | Pré-rotation d'anticipation et torsion de l'astérisque | `asteriskTwist = -30 * Math.sin(progress * Math.PI);` |
| `00:01.88` (F113) | **Impact Kick Lourd + Sub-Drop** | Cut plein écran rouge + Snap géant "CLAUDE" | `bgColor = '#F04B38'; titleScale = expoOut(1.18 -> 1.0);` |
| `00:02.35` (F141) | Snare claquante + percussion glitch | Dilatation transversale du "C" ($scaleX = 1.85$) | `scaleXC = interpolate(springProgress, [0, 1], [1.0, 1.85]);` |
| `00:02.82` (F169) | Clap syncopé + arpège aigu | Glissement ascendant masqué de `motion designer` | `subtitleY = interpolate(frame - 169, [0, 20], [80, 0]);` |
| `00:03.75` (F226) | **Drop Beat complet + Clic console** | Cut fond crème + Déploiement de la grille d'easing | `currentChapter = '02 - EASING'; bgColor = '#F2EFE6';` |
| `00:04.22` (F254) | Kick lourd + Hi-hats 1/16 | Lancement des 6 billes + impression des ticks de spacing | `isRacing = true; startFrame = 254; duration = 56;` |
| `00:05.15` (F310) | Impact cloche + onde de sub | Arrivée simultanée à B + émission de 6 ondes de choc | `shockwaveRadius = (frame - 310) * 2.2;` |
| `00:05.63` (F338) | **Kick lourd + Nappe saturée** | Cut fond cobalt + Apparition dial de morphing | `currentChapter = '03 - MORPHING'; bgColor = '#302FF5';` |
| `00:06.10` (F366) | Snare claquante + bip harmonique | Morphing 1 : Cercle $\to$ Triangle avec sillage filaire | `morphTarget = 'triangle'; springRot = 88.0;` |
| `00:06.57` (F394) | Hi-hat syncopé + bip UI | Morphing 2 : Triangle $\to$ Étoile 5 branches | `morphTarget = 'star'; springRot = 190.0;` |
| `00:07.03` (F422) | Snare lourde + balayage de filtre | Morphing 3 : Étoile $\to$ Carré Squircle | `morphTarget = 'square'; springRot = 282.4;` |
| `00:07.50` (F451) | **Kick lourd + Crépitement cliquets** | Cut fond noir + Déploiement pavage Truchet 153 tuiles | `currentChapter = '04 - SYSTEMS'; seed = 0x2A;` |
| `00:07.97` (F479) | Whoosh de balayage + cliquets | Vague 1 : Front horizontal rouge de gauche à droite | `waveFrontX = (frame - 479) * 48;` |
| `00:08.43` (F507) | Snare syncopée + sweep retour | Vague 2 : Front de rétablissement de la couleur crème | `waveFrontX2 = (frame - 507) * 48;` |
| `00:08.90` (F535) | Percussions d'inférence + onde sub | Vague 3 : Onde concentrique circulaire depuis le centre | `rippleRadius = (frame - 535) * 32;` |
| `00:09.38` (F563) | **Breakdown : Drone sub filtré** | Bascule 3D en perspective (Focal 1400, plongée $25^\circ$) | `currentChapter = '05 - DEPTH'; cameraFocal = 1400;` |
| `00:09.85` (F591) | Pulsation feutrée + réverb spatiale | Sphère 3D géodésique (576 sommets) en rotation Y | `meshType = 'sphere'; rotY = (frame - 591) * 0.024;` |
| `00:10.32` (F619) | Résonance montante + effet Doppler | Tore 3D (576 sommets) en accélération de rotation Y | `meshType = 'torus'; rotY = (frame - 619) * 0.045;` |
| `00:10.78` (F647) | **Silence total (Hang Time)** | Effondrement du tore + Écran noir de suspension | `meshAlpha = 0.0; isSuspension = true;` |
| `00:11.25` (F676) | **Mitrailleuse Kick/Snare** | Flash crème + Bandes cobalt lettre "N" | `currentChapter = '06 - KINETIC TYPE'; strobeIndex = 0;` |
| `00:11.72` (F704) | Impact Snare saturé + Bip strident | Flash jaune lime acide + Titre géant "NEVER" | `bgColor = '#E3FF44'; title = 'NEVER'; chromaticSplit = 4;` |
| `00:12.18` (F732) | Kick lourd + Whoosh laser | Flash fond noir + "LINEAR." + Tracé vecteur diagonal | `bgColor = '#0F0F11'; title = 'LINEAR.'; vectorLaunch = true;` |
| `00:12.65` (F760) | Rafale crescendo + Riser bruit blanc | Stroboscope multi-fonds frénétique (1 flash / 2 frames) | `strobeBg = [black, cream, cobalt, lime][(frame - 760) % 4];` |
| `00:13.12` (F788) | **Sub-Drop Titanesque (Peak 0.852)** | Éruption iris bloom radial + Explosion 40 confettis | `currentChapter = '07 - FIN'; triggerShockwave();` |
| `00:13.60` (F816) | Résonance sub basse + Clic mécanique | L'astérisque glisse à gauche, "CLAUDE" se verrouille | `asteriskX = interpolate(progress, [0, 1], [960, 360]);` |
| `00:14.07` (F846) | Nappe synthétique chaude | Tracé du filet horizontal + Footer de métadonnées | `ruleWidth = interpolate(progress, [0, 1], [0, 1400]);` |
| `00:14.53` (F876) | Décroissance de réverbération feutrée | Arrêt sur image parfaite sur composition finale | `isFrozen = true; timecode = '00:00:14:44';` |
| `00:15.06` (F904) | Silence complet final | Coupure finale nette du film | `playbackFinished = true;` |
