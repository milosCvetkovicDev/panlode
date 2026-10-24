# Startup idea workspace

This workspace finds and validates startup ideas. It is for **discovery and validation only**: no
product code lives here (a hook denies it), and anything that reaches `go` is built in a separate
repository. Ideas are ranked by **speed to the first paying customer**, not by size of the market.

## Pipeline

Observed pain is captured as a **signal** (`signals/`) with a source and an evidence score. Signals
that cluster around one sellable offer are promoted into an **idea** (`ideas/<slug>/idea.md`) with a
service version, a product version, scores and dated kill criteria. Each idea in `validating` runs one
**experiment** at a time (`experiments/`): outreach, interviews, a pre-sale or a concierge test, with a
budget of at most 100 € and a deadline of at most 14 days, ending in `continue`, `pivot` or `kill`.
**Interviews** (`interviews/`) are Mom Test notes that can promote new signals.

## Minimum weekly loop

There is no hour budget, only a floor:

- one `/scout-online` run a week;
- at least two prospect contacts logged per running experiment, with `/log-experiment`.

The session brief at start shows days since the last signal and since the last log entry. When either
passes 7, say so before anything else.

## Folders

| Path | Holds |
|---|---|
| `signals/` | `YYYY-MM-DD-<slug>.md`, one observed pain each |
| `ideas/<slug>/` | `idea.md` (the record) plus free-form research notes |
| `experiments/` | `exp-NNNN-<slug>.md` |
| `interviews/` | `YYYY-MM-DD-<slug>.md` notes; `targets-<segment>.md` prospect lists |
| `templates/` | one template per record type; copy, never edit in place |
| `founder/` | your profile, constraints and channels (a filter for ideas, never a source) |
| `archive/` | optional: older idea lists you bring in; read-only history that `ref` and `archive_ref` may cite |
| `scripts/` | `engine.py` and its `ideaengine/` package, with tests |
| `library/` | gitignored reference material; never written by Claude |

`INDEX.md` is **generated** by `scripts/engine.py index` (the hooks run it); never edit it by hand.

## Records and invariants

Records are Markdown with flat YAML frontmatter: `key: value`, `key: [a, b]` or a `  - item` block
list; no nested maps. Path-scoped rules in `.claude/rules/` load with each folder and carry the field
details. The engine enforces:

1. An idea lists at least one existing signal.
2. IDs (`sig-`, `idea-`, `exp-` plus four digits) are unique, well-formed and resolvable.
3. At most three ideas are `validating` at once.
4. Every experiment has a deadline; a `done` one has `result` and `decision`.
5. `score_total` equals the sum of the five scores.
6. File names are ASCII lowercase; get them from `engine.py slug`, never type accented letters into one.

The PostToolUse hook checks each record as it is written and shows errors at once; fix them before
moving on. Files written through Bash skip that check, so the Stop hook runs the full check and blocks
once if errors remain.

## Engine

```
python3 scripts/engine.py check            # all errors and warnings; exit 1 on error
python3 scripts/engine.py next-id sig      # also idea, exp
python3 scripts/engine.py slug '<title>'   # ASCII file-name slug; always single quotes
python3 scripts/engine.py brief            # the session brief
python3 -I -m unittest discover -s scripts/tests -t scripts   # tests
```

Standard library only (Python 3.10 or newer, no dependencies).

## Skills

- `/scout-online` sends up to three `signal-scout` agents, one per recipe, and writes the signals they
  bring back after you check them.
- `/log-experiment` appends a dated entry to an experiment's `## Log` and closes it when done.

Ideas and experiments are written from `templates/`, following `.claude/rules/ideas.md` and
`.claude/rules/experiments.md`.

## Decisions to respect

- **Founder fit filters, it never generates.** Ideas come from signals.
- **Real sources only.** Never invent a URL, a company, a quote or a number. Businesses and public
  roles only; no personal data of private individuals.
- **Money and identity data** (tax IDs, bank accounts, addresses) never go into this repository.

## Language

Converse in English. Records, docs, rules and code are in English. Outreach is written in the
prospect's language. (Change the first sentence to your own language; the skills report in it.)

## Your constraints

@founder/constraints.md
