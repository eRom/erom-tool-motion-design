#!/usr/bin/env python3
"""Synthèse vocale (TTS) : texte simple ou dialogue multi-voix -> fichier WAV pour logiciel de montage.

Deux voix prebuilt : un seul appel conversationnel. Avec au moins une voix designée
(ID "voice_...") ou plus de deux locuteurs : un appel par tour, puis concaténation
(silence --gap-ms entre les tours). Aucun streaming, tout est synchrone.
"""

import argparse
import os
import re
import sys
import wave

from common import (
    CUSTOM_VOICE_IDS,
    DEFAULT_MODEL,
    MODEL_CHOICES,
    concat_wavs,
    interaction_audio_bytes,
    load_client,
    save_wav,
    slugify,
)

# "Nom: texte" ; une ligne sans étiquette prolonge le tour précédent.
# Le nom est un seul mot : en français, "On part demain : tout est prêt." est une suite de phrase,
# pas un locuteur nommé "On part demain".
TURN_LINE = re.compile(r"^([\w.'-]{1,32})\s*:\s+(.+)$")


def text_block(text: str, style: str = "", speaker: str = None) -> dict:
    """Bloc texte du payload Interactions API, avec ses annotations speech_metadata."""
    metadata = {}
    if style:
        metadata["style"] = style
    if speaker:
        metadata["speaker"] = speaker
    block = {"type": "text", "text": text}
    if metadata:
        block["annotations"] = [{"type": "speech_metadata", **metadata}]
    return block


def call_single(client, model: str, text: str, voice: str, style: str) -> bytes:
    """Un appel single-speaker, rend les octets WAV du tour."""
    response = client.interactions.create(
        model=model,
        input=[{"type": "user_input", "content": [text_block(text, style)]}],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": voice}]},
    )
    audio = interaction_audio_bytes(response)
    if not audio:
        raise RuntimeError(f"no audio returned for voice {voice}")
    return audio


def call_dialogue_single(client, model: str, turns, voices, style: str) -> bytes:
    """Un seul appel multi-locuteurs : cadence conversationnelle, 2 voix prebuilt."""
    generation_config = {
        "speech_config": {
            "speakers": [{"speaker": s, "voice": voices[s]} for s in speakers_in_order(turns)],
        }
    }
    response = client.interactions.create(
        model=model,
        input=[
            {
                "type": "user_input",
                "content": [text_block(t, style, speaker=s) for s, t in turns],
            }
        ],
        response_format={"type": "audio"},
        generation_config=generation_config,
    )
    audio = interaction_audio_bytes(response)
    if not audio:
        raise RuntimeError("no audio returned for the conversational call")
    return audio


def speakers_in_order(turns):
    seen = []
    for speaker, _ in turns:
        if speaker not in seen:
            seen.append(speaker)
    return seen


def is_custom_voice(voice: str) -> bool:
    return voice.startswith(CUSTOM_VOICE_IDS)


def parse_dialogue(raw: str) -> list[tuple[str, str]]:
    """Parse un script "Speaker: texte" ; une ligne sans étiquette prolonge le tour courant."""
    turns = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        match = TURN_LINE.match(line)
        if match:
            turns.append((match.group(1), match.group(2)))
        elif turns:
            # Un "speaker" a rarement ":" au milieu d'une phrase ; ici c'est une continuation.
            speaker, text = turns[-1]
            turns[-1] = (speaker, f"{text} {line}")
        else:
            print(
                f"Error: first dialogue line must be 'Speaker: ...' (got: {line!r})",
                file=sys.stderr,
            )
            raise SystemExit(1)
    if not turns:
        print("Error: empty dialogue script.", file=sys.stderr)
        raise SystemExit(1)
    return turns


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--text", help="text to speak (single speaker) ; inline tags allowed")
    ap.add_argument(
        "--voice",
        help="voice name (e.g. Kore) or designed voice id (voice_...) ; required with --text",
    )
    ap.add_argument(
        "--style",
        default="",
        help="delivery style applied to every turn (e.g. 'whispered urgently') ; never immutable traits",
    )
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=MODEL_CHOICES,
        help="gemini-3.8-flash-tts (finaux) ou gemini-3.8-flash-lite-tts (drafts)",
    )
    ap.add_argument("--dialogue", help="path of a 'Speaker: line' script file")
    ap.add_argument("--stdin-dialogue", action="store_true", help="read the script from stdin")
    ap.add_argument(
        "--speaker-voice",
        default="",
        help="map 'Speaker=Voice[,Speaker=Voice]' (prebuilt name or voice id)",
    )
    ap.add_argument(
        "--gap-ms",
        type=int,
        default=200,
        help="silence between turns in the turn-by-turn path (default 200 ms, 0 = none)",
    )
    ap.add_argument(
        "-o",
        "--output",
        default=None,
        help="target WAV (default tts_output/<slug>.wav ; overwritten on rerun)",
    )
    args = ap.parse_args()

    if args.text and (args.dialogue or args.stdin_dialogue):
        print("Error: use --text or --dialogue, not both.", file=sys.stderr)
        raise SystemExit(1)

    if not (args.text or args.dialogue or args.stdin_dialogue):
        print("Error: give --text, --dialogue or --stdin-dialogue.", file=sys.stderr)
        raise SystemExit(1)

    if args.stdin_dialogue:
        script_raw = sys.stdin.read()
    elif args.dialogue:
        script_raw = open(args.dialogue, encoding="utf-8").read()

    client = load_client()

    if args.text:
        if not args.voice:
            print("Error: --voice is required with --text.", file=sys.stderr)
            raise SystemExit(1)
        audio = call_single(client, args.model, args.text, args.voice, args.style)
        stem = slugify(args.text)
    else:
        turns = parse_dialogue(script_raw)
        speakers = speakers_in_order(turns)
        voices = {}
        for pair in args.speaker_voice.split(","):
            pair = pair.strip()
            if not pair:
                continue
            if "=" not in pair:
                print(f"Error: bad --speaker-voice entry {pair!r} (expected Speaker=Voice).", file=sys.stderr)
                raise SystemExit(1)
            name, v = pair.split("=", 1)
            voices[name.strip()] = v.strip()
        missing = [s for s in speakers if s not in voices]
        if missing:
            print(
                f"Error: no voice given for speaker(s) {missing} ; add them via --speaker-voice.",
                file=sys.stderr,
            )
            raise SystemExit(1)

        # Deux locuteurs, deux voix prebuilt : un seul appel, meilleure cadence. Sinon tour par tour.
        audio = None
        if len(speakers) == 2 and all(not is_custom_voice(voices[s]) for s in speakers):
            try:
                audio = call_dialogue_single(client, args.model, turns, voices, args.style)
            except Exception as exc:
                print(f"Note: single conversational call failed ({exc}) ; synthesizing turn by turn.", file=sys.stderr)
        if audio is None:
            chunks = [call_single(client, args.model, t, voices[s], args.style) for s, t in turns]
            audio = concat_wavs(chunks, gap_ms=max(0, args.gap_ms))
        stem = (os.path.splitext(os.path.basename(args.dialogue))[0] if args.dialogue else "dialogue")

    out_path = args.output or f"tts_output/{stem}.wav"
    save_wav(audio, out_path)

    with wave.open(out_path, "rb") as reader:
        rate = reader.getframerate()
        seconds = reader.getnframes() / rate
        channels = reader.getnchannels()
        width = reader.getsampwidth() * 8
    print(f"OK out={os.path.abspath(out_path)} seconds={seconds:.2f} rate={rate} channels={channels} width={width}bit")


if __name__ == "__main__":
    main()