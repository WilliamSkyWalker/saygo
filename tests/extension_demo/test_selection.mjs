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
        create:async options => {
          changes.push({create:{...options}});
          const windowId = options.windowId ?? 20;
          const active = options.active ?? true;
          if (active) for (const item of tabs) {
            if (item.windowId === windowId) item.active = false;
          }
          const tab = {id:4, windowId, url:options.url, active};
          tabs.push(tab);
          return tab;
        },
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
  return {tabs, windows, changes,
    select:id => context.runRequest('select', {page_id:id}),
    create:url => context.runRequest('new_page', {url}),
    disconnect:() => vm.runInContext('port = null; negotiated = false;', context)};
}

for (const state of ['normal', 'maximized', 'minimized']) {
  test(`selecting and reselecting a tab preserves activity and ${state} window state`, async () => {
    const b = browser(state);
    const before = structuredClone({tabs:b.tabs, windows:b.windows});
    for (const page of ['test:2', 'test:2', 'test:1', 'test:3']) {
      await b.select(page);
      assert.deepEqual({tabs:b.tabs, windows:b.windows}, before,
        'logical selection must leave every visible tab and window unchanged');
      assert.deepEqual(b.changes, [], 'selection must not dispatch tab/window updates');
    }
  });

  test(`creating a page leaves existing tabs and ${state} windows unchanged`, async () => {
    const b = browser(state);
    const before = structuredClone({tabs:b.tabs, windows:b.windows});
    const url = 'https://example.test/created';
    const result = await b.create(url);
    assert.equal(result.page_id, 'test:4');
    assert.deepEqual(b.changes, [{create:{url, active:false}}]);
    assert.deepEqual(b.tabs.slice(0, before.tabs.length), before.tabs);
    assert.deepEqual(b.windows, before.windows);
    assert.equal(b.tabs.at(-1).url, url);
    assert.equal(b.tabs.at(-1).active, false);
  });
}

test('stale and closed page selections fail without changing any tab or window', async () => {
  const b = browser();
  for (const page of ['old:2', 'test:999']) {
    await assert.rejects(b.select(page), /Page closed, control released or browser restarted/);
  }
  assert.deepEqual(b.changes, []);
});

test('unsupported new-page URLs fail before creating a tab', async () => {
  const b = browser();
  const before = structuredClone({tabs:b.tabs, windows:b.windows});
  for (const url of ['about:blank', 'file:///fixture.html', 'javascript:void(0)', '']) {
    await assert.rejects(b.create(url), /Only HTTP\(S\) navigation is allowed/);
  }
  assert.deepEqual({tabs:b.tabs, windows:b.windows}, before);
  assert.deepEqual(b.changes, []);
});

test('disconnected selection and creation fail without changing tabs or windows', async () => {
  const b = browser();
  const before = structuredClone({tabs:b.tabs, windows:b.windows});
  b.disconnect();
  await assert.rejects(b.select('test:2'), /Page closed, control released or browser restarted/);
  await assert.rejects(b.create('https://example.test/created'), /Browser is disconnected/);
  assert.deepEqual({tabs:b.tabs, windows:b.windows}, before);
  assert.deepEqual(b.changes, []);
});
