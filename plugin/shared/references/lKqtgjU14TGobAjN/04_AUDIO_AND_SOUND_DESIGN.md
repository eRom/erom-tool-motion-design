# 04. Cartographie Audio & Sound Design (SFX)

Ce document analyse la bande sonore de `lKqtgjU14TGobAjN.mp4` (*CLAUDE / MOTION REEL '26*) sous l'angle du monteur et de l'ingénieur en motion design. L'objectif est de formaliser comment chaque élément sonore (pulsation métronomique, textures de bruitage, foley et silences) justifie, déclenche et propulse l'image pour un agent de fabrication logicielle.

---

## 1. Structure Rythmique & Asservissement Percussif

L'ensemble de la timeline (15.061s, 452 frames à 30 fps) est verrouillé sur une signature 4/4 à **129.2 BPM** (~130 BPM), articulée en **8 mesures musicales complètes** de 55.73 frames :

| Composant Percussif | Rôle de Déclenchement Visuel | Paramètre Moteur / Trigger de Code |
|---|---|---|
| **Kick (Grosse Caisse)**<br>(Temps 1 et 3) | **Impacts de masse & Snaps d'échelle** :<br>- Premier impact au sol de la balle (Frame 18)<br>- Snap d'entrée des mots monumentaux "EVERY" (Frame 55) et "DECISION." (Frame 82)<br>- Verrouillage de la 15e barre de données (Frame 215) | `const kickScale = 1 + 0.15 * Math.exp(-progress * 8);` |
| **Snare / Clap (Caisse Claire)**<br>(Temps 2 et 4) | **Cuts de substitution & Ruptures de forme** :<br>- Remplacement mot-à-mot "FRAME" (Frame 69) et "IS A" (Frame 74)<br>- Amorces des vagues de morphing matriciel (Frame 121 et Frame 146)<br>- Transition en volet biseauté (Frame 175) | `const isSnareHit = frame % framesPerBeat === 0;` |
| **Hi-Hats & Doubles-Croches**<br>(Pulsation continue 1/16) | **Micro-animations télémétriques HUD & Rotation** :<br>- Pas d'incrémentation de l'odomètre numérique `0` à `450`<br>- Rotation continue des fiches du carrousel 3D ($2.2^\circ/\text{frame}$)<br>- Cadence de frappe de la machine à écrire (1 char / 2 frames) | `const charIndex = Math.floor(frame / 2);` |
| **Basse Électro-Glitch (Synth Bass)** | **Ondes de déformation & Trajectoires continues** :<br>- Ondulation concentrique de la matrice de disques (`distToCenter * 0.012`)<br>- Course curviligne du traceur `expo.out`<br>- Dilatation de l'onde de choc circulaire radar (Frame 355) | `const waveRadius = progress * 700;` |

---

## 2. Typologie des SFX (Sound Effects)

Le sound design combine un groove électro-minimaliste clinique et un ensemble de bruitages concrets (Foley) synchronisés à la frame près :

### 2.1. Foley d'Impact & Rebond (Organic / Physical Foley)
- **Occurrences** :
  - `00:00.60` (Frame 18) : Thump sourd feutré couplé à une impulsion sub-bass lors du premier contact de la balle avec la ligne de sol.
  - `00:01.27` (Frame 38) : Pop d'impact amorti plus aigu et 40% moins puissant, signalant la dissipation d'énergie.
- **Règle de synchronisation** : L'attaque du son d'impact coïncide exactement avec la frame où la coordonnée $Y$ de la balle atteint son minimum ($Y = 705px$) et où le ratio $H/W$ atteint sa valeur d'écrasement maximale.

### 2.2. Risers & Balayages de Pression (Sub-Risers & Whooshes)
- **Occurrences** :
  - `00:01.50 - 00:01.80` (Frames 45 à 54) : **Sub-riser crescendo** montant en fréquence et en saturation pendant l'expansion exponentielle de la balle, débouchant sur le cut franc plein écran.
  - `00:05.83` (Frame 175) : **Whoosh tranchant de volet biseauté** accompagnant le passage de la lame noire de droite à gauche.
  - `00:09.00` (Frame 270) : Balayage Doppler stéréo accompagnant le déploiement spatial du carrousel 3D.
- **Règle de synchronisation** : Le pic d'amplitude du whoosh anticipe le franchissement de la ligne médiane de l'écran par l'objet mobile de 2 frames.

### 2.3. Bruitages Télémétriques & Clics UI (Digital Feedback)
- **Occurrences** :
  - `00:03.10` (Frame 100) : Clic d'ouverture de console au retour sur le fond crème et l'apparition de la grille.
  - `00:06.03 - 00:07.13` (Frames 181 à 214) : Crépitement haute fréquence de compte-tours numérique calé sur l'emballement de l'odomètre de `0` à `450`.
  - `00:08.67` (Frame 260) : Bip de verrouillage à l'arrivée conjointe des deux billes à la coordonnée $(1.0, 1.0)$.

### 2.4. Dactylographie Mécanique & Foley d'Interface
- **Occurrences** :
  - `00:13.03 - 00:13.80` (Frames 391 à 414) : Séquence de frappes sèches de touches de clavier mécanique à cadence ultra-rapide (style *cherry MX blue*), chaque frappe déclenchant l'apparition d'un caractère du texte `MOTION DESIGNER · REEL 2026`.
  - `00:13.83` (Frame 415) : Clic mécanique de retour de chariot marquant la fin de la ligne et l'arrêt du curseur bloc.

### 2.5. Résonance Harmonique & Sub-Drop Terminal
- **Occurrences** :
  - `00:11.83` (Frame 355) : Onde de sub-bass pure marquant la dislocation du carrousel et l'émission de l'onde circulaire radar.
  - `00:14.00 - 00:15.06` (Frames 420 à 452) : Accord de synthétiseur chaud en nappe avec longue réverbération feutrée, soutenant la pose finale de l'identité Claude jusqu'à la fin de la vidéo.

---

## 3. Gestion du Vide, Silences & Suspension (Hang Time)

L'impact visuel et l'élégance du film résultent directement de son usage mesuré des micro-silences et des points de suspension dynamique :

### 3.1. Le Silence d'Apex (Frame 28, `00:00.93`)
- **Mécanisme** : Au sommet de la parabole de vol de la balle, lorsque $dy/dt = 0$, la bande sonore retire tout transitoire percussif pour laisser flotter un souffle feutré.
- **Effet visuel** : La suspension physique de la balle est acoustiquement prolongée dans l'esprit du spectateur, valorisant la perfection du cercle non déformé ($H/W = 1.00$).

### 3.2. L'Anticipation Pré-Explosion (Frames 42 à 44, `00:01.40`)
- **Mécanisme** : Dès que la balle se pose au sol, le son coupe net tout bruitage d'impact pendant 3 frames.
- **Effet visuel** : Ce micro-silence crée une tension dramatique immédiate, faisant ressentir la compression énergétique qui libère le gonflement exponentiel à la frame 45.

### 3.3. Le Hold Statique Final (Frames 445 à 452, `00:14.83`)
- **Mécanisme** : Tout rythme percussif s'arrête. Seule la queue de réverbération du synthétiseur s'éteint doucement, sans aucun cut brutal ni effet de fade-out artificiel.
- **Effet visuel** : Confère au projet une autorité technique sereine : la composition est stable, équilibrée, et n'a pas besoin d'artifice de sortie.

---

## 4. Tableau Synoptique Audio $\to$ Image (Plan par Plan)

| Timestamp | Cue Musical / Rythme | Événement SFX Dominant | Action Graphique Asservie | Déclencheur Code (Trigger) |
|---|---|---|---|---|
| `00:00.00 - 00:00.40` | Ambiance sourde | Clic d'activation | Initialisation du Viewfinder HUD et de la ligne de sol | `frame === 0` |
| `00:00.43 - 00:00.57` | Descente silencieuse | Souffle de vélocité | Chute de la balle & étirement vertical $H/W = 1.52$ | `stretch = 1 + 0.52 * progress` |
| `00:00.60` (Frame 18) | **Kick lourd (Temps 1)** | **Thump d'impact sourd** | Écrasement squash maximal $H/W = 0.38$ sur la ligne de sol | `squashFactor = Math.sin(t * Math.PI)` |
| `00:00.93` (Frame 28) | **Creux d'énergie** | Silence de suspension | Apex de la parabole, retour à la forme sphérique pure | `y === 380 && scaleX === 1` |
| `00:01.27` (Frame 38) | Battement feutré | Pop d'impact amorti | Second écrasement amorti $H/W = 0.59$ | `dissipation = 0.6` |
| `00:01.50 - 00:01.80` | **Montée rythmique** | **Sub-riser crescendo** | Gonflement exponentiel de la balle vers fond plein | `radius = r0 * Math.exp(0.34 * t)` |
| `00:01.83` (Frame 55) | **Kick 1 Mesure 2** | Impact plein écran | Snap-in du mot "EVERY" sur fond terracotta | `text = "EVERY"` |
| `00:02.30` (Frame 69) | Snare sèche | Clac de percussion | Substitution instantanée par "FRAME" | `text = "FRAME"` |
| `00:02.47` (Frame 74) | Hi-hat ouvert | Clic percussif | Substitution instantanée par "IS A" | `text = "IS A"` |
| `00:02.73` (Frame 82) | **Snare lourde** | **Impact de clôture** | Apparition de "DECISION." avec point final | `text = "DECISION."` |
| `00:03.10` (Frame 100) | **Drop du Beat 129.2 BPM** | Clic d'interface console | Cut vers fond crème, filigrane "RHYTHM" & grille de points | `scene = 2` |
| `00:04.03` (Frame 121) | Snare syncopée | Ondulation FM filtrée | Lancement de la vague de morphing : disques $\to$ carrés | `wave1Progress > 0` |
| `00:04.87` (Frame 146) | Double-croche hi-hat | Frémissement de filtre | Lancement de la seconde vague : carrés $\to$ bâtonnets vectoriels | `wave2Progress > 0` |
| `00:05.83` (Frame 175) | **Temps 4 Mesure 4** | **Whoosh tranchant de volet** | Passage du volet biseauté noir/terracotta de droite à gauche | `wipeProgress = ease(t)` |
| `00:06.03 - 00:07.13` | Beat en marche | Crépitement d'odomètre | Emballement du compteur `0` à `443` et montée des 15 barres | `count = 450 * easeExpo(t)` |
| `00:07.17 - 00:08.67` | Ligne de basse modulée | Sifflement d'accélération | Course des deux billes traceuses (`expo.out` vs `linear`) | `raceProgress = t / 40` |
| `00:08.67` (Frame 260) | Percussion de synchronisation | Bip de verrouillage $(1.0, 1.0)$ | Jonction simultanée des deux billes sur le point cible | `raceProgress === 1.0` |
| `00:09.03` (Frame 270) | **Début Mesure 6** | **Balayage Doppler 3D** | Déploiement spatial du carrousel octogonal de fiches | `perspective = 1200px` |
| `00:09.83` (Frame 295) | Snare avec réverbe | Clic typographique lourd | Apparition du manifeste inférieur `EASE IS EMOTION.` | `opacity = 1` |
| `00:11.83` (Frame 355) | **Sub-drop feutré** | **Onde radar acoustique** | Dissolution du carrousel & onde circulaire expansive `#E0876E` | `waveRadius = progress * 700` |
| `00:12.00` (Frame 360) | Temps 1 Mesure 7 | Clic d'assemblage magnétique | Convergence des 6 branches de l'astérisque Claude au centre | `easeAssemble = 1 - 2^(-10t)` |
| `00:12.43` (Frame 373) | Glissement filtré | Son de translation pneumatique | Glissement de l'astérisque vers la gauche & entrée de "CLAUDE" | `translateX = -534 * ease(t)` |
| `00:13.03` (Frame 391) | **Reprise staccato** | **Frappes de machine à écrire** | Tracé du filet terracotta & saisie de `MOTION DESIGNER · REEL 2026` | `charsCount = t / 1.5` |
| `00:13.83` (Frame 415) | Clôture percussive | Clic de fin de ligne | Immobilisation du curseur & fondu de la tagline inférieure | `cursorBlink = true` |
| `00:14.00 - 00:15.06` | Nappe de synthé chaude | Résonance harmonique longue | Hold final stabilisé sur `TC 00:00:15:02` (Frame 450) | `hold = true` |
