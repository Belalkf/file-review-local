"""Annotate existing measurements without rereading or parsing source."""

from pathlib import PurePosixPath

from .decision import decide


def enrich(report):
    report["analysis"] = {
        "method": "Language-independent measurements and path hints",
        "limits": "No language parsing, dependency graph, responsibility detection or verified split plan",
        "annotated": len(report["rows"]),
    }
    folders = {}
    for row in report["rows"]:
        row["review"] = decide(row)
        key = (row["repository"], str(PurePosixPath(row["path"]).parent))
        folders.setdefault(key, []).append(row)
    for siblings in folders.values():
        small = [row for row in siblings if row["lines"] <= 40 and
                 row["review"]["category"] == "needs-content-review"]
        if len(small) < 3:
            continue
        # Bound output and avoid quadratic searches in folders with many tiny files.
        nearby = [row["path"] for row in small[:9]]
        for row in small:
            row["review"]["related"] = [path for path in nearby if path != row["path"]][:8]
            row["review"]["steps"].append(
                "Several small text files share this folder. Check whether they belong together; "
                "adjacency alone proves neither coupling nor a reason to combine.")
