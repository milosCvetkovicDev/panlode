---
title: FAQ
nav_order: 8
description: "Frequently asked questions about Panlode, the Claude Code workspace for finding and validating startup ideas."
---

# FAQ
{: .no_toc }

1. TOC
{:toc}

---

## Does it need an API key or a paid service?

No. It runs inside Claude Code and uses its built-in web search and fetch tools. The engine is
standard-library Python with no packages to install.

## How is this different from asking Claude for startup ideas?

Asking for ideas gets you plausible ideas with no evidence behind them. Here Claude never proposes an
idea from thin air: it records pain that someone wrote down in public, with the link and an evidence
score, and an idea can only be built on those records. Then it makes you test the idea cheaply before
you build anything.

## Which sources do the scouts read?

Three recipes ship with the template: freelance and job posts (Upwork, Freelancer, job boards), review
sites (G2, Capterra, Trustpilot), and Reddit and forums (a list of subreddits, Indie Hackers and industry
forums found through search). In the example run, search also led the scouts to PeerSpot reviews,
Hacker News threads, DEV posts and Microsoft Q&A. Each recipe is a Markdown file in
`.claude/skills/scout-online/sources/`; edit it or add your own.

## Can I write records in another language?

Yes. Set the conversation language in the workspace `CLAUDE.md`; the skills report in it. File names
stay ASCII: the slug helper folds accented Latin letters (`Računovođe` becomes `racunovodje`,
`Größe` becomes `grosse`).

## Can I use it without Claude Code?

The engine (`check`, `index`, `brief`, `next-id`, `slug`) and the Markdown records work on their own,
and the checks run in CI. Scouting, the skills and the hooks need Claude Code.

## Can I change the limits (100 €, 14 days, 3 ideas)?

They are constants in the engine, on purpose: limits you can raise in a settings file tend to get
raised. Going over budget or past 14 days is a warning, not an error, so an exception is possible when
you write down why. If you need different defaults, change the constants and the tests that pin them.

## Why can't I write code in the workspace?

Because the workspace is for deciding what to build. The `PreToolUse` hook refuses product files
(TypeScript, JavaScript, Go, Rust, Java, C#, Terraform, SQL, `package.json`, lockfiles, Dockerfiles)
in the workspace. In `scripts/`, `.claude/` and `.git/` it asks you first instead, because the engine
and its settings live there. An idea that reaches `go` gets its own repository.

## How do I update to a newer version?

With the plugin, run `/panlode:update`. With git, commit your workspace, pull the repository, then run
`install.sh --force <your workspace>` (try `--dry-run` first). It refreshes the engine, skills, rules,
agents and templates and never touches your `CLAUDE.md`, `founder/`, `.claude/settings.json` or
records. An engine file you edited yourself is replaced like the others: `git diff` shows it and
`git checkout -- <file>` brings your version back. Check the [changelog](https://github.com/milosCvetkovicDev/panlode/blob/main/CHANGELOG.md)
for changes to the settings that you may want to copy by hand.

## Is the example run real?

Yes. `examples/first-scout-run/` holds the 16 signals from the first `/scout-online` run on 2026-10-24,
with their source links. Only links to older, unpublished signals were removed. CI checks that the
example still passes `engine.py check`.

## What about privacy and terms of use of the sites?

Scouts read a handful of public pages per run through Claude Code's own web tools and store a
paraphrase, a link and at most one short quote. They record businesses and public roles only, never
private individuals. Respect each site's terms; if a site disallows automated access, remove it from
the recipes.
