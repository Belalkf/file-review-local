"""Read-only check of this public repository's effective main-branch rules."""

import json
import sys
import urllib.error
import urllib.request

URL = 'https://api.github.com/repos/Belalkf/file-review-local/rules/branches/main?per_page=100'
CHECKS = {f'test ({system}, {version})' for system in ('ubuntu-latest', 'macos-latest')
          for version in ('3.9', '3.13')} | {'Dependency review'}


def validate_rules(rules):
    errors = []
    types = {rule['type'] for rule in rules}
    for required in ('deletion', 'non_fast_forward', 'pull_request', 'required_status_checks', 'code_scanning'):
        if required not in types:
            errors.append(f'Missing active main rule: {required}')
    status_rules = [rule['parameters'] for rule in rules if rule['type'] == 'required_status_checks']
    required_checks = {item['context'] for rule in status_rules for item in rule['required_status_checks']
                       if item.get('integration_id') == 15368}  # GitHub Actions app
    if not CHECKS <= required_checks:
        errors.append('Platform and dependency-review checks must be required from GitHub Actions')
    if status_rules and not any(rule['strict_required_status_checks_policy'] for rule in status_rules):
        errors.append('Changes must be tested against the current base branch')
    for rule in rules:
        if rule['type'] == 'pull_request' and not rule['parameters']['required_review_thread_resolution']:
            errors.append('Review conversations must be resolved before merging')
    tools = [tool for rule in rules if rule['type'] == 'code_scanning'
             for tool in rule['parameters']['code_scanning_tools']]
    if not any(tool['tool'] == 'CodeQL' and tool['security_alerts_threshold'] in ('all', 'medium_or_higher')
               and tool['alerts_threshold'] in ('errors', 'errors_and_warnings', 'all') for tool in tools):
        errors.append('CodeQL must block moderate-or-higher security alerts and code errors')
    return errors


def main():
    request = urllib.request.Request(URL, headers={'Accept': 'application/vnd.github+json',
                                     'User-Agent': 'File-Review-hosting-check'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            rules = json.load(response)
        errors = validate_rules(rules)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Hosting verification unavailable: {error}', file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('Active main protection and required platform checks verified. No settings changed.')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
