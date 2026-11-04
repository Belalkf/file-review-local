import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from file_review.config import load_config
from file_review.cli import main
from file_review.render import render


class InterfaceTests(unittest.TestCase):
    def test_configuration_paths_and_duplicate_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = root / "repositories.json"
            config.write_text(json.dumps({"repositories": {"example": "."}}))
            self.assertEqual(load_config(config, []), {"example": root.resolve()})
            with self.assertRaises(ValueError):
                load_config(config, ["unknown"])
            config.write_text(json.dumps({"repositories": {"one": ".", "two": "."}}))
            with self.assertRaises(ValueError):
                load_config(config, [])

    def test_html_filenames_cannot_inject_script(self):
        from file_review.demo import example_report
        report = example_report()
        report["rows"][0]["path"] = "</script><script>alert(1)</script>REPORT_DATA"
        html = render(report)
        self.assertNotIn("<script>alert(1)", html)
        self.assertIn("\\u003c/script\\u003e", html)
        payload = html.split('<script id="data" type="application/json">')[1].split("</script>")[0]
        data = json.loads(payload)
        self.assertIn("Review briefing", data.pop("briefing"))
        self.assertIn("decision table", data.pop("guidance"))
        self.assertEqual(len(data.pop("default_rows")), len(report["rows"]))
        self.assertEqual(data, report)

    def test_json_does_not_launch_browser_and_gaps_return_failure(self):
        fake = {"rows": [], "repositories": [{"complete": False}]}
        output = io.StringIO()
        with patch("file_review.cli.targets", return_value={}), patch("file_review.cli.scan", return_value=fake), patch("file_review.output.webbrowser.open") as browser, contextlib.redirect_stdout(output):
            self.assertEqual(main(["--json"]), 1)
        browser.assert_not_called()
        self.assertEqual(json.loads(output.getvalue()), fake)

    def test_invalid_limits_rejected(self):
        for value in ["nan", "inf", "0", "-1", "1e308"]:
            with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                main(["--seconds", value])
            self.assertEqual(error.exception.code, 2)

    def test_oversized_read_limit_is_rejected_before_conversion(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main(["--max-mib", "1e308"])
        self.assertEqual(error.exception.code, 2)

    def test_browser_failure_keeps_private_report_available(self):
        fake = {"rows": [], "repositories": [{"complete": True}]}
        with tempfile.TemporaryDirectory() as folder:
            descriptor, filename = tempfile.mkstemp(dir=folder, suffix=".html")
            output, errors = io.StringIO(), io.StringIO()
            with patch("file_review.cli.targets", return_value={}), patch("file_review.cli.scan", return_value=fake), patch("file_review.output.tempfile.mkstemp", return_value=(descriptor, filename)), patch("file_review.output.webbrowser.open", return_value=False), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                self.assertEqual(main([]), 0)
            self.assertIn(filename, output.getvalue())
            self.assertIn("Open the saved report", output.getvalue())
            self.assertIn("<!doctype html>", Path(filename).read_text())
            self.assertEqual(os.stat(filename).st_mode & 0o777, 0o600)
