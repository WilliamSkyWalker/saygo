"""Opt-in browser restart checks with a real extension and isolated native host."""
from contextlib import ExitStack
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from PIL import Image

from saygo.integrations.browser_bridge import install


class StartupFixture(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'''<!doctype html><meta charset="utf-8"><title>Startup fixture</title>
        <style>body{margin:0}input{width:240px;height:50px}</style><input>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@unittest.skipUnless(os.environ.get('SAYGO_TEST_CHROME'),
                     'set SAYGO_TEST_CHROME for real extension restart integration')
class ExtensionStartupLive(unittest.TestCase):
    def setUp(self):
        if sys.platform != 'linux' or os.environ.get('SAYGO_TEST_HEADED') != '1' or not os.environ.get('DISPLAY'):
            self.skipTest('persistent extension installation requires headed Linux with DISPLAY (use xvfb-run)')
        if not shutil.which('xdotool'):
            self.skipTest('persistent extension installation requires xdotool for the native directory picker')

    def install_extension(self, context, page, extension):
        # --load-extension and Extensions.loadUnpacked are temporary installs:
        # they do not exercise the installed profile's real onStartup event.
        page.goto('chrome://extensions/')
        page.locator('#devMode').click()
        page.locator('#loadUnpacked').click()

        def xdo(*args):
            return subprocess.run(['xdotool', *map(str, args)], check=True,
                                  capture_output=True, text=True, timeout=10).stdout

        cdp = context.browser.new_browser_cdp_session()
        try:
            pid = next(process['id'] for process in cdp.send('SystemInfo.getProcessInfo')['processInfo']
                       if process['type'] == 'browser')
        finally:
            cdp.detach()
        dialog = xdo('search', '--sync', '--all', '--onlyvisible', '--pid', pid,
                     '--name', '^Select the extension directory[.]$').splitlines()[-1]
        xdo('windowmove', dialog, 100, 100)
        xdo('windowfocus', '--sync', dialog)
        xdo('key', '--clearmodifiers', 'ctrl+l')
        xdo('type', '--clearmodifiers', '--delay', 1, extension)
        page.wait_for_timeout(300)
        geometry = dict(line.split('=', 1) for line in xdo('getwindowgeometry', '--shell', dialog).splitlines())
        # Click the native GTK Open button; Return can choose a default child
        # directory instead of submitting the complete typed extension path.
        xdo('mousemove', '--window', dialog, int(geometry['WIDTH']) - 50,
            int(geometry['HEIGHT']) - 24, 'click', 1)

    def status(self, ui):
        return ui.evaluate("() => chrome.runtime.sendMessage({type:'status'})")

    def wait_connected(self, ui):
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            status = self.status(ui)
            if status.get('connected'):
                return status
            ui.wait_for_timeout(100)
        self.fail('Expected an automatically restored native connection: ' + json.dumps(status))

    def assert_stays_disconnected(self, ui):
        # Observe through the startup window rather than trusting the first reply.
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            status = self.status(ui)
            self.assertFalse(status.get('connected'), status)
            self.assertEqual(status.get('pages'), [], status)
            ui.wait_for_timeout(100)

    def test_connect_restart_stale_selection_and_release(self):
        from playwright.sync_api import sync_playwright

        with tempfile.TemporaryDirectory() as tmp, ExitStack() as cleanup, sync_playwright() as pw:
            root = Path(tmp)
            bridge = root / 'bridge'
            profile = root / 'profile'
            server = ThreadingHTTPServer(('127.0.0.1', 0), StartupFixture)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            cleanup.callback(server.server_close)
            cleanup.callback(server.shutdown)
            url = f'http://127.0.0.1:{server.server_port}/startup'
            source = Path(os.environ.get('SAYGO_TEST_EXTENSION', 'extensions/saygo-browser')).resolve()
            extension = root / 'extension'
            shutil.copytree(source, extension)
            browser_env = {**os.environ, 'HOME': tmp, 'XDG_CONFIG_HOME': str(root / '.config'),
                           'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
            cli_env = {**os.environ, 'SAYGO_HOME_DIR': str(root / 'saygo-home'),
                       'SAYGO_RUNTIME_DIR': str(root / 'runtime')}
            command = [sys.executable, '-m', 'saygo.cli', 'device']

            def cli(*args, ok=True):
                result = subprocess.run(command + list(args) + ['--session', 'startup-web'],
                                        env=cli_env, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0 if ok else 2, result.stdout + result.stderr)
                data = json.loads(result.stdout)
                if not ok:
                    self.assertFalse(data['ok'], data)
                return data

            def observe(name):
                output = root / (name + '.png')
                data = cli('screenshot', '--out', str(output))
                with Image.open(output) as image:
                    self.assertGreater(image.width, 0)
                    self.assertGreater(image.height, 0)
                    image.verify()
                artifact = os.environ.get('SAYGO_TEST_STARTUP_SCREENSHOT')
                if name == 'after-restart-after' and artifact:
                    Path(artifact).write_bytes(output.read_bytes())
                return data['observation_id']

            def input_fixture(page, phase):
                observation = observe(phase + '-before')
                tapped = cli('tap', '30', '25', '--observation-id', observation,
                             '--request-id', phase + '-focus')
                self.assertTrue(tapped['dispatched'], tapped)
                observation = observe(phase + '-focused')
                text = phase + ' 中文 input'
                typed = cli('input', text, '--observation-id', observation,
                            '--request-id', phase + '-input')
                self.assertTrue(typed['dispatched'], typed)
                observe(phase + '-after')
                # DOM is only the owned fixture's test oracle; input uses CLI/IPC.
                self.assertEqual(page.locator('input').input_value(), text)

            def launch(first_install=False):
                context = pw.chromium.launch_persistent_context(
                    str(profile), executable_path=os.environ['SAYGO_TEST_CHROME'],
                    headless=False, no_viewport=True, env=browser_env,
                    ignore_default_args=['--disable-extensions'],
                    args=['--no-sandbox', '--lang=en-US'])
                try:
                    if first_install:
                        self.install_extension(context, context.pages[0], extension)
                    worker = (context.service_workers[0] if context.service_workers else
                              context.wait_for_event('serviceworker', timeout=10000))
                    extension_id = worker.url.split('/')[2]
                    page = context.pages[0]
                    page.goto(url)
                    ui = context.new_page()
                    ui.goto(f'chrome-extension://{extension_id}/popup.html')
                    page.bring_to_front()
                    return context, page, ui, extension_id
                except Exception:
                    context.close()
                    raise

            context, page, ui, extension_id = launch(first_install=True)
            try:
                print(f'Real Chrome version: {context.browser.version}', flush=True)
                with patch('pathlib.Path.home', return_value=root):
                    install(bridge, extension_id, 'chrome')
                manifest = root / '.config/google-chrome/NativeMessagingHosts/com.saygo.browser.json'
                for directory in (root / '.config/chromium', root / '.config/google-chrome-for-testing', profile):
                    destination = directory / 'NativeMessagingHosts/com.saygo.browser.json'
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(manifest.read_bytes())
                self.assert_stays_disconnected(ui)
                page.evaluate("localStorage.setItem('startup-marker','preserved')")
                ui.locator('#connect').click()
                self.wait_connected(ui)
                page.bring_to_front()
                cli('connect', '--platform', 'browser', '--backend', 'extension',
                    '--bridge-directory', str(bridge))
                pages = cli('pages')['pages']
                self.assertEqual(len(pages), 1, pages)
                original = pages[0]['page_id']
                input_fixture(page, 'before-restart')

                # Close the actual browser process, then reuse only its disk profile.
                context.close()
                context = None
                context, page, ui, restarted_id = launch()
                self.assertEqual(restarted_id, extension_id)
                self.assertEqual(page.evaluate("localStorage.getItem('startup-marker')"), 'preserved')
                self.wait_connected(ui)  # No Connect click after the browser restart.
                self.assertEqual(page.locator('input').input_value(), '',
                                 'Browser restart must not replay earlier input')
                pages = cli('pages')['pages']
                current = next(item['page_id'] for item in pages if item['url'] == url)
                self.assertNotEqual(current, original)
                missing_output = root / 'stale.png'
                failed = cli('screenshot', '--out', str(missing_output), ok=False)
                self.assertEqual(failed['error_type'], 'PageSelectionError', failed)
                self.assertFalse(missing_output.exists())
                saved = json.loads((root / 'saygo-home/device-sessions/startup-web.json').read_text())
                self.assertEqual(saved['page_id'], original)
                chosen = cli('select-page', current)
                self.assertEqual(chosen['selected_page_id'], current)
                page.bring_to_front()
                input_fixture(page, 'after-restart')

                ui.locator('#release').click()
                self.assert_stays_disconnected(ui)
                self.assertIs(self.status(ui).get('reconnect_on_startup'), False)
                self.assertFalse(page.is_closed())
                context.close()
                context = None
                context, page, ui, _ = launch()
                self.assert_stays_disconnected(ui)
                self.assertIs(self.status(ui).get('reconnect_on_startup'), False)
                self.assertEqual(page.evaluate("localStorage.getItem('startup-marker')"), 'preserved')
            finally:
                if context is not None:
                    context.close()
