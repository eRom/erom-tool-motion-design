"""Helpers shared by the gemini-vocal-generator scripts."""

import base64
import io
import os
import re
import sys
import unicodedata
import wave

# Sortie TTS Gemini : PCM signé 16 bits petit boutien, 24 kHz, mono (doc officielle, oct 2026).
SAMPLE_RATE = 24000
CHANNELS = 1

# Modèle par défaut pour le rendu final ; le Lite reste réservé aux drafts (option --model).
DEFAULT_MODEL = "gemini-3.8-flash-tts"
MODEL_CHOICES = [DEFAULT_MODEL, "gemini-3.8-flash-lite-tts"]

# Les voix designées/replicées arrivent avec ces préfixes d'ID ; tout le reste est un nom prebuilt.
CUSTOM_VOICE_IDS = ("voice_", "voicekey_")


def load_client():
    """Crée le client Gemini. Une seule clé suffit (GEMINI_API_KEY ou GOOGLE_API_KEY du shell)."""
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print(
            "Error: no API key found.",
            "Set GEMINI_API_KEY in your environment (export GEMINI_API_KEY=..., or add it to ~/.zshenv).",
            sep="\n",
            file=sys.stderr,
        )
        sys.exit(2)
    from google import genai

    return genai.Client()


def interaction_audio_bytes(interaction) -> bytes | None:
    """Rend les octets WAV d'une réponse Interactions API, depuis output_audio ou les steps."""
    out = getattr(interaction, "output_audio", None)
    if out is not None and getattr(out, "data", None):
        return base64.b64decode(out.data)
    # Repli : payloads de forme REST, audio dans les steps de model_output.
    for step in getattr(interaction, "steps", None) or []:
        if getattr(step, "type", None) != "model_output":
            continue
        for part in getattr(step, "content", None) or []:
            if isinstance(part, dict):
                if part.get("type") == "audio" and part.get("data"):
                    return base64.b64decode(part["data"])
    return None


def save_wav(data: bytes, path: str) -> None:
    """Écrit les octets WAV reçus tels quels (header RIFF déjà présent)."""
    import pathlib

    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def concat_wavs(chunks: list[bytes], gap_ms: int = 0) -> bytes:
    """Concatène des WAV identiques (24 kHz / 16 bits / mono) en un seul WAV, silence entre tours."""
    gap_frames = int(SAMPLE_RATE * gap_ms / 1000)
    out = io.BytesIO()
    with wave.open(out, "wb") as writer:
        writer.setnchannels(CHANNELS)
        writer.setsampwidth(2)
        writer.setframerate(SAMPLE_RATE)
        for index, blob in enumerate(chunks):
            if index > 0 and gap_frames > 0:
                writer.writeframes(b"\x00" * (gap_frames * 2))
            with wave.open(io.BytesIO(blob), "rb") as reader:
                got = (reader.getframerate(), reader.getnchannels(), reader.getsampwidth())
                if got != (SAMPLE_RATE, CHANNELS, 2):
                    raise RuntimeError(f"unexpected WAV shape {got}, expected {(SAMPLE_RATE, CHANNELS, 2)}")
                writer.writeframes(reader.readframes(reader.getnframes()))
    return out.getvalue()


def slugify(text: str, max_chars: int = 48) -> str:
    """Nom de fichier court et lisible, sans accents ni tags inline."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    keep = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (keep[:max_chars].strip("-") or "tts")