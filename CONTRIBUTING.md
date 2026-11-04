# Contributing

File Review welcomes focused improvements that make local review easier without changing scanned projects. Start with the [architecture](docs/architecture.md) and [behavior contract](docs/behavior.md). Read [AGENTS.md](AGENTS.md) if you use a coding agent.

## Local checks

No Python test dependencies are required:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_*.cjs
python3 scripts/check_public.py
python3 -m file_review --demo --no-open
```

Node 20+ is needed only for report-control tests. Python tests use temporary synthetic Git repositories, never a real project. Do not commit generated real reports or local configuration. The browser harness checks controls; it does not replace visual or accessibility review.

## Changes and reports

Use a feature branch and a pull request: `main` blocks direct pushes, force pushes and deletion. Resolve review conversations and wait for the required checks against the current base before merging. Human approval is optional for the solo maintainer; automated checks do not replace review. See [GitHub protections](docs/hosting.md) for the maintained policy.

For a defect, describe the visible problem, add a failing regression, make the smallest coherent repair and rerun the affected tests. Review related failure paths and the complete diff before delivery. Documentation and interface text stay in English, with clear responsibilities and unwrapped paragraphs. Do not add dependencies or network behavior without a concrete need.

Use the GitHub issue forms for bugs and features. Share synthetic filenames and redacted diagnostics only. Describe OS, Python/Git versions, command, expected result, actual result and exit code. Avoid uploading private reports. Send security concerns through [SECURITY.md](SECURITY.md).

By contributing, you agree your contribution may be distributed under the repository's MIT license. Be respectful and focus reviews on behavior, evidence and maintainability. No response-time or long-term support guarantee is promised.

## Check packaging

Using an existing setuptools/wheel installation, build into a new empty output directory (do not reuse old artifacts):

```sh
python3 -c "from setuptools.build_meta import build_wheel; build_wheel('dist')"
python3 -c "from setuptools.build_meta import build_sdist; build_sdist('dist')"
python3 scripts/check_wheel.py dist
```

These builds create local build metadata; they do not publish. The check builds another wheel from the source archive without an index, installs both wheels in a temporary environment and removes that environment afterward. It requires pip, setuptools and wheel in the calling environment. Run source tests and privacy checks before building. If the skills CLI is already installed, check discovery with `npx --no-install skills add . --list`; do not download it implicitly for tests.
