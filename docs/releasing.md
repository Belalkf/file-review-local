# Maintainer release guide

## Review the public boundary

This public edition is independent of the original private tool. Preserve that separation: review patches before transferring changes, never copy private history or configuration, and never automatically synchronize the repositories. Use a repository-local public/noreply identity for both author and committer metadata.

Review the intended source, Git history, images and packaged assets for private content. Synthetic examples must remain synthetic. A pattern scan cannot certify privacy; reports of real projects contain paths and other private context and must not be included. The [architecture](architecture.md#public-boundary) owns the public source boundary.

## Prepare a release

1. Run the [contributor checks](../CONTRIBUTING.md), review the complete diff and check compatibility with supported Python versions. Review licences and network behaviour if dependencies change.
2. Build fresh wheel and source archives, verify report assets, and exercise the installed command outside the checkout using the packaging instructions in Contributing.
3. Keep the version and [changelog](../CHANGELOG.md) aligned. Describe user-visible changes, fixes, compatibility and remaining limits; leave commit-by-commit execution logs in the pull request and CI.
4. Use a feature branch and protected pull request. Wait for current-base checks, inspect actual scanner findings and preserve the [hosting policy](hosting.md). Recheck current GitHub options when changing that policy.
5. Create an annotated version tag and GitHub release only within the authorized publication scope and after its checks pass. Keep published tags stable; fixes belong in later commits/releases.

## Publish to PyPI

Publishing needs explicit authorization and a PyPI account. Before the first upload, check the package name, metadata, rendered description and source/wheel contents. Configure a [pending trusted publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) on PyPI with project `file-review-local`, owner `Belalkf`, repository `file-review-local`, workflow `publish.yml` and environment `pypi`. This permits that repository workflow to publish this package without a stored API token; a pending publisher does not reserve the name.

After the protected pull request and current-main checks pass, manually run **Publish to PyPI** from `main` in GitHub Actions. Its default run only builds and validates the distributions. Enable **Upload checked distributions to PyPI** only after the account configuration is correct. A separate `pypi` job then receives a short-lived publishing identity and uploads the checked artifacts; it does not check out or execute project source. The workflow never runs automatically on a push or pull request, and it refuses other branches.

After success, check the PyPI version and hashes, install `file-review-local` from PyPI in a fresh virtual environment, and run the demo and installed-command checks. Record the exact source commit and workflow result in the release or pull request. An upload is not an independent security audit or evidence of adoption.

## Verify skill distribution

Check `npx skills add Belalkf/file-review-local --list` and installation for the intended agents against the public source. According to the [skills.sh FAQ](https://skills.sh/docs/faq), leaderboard listing depends on installation telemetry; verify the actual result and current rules. Source publication does not imply a registry release or demonstrated savings.
