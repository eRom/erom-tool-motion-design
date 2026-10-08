# 04. Cartographie Audio & Sound Design Technique

Ce document décortique la bande sonore de `PRWfsEy-zcoo2ao_.mp4` sous le prisme du monteur et de l'ingénieur en motion design. Dans cette production, la piste sonore n'est pas un simple accompagnement d'ambiance : elle constitue l'horloge maîtresse absolue qui cadence, propulse et justifie chaque cut, transformation géométrique et apparition typographique.

---

## 1. Structure Rythmique & Horloge Maîtresse

### 1.1. Constantes Musicales

- **Tempo (BPM)** : **152.0 BPM** constant (mesure 4/4, électronique uptempo).
- **Période d'un temps (Beat - noire)** : `0.3947 seconde` = **11.84 frames** à 30 fps (arrondi métronome : alternance stricte 12 frames / 12 frames / 12 frames / 11 frames).
- **Période d'une mesure (Bar 4/4)** : `1.5789 seconde` = **47.37 frames** (~47-48 frames).
- **Période d'une phrase musicale standard (4 mesures)** : `6.3158 secondes` = **189.47 frames** (~190 frames).

### 1.2. Grille d'Asservissement Audio-Visuel

La batterie obéit à un schéma classique "Four-on-the-floor" électro-funk / chiptune moderne :
- **Kick (Grosse caisse)** : Battements sur les temps 1, 2, 3 et 4. Chaque impact de kick déclenche un micro-zoom de caméra ou une impulsion d'échelle (`scale: 1.0 -> 1.04 -> 1.0` sur 4 frames) sur les objets au premier plan.
- **Snare (Caisse claire claquante)** : Battements renforcés sur les temps 2 et 4. La quasi-totalité des cuts staccato et des arrivées de titrages cinétiques tombent sur le snare, garantissant une netteté d'impact maximale.
- **Hi-Hats (Charlestons en doubles croches à 16th-notes)** : Défilement continu rapide qui entraîne les particules (vortex de feuilles de papier, pluie Matrix, étincelles du lance-flammes).
- **Basse Synthétique Sidechainée** : Basse ronde compressée en ducking à chaque coup de kick, créant une respiration dynamique qui évite la saturation acoustique.

---

## 2. Typologie des Sound Effects (SFX)

L'inventaire sonore utilise une palette de bruitages d'animation de haute précision :

| Famille SFX | Descripteur Acoustique | Rôle Fonctionnel dans l'Animation | Exemples dans la Timeline |
|---|---|---|---|
| **Risers & Sweeps** | Montée en fréquence (pitch sweep) de bruit blanc filtré passe-haut | Création de tension juste avant un cut ou un changement de chapitre | `00:02.00 - 00:02.40` (pré-reveal Clawd), `00:40.80 - 00:41.60` (pré-staccato) |
| **Impacts / Sub-Drops** | Explosion grave transitoire (< 60 Hz) couplée à un clap métallique | Sanctionne l'arrivée d'une scène majeure ou d'un grand titre | `00:06.40` (drop CODE), `00:25.60` (drop DEBUG), `00:41.60` (slam staccato) |
| **Glitch & Cyber Bleeps** | Tonalités sinusoïdales courtes en modulation FM et bruits 8-bit | Matérialise les opérations logicielles et l'activation des sous-agents | `00:07.20 - 00:12.80` (apparition des 12 cartes agents, bips de validation) |
| **Foley Matériel Organique** | Froissements de feuilles, glissement de papier, frottement de tissu | Humanise le monde analogique (WRITE et RESEARCH) en contraste avec le cyber | `00:13.60` (vortex de feuilles), `00:20.00` (déroulement du rouleau parchemin) |
| **Foley Mécanique & Cartoon** | Cliquetis de clavier mécanique, ressorts comiques, sifflet de fuite | Rythme les micro-actions du personnage et accentue l'humour | `00:29.60` (petit drapeau blanc sur cure-dent), `00:44.20` (pile de chapeaux vacillante) |
| **Whooshes Aigus** | Bruit de souffle court (durée 4 à 6 frames) avec panoramique stéréo | Accompagne les volets biseautés et les essuyages de caméra (wipes) | `00:32.07` (wipe cyan ANALYZE), `00:38.40` (wipe rose DESIGN) |
| **Chimes & Shimmers** | Carillon cristallin aigu en arpège ascendant | Souligne l'achèvement réussi et le clin d'œil final | `00:43.20` (100% chart data), `00:47.80` (clin d'œil de Clawd `- ^`) |

---

## 3. Gestion du Vide & Suspensions (Hang Time)

L'efficacité du motion design réside dans le contraste dynamique : les moments de surcharge sensorielle sont systématiquement précédés ou suivis d'une décompression acoustique (micro-silences ou "hang time").

1. **Le Creux d'Énergie Pré-Drop CODE (`00:05.83 - 00:06.40`)** :
   - À la fin de la présentation du titre "DUAL MODE", la rythmique s'éteint brutalement pendant 17 frames (environ 0.5 seconde).
   - Seule subsiste une note de synthétiseur tenue qui s'interrompt net à F0190 (2 frames de silence numérique total).
   - Résultat visuel : Le flash vert et le drop lourd à `00:06.40` frappent avec 200% plus d'impact que si la boucle de batterie avait continué sans interruption.

2. **La Respiration d'Armement DEBUG (`00:25.20 - 00:25.60`)** :
   - Suspension de 12 frames juste avant la déflagration du lance-flammes : coupure de la ligne de basse, seul le cliquetis d'une vanne de gaz se fait entendre avant l'embrasement.

3. **Le Silence Comique du Drapeau Blanc (`00:29.20 - 00:29.60`)** :
   - Le rugissement du jet de flamme s'arrête net. Silence soudain de 12 frames pendant que la fumée se dissipe, juste avant le petit son cartoon `pop` du drapeau blanc agité par le bug rescapé.

4. **Le Grand Break Pré-Climax (`00:41.00 - 00:41.60`)** :
   - Rupture totale de la batterie pendant 18 frames avant la mitraillade staccato des 6 rôles. L'oreille est remise à zéro pour encaisser les 6 impacts métronomiques à venir.

5. **L'Afterglow Final (`00:44.00 - 00:51.24`)** :
   - Après la tension frénétique du récapitulatif staccato, la musique retombe dans un arpège doux et aéré à tempo apaisé, permettant d'apprécier la pose comique de Clawd avec sa pile de 7 chapeaux.

---

## 4. Tableau Synoptique Audio -> Image

Correspondance rigoureuse plan par plan entre l'événement sonore, l'action cinématique à l'écran et la variable logicielle de déclenchement (trigger) :

| Timecode & Frames | Événement Sonore Majeur | Action Visuelle Synchronisée | Déclencheur Code (Trigger Logiciel) |
|---|---|---|---|
| **00:00.00** (F0000) | Attaque Kick 1 + Click | Pop-in icône 01 Terminal CODE | `triggerPopIn({ id: 'code', scale: [0.8, 1.0] })` |
| **00:00.40** (F0012) | Snare 1 + Whoosh | Pop-in icône 02 Plume WRITE | `switchScene({ id: 'write', color: '#A6ACDC' })` |
| **00:00.80** (F0024) | Kick 2 + Bruit page | Pop-in icône 03 Livre RESEARCH | `switchScene({ id: 'research', color: '#B6CBEA' })` |
| **00:01.20** (F0036) | Snare 2 + Double-tick | Pop-in icône 04 Coccinelle DEBUG | `switchScene({ id: 'debug', color: '#AEA09D' })` |
| **00:01.60** (F0048) | Kick 3 + Tintement | Déploiement colonnes 05 ANALYZE | `animateBars({ stagger: 2, scaleY: [0, 1] })` |
| **00:02.03** (F0061) | Snare 3 + Riser court | Trait peinture rose 06 DESIGN | `strokeBrush({ path: 'wave', duration: 11 })` |
| **00:02.40** (F0072) | Riser Shōnen montant | Flash blanc + Speed lines radiales | `setSpeedLines({ active: true, zoomZ: [12, 3.8] })` |
| **00:03.20** (F0096) | Impact Kick lourd + Basse | Split Screen DUAL MODE + Mascotte | `setSplitScreen({ active: true, angle: 65 })` |
| **00:05.83** (F0175) | Coupure rythmique (Silence) | Clawd fige sa pose, attente | `pauseAnimation({ holdFrame: true })` |
| **00:06.40** (F0192) | Sub-drop + Flash audio | Flash vert Matrix + Inversion manga | `triggerFlash({ color: '#00FF66', frames: 24 })` |
| **00:07.20** (F0216) | Groove complet + Bips claviers | Entrée scène 3D CODE + Pluie Matrix | `startMatrixRain({ density: 60, speed: 1.0 })` |
| **00:12.80** (F0384) | Glitch + Swoosh papier | Flash rose + Transition WRITE | `triggerFlash({ color: '#FF007F', frames: 24 })` |
| **00:13.60** (F0408) | Battements de feuilles + Kick | Vortex de 90 feuilles de papier 3D | `startVortex({ count: 90, turbulence: 1.5 })` |
| **00:19.20** (F0576) | Synth stab + Tintement livre | Flash jaune + Transition RESEARCH | `triggerFlash({ color: '#FFE500', frames: 24 })` |
| **00:20.00** (F0600) | Claviers rapides + Bips d'onglets | Tours de livres montantes + Badge tabs | `animateCounter({ from: 3, to: 847, dur: 48 })` |
| **00:25.60** (F0768) | Déflagration sourde + Allumage gaz | Flash rouge + Transition DEBUG | `triggerFlash({ color: '#FF2200', frames: 24 })` |
| **00:26.40** (F0792) | Rugissement flammes volumétriques | Jet de flammes continu + Fuite bugs | `startFlamethrower({ active: true, shake: 8 })` |
| **00:29.60** (F0888) | Arrêt flamme + Pop cartoon | Drapeau blanc brandi par le bug | `showSurrenderFlag({ springDamping: 12 })` |
| **00:32.07** (F0962) | Whoosh laser cyan | Volet géométrique oblique ANALYZE | `startWipe({ angle: 30, color: '#00E5FF' })` |
| **00:32.80** (F0984) | Arpège synthé + Pulsation radar | Colonnes 3D animées en égaliseur | `bindEqualizerToAudio({ fftBins: 32 })` |
| **00:38.40** (F1152) | Accord piano + Bruit de brosse | Volet oblique rose DESIGN | `startWipe({ angle: 45, color: '#FF007F' })` |
| **00:39.20** (F1176) | Éclaboussures + Rythme joyeux | Déploiement rubans de peinture 3D | `extrudePaintRibbons({ progress: [0, 1] })` |
| **00:41.60** (F1248) | Kick 1 Staccato + Cloche `Ding!` | CODE : 12 checkmarks verts `✓` | `staccatoStep({ index: 1, text: 'CODE' })` |
| **00:42.00** (F1260) | Snare 1 Staccato + Tampon lourd | WRITE : Coup de tampon `THE END` | `staccatoStep({ index: 2, text: 'WRITE' })` |
| **00:42.40** (F1272) | Kick 2 Staccato + Défilement rapide | RESEARCH : Rouleau infini défilant | `staccatoStep({ index: 3, text: 'RESEARCH' })` |
| **00:42.80** (F1284) | Snare 2 Staccato + Sifflement | DEBUG : Bug avec drapeau blanc | `staccatoStep({ index: 4, text: 'DEBUG' })` |
| **00:43.20** (F1296) | Kick 3 Staccato + Flash d'énergie | ANALYZE : Colonnes à 100% zénith | `staccatoStep({ index: 5, text: 'ANALYZE' })` |
| **00:43.60** (F1308) | Snare 3 Staccato + Splash final | DESIGN : Chef-d'œuvre illuminé | `staccatoStep({ index: 6, text: 'DESIGN' })` |
| **00:44.00** (F1320) | Break musical + Décompression | Pullback sur Clawd et 7 chapeaux | `revealMultiHatClawd({ spring: true })` |
| **00:47.80** (F1434) | Tintement féerique `Twinkle!` | Clin d'œil malicieux de Clawd (`- ^`) | `triggerWink({ eye: 'left', duration: 10 })` |
| **00:49.23** (F1477) | Accord synthétique final soutenu | Packshot final DUAL MODE biseauté | `renderFinalPackshot({ fadeOutTail: true })` |
