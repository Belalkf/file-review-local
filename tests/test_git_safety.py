import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from file_review.scan import scan


class GitSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "file.py").write_text("text")
        self.git("add", ".")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args],
                              check=True, capture_output=True, timeout=10)

    def test_inherited_git_redirection_does_not_change_inventory(self):
        with patch.dict(os.environ, {"GIT_DIR": str(self.root / "missing"),
                                     "GIT_WORK_TREE": str(self.root / "missing"),
                                     "GIT_INDEX_FILE": str(self.root / "absent-index")}):
            report = scan({"example": self.root})
        self.assertTrue(report["repositories"][0]["complete"])
        self.assertEqual([row["path"] for row in report["rows"]], ["file.py"])
        self.assertFalse((self.root / "absent-index").exists())

    def test_missing_git_is_explicit_gap(self):
        with patch("file_review.scan.subprocess.run", side_effect=FileNotFoundError("Git unavailable")):
            status = scan({"example": self.root})["repositories"][0]
        self.assertFalse(status["complete"])
        self.assertIn("Git unavailable", status["issues"][0])

    def test_tracked_symlink_is_not_read(self):
        (self.root / "link").symlink_to("file.py")
        self.git("add", "link")
        report = scan({"example": self.root})
        self.assertFalse(report["repositories"][0]["complete"])
        self.assertNotIn("link", [row["path"] for row in report["rows"]])

    def test_subfolder_is_not_silently_expanded_to_whole_repository(self):
        child = self.root / "nested"
        child.mkdir()
        status = scan({"example": child})["repositories"][0]
        self.assertFalse(status["complete"])
        self.assertIn("repository root", status["issues"][0])
