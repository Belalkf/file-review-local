# GitHub protections

The public repository is [Belalkf/file-review-local](https://github.com/Belalkf/file-review-local). These settings protect its delivery workflow; they do not change what the local scanner does. The original private repository is outside this policy.

## Main branch

The active `main-safety` ruleset covers the default branch, including its owner, with no bypass actors. It blocks branch deletion and force pushes, requires a pull request, requires review conversations to be resolved and requires the four Linux/macOS × Python 3.9/3.13 checks and dependency review from the GitHub Actions app. CodeQL results must be present and free of moderate-or-higher security alerts and code errors. A pull request must be tested against the current base branch. Zero human approvals are required so a solo maintainer can merge their own reviewed work. This is not independent human review.

Use a feature branch, open a pull request, inspect its changes and checks, then merge after the gates pass. Do not disable rules to push directly to `main`. Merged branches are deleted automatically. Platform checks run on pull requests and pushes to `main`, avoiding duplicate feature-branch runs. Changes to check names or the platform matrix need a matching ruleset update so a removed check cannot leave merging blocked.

`python3 scripts/check_hosting.py` reads the public effective branch rules with a 20-second network timeout and reports missing protections. It changes no settings, reads no local source and needs no credentials. Its regression tests reject an unprotected branch, missing guards, missing/spoofed platform checks, stale-base checks, unresolved-conversation settings and missing or relaxed CodeQL gates. It checks the branch policy, not every security setting or bypass configuration; administrators should also review the ruleset details.

## Automated checks

| Protection | Configuration and boundary |
| --- | --- |
| Dependabot alerts | Enabled; identifies known vulnerable dependencies recognized by GitHub's dependency graph |
| Dependabot security updates | Enabled; proposes fixes as pull requests, without automatic merging |
| Version updates | Weekly for GitHub Actions and Python build tools; compatible minor/patch updates are grouped, with at most three open requests per ecosystem |
| Dependency review | Pull requests are checked for newly introduced known moderate-or-higher vulnerabilities in runtime, development and unknown scopes; missing dependency snapshots can cause a visible failure |
| CodeQL | Default hosted setup for Python, JavaScript/TypeScript and GitHub Actions, using extended security queries; analysis includes local input sources because this tool processes local files and command-line arguments |
| Secret scanning and push protection | Enabled for supported provider patterns; detection is not proof that a source tree contains no secrets |
| Private vulnerability reporting | Enabled; use the channel linked in [SECURITY.md](../SECURITY.md) |

Dependency review uses a pinned official GitHub action, read-only repository permissions, a five-minute job limit and up to 120 seconds of snapshot retries. It writes its findings to the workflow result, without write access for pull-request comments. Dependency update requests still need review and successful checks; a newer version is not automatically trusted.

## Actions access and deliberate limits

Default workflow tokens are read-only and cannot approve pull requests. Workflows from all external fork contributors require maintainer approval. The hosted security scanners use their necessary GitHub-managed permissions; no third-party review bot, personal token in the repository, self-hosted runner or paid AI review service was added.

Existing provider-pattern secret scanning and push protection are kept enabled. Generic non-provider patterns and secret validity checks remain off; checking token validity can contact its provider and is not needed for this initial baseline. Other account-wide settings and personal notifications were not changed. CodeQL, dependency review and passing tests do not certify absence of vulnerabilities or replace a person's review.

## Verification

The repository reports `main` as protected, and the effective public rules pass `scripts/check_hosting.py`. The security settings were read back after changes. Hosted scan results and the first protected pull-request journey are linked from [release readiness](readiness.md); a feature being enabled is separate from its analysis succeeding.

Policy references: [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), and [CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning).
