"""Repository-level checks: the engine suite, the example run, Markdown links, template hygiene."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "template"
EXAMPLE = REPO / "examples" / "first-scout-run"
ENGINE = TEMPLATE / "scripts" / "engine.py"
ISSUE_FORMS = REPO / ".github" / "ISSUE_TEMPLATE"
FORM_LINK = re.compile(r"(https?://[\w.-]+/[\w.-]+/[\w.-]+)/issues/new\?[^)\s]*?\btemplate=([\w-]+(?:\.[\w-]+)*)")
FORM_FIELD_TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
ENGINE_GUARD = '[ -f "$CLAUDE_PROJECT_DIR/scripts/engine.py" ] || exit 0; '
# Exact rules: a bare wildcard would also pre-approve `--root <any folder>`, which reads and writes outside the workspace.
ENGINE_RULES = {
    "Bash(python3 scripts/engine.py check)",
    "Bash(python3 scripts/engine.py index)",
    "Bash(python3 scripts/engine.py brief)",
    "Bash(python3 scripts/engine.py next-id *)",
    "Bash(python3 scripts/engine.py slug *)",
}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")


def engine(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-B", str(ENGINE), *args], capture_output=True, text=True, env=ENV, timeout=60)


def markdown_files() -> list[Path]:
    skip = {".git", "node_modules", "_site", ".jekyll-cache"}
    return [p for p in REPO.rglob("*.md") if not skip.intersection(p.relative_to(REPO).parts)]


def issue_forms() -> list[Path]:
    return [f for f in ISSUE_FORMS.glob("*.yml") if f.name != "config.yml"]


def issue_form_links() -> list[tuple[Path, str, str]]:
    found = []
    for path in markdown_files():
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
        found += [(path, repo, name) for repo, name in FORM_LINK.findall(text)]
    return found


def pycache_dirs(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("__pycache__")}


class EngineSuiteTest(unittest.TestCase):
    def test_template_engine_suite_passes(self):
        # An earlier CI step may already have left __pycache__ folders, so only new ones count.
        before = pycache_dirs(TEMPLATE)
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", "scripts/tests", "-t", "scripts"],
            cwd=TEMPLATE, capture_output=True, text=True, env=ENV, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])
        # -I ignores PYTHONDONTWRITEBYTECODE, so only -B keeps this run from writing bytecode into the shipped template.
        added = sorted(pycache_dirs(TEMPLATE) - before)
        self.assertEqual(added, [], f"the run created __pycache__ folders: {added}")


class ExampleRunTest(unittest.TestCase):
    def test_example_workspace_passes_the_check(self):
        result = engine("--root", str(EXAMPLE), "check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s), 0 warning(s)", result.stdout)

    def test_example_index_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "run"
            shutil.copytree(EXAMPLE, copy)
            self.assertEqual(engine("--root", str(copy), "index").returncode, 0)
            self.assertEqual(
                (copy / "INDEX.md").read_text(encoding="utf-8"), (EXAMPLE / "INDEX.md").read_text(encoding="utf-8")
            )

    def test_demo_image_shows_real_engine_output(self):
        maker = REPO / ".github" / "assets" / "src" / "make_demo.py"
        result = subprocess.run([sys.executable, "-I", "-B", str(maker), "--check"], capture_output=True, text=True, env=ENV, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_example_signals_cite_public_http_sources(self):
        signals = sorted((EXAMPLE / "signals").glob("*.md"))
        self.assertGreater(len(signals), 0)
        for path in signals:
            ref = re.search(r"^ref: (\S+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
            self.assertIsNotNone(ref, path.name)
            self.assertTrue(ref.group(1).startswith("https://"), path.name)


class MarkdownLinkTest(unittest.TestCase):
    def test_example_commands_call_the_template_engine(self):
        # From the repository root the engine lives in template/; examples/ is not in a workspace.
        for path in markdown_files():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "--root examples/" in line:
                    self.assertIn("template/scripts/engine.py", line, f"{path.relative_to(REPO)}:{number}")

    def test_issue_forms_have_the_shape_github_needs(self):
        for form in issue_forms():
            text = form.read_text(encoding="utf-8")
            for key in ("name", "description", "body"):
                self.assertRegex(text, rf"(?m)^{key}:", form.name)
            types = re.findall(r"(?m)^  - type: (\S+)$", text)
            self.assertTrue(set(types) <= FORM_FIELD_TYPES, f"{form.name}: {types}")
            self.assertTrue(set(types) - {"markdown"}, f"{form.name} has no input field")
            ids = re.findall(r"(?m)^    id: (\S+)$", text)
            self.assertEqual(len(ids), len(set(ids)), f"{form.name}: duplicate ids {ids}")
            for field_id in ids:
                self.assertRegex(field_id, r"^[A-Za-z0-9_-]+$", form.name)

    def test_issue_form_links_name_existing_forms(self):
        forms = {f.name for f in issue_forms()}
        for path, repo, name in issue_form_links():
            where = f"{path.relative_to(REPO)}: {repo} {name}"
            self.assertEqual(repo.lower(), "https://github.com/miloscvetkovicdev/panlode", where)
            self.assertIn(name, forms, where)

    def test_the_readme_links_the_share_a_run_form(self):
        names = [name for path, _, name in issue_form_links() if path == REPO / "README.md"]
        self.assertIn("share_a_run.yml", names)

    def test_the_share_a_run_form_asks_to_confirm_nothing_private_is_shared(self):
        text = (ISSUE_FORMS / "share_a_run.yml").read_text(encoding="utf-8")
        fields = re.split(r"(?m)^  - type: ", text)[1:]
        confirm = [f for f in fields if f.startswith("checkboxes") and "personal data" in f]
        self.assertEqual(len(confirm), 1, "a checkboxes field that names personal data")
        self.assertRegex(confirm[0], r"(?m)^ +required: true$")

    def test_every_relative_link_resolves(self):
        broken = []
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # links inside code blocks are examples
            for match in LINK.finditer(text):
                target = match.group(1) or match.group(2)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#") or "{{" in target:
                    continue
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                if not (path.parent / file_part).resolve().exists():
                    broken.append(f"{path.relative_to(REPO)} -> {target}")
        self.assertEqual(broken, [])


class TemplateHygieneTest(unittest.TestCase):
    def test_no_machine_specific_paths(self):
        offenders = []
        for path in TEMPLATE.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".json", ""}:
                text = path.read_text(encoding="utf-8", errors="replace")
                if "/usr/local/bin" in text or "/Users/" in text or "/home/" in text:
                    offenders.append(path.relative_to(TEMPLATE).as_posix())
        self.assertEqual(offenders, [])

    def test_settings_wire_the_four_hooks_to_the_engine(self):
        settings = json.loads((TEMPLATE / ".claude" / "settings.json").read_text(encoding="utf-8"))
        hooks = settings["hooks"]
        self.assertEqual(sorted(hooks), ["PostToolUse", "PreToolUse", "SessionStart", "Stop"])
        for event, expected in [("SessionStart", "session-start"), ("PreToolUse", "pre-write"),
                                ("PostToolUse", "post-write"), ("Stop", "stop")]:
            command = hooks[event][0]["hooks"][0]["command"]
            self.assertTrue(command.startswith(ENGINE_GUARD), command)
            self.assertIn('python3 "$CLAUDE_PROJECT_DIR/scripts/engine.py" hook ' + expected, command)
        for event in ("PreToolUse", "PostToolUse"):
            self.assertEqual(hooks[event][0]["matcher"], "Write|Edit", event)

    def test_hooks_exit_cleanly_when_the_engine_is_missing(self):
        # python3 exits 2 on a missing script, which Claude Code reads as "block": every write and every
        # stop would be refused in a folder that holds the settings but not the engine.
        settings = json.loads((TEMPLATE / ".claude" / "settings.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as empty:
            for event, entries in settings["hooks"].items():
                command = entries[0]["hooks"][0]["command"]
                result = subprocess.run(["sh", "-c", command], input="{}", capture_output=True, text=True,
                                        env={**ENV, "CLAUDE_PROJECT_DIR": empty}, timeout=30)
                self.assertEqual(result.returncode, 0, f"{event}: {result.stderr}")

    def test_pre_write_hook_blocks_when_the_engine_cannot_run(self):
        # Without onFailure, a missing or too old python3 lets every write through unchecked.
        settings = json.loads((TEMPLATE / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["hooks"]["PreToolUse"][0]["hooks"][0].get("onFailure"), "block")

    def test_recipe_domains_are_pre_approved_for_webfetch(self):
        settings = json.loads((TEMPLATE / ".claude" / "settings.json").read_text(encoding="utf-8"))
        allowed = {re.sub(r"^www\.", "", rule[len("WebFetch(domain:"):-1])
                   for rule in settings["permissions"]["allow"] if rule.startswith("WebFetch(domain:")}
        recipes = TEMPLATE / ".claude" / "skills" / "scout-online" / "sources"
        for recipe in recipes.glob("*.md"):
            text = recipe.read_text(encoding="utf-8")
            for domain in re.findall(r"(?<![\w.-])(?:www\.)?((?:[a-z0-9-]+\.)+(?:com|org|io|net|co|dev|to))\b", text):
                self.assertIn(domain, allowed, f"{recipe.name}: {domain}")

    def test_skill_bash_permissions_use_python3_engine(self):
        files = list((TEMPLATE / ".claude").glob("skills/*/SKILL.md")) + list((TEMPLATE / ".claude").glob("agents/*.md"))
        for path in files:
            header = path.read_text(encoding="utf-8").split("---", 2)[1]
            line = re.search(r"^(?:allowed-tools|tools):(.*)$", header, re.M)
            entries = re.findall(r"[A-Za-z]+(?:\([^)]*\))?", line.group(1)) if line else []
            for entry in entries:
                if entry.startswith("Bash"):
                    self.assertIn(entry, ENGINE_RULES, path.relative_to(TEMPLATE))

    def test_skills_that_draft_records_may_number_and_name_them(self):
        for path in (TEMPLATE / ".claude").glob("skills/*/SKILL.md"):
            _, header, body = path.read_text(encoding="utf-8").split("---", 2)
            if "from `templates/" not in body:
                continue
            tools = re.search(r"^allowed-tools:(.*)$", header, re.M).group(1)
            for rule in ("Bash(python3 scripts/engine.py next-id *)", "Bash(python3 scripts/engine.py slug *)"):
                self.assertIn(rule, tools, path.relative_to(TEMPLATE))
        log = (TEMPLATE / ".claude" / "skills" / "log-experiment" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Write(experiments/**)", log.split("---", 2)[1])

    def test_settings_pre_approve_only_exact_bash_commands(self):
        settings = json.loads((TEMPLATE / ".claude" / "settings.json").read_text(encoding="utf-8"))
        bash_rules = {r for r in settings["permissions"]["allow"] if r.startswith("Bash")}
        self.assertEqual(bash_rules, ENGINE_RULES | {"Bash(python3 -I -m unittest discover -s scripts/tests -t scripts)"})

    def test_wildcard_engine_rules_cannot_reach_another_root(self):
        # `next-id *` and `slug *` stay inside the workspace only because --root is refused after the subcommand.
        with tempfile.TemporaryDirectory(prefix="ie-root-") as other:
            for args in (["next-id", "sig", "--root", other], ["slug", "x", "--root", other],
                         ["next-id", "sig", f"--root={other}"], ["slug", "x", "--ro", other]):
                result = engine(*args)
                self.assertEqual(result.returncode, 2, args)
                self.assertIn("unrecognized arguments", result.stderr, args)
            self.assertEqual(os.listdir(other), [])

    def test_slug_commands_single_quote_the_title(self):
        # Titles come from scraped pages; inside double quotes a $( ) or backtick would still run.
        files = [REPO / "README.md", *TEMPLATE.rglob("*.md")]
        for path in files:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for match in re.finditer(r"(\S*)engine\.py slug (\S)", line):
                    if match.group(2) == "*" and line[:match.start()].endswith("Bash(python3 "):
                        continue  # a permission rule, not a command
                    where = f"{path.relative_to(REPO)}:{number}"
                    self.assertTrue(match.group(1).endswith("scripts/"), where)
                    self.assertIn("python3 ", line[:match.start() + 1].rsplit("`", 1)[-1], where)
                    self.assertEqual(match.group(2), "'", where)

    def test_gitignore_covers_local_state_inside_the_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            (Path(tmp) / ".gitignore").write_bytes((REPO / ".gitignore").read_bytes())
            for rel in ["template/.claude/settings.local.json", "template/.claude/checkpoints/task.md",
                        ".claude/settings.local.json"]:
                result = subprocess.run(["git", "-C", tmp, "-c", "core.excludesFile=/dev/null", "check-ignore", "-q", rel])
                self.assertEqual(result.returncode, 0, rel)

    def test_template_ships_no_records_or_generated_files(self):
        for folder in ["signals", "ideas", "experiments", "interviews"]:
            self.assertEqual(sorted(p.name for p in (TEMPLATE / folder).iterdir()), [".gitkeep"], folder)
        self.assertFalse((TEMPLATE / "INDEX.md").exists())


if __name__ == "__main__":
    unittest.main()
