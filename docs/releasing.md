# Publication and release checklist

## Before the first GitHub push

1. Run the tests and `python3 scripts/check_public.py`. Review all tracked text, images, package contents and Git metadata; a pattern scanner cannot prove the absence of all secrets.
2. Confirm `git log --all --format=fuller` contains only this public edition and identities you intend to publish. This checkout must not share the private tool's object database, remotes or history.
3. Run the synthetic demo. Never commit or upload a real project's report, screenshot, absolute path or local configuration.
4. Choose the GitHub repository slug `file-review` if available in your account. This name is descriptive; no global trademark or package-name exclusivity is claimed.
5. Create an **empty** GitHub repository without generated README/license commits. Add that URL as `origin` in this checkout, then push `main` yourself. No publish action is part of preparing this repository.
6. Enable GitHub private vulnerability reporting; review Actions permissions and branch protection appropriate to your account. No credentials are required by the supplied checks.
7. Use the description: “Local, language-independent review briefings for thoughtful code restructuring.” Suggested topics: `python`, `developer-tools`, `git`, `code-quality`, `local-first`.

The initial local commit uses a neutral contributor identity to avoid disclosing an address. GitHub will not automatically attribute that commit to your profile. Future authorship should use your chosen public identity or GitHub-provided private email. An account URL and public credit are intentionally not guessed or embedded.

## Checks for later releases

Run the full suite, review the complete diff and changed-file responsibilities, then build both a source archive and a wheel. Verify HTML/CSS/JS assets, install the wheel in an isolated environment, and exercise the installed command outside the source folder. Review licenses and network changes if introducing dependencies. Keep the changelog and version aligned.

CI is configured for macOS/Linux and Python 3.9/3.13, with read-only repository permissions, pinned action revisions, time limits and no publishing credentials. Hosted results exist only after GitHub runs it. The local machine cannot substitute for that matrix. The maintainer may later expand the matrix after verifying compatibility.

Use an annotated `v0.1.0` tag and GitHub release only when the checks actually pass. No tag or hosted release is created by the preparation task. A PyPI upload is separate, optional work: first confirm distribution-name availability and use authenticated trusted publishing rather than committing tokens.

## Portfolio wording

Suggested CV bullet, after publication: “Built File Review, a local-first Python tool that turns Git working-copy measurements into language-independent agent review briefings and an offline dashboard, with safe file reads, explicit coverage gaps and regression tests.”

Link the actual public repository. Do not claim adoption numbers, performance savings, a security audit or platform testing that has not happened. This project is intentionally a focused tool; its credibility comes from a clear boundary and demonstrable behavior.
