#!/usr/bin/env python3
"""Conçoit une voix avec l'API Gemini (voice design) : description en langage naturel, ID permanent, aperçu WAV.

Les traits qui ne changent jamais (âge, genre, timbre, accent, manière) vont ici.
Le style d'un instant précis se règle plus tard, à la synthèse (--style de synthesize.py).
"""

import argparse
import base64
import sys

from common import DEFAULT_MODEL, MODEL_CHOICES, load_client, save_wav, slugify


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--prompt",
        required=True,
        help="voice description in natural language, 1-2 crisp sentences (immutable traits only)",
    )
    ap.add_argument("--display-name", required=True, help="friendly name stored with the voice")
    ap.add_argument(
        "--gender",
        choices=["female", "male", "neutral"],
        default=None,
        help="optional hint; a description like 'she' often implies it",
    )
    ap.add_argument("--language", default="fr-FR", help="BCP-47 code (default fr-FR)")
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=MODEL_CHOICES,
        help="model that generates the sample (default: the full model)",
    )
    ap.add_argument(
        "--preview",
        default=None,
        help="where to save the sample WAV (default: tts_output/<slug of display name>.wav)",
    )
    args = ap.parse_args()

    client = load_client()

    voice_spec = {
        "model": args.model,
        "type": "prompted",
        "display_name": args.display_name,
        "language_code": args.language,
        "prompted": {"input": args.prompt},
    }
    if args.gender:
        voice_spec["gender"] = args.gender

    created = client.voices.create(store=True, voice=voice_spec)

    voice_id = getattr(created, "id", None)
    preview_path = args.preview
    if preview_path is None:
        preview_path = f"tts_output/{slugify(args.display_name)}.wav"

    if voice_id is None:
        print("Error: the API returned no voice id.", file=sys.stderr)
        raise SystemExit(1)

    sample = getattr(created, "sample_audio", None)
    if sample is not None and getattr(sample, "data", None):
        save_wav(base64.b64decode(sample.data), preview_path)
    else:
        preview_path = "none (no sample audio returned)"

    print(
        f'OK voice_id={voice_id} display_name="{args.display_name}" '
        f'language={args.language} model={args.model} preview={preview_path}'
    )


if __name__ == "__main__":
    main()