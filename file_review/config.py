"""Explicit targets and optional user-owned multi-repository configuration."""

import json
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate configuration key: {key}")
        result[key] = value
    return result


def load_config(path, selected):
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or set(data) != {"repositories"}:
        raise ValueError("configuration must contain only a repositories object")
    entries = data["repositories"]
    if not isinstance(entries, dict) or not entries:
        raise ValueError("repositories must be a nonempty name-to-path object")
    if any(name not in entries for name in selected):
        raise ValueError("unknown repository selection")
    roots = {}
    for name, relative in entries.items():
        if not name.strip() or not isinstance(relative, str) or not relative.strip():
            raise ValueError("each repository needs a nonempty name and path")
        if selected and name not in selected:
            continue
        root = (path.parent / Path(relative).expanduser()).resolve()
        if root in roots.values():
            raise ValueError("duplicate repository root")
        if not root.is_dir():
            raise ValueError(f"repository folder is missing: {root}")
        roots[name] = root
    return roots


def targets(paths):
    roots = {}
    for path in paths or [Path.cwd()]:
        root = Path(path).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"repository folder is missing: {root}")
        name = root.name or "repository"
        if root in roots.values():
            raise ValueError("duplicate repository root")
        if name in roots:
            raise ValueError("targets share a folder name; use named entries in --config")
        roots[name] = root
    return roots
