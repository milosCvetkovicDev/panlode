import contextlib
import io
import unittest

from engine import main
from tests.helpers import make_workspace, to_markdown, valid_signal

SIG = "signals/2026-10-23-invoice-rekey.md"


def run(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


class CliTest(unittest.TestCase):
    def test_next_id_and_slug(self):
        root = str(make_workspace({}))
        self.assertEqual(run("--root", root, "next-id", "sig"), (0, "sig-0001\n"))
        self.assertEqual(run("--root", root, "slug", "Računovođe", "Größe"), (0, "racunovodje-grosse\n"))

    def test_unknown_hook_name_is_a_plain_error_not_a_block(self):
        # Exit 2 tells Claude Code to block; a settings.json older than the engine must not do that.
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                code = run("--root", str(make_workspace({})), "hook", "renamed-event")[0]
            except SystemExit as exc:
                code = exc.code
        self.assertEqual(code, 1)
        self.assertIn("settings.json", err.getvalue())

    def test_check_exit_codes(self):
        self.assertEqual(run("--root", str(make_workspace({SIG: "---\nid: sig-0001\n---\n"})), "check")[0], 1)
        self.assertEqual(run("--root", str(make_workspace({SIG: to_markdown(valid_signal())})), "check")[0], 0)

    def test_index_unchanged_is_not_rewritten(self):
        root = make_workspace({SIG: to_markdown(valid_signal())})
        run("--root", str(root), "index")
        before = (root / "INDEX.md").stat().st_mtime_ns
        run("--root", str(root), "index")
        self.assertEqual((root / "INDEX.md").stat().st_mtime_ns, before)

    def test_index_through_a_symlink_is_a_plain_error(self):
        root = make_workspace({SIG: to_markdown(valid_signal())})
        outside = make_workspace({"dotfile": "mine\n"}) / "dotfile"
        (root / "INDEX.md").symlink_to(outside)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code, _ = run("--root", str(root), "index")
        self.assertEqual(code, 1)
        self.assertIn("INDEX.md is a symlink", err.getvalue())
        self.assertEqual(outside.read_text(encoding="utf-8"), "mine\n")

    def test_index_replaces_a_file_that_is_not_utf8(self):
        root = make_workspace({SIG: to_markdown(valid_signal())})
        (root / "INDEX.md").write_bytes(b"\xff\xfe broken\n")
        code, out = run("--root", str(root), "index")
        self.assertEqual((code, out.strip()), (0, "INDEX.md updated"))
        self.assertIn("Idea engine", (root / "INDEX.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
