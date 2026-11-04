const {test} = require('node:test');
const assert = require('node:assert/strict');
const {setup, row} = require('./report_harness.cjs');

test('starter request is ready, bounded, and explicitly independent of table filters', () => {
  const ui = setup(Array.from({length: 20}, (_,i) => row(`file${i}.rs`, 400+i, 2000, 80)));
  assert.match(ui.get('brief-count').textContent, /12 of 20/);
  assert.match(ui.get('request').value, /decision table/);
  assert.match(ui.get('request').value, /No language parsing/);
  assert.match(ui.get('request').value, /file0.rs/);
  assert.doesNotMatch(ui.get('request').value, /file19.rs/);
  ui.input('query', 'no match');
  assert.match(ui.get('brief-count').textContent, /regardless of table filters/);
  assert.match(ui.get('request').value, /file0.rs/);
});

test('task updates both starter and selected requests without being HTML', () => {
  const ui = setup([row('owner.swift', 400, 2000, 80)]);
  ui.input('task', 'Fix "export" <script>');
  assert.match(ui.get('request').value, /User task: "Fix \\"export/);
  ui.click('select');
  assert.match(ui.get('request').value, /User task:/);
  assert.match(ui.get('brief-count').textContent, /all 1 selected/);
});

test('explicit selection includes every chosen file, not just twelve', () => {
  const ui = setup(Array.from({length: 20}, (_,i) => row(`file${i}.rs`, 400+i, 2000, 80)));
  ui.click('select');
  assert.match(ui.get('request').value, /file19.rs/);
  assert.match(ui.get('brief-count').textContent, /all 20 selected/);
});

test('empty inventory produces useful caution instead of an empty request', () => {
  const ui = setup([]);
  assert.match(ui.get('request').value, /No measured text files/);
  assert.match(ui.get('request').value, /not a clean bill of health/);
});

test('copied request keeps facts and format warnings without repeating evidence instructions', () => {
  const rows = Array.from({length: 12}, (_, i) => ({...row(`file${i}.rs`, 400, 2000, 80),
    sha256: 'a'.repeat(64), review: {action: i ? 'inspect' : 'check-owner',
      summary: 'REPEATED SUMMARY', steps: ['REPEATED STEP']}}));
  const ui = setup(rows);
  const request = ui.get('request').value;
  assert.equal((request.match(/Choose split, retain, combine/g) || []).length, 1);
  assert.equal((request.match(/Measured SHA-256:/g) || []).length, 12);
  assert.match(request, /Path hint: inspect format or producer/);
  assert.doesNotMatch(request, /REPEATED SUMMARY|REPEATED STEP/);
  assert.match(request, /No model was called/);
});
