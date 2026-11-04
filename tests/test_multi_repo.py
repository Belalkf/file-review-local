import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from file_review.cli import main
from file_review.scan import scan


class MultipleRepositoryTests(unittest.TestCase):
    def test_two_roots_keep_paths_and_coverage_independent(self):
        with tempfile.TemporaryDirectory() as folder:
            roots = [Path(folder) / name for name in ['first', 'second']]
            for root in roots:
                root.mkdir()
                subprocess.run(['git', 'init', '-q', str(root)], check=True, timeout=10)
                (root / 'shared.rs').write_text('one\ntwo\n')
                subprocess.run(['git', '-C', str(root), 'add', '.'], check=True, timeout=10)
            (roots[1] / 'shared.rs').unlink()
            report = scan(dict(zip(['first', 'second'], roots)))
            self.assertEqual([repo['complete'] for repo in report['repositories']], [True, False])
            self.assertEqual([row['repository'] for row in report['rows']], ['first'])
            (roots[1] / 'shared.rs').write_text('three\n')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main([str(root) for root in roots] + ['--json'])
            self.assertEqual(result, 0)
            data = json.loads(output.getvalue())
            self.assertEqual({row['repository'] for row in data['rows']}, {'first', 'second'})
            self.assertEqual({row['path'] for row in data['rows']}, {'shared.rs'})

    def test_inventory_only_keeps_measurements_without_path_hints(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True, timeout=10)
            (root / 'file.ts').write_text('synthetic\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True, timeout=10)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(root), '--inventory-only', '--json']), 0)
            report = json.loads(output.getvalue())
            self.assertNotIn('analysis', report)
            self.assertNotIn('review', report['rows'][0])
            self.assertIn('sha256', report['rows'][0])

    def test_inventory_only_demo_obeys_the_same_contract(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(['--demo', '--inventory-only', '--json']), 0)
        report = json.loads(output.getvalue())
        self.assertNotIn('analysis', report)
        self.assertTrue(all('review' not in row for row in report['rows']))
