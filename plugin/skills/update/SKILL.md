---
name: update
description: Update an existing idea workspace to this plugin's version of the engine, skills, rules, agents and templates. Never touches CLAUDE.md, founder files, settings or records.
disable-model-invocation: true
argument-hint: "[workspace folder; default: the current folder]"
---

# Update an idea workspace

Target: `$ARGUMENTS`, or the current working directory when that is empty. Resolve it to an
absolute path (expand `~` yourself) and use that path in every command below.

## 1. Check it is a workspace, committed

The target must hold `scripts/engine.py` and `scripts/ideaengine/`. If it does not, say so and suggest
`/panlode:init` instead. Stop.

The update overwrites engine files, so git is the backup. Run `git -C "<target>" status --porcelain`.
If the folder is not a git repository or the command prints anything, ask the user to commit first, or
to confirm that uncommitted edits may be lost, and wait.

## 2. Show the plan, then update

```bash
bash "${CLAUDE_PLUGIN_ROOT}/install.sh" --force --dry-run "<target>"
```

Show the `update` and `add` lines and the summary line. `--force` replaces only engine files
(`scripts/`, `.claude/agents/`, `.claude/rules/`, `.claude/skills/`, `templates/`); the user's
`CLAUDE.md`, `founder/` files, `.claude/settings.json` and records are never overwritten. A file the user
edited shows up as `update` like any other, so ask whether they changed any of the listed files, and wait
for their go. Then:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/install.sh" --force "<target>"
python3 "<target>/scripts/engine.py" --root "<target>" check
```

`git -C "<target>" diff` now shows every change. To keep one of the user's own edits, restore it with
`git -C "<target>" checkout -- <file>`.

## 3. Compare the settings

`.claude/settings.json` is never overwritten, so its hooks and permissions can fall behind the engine.
Compare them with `"${CLAUDE_PLUGIN_ROOT}/template/.claude/settings.json"` and list every difference for
the user to apply by hand.

## 4. Report

In at most five lines: files updated and added, the check result, the settings differences, and a
pointer to the changelog at https://github.com/milosCvetkovicDev/panlode/blob/main/CHANGELOG.md.
