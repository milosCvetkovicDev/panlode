"""Render .github/assets/demo.svg from real engine runs on the example workspace.

    python3 .github/assets/src/make_demo.py           # write demo.svg
    python3 .github/assets/src/make_demo.py --check   # exit 1 when demo.svg is stale

The brief comes from examples/first-scout-run; the check output comes from a copy of it with one
hand-written idea that breaks four rules. Nothing in the repository is modified except demo.svg.
"""

import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
ENGINE = REPO / "template" / "scripts" / "engine.py"
EXAMPLE = REPO / "examples" / "first-scout-run"
OUT = REPO / ".github" / "assets" / "demo.svg"
TODAY = "2026-10-24"

BROKEN_IDEA = """---
id: idea-0001
type: idea
title: CI failure triage for small teams
status: validating
shape: service
signals: [sig-0013, sig-0018, sig-0099]
segment: small software teams on GitHub Actions
offer: Fix and explain failing pipelines within 24 hours, 300 EUR per month
product_path: a bot that triages failed runs
price_hypothesis: 300 EUR per month per team
first_customer_days: 14
score_pain: 4
score_reach: 3
score_willingness: 3
score_speed: 4
score_fit: 5
score_total: 20
kill_criteria:
  - fewer than 3 of 20 teams reply
next: exp-0001
created: 2026-10-24
updated: 2026-10-24
---

## Problem
"""


def run(root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(ENGINE), "--root", str(root), *args],
        capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}, timeout=60,
    )
    return result.stdout.splitlines()


def transcript() -> list[tuple[str, str]]:
    lines = [("dim", "# SessionStart hook: the brief Claude sees before your first message")]
    brief = run(EXAMPLE, "brief", "--today", TODAY)
    lines += [("bold", brief[0])] + [("text", line) for line in brief[1:]]
    lines += [("blank", ""), ("dim", "# a hand-written idea with four mistakes"), ("cmd", "python3 scripts/engine.py check")]
    with tempfile.TemporaryDirectory(prefix="demo-") as tmp:
        root = Path(tmp) / "ws"
        shutil.copytree(EXAMPLE, root)
        (root / "ideas" / "ci-debugging").mkdir(parents=True)
        (root / "ideas" / "ci-debugging" / "idea.md").write_text(BROKEN_IDEA, encoding="utf-8")
        for line in run(root, "check"):
            if line.startswith("error "):
                lines.append(("err", line.removeprefix("error ")))
            else:
                lines.append(("sum", line))
    return lines


def render(lines: list[tuple[str, str]]) -> str:
    width, line_height, x, top = 820, 21, 24, 56
    height = top + line_height * len(lines) + 22
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">',
        '<title id="t">Session brief and engine check</title>',
        '<desc id="d">The session brief for a workspace with 16 signals, then engine.py check reporting four errors in a '
        "hand-written idea: an undated kill criterion, a score total that does not add up, and two unknown ids.</desc>",
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:13.5px}'
        ".dim{fill:#8b8f98}.text{fill:#d7dae0}.bold{fill:#ffffff;font-weight:700}.cmd{fill:#ffffff}.p{fill:#7ee787}"
        ".e{fill:#ff7b72;font-weight:700}.err{fill:#d7dae0}.sum{fill:#ffa657;font-weight:700}.title{fill:#9da3ad;font-size:12.5px}</style>",
        f'<rect width="{width}" height="{height}" rx="12" fill="#16181d"/>',
        f'<rect width="{width}" height="36" rx="12" fill="#22252c"/><rect y="24" width="{width}" height="12" fill="#22252c"/>',
        '<circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>',
        f'<text class="title" x="{width // 2}" y="22" text-anchor="middle">~/ideas — claude</text>',
    ]
    y = top
    for kind, text in lines:
        if kind == "cmd":
            out.append(f'<text x="{x}" y="{y}"><tspan class="p">$ </tspan><tspan class="cmd">{escape(text)}</tspan></text>')
        elif kind == "err":
            out.append(f'<text x="{x}" y="{y}"><tspan class="e">error </tspan><tspan class="err">{escape(text)}</tspan></text>')
        elif kind != "blank":
            out.append(f'<text class="{kind}" x="{x}" y="{y}">{escape(text)}</text>')
        y += line_height
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    svg = render(transcript())
    if "--check" in sys.argv[1:]:
        if OUT.read_text(encoding="utf-8") != svg:
            print(f"{OUT.relative_to(REPO)} is stale; run python3 {Path(__file__).relative_to(REPO)}")
            return 1
        return 0
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
