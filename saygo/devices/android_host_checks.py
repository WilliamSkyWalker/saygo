"""Read-only Android host probes, also runnable by the stdlib Windows host Python.

No downloads, adb server startup, Appium server startup, or device connections.
The WSL client sends paths as JSON, never as interpolated executable source.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def _run(argv, env):
    options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
    return subprocess.run(argv, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=15, **options)


def inspect_host(config):
    root = Path(config['sdk_root'])
    runtime = Path(config['runtime'])
    suffix = '.exe' if os.name == 'nt' else ''
    env = os.environ.copy()
    env.update(ANDROID_HOME=str(root), ANDROID_SDK_ROOT=str(root))
    private_java = runtime / 'jdk' / 'bin' / ('java' + suffix)
    if private_java.is_file(): env['JAVA_HOME'] = str(private_java.parent.parent)
    paths = [str(root / 'platform-tools')]
    if env.get('JAVA_HOME'): paths.append(str(Path(env['JAVA_HOME']) / 'bin'))
    env['PATH'] = os.pathsep.join(paths + [env.get('PATH', '')])
    checks = []

    def record(name, status, message):
        checks.append(dict(id=name, status=status, message=message))

    def file_check(name, candidates, message):
        found = next((p for p in candidates if p.is_file()), None)
        record(name, 'ready' if found else 'missing', str(found) if found else message)

    file_check('adb', [root / 'platform-tools' / ('adb' + suffix),
                      runtime / 'platform-tools' / ('adb' + suffix)], 'Android SDK platform-tools are missing')
    file_check('android_platform', root.glob('platforms/*/android.jar'), 'Android SDK platform is missing')
    file_check('android_build_tools', root.glob('build-tools/*/aapt' + suffix), 'Android SDK build-tools are missing')
    file_check('sdk_manager', root.glob('cmdline-tools/*/bin/sdkmanager' + ('.bat' if os.name == 'nt' else '')),
               'Android SDK command-line tools are missing')
    managed_only = bool(config.get('managed_only'))
    private_appium = runtime / 'node_modules' / 'appium' / 'build' / 'lib' / 'main.js'
    appium = None if managed_only else config.get('appium')
    if not appium and private_appium.is_file(): appium = str(private_appium)
    if not appium and not managed_only: appium = shutil.which('appium')
    managed_appium = (managed_only or config.get('managed_appium') or
                      (appium and os.path.realpath(appium) == os.path.realpath(private_appium)))
    if appium:
        # Match AppiumServerManager: an external Appium's bin directory chooses
        # its Node before an unrelated Node on PATH or in the private runtime.
        env['PATH'] = str(Path(appium).parent) + os.pathsep + env['PATH']
    java = config.get('java') or shutil.which('java' + suffix, path=env['PATH'])
    node = None if managed_only else config.get('node')
    if not node and (managed_appium or not appium):
        private_node = runtime / 'node' / ('node.exe' if os.name == 'nt' else 'bin/node')
        marker = runtime / 'node_path.txt'
        node = str(private_node) if private_node.is_file() else None
        if not node and marker.is_file():
            candidate = marker.read_text().strip()
            if candidate and Path(candidate).is_file(): node = candidate
    if not node and appium and not managed_appium:
        adjacent_node = Path(appium).parent / ('node' + suffix)
        if adjacent_node.is_file(): node = str(adjacent_node)
    if not node and not managed_only:
        node = shutil.which('node' + suffix, path=env['PATH'])
    for name, binary, flag in [('java', java, '-version'), ('node', node, '--version')]:
        if not binary:
            record(name, 'missing', 'Java 17+ is required' if name == 'java' else 'Appium-compatible Node is required')
            continue
        try:
            response = _run([binary, flag], env=env)
            output = response.stdout + response.stderr
            match = re.search(r'version "(\d+)', output) if name == 'java' else re.search(r'v(\d+)\.(\d+)\.(\d+)', output)
            if response.returncode or not match:
                record(name, 'unknown', f'Cannot determine {name} version: {output[-500:]}')
                continue
            version = tuple(map(int, match.groups()))
            valid = version[0] >= 17 if name == 'java' else (
                (version[0] == 20 and version[1] >= 19) or (version[0] == 22 and version[1] >= 12) or version[0] >= 24)
            record(name, 'ready' if valid else 'missing', f'{binary}: {match[0]}')
        except (OSError, subprocess.SubprocessError) as exc:
            record(name, 'unknown', str(exc))
    if not appium:
        record('appium', 'missing', 'Appium is missing on the Android host')
        record('uiautomator2', 'unknown', 'Appium is required to query its installed drivers')
        return checks
    record('appium', 'ready', appium)
    if managed_only and not node:
        record('uiautomator2', 'unknown', 'The private Windows host requires an existing private or recorded Node')
        return checks
    if node: env['PATH'] = str(Path(node).parent) + os.pathsep + env['PATH']
    if managed_only: env['APPIUM_HOME'] = str(runtime / 'appium_home')
    elif config.get('appium_home'): env['APPIUM_HOME'] = config['appium_home']
    elif managed_appium: env['APPIUM_HOME'] = str(runtime / 'appium_home')
    argv = [*([node or 'node'] if appium.endswith('.js') else []), appium,
            'driver', 'list', '--installed', '--json']
    # npm's .cmd entry point needs cmd.exe on Windows. Prefer its JS entry point
    # to avoid shell interpolation of paths containing special characters.
    if os.name == 'nt' and appium.lower().endswith(('.cmd', '.bat')):
        js = Path(appium).parent / 'node_modules/appium/build/lib/main.js'
        if not js.is_file():
            record('uiautomator2', 'unknown', 'Cannot inspect this Appium wrapper; use the Saygo toolchain installer')
            return checks
        argv = [node or 'node', str(js), *argv[1:]]
    try:
        response = _run(argv, env=env)
        if response.returncode: raise ValueError(response.stderr[-500:] or 'Appium driver query failed')
        drivers = json.loads(response.stdout)
        if not isinstance(drivers, dict): raise ValueError('Invalid Appium driver list')
        record('uiautomator2', 'ready' if 'uiautomator2' in drivers else 'missing',
               'Appium UiAutomator2 driver is installed' if 'uiautomator2' in drivers else 'Appium UiAutomator2 driver is missing')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        record('uiautomator2', 'unknown', str(exc))
    return checks


if __name__ == '__main__':
    print(json.dumps(inspect_host(json.load(sys.stdin))))
