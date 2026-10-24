---
name: init
description: Set up a startup idea workspace (signals, ideas, experiments, the engine, its hooks, the /scout-online and /log-experiment skills) in an empty folder. Never overwrites an existing file.
disable-model-invocation: true
argument-hint: "[target folder; default: the current folder]"
---

# Set up an idea workspace

Target: `$ARGUMENTS`, or the current working directory when that is empty. Resolve it to an absolute
path and say which folder you are about to use.

## 1. Look before writing

List the target (it may not exist yet; that is fine). Stop and suggest a new, empty folder such as
`~/ideas` instead when:

- the target is the home folder, the root folder or a parent of the home folder: its `.claude/` and
  `CLAUDE.md` would apply to every project below it (the installer refuses these too);
- the target, or a parent folder up to the home folder, is a code project: a `package.json`,
  `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, a `src/` folder, or source files. The workspace
  hooks refuse product code, so a workspace must never share a folder with one;
- the target holds files of its own and is not a workspace: ask first.

When the target already holds `scripts/engine.py` and `scripts/ideaengine/`, it is a workspace already:
suggest `/panlode:update` and stop.

## 2. Install

Run the dry run, show its summary line, and wait for the user's go:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/install.sh" --dry-run "<target>"
```

Then install:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/install.sh" "<target>"
```

The installer never overwrites a file. If it prints a warning that Python 3.10 or newer was not found
as `python3`, tell the user: the engine and the hooks need it.

## 3. Hand over

Report in at most six lines:

- the folder and how many files were added;
- if the folder is not a git repository yet: `cd "<target>" && git init`;
- fill in `founder/profile.md`, `founder/constraints.md` and `founder/channels.md`;
- then start a new Claude Code session in that folder, so its `CLAUDE.md`, rules and hooks load, and run
  `/scout-online`.
