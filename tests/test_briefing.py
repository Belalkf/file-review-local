import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from file_review.analysis.runner import enrich
from file_review.briefing import briefing
from file_review.cli import main
from file_review.demo import example_report
from file_review.measure import measure


class ReviewTests(unittest.TestCase):
    def test_all_languages_get_the_same_honest_guidance_without_rereads(self):
        report = example_report()
        report['rows'] = [dict(path='src/owner.' + ext, lines=300, bytes=1000, longest_line=80,
                               repository='example-app') for ext in ['py', 'rs', 'swift', 'ts', 'odd']]
        with patch('builtins.open', side_effect=AssertionError('must not reread source')):
            enrich(report)
        reviews = [row['review'] for row in report['rows']]
        self.assertTrue(all(review == reviews[0] for review in reviews))
        self.assertEqual(reviews[0]['action'], 'inspect')
        self.assertIn('No language parsing', report['analysis']['limits'])
        self.assertNotIn('Python', briefing(report))

    def test_path_hints_do_not_claim_a_verified_keep_or_split(self):
        report = example_report()
        report['rows'] += [dict(report['rows'][0], path='vendor/custom.rs')]
        enrich(report)
        for row in [report['rows'][3], report['rows'][-1]]:
            self.assertEqual(row['review']['action'], 'check-owner')
            self.assertIn('not proof', row['review']['steps'][0])

    def test_small_neighbors_cross_languages_but_not_repositories(self):
        report = example_report()
        report['rows'] = [dict(report['rows'][0], path='src/' + name, lines=20)
                          for name in ['a.rs', 'b.ts', 'c.swift', 'data.json']]
        report['rows'].append(dict(report['rows'][0], repository='other', path='src/private.rs'))
        enrich(report)
        self.assertEqual(report['rows'][0]['review']['related'], ['src/b.ts', 'src/c.swift'])
        self.assertEqual(report['rows'][3]['review']['related'], [])
        self.assertEqual(report['rows'][4]['review']['related'], [])

    def test_briefing_is_bounded_quotes_paths_and_carries_coverage(self):
        report = example_report()
        report['rows'] = [dict(report['rows'][0], path=f'src/file{i}.rs') for i in range(20)]
        report['rows'][0]['path'] = 'src/quote"\n</script>.rs'
        report['rows'][0]['lines'] = 1000
        enrich(report)
        report['rows'][0]['sha256'] = 'a' * 64
        report['repositories'][0]['complete'] = False
        report['repositories'][0]['issues'] = ['A file changed; rerun']
        report['task'] = 'Make export easier to test'
        text = briefing(report)
        self.assertIn('12 of 20', text)
        self.assertIn('WARNING: Inventory is incomplete', text)
        self.assertIn('A file changed; rerun', text)
        self.assertIn('scan budget: 60 seconds', text)
        self.assertIn('User task:', text)
        self.assertIn('quote\\"\\n', text)
        self.assertIn('Measured SHA-256: ' + 'a' * 64, text)
        self.assertIn('callers, imports, shared state', text)
        self.assertIn('not authorization', text)
        self.assertIn('decision table', text)

    def test_empty_inventory_is_not_a_clean_bill_of_health(self):
        report = example_report()
        report['rows'] = []
        self.assertIn('no clean bill of health', briefing(report))

    def test_hash_matches_measured_bytes_without_source_in_report(self):
        with tempfile.TemporaryDirectory() as folder:
            content = b'private source body\r\n'
            (Path(folder) / 'example.rs').write_bytes(content)
            row, reason = measure(Path(folder), 'example.rs', 1000, time.monotonic() + 5)
        self.assertIsNone(reason)
        self.assertEqual(row['sha256'], hashlib.sha256(content).hexdigest())
        self.assertNotIn('private source body', json.dumps(row))

    def test_plan_with_task_needs_no_browser_and_invalid_task_stops_before_scan(self):
        output = io.StringIO()
        with patch('file_review.output.webbrowser.open') as browser, contextlib.redirect_stdout(output):
            self.assertEqual(main(['--demo', '--plan', '--task', 'Keep exports stable']), 0)
        browser.assert_not_called()
        self.assertIn('Keep exports stable', output.getvalue())
        with patch('file_review.cli.scan') as scan, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(['--task', 'x' * 2001])
        self.assertEqual(error.exception.code, 2)
        scan.assert_not_called()

    def test_common_guidance_is_not_repeated_per_file(self):
        report = example_report()
        report['rows'] = [dict(report['rows'][0], path=f'file{i}.rs', sha256='a' * 64)
                          for i in range(12)]
        enrich(report)
        text = briefing(report)
        self.assertEqual(text.count('Choose split, retain, combine'), 1)
        self.assertEqual(text.count('Measured SHA-256:'), 12)
        self.assertNotIn('  Next:', text)
        self.assertIn('No model was called', text)

    def test_format_hint_survives_compact_briefing(self):
        from file_review.briefing import row_briefing
        report = example_report()
        enrich(report)
        self.assertIn('Path hint:', row_briefing(report['rows'][3]))
