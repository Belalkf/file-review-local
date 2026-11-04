# File Review

[![Checks](https://github.com/Belalkf/file-review-local/actions/workflows/ci.yml/badge.svg)](https://github.com/Belalkf/file-review-local/actions/workflows/ci.yml)

**Find the files worth a closer look. Decide what should stay together.**

File Review turns a local Git inventory into a ready-to-copy review briefing for your coding agent. Add what you want to change, inspect the evidence when needed, and ask for a reasoned decision: split, keep, combine, or simply read more selectively. The workflow is the same for every readable text file, regardless of programming language.

![Synthetic File Review dashboard](docs/preview.png)

No AI service, runtime Python dependencies, background server, telemetry or project changes. Python 3.9+ and Git are required. Designed for macOS and Linux; native Windows is rejected because the safe file reader needs POSIX features. WSL may work but has not been verified.

## Try the synthetic demo

Get the public source:

```sh
git clone https://github.com/Belalkf/file-review-local.git
cd file-review-local
```

From this checkout, preview a synthetic report without reading any repository:

```sh
python3 -m file_review --demo
```

Then inspect a Git repository root (not a subfolder):

```sh
python3 -m file_review /path/to/project
python3 -m file_review /path/to/project --terminal
```

The checkout can live anywhere: beside your projects, inside one, or in a tools folder. It does not need a fixed relationship to the repositories it scans. With no path, it scans your current folder, which must itself be a Git root. Nothing is installed or downloaded by these commands.

## Install an everyday command

Install from a local checkout in a new virtual environment. The build-tool step downloads setuptools and wheel; the application has no runtime Python dependencies:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'setuptools>=58' wheel
python -m pip install --no-build-isolation --no-deps .
file-review /path/to/project
```

If setuptools 58+ and wheel are already available in your chosen environment, skip the build-tool download. Run from source if you want no packaging setup. There is no published PyPI release; the distribution name `file-review-local` is local metadata, not a claim to a reserved registry name.

Alternatively, with Git and the build tools already installed, install directly from the public GitHub repository into an activated virtual environment:

```sh
python -m pip install --no-build-isolation --no-deps 'git+https://github.com/Belalkf/file-review-local.git'
file-review --version
```

This downloads the current default branch; use a reviewed commit or release tag after `@` in the URL to pin a version. The GitHub source and a future PyPI release are separate distribution choices; no PyPI package is claimed or published yet.

## Optional coding-agent skill

The optional [File Review skill](skills/file-review/SKILL.md) helps an agent run the command, interpret coverage and inspect the actual code before proposing changes. It adds a reusable workflow and discovery; the existing CLI and copyable briefing work without it. Install the Python command separately as above, then from the project where you use your agent run:

```sh
npx skills add Belalkf/file-review-local
```

Choose the skill and agent when prompted. The skills CLI requires Node.js and downloads its own package and the skill; it does not install the Python executable. This command can discover the skill after these changes are published to the public repository. See [agent integration](docs/usage.md#optional-agent-skill) for local discovery and privacy limits.

## What you get

- A self-contained browser report with local filters, sorting, selection and a copyable review request.
- Tracked working-copy text measurements, including local edits; optional non-ignored untracked files.
- Visible coverage gaps when files cannot be measured, so incomplete scans never masquerade as a clean bill of health.
- JSON and terminal output for scripts or remote shells.
- A starter request for up to 12 files without manual selection; explicit selections replace that scope.
- An optional task, file fingerprints to check freshness, and expandable evidence with honest limits.
- A split / keep / combine / focused-reading request that asks the agent to inspect relationships and tests first.

Default filters show at least 150 lines **or** 32 KiB **or** a 1,000-byte line. These are adjustable review signals, not quality scores or mandatory limits. Generated files, lockfiles and connected formats may be best kept intact. File Review measures size and adds conservative path hints. It does not parse any language, infer architecture, edit files or launch agents. The agent you choose must read the actual code to make architectural decisions.

## Why use this alongside an agent?

The useful part is the handoff: a small starting scope, visible missing coverage, preserved-format warnings, and an explicit requirement to justify restructuring before doing it. This is a focused alternative to setting up an automated refactoring service, not a claim to a unique algorithm or guaranteed token savings. See [alternatives and product choices](docs/positioning.md).

## More than one repository

```sh
file-review /path/to/api /path/to/web --no-open
file-review --config examples/repositories.json --repo example-app --terminal
file-review /path/to/project --plan --task "Make export changes easier to test"
file-review /path/to/project --json
file-review /path/to/project --include-untracked --seconds 90 --max-mib 24
file-review /path/to/project --output report.html --no-open
```

The example configuration is a template: create your own paths first. Paths in a configuration are relative to that file. `--repo` selects configured names; positional paths and configuration cannot be mixed. Duplicate roots or ambiguous folder names are rejected. `--output` creates a new private HTML file and refuses existing files, including links. Shell redirection such as `> report.json` follows your shell's overwrite and permission rules.

## Privacy and limits

Reports include repository names, absolute root paths, filenames, measurements, content fingerprints and any task you enter; they exclude source contents. Treat real reports as private. The report contacts no external service, but copying a request into another tool shares those paths with that tool. Default reports are unique private files in the system temporary folder and are not automatically deleted; remove them when finished. Refresh by running a new scan: browser reload keeps the same snapshot.

Only valid UTF-8 without NUL bytes is measured. Blank lines and comments count. Default limits: 16 MiB per file, 60 seconds total, 100,000 attempted paths. Symlinks are not followed; submodules are not traversed. Changed, missing, linked, oversized and unreadable files remain explicit gaps. A stalled filesystem read can exceed the time budget; this is a cooperative bound, not a hard real-time guarantee. See [measurement and safety](docs/behavior.md) for exact coverage and exit codes.

## Public history

This is the initial public snapshot of a previously private tool. Private development history and configuration are intentionally excluded. Future changes are recorded here.

## Project guide

[Usage and troubleshooting](docs/usage.md) · [Architecture](docs/architecture.md) · [Contributing and tests](CONTRIBUTING.md) · [Security](SECURITY.md) · [Release checklist](docs/releasing.md) · [Changelog](CHANGELOG.md)

Early public version, licensed under [MIT](LICENSE). See [supported platforms and verification limits](docs/readiness.md) before relying on platform or testing claims.
