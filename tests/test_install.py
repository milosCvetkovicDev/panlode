"""install.sh: fresh install, idempotence, --force scope, --dry-run, odd paths, usage errors."""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"
TEMPLATE = REPO / "template"


# /bin/bash is bash 3.2 on macOS, the oldest shell install.sh promises to support.
BASH = "/bin/bash"


def run_install(*args: str, installer: Path = INSTALL, cwd: Path | None = None,
                env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", **(env_extra or {})}
    return subprocess.run([BASH, str(installer), *args], capture_output=True, text=True, env=env,
                          cwd=cwd, timeout=60)


def planned(stdout: str) -> list[str]:
    """The paths of the add and update lines, in the order the installer reports them."""
    return [line.split(" ", 1)[1] for line in stdout.splitlines() if line.startswith(("add ", "update "))]


def tree_digest(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def engine_check(root: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-I", "-B", str(root / "scripts" / "engine.py"), "--root", str(root), "check"],
        capture_output=True, text=True, env=env, timeout=60,
    )


class InstallTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_fresh_install_copies_the_template_and_passes_the_check(self):
        target = self.tmp / "ideas-workspace"
        result = run_install(str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        for rel in ["CLAUDE.md", ".claude/settings.json", ".claude/agents/signal-scout.md",
                    ".claude/skills/scout-online/SKILL.md", "scripts/engine.py", "templates/signal.md",
                    "founder/constraints.md", "signals/.gitkeep", ".gitignore", "INDEX.md"]:
            self.assertTrue((target / rel).is_file(), rel)
        check = engine_check(target)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_install_copies_no_bytecode_or_finder_files(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        junk = [p for p in target.rglob("*") if p.name in ("__pycache__", ".DS_Store") or p.suffix == ".pyc"]
        self.assertEqual(junk, [])

    def test_second_install_without_force_changes_nothing(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        before = tree_digest(target)
        result = run_install(str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tree_digest(target), before)
        self.assertIn("skip", result.stdout)

    def test_existing_user_files_are_never_overwritten_without_force(self):
        target = self.tmp / "w"
        target.mkdir()
        (target / "CLAUDE.md").write_text("my own rules\n", encoding="utf-8")
        self.assertEqual(run_install(str(target)).returncode, 0)
        self.assertEqual((target / "CLAUDE.md").read_text(encoding="utf-8"), "my own rules\n")

    def test_force_updates_engine_files_but_never_user_files(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        (target / "scripts" / "engine.py").write_text("# stale\n", encoding="utf-8")
        (target / "CLAUDE.md").write_text("custom\n", encoding="utf-8")
        (target / "founder" / "profile.md").write_text("me\n", encoding="utf-8")
        (target / ".claude" / "settings.json").write_text("{}\n", encoding="utf-8")
        record = target / "signals" / "2026-01-01-a.md"
        record.write_text("keep me\n", encoding="utf-8")
        result = run_install("--force", str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / "scripts" / "engine.py").read_bytes(), (TEMPLATE / "scripts" / "engine.py").read_bytes())
        self.assertEqual((target / "CLAUDE.md").read_text(encoding="utf-8"), "custom\n")
        self.assertEqual((target / "founder" / "profile.md").read_text(encoding="utf-8"), "me\n")
        self.assertEqual((target / ".claude" / "settings.json").read_text(encoding="utf-8"), "{}\n")
        self.assertEqual(record.read_text(encoding="utf-8"), "keep me\n")

    def test_dry_run_writes_nothing(self):
        target = self.tmp / "w"
        result = run_install("--dry-run", str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(target.exists())
        self.assertIn("add CLAUDE.md", result.stdout)

    def test_target_path_with_spaces(self):
        target = self.tmp / "my ideas"
        self.assertEqual(run_install(str(target)).returncode, 0)
        self.assertTrue((target / "CLAUDE.md").is_file())

    def test_missing_target_prints_usage_and_exits_2(self):
        result = run_install()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr.lower())

    def test_unknown_option_exits_2(self):
        result = run_install("--frobnicate", str(self.tmp / "w"))
        self.assertEqual(result.returncode, 2)

    def test_target_that_is_a_file_fails(self):
        target = self.tmp / "file"
        target.write_text("x", encoding="utf-8")
        result = run_install(str(target))
        self.assertNotEqual(result.returncode, 0)

    def test_force_dry_run_writes_nothing_in_a_modified_workspace(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        (target / "scripts" / "engine.py").write_text("# stale\n", encoding="utf-8")
        before = tree_digest(target)
        result = run_install("--force", "--dry-run", str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("update scripts/engine.py", result.stdout)
        self.assertEqual(tree_digest(target), before)

    def test_settings_are_installed_after_the_engine(self):
        # An install cut short must not leave hooks wired to an engine that is not there yet.
        order = planned(run_install("--dry-run", str(self.tmp / "w")).stdout)
        self.assertEqual(order[-1], ".claude/settings.json", order[-3:])

    def test_home_folder_and_its_parents_are_refused(self):
        home = self.tmp / "home"
        home.mkdir()
        for target in (home, self.tmp, Path("/")):
            result = run_install("--dry-run", str(target), env_extra={"HOME": str(home)})
            self.assertEqual(result.returncode, 1, f"{target}: {result.stdout}{result.stderr}")
            self.assertIn("refusing", result.stderr)
        self.assertEqual(list(home.iterdir()), [])

    def test_dotdot_after_a_missing_folder_is_refused(self):
        # resolve() cannot cd into a folder that does not exist, so a later .. stayed in the path and slipped
        # past the home and release guards, which compare strings.
        home = self.tmp / "home"
        home.mkdir()
        for target in (f"{home}/nx/..", f"{home}/nx/../..", f"{REPO}/nx/.."):
            result = run_install(target, env_extra={"HOME": str(home)})
            self.assertEqual(result.returncode, 2, f"{target}: {result.stdout}{result.stderr}")
            self.assertIn("does not exist yet", result.stderr, target)
        self.assertEqual(list(home.iterdir()), [])
        self.assertEqual(sorted(p.name for p in self.tmp.iterdir()), ["home"])
        self.assertFalse((REPO / "nx").exists())

    def test_newline_in_the_target_is_refused(self):
        # $(dirname) strips a trailing newline, so "..<newline>" below a missing folder turned into a real ..
        home = self.tmp / "home"
        (home / "Documents").mkdir(parents=True)
        result = run_install(f"{home}/Documents/..\n/.", env_extra={"HOME": str(home)})
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("newline", result.stderr)
        self.assertEqual(sorted(p.name for p in home.iterdir()), ["Documents"])

    def test_home_and_release_spelled_in_another_case_are_refused(self):
        # macOS volumes are case-insensitive by default, and pwd -P keeps the case as typed.
        home = self.tmp / "home"
        home.mkdir()
        if not (self.tmp / "HOME").is_dir():
            self.skipTest("case-sensitive file system: HOME and home are different folders here")
        runs = [(self.tmp / "HOME",), (self.tmp / "Home" / ".",), ("--dry-run", REPO.parent / REPO.name.upper() / "x")]
        for *options, target in runs:
            result = run_install(*options, str(target), env_extra={"HOME": str(home)})
            self.assertEqual(result.returncode, 1, f"{target}: {result.stdout}{result.stderr}")
            self.assertIn("refusing", result.stderr, target)
        self.assertEqual(list(home.iterdir()), [])

    def test_dotdot_through_existing_folders_still_works(self):
        (self.tmp / "clone").mkdir()
        result = run_install("--dry-run", "../ideas", cwd=self.tmp / "clone")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("add CLAUDE.md", result.stdout)

    def test_target_inside_the_release_is_refused(self):
        for target in (TEMPLATE, TEMPLATE / "nested", REPO):
            result = run_install("--dry-run", str(target))
            self.assertEqual(result.returncode, 1, f"{target}: {result.stdout}{result.stderr}")
        self.assertFalse((TEMPLATE / "nested").exists())

    def test_unexpanded_tilde_is_refused(self):
        result = run_install("~/ideas", cwd=self.tmp)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(list(self.tmp.iterdir()), [])

    def test_force_needs_an_existing_workspace(self):
        fresh = self.tmp / "fresh"
        self.assertEqual(run_install("--force", str(fresh)).returncode, 1)
        self.assertFalse(fresh.exists())
        lookalike = self.tmp / "project"
        (lookalike / "scripts").mkdir(parents=True)
        (lookalike / "signals").mkdir()
        (lookalike / "scripts" / "engine.py").write_text("# someone else's engine\n", encoding="utf-8")
        before = tree_digest(lookalike)
        self.assertEqual(run_install("--force", str(lookalike)).returncode, 1)
        self.assertEqual(tree_digest(lookalike), before)

    def test_existing_index_is_kept_and_an_existing_engine_is_never_run(self):
        target = self.tmp / "notes"
        (target / "scripts").mkdir(parents=True)
        (target / "INDEX.md").write_text("my own index\n", encoding="utf-8")
        marker = self.tmp / "ran"
        (target / "scripts" / "engine.py").write_text(
            f"open({str(marker)!r}, 'w').close()\n", encoding="utf-8")
        result = run_install(str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / "INDEX.md").read_text(encoding="utf-8"), "my own index\n")
        self.assertFalse(marker.exists(), "install.sh ran the engine that was already in the target")

    def test_fresh_install_generates_the_index_with_the_shipped_engine(self):
        target = self.tmp / "w"
        result = run_install("--dry-run", str(target))
        self.assertIn("generate INDEX.md", result.stdout)
        self.assertEqual(run_install(str(target)).returncode, 0)
        self.assertTrue((target / "INDEX.md").read_text(encoding="utf-8").startswith("<!-- Generated"))

    def test_symlinks_in_the_target_are_never_written_through(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        outside = self.tmp / "shared-rule.md"
        outside.write_text("mine\n", encoding="utf-8")
        rule = target / ".claude" / "rules" / "signals.md"
        rule.unlink()
        rule.symlink_to(outside)
        dangling = target / ".claude" / "rules" / "ideas.md"
        dangling.unlink()
        dangling.symlink_to(self.tmp / "nowhere.md")
        result = run_install("--force", str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(outside.read_text(encoding="utf-8"), "mine\n")
        self.assertFalse((self.tmp / "nowhere.md").exists())
        self.assertIn("skip .claude/rules/signals.md (symlink", result.stdout)

    def test_symlinked_folders_in_the_target_are_never_written_through(self):
        target = self.tmp / "w"
        self.assertEqual(run_install(str(target)).returncode, 0)
        shared = self.tmp / "shared-rules"
        shutil.copytree(target / ".claude" / "rules", shared)
        (shared / "signals.md").write_text("mine\n", encoding="utf-8")  # differs: --force would update it
        (shared / "ideas.md").unlink()  # missing: a plain install would add it
        shutil.rmtree(target / ".claude" / "rules")
        (target / ".claude" / "rules").symlink_to(shared, target_is_directory=True)
        before = tree_digest(shared)
        for args in (["--force", str(target)], [str(target)]):
            result = run_install(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_digest(shared), before, args)
            self.assertIn("skip .claude/rules/ideas.md (symlinked folder", result.stdout, args)

    def test_local_state_in_the_template_is_never_installed(self):
        release = self.tmp / "release"
        release.mkdir()
        shutil.copy2(INSTALL, release / "install.sh")
        shutil.copytree(TEMPLATE, release / "template", ignore=shutil.ignore_patterns("__pycache__"))
        planted = [".claude/settings.local.json", ".claude/checkpoints/task.md", "INDEX.md",
                   "notes.md.swp", "CLAUDE.md~", ".pytest_cache/v/cache/x"]
        for rel in planted:
            (release / "template" / rel).parent.mkdir(parents=True, exist_ok=True)
            (release / "template" / rel).write_text("local\n", encoding="utf-8")
        target = self.tmp / "w"
        result = run_install(str(target), installer=release / "install.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        for rel in planted:
            path = target / rel
            self.assertFalse(path.exists() and path.read_text(encoding="utf-8") == "local\n", rel)

    def test_leading_dash_target(self):
        result = run_install("--", "-ideas", cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.tmp / "-ideas" / "CLAUDE.md").is_file())

    def test_more_than_one_target_after_double_dash_is_refused(self):
        for args in (("a", "--", "b"), ("--", "a", "b")):
            result = run_install(*args, cwd=self.tmp)
            self.assertEqual(result.returncode, 2, args)
        self.assertEqual(list(self.tmp.iterdir()), [])

    def test_cdpath_does_not_break_locating_the_template(self):
        result = run_install("--dry-run", str(self.tmp / "w"), installer=Path(REPO.name) / "install.sh",
                             cwd=REPO.parent, env_extra={"CDPATH": str(REPO.parent)})
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
