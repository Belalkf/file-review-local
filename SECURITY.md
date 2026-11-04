# Security and privacy

The current 0.1.x line receives fixes on a best-effort basis. No audit, sandbox or hard real-time guarantee is claimed.

## Reporting a vulnerability

Use the repository's GitHub **Security → Advisories → Report a vulnerability** option when enabled. If it is unavailable, open an issue asking for a private reporting channel without publishing exploit details, private paths or source contents. A maintainer must enable private vulnerability reporting after publication; no personal email or external reporting service is embedded here.

## Trust boundary

The application never imports scanned code or launches an AI tool. It invokes the installed Git executable only for path discovery, with inherited Git redirection variables removed, global/system Git configuration disabled and filesystem monitor hooks disabled. Repository Git metadata is still read; keep Git patched and scan repositories you trust. It is not a malware sandbox.

File reads reject symlinks and non-regular files and detect ordinary changes during measurement. This reduces accidental traversal and stale results; it does not guarantee a consistent snapshot under adversarial filesystem mutation. Local storage or Git can stall beyond cooperative deadlines. Inventory output is buffered in memory before the attempted-file cap applies. Avoid enormous or hostile repositories on constrained machines.

HTML payloads escape markup, labels use text nodes and the report's content policy blocks external connections. A hostile filename can still mislead a person or an AI when copied elsewhere. Review the request and treat quoted paths as data. Real reports contain sensitive names and absolute paths. Clipboard sharing is a deliberate action; no remote service receives the report from this tool.

## Files created

HTML output uses exclusive creation and owner-only permissions on supported systems. Existing paths are never replaced by the tool. Real reports are not automatically deleted. Output write failures may leave a partial owned file; remove it before retrying. JSON written by shell redirection inherits your shell's behavior. Do not publish real scan output in issues, screenshots or commits.
