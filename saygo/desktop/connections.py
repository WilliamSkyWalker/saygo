"""Desktop onboarding using the shared connection service."""
from argparse import Namespace
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

from saygo.devices import control
from saygo.platforms import device_session as ds

COMPUTER = 'saygo-desktop-computer'
BROWSER = 'saygo-desktop-browser'


def arguments(kind, session, **options):
    values = dict(platform=kind, session=session, app=None, device=None, server_url=None,
                  team_id=None, background=False, process_name=None, launch=None,
                  new_window=False, new_window_args=[], backend='extension' if kind == 'browser' else None,
                  bridge_directory=None, page_id=None)
    values.update(options)
    return Namespace(**values)


def connect_computer():
    return control.connect(arguments('desktop', COMPUTER, desktop_scope='computer'))


def browser_status():
    """A bounded live probe; saved session files alone are not connection evidence."""
    config = ds.STATE_DIR.parent / 'browser-bridge.json'
    if not config.exists():
        return {'connected': False, 'message': '尚未连接 · 点击连接 Chrome 安装扩展'}
    try:
        from saygo.integrations.browser_bridge import Client
        directory = json.loads(config.read_text(encoding='utf-8'))['directory']
        pages = Client(directory, timeout=3).call('pages')
        return {'connected': True, 'pages': pages, 'directory': directory}
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        return {'connected': False, 'message': '等待扩展连接 · 在扩展中点击 Connect local bridge', 'detail': str(exc)}


def connect_browser(status):
    return control.connect(arguments('browser', BROWSER, bridge_directory=status['directory'], auto_page=True))


def open_chrome(url):
    if platform.system() == 'Windows':
        candidates = []
        import winreg
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                with winreg.OpenKey(hive, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe') as key:
                    candidates.append(winreg.QueryValue(key, None))
            except OSError:
                pass
        for name in ('LOCALAPPDATA', 'PROGRAMFILES', 'PROGRAMFILES(X86)'):
            if os.environ.get(name):
                candidates.append(str(Path(os.environ[name])/'Google/Chrome/Application/chrome.exe'))
        chrome = next((p for p in candidates if Path(p).is_file()), None)
        if not chrome:
            raise RuntimeError('未找到 Chrome，请先安装 Chrome，再点击连接 Chrome')
        subprocess.Popen([chrome, url])
    elif platform.system() == 'Darwin':
        subprocess.run(['open', '-a', 'Google Chrome', url], check=True, timeout=15)
    else:
        chrome = shutil.which('google-chrome') or shutil.which('chromium')
        if not chrome:
            raise RuntimeError('未找到 Chrome，请先安装 Chrome')
        subprocess.Popen([chrome, url])


def install_browser():
    from saygo.integrations.browser_setup import setup, STORE_EXTENSION_ID, STORE_EXTENSION_URL
    from saygo.integrations.browser_bridge import atomic_json
    result = setup(STORE_EXTENSION_ID)
    atomic_json(ds.STATE_DIR.parent/'browser-bridge.json', result)
    open_chrome(STORE_EXTENSION_URL)
    return '已打开 Chrome 插件页。安装 Saygo Browser 后，打开扩展点击 Connect local bridge；此处会自动更新。'
