const {test} = require('node:test');
const assert = require('node:assert/strict');
const {setup, row} = require('./report_harness.cjs');

test('each size condition independently finds large files; zero disables a condition', () => {
  const ui = setup([row('lines.py', 300, 600, 2), row('wide.json', 1, 40000, 40000), row('long.txt', 1, 1500, 1500), row('small.py', 1, 5, 5)]);
  assert.match(ui.get('count').textContent, /^3 match/);
  ui.input('bytes', '0'); ui.input('longest', '0');
  assert.match(ui.get('count').textContent, /^1 match/);
  ui.click('all');
  assert.match(ui.get('count').textContent, /^4 match/);
});

test('selection survives hidden rows, quotes unusual paths, and can be cleared', () => {
  const ui = setup([row('folder/quote"\nname.py', 400, 800, 2)]);
  ui.click('select'); ui.input('query', 'no match');
  assert.equal(ui.get('count').textContent, '0 match · 1 selected');
  assert.match(ui.get('request').value, /quote\\"\\nname/);
  assert.match(ui.get('files').children[0].children[0].textContent, /No measured files/);
  ui.click('clear'); assert.match(ui.get('brief-count').textContent, /Starter request/);
  assert.match(ui.get('request').value, /quote/);
});

test('pagination selects only displayed files and sort changes row order', () => {
  const rows = Array.from({length: 301}, (_,i) => row(`file${i}.py`, 400+i, 1000-i, 1));
  const ui = setup(rows);
  assert.equal(ui.get('files').children.length, 250);
  ui.click('select'); assert.match(ui.get('count').textContent, /250 selected/);
  ui.click('more'); assert.equal(ui.get('files').children.length, 301);
  ui.input('sort', 'bytes');
  const fileCell = ui.get('files').children[0].children[1];
  assert.equal(fileCell.children[1].textContent, 'file0.py');
});

test('coverage gaps remain visible even with no matching files', () => {
  const ui = setup([], false);
  assert.match(ui.get('coverage').textContent, /Incomplete coverage/);
  assert.match(ui.get('statuses').textContent, /INCOMPLETE/);
});

test('clipboard failure selects the request for manual copying', async () => {
  const ui = setup([row('file.py', 400, 800, 2)]);
  ui.click('select'); await ui.click('copy');
  assert.equal(ui.get('request').selected, true);
  assert.match(ui.get('copy-status').textContent, /Text selected/);
});

test('default line threshold includes 150 and excludes 149', () => {
  const ui = setup([row('below.py', 149, 300, 2), row('boundary.py', 150, 300, 2), row('above.py', 151, 300, 2)]);
  assert.equal(ui.get('lines').value, '150');
  assert.match(ui.get('count').textContent, /^2 match/);
  ui.click('select');
  assert.doesNotMatch(ui.get('request').value, /below\.py/);
  assert.match(ui.get('request').value, /boundary\.py/);
  assert.match(ui.get('request').value, /Size is a review signal/);
  assert.match(ui.get('request').value, /Keep connected formats, generated data and cohesive owners/);
});

test('review request weighs splitting, keeping and combining supported files', () => {
  const ui = setup([row('App.xcodeproj/project.pbxproj', 935, 165704, 6175)]);
  ui.click('select');
  const request = ui.get('request').value;
  assert.match(request, /Keep connected formats/);
  assert.match(request, /Choose split, retain, combine/);
  assert.match(request, /initialization/);
  assert.match(request, /proposed boundary, risks and checks/);
  assert.match(request, /project\.pbxproj/);
});

test('snapshot describes this report without claiming other agents are idle', () => {
  const ui = setup([]);
  assert.match(ui.get('snapshot').textContent, /This report starts no agents/);
  assert.doesNotMatch(ui.get('snapshot').textContent, /No agent running/);
});
