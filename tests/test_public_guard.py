import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_public


class PublicGuardTests(unittest.TestCase):
    def check(self, filename, content):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / filename).write_text(content)
            with patch.object(check_public, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return check_public.main()

    def test_setuptools_empty_generated_assignment_is_allowed(self):
        self.assertFalse(self.check('setup.cfg', '[metadata]\nclassifiers = \n\tExample\n[options.entry_points]\nconsole_scripts = \n\tcmd = app:main\n[egg_info]\ntag_build = \ntag_date = 0\n'))

    def test_real_trailing_whitespace_is_still_reported(self):
        self.assertTrue(self.check('source.py', 'value = 1 \n'))
        self.assertTrue(self.check('setup.cfg', 'name = example \n'))
        self.assertTrue(self.check('notes.md', 'tag_build = \n'))
