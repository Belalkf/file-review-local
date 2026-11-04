"""Keep the optional skill discoverable and its dependency explicit."""

from pathlib import Path
import re
import unittest


class SkillTests(unittest.TestCase):
    def test_discovery_frontmatter_and_dependency(self):
        skill = Path(__file__).resolve().parents[1] / "skills/file-review/SKILL.md"
        content = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", content)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), skill.parent.name)
        self.assertLessEqual(len(match.group(2)), 1024)
        self.assertIn("does not install", content)
        self.assertIn("--plan", content)
        self.assertIn("incomplete", content)


if __name__ == "__main__":
    unittest.main()
