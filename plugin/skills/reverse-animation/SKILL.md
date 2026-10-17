---
name: reverse-animation
description: "Rétro-ingénierie d'une animation ou d'une interaction front-end à partir d'une vidéo (.mov, .mp4, .webm) : chorégraphie, propriétés animées, durées, stagger, easing (cubic-bezier, ease GSAP ou ressort), puis spec et code prêts à implémenter (CSS, GSAP, Framer Motion, HyperFrames). Combine le modèle vision Glimpse (elorian/glimpse via OpenRouter) pour comprendre ce qui bouge et une planche-contact mesurée image par image pour le timing. À utiliser dès qu'on veut reproduire, recréer, copier ou décortiquer un effet vu dans une capture d'écran animée, un enregistrement de site, un Dribbble, un hero, une carte qui s'ouvre, un menu, un hover, une transition de page, même sans dire « rétro-ingénierie » : « comment ils ont fait cette anim », « refais-moi cette transition », « utilise Glimpse sur cette vidéo ». Pas pour un bug d'UI ou un test e2e (c'est /erom-vision:glimpse-vision), ni pour créer une animation sans vidéo source (c'est /hyperframes:hyperframes)."
---

# Rétro-ingénierie d'animation

Glimpse voit la vidéo, Claude ne la voit pas. Mais Glimpse échantillonne environ une image par seconde : sur une animation de 800 ms, il voit au mieux une image en mouvement. La skill sépare donc les deux questions :

- **Qu'est-ce qui bouge, et comment ?** (éléments, propriétés, calques, effets) : Glimpse, sur un extrait ralenti.
- **Quand et à quelle vitesse ?** (début, durée, stagger, easing) : Claude, en mesurant une planche-contact à 20 images par seconde. Ces chiffres-là ne viennent jamais de Glimpse seul.

Recette du 2026-10-17 sur une vidéo témoin (deux cartes, translateY de 80 px, 800 ms, easeOutCubic, stagger 150 ms), qui fonde cette séparation :

| Entrée | Ce que Glimpse a rendu |
|---|---|
| Vidéo à vitesse réelle | Faux sur tout : un `scaleY` élastique depuis 0 avec 43 % de dépassement, cartes de 280 px de haut au lieu de 200, le tout marqué « mesuré ». |
| Ralenti x4 | Géométrie juste (300×200, 340 → 260 px, 80 px de course). Timing faux : 550 ms au lieu de 800, stagger 0 au lieu de 150 ms, easing **inversé** (ease-in au lieu d'ease-out), et une « bande de balayage » qui n'existe pas. |
| Ralenti x8 | Début (500 ms), stagger (150 ms) et sens de l'easing (ease-out) justes, course à 85 px. Durée encore fausse (450-500 ms au lieu de 800), famille d'easing fausse (`expo.out` au lieu de `power2.out`), et une « bande d'ombre » qui n'existe pas non plus. |
| Planche-contact 20 i/s lue par Claude | Stagger de 150 ms et décélération visibles à l'œil, à une case près (50 ms). |

Entrée brute :
$ARGUMENTS

## Prérequis

- `bun` et `ffmpeg` dans le PATH (`brew install ffmpeg`).
- `OPENROUTER_API_KEY` dans l'environnement. Vérifie sa présence avec
  `test -n "$OPENROUTER_API_KEY" && echo présente`, jamais en l'affichant.

Les fichiers de travail (extraits, planches, images) vont dans le scratchpad de la session, ou à défaut dans un dossier temporaire, jamais dans le projet de l'utilisateur.

## 1. Situer l'animation

```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of default=nw=1 <vidéo>
```

Si la vidéo dure plus de quelques secondes, repère la fenêtre où ça bouge avec une planche large (4 i/s) :

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/reverse-animation/scripts/contact-sheet.sh" <vidéo> 0 <durée> <work>/overview.jpg 4 6 240
```

Lis la planche (Read) et la table case → horodatage imprimée sur stdout. Le ffmpeg de Homebrew n'a pas `drawtext` : les horodatages ne sont pas incrustés, ils sont dans cette table.

Puis découpe l'extrait, avec 300 ms de marge de chaque côté :

```bash
ffmpeg -loglevel error -y -ss <début> -t <durée> -i <vidéo> -an <work>/clip.mp4
```

Les temps mesurés ensuite sont relatifs à l'extrait. Si l'utilisateur vise un élément (« la carte »), garde-le en tête pour toute la suite.

## 2. Comprendre avec Glimpse

```bash
bun "${CLAUDE_PLUGIN_ROOT}/skills/reverse-animation/scripts/glimpse.ts" <work>/clip.mp4 "<élément visé et contexte>" --stack "<cible>"
```

Timeout Bash de 400000 ms : un extrait de 2,5 s ralenti x8 en effort `high` a pris 77 s et 0,05 $. Le coût d'entrée croît avec la durée ralentie (17 k tokens pour ces 20 s) : c'est une raison de plus pour découper avant.

- **Question** : nomme l'élément et ce qu'on veut en faire. « L'animation d'ouverture de la carte produit, pour la refaire en GSAP dans le hero » oriente mieux que rien. Sans question, le script demande l'animation principale.
- **`--slowmo N`** (1 à 8, défaut 8) : ralentit l'extrait avant envoi et demande au modèle de rediviser les temps. Ne descends pas à 1 : la vitesse réelle est le cas qui a tout halluciné.
- **`--stack`** : la cible d'implémentation (`CSS + GSAP` par défaut). Pour une composition, `HyperFrames (timeline GSAP en pause, seek-safe)`.
- **`--effort`** : `high` par défaut.

La spec sort sur stdout, une ligne de métadonnées sur stderr (transcodage, durée, tokens, coût).

De ce rapport, garde comme hypothèses solides : quels éléments bougent, quelles propriétés (translation, scale, opacity, clip-path, flou), le sens du mouvement, les positions de départ et d'arrivée, l'ordre de superposition. Ses durées, son stagger et son easing ne sont qu'un premier jet que l'étape 3 confirme ou remplace. Tout effet secondaire qu'il décrit (bande, ombre, reflet, masque) se vérifie sur une image pleine résolution avant d'entrer dans la spec : il en a inventé un à chaque run de la recette, sur des cartes unies.

## 3. Mesurer le timing soi-même

Planche serrée sur la fenêtre de mouvement :

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/reverse-animation/scripts/contact-sheet.sh" <work>/clip.mp4 <début> <fin> <work>/sheet.jpg 20 6 320
```

20 i/s donne un pas de 50 ms ; monte à 30 pour une micro-interaction de moins de 300 ms (60 cases maximum). Pour chaque élément, relève sur la planche :

1. La première case où il a bougé et la première où il est arrivé : début et durée, à un pas près.
2. Le décalage de départ entre éléments : le stagger.
3. Sa position sur 4 à 6 cases intermédiaires, convertie en progression 0 → 1 de la course.

Pour un chiffre en pixels qui compte, extrais l'image pleine taille et mesure-la :

```bash
ffmpeg -loglevel error -y -ss <secondes> -i <work>/clip.mp4 -frames:v 1 -vf scale=900:-2 <work>/frame.jpg
```

Un JPEG réduit passe au Read ; un PNG pleine taille de plus de 1 Mo a été refusé.

### Reconnaître l'easing

Compare la progression mesurée à mi-durée et au quart de la durée à cette table (valeurs exactes des courbes, GSAP entre parenthèses) :

| Courbe | p à 25 % du temps | p à 50 % du temps |
|---|---|---|
| linéaire (`none`) | 0,25 | 0,50 |
| easeOutQuad (`power1.out`) | 0,44 | 0,75 |
| easeOutCubic (`power2.out`) | 0,58 | 0,88 |
| easeOutQuart (`power3.out`) | 0,68 | 0,94 |
| easeOutExpo (`expo.out`) | 0,82 | 0,97 |
| easeInCubic (`power2.in`) | 0,02 | 0,13 |
| easeInOutCubic (`power2.inOut`) | 0,06 | 0,50 |

Une progression qui dépasse 1 puis revient trahit un `back.out` ou un ressort : relève l'amplitude du dépassement et l'instant du pic. Si la course ne tient que sur trois cases, dis que l'easing est estimé, pas mesuré.

## 4. Livrer

Une spec en français, puis le code :

1. **Chorégraphie** : tableau élément par élément, début et fin en ms, stagger.
2. **Propriétés** : valeur de départ et d'arrivée de chaque propriété animée, `transform-origin` si scale ou rotation.
3. **Easing** : la courbe retenue, en cubic-bezier et en nom GSAP, avec les deux progressions mesurées qui la justifient.
4. **Code** dans la stack visée. Pour HyperFrames, passe la main à `/hyperframes:hyperframes-animation` avec la spec : la timeline doit rester en pause et seek-safe, le code « navigateur » de Glimpse (`gsap.to` au chargement) ne s'y pose pas tel quel.
5. **Confiance** : pour chaque valeur, sa source (planche, image pleine taille, Glimpse seul) et sa précision. Ce qui n'a pas pu être mesuré est dit comme tel.

Ne recopie pas le rapport Glimpse : il fait 8 Ko et contredit souvent la mesure. Cite-le seulement là où il apporte ce que la planche ne montre pas.

## Échecs

`glimpse.ts` sort avec un code non nul et un message `glimpse: …` sur stderr (clé absente, format non supporté, fichier trop lourd après transcodage, erreur OpenRouter, réponse vide). `contact-sheet.sh` refuse au-delà de 60 cases. Rapporte le message tel quel et l'action qu'il propose. Si Glimpse échoue, la planche suffit pour livrer une spec de timing ; dis que la lecture qualitative manque. Ne remplace jamais un rapport absent par une description inventée de la vidéo.
