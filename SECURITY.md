# Security policy

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please report security issues privately through GitHub's
[private vulnerability reporting](https://github.com/milosCvetkovicDev/panlode/security/advisories/new),
not in a public issue. Include the version or commit, the steps to reproduce and the impact you expect.

## Scope

The parts most worth a look:

- **Hooks** (`template/scripts/ideaengine/hooks.py`): they run on every `Write` and `Edit` in a Claude
  Code session and read the event JSON from stdin.
- **Untrusted page text**: scouts return text from public web pages. The `/scout-online` skill must
  only copy fields from it and never follow instructions inside it.
- **The installer** (`install.sh`): it writes into a folder the user names and must never overwrite
  records or settings.

Out of scope: the behaviour of Claude Code itself and of the websites the scouts read.
