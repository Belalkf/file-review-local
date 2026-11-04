const {test} = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const {spawnSync} = require('node:child_process');

test('report harness ignores an inherited Python executable override', () => {
  const result = spawnSync(process.execPath, ['-e', "require('./tests/report_harness.cjs')"], {
    cwd: path.join(__dirname, '..'),
    env: {...process.env, PYTHON: '/invalid/file-review-python'},
    encoding: 'utf8', timeout: 20000,
  });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 0, result.stderr);
});
