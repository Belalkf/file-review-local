# Supported platforms and verification

File Review is an early public edition. See [README](../README.md) for release and source installation instructions and the PyPI project page for available versions.

## Platform support

| Platform | Support and verification |
| --- | --- |
| macOS | Supported; hosted command-line, report-control and packaging checks on Python 3.9 and 3.13 |
| Linux | Supported; the same hosted checks on Python 3.9 and 3.13 |
| Native Windows | Intentionally rejected because the safe reader requires POSIX features |
| WSL | Unverified |

See the [Checks workflow](https://github.com/Belalkf/file-review-local/actions/workflows/ci.yml) for results tied to each commit, and [Contributing](../CONTRIBUTING.md) to reproduce the checks. Source tests, an in-memory browser-control harness, source guards, isolated builds and installed-command checks cover different parts of the workflow; none replaces human or accessibility review.

## Verification limits

The synthetic Firefox report was visually reviewed. The README screenshot predates the revised explanatory wording. Linux browser appearance, mobile layout, screen-reader quality and interactive Finder launcher input remain unverified. A syntax/non-interactive launcher check does not establish that interactive journey.

There is no demonstrated token saving or independent evaluation of the receiving agent's architectural decisions. The tool prepares measurements and path hints; its [behaviour contract](behavior.md) defines coverage and safety limits. Scanned source is not parsed or refactored, and no agent is started.

[GitHub protections](hosting.md) describes the contribution and scanner policy. Successful scans and source privacy patterns do not certify the absence of vulnerabilities or secrets. Exact per-change verification belongs to workflow runs and pull requests.
