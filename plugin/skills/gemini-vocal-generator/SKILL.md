---
name: gemini-vocal-generator
description: Créer, gérer et synthétiser des voix avec l'API Gemini (voice design, TTS single ou multi-locuteurs, modèles gemini-3.8-flash-tts et gemini-3.8-flash-lite-tts), puis poser le WAV dans une composition HyperFrames. Sert dès que la demande touche une voix sur mesure ou un dialogue - concevoir une voix personnalisée depuis une description, lister/auditionner/supprimer des voix, faire parler un ou plusieurs personnages, narration avec une voix designée, même si le mot "TTS" ou "voice design" n'apparaît pas. Pour une simple voix off avec une voix prête, `/hyperframes:media-use` suffit aussi ; cette skill sert quand il faut une voix designée, un dialogue ou un contrôle fin du style. Pas de temps réel ni de streaming, jamais.
---

# gemini-vocal-generator

Fichiers audio (WAV 24 kHz, mono, 16 bits) avec l'API Gemini TTS, posés ensuite comme
piste `<audio>` dans une composition HyperFrames. Chaque appel est synchrone : il bloque,
puis rend un fichier. JAMAIS de temps réel ni de streaming.

**Quand cette skill, quand HyperFrames.** `/hyperframes:media-use` sait déjà faire une voix
off Gemini avec une voix prête, et rend en plus le minutage des mots pour les sous-titres.
Cette skill apporte ce qu'il n'a pas : la création de voix sur mesure (voice design), les
dialogues à plusieurs voix, et le style piloté tour par tour.

## Prérequis

- `GEMINI_API_KEY` (ou `GOOGLE_API_KEY`) dans l'environnement. Vérifier la présence avec
  `test -n "$GEMINI_API_KEY" && echo presente` : ne jamais afficher la clé.
- Toujours exécuter les scripts via uv, qui pin le SDK (l'API exige >= 2.25.0) :

```bash
G="${CLAUDE_PLUGIN_ROOT}/skills/gemini-vocal-generator/scripts"
uv run --with 'google-genai>=2.25' "$G/<script>.py" <args>
```

Dans les exemples ci-dessous, `<uv>` abrège `uv run --with 'google-genai>=2.25'`.

- Sortie : viser directement le projet HyperFrames avec `-o <projet>/assets/voice/<nom>.wav`.
  Sans `-o`, le fichier part dans `tts_output/<slug>.wav` du répertoire courant. Un rerun
  écrase le fichier cible.

## Modèles

- `gemini-3.8-flash-tts` : défaut ; rendus finaux.
- `gemini-3.8-flash-lite-tts` : flag `--model` pour les drafts/essais de script (moins
  cher, moins de finition) ; remplacer par le full model au rendu final.
- Les deux gèrent single, multi-locuteurs et voice design.

## Workflow

### 1. Concevoir une voix (voice design)

```bash
<uv> "$G/design_voice.py" \
  --prompt "Une narratrice française, chaleur posée, voix grave d'un peu plus de trente ans, élocution nette et lente." \
  --display-name "Narratrice FR" --language fr-FR --preview narration.wav
```

- `--prompt` : 1-2 phrases nettes, traits permanents uniquement (âge, genre, timbre,
  accent, manière de parler). Une description de 1-2 phrases bat un long paragraphe.
- Le script imprime `voice_id=voice_...` : le conserver précieusement (c'est la seule
  référence de la voix ; on la retrouve aussi avec `voices.py list`).
- `--preview` écrit l'aperçu WAV ; le faire écouter à Romain (`afplay <fichier>`)
  avant de produire quoi que ce soit.
- Itérer = créer une NOUVELLE voix (une voix stockée n'est pas modifiable) ; supprimer
  les brouillons avec `voices.py delete` quand le design est validé.
- Une fois la voix validée : ne plus passer les traits à la synthèse. Tout style
  momentané passe par `--style` (voir prompting-guide).

### 2. Gérer les voix

```bash
<uv> "$G/voices.py" list                      # mes voix designées (type prompted)
<uv> "$G/voices.py" list --type prebuilt      # les 30 voix prêtes (Kore, Puck...)
<uv> "$G/voices.py" list --search warm --limit 20
<uv> "$G/voices.py" get --id voice_xxx --preview ecoute.wav
<uv> "$G/voices.py" delete --id voice_xxx --yes
```

- Jamais de `delete` sans confirmation explicite de Romain : c'est irréversible.
- `list` ne renvoie pas l'aperçu audio ; `get --preview` le télécharge.
- `list` affiche 50 voix au plus (une seule page).

### 3. Synthèse

Single-speaker (défaut de l'API) :

```bash
<uv> "$G/synthesize.py" --text "Bonjour, et bienvenue dans cet atelier." --voice Kore -o <projet>/assets/voice/intro.wav
<uv> "$G/synthesize.py" --text "..." --voice voice_abc123 --style "warm and reflective" -o <projet>/assets/voice/intro.wav
```

Dialogue à deux voix prebuilt (un seul appel, cadence conversationnelle naturelle) :

```bash
<uv> "$G/synthesize.py" --dialogue script.txt --speaker-voice "Joe=Puck,Jane=Kore" -o <projet>/assets/voice/dialogue.wav
```

Dialogue avec voix designées (un appel par tour, concaténés dans un seul WAV) :

```bash
<uv> "$G/synthesize.py" --dialogue script.txt --speaker-voice "Narrateur=voice_abc,Invitee=voice_def" --gap-ms 300 -o <projet>/assets/voice/dialogue.wav
```

- Format du script : `Locuteur: texte` par ligne, le nom du locuteur en **un seul mot**
  (`Narrateur`, `Jean-Luc`, `Invitee`). Une ligne qui ne commence pas par un nom suivi de
  `:` prolonge le tour précédent, même si elle contient un « : » à la française.
- `--gap-ms` : silence entre tours du chemin tour-par-tour (défaut 200 ms ; 0 = collé).
- `--style` s'applique à tous les tours. Pour changer d'émotion en cours de route,
  produire plusieurs fichiers avec des `--style` différents et les poser bout à bout.
- Le script imprime `OK out=<chemin absolu> seconds=X.XX rate=... channels=... width=...`,
  lus dans le fichier écrit : c'est la preuve de durée. `afplay` pour écouter.

### 4. Rédiger le texte qui sonne

Lire `references/prompting-guide.md` avant d'écrire un texte long ou un dialogue :
tags inline en ANGLAIS même pour du français (`<short pause>`, `<sigh>`, `<laugh>`),
ponctuation et pauses, MAJUSCULES pour l'emphase, syntaxe `|réaction|`, et la liste des
anti-patterns. Règle générale : transcript naturel nu d'abord, écoute, puis un court
style persistant si nécessaire - jamais de longs « profils audio » dans le texte.

### 5. Poser dans la composition HyperFrames

Une piste `<audio>` par fichier, calée par `data-start` (secondes), sur sa propre
`data-track-index`, séparée de la musique et des bruitages :

```html
<audio id="voice-intro" src="assets/voice/intro.wav"
       data-start="1.5" data-track-index="12" data-volume="1"></audio>
```

- **Chaque `<audio>` a un `id`**, sinon le mixeur ne la voit pas et la voix est muette
  au rendu (`lint` : `media_missing_id`).
- `data-start` se lit sur la ligne `seconds=` du script : une voix de 4,2 s posée à 1,5 s
  occupe jusqu'à 5,7 s. Caler l'animation du texte à l'écran sur cette fenêtre.
- Musique trop forte sous la voix : ducking (ou « voiceover carve ») avec
  `/hyperframes:hyperframes-audio`, pas en retouchant le WAV.
- Sous-titres : Gemini TTS ne donne pas le minutage des mots. Le récupérer avec
  `npx hyperframes transcribe assets/voice/<nom>.wav --model small --language fr`, qui
  écrit `transcript.json` ; vérifier que les noms et les nombres ont survécu, puis suivre
  les captions de `/hyperframes:media-use`.
- Vérifier avec `npx hyperframes lint`, puis à l'écoute du rendu.

## Limites et pièges

- Dans `references/api-notes.md` : 200 voix max par projet (TTL 1 an), 2 locuteurs
  prebuilt max par appel, formes exactes des payloads, formats audio.
- `delete` sans `--yes` refusé par le script ; demander quand même à Romain AVANT.
