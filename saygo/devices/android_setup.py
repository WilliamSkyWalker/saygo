"""Shared Android prerequisite diagnostics and host-specific repair guidance."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

from .dependency_commands import format_command, mobile_python_check


def toolchain_commands(host):
    prefix = ['saygo'] if getattr(sys, 'frozen', False) else [sys.executable, '-m', 'saygo.cli']
    install = [*prefix, 'device', 'install', '--platform', 'android', '--host', host, '--tools-only']
    return [dict(argv=argv, **format_command(argv), run_on='client', label=label)
            for argv, label in [(install + ['--dry-run'], 'Preview Android host toolchain installation'),
                                (install, 'Install Android host tools after reviewing SDK licenses')]]


def local_checks():
    from . import mobile, toolchain
    from .android_host_checks import inspect_host
    from saygo.platforms.appium_server import find_appium_binary
    paths = toolchain.sandbox_paths()
    appium = find_appium_binary()
    managed = bool(appium and paths.get('appium_bin') and
                   os.path.realpath(appium) == os.path.realpath(paths['appium_bin']))
    return inspect_host(dict(sdk_root=str(mobile.sdk_root()), runtime=str(mobile.home()),
                             appium=appium, node=paths.get('node_bin') if managed else None,
                             appium_home=paths.get('appium_home') if managed else None,
                             managed_appium=managed))


def windows_checks():
    """Inspect the WSL Windows host without copying a worker or installing Python."""
    from . import mobile_host
    info = mobile_host.windows_info()
    python = Path(mobile_host.wsl_path(info['home'])) / 'python' / 'python.exe'
    if not python.is_file():
        return [dict(id='windows_host', status='missing', message='The private Windows Android host is not installed')]
    config = {'sdk_root': info['sdk_root'], 'runtime': info['home'].rstrip('\\/') + '\\runtime',
              'managed_only': True}
    source = Path(__file__).with_name('android_host_checks.py').read_text(encoding='utf-8')
    result = subprocess.run([str(python), '-c', source], input=json.dumps(config),
                            capture_output=True, text=True, encoding='utf-8', timeout=55)
    if result.returncode: raise RuntimeError(result.stderr[-1000:] or 'Windows prerequisite probe failed')
    checks = json.loads(result.stdout.lstrip('\ufeff'))
    if not isinstance(checks, list) or not all(isinstance(row, dict) and row.get('status') in {'ready', 'missing', 'unknown'} for row in checks):
        raise ValueError('Invalid Windows prerequisite probe response')
    return checks


def diagnose(host='auto', server_url=None):
    from . import mobile_host
    client = 'wsl' if mobile_host.is_wsl() else {'Darwin': 'macos', 'Windows': 'windows'}.get(platform.system(), 'linux')
    python = mobile_python_check()
    checks = [python]
    commands = list(python.get('commands', []))
    notes = list(python.get('notes', []))
    if getattr(sys, 'frozen', False):
        notes.append('Toolchain commands require a separately installed Saygo CLI; the packaged application executable is not a Python interpreter.')
    if server_url:
        selected = 'remote'
        notes.append('Only Python client dependencies are checked here. Java, Android SDK, Appium and its driver belong on the remote server.')
    else:
        selected = mobile_host.select_host(host, 'android')
        try:
            host_checks = windows_checks() if selected == 'windows' else local_checks()
        except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as exc:
            host_checks = [dict(id='android_host', status='unknown', message=str(exc))]
        checks.extend(host_checks)
        if any(row['status'] != 'ready' for row in host_checks): commands.extend(toolchain_commands(selected))
        if selected == 'windows':
            notes.append('Run the commands in WSL. Python client dependencies stay in WSL; Android tools are prepared on the Windows host. Do not run mcp init in WSL to repair Windows tools.')
        elif client == 'windows':
            notes.append('Run the commands in Windows PowerShell. This prepares the native Windows Android host; WSL is not required.')
        elif client == 'macos':
            notes.append('Run the commands in macOS Terminal. Android tools run locally on Intel or Apple Silicon Macs.')
        elif client == 'wsl':
            notes.append('This checks the local WSL Android host. Use --host windows to explicitly prepare the Windows host instead.')
        notes.append('Tools-only installation does not create a simulator. Connect and authorize a USB device separately; use device install without --tools-only for an emulator.')
    notes.append('These checks do not prove that a device is connected or controllable. Retry discovery and verify a screenshot after setup.')
    return dict(ok=all(row['status'] == 'ready' for row in checks), platform='android',
                client_os=client, host=selected, checks=checks, commands=commands,
                notes=notes, device_online=None)


class MobileSetupError(RuntimeError):
    def __init__(self, message, setup):
        self.setup = setup
        commands = '\n'.join(item['command'] for item in setup.get('commands', []))
        super().__init__(message + ('\n' + commands if commands else ''))


def python_dependency_error(cause):
    check = mobile_python_check(force=True)
    check = {**check, 'message': check['message'] + ' ' + str(cause), 'cause': str(cause)}
    return MobileSetupError('Mobile Python dependencies are missing or incomplete: ' + str(cause),
                            dict(ok=False, checks=[check], commands=check.get('commands', []),
                                 notes=check.get('notes', []), host='client'))


def error_payload(exc):
    result = dict(ok=False, error=str(exc), error_type=type(exc).__name__)
    if isinstance(getattr(exc, 'setup', None), dict): result['setup'] = exc.setup
    return result
