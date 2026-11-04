# Usage and troubleshooting

## Choose where to run

From source, run `python3 -m file_review` in the tool checkout with a target root path. After installation, run `file-review` from anywhere. An argument-free run inspects the current folder, not the tool's installation directory. The target must be a Git root; subfolders are refused rather than silently widening the scan. Bare repositories have no working files and are unsupported.

For repeated multi-project use, copy `examples/repositories.json` to `repositories.local.json` and edit its named paths. This local filename is ignored by Git. Relative entries resolve beside that configuration file, never beside the executable. Home-directory expansion is supported. Use `--config /path/to/repositories.local.json --repo NAME` to select named projects. Unselected missing folders do not prevent a selected project from being scanned. Unknown names, duplicate JSON keys, duplicate selected roots and unknown top-level keys are rejected.

## Common situations

| What you see | What to do |
| --- | --- |
| Not a repository root | Pass the folder containing `.git`, or a worktree root |
| Git is missing | Install Git yourself; the tool never downloads it |
| Browser did not open | Open the printed HTML path manually, or use `--terminal` |
| Clipboard access denied | Select/copy the request using the offered fallback |
| No matching files | Check coverage, then choose “Show all sizes” |
| INCOMPLETE / over read limit | Inspect exclusions; increase a limit only if appropriate |
| Missing or changed files | Finish edits and rerun for a fresh snapshot |
| Existing output path | Choose a new filename; originals are preserved |
| Same target folder names | Give them distinct names in an explicit configuration |
| Native Windows | Use a supported macOS/Linux environment; WSL is unverified |

The `.command` launcher is an optional macOS convenience. It asks for a repository root, so double-clicking does not accidentally scan a configured private project list. Terminal use remains the portable route. No Finder Quick Action is installed.

## Inspect without opening a browser

```sh
file-review /path/to/project --terminal
file-review /path/to/project --json
file-review /path/to/project --plan --task "Simplify testing export behavior"
file-review /path/to/project --no-open --output /tmp/new-review.html
```

Always quote paths containing spaces. Do not paste a real report into public issues. Use `--demo` when making public screenshots or testing browser controls. Delete temporary reports when they are no longer needed. No background service or auto-refresh exists.

## Review with your agent

Open the report, optionally add your goal, then copy the starter request. Expand evidence if you want to understand a hint. Select specific files to replace the starter scope; table filters alone do not change the request. Paste it into an agent that can access the local repository. If the agent cannot read the files, it should ask for access rather than guess boundaries. Sharing only a request with a remote chat does not grant that chat local source access.

Ask for the decision table first. Keep files intact when the evidence supports it, and try selective reading before restructuring a cohesive owner. Follow the project’s existing permission rules before implementing any proposal. File Review itself never executes the request.
