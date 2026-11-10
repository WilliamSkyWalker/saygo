import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
import {Clock} from './clock.mjs';

const source = await readFile(new URL('../../extensions/saygo-browser/background.js', import.meta.url), 'utf8');
function browser({href='https://example.test/resolved', download=false, missing=false, detached=false, handler, createError=false} = {}) {
  const calls = [], created = [], clock = new Clock();
  const tab = {id:7, windowId:3, url:'https://example.test/source', active:false};
  const anchor = {nodeType:1, localName:'a', namespaceURI:'http://www.w3.org/1999/xhtml',
    href, hasAttribute:name => name === 'href' || (name === 'download' && download)};
  const hit = {nodeType:1, isConnected:!detached, localName:'span', parentElement:missing ? null : anchor};
  const listener = {addListener() {}};
  const context = vm.createContext({setTimeout:clock.setTimeout, clearTimeout:clock.clearTimeout, Date:clock.Date,
    URL, NetworkJournal:class {}, chrome:{
      storage:{local:{get:async () => ({})}, session:{get:async () => ({epoch:'test', blocked:[]})}},
      tabs:{query:async () => [tab], get:async () => ({...tab}),
        create:async options => { created.push(JSON.parse(JSON.stringify(options))); if (createError) throw Error('creation outcome unknown'); return {id:8}; },
        update:async () => { throw Error('Must not activate a tab'); },
        onCreated:listener, onUpdated:listener, onRemoved:listener},
      debugger:{attach:async () => {}, onDetach:listener, onEvent:listener,
        sendCommand:async (target, method, params) => {
          calls.push({target, method, params});
          const intercepted = handler?.(method, params, tab);
          if (intercepted !== undefined) return intercepted;
          if (method === 'Page.getLayoutMetrics') return {cssVisualViewport:{clientWidth:800, clientHeight:600}};
          if (method === 'DOM.getNodeForLocation') return {backendNodeId:17, frameId:'frame'};
          if (method === 'Page.createIsolatedWorld') return {executionContextId:11};
          if (method === 'DOM.resolveNode') return {object:{objectId:'point-node'}};
          if (method === 'Runtime.callFunctionOn') return {result:{value:vm.runInNewContext('(' + params.functionDeclaration + ')').call(hit)}};
        }},
      runtime:{onStartup:listener, onMessage:listener}
    }});
  vm.runInContext(source.replace("import {NetworkJournal} from './network.js';", '') +
    '\nport = {}; negotiated = true;', context);
  return {calls, created, tab, clock, context,
    run:(operation='open_link_background', args = {}) => context.runRequest(operation, {page_id:'test:7', x:40, y:80, ...args})};
}

test('coordinate link URL is read in an isolated world and opened inactive in the same window', async () => {
  const b = browser();
  const result = await b.run();
  assert.equal(result.page_id, 'test:8');
  assert.deepEqual(b.created, [{url:'https://example.test/resolved', active:false, windowId:3}]);
  assert.equal(b.tab.active, false);
  const locate = b.calls.find(c => c.method === 'DOM.getNodeForLocation');
  assert.deepEqual([locate.target.tabId, locate.params.x, locate.params.y], [7, 40, 80]);
  const resolve = b.calls.find(c => c.method === 'DOM.resolveNode');
  assert.equal(resolve.params.executionContextId, 11);
  const read = b.calls.find(c => c.method === 'Runtime.callFunctionOn');
  assert.equal(read.params.userGesture, false);
  assert.equal(read.params.objectId, 'point-node');
  assert.equal(b.calls.at(-1).method, 'Runtime.releaseObjectGroup');
  assert.equal(b.calls.some(c => c.method.startsWith('Input.')), false);
});

test('ordinary taps keep their left-click semantics', async () => {
  const b = browser();
  await b.run('tap');
  assert.deepEqual(b.calls.filter(c => c.method.startsWith('Input.')).map(c => c.params.button), ['left', 'left']);
  assert.deepEqual(b.created, []);
});

test('invalid and stale coordinates never read a node or create a tab', async () => {
  const b = browser();
  for (const args of [{x:-1}, {y:600}, {x:800}, {x:NaN}, {page_id:'old:7'}])
    await assert.rejects(b.run('open_link_background', args), /Invalid coordinates|outside viewport|Page closed/);
  assert.equal(b.calls.some(c => c.method.startsWith('DOM.')), false);
  assert.deepEqual(b.created, []);
});

test('non-links, downloads and unsupported URLs are rejected without click fallback', async () => {
  for (const options of [{missing:true}, {download:true}, {href:'javascript:alert(1)'}, {href:'file:///tmp/fixture'}, {href:'invalid'}]) {
    const b = browser(options);
    await assert.rejects(b.run(), /hyperlink|Download|HTTP/);
    assert.deepEqual(b.created, []);
    assert.equal(b.calls.some(c => c.method.startsWith('Input.')), false);
    assert.equal(b.calls.at(-1).method, 'Runtime.releaseObjectGroup');
  }
});

test('navigation during lookup invalidates the URL and prevents creation', async () => {
  const b = browser({handler(method, params, tab) { if (method === 'Runtime.callFunctionOn') tab.url += '/changed'; }});
  await assert.rejects(b.run(), /page\/control changed/);
  assert.deepEqual(b.created, []);
});

test('a hit removed from the same document cannot open a stale link', async () => {
  const b = browser({detached:true});
  await assert.rejects(b.run(), /target changed/);
  assert.deepEqual(b.created, []);
  assert.equal(b.calls.at(-1).method, 'Runtime.releaseObjectGroup');
});

test('late link lookup cannot create a tab after timeout', async () => {
  let finish;
  const b = browser({handler(method) { if (method === 'Runtime.callFunctionOn') return new Promise(resolve => { finish = resolve; }); }});
  const rejection = assert.rejects(b.run(), /outcome unknown/);
  await b.clock.advance(20000);
  await rejection;
  await assert.rejects(b.run(), /input is still pending/);
  finish({result:{value:{url:'https://example.test/late'}}});
  await new Promise(resolve => setImmediate(resolve));
  assert.deepEqual(b.created, []);
  assert.equal(vm.runInContext('inputPending', b.context), false);
});

test('unknown tab creation outcome is never retried', async () => {
  const b = browser({createError:true});
  await assert.rejects(b.run(), /creation outcome unknown/);
  assert.equal(b.created.length, 1);
});
