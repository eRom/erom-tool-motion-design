# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `pleometrix-mexica.mp4` (*P(doom)* par Mexica / @pleometrix) sous l'angle du montage et de l'animation. L'objectif est de formaliser comment chaque élément sonore (pulsation, SFX, voix, silence) justifie, déclenche ou amplifie l'image pour un agent de fabrication.

---

## 1. Structure Rythmique & Synchronisation Image

L'ensemble de la timeline est verrouillé sur une signature 4/4 à **129.2 BPM** (~130 BPM), où chaque événement visuel majeur est asservi à un composant de la batterie :

| Élément Percussif | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse)**<br>(Temps 1 et 3) | **Impacts de masse et impulsions d'échelle** :<br>- Arrivée des mots monumentaux en kinetic typo<br>- Impulsion de scale caméra (`scale: 1.04 -> 1.0` en 5 frames)<br>- Scissions de formes ou collisions géométriques | `const kickScale = 1 + 0.08 * Math.exp(-progress * 6);` |
| **Snare / Clap (Caisse Claire)**<br>(Temps 2 et 4) | **Cuts francs et bascules de contraste** :<br>- Cuts de changement de plan ou de perspective<br>- Inversion de style (passage de plein à filaire `stroke`)<br>- Flash optique blanc (1 frame) ou impulsion d'aberration chromatique (2px à 6px) | `const chromaticGlitch = isSnare ? (1 - progress) * 6 : 0;` |
| **Hi-Hats & Percussions Rapides**<br>(Croches et doubles) | **Micro-animations télémétriques HUD** :<br>- Pas de défilement des compteurs numériques et valeurs d'angle<br>- Clignotement du curseur de console terminale<br>- Jitter et micro-vibrations des cadres de visée | `const stepTick = Math.floor(frame / (framesPerBeat / 4));` |
| **Voix Lead (Phrasé)** | **Kinetic Typography mot-à-mot** :<br>- Apparition synchronisée à la syllabe près<br>- Déformation de crête d'onde suivant la modulation vocale (oscilloscope 00:38) | Déclenchement d'opacité `0 -> 1` au début exact de la voyelle tonique. |

---

## 2. Typologie des SFX (Sound Effects)

Le sound design combine des textures de science-fiction synthétique et des bruitages diégétiques (Foley) très concrets qui ancrent les concepts mathématiques abstraits dans la matière physique.

### 2.1. Whooshes (Balayages & Vélocité)
- **Usage** : Justifier les mouvements de caméra brutaux et les déplacements d'objets traversant le viewport.
- **Occurrences clés** :
  - `00:05` : Whip-pan horizontal rapide faisant basculer la licorne de gauche à droite.
  - `00:26` : Travelling avant accéléré (dolly-in) s'enfonçant dans la bibliothèque 3D filaire de la chambre chinoise.
  - `01:44` : Balayage de caméra suivant la fuite de la mèche d'explosif vers la droite.
- **Règle de montage** : Le whoosh audio commence 3 à 5 frames **avant** le début du mouvement d'image pour anticiper l'inertie physique.

### 2.2. Risers & Pitch-Bends (Tension & Accélération)
- **Usage** : Matérialiser une perte de contrôle, une montée en puissance de calcul ou l'approche d'une singularité.
- **Occurrences clés** :
  - `00:09` : **Sub-bass dive** (glissando descendant très lourd) accompagnant la chute verticale de la courbe de *training loss*.
  - `00:21 - 00:22` : Riser de bruit blanc montant en filtre passe-haut jusqu'au point de rupture du flash blanc (00:22).
  - `00:46 - 00:52` : Riser harmonique accélérant la vitesse orbitale autour du trou noir avant la dispersion atomique.
  - `02:24 - 02:27` : Montée en fréquence staccato saturant le spectre audio pendant l'emballement exponentiel de `1e1000`.

### 2.3. Impacts & Sub-Drops (Poids & Clôture)
- **Usage** : Donner une masse colossale aux objets graphiques lors de leur apparition.
- **Occurrences clés** :
  - `00:22` : Impact d'explosion au sortir du flash blanc ouvrant le refrain sur *"'CAUSE THE FUTURE GOES BOOM"*.
  - `01:11` : **Impact de tampon mécanique lourd** : le tampon "SAFE ENOUGH" produit un son mat de claque sur papier couplé à une sous-fréquence sourde, déclenchant un tremblement caméra (screen shake).
  - `01:19` : Impact sec et buzzer d'erreur lors du claquage de la grande croix rouge sur l'architecture Von Neumann.

### 2.4. Glitches & Bleeps Télémétriques (UI & HUD)
- **Usage** : Signifier l'inférence machine, le tracking de vision et le traitement de données.
- **Occurrences clés** :
  - `00:16` : Bips discrets et textures FM d'échantillonnage de tokens lors de l'affichage des logits de prédiction (`top-p`).
  - `00:30 - 00:37` : Chirps électroniques haute fréquence (style radar/sonar) à chaque fois qu'une bounding box YOLO orange verrouille un œil du Shoggoth.
  - `00:38 - 00:41` : Bourdonnement analogique continu (hum 50/60 Hz de tube cathodique) couplé à une sinusoïde pure stabilisée.

### 2.5. Foley Matériel & Organique (Tactile)
- **Usage** : Créer un contraste satirique entre l'IA abstraite et des objets physiques obsolètes.
- **Occurrences clés** :
  - **Crépitement continu d'étincelle** (`00:00 - 00:05`, `01:41 - 01:45`, `02:30`) : Bruitage de cierge magique (fizzing sparkler foley) calé en temps réel sur la tête de tracé SVG.
  - **Dactylographie mécanique** (`00:16`, `01:10`, `01:29`) : Claquement sec de touches de clavier machine à écrire vintage (*IBM Selectric*), variable en cadence.
  - **Cliquetis d'odomètre rotatif** (`01:06 - 01:09`) : Bruitage mécanique d'engrenages et de tambours à chiffres défilant à grande vitesse (ratchet sound).
  - **Cascade métallique de trombones** (`01:37 - 01:40`) : Bruitage de milliers de petits trombones métalliques s'entrechoquant et tombant en pluie sur le sol.
  - **Barreaux de prison** (`00:53`) : Clang métallique lourd d'une grille de cellule qui s'abat.

---

## 3. Gestion du Vide, Silences & Suspension (Hang Time)

L'intensité visuelle du film est directement proportionnelle à sa gestion des ruptures acoustiques :

### 3.1. Le Micro-Silence Pré-Drop (Frame 1340, `00:22.3`)
- **Mécanisme** : La montée en tension (riser) est coupée net 2 frames avant l'impact du refrain.
- **Effet visuel** : Le flash blanc plein écran survient exactement dans ce vide acoustique d'une fraction de seconde. L'explosion de la batterie au retour de l'image décuple l'effet de souffle perçu par le spectateur.

### 3.2. La Rupture Théâtrale "Ilya" (`02:12 - 02:19`)
- **Mécanisme** : Arrêt total et immédiat de la rythmique électro-pop (batterie, basse, arpèges).
- **Ambiance** : Un piano acoustique solo intimiste, enregistré avec une longue réverbération de salle vide, accompagné d'un très léger souffle d'air.
- **Effet visuel** : L'image bascule du déluge numérique vers une scène de théâtre sombre avec un faisceau de projecteur conique sur un ordinateur portable (`REDACTED`). C'est le moment de suspension dramatique (*hang time*) indispensable avant l'explosion finale du climax.

### 3.3. L'Extinction CRT Terminale (`02:35 - 02:36`)
- **Mécanisme** : Sifflement d'extinction à haute fréquence d'un écran cathodique (décharge THT ~15 kHz), suivi d'un "pop" d'implosion sourd et d'un silence absolu.
- **Effet visuel** : L'image se replie horizontalement sur une ligne blanche avant de disparaître en un point central `(0,0)` qui s'éteint.

---

## 4. Tableau Synoptique Audio -> Image (Plan par Plan)

| Timestamp | Cue Musical / Rythme | Événement SFX Dominant | Action Graphique Asservie | Déclencheur Code (Trigger) |
|---|---|---|---|---|
| `00:00 - 00:05` | Synth doux + Kick sur AGI | Crépitement d'étincelle + clac d'intro | Tracé vectoriel TikZ licorne + snap AGI | Émetteur de particules calé sur volume sparkler |
| `00:09 - 00:10` | Voix : *"sudden drop"* | Sub-bass dive glissando | Chute abrupte de la courbe de loss | `translateY` indexé sur le pitch bend audio |
| `00:10 - 00:15` | Riser montant | Filtre passe-bas qui s'ouvre | Plongée caméra dans l'entonnoir 3D | Caméra Z liée au balayage de fréquence du synthé |
| `00:16 - 00:22` | Beat doux régulier | Dactylographie mécanique + bleeps | Typewriter text + barres de distribution tokens | Frappe caractère déclenchée par impulsion audio |
| `00:22.3` | **Micro-silence (2 frames)** | Rupture audio nette | **Flash optique blanc 1 frame** | Seuil de silence déclenchant l'overlay blanc |
| `00:23 - 00:25` | Drop du refrain (kick lourd) | Sub-drop + kick d'impact | Mots géants "MY / FUTURE GOES BOOM" | Snap-in typographique sur front d'onde du kick |
| `00:30 - 00:37` | Groove 130 BPM | Bip-bip de radar de visée | Bounding boxes verrouillant les yeux | Bounding box pop sur crête transitoire aiguë |
| `00:38 - 00:41` | Basse sinusoïdale pure | Bourdonnement CRT 50Hz + bip stable | Onde d'oscilloscope en tracé continu | Déformation d'onde calée sur la fréquence fondamentale |
| `00:53 - 00:58` | Basse sourde étouffée | Clang métallique de grille de prison | Barreaux 3D descendant du haut | Chute avec rebond élastique sur le son d'impact |
| `01:06 - 01:09` | Voix parlée rythmée | Cliquetis mécanique d'odomètre | Rouleaux de chiffres défilant à grande vitesse | Vitesse de rotation liée au tempo du cliquetis |
| `01:11` | Claque percussive | Bruitage sec de tampon encreur + sub | Tampon "SAFE ENOUGH" claquant sur papier | Screen shake vertical de 4px sur l'attaque du tampon |
| `01:19` | Temps fort 4 | Buzzer d'erreur / coupure | Croix rouge barrant Von Neumann | Apparition instantanée sur la consonne dure |
| `01:37 - 01:40` | Montée en puissance | Pluie métallique de trombones | Multiplication exponentielle de trombones 3D | Instanciation de maillages liée à la densité du foley |
| `01:41 - 01:45` | Synth arpège montant | Mèche qui se consume (fizzing) | Tête d'étincelle filant le long de la spline | Avancement de `strokeDashoffset` sur crépitement |
| `01:50 - 01:54` | Percussion martelée | Enclenchement mécanique lourd | Blocs Transformer empilés en ascenseur | Translation verticale par pas à chaque mesure |
| `02:12 - 02:19` | **Silence batterie / Piano solo** | Réverbération d'espace vide + souffle | Salle de spectacle sombre + projecteur conique | Atténuation drastique du motion blur et du jitter |
| `02:20 - 02:27` | Reprise brutale du refrain | Frénésie mécanique saturée | Explosion du compteur P(DOOM) vers 1e1000 | Vitesse d'incrément de chiffres exponentielle |
| `02:35 - 02:36` | Fin du morceau | Bip THT d'extinction CRT + clac | Ligne horizontale s'éteignant au centre `(0,0)` | Réduction de l'échelle Y à 0 sur la descente du bip |
