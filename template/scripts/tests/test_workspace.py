import unittest

from ideaengine.workspace import check, load, next_id
from tests.helpers import (
    make_workspace,
    to_markdown,
    valid_experiment,
    valid_idea,
    valid_interview,
    valid_signal,
)

KILL = ["2026-11-01 fewer than 3 of 10 confirm the pain"]


class LoadTest(unittest.TestCase):
    def test_load_skips_non_records(self):
        root = make_workspace({
            "ideas/x/research.md": "notes",
            "interviews/targets-accountants.md": "list",
            "archive/old/idea.md": "x",
            "signals/2026-10-23-a.md": to_markdown(valid_signal()),
        })
        records, issues = load(root)
        self.assertEqual([r.rel_path for r in records], ["signals/2026-10-23-a.md"])
        self.assertEqual(issues, [])

    def test_parse_errors_become_issues(self):
        root = make_workspace({"signals/2026-10-23-a.md": ""})
        self.assertEqual([str(i) for i in check(root)], ["error signals/2026-10-23-a.md: line 1: no frontmatter"])

    def test_non_utf8_file_becomes_issue(self):
        root = make_workspace({})
        (root / "signals").mkdir()
        (root / "signals/2026-10-23-a.md").write_bytes(b"---\nid: sig-0001\ntitle: \xff\n---\n")
        self.assertEqual([str(i) for i in check(root)], ["error signals/2026-10-23-a.md: file is not UTF-8 text"])


class InvariantTest(unittest.TestCase):
    def test_duplicate_ids(self):
        root = make_workspace({
            "signals/2026-10-01-a.md": to_markdown(valid_signal()),
            "signals/2026-10-02-b.md": to_markdown(valid_signal()),
        })
        paths = sorted(i.path for i in check(root) if i.message == "duplicate id sig-0001")
        self.assertEqual(paths, ["signals/2026-10-01-a.md", "signals/2026-10-02-b.md"])

    def test_dangling_references(self):
        root = make_workspace({
            "ideas/a/idea.md": to_markdown(
                valid_idea(signals=["sig-0009"], status="validating", next="exp-0009", kill_criteria=KILL)
            ),
            "experiments/exp-0001-a.md": to_markdown(valid_experiment(idea="idea-0009")),
        })
        got = {(i.path, i.message) for i in check(root)}
        self.assertIn(("ideas/a/idea.md", "unknown id sig-0009 in signals"), got)
        self.assertIn(("ideas/a/idea.md", "unknown id exp-0009 in next"), got)
        self.assertIn(("experiments/exp-0001-a.md", "unknown id idea-0009 in idea"), got)

    def test_wip_limit(self):
        files = {
            "signals/2026-10-01-a.md": to_markdown(valid_signal()),
            "experiments/exp-0001-a.md": to_markdown(valid_experiment()),
        }
        for n in range(1, 5):
            files[f"ideas/i{n}/idea.md"] = to_markdown(
                valid_idea(id=f"idea-000{n}", status="validating", next="exp-0001", kill_criteria=KILL)
            )
        message = "4 ideas are validating; the limit is 3"
        self.assertEqual(len([i for i in check(make_workspace(files)) if i.message == message]), 4)
        del files["ideas/i4/idea.md"]
        self.assertEqual([i for i in check(make_workspace(files)) if "validating" in i.message], [])

    def test_check_clean_workspace(self):
        root = make_workspace({
            "signals/2026-10-20-invoice-rekey.md": to_markdown(
                valid_signal(status="promoted", cluster="invoices", ideas=["idea-0001"])
            ),
            "ideas/invoice-import/idea.md": to_markdown(valid_idea(status="validating", next="exp-0001", kill_criteria=KILL)),
            "experiments/exp-0001-invoice-outreach.md": to_markdown(valid_experiment()),
            "interviews/2026-10-23-accountant.md": to_markdown(valid_interview(promoted_to=["sig-0001"])),
        })
        self.assertEqual(check(root), [])


class NextIdTest(unittest.TestCase):
    def test_next_id(self):
        self.assertEqual(next_id(make_workspace({}), "sig"), "sig-0001")
        root = make_workspace({
            "signals/2026-10-01-a.md": to_markdown(valid_signal(id="sig-0001")),
            "signals/2026-10-02-b.md": to_markdown(valid_signal(id="sig-0007")),
            "signals/2026-10-03-c.md": "---\nid: sig-0012\n",  # malformed, but its id still counts
        })
        self.assertEqual(next_id(root, "sig"), "sig-0013")


if __name__ == "__main__":
    unittest.main()
