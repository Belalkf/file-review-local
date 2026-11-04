from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from file_review.scan import scan


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def test_tracked_working_copy_and_optional_untracked(self):
        (self.root / "tracked.py").write_text("old")
        (self.root / ".gitignore").write_text("ignored.py\n")
        self.git("add", ".")
        (self.root / "tracked.py").write_text("new\nmore\n")
        (self.root / "new file\nname.py").write_text("fresh")
        (self.root / "ignored.py").write_text("ignored")
        (self.root / "binary").write_bytes(b"\0")
        self.git("add", "binary")
        report = scan({"test": self.root})
        self.assertTrue(report["repositories"][0]["complete"])
        self.assertEqual({row["path"] for row in report["rows"]}, {".gitignore", "tracked.py"})
        self.assertEqual(report["rows"][0]["lines"], 2)
        report = scan({"test": self.root}, include_untracked=True)
        self.assertIn("new file\nname.py", {row["path"] for row in report["rows"]})
        self.assertNotIn("ignored.py", {row["path"] for row in report["rows"]})

    def test_missing_tracked_file_and_oversized_file_flag_gaps(self):
        (self.root / "missing").write_text("x")
        (self.root / "large").write_text("x" * 11)
        self.git("add", ".")
        (self.root / "missing").unlink()
        status = scan({"test": self.root}, max_bytes=10)["repositories"][0]
        self.assertFalse(status["complete"])
        self.assertEqual(sum(status["skipped"].values()), 2)

    def test_file_budget_and_deadline_remain_visible(self):
        (self.root / "one").write_text("x")
        self.git("add", ".")
        for kwargs in [{"max_files": 0}, {"seconds": 0}]:
            report = scan({"first": self.root, "second": self.root}, **kwargs)
            self.assertTrue(all(not item["complete"] for item in report["repositories"]))

    def test_git_failure_does_not_hide_other_repositories(self):
        other = self.root / "nested"
        other.mkdir()
        report = scan({"invalid": other, "valid": self.root})
        self.assertFalse(report["repositories"][0]["complete"])
        self.assertTrue(report["repositories"][1]["complete"])

    def test_mid_file_timeout_is_reported(self):
        from file_review.measure import ScanLimit
        (self.root / "one").write_text("x")
        self.git("add", ".")
        with patch("file_review.scan.measure", side_effect=ScanLimit):
            report = scan({"test": self.root})
        self.assertFalse(report["repositories"][0]["complete"])
        self.assertIn("time limit", report["repositories"][0]["issues"][0])
