# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `minchoi-check-out.mp4` (*Hypergentik Manifesto* par Min Choi / @minchoi) sous l'angle du monteur et du motion designer. Il formalise comment chaque composant acoustique (grille 120 BPM, pulsation de batterie, effets sonores SFX, suspensions et silences) dicte, propulse et justifie l'image pour un agent de fabrication logicielle.

---

## 1. Structure Rythmique & Synchronisation Image

La bande sonore est calibrée sur une signature standard 4/4 à **120.0 BPM**, créant une relation mathématique directe entre la musique et la cadence d'affichage vidéo (60.0 fps) :

- **1 temps musical (Beat)** = `0.500 seconde` = **exactement 30.0 frames**.
- **1 mesure complète (Bar 4/4)** = `2.000 secondes` = **exactement 120.0 frames**.
- **1 demi-temps (Croche)** = `0.250 seconde` = **15.0 frames**.
- **1 quart de temps (Double croche)** = `0.125 seconde` = **7.5 frames**.

Chaque événement visuel majeur est asservi à un instrument de la composition sonore :

| Élément Percussif | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse)**<br>(Temps 1 et 3) | **Impacts de masse et impulsions d'échelle** :<br>- Entrées d'impacts de nouveaux blocs de texte<br>- Impulsion de scale caméra (`scale: 1.05 -> 1.0` en 6 frames)<br>- Déclenchement des flashs optiques lumineux (frame 480, frame 3120) | `const kickScale = 1 + 0.05 * Math.exp(-progress * 8);` |
| **Snare / Clap (Caisse Claire)**<br>(Temps 2 et 4) | **Cuts francs et bascules de contraste** :<br>- Changements de plans et coupures franches<br>- Clignotement des wireframes UI<br>- Micro-sursauts d'aberration chromatique (2px à 5px) | `const glitchOffset = isSnare ? (1 - progress) * 4 : 0;` |
| **Hi-Hats & Shakers**<br>(Doubles croches / 7.5 frames) | **Micro-animations télémétriques & UI** :<br>- Cadence de frappe des caractères du terminal<br>- Fréquence de scintillation des particules d'arrière-plan<br>- Jitter des indicateurs numériques dans les dashboards | `const charStep = Math.floor(frame / 2.5);` |
| **Synth Lead & Bassline** | **Morphoses géométriques continues** :<br>- Vitesse angulaire de rotation du tesseract 4D<br>- Vitesse de défilement des colonnes de code radial<br>- Balayage de la ligne de scan laser | `const laserY = (frame % framesPerBar) / framesPerBar;` |

---

## 2. Typologie des SFX (Sound Effects)

Le sound design du film se dispense totalement de voix off parlée : la narration est portée par la typographie cinétique et amplifiée par une scénographie sonore riche combinant science-fiction analogique et textures numériques tranchantes.

### 2.1. Whooshes & Swishes (Balayages & Inertie)
- **Rôle** : Matérialiser la vitesse de déplacement physique des éléments graphiques à travers l'écran.
- **Occurrences clés** :
  - `00:12` : Whoosh panoramique doux accompagnant la translation latérale de l'astérisque 3D vers la droite.
  - `00:16` : Swish d'aspiration tourbillonnaire (vortex sound) lors de la mise en rotation des cartes de tâches.
  - `00:24` : Balayage spatial lors de la bascule de caméra vers le sol en perspective 3D.
  - `00:36` : Whoosh volumétrique continu lors de la traversée des anneaux hexagonaux dans le tunnel hyperspace.
- **Règle de synchronisation** : Le balayage audio démarre 4 frames **avant** le mouvement visuel pour anticiper l'inertie de l'objet.

### 2.2. Risers & Tension Sweeps (Montées & Ruptures)
- **Rôle** : Créer une tension dramatique annonçant les bascules narratives du film.
- **Occurrences clés** :
  - `00:06 - 00:08` : Riser de bruit blanc filtré montant jusqu'à la rupture de la frame 480 (apparition du tesseract).
  - `00:38 - 00:40` : Montée harmonique et accélération de pulsation avant la coupure au silence de 00:40.
  - `00:50 - 00:52` : Roulement de caisse claire s'accélérant avec sweep de filtre résonant avant le Climax Vert.

### 2.3. Sub-Drops & Percussive Heavy Impacts (Poids & Choc)
- **Rôle** : Conférer une masse monumentale aux apparitions clés du récit.
- **Occurrences clés** :
  - `00:08` (Frame 480) : **Sub-drop cataclysmique (Pic RMS 0.3422)** marquant la matérialisation du tesseract et l'ouverture de la grille alvéolaire.
  - `00:41` (Frame 2460) : Impact sec et lourd sur la première antithèse (*"It cannot tell you whether the interface should exist"*).
  - `00:44` (Frame 2640) : Impact percussif sur le cylindre de code.
  - `00:47` (Frame 2820) : Impact percussif sur le mur de vignettes visuelles.
  - `00:52` (Frame 3120) : **Impact maximal du film (Downbeat Bar 27)** déclenchant l'inversion vers le plein écran vert fluo.

### 2.4. Telemetry Glitches & UI Audio (Sons d'Interface)
- **Rôle** : Donner vie aux interfaces logicielles et signifier l'exécution computationnelle.
- **Occurrences clés** :
  - `00:01 - 00:04` : Clavier terminal dactylographique rapide à touches courtes et feutrées (soft mechanical click).
  - `00:21 - 00:23` : Bip électronique cristallin (ping aigu) à chaque validation de coche `[✓]` sur les cartes de valeur le long du laser.
  - `00:25 - 00:27` : Bourdonnement statique haute fréquence (hum 12 kHz) calé sur le passage vertical de la ligne de scan laser.
  - `00:29` : Bleeps télémétriques discrets sur l'actualisation des chiffres du dashboard (*"412 hours"*, *"3,208 tasks"*).

### 2.5. Textures Spatiales & Foley Atmosphérique
- **Rôle** : Poser l'immensité du vide et contraster avec la frénésie du code.
- **Occurrences clés** :
  - `00:32 - 00:35` : Réverbération spatiale cathédrale avec souffle cosmique grave lors de la plongée dans l'écran mobile et la contemplation des aurores boréales.

---

## 3. Gestion du Vide & Suspensions (Hang Time)

L'intensité visuelle et rythmique du film ne fonctionne que par la présence de respirations acoustiques stratégiques :

1. **La Suspension Pré-Impact (00:07.5 / Frames 450 - 480)** :
   - Extinction subite des fréquences aiguës sur les deux derniers temps de la mesure 4.
   - Micro-silence de 10 frames juste avant le blast percussif de la frame 480 : le cerveau du spectateur anticipe le choc.

2. **Le Break Contemplatif (00:32 - 00:35 / Bar 17 - 18)** :
   - Chute spectaculaire de l'énergie RMS (de 0.27 à 0.14).
   - Arrêt complet des percussions pour laisser flotter les portails de storytelling.

3. **Le Silence de l'Antithèse (00:40.0 - 00:40.8 / Frame 2400 - 2450)** :
   - Creux d'énergie le plus bas du film après l'intro (RMS 0.0559).
   - La musique se fige pendant que le terminal dactylographie `AI can generate an interface.`, décuplant la violence du snap de la phrase suivante.

4. **L'Extinction Finale (01:05 - 01:06.1)** :
   - Décroissance logarithmique du volume master jusqu'au silence parfait.

---

## 4. Tableau Synoptique Audio -> Image

| Mesure (Bar 4/4) | Frames @ 60fps | Événement Sonore Majeur | Action Visuelle Déclenchée | Paramètre / Variable Remotion & Three.js |
|---|---|---|---|---|
| **Bar 01 - 02** | 0 - 240 | Nappe de synthé douce + pulsation discrète | Dactylographie progressive de la ligne monospace | `charCount = Math.floor(frame / 2.5)` |
| **Bar 03 - 04** | 241 - 480 | Riser de souffle + micro-silence pré-drop | Push vertical et snap-in du titre vert | `translateY = interpolate(springVal, [0, 1], [40, 0])` |
| **Bar 05 - 06** | 481 - 720 | **Sub-drop lourd (Pic RMS 0.34)** + Basse | Flash optique 1 frame + Matérialisation du Tesseract 4D | `triggerFlash = frame === 480; tesseractAlpha = 1.0;` |
| **Bar 07 - 08** | 721 - 960 | Basse ronde continue (RMS 0.25) | Tesseract se condense en astérisque 3D et glisse à droite | `asteriskX = spring(frame - 720, { stiffness: 180 })` |
| **Bar 09 - 10** | 961 - 1200 | **Entrée du Beat Principal complet** | Cut sur vortex d'aspiration des cartes de tâches | `vortexG = 1200; cardsOrbitSpeed = 1.8;` |
| **Bar 11 - 12** | 1201 - 1440 | Beat énergique + filtrage aiguës | Projection du faisceau laser vert + pings des 3 cartes | `laserProgress = interpolate(frame, [1201, 1260], [0, 1])` |
| **Bar 13 - 14** | 1441 - 1680 | Snare roll + bourdonnement électrique | Bascule de caméra sol 3D + ligne de scan laser UI | `scanProgress = (frame - 1441) / 180;` |
| **Bar 15 - 16** | 1681 - 1920 | Groove complet + bleeps télémétriques | Animation dynamique des dashboards et lueur smartphone | `throughputPoint = interpolate(frame, [1681, 1920], [0, 100])` |
| **Bar 17 - 18** | 1921 - 2160 | **Drop acoustique (RMS 0.14)** + nappe spatiale | Plongée à travers l'écran vers les portails vidéo 3D | `cameraZ = interpolate(frame, [1921, 2160], [0, 800])` |
| **Bar 19 - 20** | 2161 - 2400 | Riser de bruit blanc + battements sourds | Accélération hyperspace + star streaks directionnels | `warpFactor = Math.pow((frame - 2161) / 240, 2) * 12;` |
| **Bar 21.1 - 22.2** | 2401 - 2580 | **Silence partiel (0.05)** puis impact Bar 21 | Mur de wireframes sombres + Snap antithèse 1 (Interface) | `snapQuote1 = frame >= 2460; isGreenAccent = true;` |
| **Bar 22.3 - 23.4** | 2581 - 2760 | Impact percussif lourd Bar 22.3 | Cylindre de code en rotation + Snap antithèse 2 (Code) | `codeCylinderRotY = (frame - 2581) * 0.012;` |
| **Bar 24.1 - 25.2** | 2761 - 2940 | Impact percussif Bar 24.1 | Mur de vignettes visuelles + Snap antithèse 3 (Image) | `mosaicScale = interpolate(frame, [2761, 2940], [1.1, 1.0])` |
| **Bar 25.3 - 26.4** | 2941 - 3120 | Riser saturé puissant + caisse claire en roulement | Retour du Tesseract 4D + Titre "Humans with better tools" | `tesseractRotSpeed = 0.04; particleBurst = true;` |
| **Bar 27 - 29** | 3121 - 3480 | **Climax maximal du film (Downbeat Bar 27)** | **Inversion totale vers fond plein écran vert fluo** | `bgHexColor = '#6AFF3C'; textColor = '#000000';` |
| **Bar 30** | 3481 - 3600 | Sweep de décompression sonore (Bar 30.1) | Dissolution alvéolaire hexagonale de gauche à droite | `hexWipeProgress = (frame - 3481) / 120;` |
| **Bar 31 - 33.2** | 3601 - 3900 | Groove d'outro feutré, accords suspendus | Recomposition particulaire du logo `hypergentik*` | `logoParticleProgress = spring(frame - 3601);` |
| **Bar 33.3 - 34** | 3901 - 3967 | Fade out sonore vers le silence | Fondu au noir complet (Fade to black) | `masterOpacity = interpolate(frame, [3901, 3967], [1, 0])` |
