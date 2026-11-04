"""Low-cost public-source guard, not a substitute for a human privacy review."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "__pycache__", "build", "dist"}
PATTERNS = [
    re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
]


def main():
    errors = []
    count = 0
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f"{relative}: unexpected symlink")
            continue
        if not path.is_file():
            continue
        if path.name.startswith(".env") or path.name == "repositories.local.json":
            errors.append(f"{relative}: private configuration in source tree")
        if path.suffix == ".png":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"{relative}: unexpected binary file")
            continue
        count += 1
        for pattern in PATTERNS:
            if pattern.search(content):
                errors.append(f"{relative}: possible private information (inspect locally)")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if "://" in target or target.startswith("#"):
                    continue
                linked = path.parent / target.split("#")[0].replace("%20", " ")
                if not linked.exists():
                    errors.append(f"{relative}: missing link target {target}")
        if len(content.splitlines()) >= 150:
            errors.append(f"{relative}: review file responsibility (150+ lines)")
        # Setuptools writes a space after empty INI assignments in source archives.
        trailing = [line for line in content.splitlines() if line.rstrip() != line]
        if any(not (path.name == "setup.cfg" and re.fullmatch(r"[A-Za-z_][\w.-]* = [ \t]*", line)) for line in trailing):
            errors.append(f"{relative}: trailing whitespace")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Reviewed {count} text files; {len(errors)} guard findings.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
