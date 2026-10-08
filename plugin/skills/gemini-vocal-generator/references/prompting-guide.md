# Prompting guide TTS Gemini (docs officielles, vérifié 2026-10-08)

## Le texte est un transcript verbatim
Le modèle lit le texte comme un script qu'on lui fait prononcer. Les instructions
générales n'y ont pas de place : deux canaux de style existent.
- **Style du tour** : flag `--style` (annotation `speech_metadata.style`), ex. `"whispered urgently"`, `"warm and enthusiastic"`, `"speaking rapidly"`. Ce style s'applique à tout le texte passé.
- **Événement ponctuel** : tag inline dans le texte lui-même (`<sigh>`, `<short pause>`).
- À ne JAMAIS mettre dans `--style` : les traits immuables (âge, genre, accent). Ils
  appartiennent à la création de la voix (`design_voice.py`). Un style du type
  « a 60-year-old man » est un anti-pattern reconnu par la doc.

## Ponctuation et pacing (3 niveaux)
1. Ponctuation : virgules, points de suspension (…), tirets `--` pour des pauses.
2. Tags explicites, position exacte : `<short pause>`, `<long pause>`.
3. Rythme au niveau du tour : `"speaking rapidly"`, `"speaking slowly"` dans `--style`.
Si l'émotion change en cours de texte : découper en plusieurs fichiers, un `--style` par
émotion, posés bout à bout dans la composition, plutôt qu'un style unique sur tout.
(`--dialogue` applique le même `--style` à tous les tours.)

## Prosodie (pitch, intonation)
Se règle via le style : `"high pitch, cheerful and excited inflection"`,
`"monotone and flat"`, `"reflective and awe-inspired"`…

## Emphase
Mots en MAJUSCULES + ponctuation : « This is a VERY important point! ».
En français : « Et ça, c'est un point TRÈS important ! ».

## Tags inline (tous entre chevrons, position exacte)
**Les tags s'écrivent en ANGLAIS même pour un texte français** (« use English inline tags
for best results ») :
`<argh>` `<breath>` `<heavy breath>` `<exhales>` `<cackle>` `<cheer>` `<chuckle>` `<cough>`
`<cry>` `<gasp>` `<giggle>` `<groan>` `<growl>` `<grunt>` `<grr>` `<hiss>` `<laugh>`
`<laughter>` `<moan>` `<pant>` `<pff>`/`<phew>` `<scream>` `<shout>` `<shriek>` `<sigh>`
`<sneeze>` `<snicker>` `<snort>` `<sob>` `<throat-clearing>` `<tsk>` `<whimper>`
`<whispers>` `<yawn>` `<short pause>` `<long pause>`.

## Backchannels / chevauchement
Syntaxe `|réaction|` pour glisser une réaction d'un second locuteur dans une phrase :
« So the launch is Thursday |oh hmm| Are we actually ready? ».
(Réservé aux appels multi-locuteurs.)

## À éviter (anti-patterns de la doc)
- Meta-instructions de stabilité dans le texte (« do not switch speaker identity »).
- Longs blocs « Audio Profile » / « Director's Notes » dans le texte : ces traits vont
  dans la création de la voix (voice design). Le texte reste un script naturel.
- Workflow recommandé par la doc : écrire le transcript NU d'abord, synthétiser sans
  `--style`, écouter, puis n'ajouter UN court style persistant si nécessaire.

## Dialogue
- Deux voix prebuilt : un seul appel conversationnel (synthesize.py le fait).
- Voix designées : un appel par tour. C'est aussi la règle si les émotions
  contrastent fortement entre les tours.