"""Generate records from seed rows, variable combinations, and string templates."""

from __future__ import annotations

import json
import math
import os
import re
import tempfile
from collections.abc import Iterable, Mapping
from itertools import product
from pathlib import Path
from string import Template
from typing import Any


def _validate_variables(values: Any, label: str) -> dict[str, Any]:
    if not isinstance(values, dict):
        raise ValueError(f"{label} must be a JSON object")
    for key in values:
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(f"{label} keys must be ASCII variable names")
    return values


def generate(recipe: Mapping[str, Any]) -> list[dict[str, str]]:
    """Expand a recipe deterministically, validate required fields, and deduplicate.

    ``seeds`` is a list of string-valued records; each row remains intact.
    ``variables`` maps independent dimensions to lists of strings. Each seed is
    combined with their Cartesian product. ``templates`` maps output field names
    to Python string.Template expressions (``${name}``, ``$$`` for a literal $).
    ``required_fields`` defaults to every output field. ``max_records`` limits
    candidates BEFORE deduplication; exceeding it raises instead of truncating.

    No models, external services, or code from the recipe are executed.
    """
    if not isinstance(recipe, Mapping):
        raise ValueError("recipe must be a JSON object")
    allowed = {"seeds", "variables", "templates", "required_fields", "max_records"}
    if set(recipe) - allowed:
        raise ValueError("recipe contains unknown keys")

    templates = recipe.get("templates")
    if not isinstance(templates, dict) or not templates:
        raise ValueError("templates must be a non-empty object")
    if any(not isinstance(k, str) or not k.strip() for k in templates):
        raise ValueError("template field names must be non-empty strings")
    if any(not isinstance(v, str) for v in templates.values()):
        raise ValueError("template values must be strings")

    variables = _validate_variables(recipe.get("variables", {}), "variables")
    for choices in variables.values():
        if not isinstance(choices, list) or not choices:
            raise ValueError("each variable must contain a non-empty list")
        if any(not isinstance(v, str) for v in choices):
            raise ValueError("variable choices must be strings")

    seeds = recipe.get("seeds", [{}])
    if not isinstance(seeds, list) or not seeds:
        raise ValueError("seeds must be a non-empty list of objects")
    seed_keys = None
    for seed in seeds:
        _validate_variables(seed, "seed")
        if any(not isinstance(value, str) for value in seed.values()):
            raise ValueError("seed values must be strings")
        if set(seed) & set(variables):
            raise ValueError("seed and variable names must not overlap")
        if seed_keys is None:
            seed_keys = set(seed)
        elif set(seed) != seed_keys:
            raise ValueError("all seed rows must have the same fields")

    required = recipe.get("required_fields", list(templates))
    if not isinstance(required, list) or any(not isinstance(k, str) for k in required):
        raise ValueError("required_fields must be a list of field names")
    if not set(required).issubset(templates):
        raise ValueError("required_fields must reference template fields")

    limit = recipe.get("max_records", 10_000)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("max_records must be a positive integer")
    candidates = len(seeds) * math.prod(len(v) for v in variables.values())
    if candidates > limit:
        raise ValueError(f"recipe expands to {candidates} candidates, above max_records={limit}")

    compiled = {key: Template(value) for key, value in templates.items()}
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for seed in seeds:
        for choices in product(*variables.values()):
            context = {**seed, **dict(zip(variables, choices))}
            try:
                record = {key: template.substitute(context) for key, template in compiled.items()}
            except (KeyError, ValueError) as exc:
                raise ValueError("invalid template or undefined variable; use ${name} and $$") from exc
            if any(not record[key].strip() for key in required):
                raise ValueError("a required output field is blank")
            fingerprint = json.dumps(record, sort_keys=True, ensure_ascii=False)
            if fingerprint not in seen:
                records.append(record)
                seen.add(fingerprint)
    return records


def write_jsonl(records: Iterable[Mapping[str, Any]], path: str | Path) -> int:
    """Write UTF-8 JSONL atomically; never overwrite an existing file.

    The parent directory must exist. All records must be JSON-serializable
    objects. If generation or serialization fails, no destination is created.
    Returns the number of records written.
    """
    destination = Path(path)
    count = 0
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
        prefix=".opensynthlab-", suffix=".tmp", delete=False,
    ) as stream:
        temporary = Path(stream.name)
        try:
            for record in records:
                if not isinstance(record, Mapping):
                    raise ValueError("each JSONL record must be an object")
                stream.write(json.dumps(dict(record), ensure_ascii=False, allow_nan=False) + "\n")
                count += 1
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    try:
        # A same-directory hard link publishes a complete file without clobbering
        # a destination another process might have created in the meantime.
        os.link(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return count
