"""Git inventory and scan accounting. Never import code from scanned projects."""

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import os
import subprocess
import time

from .measure import ScanLimit, measure
from .analysis.runner import enrich


def inventory(root, include_untracked, deadline):
    timeout = min(10, deadline - time.monotonic())
    if timeout <= 0:
        raise ScanLimit()
    # Ignore inherited Git redirection/configuration; disable optional index writes.
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0",
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    base = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root)]
    probe = subprocess.run(base + ["rev-parse", "--show-toplevel"], capture_output=True,
                           timeout=timeout, env=environment, check=True)
    if Path(os.fsdecode(probe.stdout).removesuffix("\n")).resolve() != root:
        raise ValueError("configured folder must be a repository root")
    args = ["ls-files", "-z", "--cached"]
    if include_untracked:
        args += ["--others", "--exclude-standard"]
    result = subprocess.run(base + args, capture_output=True,
                            timeout=max(0.01, min(10, deadline - time.monotonic())),
                            env=environment, check=True)
    return sorted(set(os.fsdecode(path) for path in result.stdout.split(b"\0") if path))


def scan(repositories, include_untracked=False, seconds=60, max_bytes=16 * 1024 * 1024,
         max_files=100000, analyze=True):
    deadline = time.monotonic() + seconds
    report = {"schema_version": 1, "created": datetime.now(timezone.utc).isoformat(), "rows": [], "repositories": [],
              "include_untracked": include_untracked, "max_bytes": max_bytes, "seconds": seconds}
    attempted = 0
    for name, root in repositories.items():
        root = Path(root).resolve()
        status = {"name": name, "root": str(root), "listed": 0, "measured": 0,
                  "skipped": {}, "issues": [], "complete": True}
        report["repositories"].append(status)
        skipped = Counter()
        try:
            paths = inventory(root, include_untracked, deadline)
            status["listed"] = len(paths)
            for index, path in enumerate(paths):
                if attempted >= max_files or time.monotonic() >= deadline:
                    status["complete"] = False
                    status["issues"].append(f"Scan limit reached; {len(paths) - index} paths not read")
                    break
                attempted += 1
                try:
                    row, reason = measure(root, path, max_bytes, deadline)
                except (OSError, ValueError) as error:
                    row, reason = None, "unreadable, missing, linked or non-regular"
                    if len(status["issues"]) < 12:
                        status["issues"].append(f"{path}: {error}")
                if reason:
                    skipped[reason] += 1
                    if reason != "binary or non-UTF-8":
                        status["complete"] = False
                else:
                    report["rows"].append(dict(row, repository=name))
                    status["measured"] += 1
        except (OSError, ValueError, subprocess.SubprocessError, ScanLimit) as error:
            status["complete"] = False
            status["issues"].append(str(error) or "Scan time limit reached")
        status["skipped"] = dict(skipped)
    report["rows"].sort(key=lambda row: (-row["lines"], -row["bytes"], row["repository"], row["path"]))
    if analyze:
        enrich(report)
    return report
