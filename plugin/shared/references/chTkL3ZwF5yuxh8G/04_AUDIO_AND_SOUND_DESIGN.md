# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `chTkL3ZwF5yuxh8G.mp4` (*Crew in the Dark* / *Every Frame Is Code*) sous l'angle exclusif du montage et de l'ingénierie cinématique. Il détaille la corrélation physique entre chaque événement acoustique (pulsation percussive, texture SFX, attaque vocale, silence de rupture) et son déclencheur graphique dans le code.

---

## 1. Structure Rythmique & Synchronisation Image

L'ensemble de la timeline visuelle est asservi à une métrique 4/4 à **123.05 BPM** cadencée à **30.0 fps** constants.

| Paramètre Temporel | Valeur Audio | Équivalent Vidéo (30 fps) | Rôle de Synchronisation Graphique |
|---|---|---|---|
| **Pulsation (Quarter Note / Beat)** | `0.4876 s` | **14.63 frames** | Snap-in des mots, impulsion de scale caméra, pas d'incrémentation HUD |
| **Demi-mesure (Half Bar - 2 beats)** | `0.9752 s` | **29.26 frames** | Changements de lignes de texte, alternance de quadrants |
| **Mesure Complète (Bar 4/4)** | `1.9504 s` | **58.51 frames** | Cuts majeurs de plan, rotations d'angle caméra, basculements de styles |
| **Phrase Harmonique (4 Mesures)** | `7.8016 s` | **234.05 frames** | Changement de bloc narratif (Prompt -> Feed -> Rail -> Odomètre) |
| **Section Formelle (8 Mesures)** | `15.603 s` | **468.10 frames** | Transition Couplet / Refrain / Pont / Outro |

### Asservissement aux Composants de Batterie

1. **Kick (Grosse Caisse - Temps 1 et 3)** :
   - **Déclencheur d'Échelle & Punch Caméra** :
     Chaque impact de kick déclenche une impulsion de zoom instantanée suivie d'un amortissement exponentiel :
     ```typescript
     const kickImpulse = isKick ? Math.exp(-frameSinceKick * 0.35) * 0.06 : 0;
     const currentCameraScale = 1.0 + kickImpulse;
     ```
   - **Arrivée des Mots Géants en Kinetic Typo** :
     Les termes monumentaux ("WOKE UP", "ZERO", "ONE PROMPT", "GRADIENT", "IT'S A CREW", "ONE") claquent rigoureusement sur le temps 1.
2. **Snare / Clap (Caisse Claire - Temps 2 et 4)** :
   - **Cuts Francs & Bascules de Contraste** :
     Les changements de plan, inversions noir/papier et coupes sèches tombent sur le temps 2 ou 4.
   - **Glitch Optique d'Aberration Chromatique** :
     Une impulsion de séparation RVB est injectée sur la snare :
     ```typescript
     const chromaticOffset = isSnare ? Math.max(0, 3.0 - frameSinceSnare * 0.75) : 0;
     ```
3. **Hi-Hats & Double-Croches (Subdivisions Rapides)** :
   - **Micro-Télémétrie HUD & Jitter** :
     Le clignotement du curseur terminal, l'incrémentation des millisecondes du timecode et le pas de défilement des logs sont cadencés sur les croches (toutes les 7.3 frames).
4. **Voix Lead (Attaques Consonnes & Voyelles Toniques)** :
   - **Kinetic Typography Syllabique** :
     L'apparition des mots secondaires n'est pas interpolée en continu : elle pop en opacité binaire (`0 -> 1` en 1 frame) calée sur le transitoire vocal exact.

---

## 2. Typologie des SFX (Sound Effects)

Le sound design combine des textures de science-fiction logicielle (bips, consoles, modems) et des bruitages diégétiques (Foley) très matériels qui incarnent la physicalité du code.

### 2.1. Whooshes (Balayages & Vélocité Caméra)
- **Usage** : Justifier les accélérations de travelling virtuel et l'inertie des déplacements d'objets.
- **Occurrences clés** :
  - `00:08` : Whoosh grave et ample accompagnant le plongeon caméra au-dessus du tapis social de Twitter.
  - `00:13` : Whoosh fluide et étiré accompagnant le défilement du ruban de film 35mm et la spline de voie ferrée.
  - `01:25` : Whoosh hyperspatial lourd et fendant propulsant le mot 3D `"ONE"` vers le spectateur.
- **Règle de synchronisation** : Le whoosh audio prend naissance **3 frames avant** le cut ou le démarrage du mouvement pour conférer une sensation d'inertie physique naturelle.

### 2.2. Risers & Pitch-Bends (Tension & Montée en Énergie)
- **Usage** : Créer l'attente d'une délivrance cinématique ou d'un basculement de structure.
- **Occurrences clés** :
  - `00:06 - 00:08` : Riser de bruit blanc filtré par filtre passe-haut montant en puissance durant la jauge `RENDERING 059%` jusqu'au kick de *"Woke up"*.
  - `00:42 - 00:44` : Sub-bass sweep descendant et distorsion pitchée matérialisant l'aspiration de la matière dans le trou noir.
  - `01:38 - 01:42` : Riser harmonique staccato saturant progressivement le spectre audio avant la coupure au noir.

### 2.3. Impacts & Sub-Drops (Masse Physique & Autorité)
- **Usage** : Imprimer un poids colossal et une autorité d'ingénierie sans appel.
- **Occurrences clés** :
  - `00:44` : Sub-drop tellurique ouvrant le refrain multi-agent post-trou noir (*"It was never one shot"*).
  - `00:56` : **Frappe de tampon mécanique lourd** : le tampon rouge `P0` produit un son mat et sourd de claque sur papier épais, combiné à un tremblement caméra (screen shake).
  - `01:19` : **Coupure nette de ciseaux** : son sec d'acier tranchant une feuille de papier sur le mot "HARD CUT".
  - `01:50` : **Clap de cinéma en bois** : claquement percutant du bras articulé du clap avec écho de studio de tournage.

### 2.4. Glitches & Télémétrie UI (Bleeps & Console)
- **Usage** : Manifester visuellement et acoustiquement le fonctionnement temps réel de l'agent IA.
- **Occurrences clés** :
  - `00:04` : Bruitages métalliques de clavier mécanique tactile tapant la commande prompt (`* > make it dynamic`).
  - `00:05` : Chirps FM haute fréquence à chaque rafraîchissement des probabilités de tokens (`dynamic: 0.62`).
  - `01:14` : Bip d'alerte chirurgical à tonalité double signalant l'anomalie d'alignement (`Δ 14° · FLAGGED`).
  - `01:35` : Son de surlignage feutre sec au moment où la ligne de checklist est rayée en rouge (`[✓] text overlaps at 0:41`).

### 2.5. Foley Matériel & Analogique
- **Usage** : Humaniser et donner une texture palpable au travail abstrait de l'ingénieur.
- **Occurrences clés** :
  - **Crépitement de cierge magique (Sparkler Foley)** (`00:00 - 00:04`, `00:13 - 00:16`, `01:28 - 01:31`) : Bruit continu de combustion d'étincelle crépitante calé sur la vitesse de déplacement de la tête de tracé.
  - **Cliquetis mécanique d'odomètre (Ratchet Gear)** (`00:18 - 00:20`) : Bruitage d'engrenages métalliques défilant à grande vitesse avant de se bloquer net avec un verrouillage de cliquet.
  - **Extinction de tube cathodique (CRT Power-down)** (`01:56`) : Sifflement aigu à 15 kHz décroissant instantanément dans un claquement de condensateur électrique.

---

## 3. Gestion du Vide & Silences Dramatiques (Hang Time)

L'une des signatures artistiques fondamentales de la vidéo réside dans la maîtrise chirurgicale du vide pour amplifier le relief dramatique :

### La Rupture Maîtresse : 01:42 - 01:44 (Frames 3061 - 3120)
- **Durée exacte** : **1.00 seconde** = **30 frames** (soit exactement 2 temps musicaux).
- **Phénomène acoustique** : Coupure instantanée de **l'intégralité du mix audio** (mute brutal de la batterie, des synthétiseurs, des voix et de la réverbération).
- **Phénomène visuel** : Cut au noir complet. Un unique point orange braise minuscule (`#FF5533`) immobile au centre géométrique `(0,0)`, avec la télémétrie `HOLD · 1.00 S`.
- **Rôle perceptif** : Cette suspension totale réinitialise l'attention du spectateur après la frénésie du couplet. Elle confère au drop final ("MAKE IT DYNAMIC V4") un impact physique démultiplié qui serait impossible dans un flot ininterrompu.

---

## 4. Tableau Synoptique Audio -> Image -> Trigger de Code

Correspondance plan par plan entre l'événement sonore, l'action à l'écran et la formule de déclenchement dans le code :

| Timestamp | Cue Audio & Événement | Action Visuelle / Mouvement | Déclencheur Algorithmique (Trigger Code) |
|---|---|---|---|
| `00:00` | Fizzing d'étincelle + sub-hum | Naissance du point `(0,0)` et arc polaire | `sparkEngine.emit(cx, cy, currentAngle);` |
| `00:04` | Dactylographie mécanique | Prompt tapé caractère par caractère | `const charCount = Math.floor(frame / 4);` |
| `00:08` | **Kick 1 + Voix Lead** : *"Woke up"* | Snap-in Z de "WOKE UP" + début travelling feed | `z = interpolate(springVal, [0, 1], [-400, 0]);` |
| `00:13` | Synth riff + Voix : *"Every frame"* | Défilement film 35mm + étincelle sur spline | `progress = (frame - start) / duration;` |
| `00:16` | Caisse claire : *"'Zero After Effects'"* | Cut direct sur guillemets orange braise | `cameraScale = 1.0 + 0.08 * Math.exp(-t * 8);` |
| `00:18` | Cliquetis mécanique d'engrenage | Rotation rapide des tambours odomètre | `drumRot = targetRot * easeOutBack(t);` |
| `00:20` | Voix : *"and they call it art"* | Cut papier + apparition cursive de *"art"* | `strokeDashoffset = length * (1 - ease(t));` |
| `00:24` | **Drop Refrain 1 (Batterie complète)** | Nappe 3D infinie de cartes dégradées violet | `cardFloor.updatePositions(scrollSpeed * t);` |
| `00:28` | Voix : *"Gradient in the middle"* | Centrage frontal de la typo géante | `gsap.to('.title', { x: 0, ease: 'power4.out' });` |
| `00:32` | Coup de caisse claire réverbéré | Flash blanc/orange + inversion de polarité | `flashOpacity = Math.max(0, 1.0 - t / 4);` |
| `00:36` | Voix : *"Everybody's genius / same"* | Tapisserie répétitive avec mot braise actif | `isLit = (wordIndex === 42 || wordIndex === 88);` |
| `00:40` | Montée de filtre & sub-bass dive | Vortex trou noir aspirant la carte violette | `r_warp = r * (1.0 - (rs * rs) / (r * r));` |
| `00:44` | **Sub-drop massif + Drop batterie** | Apparition 3D des 4 blocs d'agents | `crewBoxes.forEach((b, i) => b.spawn(i * 4));` |
| `00:50` | Voix : *"it's a crew"* | Embrasement orange des contours filaires | `wireframeColor = lerpColor(dim, ember, t);` |
| `00:56` | **Impact sourd de tampon mécanique** | Claquage violent du tampon rouge `P0` | `stampScale = 1.0 + 0.15 * Math.sin(t * 12) * Math.exp(-t * 6);` |
| `01:00` | Chops vocaux syncopés (*"I, I..."*) | Saccades typographiques en décalage | `glyphIndex = Math.floor(frame / framesPerBeat);` |
| `01:05` | Commande shell tapée | Console `$ ffmpeg` + planche contact 4x4 | `ffmpegCursorBlink = Math.floor(frame / 8) % 2 === 0;` |
| `01:09` | Clarté de synthé douce | Projecteur conique braqué sur Storyboard B | `spotlight.render(ctx, lightX, floorY);` |
| `01:14` | Bip d'alerte haute fréquence | Réticule rouge sur défaut `Δ 14° · FLAGGED` | `reticleAngle = lerp(14, 0, spring(t));` |
| `01:19` | Coup sec de ciseaux | Ligne pointillée rouge tranchée horizontalement | `cutX = interpolate(t, [0, 1], [0, totalWidth]);` |
| `01:25` | Whoosh hyperspatial violent | Dolly avant foudroyant sur mot 3D `"ONE"` | `cameraZ = interpolate(t, [0, 1], [1200, 0]);` |
| `01:31` | Climax vocal : *"crew in the dark"* | Graphe constellation avec astérisque central | `nodeGlow = 0.5 + 0.5 * Math.sin(t * 8);` |
| `01:35` | Son de surlignage feutre | Rature animée de la ligne de checklist P0 | `strikethroughWidth = progress * 100;` |
| `01:42` | **SILENCE COMPLET (0 dB, 1.00s)** | Écran noir total, point fixe `HOLD · 1.00 S` | `ctx.fillStyle = '#000000'; ctx.fillRect(0,0,W,H);` |
| `01:44` | Kick percutant + *"da-da-da"* | Papier ligné écolier : "MAKE IT DYNAMIC V4" | `pageScale = 1.0 + 0.04 * Math.exp(-t * 8);` |
| `01:46` | Voix feutrée : *"You're the director"* | Faisceau conique sur fauteuil de réalisateur | `chairAlpha = easeInQuad(t);` |
| `01:50` | **Claquement sec de clap (Foley)** | Impact du bras supérieur du clap 3D | `clapperAngle = t < 6 ? interpolate(t, [0, 6], [35, 0]) : 0;` |
| `01:54` | Voix parlée : *"Roll it again"* | Cible polaire `(0,0)` + extinction CRT | `crtScanlineHeight = Math.max(0, 1.0 - t / 4);` |
