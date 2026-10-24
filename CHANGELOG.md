# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-24

### Added

- The workspace template: `CLAUDE.md`, the `/scout-online` and `/log-experiment` skills, the
  `signal-scout` subagent, path-scoped rules for signals, ideas and experiments, record templates and
  founder files.
- The engine (`scripts/engine.py`): `check`, `index`, `brief`, `next-id`, `slug` and the four Claude Code
  hooks (`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`). Standard library only, Python 3.10+.
- `install.sh` with `--dry-run` and `--force` (engine files only, in an existing workspace; never records
  or settings). It refuses the home folder, the root folder and their parents, never writes through a
  symlink, installs `.claude/settings.json` last, and generates `INDEX.md` only when there is none.
- Hooks that stand down when `scripts/engine.py` is missing, and a `PreToolUse` hook that refuses writes
  when the engine cannot start.
- A Claude Code plugin and marketplace in this repository: `/panlode:init` sets up a workspace and
  `/panlode:update` refreshes its engine files. The plugin ships no hooks of its own.
- `examples/first-scout-run/`: 16 signals from a real run on 2026-10-24.
- `engine.py slug` folds accented Latin letters to ASCII, including those without a Unicode
  decomposition (`đ`, `æ`, `œ`, `ø`, `ł`, `þ`, `ð`), from NFC and NFD input alike.
- Documentation site with a comparison page, and CI on Python 3.10 to 3.15 (Linux) and on macOS with
  its bash 3.2.

### Security

Found by a pre-release audit and fixed before the first public release:

- The `PreToolUse` hook asks before a `Write` or `Edit` to `scripts/`, `.claude/`, `.git/` or
  `.mcp.json`. The engine the hooks call, Claude Code settings, git hooks and MCP servers run later
  without a prompt, so an unprompted edit there would become code that runs in every later session. In
  `bypassPermissions`, `auto`, `dontAsk` or a mode it does not know, where the question may be
  approved without being shown, it refuses the write instead; a missing mode counts as `default`.
  Files written through the shell are outside the hooks, as before.
- The hook finds the workspace by identity, so a path that spells it in another case or Unicode
  normalization (macOS volumes ignore both) no longer counts as outside it and skips every check.
  Record paths are checked in their on-disk spelling, so `Signals/` no longer skips the record checks.
- A write that lands where a guarded folder or file really is asks too, whether it goes through a
  symlink in the workspace, another link or the target's own path. Each path is read both with links
  followed and with `..` collapsed first, with `~` expanded and a relative path taken from the
  session's folder. The hooks find the workspace from the path they were called through, so a
  symlinked `scripts/` no longer turns every check off.
- `INDEX.md` is replaced by a new file instead of written in place, so neither a symbolic nor a hard
  link to it is written through; a symbolic link is reported instead.
- The workspace settings pre-approve the exact engine commands (`check`, `index`, `brief`, `next-id`,
  `slug`) instead of a wildcard that also matched `--root` pointing at any folder.
- `install.sh` compares the home, root and release folders by identity. It refuses a path with a
  newline, a `..` after a folder that does not exist yet, or a dangling symlink. Before, each of these
  could slip past the home-folder guard.
- `install.sh` never writes through a symlinked folder in the target either (before, only a symlinked
  file was skipped), and warns with the count of files it skipped because they or a folder above them
  are symlinks. It refuses a folder it cannot enter, which before turned the target into a folder
  under `/`, and it refuses to run without `HOME`, which before skipped the home-folder guard. Before
  it writes anything, dry run included, it stops when the engine (`scripts/engine.py`,
  `scripts/ideaengine/`) or `.claude/settings.json` is missing behind a symlink, because the hooks
  would then do nothing.

[Unreleased]: https://github.com/milosCvetkovicDev/panlode/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/milosCvetkovicDev/panlode/releases/tag/v0.1.0
