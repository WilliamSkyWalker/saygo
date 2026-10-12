"""Install the stdlib native host on the browser OS, including Windows from WSL."""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
import shutil
import subprocess
import tempfile

from . import browser_bridge

STORE_EXTENSION_ID = "ehomcchjfomfkcmbeinlcmpbaamdhfbo"
STORE_EXTENSION_URL = "https://chromewebstore.google.com/detail/" + STORE_EXTENSION_ID


def setup(extension_id, browser='chrome', directory=None):
    if not re.fullmatch('[a-p]{32}', extension_id):
        raise ValueError('Expected a 32-letter Chrome extension ID')
    from .browser_location import resolve_directory
    directory = resolve_directory(directory, browser, extension_id)
    from saygo.devices import mobile_host, mobile
    if not mobile_host.is_wsl():
        value = browser_bridge.install(directory, extension_id, browser)
        command = ([sys.executable, '--native-host-uninstall'] if getattr(sys, 'frozen', False) else
                   [sys.executable, '-I', '-m', 'saygo.integrations.browser_bridge', 'uninstall'])
        return {**value, 'host':'local', 'uninstall_command': command +
                ['--directory', value['directory'], '--browser', browser]}
    root = Path(directory).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    python = root / 'runtime/python/python.exe'
    if not python.is_file():
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            archive = Path(tmp)/'python.zip'
            mobile.download(mobile_host.PYTHON_URL, archive, mobile_host.PYTHON_SHA256)
            mobile.unpack(archive, Path(tmp)/'python')
            if python.parent.exists():
                raise RuntimeError('Incomplete private Windows Python; inspect ' + str(python.parent))
            python.parent.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(Path(tmp)/'python'), python.parent)
    content = Path(browser_bridge.__file__).read_bytes()
    script = root / 'runtime' / hashlib.sha256(content).hexdigest()[:16] / 'browser_bridge.py'
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_bytes(content)
    win_script = mobile_host.wsl_path(script, windows=True)
    win_directory = mobile_host.wsl_path(root, windows=True)
    command = [str(python), win_script, 'install', '--directory', win_directory,
               '--extension-id', extension_id, '--browser', browser]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=30, check=True)
    value = json.loads(result.stdout)
    return {**value, 'host':'windows', 'directory':str(root),
            'uninstall_command':[str(python), win_script, 'uninstall', '--directory', win_directory, '--browser',browser]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extension-id', required=True)
    parser.add_argument('--browser', choices=['chrome','edge'], default='chrome')
    parser.add_argument('--directory')
    parser.add_argument('--save-default', action='store_true')
    parser.add_argument('--resolve-only', action='store_true', help='Read the shared bridge location without installing')
    args = parser.parse_args()
    if args.resolve_only:
        from .browser_location import resolve_directory, registration_directory
        selected = resolve_directory(args.directory, args.browser, args.extension_id)
        registered = registration_directory(args.browser, args.extension_id)
        print(json.dumps({'directory':str(selected), 'registered_directory':str(registered) if registered else None}))
        return
    value = setup(args.extension_id, args.browser, args.directory)
    if args.save_default:
        root = Path(os.environ.get('SAYGO_HOME_DIR', Path.home()/'.saygo'))
        root.mkdir(parents=True, exist_ok=True)
        browser_bridge.atomic_json(root/'browser-bridge.json', value)
    print(json.dumps(value))


if __name__ == '__main__':
    main()
