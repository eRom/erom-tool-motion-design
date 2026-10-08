---
name: sonniss-catalog-audio-fx
description: Trouve et récupère des bruitages (SFX) dans la banque Sonniss GDC 2024 de Romain (609 WAV, 27,5 Go sur Google Drive) pour une scène motion design, puis les mixe à la musique pour qu'ils s'entendent au rendu. À utiliser dès qu'une scène, un teaser ou une vidéo a besoin d'un son autre que la musique, même sans le mot « Sonniss » - whoosh, impact, boom, montée, braam, stinger, clic d'interface, glitch, ambiance, bruitage, sound design, « il me faut un son de… », « ajoute un effet sonore sur le titre », « ça manque de punch à 14 s ». Pas pour générer une musique (c'est `motion music` / Lyria).
---

# Banque de bruitages Sonniss GDC 2024

La banque vit sur `gdrive:sound-fx/GDC2024/` (rclone). On ne fouille jamais Drive : tout se cherche dans l'index local, et on ne télécharge que les sons retenus.

- `references/index.tsv` : une ligne par son. Colonnes `cat_id` (catégorie UCS, vide pour 280 sons), `pack`, `name`, `duration_s`, `channels`, `sample_rate`, `bits`, `size_mb`, `path` (chemin Drive).
- `references/ucs-categories.md` : ce que veulent dire les préfixes (`WHSH`, `DSGNBoom`, `UIClick`…) et à quoi ils servent en motion. À lire quand la demande est floue (« un truc qui claque sur le titre »).

## 1. Chercher

Les noms sont en anglais. Traduire l'intention de Romain en plusieurs mots anglais, synonymes compris, et viser une catégorie quand elle est évidente :

```bash
S=.claude/skills/sonniss-catalog-audio-fx
bun $S/scripts/search.ts whoosh fast swoosh --max 3
bun $S/scripts/search.ts impact boom hit --cat DSGN
bun $S/scripts/search.ts rise riser tension build --min 3 --max 12
bun $S/scripts/search.ts --cat UI --limit 20
```

Le score `[2/3]` compte les mots trouvés. Les durées filtrent beaucoup : un whoosh fait moins de 3 s, une montée 3 à 12 s, une ambiance dépasse souvent la minute (on la coupera). Si rien ne sort, élargir les synonymes avant de conclure que la banque n'a pas ce son : 609 sons, c'est riche mais pas infini, et le dire franchement vaut mieux qu'un son à côté.

Proposer 3 à 5 candidats avec leur durée et ce qui les distingue (le nom en dit souvent long : `Heavy`, `Airy`, `Fast`, `Low`). Romain choisit à l'oreille, pas sur le nom.

## 2. Récupérer et faire écouter

```bash
bash $S/scripts/fetch.sh <dossier de scène> "<path>" ["<path>"…]
afplay "<scène>/assets/sfx/<fichier>.wav"
```

Les fichiers arrivent dans `<scène>/assets/sfx/`. Télécharger les 3 à 5 candidats d'un coup coûte peu (la plupart pèsent quelques Mo) et permet de les comparer. Une fois le choix fait, mettre les recalés à la Corbeille (`trash`) pour garder la scène légère.

Une ambiance de plusieurs minutes se coupe avant le mix, sinon elle alourdit tout :

```bash
ffmpeg -ss 12 -t 6 -i assets/sfx/long.wav -c:a pcm_s24le assets/sfx/long-cut.wav
```

## 3. Mixer : sans ça, le bruitage ne s'entend pas

`motion render` n'embarque qu'**une** piste son, celle du champ `audio:` de `Motion.scene`. Un bruitage posé dans `assets/sfx/` sans mix n'apparaît donc jamais dans le MP4. On fabrique `assets/mix.wav` = musique + bruitages calés, puis on pointe `audio:` dessus.

Les instants viennent des oreilles de la scène (`assets/ears.json`) : un impact sur un drop, un whoosh qui démarre 0,2 s avant une coupe pour arriver pile dessus.

```bash
ffmpeg -y -i assets/music.mp3 -i assets/sfx/whoosh.wav -i assets/sfx/boom.wav -filter_complex "\
[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.7,adelay=3800:all=1[s1];\
[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.9,adelay=14130:all=1[s2];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[m];\
[m][s1][s2]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[out]" \
-map "[out]" -c:a pcm_s24le assets/mix.wav
```

- `adelay` est en millisecondes : 14,13 s donne `14130`.
- `aformat=channel_layouts=stereo` ramène les sons mono, 4 canaux ou surround au stéréo, sinon `amix` refuse ou déséquilibre.
- `normalize=0` garde la musique à son niveau (sinon `amix` la baisse à chaque son ajouté), `alimiter` évite la saturation quand un impact tombe sur un kick.
- Garder `ears.json` calculé sur la musique seule : repasser `motion ears` sur le mix ferait prendre les bruitages pour des temps.

Puis dans `index.html` : `audio: "assets/mix.wav"`. Vérifier sur le MP4 rendu, à l'oreille ou avec `motion frames` autour des instants posés, et faire écouter un extrait à Romain : c'est lui qui juge si le son tombe juste.

## Si rclone refuse

`couldn't fetch token: invalid_grant` : le jeton Drive a expiré. Romain doit lancer `rclone config reconnect gdrive:` dans un Terminal à part (c'est interactif, ça ouvre le navigateur). Ne pas tenter de contourner.

## Mettre l'index à jour

L'index est une copie de `~/dev/EROM-HQ/lab/sonniss-drive/index.tsv`, produit par `bun build-index.ts` dans ce dossier (il ne lit que l'en-tête des WAV sur Drive). Si la banque grandit (GDC 2025…), régénérer là-bas puis recopier ici.
