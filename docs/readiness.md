# Release readiness

The initial public source edition was published on November 4, 2026 at [Belalkf/file-review-local](https://github.com/Belalkf/file-review-local). The original tool remains private. No hosted release or registry upload has been created.

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

## Executed on GitHub

[Checks run 41746253412](https://github.com/Belalkf/file-review-local/actions/runs/41746253412) passed for source commit `77489f94874bbb54a6381548505d5e5c50216c55` on November 4, 2026. Job logs confirm 45 Python tests, 12 report-control tests, the public-source guard, wheel/source builds and isolated installed-command checks in every combination below.

| GitHub runner | Python | Result |
| --- | --- | --- |
| `ubuntu-latest` | 3.9 | Passed |
| `ubuntu-latest` | 3.13 | Passed |
| `macos-latest` | 3.9 | Passed |
| `macos-latest` | 3.13 | Passed |

Node 22 runs the report tests. These are standard hosted GitHub runners; no local virtual machine was installed. The README badge shows the latest workflow state; the linked run preserves the exact tested source and result. Linux browser appearance and screen-reader behavior were not tested by the command-line checks.

## Missing and unverified

There is no language parser, dependency graph, automatic responsibility detection, automatic refactoring, agent execution, cloud integration or demonstrated token saving. The starter scope uses size and path hints; adding a task does not automatically identify relevant files. The chosen agent needs access to source and must validate boundaries itself.

Python/Node/browser versions beyond those recorded above, native Windows, WSL, mobile layout, screen-reader quality and hostile-filesystem behavior were not accepted by these checks. Native Windows is intentionally rejected. A custom logo is optional and has not been created. Repository description, topics and commit attribution are set, and private vulnerability reporting is enabled; account-wide protection settings are outside this release.

Original private tool history/configuration was not imported. This checkout began with an empty Git object store and no remote; its public remote was added only for the authorized publication. The initial public commit uses a neutral contributor identity; see [publication](releasing.md) before choosing future public authorship.
