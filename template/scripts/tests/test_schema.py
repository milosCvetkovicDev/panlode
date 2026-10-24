import unittest

from ideaengine.schema import validate_record
from tests.helpers import valid_experiment, valid_idea, valid_interview, valid_signal

SIG = "signals/2026-10-23-invoice-rekey.md"
IDEA = "ideas/invoice-rekey/idea.md"
EXP = "experiments/exp-0001-invoice-outreach.md"


def msgs(issues):
    return [i.message for i in issues]


def errors(issues):
    return [i for i in issues if i.level == "error"]


class ValidateRecordTest(unittest.TestCase):
    def test_valid_records_have_no_issues(self):
        for rel, f in [
            ("signals/2026-10-23-invoice-rekey.md", valid_signal()),
            ("ideas/invoice-rekey/idea.md", valid_idea()),
            ("experiments/exp-0001-invoice-outreach.md", valid_experiment()),
            ("interviews/2026-10-23-accountant.md", valid_interview()),
        ]:
            self.assertEqual(validate_record(rel, f), [], rel)

    def test_missing_required_field(self):
        f = valid_signal()
        del f["pain"]
        self.assertIn("missing required field: pain", msgs(validate_record(SIG, f)))

    def test_enum_and_ranges(self):
        for over in [{"source": "tiktok"}, {"evidence": "6"}, {"evidence": "x"}]:
            self.assertTrue(errors(validate_record(SIG, valid_signal(**over))), over)

    def test_dates(self):
        self.assertIn(
            "invalid date in captured: 2026-02-30", msgs(validate_record(SIG, valid_signal(captured="2026-02-30")))
        )

    def test_id_format(self):
        self.assertTrue(errors(validate_record(SIG, valid_signal(id="sig-1"))))

    def test_filename_rules(self):
        self.assertIn(
            "file name must be ASCII lowercase",
            msgs(validate_record("signals/2026-10-23-računovođe.md", valid_signal())),
        )
        self.assertIn(
            "file name does not match id exp-0001",
            msgs(validate_record("experiments/exp-0002-x.md", valid_experiment())),
        )

    def test_type_matches_folder(self):
        self.assertTrue(errors(validate_record("signals/2026-10-23-x.md", valid_idea())))

    def test_conditional_fields(self):
        self.assertIn(
            "cluster is required when status is clustered",
            msgs(validate_record(SIG, valid_signal(status="clustered"))),
        )
        self.assertIn(
            "product_path is required when shape is service",
            msgs(validate_record(IDEA, valid_idea(shape="service", product_path=""))),
        )
        m = msgs(validate_record(IDEA, valid_idea(status="validating")))
        self.assertIn("kill_criteria is required when status is validating", m)
        self.assertIn("next is required when status is validating", m)
        self.assertIn(
            "kill_criteria item has no date",
            msgs(validate_record(IDEA, valid_idea(status="validating", next="exp-0001", kill_criteria=["fewer replies"]))),
        )
        m = msgs(validate_record(EXP, valid_experiment(status="done")))
        self.assertIn("result is required when status is done", m)
        self.assertIn("decision is required when status is done", m)

    def test_score_total_mismatch(self):
        self.assertIn(
            "score_total is 16 but the scores sum to 15", msgs(validate_record(IDEA, valid_idea(score_total="16")))
        )

    def test_soft_warnings(self):
        for f, rel in [
            (valid_experiment(budget_eur="150"), EXP),
            (valid_experiment(created="2026-10-01", deadline="2026-10-16"), EXP),
            (valid_signal(colour="red"), SIG),
            (valid_signal(pain="x" * 201), SIG),
        ]:
            issues = validate_record(rel, f)
            self.assertEqual([i.level for i in issues], ["warning"], f)

    def test_template_placeholder_is_error(self):
        sig = msgs(errors(validate_record(SIG, valid_signal(
            title="<one specific line: who does what painful thing>", trigger="<what makes it urgent now, or unknown>",
        ))))
        self.assertIn("template placeholder left in title", sig)
        self.assertIn("template placeholder left in trigger", sig)
        idea = msgs(errors(validate_record(IDEA, valid_idea(segment="<who pays>"))))
        self.assertIn("template placeholder left in segment", idea)
        self.assertEqual(errors(validate_record(SIG, valid_signal(pain="Costs <2h a week, says the owner>"))), [])


if __name__ == "__main__":
    unittest.main()
