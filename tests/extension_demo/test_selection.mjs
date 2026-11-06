import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../../extensions/saygo-browser/background.js', import.meta.url), 'utf8');

function browser(state = 'normal') {
  const tabs = [
    {id:1, windowId:10, url:'https://example.test/first', active:true},
    {id:2, windowId:10, url:'https://example.test/second', active:false},
    {id:3, windowId:20, url:'https://example.test/cover', active:true}
  ];
  const windows = [{id:10, state, focused:false}, {id:20, state:'normal', focused:true}];
  const changes = [];
  const listener = {addListener() {}};
  const context = vm.createContext({
    setTimeout, clearTimeout, Date,
    NetworkJournal:class {},
    chrome:{
      storage:{local:{get:async () => ({})}, session:{get:async () => ({epoch:'test', blocked:[]})}},
      tabs:{query:async () => tabs,
        update:async (id, options) => {
          const tab = tabs.find(t => t.id === id);
          changes.push({tab:id, options});
          if (options.active) for (const item of tabs) {
            if (item.windowId === tab.windowId) item.active = item.id === id;
          }
          return tab;
        }, onCreated:listener, onUpdated:listener, onRemoved:listener},
      windows:{update:async (id, options) => {
        changes.push({window:id, options});
        if (options.focused) for (const item of windows) item.focused = item.id === id;
        return windows.find(w => w.id === id);
      }},
      debugger:{onDetach:listener, onEvent:listener},
      runtime:{onStartup:listener, onMessage:listener}
    }
  });
  vm.runInContext(source.replace("import {NetworkJournal} from './network.js';", '') +
    '\nport = {}; negotiated = true;', context);
  return {tabs, windows, changes, select:id => context.runRequest('select', {page_id:id})};
}

for (const state of ['normal', 'maximized', 'minimized']) {
  test(`selecting and reselecting a tab preserves the foreground ${state} window state`, async () => {
    const b = browser(state);
    const before = structuredClone(b.windows);
    for (const page of ['test:2', 'test:2', 'test:1']) {
      await b.select(page);
      assert.equal(b.tabs.find(t => t.windowId === 10 && t.active).id, Number(page.split(':')[1]));
      assert.deepEqual(b.windows, before);
      assert.equal(b.changes.some(change => 'window' in change), false);
      assert.equal(b.tabs[2].active, true);
    }
  });
}

test('stale and closed page selections fail without changing any tab or window', async () => {
  const b = browser();
  for (const page of ['old:2', 'test:999']) {
    await assert.rejects(b.select(page), /Page closed, control released or browser restarted/);
  }
  assert.deepEqual(b.changes, []);
});
