"""Command line contract; no implicit private project list."""

import argparse
import json
import math
import os
from pathlib import Path
import sys

from . import __version__
from .config import load_config, targets
from .output import save_html, terminal
from .scan import scan
from .briefing import briefing


def main(argv=None):
    parser = argparse.ArgumentParser(description="Review local Git file sizes without changing projects.")
    parser.add_argument("paths", nargs="*", type=Path, help="Git roots; default: current folder")
    parser.add_argument("--version", action="version", version=f"File Review {__version__}")
    parser.add_argument("--config", type=Path, help="explicit JSON repository list")
    parser.add_argument("--repo", action="append", default=[], help="name from --config; repeatable")
    parser.add_argument("--include-untracked", action="store_true")
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--max-mib", type=float, default=16)
    parser.add_argument("--no-open", action="store_true", help="save HTML without opening a browser")
    parser.add_argument("--output", type=Path, help="new HTML path; refuses to overwrite")
    parser.add_argument("--demo", action="store_true", help="synthetic example; reads no repository")
    parser.add_argument("--task", default="", help="optional review goal, at most 2000 characters")
    parser.add_argument("--inventory-only", action="store_true", help="skip path hints and nearby-file guidance")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--terminal", action="store_true")
    output.add_argument("--json", action="store_true")
    output.add_argument("--plan", action="store_true", help="print a bounded agent review briefing")
    args = parser.parse_args(argv)
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        parser.error("safe file reads require macOS or Linux; on Windows use WSL")
    if len(args.task) > 2000:
        parser.error("task must be at most 2000 characters")
    if args.config and args.paths:
        parser.error("choose paths or --config, not both")
    if args.repo and not args.config:
        parser.error("--repo requires --config")
    if args.demo and (args.config or args.paths or args.repo or args.include_untracked):
        parser.error("--demo cannot be combined with repository inputs")
    if (args.output or args.no_open) and (args.json or args.terminal or args.plan):
        parser.error("--output and --no-open apply only to HTML reports")
    if any(not math.isfinite(value) or value <= 0 for value in (args.seconds, args.max_mib)):
        parser.error("time and read limits must be positive finite numbers")
    if args.seconds > 3600 or args.max_mib > 1024:
        parser.error("scan time cannot exceed 3600 seconds; per-file read limit cannot exceed 1024 MiB")
    if args.max_mib * 1024 * 1024 < 1:
        parser.error("read limit must allow at least one byte")
    try:
        repositories = {} if args.demo else (
            load_config(args.config.expanduser().resolve(), args.repo) if args.config else targets(args.paths))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if args.demo:
        from .demo import example_report
        report = example_report(analyze=not args.inventory_only)
    else:
        if not args.json and not args.plan:
            print("Reading local file sizes. This tool starts no agents.", file=sys.stderr, flush=True)
        report = scan(repositories, args.include_untracked, args.seconds,
                      int(args.max_mib * 1024 * 1024), analyze=not args.inventory_only)
    report["task"] = args.task
    try:
        if args.json:
            print(json.dumps(report, ensure_ascii=True, indent=2))
        elif args.terminal:
            terminal(report)
        elif args.plan:
            print(briefing(report))
        else:
            save_html(report, args.output, not args.no_open)
    except (OSError, UnicodeError) as error:
        print(f"Could not write report: {ascii(str(error))}", file=sys.stderr)
        return 1
    return 0 if all(item["complete"] for item in report["repositories"]) else 1


def entrypoint():
    try:
        result = main()
    except KeyboardInterrupt:
        print("\nScan cancelled.", file=sys.stderr)
        result = 130
    except BrokenPipeError:
        result = 1
    sys.exit(result)
