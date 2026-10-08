# Notes API (vérifiées le 2026-10-08 sur ai.google.dev, pages maj 2026-09-24 et 2026-10-01)

Exemples de code de la doc officielle sous licence Apache 2.0 (© Google), adaptés ici.

## Modèles TTS

| Modèle | Single | Multi | Voice design | Replication | Usage |
|---|---|---|---|---|---|
| `gemini-3.8-flash-tts` | oui | oui | oui | oui | défaut, rendus finaux |
| `gemini-3.8-flash-lite-tts` | oui | oui | oui | oui | drafts/preview uniquement |

SDK requis : `google-genai >= 2.25.0` (Python) - les commandes du SKILL.md pinent cette
version via `uv run --with 'google-genai>=2.25'`.

## Formes exactes de la synthèse (Interactions API)

Single-speaker : `speech_config` est un **tableau**.
```python
generation_config={"speech_config": [{"voice": "Kore"}]}
```
La valeur `voice` accepte : nom prebuilt (`Kore`), voix de la Extended Voice Library,
ID de voice design (`voice_...`), ID de voice replication (`voice_...` ou `voicekey_...`).

Multi-speaker : `speech_config` est un **objet**.
```python
generation_config={"speech_config": {"mode": "conversational", "speakers": [
    {"speaker": "Joe", "voice": "Puck"}, {"speaker": "Jane", "voice": "Kore"}]}}
```
- `mode: "conversational"` n'est garanti que côté REST ; le script replie sur un appel
  par tour si l'appel unique échoue.
- 2 locuteurs prebuilt max par appel. Avec des voix designées (`voice_...`) :
  un appel par tour obligatoirement - c'est le chemin tour-par-tour de synthesize.py.
- Chaque tour de dialogue est un bloc `text` annoté `speech_metadata` avec `speaker`
  obligatoire (et `style` optionnel).

Payload complet d'un tour :
```python
input=[{"type": "user_input", "content": [{
    "type": "text", "text": "...",
    "annotations": [{"type": "speech_metadata", "style": "...", "speaker": "..."}],
}]}]
response_format={"type": "audio"}   # WAV par défaut en unary
```

## Voix (gestion)

- Création : `client.voices.create(store=True, voice={...})` sur `/v1beta/voices`.
  `voice` : `model`, `type="prompted"`, `display_name`, `gender`?, `language_code`,
  `prompted.input` (description naturelle). Retour : `id` permanent + `sample_audio`
  (WAV en base64) pour audition immédiate.
- Lecture : `voices.list / voices.get / voices.delete`.
- `sample_audio` : présent sur create/get uniquement, et pour les voix `prompted` :
  absent de `list` (le get renvoie l'aperçu).
- Limites : **200 voix stockées max par projet**, TTL d'un an prolongé à chaque usage.
  Les voix prebuilt sont hors quota (elles ne sont pas "les nôtres").
- 30 voix prebuilt + Extended Voice Library (centaines, via `voices.list(type=["prebuilt"])`).

## Sortie audio

- Appel synchrone (unary) : **WAV** `audio/wav` avec header RIFF standard : 24 kHz,
  mono, PCM signé 16 bits petit boutien. Header 44 octets ; écrit en `.wav` tel quel.
- Formats alternatifs via `response_format.mime_type` : `audio/l16` (PCM brut),
  `audio/mulaw` / `audio/alaw` (téléphonie), avec `sample_rate` optionnel
  (24000, 16000, 8000). La skill n'utilise que WAV : c'est le plus portable pour le montage.
- Streaming (`stream=True`) : chunks PCM bruts sans header. HORS SCOPE de cette skill
  (pas de temps réel).
- Concaténation de tours : via le module `wave` (frames PCM 24 kHz directement
  concaténables). `concat_wavs` vérifie 24 kHz / mono / 16 bits avant d'écrire.

## Pour le montage
WAV 24 kHz mono 16 bits se pose tel quel sur une piste (Premiere, Resolve, CapCut,
Audition, Pro Tools). Si la séquence de montage est en 48 kHz, l'éditeur resample à
l'import - ou à la main : `ffmpeg -i in.wav -ar 48000 out.wav`.

## Pièges connus
- Clé absente : `load_client()` s'arrête avec un message clair (exit 2).
- `voice` inconnu dans la synthèse : erreur API ; revérifier l'ID via
  `voices.py list` exact (copier-coller l'ID complet).
- Suppression de voix : irréversible, `voices.py delete` exige `--yes` après
  confirmation explicite de Romain.
- Quotas standard de l'API Gemini applicables (par minute/jour selon le palier de clé).