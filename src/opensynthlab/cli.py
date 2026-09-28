"""Command-line interface for the initial template synthesis workflow."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import generate, write_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic records from a JSON recipe.")
    parser.add_argument("--version", action="version", version=f"opensynthlab {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Expand, validate, deduplicate, and export a template recipe")
    run.add_argument("recipe", type=Path, help="Path to a JSON recipe")
    run.add_argument("--output", type=Path, required=True, help="New JSONL file; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        recipe = json.loads(args.recipe.read_text(encoding="utf-8"))
        records = generate(recipe)
        count = write_jsonl(records, args.output)
    except (OSError, ValueError, TypeError) as exc:
        print(f"opensynthlab: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {count} unique records to {args.output}")
    return 0
