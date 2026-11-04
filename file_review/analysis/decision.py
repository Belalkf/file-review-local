"""Language-independent review routes; path hints never prove architecture."""

from pathlib import PurePosixPath

CONNECTED = {".json", ".jsonl", ".lock", ".pbxproj", ".svg", ".xml", ".toml", ".yaml", ".yml"}
GENERATED = {"package-lock.json", "yarn.lock", "poetry.lock", "Cargo.lock"}


def classify(path):
    item = PurePosixPath(path)
    if any(part.lower() in {"vendor", "vendored", "generated", "dist", "build", "node_modules"}
           for part in item.parts) or item.name in GENERATED:
        return "generated-or-vendor-path"
    if item.suffix.lower() in CONNECTED:
        return "connected-format"
    return "needs-content-review"


def decide(row):
    category = classify(row["path"])
    result = {"action": "inspect", "confidence": "measurements and path hints only", "category": category,
              "summary": "Read responsibilities and relationships before choosing split, keep, or combine.",
              "steps": ["Inspect callers, shared state, initialization, public routes and affected tests.",
                        "Try focused reading first if restructuring would add more navigation."],
              "related": []}
    if category != "needs-content-review":
        result.update(action="check-owner", summary="Check the producer or consuming format before considering changes.",
                      steps=["This path is a hint, not proof that the file is generated or inseparable.",
                             "Preserve the original format; change its source or use supported composition only."])
    return result
