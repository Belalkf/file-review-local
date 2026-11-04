"""Synthetic showcase: no source files, user paths or repository access."""


def example_report(analyze=True):
    files = [
        ("src/workflows/export.py", 428, 18420, 108),
        ("tests/export.test.ts", 286, 11960, 96),
        ("docs/design.md", 164, 14320, 704),
        ("assets/catalog.json", 42, 48200, 3280),
        ("src/settings.ts", 86, 2440, 88),
    ]
    report = {
        "schema_version": 1, "created": "2026-01-01T12:00:00+00:00", "demo": True,
        "include_untracked": False, "max_bytes": 16777216, "seconds": 60,
        "rows": [dict(repository="example-app", path=path, lines=lines, bytes=size,
                      longest_line=longest) for path, lines, size, longest in files],
        "repositories": [{"name": "example-app", "root": "/projects/example-app",
                          "listed": 6, "measured": 5, "complete": True,
                          "skipped": {"binary or non-UTF-8": 1}, "issues": []}],
    }

    if analyze:
        from .analysis.runner import enrich
        enrich(report)
    return report
