// Opt-in CLI -> native host -> extension test with another native app in front.
// Requires SAYGO_TEST_CHROME, SAYGO_TEST_PYTHON (with AppKit/Quartz), and optionally
// SAYGO_TEST_PLAYWRIGHT_MODULE (module path/name; defaults to playwright).
// SAYGO_TEST_FOCUS_DIAGNOSTICS=1 enables isolated bridge/capture probes before the regression.
// SAYGO_TEST_FOCUS_LEFT_CLICK=1 runs the ordinary-click failure reproduction instead of acceptance.
import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {dirname, join, resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {mkdtemp, mkdir, cp, copyFile, readFile, writeFile, realpath, rm} from 'node:fs/promises';
import {createHash, randomUUID} from 'node:crypto';
import {createServer} from 'node:http';
import {spawn, execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createInterface} from 'node:readline';

const run = promisify(execFile);
const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../..');
const enabled = process.platform === 'darwin' && process.env.SAYGO_TEST_HEADED === '1' &&
  process.env.SAYGO_TEST_CHROME && process.env.SAYGO_TEST_PYTHON;

test('macOS background page selection, creation and link opening preserve foreground application',
  {skip: !enabled, timeout: 180000}, async () => {
    const require = createRequire(import.meta.url);
    const {chromium} = require(process.env.SAYGO_TEST_PLAYWRIGHT_MODULE || 'playwright');
    const python = process.env.SAYGO_TEST_PYTHON;
    const root = await realpath(await mkdtemp(join(tmpdir(), 'saygo-mac-focus-')));
    const extension = join(root, 'extension');
    const profile = join(root, 'profile');
    const bridge = join(root, 'bridge');
    const nativeHost = 'com.example.saygo_focus_' + randomUUID().replaceAll('-', '');
    const env = {...process.env, PYTHONPATH: repo, SAYGO_HOME_DIR: join(root, 'saygo-home'),
      SAYGO_RUNTIME_DIR: join(root, 'runtime'), XDG_CONFIG_HOME: join(root, '.config')};
    const server = createServer((req, res) => {
      res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
      const created = req.url === '/created';
      const popup = req.url === '/popup';
      res.end(`<!doctype html><title>Focus fixture</title><style>body{margin:0;background:${created ? '#ddeeff' : '#ccffdd'}}
        input{position:absolute;left:20px;top:80px;width:300px;height:40px}
        a{position:absolute;left:20px;top:160px;width:300px;height:40px;display:block}
        button{position:absolute;left:20px;top:230px;width:300px;height:40px}</style>
        <h1>${created ? 'Created page' : popup ? 'Popup page' : 'Original page'}</h1>
        <input aria-label="Fixture input"><a href="/popup" target="_blank"
          onclick="window.fixtureLinkClicks=(window.fixtureLinkClicks||0)+1">Open popup fixture</a>
        <button onclick="window.open('/unexpected-button-popup')">Button without a hyperlink</button>`);
    });
    let context, cover;
    const pending = [];
    let coverError = '';
    try {
      await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
      const url = `http://127.0.0.1:${server.address().port}`;
      await cp(process.env.SAYGO_TEST_EXTENSION || join(repo, 'extensions/saygo-browser'), extension, {recursive: true});
      // A unique host name prevents touching any installed user's native host,
      // even if this browser ignores the disposable profile's manifest folder.
      const background = join(extension, 'background.js');
      const source = await readFile(background, 'utf8');
      assert.equal(source.split('connectNative("com.saygo.browser")').length, 2);
      await writeFile(background, source.replace('connectNative("com.saygo.browser")', `connectNative("${nativeHost}")`));
      const manifest = JSON.parse(await readFile(join(extension, 'manifest.json'), 'utf8'));
      const eid = createHash('sha256').update(Buffer.from(manifest.key, 'base64')).digest('hex').slice(0, 32)
        .replace(/[0-9a-f]/g, ch => String.fromCharCode(97 + parseInt(ch, 16)));
      await run(python, ['-c', `from pathlib import Path
from unittest.mock import patch
from saygo.integrations.browser_bridge import install
import sys
with patch('pathlib.Path.home', return_value=Path(sys.argv[1])), patch('saygo.integrations.browser_bridge.HOST', sys.argv[4]):
    install(sys.argv[2], sys.argv[3], 'chrome')`, root, bridge, eid, nativeHost], {cwd: root, env});
      await mkdir(join(profile, 'NativeMessagingHosts'), {recursive: true});
      await copyFile(join(bridge, nativeHost + '.json'), join(profile, 'NativeMessagingHosts', nativeHost + '.json'));
      await mkdir(join(profile, 'Default'), {recursive: true});
      await writeFile(join(profile, 'Default/Preferences'), JSON.stringify({extensions: {ui: {developer_mode: true}}}));
      context = await chromium.launchPersistentContext(profile, {
        executablePath: process.env.SAYGO_TEST_CHROME, headless: false, viewport: null, env,
        ignoreDefaultArgs: ['--disable-extensions', '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding'],
        // Stable builds can ignore command-line extension loading, and an
        // except-list can block a CDP-loaded path after macOS resolves symlinks.
        args: ['--enable-unsafe-extension-debugging', '--enable-extension-targets']
      });
      console.log('[focus setup] isolated browser launched: ' + context.browser().version());
      const cdp = await context.browser().newBrowserCDPSession();
      const loaded = await cdp.send('Extensions.loadUnpacked', {path: extension});
      assert.equal(loaded.id, eid, 'CDP must load the isolated extension with the expected key');
      console.log('[focus setup] isolated extension loaded through CDP: ' + loaded.id);
      const browserPID = (await cdp.send('SystemInfo.getProcessInfo')).processInfo.find(p => p.type === 'browser').id;
      const page = context.pages()[0];
      await page.goto(url + '/original');
      const ui = await context.newPage();
      ui.on('pageerror', error => console.log('[focus setup] extension UI error: ' + error.message));
      try {
        await ui.goto(`chrome-extension://${eid}/popup.html`, {timeout: 10000});
      } catch (error) {
        // Report only this disposable extension's actual disabled/error state.
        const diagnostics = await context.newPage();
        try {
          await diagnostics.goto('chrome://extensions/', {timeout: 5000});
          const info = await diagnostics.evaluate(id => {
            if (!chrome.developerPrivate?.getExtensionsInfo) return {error: 'Extension diagnostics API unavailable'};
            return Promise.race([
              new Promise(resolve => chrome.developerPrivate.getExtensionsInfo(
                {includeDisabled: true, includeTerminated: true}, rows => {
                  if (chrome.runtime.lastError) return resolve({error: chrome.runtime.lastError.message});
                  const row = rows.find(row => row.id === id);
                  if (!row) return resolve({error: 'Isolated extension is absent from browser registration'});
                  resolve(Object.fromEntries(['id', 'state', 'disableReasons', 'runtimeErrors', 'manifestErrors',
                    'installWarnings', 'runtimeWarnings', 'location'].map(key => [key, row[key]])));
                })),
              new Promise(resolve => setTimeout(() => resolve({error: 'Extension diagnostics timed out'}), 3000))
            ]);
          }, eid);
          console.log('[focus setup] isolated extension diagnostics: ' + JSON.stringify(info));
        } catch (diagnosticError) {
          console.log('[focus setup] extension diagnostics unavailable: ' + diagnosticError.message);
        } finally { await diagnostics.close(); }
        throw error;
      }
      const loadedManifest = await ui.evaluate(() => ({id: chrome.runtime.id, version: chrome.runtime.getManifest().version}));
      assert.deepEqual(loadedManifest, {id: eid, version: manifest.version});
      // An idle MV3 worker need not appear in Playwright's serviceWorkers list.
      // Opening its own popup and sending a status message wakes it normally.
      const send = type => ui.evaluate(type => chrome.runtime.sendMessage({type}), type);
      const initialStatus = await send('status');
      assert.ok(initialStatus && typeof initialStatus === 'object', 'extension worker must answer status');
      console.log('[focus setup] extension popup and worker responded; connecting isolated native host');
      await send('connect');
      let status;
      for (let i = 0; i < 100; i++) {
        status = await send('status');
        if (status.connected && status.pages.length) break;
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      assert.equal(status.connected, true, JSON.stringify(status));
      console.log('[focus setup] isolated native host connected');
      let worker = context.serviceWorkers().find(worker => new URL(worker.url()).host === eid);
      if (!worker) {
        try {
          worker = await context.waitForEvent('serviceworker', {
            predicate: worker => new URL(worker.url()).host === eid, timeout: 5000
          });
        } catch { /* Some builds do not expose extension workers to Playwright. */ }
      }
      let tabOracle = worker;
      if (worker) {
        assert.equal(new URL(worker.url()).host, eid, 'read-only oracles require the isolated extension worker');
      } else {
        // Prepare before foreground checks; explicitly suppress page user gestures.
        const oracleSession = await context.newCDPSession(ui);
        tabOracle = {evaluate: async (fn, argument) => {
          const result = await oracleSession.send('Runtime.evaluate', {
            expression: `(${fn.toString()})(${JSON.stringify(argument) ?? 'undefined'})`,
            awaitPromise: true, returnByValue: true, userGesture: false
          });
          assert.equal(result.exceptionDetails, undefined, 'read-only extension oracle must succeed');
          return result.result.value;
        }};
        console.log('[focus setup] worker unavailable; read-only oracle uses explicit userGesture:false');
      }
      const popupScreenshot = process.env.SAYGO_TEST_FOCUS_POPUP_SCREENSHOT ||
        (process.env.SAYGO_TEST_FOCUS_SCREENSHOT ? process.env.SAYGO_TEST_FOCUS_SCREENSHOT.replace(/\.png$/i, '') + '-popup.png' :
          join(root, 'extension-popup.png'));
      await ui.reload();
      await ui.locator('#status').filter({hasText: 'Connected'}).waitFor({timeout: 5000});
      await ui.screenshot({path: popupScreenshot, fullPage: true});
      console.log('[focus setup] connected extension popup screenshot: ' + popupScreenshot);
      const original = status.pages.find(p => p.url === url + '/original').page_id;
      const tab = Number(original.split(':').at(-1));
      const windowId = (await ui.evaluate(id => chrome.tabs.get(id), tab)).windowId;
      const other = await ui.evaluate(o => chrome.tabs.create(o), {windowId, url: url + '/second', active: false});
      const second = original.slice(0, original.lastIndexOf(':') + 1) + other.id;
      const callCLI = async (expectOK, args) => {
        let result;
        try {
          result = await run(python, ['-m', 'saygo.cli', 'device', ...args, '--session', 'focus-test'],
            {cwd: root, env, timeout: 45000, maxBuffer: 2 * 1024 * 1024});
        } catch (error) {
          if (expectOK || error.code !== 2) throw error;
          result = error;
        }
        const data = JSON.parse(result.stdout);
        assert.equal(data.ok !== false, expectOK, result.stdout);
        if (!expectOK) assert.equal(result.code, 2, 'rejected CLI action must return the error exit code');
        return data;
      };
      const cli = (...args) => callCLI(true, args);
      const cliError = (...args) => callCLI(false, args);
      const raw = async (operation, pageId) => {
        const result = await run(python, ['-c', `import base64, io, json, sys
from PIL import Image
from saygo.integrations.browser_bridge import Client
result = Client(sys.argv[1]).call(sys.argv[2], page_id=sys.argv[3])
if sys.argv[2] == 'screenshot':
    with Image.open(io.BytesIO(base64.b64decode(result['data'], validate=True))) as image:
        image.verify()
    result = {'size': result['size'], 'png_verified': True}
print(json.dumps(result))`, bridge, operation, pageId], {cwd: root, env, timeout: 45000});
        return JSON.parse(result.stdout);
      };
      await cli('connect', '--platform', 'browser', '--backend', 'extension', '--bridge-directory', bridge, '--page-id', original);
      await ui.evaluate(id => chrome.tabs.update(id, {active: true}), tab);
      // Wait for setup's debugger attachment/network subscription, without
      // prewarming screenshots or selecting either regression target.
      let initialReady = false;
      for (let i = 0; i < 50; i++) {
        const samples = [await raw('diagnose', original), await raw('diagnose', second)];
        initialReady = samples.every(sample => sample.debugger_attached &&
          !sample.debug.input_pending && sample.debug.pending_captures === 0 &&
          sample.debug.active_capture_streams === 0 &&
          Object.values(sample.debug.commands).every(command => command.pending === 0));
        if (initialReady) break;
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      assert.equal(initialReady, true, 'initial test tabs must finish debugger setup');
      console.log('[focus setup] initial tabs attached with no pending commands; screenshots remain cold');
      const originalActive = await tabOracle.evaluate(() => chrome.tabs.query({active: true}));
      cover = spawn(python, [join(here, 'focus_mac_fixture.py'), String(browserPID)], {stdio: ['pipe', 'pipe', 'pipe']});
      cover.stderr.on('data', data => { coverError += data; });
      const waitReply = () => new Promise((resolve, reject) => {
        const request = {resolve: value => { clearTimeout(timer); resolve(value); },
          reject: error => { clearTimeout(timer); reject(error); }};
        const timer = setTimeout(() => {
          const index = pending.indexOf(request);
          if (index !== -1) pending.splice(index, 1);
          reject(new Error('Focus fixture response timed out: ' + coverError));
        }, 10000);
        pending.push(request);
      });
      const ready = waitReply();
      createInterface({input: cover.stdout}).on('line', line => {
        const request = pending.shift();
        if (request) { try { request.resolve(JSON.parse(line)); } catch (e) { request.reject(e); } }
      });
      cover.on('error', error => { for (const p of pending.splice(0)) p.reject(error); });
      cover.on('exit', code => { for (const p of pending.splice(0)) p.reject(new Error(`Focus fixture exited (${code}): ${coverError}`)); });
      const rpc = command => {
        if (cover.exitCode !== null || cover.killed || cover.stdin.destroyed)
          throw new Error('Focus fixture is not running: ' + coverError);
        const response = waitReply();
        cover.stdin.write(command + '\n');
        return response;
      };
      await ready;
      for (let i = 0; i < 100; i++) {
        const {state} = await rpc('state');
        if (state.frontmost_pid === state.fixture_pid && state.window_order[0]?.[0] === state.fixture_pid) break;
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      const check = async (label, work) => {
        console.log('[focus check] ' + label);
        const before = (await rpc('mark')).state;
        assert.equal(before.frontmost_pid, before.fixture_pid, 'owned cover app must be foreground');
        assert.equal(before.window_order[0]?.[0], before.fixture_pid, 'owned cover window must be topmost');
        const result = await work();
        await new Promise(resolve => setTimeout(resolve, 300));
        const after = await rpc('state');
        assert.deepEqual(after.state, before, `${label} changed foreground application or window order`);
        assert.deepEqual(after.changes, [], `${label} transiently changed foreground application or window order`);
        return result;
      };
      await check('owned cover idle baseline without browser requests',
        () => new Promise(resolve => setTimeout(resolve, 1000)));
      await check('read-only tab state oracle', () => tabOracle.evaluate(() => chrome.tabs.query({active: true})));
      if (process.env.SAYGO_TEST_FOCUS_DIAGNOSTICS === '1') {
        const failures = [];
        for (const [label, work] of [
          ['diagnostic CLI pages', () => cli('pages')],
          ['diagnostic raw select inactive page', () => raw('select', second)],
          ['diagnostic CLI screenshot original active page', () => cli('screenshot', '--out', join(root, 'diagnostic-original.png'))],
          ['diagnostic raw screenshot inactive page', () => raw('screenshot', second)]
        ]) {
          try { await check(label, work); console.log('[focus diagnostic] ' + label + ': passed'); }
          catch (error) { failures.push({label, error}); console.log('[focus diagnostic] ' + label + ': ' + error.message); }
          await rpc('front');
          await new Promise(resolve => setTimeout(resolve, 400));
        }
        if (failures.length) throw new AggregateError(failures.map(row => row.error),
          'Focus diagnostic failures: ' + failures.map(row => row.label).join(', '));
      }
      for (const [label, id] of [['select inactive page', second], ['reselect same page', second], ['select original page', original]]) {
        const data = await check(label, () => cli('select-page', id));
        assert.equal(data.selected_page_id, id);
        assert.deepEqual((await tabOracle.evaluate(() => chrome.tabs.query({active: true}))).map(t => t.id), originalActive.map(t => t.id));
      }
      const created = await check('new-page', () => cli('new-page', url + '/created'));
      assert.equal(created.selected_page_id, original);
      const createdTab = Number(created.created_page_id.split(':').at(-1));
      assert.equal((await tabOracle.evaluate(id => chrome.tabs.get(id), createdTab)).active, false);
      await check('select created page', () => cli('select-page', created.created_page_id));
      const screenshot = process.env.SAYGO_TEST_FOCUS_SCREENSHOT || join(root, 'after-input.png');
      const shot = await check('background screenshot', () => cli('screenshot', '--out', screenshot));
      await check('background tap', () => cli('tap', '60', '100', '--observation-id', shot.observation_id, '--request-id', 'focus-tap'));
      const focused = await check('focused input screenshot', () => cli('screenshot', '--out', screenshot));
      await check('background input', () => cli('input', 'Background input verified', '--observation-id', focused.observation_id, '--request-id', 'focus-input'));
      const after = await check('result screenshot', () => cli('screenshot', '--out', screenshot));
      assert.equal(after.page_id, created.created_page_id);
      await run(python, ['-c', `from PIL import Image
import sys
with Image.open(sys.argv[1]) as im:
    assert im.format == 'PNG' and im.width > 100 and im.height > 100
    assert im.convert('RGB').getpixel((im.width - 10, 10)) == (221, 238, 255)
with Image.open(sys.argv[1]) as im:
    im.verify()`, screenshot], {cwd: root, env});
      // The owned fixture's link has a fixed visual position. Input goes
      // through CLI coordinates; the page list is only the result oracle.
      const linkShot = await check('before target blank link screenshot', () => cli('screenshot', '--out', screenshot));
      if (process.env.SAYGO_TEST_FOCUS_LEFT_CLICK === '1') {
        await check('ordinary left-click foregrounding reproduction', () => cli('tap', '60', '180',
          '--observation-id', linkShot.observation_id, '--request-id', 'focus-left-click'));
        assert.fail('Ordinary left-click did not reproduce foregrounding; reproduction mode is not background-link acceptance');
      }
      const openedLink = await check('open webpage link URL in background', () => cli('act', JSON.stringify({
        type: 'open_link_background', x: 60, y: 180, coordinate_space: 'screen'
      }), '--observation-id', linkShot.observation_id, '--request-id', 'focus-background-link'));
      const popupState = await check('discover webpage popup', () => cli('pages'));
      assert.equal(popupState.selected_page_id, created.created_page_id, 'webpage popup must not replace the selected target');
      const popupPageId = popupState.pages.find(p => p.url === url + '/popup')?.page_id;
      assert.ok(popupPageId, 'webpage popup must be discoverable');
      assert.equal(openedLink.created_page_id, popupPageId, 'action must return the newly discovered page ID');
      assert.equal((await tabOracle.evaluate(id => chrome.tabs.get(id), Number(popupPageId.split(':').at(-1)))).active, false);
      await check('select background-opened popup', () => cli('select-page', popupPageId));
      const popupResultScreenshot = screenshot.replace(/\.png$/i, '') + '-webpage-popup.png';
      const popupShot = await check('background popup screenshot', () => cli('screenshot', '--out', popupResultScreenshot));
      assert.equal(popupShot.page_id, popupPageId);
      await check('background popup tap', () => cli('tap', '60', '100',
        '--observation-id', popupShot.observation_id, '--request-id', 'focus-popup-tap'));
      const popupFocused = await check('background popup input screenshot', () => cli('screenshot', '--out', popupResultScreenshot));
      await check('background popup input', () => cli('input', 'Popup input verified',
        '--observation-id', popupFocused.observation_id, '--request-id', 'focus-popup-input'));
      await check('background popup result screenshot', () => cli('screenshot', '--out', popupResultScreenshot));
      await run(python, ['-c', `from PIL import Image
import sys
with Image.open(sys.argv[1]) as im:
    assert im.format == 'PNG' and im.width > 100 and im.height > 100
    assert im.convert('RGB').getpixel((im.width - 10, 10)) == (204, 255, 221)
with Image.open(sys.argv[1]) as im:
    im.verify()`, popupResultScreenshot], {cwd: root, env});
      const beforeRejected = await check('page list before non-link rejection', () => cli('pages'));
      const nonLinkShot = await check('before non-link screenshot', () => cli('screenshot', '--out', popupResultScreenshot));
      const rejectedLink = await check('reject button without a hyperlink', () => cliError('act', JSON.stringify({
        type: 'open_link_background', x: 60, y: 250, coordinate_space: 'screen'
      }), '--observation-id', nonLinkShot.observation_id, '--request-id', 'focus-non-link'));
      assert.match(rejectedLink.error, /link|HTTP|URL/i, 'non-link rejection must explain the unsupported target');
      const afterRejected = await check('page list after non-link rejection', () => cli('pages'));
      assert.equal(afterRejected.selected_page_id, beforeRejected.selected_page_id);
      assert.deepEqual(afterRejected.pages.map(page => page.page_id).sort(), beforeRejected.pages.map(page => page.page_id).sort(),
        'rejecting a non-link must not open any page');
      // Page-level CDP/DOM oracles run only after every foreground assertion.
      const createdPage = context.pages().find(p => p.url() === url + '/created');
      assert.ok(createdPage, 'created fixture page must be discoverable');
      assert.equal(await createdPage.locator('input').inputValue(), 'Background input verified');
      assert.equal(await createdPage.evaluate(() => window.fixtureLinkClicks || 0), 0, 'background URL opening must not run click handlers');
      const popupPage = context.pages().find(p => p.url() === url + '/popup');
      assert.ok(popupPage, 'background-opened popup must remain available');
      assert.equal(await popupPage.locator('input').inputValue(), 'Popup input verified');
      console.log(JSON.stringify({browser_version: context.browser().version(), extension_version: manifest.version,
        selection: 'passed', creation: 'passed', screenshot: 'passed', input: 'passed',
        background_link: 'passed', popup_input: 'passed', non_link_rejection: 'passed', screenshot_path: screenshot,
        extension_popup_screenshot: popupScreenshot, webpage_popup_screenshot: popupResultScreenshot}));
    } finally {
      if (cover && cover.exitCode === null) {
        cover.stdin.end('quit\n');
        await new Promise(resolve => { cover.once('exit', resolve); setTimeout(() => { if (cover.exitCode === null) cover.kill(); resolve(); }, 3000).unref(); });
      }
      if (context) await context.close();
      await new Promise(resolve => server.close(resolve));
      await rm(root, {recursive: true, force: true});
    }
  });
