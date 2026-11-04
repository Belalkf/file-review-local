const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const html = execFileSync('python3', ['-c',
  'from file_review.demo import example_report; from file_review.render import render; print(render(example_report()))'],
  {cwd: path.join(__dirname, '..'), encoding: 'utf8', timeout: 15000});
const base = JSON.parse(html.split('<script id="data" type="application/json">')[1].split('</script>')[0]);

// An in-memory document exercises local report behavior without a browser,
// network, clipboard access, or downloaded test dependencies.
class Element {
  constructor(fragment = false) {
    this.children = []; this.events = {}; this.value = ''; this.textContent = '';
    this.classList = {toggle() {}}; this.fragment = fragment;
  }
  append(...items) { for (const item of items) this.children.push(...(item.fragment ? item.children : [item])); }
  replaceChildren(...items) {this.children = []; this.append(...items);}
  setAttribute() {}
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {this.focused = true;}
  select() {this.selected = true;}
}

function setup(rows, complete = true) {
  const elements = {};
  const get = id => elements[id] ||= new Element();
  get('data').textContent = JSON.stringify({...base, default_rows: rows.map((_, i) => i).slice(0, 12), created: '2026-10-19T12:00:00Z', rows,
    max_bytes: 16777216, seconds: 60, repositories: [{name: 'example', root: '/local/project',
    complete, measured: rows.length, listed: rows.length, skipped: {}, issues: []}]});
  const template = fs.readFileSync(path.join(__dirname, '../file_review/report.html'), 'utf8');
  for (const id of ['lines', 'bytes', 'longest']) {
    get(id).value = template.match(new RegExp(`id="${id}"[^>]*value="([^"]+)"`))[1];
  }
  get('sort').value = 'review';
  const context = vm.createContext({document: {getElementById: get,
    createElement: () => new Element(), createDocumentFragment: () => new Element(true)}, navigator: {}});
  // Execute only this checkout's trusted report implementation, never scanned project code.
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../file_review/report.js'), 'utf8'), context);
  return {get, click: id => get(id).events.click(),
    input(id, value) {get(id).value = value; get(id).events.input();}};
}

function row(path, lines, bytes, longest_line) {return {repository: 'example', path, lines, bytes, longest_line};}
module.exports = {setup, row};
