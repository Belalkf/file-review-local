# Local release readiness

This is an initial public source edition prepared on November 4, 2026. It is ready for review and a first GitHub publication; no remote repository, hosted release, registry upload or hosted CI result was created by preparation.

## Implemented

- Local Git working-copy inventory from explicit paths, supporting one or multiple repositories independently.
- Offline HTML, JSON, terminal inventory and a copyable agent briefing, with optional task context.
- The same review workflow for any measured text language; path/format hints and small-file adjacency are explicitly limited evidence.
- Safe regular-file measurement, content fingerprints, visible coverage gaps, bounded work and exclusive private report creation.
- Installable command, synthetic showcase and screenshot, MIT licence, contribution/security guidance and pinned CI configuration.

## Executed locally

On macOS with Python 3.9.6, Git 2.39.5 and Node 23.5.0:

| Check | Result and scope |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 45 tests passed, including multiple repositories, file preservation, links, concurrent replacement, budgets, Git environment isolation, language-neutral guidance and task handoff |
| `node --test tests/test_*.cjs` | 12 report-control tests passed; in-memory document harness, not a real-browser engine |
| `python3 scripts/check_public.py` | Passed source privacy-pattern, local-link, whitespace and file-responsibility checks; not proof of absence of all secrets |
| Wheel and source archive | Built with installed setuptools 58.0.4 and wheel 0.37.0, without downloading dependencies; package contents checked |
| `python3 scripts/check_wheel.py DIST_DIRECTORY` | Passed isolated offline wheel installation and commands outside the source folder, including HTML, JSON and task briefing |
| Firefox local HTML | Visually reviewed synthetic report, request jump, optional task updates and disclosure layout; screenshot contains synthetic paths only and no PNG metadata |
| macOS launcher | Syntax and non-interactive demo invocation checked; Finder double-click and interactive input not accepted |

The archive includes the tests, their browser harness and release-check scripts so contributors can reproduce the documented checks. No real project report or source body is included in the public snapshot. Review the complete source and intended Git identity again before publication; automated patterns cannot certify privacy.

## Missing and unverified

There is no language parser, dependency graph, automatic responsibility detection, automatic refactoring, agent execution, cloud integration or demonstrated token saving. The starter scope uses size and path hints; adding a task does not automatically identify relevant files. The chosen agent needs access to source and must validate boundaries itself.

Linux, other Python/Node/browser versions, native Windows, WSL, mobile layout, screen-reader quality and hostile-filesystem behavior were not accepted by these local checks. Native Windows is intentionally rejected. macOS/Linux CI is configured but must run on GitHub after publication. Project-name availability, public-account attribution, private vulnerability reporting and account protection settings require the actual destination account. A custom logo is optional and has not been created.

Original private tool history/configuration was not imported. This checkout began with an empty Git object store and no remote. The initial public commit uses a neutral contributor identity; see [publication](releasing.md) before choosing future public authorship.
