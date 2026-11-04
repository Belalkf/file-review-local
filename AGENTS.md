# Maintainer entry point

Read README.md, docs/architecture.md and docs/behavior.md before changing behavior. This repository is independent: do not rely on sibling folders, private paths, global preferences or external continuation documents.

## Product boundary

The scanner reads local files. Never execute scanned project code, run agents, upload source, install packages at runtime or modify scanned repositories. Preserve originals, refuse unsafe inputs and show incomplete coverage explicitly. Synthetic examples must contain no real user or repository details.

## Change discipline

Keep discovery, safe measurement, presentation and command handling separate. Add a regression test for every defect. Review the entire change and wider user journey after implementation, including invalid inputs, cancellation, incomplete scans, filenames with markup and preservation of existing files. Run focused checks appropriate to the change; report unexecuted checks honestly.

Split only at useful responsibility boundaries. Size alone never requires splitting data, connected formats or cohesive source. Prefer fewer clear owners to scattered helpers. Aim below 150 lines for authored modules and documents; explain specific exceptions in docs/architecture.md with a reason and revisit condition. Do not compress code or prose to satisfy a count. Keep documentation paragraphs unwrapped.

## Delivery

Use the commands in CONTRIBUTING.md. Keep jobs owned, cancellable and bounded. Do not alter unrelated work, weaken protections, download dependencies or publish without authorization. Inspect staged files and Git metadata for private information before committing. State implemented behavior, missing behavior and actual validation separately. No automatic new agent sessions.
