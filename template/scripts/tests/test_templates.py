import re
import unittest
from pathlib import Path

from ideaengine.frontmatter import parse
from ideaengine.schema import FIELDS

TEMPLATES = Path(__file__).resolve().parents[2] / "templates"

HEADINGS = {
    "signal": ["## Context", "## Quote", "## Why it matters", "## Open questions"],
    "idea": [
        "## Problem", "## Who", "## Why now", "## Service version", "## Product version",
        "## Reaching twenty prospects", "## Competitors", "## Risks", "## Founder fit",
    ],
    "experiment": ["## Plan", "## Where the prospects are", "## Message templates", "## Interview script", "## Log"],
    "interview": ["## Context", "## Their story", "## Costs and workarounds", "## Quote", "## Signals to promote"],
}


def is_placeholder(value) -> bool:
    if isinstance(value, list):
        return all(is_placeholder(item) for item in value)
    return value.startswith("<") and value.endswith(">")


class TemplatesTest(unittest.TestCase):
    def test_templates_match_schema(self):
        for kind, (required, optional) in FIELDS.items():
            with self.subTest(kind=kind):
                fields, body = parse((TEMPLATES / f"{kind}.md").read_text(encoding="utf-8"))
                self.assertEqual(set(fields), required | optional)
                self.assertEqual(fields["type"], kind)
                for key, value in fields.items():
                    if key != "type":
                        self.assertTrue(is_placeholder(value), f"{kind}.{key} = {value!r}")
                headings = re.findall(r"^## .+$", body, re.MULTILINE)
                for heading in HEADINGS[kind]:
                    self.assertTrue(any(h.startswith(heading) for h in headings), f"{kind}: {heading}")

    def test_experiment_body_ends_with_log(self):
        _, body = parse((TEMPLATES / "experiment.md").read_text(encoding="utf-8"))
        self.assertEqual(re.findall(r"^## .+$", body, re.MULTILINE)[-1], "## Log")
        self.assertRegex(body, r"(?m)^- <YYYY-MM-DD> <note>$")


if __name__ == "__main__":
    unittest.main()
