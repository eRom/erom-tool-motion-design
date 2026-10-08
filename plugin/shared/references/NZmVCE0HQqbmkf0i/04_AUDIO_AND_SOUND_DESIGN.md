# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de la vidéo MIRR (`NZmVCE0HQqbmkf0i.mp4`) sous l'angle du monteur et de l'ingénieur de motion design. L'objectif est de formaliser comment chaque composant acoustique (rythmique électro, transitoires percussifs, sound effects UI/Foley, suspensions et silences) justifie, propulse et verrouille l'image à la frame près.

---

## 1. Structure Rythmique & Synchronisation Image

La timeline musicale repose sur une production électronique moderne cadencée rigoureusement à **129.2 BPM** en signature **4/4** :
- **Durée par temps (Beat)** : `0.4644 seconde` = **27.86 frames** à 60.0 fps.
- **Durée par mesure (Bar 4/4)** : `1.858 seconde` = **111.46 frames** à 60.0 fps.
- **Périodicité Structurelle** : L'intégralité des modules produit (Dashboard, Kanban, Devis, Factures, NLP, Telegram, Pointeuse, Bilan) respecte un cycle immuable de **2 mesures complètes** (8 temps / ~222 frames), créant une cadence hypnotique propice à l'absorption d'informations denses.

### Matrice d'Asservissement Percussif

| Élément de Percussion | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse Lourde)**<br>(Temps 1 et 3) | **Impacts de masse et impulsions d'échelle** :<br>- Ouverture explosive du tableau de bord (00:05.93, f 356)<br>- Révélation monumentale du ratio de marge `+42%` (00:24.53, f 1472)<br>- Clic d'arrêt synchrone des pointeuses d'ouvriers (00:34.00, f 2040)<br>- Secousses caméra (camera shake) en impulsion exponentielle | `const kickImpulse = 1 + 0.06 * Math.exp(-progress * 8);` |
| **Snare / Clap (Caisse Claire)**<br>(Temps 2 et 4) | **Cuts francs et bascules spatiales** :<br>- Déclenchement des whip-pans horizontaux entre les modules<br>- Inversion d'états (bouton STOP rouge virant au badge validé)<br>- Flashs stroboscopiques de transition | `const isCutFrame = frame % framesPerBeat < 1;` |
| **Hi-Hats & Cymbales Fines**<br>(Doubles-croches) | **Micro-pulsations télémétriques** :<br>- Cadence de clignotement du curseur de saisie dans le prompt IA<br>- Micro-vibrations des coins de cadrage `[ ]` de l'appareil photo<br>- Pas de défilement des barres d'histogramme de finance | `const tickStep = Math.floor(frame / (framesPerBeat / 4));` |
| **Bassline Synthé (Sub-Bass)** | **Soutien de flottaison 3D** :<br>- Maintien de la tension cinétique pendant les lents travellings avant (dolly-in) des cartes isométriques | Fréquence fondamentale calée entre 45 Hz et 65 Hz. |

---

## 2. Typologie des SFX (Sound Effects)

Le sound design combine des textures électroniques épurées et des bruitages concrets (Foley) pour donner un corps physique aux manipulations logicielles abstraites.

### 2.1. Whooshes (Balayages & Vélocité Latérale)
- **Rôle** : Justifier les mouvements de caméra brutaux et masquer les transitions de scènes lourdes.
- **Occurrences Clés** :
  - `00:05.90` : Whoosh d'ouverture basse fréquence accompagnant l'onde de choc vers le Dashboard.
  - `00:09.40` : Whoosh horizontal rapide soutenant le whip-pan du Dashboard vers le Kanban.
  - `00:13.05` : Balayage acoustique accompagnant l'agrandissement de la carte prospect vers la modale de devis.
- **Règle de Montage** : Le whoosh audio prend naissance **4 frames avant** le pic de flou de mouvement visuel pour préparer l'oreille à l'inertie.

### 2.2. Risers & Pitch-Bends (Tension & Montée en Puissance)
- **Rôle** : Créer une aspiration dramatique avant chaque libération d'information majeure.
- **Occurrences Clés** :
  - `00:03.50 - 00:04.00` : Riser de bruit blanc montant vers le centre lors de la convergence des 4 frictions.
  - `00:16.80 - 00:17.00` : Riser haute fréquence annonçant le déclencheur de scan OCR.
  - `00:36.50 - 00:38.90` : Riser harmonique montant en crescendo continu sur toute la séquence d'histogramme annuel, saturant l'espace avant le lâcher du climax staccato.

### 2.3. Impacts & Sub-Drops (Poids & Consécration)
- **Rôle** : Conférer un sentiment d'irréversibilité et de vérité comptable indiscutable.
- **Occurrences Clés** :
  - `00:04.00` (f 240) : Sub-drop sourd lors de l'arrêt de la pastille cyan au centre sur l'interrogation `A gdyby to było w jednym miejscu?`.
  - `00:24.53` (f 1472) : Coup de grosse caisse surchargé en sous-graves (sub-bass hit) lors de l'apparition en snap-in du `+42%`.
  - `00:34.00` (f 2040) : Impact percutant mat marquant l'arrêt net des chronomètres et le calcul des heures.

### 2.4. Glitches & Bleeps UI (Télémétrie Numérique)
- **Rôle** : Matérialiser l'intelligence en action et le traitement de données en coulisses.
- **Occurrences Clés** :
  - `00:17.80` : Bip haute fréquence (chirp) émis lors de la reconnaissance de facture (`FAKTURA WYKRYTA`).
  - `00:21.00 - 00:22.50` : Clics feutrés et réguliers de touches d'ordinateur (mechanical keyboard tactile foley) pendant la saisie de l'invite `Ile zarobiliśmy na Michalskim?`.
  - `00:23.20` : Sonorité synthétique douce de notification IA au moment où la réponse `Liczę z faktur...` commence à streamer.
  - `00:28.20` : Ding cristallin standard de message reçu Telegram sur le smartphone 3D.

### 2.5. Foley Matériel & Mécanique (Ancrage Terrain BTP)
- **Rôle** : Rappeler la réalité concrète du chantier et des transactions.
- **Occurrences Clés** :
  - `00:14.50 - 00:15.50` : Cliquetis métallique d'odomètre rotatif (roulette mécanique) pendant le défilement accéléré des montants nets.
  - `00:18.20` : Bruitage mécanique de déclenchement d'obturateur photo de reflex/smartphone (shutter click).
  - `00:32.20 - 00:33.80` : Tic-tac précipité de trotteuse mécanique (fast ratchet ticking) accompagnant la course folle des chronomètres ouvriers.

---

## 3. Gestion du Vide & Silences (Hang Time)

L'impact émotionnel du film repose autant sur ses creux d'énergie calculés que sur sa vélocité :

1. **La Suspension Initiale (00:00 - 00:03.40)** :
   - Niveau d'énergie : `RMS = 0.018` (silence presque total).
   - Rôle : Créer un contraste radical avec le vacarme habituel des chantiers. Le spectateur est placé dans le silence solitaire du dirigeant dans sa camionnette à 21h47.
2. **Le Creux d'Attention NLP (00:20.60 - 00:22.00)** :
   - Atténuation de la ligne de basse, seules les percussions aiguës et le bruit des touches subsistent.
   - Rôle : Focaliser 100% de la bande passante cognitive sur la simplicité enfantine du prompt textuel.
3. **La Micro-Rupture Pré-Climax (00:38.80 - 00:38.90, 6 frames)** :
   - Extinction subite du riser 100ms avant le premier flash-cut staccato.
   - Rôle : Créer un "trou d'air" acoustique rendant le mitraillage de cuts d'autant plus percutant.
4. **Le Decay Réverbéré Final (00:44.00 - 00:48.81)** :
   - Retrait complet de la batterie, accord de nappe synthétique s'éteignant avec une réverbération spatiale de 4 secondes.
   - Rôle : Laisser le logo `MIRR.` et son URL `mirr.pl` s'imprimer sur la rétine dans le calme retrouvé.

---

## 4. Tableau Synoptique Audio -> Image

| Séquence | Timestamp | Déclencheur Sonore (Audio Cue) | Action Graphique & Mouvement | Paramètre de Code / Event Trigger |
|---|---|---|---|---|
| **01. Intro** | `00:00.17` (f 10) | Click feutré | Apparition de la pastille cyan sur Cadran 1 | `onWaypointEnter(0)` |
| | `00:00.75` (f 45) | Micro-whoosh doux | Glissement de la pastille vers Cadran 2 | `startSpringTransition(1)` |
| | `00:03.50` (f 210) | Début du riser passe-haut | Translation au centre et expansion du rayon | `coreExpansionStart()` |
| | `00:04.00` (f 240) | Sub-drop sourd | Arrêt de la pastille, kinetic typo `A gdyby to było...` | `triggerDropHeadline()` |
| **02. Pulpit** | `00:05.93` (f 356) | **Kick lourd + whoosh sub** | Onde de choc circulaire, explosion 3D du Dashboard | `triggerShockwave(cx, cy)` |
| **03. Kanban** | `00:09.45` (f 567) | Snare sec + whoosh latéral | Whip-pan horizontal, arrivée de la grille Kanban | `triggerWhipPan('right')` |
| | `00:11.20` (f 672) | Clic doux de carte | Élévation 3D de `Jakub Kowalski` avec lueur teal | `elevateCard('jakub-kowalski')` |
| **04. Devis** | `00:13.10` (f 786) | Beat continu + cliquetis | Expansion de la carte en tableau métré de devis | `expandModalToQuotation()` |
| | `00:15.00` (f 900) | Cliquetis d'odomètre | Rotation des tambours du montant `5 414,50 zł` | `spinOdometer(5414.50)` |
| **05. Facture** | `00:16.97` (f 1018) | Transitoire percussion | Apparition facture 3D + laser cyan descendant | `startLaserScan(duration: 45)` |
| | `00:18.20` (f 1092) | Shutter photo + bip OCR | Réticule resserré, flash blanc (1f), insertion liste | `triggerPhotoCapture()` |
| **06. Agent** | `00:20.63` (f 1238) | Dépression audio (creux) | Slide-up boîte de chat, titre `Piszesz po ludzku.` | `openChatModal()` |
| | `00:21.00` (f 1260) | Bruitage clavier dactylo | Saisie caractère par caractère du prompt | `typewriterText(promptString)` |
| | `00:23.20` (f 1392) | Chirp confirmation IA | Streaming de la réponse agent avec pulsing dot | `agentResponseStream()` |
| **07. Marża** | `00:24.53` (f 1472) | **Kick drum surchargé** | Snap brutal du `+42%` géant avec lueur de bloom | `triggerGiantKpiSnap('+42%')` |
| **08. Telegram** | `00:28.17` (f 1690) | Ding notification Telegram | Smartphone 3D entrant à droite, bulle facture | `showTelegramMockup()` |
| | `00:29.50` (f 1770) | Pop de validation | Apparition bulle `✔ Zaksięgowane` | `triggerTelegramReply()` |
| **09. Pointeuse** | `00:31.88` (f 1913) | Cliquetis de trotteuse | Lancement des chronomètres ouvriers en avance rapide | `startFastTimers()` |
| | `00:34.00` (f 2040) | **Impact mat percutant** | Clic STOP simultané, bascule en cyan, jauge budget | `stopTimersAndCalculate()` |
| **10. Bilan** | `00:36.27` (f 2176) | Riser synthé ascendant | Barres d'histogramme s'élevant de gauche à droite | `animateBarChartSequential()` |
| **11. Climax** | `00:38.92` (f 2335) | **8 impacts mitraillés** | 8 flash-cuts (Jakub, 91k, Facture, +42%, Wave, 8h30, 30%, Core) | `triggerStaccatoCuts(cuts)` |
| **12. Orbites** | `00:39.42` (f 2365) | Nappe mélodique apaisée | Déploiement des 6 satellites gravitant autour du noyau | `startOrbitalSystem()` |
| **13. Outro** | `00:43.37` (f 2602) | Accord synthé final en decay | Effondrement des orbites vers le point `MIRR.`, CTA | `snapOrbitalToLogoDot()` |
