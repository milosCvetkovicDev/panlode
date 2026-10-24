import unittest
from datetime import date

from ideaengine.report import INDEX_HEADER, render_brief, render_index
from ideaengine.workspace import load
from tests.helpers import make_workspace, to_markdown, valid_experiment, valid_idea, valid_signal

TODAY = date(2026, 10, 23)
KILL = ["2026-11-01 fewer than 3 of 10 confirm the pain"]
LOG_BODY = "\n## Log\n\n- 2026-10-21 sent 5 messages\n"


def sample_files() -> dict[str, str]:
    return {
        "signals/2026-10-16-invoice-rekey.md": to_markdown(valid_signal(captured="2026-10-16")),
        "ideas/invoice-import/idea.md": to_markdown(valid_idea(title="Invoice import")),
        "ideas/invoice-audit/idea.md": to_markdown(
            valid_idea(id="idea-0002", title="Invoice audit", status="validating", next="exp-0001", kill_criteria=KILL)
        ),
        "experiments/exp-0001-invoice-outreach.md": to_markdown(
            valid_experiment(idea="idea-0002", deadline="2026-10-20"), LOG_BODY
        ),
    }


SAMPLE = load(make_workspace(sample_files()))[0]

_overdue = sample_files()
for _n in range(2, 32):
    _overdue[f"experiments/exp-{_n:04d}-late.md"] = to_markdown(
        valid_experiment(id=f"exp-{_n:04d}", deadline="2026-10-15", created="2026-10-10")
    )
SAMPLE_WITH_30_OVERDUE = load(make_workspace(_overdue))[0]


class IndexTest(unittest.TestCase):
    def test_index_is_deterministic_and_marked(self):
        a, b = render_index(SAMPLE), render_index(SAMPLE)
        self.assertEqual(a, b)
        self.assertTrue(a.startswith(INDEX_HEADER))
        self.assertLess(a.index("idea-0002"), a.index("idea-0001"))  # validating sorts before shaped


class BriefTest(unittest.TestCase):
    def test_brief_empty(self):
        self.assertIn("Empty pipeline — start with /scout-online.", render_brief([], TODAY))

    def test_brief_overdue_and_days_since(self):
        out = render_brief(SAMPLE, TODAY)
        self.assertRegex(out, r"Overdue:.*exp-0001")
        self.assertIn("Days since last signal: 7", out)
        self.assertIn("Days since last log entry: 2", out)

    def test_brief_max_25_lines(self):
        self.assertLessEqual(len(render_brief(SAMPLE_WITH_30_OVERDUE, TODAY).splitlines()), 25)


if __name__ == "__main__":
    unittest.main()
