import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from file_review.config import load_config, targets


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = self.root / "repos.json"

    def test_default_target_is_current_directory(self):
        with patch("file_review.config.Path.cwd", return_value=self.root):
            self.assertEqual(targets([]), {self.root.name: self.root})

    def test_unselected_missing_target_does_not_block_selection(self):
        self.config.write_text(json.dumps({"repositories": {"one": ".", "absent": "missing"}}))
        self.assertEqual(load_config(self.config, ["one"]), {"one": self.root})
        with self.assertRaises(ValueError):
            load_config(self.config, [])

    def test_duplicate_keys_and_bad_shapes_are_rejected(self):
        for content in ['{"repositories":{"one":".","one":"missing"}}',
                        '{"repositories":{"one":"."},"repositories":{"two":"."}}',
                        '[]', 'null', '{"repositories":[]}', '{"repositories":{}}',
                        '{"repositories":{"one":""}}', '{"repositories":{"one":4}}',
                        '{"repositories":{" ":"."}}', '{"repositories":{"one":"."},"typo":1}']:
            with self.subTest(content=content):
                self.config.write_text(content)
                with self.assertRaises(ValueError):
                    load_config(self.config, [])

    def test_duplicate_roots_and_ambiguous_names_are_rejected(self):
        with self.assertRaises(ValueError):
            targets([self.root, self.root / "."])
        for parent in ("a", "b"):
            (self.root / parent / "same").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "folder name"):
            targets([self.root / "a/same", self.root / "b/same"])

    def test_missing_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            targets([self.root / "absent"])
