# Architecture

The dependency direction is command → discovery/measurement → report data → presentation. Scanned code is never imported. There is no server or remote API.

| Owner | Responsibility |
| --- | --- |
| `file_review/cli.py` | Arguments, validation, exit status and cancellation |
| `file_review/config.py` | Explicit targets and user-owned configuration |
| `file_review/scan.py` | Git discovery, accounting, budgets and row ordering |
| `file_review/measure.py` | Safe regular-file reads and text measurements |
| `file_review/analysis/` | Language-independent path hints and bounded same-folder navigation |
| `file_review/briefing.py` | Shared agent guidance, priority and terminal briefing |
| `file_review/render.py` | Self-contained HTML assembly and payload escaping |
| `file_review/output.py` | Private report creation and terminal display |
| `file_review/report.*` | Browser layout, filters, selection and copy controls |
| `file_review/demo.py` | Synthetic showcase data only |

## Organization decisions

File size is a review signal. Split source when distinct responsibilities make ordinary changes easier to understand. Keep connected formats, generated artifacts, cohesive tests and data intact when arbitrary division harms their consumer or meaning. Consolidate unnecessary fragments when they obscure a single owner. The scanner cannot infer these architectural decisions from size; the copied request says so explicitly. There are no language parsers. Path/format hints are tentative and apply consistently across languages; same-folder small files are navigation hints, never a dependency graph. Python is the implementation language, not the target-language scope.

The report-control JavaScript stays together because its filter, selection and pagination state form one small interaction owner. Reconsider if another independent interaction emerges. HTML, CSS and JavaScript remain separate authoring assets and are bundled into a single generated report. Keep CSS readable, with normal rule blocks rather than giant minified lines. No current authored file needs a 150-line exception. Synthetic screenshots are binary presentation assets, not source-size targets.

## Distribution

`pyproject.toml` selects the setuptools backend; `setup.cfg` owns metadata, package assets and the `file-review` entry point. This uses the locally available packaging toolchain without requiring modern metadata support in the runtime interpreter. Runtime dependencies are empty. Both wheel and source archive must contain the three report assets. The source archive also carries the optional skill; the Python wheel need not install agent instructions. Distribution metadata has no personal author or email.

The standalone CLI is the primary product. A small optional skill in `skills/file-review/` makes its workflow discoverable to compatible agents and adds no application logic or runtime dependency. It stays with the tool so instructions and behavior can be reviewed together. The existing copyable briefing remains useful without an agent skill. GitHub installation is available now; PyPI may offer simpler versioned installation after a separately authorized release and name review.

## Public boundary

This edition started from selected implementation and tests, not a Git clone. No old commits, private configuration or shared-workspace instructions belong here. Future updates should be reviewed patches, not automatic synchronization with a private checkout. See [releasing](releasing.md) for the source and history review gate.
