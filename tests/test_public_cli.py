import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from file_review.cli import entrypoint, main
from file_review.demo import example_report
from file_review.output import save_html


class PublicCommandTests(unittest.TestCase):
    def test_conflicting_inputs_fail_before_scan(self):
        cases = [[".", "--config", "x"], ["--repo", "one"], ["--demo", "."],
                 ["--demo", "--config", "x"], ["--demo", "--include-untracked"],
                 ["--json", "--no-open"], ["--terminal", "--output", "x"]]
        for args in cases:
            with self.subTest(args=args), patch("file_review.cli.scan") as scan:
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                    main(args)
                self.assertEqual(error.exception.code, 2)
                scan.assert_not_called()

    def test_demo_reads_no_repository_and_opens_no_browser_for_json(self):
        with patch("file_review.cli.scan") as scan, patch("file_review.output.webbrowser.open") as browser:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["--demo", "--json"]), 0)
            self.assertTrue(json.loads(output.getvalue())["demo"])
            scan.assert_not_called()
            browser.assert_not_called()

    def test_no_open_creates_private_file_and_refuses_overwrite_and_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.html"
            with patch("file_review.output.webbrowser.open") as browser:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(main(["--demo", "--no-open", "--output", str(path)]), 0)
                browser.assert_not_called()
            original = path.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["--demo", "--no-open", "--output", str(path)]), 1)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            link = Path(folder) / "link.html"
            link.symlink_to(path)
            with self.assertRaises(FileExistsError):
                save_html(example_report(), link, False)
            self.assertEqual(path.read_bytes(), original)

    def test_unsupported_platform_is_clear(self):
        with patch("file_review.cli.os.name", "nt"), contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit) as error:
                main(["--demo"])
        self.assertEqual(error.exception.code, 2)
        self.assertIn("macOS or Linux", errors.getvalue())

    def test_keyboard_interrupt_has_dedicated_exit_status(self):
        with patch("file_review.cli.main", side_effect=KeyboardInterrupt):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                entrypoint()
        self.assertEqual(error.exception.code, 130)

    def test_subprocess_outside_tool_uses_explicit_target_and_preserves_git_state(self):
        tool = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "tracked.py").write_text("one\ntwo\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            index = (root / ".git/index").read_bytes()
            result = subprocess.run([sys.executable, "-m", "file_review", str(root), "--json"],
                                    cwd=tool, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["schema_version"], 1)
            self.assertEqual(report["rows"][0]["lines"], 2)
            self.assertEqual((root / ".git/index").read_bytes(), index)
