---
name: sonniss-catalog-audio-fx
description: Trouve et récupère des bruitages (SFX) dans la banque Sonniss GDC 2024 de Romain (609 WAV, 27,5 Go sur Google Drive) pour une composition HyperFrames, puis les pose comme pistes `<audio>` calées sur la musique. À utiliser dès qu'une scène, un teaser ou une vidéo a besoin d'un son autre que la musique, même sans le mot « Sonniss » - whoosh, impact, boom, montée, braam, stinger, clic d'interface, glitch, ambiance, bruitage, sound design, « il me faut un son de… », « ajoute un effet sonore sur le titre », « ça manque de punch à 14 s ». Pas pour générer une musique (c'est Lyria, voir `motion-context`), ni pour régler le mix une fois les pistes posées (c'est `/hyperframes:hyperframes-audio`).
---

# Banque de bruitages Sonniss GDC 2024

La banque vit sur `gdrive:sound-fx/GDC2024/` (rclone). On ne fouille jamais Drive : tout se cherche dans l'index local, et on ne télécharge que les sons retenus.

- `references/index.tsv` : une ligne par son. Colonnes `cat_id` (catégorie UCS, vide pour 280 sons), `pack`, `name`, `duration_s`, `channels`, `sample_rate`, `bits`, `size_mb`, `path` (chemin Drive).
- `references/ucs-categories.md` : ce que veulent dire les préfixes (`WHSH`, `DSGNBoom`, `UIClick`…) et à quoi ils servent en motion. À lire quand la demande est floue (« un truc qui claque sur le titre »).

## 1. Chercher

Les noms sont en anglais. Traduire l'intention de Romain en plusieurs mots anglais, synonymes compris, et viser une catégorie quand elle est évidente :

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/sonniss-catalog-audio-fx"
bun $S/scripts/search.ts whoosh fast swoosh --max 3
bun $S/scripts/search.ts impact boom hit --cat DSGN
bun $S/scripts/search.ts rise riser tension build --min 3 --max 12
bun $S/scripts/search.ts --cat UI --limit 20
```

Le score `[2/3]` compte les mots trouvés. Les durées filtrent beaucoup : un whoosh fait moins de 3 s, une montée 3 à 12 s, une ambiance dépasse souvent la minute (on la coupera). Si rien ne sort, élargir les synonymes avant de conclure que la banque n'a pas ce son : 609 sons, c'est riche mais pas infini, et le dire franchement vaut mieux qu'un son à côté.

Proposer 3 à 5 candidats avec leur durée et ce qui les distingue (le nom en dit souvent long : `Heavy`, `Airy`, `Fast`, `Low`). Romain choisit à l'oreille, pas sur le nom.

## 2. Récupérer et faire écouter

```bash
bash $S/scripts/fetch.sh <projet HyperFrames> "<path>" ["<path>"…]
afplay "<projet>/assets/sfx/<fichier>.wav"
```

Les fichiers arrivent dans `<projet>/assets/sfx/`, à côté de l'`index.html` de la composition. Télécharger les 3 à 5 candidats d'un coup coûte peu (la plupart pèsent quelques Mo) et permet de les comparer. Une fois le choix fait, mettre les recalés à la Corbeille (`trash`) pour garder le projet léger.

Une ambiance de plusieurs minutes se coupe avant de la poser, sinon elle alourdit le projet :

```bash
ffmpeg -ss 12 -t 6 -i assets/sfx/long.wav -c:a pcm_s24le assets/sfx/long-cut.wav
```

## 3. Poser dans la composition

HyperFrames mixe lui-même toutes les pistes `<audio>` de la composition, en preview comme au rendu. Pas de pré-mix ffmpeg : chaque bruitage retenu devient une piste à part, calée par son `data-start` (en secondes).

Les instants viennent de la musique. `npx hyperframes beats <projet> --json` analyse la piste marquée `data-timeline-role="music"` et donne ses temps. Un impact tombe sur un drop ; un whoosh démarre environ 0,2 s avant une coupe pour arriver pile dessus.

```html
<audio id="music" src="assets/music.mp3" data-timeline-role="music"
       data-start="0" data-track-index="10" data-volume="1"></audio>

<audio id="sfx-whoosh-title" src="assets/sfx/whoosh.wav"
       data-start="3.8" data-track-index="11" data-volume="0.7"></audio>
<audio id="sfx-boom-drop" src="assets/sfx/boom.wav"
       data-start="14.13" data-track-index="11" data-volume="0.9"></audio>
```

- **Chaque `<audio>` a un `id`.** Sans `id`, le mixeur ne la voit pas et le rendu est muet sur ce son (`lint` le signale : `media_missing_id`).
- Un `id` qui dit le rôle et l'instant (`sfx-boom-drop`) rend la timeline lisible dans le Studio.
- Les bruitages vont sur leur propre `data-track-index`, séparé de la musique : une piste par sorte d'élément.
- `data-duration` peut être omis pour un son court joué en entier. On le met pour couper une ambiance longue sans la retailler.
- Jamais d'attribut `crossorigin` sur un `<audio>` : `lint` le refuse.

Le réglage fin (fondu, limiteur quand un impact tombe sur un kick, ducking de la musique) se fait avec `/hyperframes:hyperframes-audio`, via `data-fx-chain` et `data-automation` sur la piste.

Vérifier avec `npx hyperframes lint` puis à l'écoute du rendu, autour des instants posés. Faire écouter un extrait à Romain : c'est lui qui juge si le son tombe juste.

## Si rclone refuse

`couldn't fetch token: invalid_grant` : le jeton Drive a expiré. Romain doit lancer `rclone config reconnect gdrive:` dans un Terminal à part (c'est interactif, ça ouvre le navigateur). Ne pas tenter de contourner.

## Mettre l'index à jour

L'index est une copie de `~/dev/EROM-HQ/lab/sonniss-drive/index.tsv`, produit par `bun build-index.ts` dans ce dossier (il ne lit que l'en-tête des WAV sur Drive). Si la banque grandit (GDC 2025…), régénérer là-bas puis recopier ici.
