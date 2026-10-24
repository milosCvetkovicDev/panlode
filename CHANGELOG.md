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

[Unreleased]: https://github.com/milosCvetkovicDev/panlode/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/milosCvetkovicDev/panlode/releases/tag/v0.1.0
