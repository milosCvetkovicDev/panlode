import unittest

from ideaengine.frontmatter import FrontmatterError, parse


class ParseTest(unittest.TestCase):
    def test_scalars_and_body(self):
        f, body = parse("---\nid: sig-0001\ntitle: Accountants re-key supplier invoices\n---\nBody\n")
        self.assertEqual(f, {"id": "sig-0001", "title": "Accountants re-key supplier invoices"})
        self.assertEqual(body, "Body\n")

    def test_inline_and_block_lists(self):
        f, _ = parse(
            "---\nrelated: [sig-0002, sig-0003]\nideas: []\nkill_criteria:\n"
            "  - 2026-11-01 fewer than 3 replies\n  - 2026-11-15 no pre-sale\n---\n"
        )
        self.assertEqual(f["related"], ["sig-0002", "sig-0003"])
        self.assertEqual(f["ideas"], [])
        self.assertEqual(f["kill_criteria"], ["2026-11-01 fewer than 3 replies", "2026-11-15 no pre-sale"])

    def test_hash_and_colon_inside_values_are_data(self):
        f, _ = parse(
            "---\n# a comment line\nref: https://news.ycombinator.com/item?id=1#c2\n"
            "title: Ops: manual invoices\n---\n"
        )
        self.assertEqual(f, {"ref": "https://news.ycombinator.com/item?id=1#c2", "title": "Ops: manual invoices"})

    def test_quoted_scalars_are_unquoted(self):
        f, _ = parse("---\ntitle: \"a, b\"\npain: 'x'\n---\n")
        self.assertEqual((f["title"], f["pain"]), ("a, b", "x"))

    def test_bom_and_crlf(self):
        self.assertEqual(parse("﻿---\r\nid: sig-0001\r\n---\r\nBody\r\n"), ({"id": "sig-0001"}, "Body\n"))

    def test_errors_carry_line_numbers(self):
        cases = [
            ("", 1, "no frontmatter"),
            ("---\nid: x\n", 2, "not closed"),
            ("---\nid: a\nid: b\n---\n", 3, "duplicate key"),
            ("---\nmeta:\n  a: b\n---\n", 3, "nested maps are not supported"),
        ]
        for text, line, msg in cases:
            with self.subTest(text=text):
                with self.assertRaises(FrontmatterError) as cm:
                    parse(text)
                self.assertEqual(cm.exception.line, line)
                self.assertIn(msg, str(cm.exception))


if __name__ == "__main__":
    unittest.main()
