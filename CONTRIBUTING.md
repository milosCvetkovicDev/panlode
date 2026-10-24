# Contributing

Thanks for taking the time. Bug reports, recipe improvements and small, focused pull requests are all
welcome.

## Ground rules

- **Standard library only.** The engine and the tests must run on a bare Python 3.10 or newer, with
  nothing to install. Hooks run on every write in someone's Claude Code session; a dependency there is
  a liability.
- **Tests first.** Write the failing test, watch it fail, then make it pass. Every behaviour change in
  `template/scripts/` comes with a test in `template/scripts/tests/`; installer and repository changes
  with a test in `tests/`.
- **bash 3.2.** `install.sh` must run on the bash that ships with macOS: no `mapfile`, no associative
  arrays, no `${var,,}`.
- **Real sources only.** Example signals and docs never contain invented URLs, companies, quotes or
  numbers, and never personal data of private individuals.
- **Small pull requests**, one concern each, with a [Conventional Commits](https://www.conventionalcommits.org/)
  title (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).

## Run the checks

```bash
# engine unit tests
cd template && python3 -I -m unittest discover -s scripts/tests -t scripts && cd ..

# installer, plugin manifests, example run, demo image, Markdown links, template hygiene
python3 -m unittest discover -s tests -t .

# plugin and marketplace manifests, with the Claude Code CLI
claude plugin validate .
```

CI runs both test suites on Python 3.10 to 3.15 on Linux and on Python 3.14 on macOS, then installs into
an empty folder and runs `check` and `brief` there. It does not run `claude plugin validate`.

## Where things live

| Path | What |
|---|---|
| `template/` | Everything a user's workspace gets. Changes here reach users through `install.sh --force`. |
| `template/scripts/ideaengine/` | The engine. See [Architecture](docs/architecture.md). |
| `template/.claude/skills/scout-online/sources/` | Scouting recipes. A new recipe is a Markdown file; keep it to public pages and businesses. |
| `install.sh` | The installer. |
| `.claude-plugin/`, `plugin/skills/` | The Claude Code plugin and marketplace: `init` and `update`, which run `install.sh`. No hooks. |
| `.github/assets/` | Logo, demo and social image. `src/make_demo.py` and `src/render.sh` regenerate them. |
| `tests/` | Repository-level tests. |
| `examples/` | Real runs. Do not edit signals by hand beyond removing personal data. |
| `docs/` | The documentation site (GitHub Pages, Just the Docs). |

## Adding a scouting recipe

Copy one of the files in `template/.claude/skills/scout-online/sources/`, keep its sections (Where,
Search patterns, What counts as a signal, Evidence hints, Known noise, Caps), add the new file to the
dispatch list in `template/.claude/skills/scout-online/SKILL.md` if it should run by default (three scouts at most per
run), and add any new domains to the `WebFetch` allow list in `template/.claude/settings.json`.

## Releasing

1. Move the `Unreleased` entries in `CHANGELOG.md` under a new `## [X.Y.Z] - YYYY-MM-DD` heading and
   update the compare links at the bottom.
2. Set the same version in `.claude-plugin/plugin.json`. `tests/test_plugin.py` fails when the two
   disagree. Plugin users get the update only when the version changes.
3. Merge to `main` with CI green, tag `vX.Y.Z` and publish a GitHub release with the changelog section.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you agree to
uphold it.
