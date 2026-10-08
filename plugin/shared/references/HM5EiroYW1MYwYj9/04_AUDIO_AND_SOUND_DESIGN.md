# 04_AUDIO_AND_SOUND_DESIGN.md
## Spécifications Audio, Rythme & Sound Design
**Référence vidéo** : `HM5EiroYW1MYwYj9.mp4` (1920x1080 @ 30fps, 4247 frames, 141.568 s)  
**Tempo mesuré** : 143.55 BPM  
**Signature rythmique** : 4/4 Dance-Pop Électro-Japonaise / Synthpop Chiptune  

---

### Table des Matières
1. [Grille Rythmique & Métrique Temporelle Frame-Accurate](#1-grille-rythmique--métrique-temporelle-frame-accurate)
2. [Structure Musicale & Découpage en Sections](#2-structure-musicale--découpage-en-sections)
3. [Typologie Exhaustive du Sound Design (SFX Library)](#3-typologie-exhaustive-du-sound-design-sfx-library)
4. [Analyse des Suspensions, Creux d'Énergie et Silences (Hang Time)](#4-analyse-des-suspensions-creux-dénergie-et-silences-hang-time)
5. [Synoptique Audio vers Image (Mapping Événementiel Frame-Accurate)](#5-synoptique-audio-vers-image-mapping-événementiel-frame-accurate)
6. [Formules et Helpers de Synchronisation pour Codeurs (Remotion)](#6-formules-et-helpers-de-synchronisation-pour-codeurs-remotion)

---

### 1. Grille Rythmique & Métrique Temporelle Frame-Accurate

La composition musicale est verrouillée sur une horloge à 143.55 BPM. À une cadence vidéo de 30.0 images par seconde, les équivalences d'intervalles sont les suivantes :

| Subdivision Rythmique | Durée en Secondes | Durée en Frames Vidéo (@30fps) | Règle d'Arrondi Frame Remotion |
| :--- | :--- | :--- | :--- |
| **1/16 Note (Double croche)** | 0.1045 s | 3.135 frames | Alternance 3 / 3 / 3 / 4 frames |
| **1/8 Note (Croche)** | 0.2090 s | 6.270 frames | Alternance 6 / 6 / 7 frames |
| **1/4 Note (Noire / 1 Beat)** | 0.4180 s | 12.539 frames | Alternance 12 / 13 frames (moyenne 12.54) |
| **1/2 Note (Blanche / 2 Beats)**| 0.8359 s | 25.078 frames | 25 frames (correction +1 frame tous les 13 temps) |
| **1 Bar (Mesure 4/4)** | 1.6719 s | 50.157 frames | 50 frames (ajustement périodique de 51 frames) |
| **2 Bars (Demi-phrase)** | 3.3438 s | 100.313 frames | 100 frames |
| **4 Bars (Phrase musicale)** | 6.6876 s | 200.627 frames | 201 frames |
| **8 Bars (Section complète)** | 13.3751 s | 401.254 frames | 401 frames |

> **Règle d'or de synchronicité** : Les cuts majeurs et les apparitions de typographie cinétique ne tombent jamais de manière aléatoire. Ils sont asservis soit sur le temps fort (Beat 1 de la mesure, toutes les 50 frames), soit sur le contretemps de caisse claire (Beats 2 et 4, décalage de +12.5 et +37.6 frames).

---

### 2. Structure Musicale & Découpage en Sections

La pièce musicale se déploie selon une architecture pop en 7 grands blocs dynamiques :

```
[00:00.00] Intro Rétro-Chiptune & Solo Guitare Crunch
      │  (Mesures 1 à 6 / frames 0 à 301)
      ▼
[00:10.03] Couplet 1 : Rhythmique Groove & Basse Électro Bondissante
      │  (Mesures 7 à 22 / frames 301 à 1103)
      ▼
[00:36.78] Pré-Refrain 1 : Montée Harmonique, Arpèges Synthwave
      │  (Mesures 23 à 30 / frames 1103 à 1504)
      ▼
[00:50.13] Refrain 1 (Drop Majeur) : Tutti Synthpop, Chant Aigu, Kick Four-on-the-Floor
      │  (Mesures 31 à 46 / frames 1504 à 2307)
      ▼
[01:16.90] Couplet 2 / Pont Technique : Shift de Tonalité, Complexité Polyrythmique
      │  (Mesures 47 à 62 / frames 2307 à 3109)
      ▼
[01:43.65] Pré-Refrain 2 & Pont Suspendu : Solo Piano, Tension Maximale
      │  (Mesures 63 à 74 / frames 3109 à 3711)
      ▼
[02:03.70] Le Grand Hang Time (Coupure Totale & Reprise Choc)
      │  (Mesures 75 à 76 / frames 3711 à 3810 - silence à la frame 3764)
      ▼
[02:07.00] Refrain Final & Climax : Explosion Visuelle et Sonore, Overdrive
      │  (Mesures 77 à 84 / frames 3810 à 4210)
      ▼
[02:20.33] Outro & Résonance d'Extinction (frames 4210 à 4247)
```

---

### 3. Typologie Exhaustive du Sound Design (SFX Library)

La bande-son mêle la production musicale électronique japonaise à un habillage sonore diégétique et cartoonesque extrêmement fouillé. Six familles de bruitages sont synchronisées à l'image :

#### Famille A : Textures Papier, Adhésif & Sérigraphie (Papercraft SFX)
- **Tape Tear & Snap** : Bruit sec de déchirement et claquement de ruban adhésif vinyle ou papier Washi.
  - *Occurrences clés* : Apparition des cartouches de texte `AI WILL SURPASS US` (frame 150), transition de masquage (frame 952).
  - *Caractéristiques spectrales* : Pic transitoire entre 2.5 kHz et 5 kHz, durée courte (60 ms), décroissance abrupte.
- **Riso Stamp Thud** : Claquement sourd de tampon encreur mécanique et passage de cylindre d'impression.
  - *Occurrences clés* : Tampons `PROVEN` dans l'éditeur Lean 4 (frame 601), impact des chiffres de l'odomètre (frame 2553).
  - *Caractéristiques spectrales* : Résonance boisée autour de 220 Hz combinée à un cliquetis métallique à 4 kHz.

#### Famille B : Interface Informatique & Vintage Computing (Tech SFX)
- **Mechanical Keyboard Click (Chunky Clack)** : Frappe sur switch mécanique bleu/vert vintage.
  - *Occurrences clés* : Défilement des lignes de code Lean 4 (frames 601-752), saisie du prompt (frame 301).
- **Relay Switch & Geneva Drive Click** : Cliquetis métallique d'odomètre et relais bistable.
  - *Occurrences clés* : Rotation des tambours de calcul de FLOPs (frames 2553-2703).
- **CRT High-Pitch Whine & De-gauss** : Sifflement d'oscillateur cathodique à 15.6 kHz suivi d'une décharge magnétique sourde.
  - *Occurrences clés* : Plans de caméra thermique/vision nocturne (frames 2103, 3960).

#### Famille C : Cartoon, Burlesque & Pop Manga (Anime SFX)
- **Referee Whistle** : Coup de sifflet d'arbitre court et strident avec trille de bille.
  - *Occurrences clés* : Mascotte tournesol arbitre brandissant le carton rouge `OVERSIGHT FAIL` (frame 1203).
- **Creature Squeak & Purr** : Gloussement guttural et couinement synthétique.
  - *Occurrences clés* : Apparitions du Shoggoth masqué (frame 1052) et du chat Gato qui miaule sur le beat (frame 3309).
- **Spring Boing** : Son de ressort spirale en détente rapide avec modulation de pitch ascendante.
  - *Occurrences clés* : Rebond des mascottes sur la courbe de perte d'entraînement (frame 1752).

#### Famille D : Impacts Typographiques & Sub-Drops (Impact SFX)
- **Sub-Bass 808 Boom** : Onde sinusoïdale descendante de 90 Hz vers 35 Hz avec saturation d'harmoniques impaires.
  - *Occurrences clés* : Impact pleine page des mots géants `AGI`, `DOOM`, `SHOW`, `ALIGN` (frames 1504, 3810).
- **Glass Shutter Glitch** : Craquement d'échantillonnage numérique (bitcrush 8-bit) couplé à un bris de verre miniature.
  - *Occurrences clés* : Transitions de flash blanc stroboscopique (frames 1504, 2703, 3810).

---

### 4. Analyse des Suspensions, Creux d'Énergie et Silences (Hang Time)

L'intensité dramatique du clip repose sur un contraste saisissant entre une densité sonore saturée (tutti musical à 143.55 BPM) et des ruptures de vide chirurgicales.

#### Le Creux Pré-Drop Majeur (Frames 3764 à 3810 / 125.46 s à 127.00 s)
C'est le moment pivot narratif et technique de l'animation :
1. **Frame 3764 (125.46 s) - Coupure Sèche (The Vacuum Cut)** :
   - Tous les instruments (batterie, basse saturée, synthétiseurs en arpeggio) sont brutalement mutés sur un quart de temps.
   - Ne subsiste qu'un léger souffle de bande analogique (room tone).
   - *À l'écran* : La chanteuse se fige devant une porte close de laboratoire fermée par du ruban de sécurité ("DANGER : DO NOT ENTER").
2. **Frame 3788 (126.25 s) - Note Suspendue Isolée (The Solitary Strum)** :
   - Un accord unique de piano droit acoustique non réverbéré résonne dans le silence (durée d'extinction : 450 ms).
   - *À l'écran* : La poignée de la porte s'abaisse au ralenti, la lumière fuit par l'interstice.
3. **Frame 3810 (127.00 s) - Détonation Tutti (The Explosive Drop)** :
   - Reprise simultanée du kick, de la basse en distorsion fuzz, de la voix en cri d'octave supérieure et d'un sub-bass drop 808.
   - *À l'écran* : Flash blanc stroboscopique de 2 frames, explosion du mot géant `SHOW` en jaune cadmium et rouge néon, déploiement des 4 mascottes en formation symétrique.

#### Suspension d'Extinction Finale (Frames 4208 à 4247 / 140.25 s à 141.57 s)
- Atténuation progressive des fréquences aiguës par filtre passe-bas résonant (cutoff sweep 20 kHz vers 300 Hz).
- Un dernier cliquetis mécanique d'interrupteur électrique coupe le signal à la frame 4240.

---

### 5. Synoptique Audio vers Image (Mapping Événementiel Frame-Accurate)

| Intervalle Frames | Horodatage | Événement Sonore Dominant | Événement Visuel & Motion Design | Règle de Synchronisation |
| :--- | :--- | :--- | :--- | :--- |
| **0 - 50** | 00:00.00 | Intro chiptune 8-bit solo | Logo de démarrage, apparition du widget `P(DOOM)` | Synchro sur note lead |
| **150 - 200** | 00:05.00 | Riff de guitare crunch + crash cymbale | Déploiement élastique des rubans washi tape roses | Spring déclenché sur le crash |
| **301 - 351** | 00:10.03 | Entrée du beat Kick / Snare + Chant | Cut sur la chanteuse au bureau, mouvement de tête | Head-bob calé sur le kick (12.5f) |
| **601 - 651** | 00:20.03 | Bruitages de clavier mécanique rapide | Défilement vertical du code Lean 4, tampons verts | 1 caractère / 3 frames (double croche) |
| **952 - 1002** | 00:31.73 | Snare roll ascendant en doubles croches | Zoom caméra avant rapide vers l'écran | Accélération exponentielle du zoom |
| **1103 - 1153** | 00:36.78 | Balayage de filtre synthé montant | Entrée du chœur des 4 mascottes fleurs | Rebond vertical sur chaque noire |
| **1203** | 00:40.10 | Coup de sifflet d'arbitre strident | Mascotte brandit le carton rouge `FAIL` | Déclenchement frame 1203 pile |
| **1504 - 1554** | 00:50.13 | **DROP 1** : Kick massif + Sub-boom + Tutti | Flash stroboscopique 2f, explosion typographique `AGI` | Impact percussif = cut + échelle 150% |
| **1752 - 1802** | 00:58.40 | Ligne de synthé glissando descendante | Mascotte glissant sur la courbe de perte SVG | Position liée à la hauteur de note |
| **2103 - 2153** | 01:10.10 | Bip sonar et bruit blanc thermique | Bascule en palette inversée infrarouge | Cut chromatique sur le temps fort |
| **2307 - 2357** | 01:16.90 | Couplet 2 : Basse slap percutante | Chanteuse debout sur la chaise, kick caméra | Zoom-out sur chaque coup de basse |
| **2553 - 2603** | 01:25.10 | Cliquetis de roue à rochet d'odomètre | Roulement rapide des chiffres FLOPs $10^{30}$ | Rotation tambours asservie au tempo |
| **2854 - 2904** | 01:35.13 | Arpège synthé en cascade descendante | Inondation exponentielle de trombones | Multiplicateur de spawn x1.11 / frame |
| **3109 - 3159** | 01:43.65 | Pré-refrain 2 : Balayage stéréo du chant | Balancement alternatif gauche-droite de la caméra | Oscillation sinusoïdale sur 2 bars (100f)|
| **3764 - 3809** | 02:05.46 | **SILENCE COMPLET (Hang Time)** | Chanteuse immobile devant la porte close | Gel total des mouvements (0 px/frame) |
| **3810 - 3860** | 02:07.00 | **DROP CLIMAX** : Explosion sonore tutti | Flash stroboscopique, typographie `SHOW` géante | Shake caméra 24px + échelle 120% |
| **4050 - 4100** | 02:15.00 | Solo de guitare envolée lyrique | Chanteuse en plein saut héroïque avec le câble | Élongation vectorielle sur les notes tenues |
| **4210 - 4247** | 02:20.33 | Extinction par filtre résonant + switch off | Fondu au noir avec trame risographe rémanente | Fade-out opacité lié au volume audio |

---

### 6. Formules et Helpers de Synchronisation pour Codeurs (Remotion)

Pour garantir une synchronisation automatique mathématiquement exacte dans Remotion, voici la boîte à outils TypeScript de référence :

```typescript
// AudioSyncUtils.ts

export const AUDIO_CONSTANTS = {
  BPM: 143.55,
  FPS: 30.0,
  FRAMES_PER_BEAT: (30.0 * 60) / 143.55, // 12.539185 frames
  FRAMES_PER_BAR: ((30.0 * 60) / 143.55) * 4, // 50.15674 frames
};

/**
 * Renvoie l'indice de beat absolu (flottant ou entier) à une frame donnée.
 */
export function getBeatAtFrame(frame: number): number {
  return frame / AUDIO_CONSTANTS.FRAMES_PER_BEAT;
}

/**
 * Renvoie la frame absolue la plus proche correspondant au début d'un beat donné.
 */
export function getFrameAtBeat(beatIndex: number): number {
  return Math.round(beatIndex * AUDIO_CONSTANTS.FRAMES_PER_BEAT);
}

/**
 * Renvoie la frame absolue du début de la mesure (bar) donnée (base 0).
 */
export function getFrameAtBar(barIndex: number): number {
  return Math.round(barIndex * AUDIO_CONSTANTS.FRAMES_PER_BAR);
}

/**
 * Calcule un coefficient d'impact percussif (bounce / bump) amorti
 * qui se déclenche à chaque noire (beat) pour animer l'échelle ou le pompage d'une caméra.
 * Valeur retournée : entre 1.0 (repos) et (1.0 + intensity).
 */
export function getBeatPulse(
  frame: number,
  intensity = 0.08,
  decayRate = 0.35
): number {
  const beatProgress = (frame % AUDIO_CONSTANTS.FRAMES_PER_BEAT) / AUDIO_CONSTANTS.FRAMES_PER_BEAT;
  // Décroissance exponentielle à partir du début de chaque beat
  const pulse = Math.exp(-beatProgress * (decayRate * 10));
  return 1.0 + pulse * intensity;
}

/**
 * Détermine si la frame actuelle se situe dans la fenêtre critique de Hang Time (Silence pré-drop).
 */
export function isHangTimeFrame(frame: number): boolean {
  return frame >= 3764 && frame < 3810;
}
```

---

### Synthèse pour l'Intégration Sonore & Mixage Final
1. **Équilibrage de la dynamique (Loudness Targets)** :
   - Voix principale : -14 LUFS, centrée, présence rehaussée à 3.5 kHz.
   - SFX Pop Riso (trombones, tampons, scotch) : crête à -6 dBFS avec panoramique dynamique suivant la position $(x, y)$ des éléments à l'écran.
   - Sous-basses d'impact (Sub-drops) : centrées, coupe-bas raide sous 30 Hz pour préserver la réserve de puissance dynamique.
2. **Mastering et synchronisation** : Aucun décalage de latence de lecture ne doit être toléré. Le buffer audio sous Remotion ou le player de rendu doit être configuré avec un offset de compensation à 0 ms.
