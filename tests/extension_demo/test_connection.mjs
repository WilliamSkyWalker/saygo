import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
import {Clock} from './clock.mjs';

const source = await readFile(new URL('../../extensions/saygo-browser/background.js', import.meta.url), 'utf8');
function browser(tabs = [{id:1,url:'https://example.test'}]) {
  let disconnected = 0;
  const clock=new Clock();
  const removed = [];
  const messages = [];
  const listeners = {};
  const listener = {addListener() {}};
  const port = {
    onDisconnect:listener,
    onMessage:{addListener(fn) { listeners.message = fn; }},
    postMessage(message) { messages.push(message); }, disconnect() { disconnected++; }
  };
  const context = vm.createContext({
    setTimeout:clock.setTimeout,clearTimeout:clock.clearTimeout,Date:clock.Date,
    NetworkJournal:class {},
    chrome:{
      storage:{local:{get:async () => ({}),set:async () => {}},session:{get:async () => ({epoch:'test',blocked:[]}),set:async () => {}}},
      tabs:{query:async () => tabs, remove:async id => removed.push(id),
        onCreated:listener,onUpdated:listener,onRemoved:listener},
      debugger:{onDetach:listener,onEvent:listener},
      runtime:{onStartup:listener,connectNative:() => port,onMessage:listener,getManifest:() => ({version:'test'})}
    }
  });
  vm.runInContext(source.replace("import {NetworkJournal} from './network.js';", ''), context);
  return {clock, context, removed, listeners, messages, disconnected:() => disconnected,
    connected:() => vm.runInContext('port !== null', context),
    activate:() => vm.runInContext('port = {}; negotiated = true;', context)};
}

test('native response chunks preserve Unicode at frame boundaries', async () => {
  const b=browser([]);
  const connected=b.context.connect();
  await new Promise(resolve=>setImmediate(resolve));
  b.listeners.message({type:'hello',protocol:1});
  await connected;
  const prefix=JSON.stringify({result:''}).indexOf('""')+1;
  const body='x'.repeat(100000-prefix-1)+'😀尾'.repeat(40000);
  b.context.execute=async()=>body;
  b.listeners.message({id:'large',operation:'network_read',deadline:Date.now()/1000+60});
  await new Promise(resolve=>setImmediate(resolve));
  const frames=b.messages.filter(m=>m.id==='large');
  assert.ok(frames.length>1);
  for (const frame of frames) {
    assert.ok(frame.chunk.isWellFormed(), 'a native frame must not split a Unicode code point');
    assert.ok(Buffer.byteLength(JSON.stringify(frame))<1024*1024);
  }
  assert.equal(frames.at(-1).last,true);
  assert.equal(JSON.parse(frames.map(f=>f.chunk).join('')).result,body);
});

test('handshake timeout keeps the native port open', async () => {
  const b = browser();
  const rejection=assert.rejects(b.context.connect(), /handshake timed out/);
  await b.clock.advance(10000);
  await rejection;
  assert.equal(b.disconnected(), 0);
  assert.equal(b.connected(), true);
});

test('protocol mismatch keeps the native port open', async () => {
  const b = browser();
  const pending = b.context.connect();
  await new Promise(resolve => setImmediate(resolve));
  b.listeners.message({type:'hello',protocol:99});
  await assert.rejects(pending, /protocol mismatch/);
  assert.equal(b.disconnected(), 0);
  assert.equal(b.connected(), true);
});

test('timed-out input allows reads, rejects overlapping input, and is not replayed', async () => {
  const b = browser();
  let finish;
  const calls = [];
  b.context.execute = async operation => {
    calls.push(operation);
    if (operation === 'scroll_at') await new Promise(resolve => { finish = resolve; });
    return operation;
  };
  const rejection=assert.rejects(b.context.runRequest('scroll_at'), /outcome unknown/);
  await b.clock.advance(20000);
  await rejection;
  assert.equal(await b.context.runRequest('screenshot'), 'screenshot');
  assert.equal(await b.context.runRequest('pages'), 'pages');
  await assert.rejects(b.context.runRequest('tap'), /still pending/);
  finish();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(await b.context.runRequest('tap'), 'tap');
  assert.deepEqual(calls, ['scroll_at','screenshot','pages','tap']);
  assert.equal(b.disconnected(), 0);
});

test('closing the last tab is rejected, other tabs can be closed', async () => {
  const b = browser(); b.activate();
  await assert.rejects(b.context.execute('close', {page_id:'test:1'}), /last browser tab manually/);
  assert.deepEqual(b.removed, []);
  const multi = browser([{id:1,url:'https://example.test'}, {id:2,url:'https://example.test/other'}]);
  multi.activate();
  await multi.context.execute('close', {page_id:'test:1'});
  assert.deepEqual(multi.removed, [1]);
});
