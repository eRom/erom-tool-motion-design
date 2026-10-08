#!/usr/bin/env python3
"""Gère les voix stockées du projet Gemini : lister, détailler (avec aperçu), supprimer.

Sans filtre, `list` ne rend que les voix designées (type "prompted") : ce sont "mes" voix.
Les voix prebuilt (Kore, Puck...) et la Extended Voice Library demandent --type prebuilt/all.
"""

import argparse
import base64
import sys

from common import load_client, save_wav, slugify

VOICE_TYPES = ["prompted", "prebuilt", "replicated", "all"]


def cmd_list(args, client):
    kwargs = {"page_size": min(args.limit, 50)}
    if args.type != "all":
        kwargs["type_"] = [args.type]
    if args.language:
        kwargs["language_code"] = [args.language]
    if args.search:
        kwargs["search"] = args.search
    response = client.voices.list(**kwargs)
    voices = getattr(response, "voices", None) or []
    if not voices:
        print("No voices found for this filter.")
        return
    for voice in voices[: args.limit]:
        # Les listes ne portent pas toujours tous les champs : ce qui manque est vide.
        row = [
            getattr(voice, "id", "") or "-",
            getattr(voice, "display_name", "") or "-",
            getattr(voice, "type", "") or "-",
            getattr(voice, "language_code", "") or "-",
            getattr(voice, "gender", "") or "-",
        ]
        print("\t".join(row))
    print(f"{len(voices)} voice(s) shown (limit {args.limit})", file=sys.stderr)


def cmd_get(args, client):
    voice = client.voices.get(id=args.id)
    sample = getattr(voice, "sample_audio", None)
    if args.preview:
        if sample is not None and getattr(sample, "data", None):
            save_wav(base64.b64decode(sample.data), args.preview)
            print(f"OK preview={args.preview}")
        else:
            print("No sample audio attached to this voice (prompted voices only, on get/create).", file=sys.stderr)
    for field in ("id", "display_name", "type", "language_code", "gender", "model"):
        value = getattr(voice, field, None)
        if value is not None:
            print(f"{field}={value}")


def cmd_delete(args, client):
    if not args.yes:
        # Suppression irréversible : on exige --yes, après une confirmation de Romain en clair.
        print(
            "Refusing to delete without explicit confirmation.",
            "Rerun with: --yes after the user has confirmed.",
            sep="\n",
            file=sys.stderr,
        )
        raise SystemExit(2)
    client.voices.delete(id=args.id)
    print(f"OK deleted voice_id={args.id}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list voices (default: my prompted voices)")
    p_list.add_argument("--type", choices=VOICE_TYPES, default="prompted")
    p_list.add_argument("--language", default=None, help="BCP-47 filter, e.g. fr-FR")
    p_list.add_argument("--search", default=None, help="free-text search over names/descriptions")
    p_list.add_argument("--limit", type=int, default=50, help="max 50 (single page, no pagination)")
    p_list.set_defaults(handler=cmd_list)

    p_get = sub.add_parser("get", help="show one voice in detail, optional preview WAV")
    p_get.add_argument("--id", required=True)
    p_get.add_argument("--preview", default=None, help="where to save the sample WAV")
    p_get.set_defaults(handler=cmd_get)

    p_del = sub.add_parser("delete", help="permanently delete a stored voice")
    p_del.add_argument("--id", required=True)
    p_del.add_argument("--yes", action="store_true", help="confirm the irreversible delete")
    p_del.set_defaults(handler=cmd_delete)

    args = ap.parse_args()
    client = load_client()
    args.handler(args, client)


if __name__ == "__main__":
    main()