"""Resolve the browser OS's shared bridge, independent of the client runtime.

Only installation/default discovery uses this resolver. Saved page bindings are
never silently moved to another bridge or another tab.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

from .browser_bridge import Client, HOST, PROTOCOL


def _windows_info(browser):
    vendor = 'Google\\Chrome' if browser == 'chrome' else 'Microsoft\\Edge'
    key = rf'Software\{vendor}\NativeMessagingHosts\{HOST}'
    from saygo.devices.mobile_host import is_wsl
    if is_wsl():
        # All interpolated values are fixed constants, never user-supplied paths.
        script = ("[Console]::OutputEncoding=[Text.Encoding]::UTF8; "
                  "$manifest=$null; "
                  f"if (Test-Path 'HKCU:\\{key}') {{ $manifest=(Get-Item 'HKCU:\\{key}').GetValue('') }}; "
                  "@{home=$env:USERPROFILE;local=$env:LOCALAPPDATA;manifest=$manifest} | ConvertTo-Json -Compress")
        raw = subprocess.check_output(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script],
                                      text=True, encoding='utf-8', timeout=15)
        return json.loads(raw.lstrip('\ufeff'))
    manifest = None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as handle:
            manifest = winreg.QueryValueEx(handle, '')[0]
    except (ImportError, OSError):
        pass
    return {'home':str(Path.home()), 'local':os.environ.get('LOCALAPPDATA'), 'manifest':manifest}


def _layout(browser):
    from saygo.devices.mobile_host import is_wsl, wsl_path
    wsl = is_wsl()
    if wsl or sys.platform == 'win32':
        info = _windows_info(browser)
        if not info.get('local') or not info.get('home'):
            raise RuntimeError('Cannot determine the Windows browser user directories')
        path = lambda value: Path(wsl_path(value) if wsl else value).expanduser().resolve()
        home, local = path(info['home']), path(info['local'])
        default = local / 'Saygo/browser-bridge'
        legacy = home / '.saygo/browser-bridge'
        manifest = path(info['manifest']) if info.get('manifest') else None
    else:
        default = Path.home() / '.saygo/browser-bridge'
        legacy = default
        if sys.platform == 'darwin':
            config = Path.home() / 'Library/Application Support' / ('Google/Chrome' if browser == 'chrome' else 'Microsoft Edge')
        else:
            config = Path.home() / '.config' / ('google-chrome' if browser == 'chrome' else 'microsoft-edge')
        manifest = config / 'NativeMessagingHosts' / (HOST + '.json')
    return default.resolve(), legacy.resolve(), manifest


def _registered_directory(manifest, extension_id):
    if not manifest or not manifest.is_file():
        return None
    value = json.loads(manifest.read_text(encoding='utf-8'))
    if value.get('name') != HOST or value.get('type') != 'stdio':
        raise RuntimeError('Invalid Saygo native host registration: ' + str(manifest))
    from saygo.devices.mobile_host import is_wsl, wsl_path
    launcher = value['path']
    if is_wsl():
        launcher = wsl_path(launcher)
    launcher = Path(launcher).expanduser().resolve()
    if launcher.name not in {'host.cmd', 'host.sh'}:
        raise RuntimeError('Unrecognized native host launcher: ' + str(launcher))
    status = launcher.parent / 'status.json'
    if (extension_id and f'chrome-extension://{extension_id}/' not in value.get('allowed_origins', [])
            and status.is_file() and json.loads(status.read_text(encoding='utf-8')).get('connected')):
        raise RuntimeError('Connected native host belongs to another extension identity; release it manually before migration')
    return launcher.parent


def resolve_directory(directory=None, browser='chrome', extension_id=None):
    """Keep an existing live bridge; otherwise use its registered/default location.

    An explicit nonstandard directory is an intentional installation override.
    Old standard paths supplied by saved installers are migration hints, not
    permission to split a currently connected shared bridge.
    """
    if browser not in {'chrome', 'edge'}:
        raise ValueError('Unsupported browser')
    requested = Path(directory).expanduser().resolve() if directory else None
    if requested and requested.parts[-2:] not in {('.saygo', 'browser-bridge'), ('Saygo', 'browser-bridge')}:
        return requested
    default, legacy, manifest = _layout(browser)
    if requested and requested not in {default, legacy}:
        return requested
    registered = _registered_directory(manifest, extension_id)
    candidates = list(dict.fromkeys(p for p in (registered, default, legacy) if p))
    live = []
    for candidate in candidates:
        status = candidate / 'status.json'
        if not status.is_file():
            continue
        info = json.loads(status.read_text(encoding='utf-8'))
        if not info.get('connected'):
            continue
        # A second legacy folder can belong to an unpacked extension even when
        # the current registration has already been switched to the store ID.
        _registered_directory(candidate / (HOST + '.json'), extension_id)
        if info.get('protocol') != PROTOCOL:
            raise RuntimeError('Connected browser bridge protocol mismatch: ' + str(candidate))
        # A stale connected flag is not sufficient proof. A busy/unresponsive
        # host fails discovery rather than causing a second installation.
        Client(candidate, timeout=3).call('pages')
        live.append(candidate)
    if len(live) > 1:
        raise RuntimeError('Multiple browser bridges are connected; select one explicitly: ' + ', '.join(map(str, live)))
    return live[0] if live else (registered or requested or default)


def default_directory(state_root, browser='chrome'):
    """Use shared OS discovery even when a client's cached default is stale."""
    config = Path(state_root) / 'browser-bridge.json'
    directory = json.loads(config.read_text(encoding='utf-8')).get('directory') if config.is_file() else None
    return resolve_directory(directory, browser)


def registration_directory(browser='chrome', extension_id=None):
    """Expose registration separately: a running host can outlive its registration."""
    _, _, manifest = _layout(browser)
    return _registered_directory(manifest, extension_id)
