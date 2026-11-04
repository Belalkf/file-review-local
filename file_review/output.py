"""Private report creation and terminal presentation."""

import os
from pathlib import Path
import tempfile
import webbrowser

from .render import render


def terminal(report):
    for item in report["repositories"]:
        print(f"{ascii(item['name'])}: {item['measured']}/{item['listed']} text files; "
              f"{'inventory complete' if item['complete'] else 'INCOMPLETE'}; excluded {item['skipped']}")
        for issue in item["issues"]:
            print("  " + ascii(issue))
    print("\nLargest 50 measured text files by lines (not all files):")
    print("   Lines       Bytes   Longest line  File")
    for row in report["rows"][:50]:
        print(f"{row['lines']:8} {row['bytes']:11} {row['longest_line']:14}  "
              f"{ascii(row['repository'] + '/' + row['path'])}")


def save_html(report, destination=None, open_browser=True):
    content = render(report)
    if destination is None:
        descriptor, filename = tempfile.mkstemp(prefix="file-review-", suffix=".html")
    else:
        filename = str(destination.expanduser().absolute())
        descriptor = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as target:
        target.write(content)
    print(f"Report: {ascii(filename)}")
    if open_browser:
        try:
            opened = webbrowser.open(Path(filename).as_uri())
        except (webbrowser.Error, OSError):
            opened = False
        if not opened:
            print("Open the saved report path in your browser.")
