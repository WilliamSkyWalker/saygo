import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {randomUUID} from 'node:crypto';
import vm from 'node:vm';
import {Clock} from './clock.mjs';

const source = await readFile(new URL('../../extensions/saygo-browser/background.js', import.meta.url), 'utf8');
function deferred() {
  let resolve;
  const promise = new Promise(done => { resolve = done; });
  return {promise, resolve};
}
function browser(local = {}, hooks = {}) {
  const clock = new Clock(), events = {}, ports = [], attachments = new Set();
  const session = {};
  const listener = name => ({addListener(fn) { events[name] = fn; }});
  const context = vm.createContext({
    setTimeout:clock.setTimeout, clearTimeout:clock.clearTimeout, Date:clock.Date,
    crypto:{randomUUID},
    NetworkJournal:class {
      tabs = new Map();
      begin(id) { this.tabs.set(id, {active:true}); }
      end(id) { this.tabs.delete(id); }
      reset() { this.tabs.clear(); }
    },
    chrome:{
      storage:{
        local:{get:async () => { await hooks.read?.(); return {...local}; },
          set:async data => { await hooks.write?.(data); Object.assign(local, data); }},
        session:{get:async () => { await hooks.sessionRead?.(); return {...session}; },
          set:async data => { await hooks.sessionWrite?.(data); Object.assign(session, data); }}
      },
      tabs:{query:async () => { await hooks.query?.(); return [{id:1,url:'https://example.test/fixture'}]; },
        onCreated:listener('created'), onUpdated:listener('updated'), onRemoved:listener('removed')},
      debugger:{attach:async ({tabId}) => { await hooks.attach?.(); attachments.add(tabId); },
        detach:async ({tabId}) => { await hooks.detach?.(); attachments.delete(tabId); },
        sendCommand:async () => ({}), onDetach:listener('detach'), onEvent:listener('debug')},
      runtime:{id:'test-extension', getManifest:() => ({version:'test'}),
        onStartup:listener('startup'), onMessage:listener('message'),
        connectNative() {
          const handlers = {};
          const port = {disconnected:false,
            onDisconnect:{addListener(fn) { handlers.disconnect = fn; }},
            onMessage:{addListener(fn) { handlers.message = fn; }},
            postMessage() {}, disconnect() { port.disconnected = true; },
            hello(protocol = 1) { handlers.message({type:'hello',protocol}); },
            fail() { port.disconnected = true; handlers.disconnect(); }};
          ports.push(port);
          if (hooks.autoHello !== false) Promise.resolve().then(() => port.hello());
          return port;
        }
      }
    }
  });
  vm.runInContext(source.replace("import {NetworkJournal} from './network.js';", ''), context);
  return {clock, context, events, ports, attachments,
    send:type => new Promise(resolve => events.message({type}, {id:'test-extension'}, resolve)),
    async startup() { events.startup?.(); await clock.flush(); }};
}

test('first install and missing legacy preference stay disconnected', async () => {
  const b = browser();
  await b.startup();
  assert.equal(b.ports.length, 0);
  assert.equal((await b.send('status')).connected, false);
});

test('a successful connection resumes after a new browser session with a new page identity', async () => {
  const local = {}, first = browser(local);
  const before = await first.send('connect');
  assert.equal(before.connected, true);
  const second = browser(local);
  await second.startup();
  assert.equal(second.ports.length, 1, 'the previous enabled state must restore its native connection');
  const after = await second.send('status');
  assert.equal(after.connected, true);
  assert.notEqual(after.pages[0].page_id, before.pages[0].page_id);
  await assert.rejects(second.context.target(before.pages[0].page_id), /restarted/);
});

test('explicit release is remembered across repeated restarts', async () => {
  const local = {}, b = browser(local);
  await b.send('connect');
  assert.equal((await b.send('release')).connected, false);
  for (let i = 0; i < 2; i++) {
    const restarted = browser(local);
    await restarted.startup();
    assert.equal(restarted.ports.length, 0);
    assert.equal((await restarted.send('status')).reconnect_on_startup, false);
  }
});

test('a service worker wakeup alone never restores control', async () => {
  const b = browser({reconnectOnStartup:true});
  await b.clock.flush();
  await b.send('status');
  assert.equal(b.ports.length, 0);
});

test('native host failure preserves intent without an immediate reconnect loop', async () => {
  const local = {}, b = browser(local);
  await b.send('connect');
  b.ports[0].fail();
  await b.clock.advance(30000);
  assert.equal((await b.send('status')).connected, false);
  assert.equal(b.ports.length, 1);
  const restarted = browser(local);
  await restarted.startup();
  assert.equal(restarted.ports.length, 1);
});

for (const [reason, expected] of [['canceled_by_user', false], ['target_closed', true]]) {
  test(`debugger ${reason} sets the next browser startup state correctly`, async () => {
    const local = {}, b = browser(local);
    await b.send('connect');
    b.events.detach({tabId:1}, reason);
    await b.clock.flush();
    if (!expected) assert.equal((await b.send('status')).pages.length, 0);
    const restarted = browser(local);
    await restarted.startup();
    assert.equal(restarted.ports.length, Number(expected));
  });
}

test('startup and simultaneous Connect requests share one native handshake', async () => {
  const b = browser({reconnectOnStartup:true}, {autoHello:false});
  b.events.startup?.();
  const first = b.send('connect'), second = b.send('connect');
  await b.clock.flush();
  assert.equal(b.ports.length, 1);
  b.ports[0].hello();
  assert.equal((await first).connected, true);
  assert.equal((await second).connected, true);
});

test('Release during startup preference lookup prevents a later automatic connection', async () => {
  const gate = deferred(), local = {reconnectOnStartup:true};
  const b = browser(local, {read:() => gate.promise});
  b.events.startup?.();
  const released = b.send('release');
  gate.resolve();
  await released;
  await b.clock.flush();
  assert.equal(b.ports.length, 0);
  assert.equal(local.reconnectOnStartup, false);
});

test('Release cancels a connection before native dispatch', async () => {
  const gate = deferred();
  let writes = 0;
  const b = browser({}, {sessionWrite:() => ++writes === 2 ? gate.promise : undefined});
  await b.clock.flush();
  const connecting = b.send('connect');
  await b.clock.flush();
  const released = b.send('release');
  gate.resolve();
  await Promise.all([connecting, released]);
  assert.equal(b.ports.length, 0);
});

test('Release during handshake rejects late messages from the old port', async () => {
  const b = browser({}, {autoHello:false});
  const connecting = b.send('connect');
  await b.clock.flush();
  const old = b.ports[0];
  await b.send('release');
  old.hello();
  await connecting;
  const next = b.send('connect');
  await b.clock.flush();
  old.hello();
  assert.equal((await b.send('status')).connected, false);
  b.ports[1].hello();
  assert.equal((await next).connected, true);
});

test('Release wins over a delayed successful-connection preference write', async () => {
  const gate = deferred(), local = {};
  const b = browser(local, {write:data => data.reconnectOnStartup ? gate.promise : undefined});
  const connecting = b.send('connect');
  await b.clock.flush();
  const released = b.send('release');
  gate.resolve();
  await Promise.all([connecting, released]);
  assert.equal(local.reconnectOnStartup, false);
  assert.equal((await b.send('status')).connected, false);
});

test('reconnection waits for the previous debugger cleanup', async () => {
  const gate = deferred(), b = browser({}, {detach:() => gate.promise});
  await b.send('connect');
  const released = b.send('release');
  await b.clock.flush();
  const connecting = b.send('connect');
  await b.clock.flush();
  assert.equal(b.ports.length, 1, 'old detach must finish before a new native connection');
  gate.resolve();
  await Promise.all([released, connecting]);
  assert.equal((await b.send('status')).connected, true);
  assert.equal(b.attachments.has(1), true);
});

test('failed persistence reports an error while Release still removes current control', async () => {
  let fail = false;
  const b = browser({}, {write:() => { if (fail) throw new Error('disk unavailable'); }});
  await b.send('connect');
  fail = true;
  const result = await b.send('release');
  assert.match(result.error, /startup|preference/i);
  assert.match(result.error, /disk unavailable/);
  const status = await b.send('status');
  assert.equal(status.connected, false);
  assert.equal(status.reconnect_on_startup, null, 'failed persistence must not claim startup is off');
  assert.equal(b.ports[0].disconnected, true);
  assert.equal(b.attachments.size, 0);
});

test('a failed first handshake does not opt a new installation into startup reconnect', async () => {
  const local = {}, b = browser(local, {autoHello:false});
  const pending = b.send('connect');
  await b.clock.flush();
  b.ports[0].hello(99);
  assert.match((await pending).error, /protocol mismatch/);
  const restarted = browser(local);
  await restarted.startup();
  assert.equal(restarted.ports.length, 0);
});

test('Cancel during an unfinished connection cannot be overwritten by the handshake', async () => {
  const local = {}, b = browser(local, {autoHello:false});
  const connecting = b.send('connect');
  await b.clock.flush();
  b.events.detach({tabId:1}, 'canceled_by_user');
  await b.clock.flush();
  b.ports[0].hello();
  await connecting;
  assert.equal(local.reconnectOnStartup, false);
  const restarted = browser(local);
  await restarted.startup();
  assert.equal(restarted.ports.length, 0);
});

test('startup storage read failure stays disconnected and reports the failure', async () => {
  const b = browser({reconnectOnStartup:true}, {read:() => { throw new Error('storage unreadable'); }});
  await b.startup();
  assert.equal(b.ports.length, 0);
  const status = await b.send('status');
  assert.match(status.error, /storage unreadable/);
  assert.equal(status.reconnect_on_startup, null);
});

test('a failed automatic handshake is visible and is not retried until the next startup', async () => {
  const local = {reconnectOnStartup:true}, b = browser(local, {autoHello:false});
  await b.startup();
  assert.equal(b.ports.length, 1);
  await b.clock.advance(10000);
  const status = await b.send('status');
  assert.equal(status.connected, false);
  assert.match(status.error, /handshake timed out/);
  await b.clock.advance(30000);
  assert.equal(b.ports.length, 1);
  assert.equal(local.reconnectOnStartup, true);
});

test('Release waits for an in-flight debugger attachment before reconnecting', async () => {
  const gate = deferred();
  let attaches = 0;
  const b = browser({}, {attach:() => ++attaches === 1 ? gate.promise : undefined});
  const first = b.send('connect');
  await b.clock.flush();
  assert.equal(attaches, 1);
  const released = b.send('release');
  const second = b.send('connect');
  await b.clock.flush();
  gate.resolve();
  await Promise.all([first, released, second]);
  assert.equal((await b.send('status')).connected, true);
  assert.equal(b.attachments.has(1), true);
});

test('a delayed network startup cannot attach after Release', async () => {
  const gate = deferred(), hooks = {}, b = browser({}, hooks);
  await b.send('connect');
  hooks.sessionRead = () => gate.promise;
  const network = b.context.startNetwork(2);
  await b.clock.flush();
  const released = b.send('release');
  await b.clock.flush();
  assert.equal(b.attachments.size, 0);
  gate.resolve();
  await Promise.all([network, released]);
  assert.equal(b.attachments.size, 0, 'old network setup must not reattach after control was revoked');
});

for (const reconnect of [false, true]) {
  test(`Release invalidates a delayed page query${reconnect ? ' even after reconnect' : ''}`, async () => {
    const gate = deferred(), hooks = {}, b = browser({}, hooks);
    const connected = await b.send('connect');
    hooks.query = () => { delete hooks.query; return gate.promise; };
    const input = b.context.execute('input', {page_id:connected.pages[0].page_id, text:'stale input'});
    const rejected = assert.rejects(input, /released|restarted/i);
    await b.clock.flush();
    await b.send('release');
    if (reconnect) await b.send('connect');
    gate.resolve();
    await rejected;
    assert.equal(b.attachments.size, Number(reconnect));
  });
}
