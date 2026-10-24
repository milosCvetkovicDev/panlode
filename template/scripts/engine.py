#!/usr/bin/env python3
"""Idea engine CLI: check, index, brief, next-id, slug, and the Claude Code hook entry point.

Standard library only. Runs as `python3 scripts/engine.py ...` (Python 3.10 or newer), also under `-I`.
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# -I drops the script's folder from sys.path; put it back so `ideaengine` imports.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ideaengine.hooks import run_hook, write_index  # noqa: E402
from ideaengine.report import render_brief  # noqa: E402
from ideaengine.text import slugify  # noqa: E402
from ideaengine.workspace import check, load, next_id  # noqa: E402

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
HOOKS = ("pre-write", "post-write", "stop", "session-start")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engine.py", description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="workspace root (default: repo root)")
    sub = parser.add_subparsers(dest="command", required=True)
    check_cmd = sub.add_parser("check", help="validate every record; exit 1 on any error")
    check_cmd.add_argument("--file", help="only report issues for this repo-relative path")
    sub.add_parser("index", help="regenerate INDEX.md")
    brief_cmd = sub.add_parser("brief", help="print the session brief")
    brief_cmd.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    id_cmd = sub.add_parser("next-id", help="print the next free id")
    id_cmd.add_argument("prefix", choices=("sig", "idea", "exp"))
    slug_cmd = sub.add_parser("slug", help="print an ASCII file-name slug")
    slug_cmd.add_argument("text", nargs="+")
    hook_cmd = sub.add_parser("hook", help="Claude Code hook entry point; reads the event JSON on stdin")
    # No argparse choices: its exit 2 would read as "block" to Claude Code (see main).
    hook_cmd.add_argument("name", help=", ".join(HOOKS))
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)
    root = args.root.resolve()

    if args.command == "check":
        issues = [i for i in check(root) if args.file is None or i.path == args.file]
        for issue in issues:
            print(issue)
        errors = sum(i.level == "error" for i in issues)
        print(f"{errors} error(s), {len(issues) - errors} warning(s)")
        return 1 if errors else 0
    if args.command == "index":
        print("INDEX.md updated" if write_index(root) else "INDEX.md unchanged")
        return 0
    if args.command == "brief":
        print(render_brief(load(root)[0], args.today or date.today()), end="")
        return 0
    if args.command == "next-id":
        print(next_id(root, args.prefix))
        return 0
    if args.command == "slug":
        print(slugify(" ".join(args.text)))
        return 0
    if args.name not in HOOKS:
        print(f"engine.py: unknown hook {args.name!r}; .claude/settings.json is out of step with the engine, "
              f"so copy its hooks block from the template (known: {', '.join(HOOKS)})", file=sys.stderr)
        return 1
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    result = run_hook(args.name, raw, root, date.today())
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
