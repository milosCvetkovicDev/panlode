---
title: Getting started
nav_order: 2
description: "Install the Panlode workspace for Claude Code, describe your constraints, and run the first /scout-online pass for startup idea signals."
---

# Getting started
{: .no_toc }

Ten minutes from install to the first scouting run.
{: .fs-6 .fw-300 }

1. TOC
{:toc}

---

## Requirements

- [Claude Code](https://code.claude.com/docs/en/overview), signed in.
- `git`.
- Python 3.10 or newer, reachable as `python3`. The engine uses the standard library only; there is
  nothing to `pip install`.
- macOS or Linux. The installer is plain bash and also runs on the bash 3.2 that ships with macOS.
  On Windows, use WSL.

## 1. Install the workspace

Pick a new, empty folder: the workspace refuses product code, so it never shares a folder with a code
project. Two ways to fill it, with the same result.

**With the Claude Code plugin** (Claude Code 2.1.295 or later). In any Claude Code session:

```text
/plugin install panlode --marketplace milosCvetkovicDev/panlode
/panlode:init ~/ideas
```

`/panlode:init` checks that the folder is not a code project, shows the plan, then runs the
installer. The plugin itself adds only `/panlode:init` and `/panlode:update`; it installs no hooks,
so other projects are not affected.

**With git.** From your shell:

```bash
git clone https://github.com/milosCvetkovicDev/panlode.git
panlode/install.sh ~/ideas
```

Then put the workspace under version control:

```bash
cd ~/ideas && git init && git add -A && git commit -m "chore: start the idea workspace"
```

The installer copies `template/` into the folder you name and **never overwrites a file that already
exists**. It prints a line for each file it adds (`add`) or leaves alone because yours differs or it is a
symlink or sits in a symlinked folder (`skip`), and a summary; it generates `INDEX.md` only when the folder has none. It refuses your
home folder, the root folder and any parent of the home folder, because a workspace's `.claude/` and
`CLAUDE.md` would then apply to every project below it, and a path with a `..` after a folder that
does not exist yet. Useful options:

| Option | Effect |
|---|---|
| `--dry-run` | Print the plan; write nothing. |
| `--force` | In an existing workspace only, refresh the engine files: `scripts/`, `.claude/agents/`, `.claude/rules/`, `.claude/skills/`, `templates/`. Your `CLAUDE.md`, `founder/` files, `.claude/settings.json` and records are never touched. Commit first: an engine file you edited is replaced too, and git brings it back. `/panlode:update` runs this for you. |

## 2. Describe yourself, briefly

Open the three files in `founder/` and replace every `<placeholder>`:

| File | What to write | What it feeds |
|---|---|---|
| `profile.md` | what you can build and deliver fast | `score_fit`, `score_speed` |
| `constraints.md` | capital, budget, capacity, and **vetoes**: the kinds of business you will not do | every session (imported into `CLAUDE.md`) and the scouts' skip list |
| `channels.md` | where you can actually reach prospects | `score_reach` |

The founder files **filter** ideas; they never generate them. "I could build this" is not a signal.

If you want Claude to converse in another language, change the first sentence of the `Language`
section in `CLAUDE.md`. Records stay in English unless you decide otherwise; file names are always ASCII.

## 3. Start Claude Code

```bash
claude
```

The `SessionStart` hook gives Claude the brief. In an empty workspace it reads:

```text
Idea engine — 2026-10-24
Empty pipeline — start with /scout-online.
Minimum loop: one /scout-online per week; ≥2 prospect contacts logged per running experiment.
```

## 4. Scout

```text
/scout-online
/scout-online accounting firms e-invoicing     # optional focus
```

Three `signal-scout` subagents run in parallel, one per recipe in
`.claude/skills/scout-online/sources/`: freelance and job posts, review sites, Reddit and forums. Each
returns at most eight candidates with a source link, plus the searches that led nowhere. Claude
removes duplicates and anything that hits a veto, scores the evidence (taking the lower score when
unsure), writes each kept candidate to `signals/` and prints a digest with suggested clusters.

Every write goes through the hooks: a malformed record is reported at once and fixed before the next.

## 5. From signals to an idea

When two or more signals share a segment or a pain, mark them `clustered` with the same `cluster`
slug. When a cluster has enough evidence (the digest suggests it once three signals score 3 or more),
shape an idea:

```bash
python3 scripts/engine.py next-id idea          # e.g. idea-0001
python3 scripts/engine.py slug "Invoice import for small accounting firms"
```

Ask Claude to write `ideas/<slug>/idea.md` from `templates/idea.md`. The rules for ideas load
automatically when Claude works in `ideas/`.

## 6. Run one experiment

Write the experiment from `templates/experiment.md`, in this order so every reference resolves:

1. the idea with `status: shaped`;
2. the experiment with `idea: idea-NNNN`, a `success_metric` (numeric where possible), a `budget_eur`
   and a `deadline`;
3. the idea set to `validating`, with `next: exp-NNNN` and dated `kill_criteria`.

Log every contact and result as it happens:

```text
/log-experiment exp-0001 sent 10 cold emails to accounting firms, 2 replies, 1 call booked
```

When the deadline passes or the metric is met, `/log-experiment` asks for `continue`, `pivot` or
`kill` and updates both records.

## 7. Check and commit

```bash
python3 scripts/engine.py check     # exit 0 means every invariant holds
git add -A && git commit -m "docs(signals): first scouting run"
```

`INDEX.md` is regenerated by the hooks; never edit it by hand. Next: [the weekly loop](weekly-loop.md).
