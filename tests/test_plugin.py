"""The Claude Code plugin and marketplace manifests: valid, in sync, and free of global hooks."""

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    return dict(re.findall(r"^([a-z-]+):\s*(.+)$", match.group(1), re.MULTILINE))


class ManifestTest(unittest.TestCase):
    def test_plugin_manifest_has_the_listing_fields(self):
        plugin = load(PLUGIN)
        self.assertRegex(plugin["name"], KEBAB)
        for key in ("version", "description", "author", "homepage", "repository", "license", "keywords"):
            self.assertIn(key, plugin)
        self.assertEqual(plugin["license"], "MIT")
        self.assertRegex(plugin["version"], r"^\d+\.\d+\.\d+$")

    def test_marketplace_lists_this_repository_as_the_plugin(self):
        plugin, market = load(PLUGIN), load(MARKETPLACE)
        self.assertEqual(market["name"], plugin["name"])
        self.assertIn("name", market["owner"])
        [entry] = market["plugins"]
        self.assertEqual(entry["name"], plugin["name"])
        self.assertEqual(entry["source"], "./")
        self.assertNotIn("version", entry)  # plugin.json owns the version

    def test_version_has_a_changelog_section(self):
        version = load(PLUGIN)["version"]
        changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(changelog, rf"(?m)^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$")


class PluginComponentsTest(unittest.TestCase):
    def test_plugin_ships_no_hooks_agents_or_commands(self):
        # Workspace hooks deny product code; enabled globally they would break every other project.
        plugin = load(PLUGIN)
        for key in ("hooks", "agents", "commands", "mcpServers"):
            self.assertNotIn(key, plugin)
        for default in ("hooks", "agents", "commands", "skills"):
            self.assertFalse((REPO / default).exists(), default)
        self.assertFalse((REPO / ".mcp.json").exists())

    def test_plugin_skills_exist_and_drive_the_installer(self):
        skills_dir = REPO / load(PLUGIN)["skills"]
        names = sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md"))
        self.assertEqual(names, ["init", "update"])
        for name in names:
            path = skills_dir / name / "SKILL.md"
            meta = frontmatter(path)
            self.assertEqual(meta.get("name"), name)
            self.assertTrue(meta.get("description"))
            self.assertEqual(meta.get("disable-model-invocation"), "true")
            self.assertIn('"${CLAUDE_PLUGIN_ROOT}/install.sh"', path.read_text(encoding="utf-8"))

    def test_init_waits_for_the_user_after_the_dry_run(self):
        text = (REPO / "plugin" / "skills" / "init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("wait for the user's go", text)
        self.assertIn("home folder", text)

    def test_update_protects_the_users_own_edits(self):
        text = (REPO / "plugin" / "skills" / "update" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("absolute path", text)
        self.assertIn("scripts/ideaengine/", text)
        self.assertIn("status --porcelain", text)
        self.assertIn("\" diff", text)
        self.assertIn('"${CLAUDE_PLUGIN_ROOT}/template/.claude/settings.json"', text)


class TemplateComponentsTest(unittest.TestCase):
    def test_template_skills_and_agents_have_name_and_description(self):
        claude = REPO / "template" / ".claude"
        files = list(claude.glob("skills/*/SKILL.md")) + list(claude.glob("agents/*.md"))
        self.assertGreaterEqual(len(files), 3)
        for path in files:
            meta = frontmatter(path)
            expected = path.parent.name if path.name == "SKILL.md" else path.stem
            self.assertEqual(meta.get("name"), expected, path)
            self.assertTrue(meta.get("description"), path)

    def test_every_recipe_the_scout_skill_dispatches_exists(self):
        skill = REPO / "template" / ".claude" / "skills" / "scout-online" / "SKILL.md"
        recipes = re.findall(r"`\.claude/skills/scout-online/sources/([a-z0-9-]+\.md)`", skill.read_text(encoding="utf-8"))
        self.assertEqual(len(recipes), 3)
        for recipe in recipes:
            self.assertTrue((skill.parent / "sources" / recipe).is_file(), recipe)


if __name__ == "__main__":
    unittest.main()
