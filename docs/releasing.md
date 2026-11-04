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

A PyPI upload is separate, optional work requiring authorization, name-availability checks, metadata and rendered-description review, versioned artifact checks and secure publisher setup. Before advertising the skill, publish the reviewed source through the normal authorized process, check `npx skills add Belalkf/file-review-local --list`, and verify installation for the intended agents. According to the [skills.sh FAQ](https://skills.sh/docs/faq), leaderboard listing depends on installation telemetry; verify the actual result and current rules. Source publication does not imply a registry release, adoption, demonstrated savings or an independent security audit.
