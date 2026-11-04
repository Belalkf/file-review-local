# Measurement and safety contract

## Discovery

Each input must be a Git repository root. Git lists tracked paths using NUL delimiters; current filesystem contents are measured, not committed blobs. Add `--include-untracked` for non-ignored untracked files. Tracked ignored files remain included. Unmerged index paths are deduplicated. Submodules appear as unmeasured non-regular entries, not recursive scans. Sparse-checkout missing paths also make coverage incomplete.

Repositories are processed in input order. Default budget: 60 seconds and 100,000 attempted paths across all targets. Each Git invocation has at most a 10-second wait within the remaining deadline. Inventory output is buffered before the attempt cap applies. A slow filesystem read is not forcibly interrupted by the budget. Control-C cancels between interruptible operations; no worker or background process is left running by the tool.

## Measurement

Only regular files are opened. Directory and file symlinks are refused. UTF-8 decoding is strict; NUL-containing or invalid UTF-8 files are classified as expected exclusions. Other exclusions mark coverage incomplete. Each file defaults to a 16 MiB maximum; configurable up to 1,024 MiB. Scan time is configurable up to 3,600 seconds. Reading is chunked and identity/size/timestamps are checked before, after and by reopening the path. This detects ordinary concurrent edits and replacement; it is not an adversarial filesystem snapshot.

LF, CRLF and CR each count as one line ending. A final unterminated line counts; an empty file has zero lines. Blank lines and comments count. Size and longest line are bytes, excluding line-ending bytes from the longest line, not Unicode characters, rendered columns or AI tokens. A UTF-8 byte-order mark contributes bytes. The tool does not guess encoding or decode archives.

## Reports

Rows sort by descending lines, descending size, repository name and path. Terminal output shows the first 50 measured text files. HTML initially shows up to 250 matches, with more available. Selection persists when rows are filtered out. “Select visible” selects only displayed rows. Zero disables a size condition; three zeroes show all sizes. The clipboard has a selectable-text fallback.

Coverage is independent of filters: an empty table is never proof of complete coverage. HTML and JSON contain absolute roots and content SHA-256 fingerprints; neither includes source content. The JSON envelope includes `schema_version: 1`, UTC `created`, budgets, `repositories` coverage records and measured `rows`. Additive keys may appear in 0.1.x; consumers should ignore unknown keys. Breaking changes need a new schema version. HTML is a static snapshot; rerun to refresh.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Complete inventory, allowing expected binary/non-UTF-8 exclusions |
| 1 | Inventory gaps or an output failure |
| 2 | Invalid arguments/configuration or unsupported platform |
| 130 | Interrupted by Control-C |

A browser-opening failure preserves the report and prints manual-opening guidance; it does not turn a completed scan into a failure. A missing Git executable becomes an explicit incomplete inventory. A non-repository directory produces a report with a gap and exit 1; a missing input folder is rejected before scanning with exit 2.

## Review guidance

By default, measured rows receive path/format hints without another source read. `--inventory-only` omits these hints. No language is parsed and no split boundary or keep decision is certified. Three or more small text files (at most 40 lines each) in the same repository folder receive up to eight adjacency links, excluding connected-format and generated-looking paths. Small-file counts and adjacency are not evidence of over-fragmentation.

`--plan` prints a starter request for at most 12 files, prioritizing content review before format/producer checks, then descending line count and stable path order. HTML starts with the same scope regardless of table filters; its scope message says so. Selecting files replaces the starter scope and includes every selection, including hidden rows. Clear selection restores the starter. `--task` (at most 2,000 characters) adds a goal; HTML lets you change it locally. A task does not automatically match files or prove relevance. Inspect and adjust the proposed scope.

The copied request carries inventory gaps, measurement limits and the need to check current contents, project rules, callers, shared state, interfaces and tests. A SHA-256 fingerprint identifies measured bytes; it does not prove correctness or guarantee freshness. The report remains a static snapshot. Agent execution, parsing, measured token savings and automatic restructuring are not implemented.

The shared instructions appear once in each request; file entries carry quoted paths, measurements, fingerprints and format warnings. Expandable table evidence retains navigation hints without repeating them in the copied request. The request is assembled by fixed rules. Only the receiving coding agent supplies model judgment after reading source.
