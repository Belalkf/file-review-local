import copy
import unittest

from scripts.check_hosting import CHECKS, validate_rules


def protected_rules():
    return [{'type': 'deletion'}, {'type': 'non_fast_forward'},
            {'type': 'pull_request', 'parameters': {'required_review_thread_resolution': True}},
            {'type': 'required_status_checks', 'parameters': {
                'strict_required_status_checks_policy': True,
                'required_status_checks': [{'context': name, 'integration_id': 15368} for name in sorted(CHECKS)]}},
            {'type': 'code_scanning', 'parameters': {'code_scanning_tools': [
                {'tool': 'CodeQL', 'security_alerts_threshold': 'medium_or_higher', 'alerts_threshold': 'errors'}]}}]


class HostingProtectionTests(unittest.TestCase):
    def test_unprotected_branch_is_rejected(self):
        self.assertTrue(validate_rules([]))

    def test_missing_each_required_guard_is_rejected(self):
        rules = protected_rules()
        for index in range(len(rules)):
            with self.subTest(removed=rules[index]['type']):
                self.assertTrue(validate_rules(rules[:index] + rules[index + 1:]))

    def test_missing_platform_spoofed_checks_and_stale_base_are_rejected(self):
        for mutation in ('missing', 'spoofed', 'stale', 'unresolved'):
            rules = copy.deepcopy(protected_rules())
            status = rules[3]['parameters']
            if mutation == 'missing':
                status['required_status_checks'].pop()
            elif mutation == 'spoofed':
                status['required_status_checks'][0]['integration_id'] = None
            elif mutation == 'stale':
                status['strict_required_status_checks_policy'] = False
            else:
                rules[2]['parameters']['required_review_thread_resolution'] = False
            with self.subTest(mutation=mutation):
                self.assertTrue(validate_rules(rules))

    def test_active_guard_accepts_additional_protections(self):
        rules = protected_rules() + [{'type': 'required_signatures'}]
        self.assertEqual(validate_rules(rules), [])

    def test_disabled_or_relaxed_security_scan_is_rejected(self):
        for field, value in [('tool', 'Other tool'), ('security_alerts_threshold', 'high_or_higher'),
                             ('alerts_threshold', 'none')]:
            rules = protected_rules()
            rules[-1]['parameters']['code_scanning_tools'][0][field] = value
            with self.subTest(field=field):
                self.assertTrue(validate_rules(rules))
