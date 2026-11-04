"""Reject an installed command whose JSON works but other output is broken."""

from pathlib import Path
import re
from subprocess import CompletedProcess
import tempfile
import unittest
from unittest.mock import patch

from scripts.check_wheel import check_installation


class InstalledCommandTests(unittest.TestCase):
    def test_pypi_description_has_no_checkout_relative_links(self):
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            with self.subTest(target=target):
                self.assertTrue("://" in target or target.startswith("#"))

    def test_broken_html_is_not_hidden_by_working_json_and_plan(self):
        def run(command, **kwargs):
            if "--json" in command:
                return CompletedProcess(command, 0, '{"demo": true}')
            if "--plan" in command:
                return CompletedProcess(command, 0, 'User task: "Test export"\nNo language parsing')
            if "--output" in command:
                Path(command[-1]).write_text("Broken report")
            return CompletedProcess(command, 0, "")

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch("scripts.check_wheel.subprocess.run", side_effect=run):
                with self.assertRaises(AssertionError):
                    check_installation(root / "bin", root, {})


if __name__ == "__main__":
    unittest.main()
