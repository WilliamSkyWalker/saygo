"""Managed runtime update checks and launcher (stdlib only).

Copied into the installation root so cached client configurations keep following
one runtime pointer. Updates are opt-in and never replace an executing runtime.
"""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

REPOSITORY = 'WilliamSkyWalker/saygo'
API = 'https://api.github.com/repos/' + REPOSITORY + '/releases?per_page=100'
PACKAGE_API = 'https://pypi.org/pypi/saygo-agent-control/json'
DOWNLOAD = 'https://github.com/' + REPOSITORY + '/releases/download/'
INTERVAL = 86400
_CHECK_THREADS = {}
_CHECK_THREADS_LOCK = threading.Lock()


def read(path, default=None):
    return json.loads(Path(path).read_text()) if Path(path).is_file() else (default or {})


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.update-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, ensure_ascii=True, indent=2)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextlib.contextmanager
def lock(path, blocking=False):
    """Nonblocking OS lock; crashes release it on both Windows and POSIX."""
    with Path(path).open('a+b') as stream:
        if os.name == 'nt':
            import msvcrt
            stream.write(b'0'); stream.flush(); stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def version(value):
    if not re.fullmatch(r'v?\d+\.\d+\.\d+', value):
        raise ValueError('Unsupported release version')
    return tuple(map(int, value.removeprefix('v').split('.')))


def fetch(url, timeout=5):
    request = urllib.request.Request(url, headers={'User-Agent': 'Saygo-Updater', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def current(root):
    installed = read(root/'installation.json')
    if installed.get('runtime_mode') == 'package':
        number = subprocess.check_output(
            [installed['python'], '-I', '-c',
             'from importlib.metadata import version; print(version("saygo-agent-control"))'],
            text=True, timeout=10).strip()
        return {**installed, 'version': number}
    selected = read(root/'active-runtime.json')
    if selected and Path(selected.get('python', '')).is_file():
        return {**installed, **selected}
    return installed


def update_data(path):
    """Disposable update metadata must never prevent using a working device."""
    try:
        value = read(path)
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def fresh(state, installed):
    checked = state.get('checked_at')
    return (isinstance(checked, (int, float)) and not isinstance(checked, bool)
            and 0 <= time.time() - checked < INTERVAL
            and state.get('current') == installed.get('version'))


def check(root, force=False):
    root = Path(root)
    with lock(root/'check.lock', blocking=True):
        return _check(root, force)


def _check(root, force):
    config = update_data(root/'updates.json')
    state = update_data(root/'update-state.json')
    installed = current(root)
    if not force and fresh(state, installed):
        return state
    package = installed.get('runtime_mode') == 'package'
    channel = 'stable' if package else config.get('channel', 'stable')
    try:
        if package:
            # pipx upgrades from the package index, not from GitHub release assets.
            published = json.loads(fetch(PACKAGE_API))['releases']
            releases = [{'tag_name': 'v'+number} for number, files in published.items()
                        if re.fullmatch(r'\d+\.\d+\.\d+', number)
                        and any(not entry.get('yanked', False) for entry in files)]
        else:
            releases = json.loads(fetch(API))
        candidates = []
        for release in releases:
            tag = release.get('tag_name', '')
            if release.get('draft') or (release.get('prerelease') and channel != 'beta'):
                continue
            if re.fullmatch(r'v\d+\.\d+\.\d+', tag) and version(tag) > version(installed['version']):
                candidates.append(release)
        latest = max(candidates, key=lambda item: version(item['tag_name'])) if candidates else None
        state = {'checked_at': time.time(), 'current': installed['version'], 'channel': channel,
                 'available': bool(latest), 'release': latest, 'error': None}
    except Exception as exc:
        state = {**state, 'current': installed['version'], 'checked_at': time.time(),
                 'error': 'Update check failed: ' + str(exc)}
    write(root/'update-state.json', state)
    return state


def _background_check(root, force):
    try:
        check(root, force=force)
        info = notice(root, refresh=False)
        if info.get('available') or info.get('error'):
            print('[Saygo update] '+json.dumps(info), file=sys.stderr)
    except Exception as exc:
        # A read-only filesystem, broken cache, or index outage is not an MCP failure.
        print('[Saygo update] Update check failed: '+str(exc), file=sys.stderr)
    finally:
        with _CHECK_THREADS_LOCK:
            _CHECK_THREADS.pop(str(root), None)


def start_check(root, force=False):
    """Coalesce tool calls in this process; check.lock serializes cache writers."""
    root = Path(root).resolve()
    key = str(root)
    with _CHECK_THREADS_LOCK:
        if key not in _CHECK_THREADS:
            worker = threading.Thread(target=_background_check, args=(root, force),
                                      daemon=True, name='saygo-update-check')
            _CHECK_THREADS[key] = worker
            try:
                worker.start()
            except Exception:
                _CHECK_THREADS.pop(key, None)
                raise
    return True


def notice(root, refresh=True):
    root = Path(root)
    try:
        installed = current(root)
    except Exception as exc:
        return {'automatic': False, 'error': 'Cannot read installed version: '+str(exc)}
    package = installed.get('runtime_mode') == 'package'
    state = update_data(root/'update-state.json')
    config = update_data(root/'updates.json')
    result = {'current': installed.get('version'),
              'automatic': False if package else config.get('automatic', False),
              'channel': 'stable' if package else config.get('channel', 'stable')}
    if package:
        result.update(runtime_mode='package',
                      message='Upgrade with pipx upgrade saygo-agent-control; restart the Agent client to load it.')
    if state.get('checked_at'):
        result['checked_at'] = state['checked_at']
    release = state.get('release')
    tag = release.get('tag_name', '') if isinstance(release, dict) else ''
    try:
        available = state.get('available') and version(tag) > version(installed['version'])
    except (TypeError, ValueError, KeyError):
        available = False
    if available:
        result.update(available=tag,
                      url=('https://pypi.org/project/saygo-agent-control/'+tag.removeprefix('v')+'/'
                           if package else 'https://github.com/'+REPOSITORY+'/releases/tag/'+tag),
                      message=('Saygo '+tag+' is available. Run pipx upgrade saygo-agent-control; restart the Agent client to load it.'
                               if package else 'Saygo '+tag+' is available. Run saygo update --apply, or enable saygo update --auto on.'))
    if state.get('error'): result['error'] = state['error']
    if state.get('deferred') and not package: result['deferred'] = state['deferred']
    if refresh and not fresh(state, installed):
        try:
            result['checking'] = start_check(root)
        except Exception as exc:
            result['error'] = 'Cannot start update check: '+str(exc)
    return result


def compatibility(source):
    """Protocol/extension/Skill changes require the full installer, not a pointer switch."""
    source = Path(source)
    release = read(source/'distribution/release.json')
    digest = hashlib.sha256(str(release['protocol']).encode())
    paths = [source/'saygo/integrations/browser_bridge.py', source/'saygo/integrations/browser_setup.py']
    for directory in ('plugins/saygo-device', 'extensions/saygo-browser'):
        paths.extend(p for p in (source/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    for path in sorted(paths):
        data = path.read_bytes().replace(release['version'].encode(), b'<release-version>')
        digest.update(path.relative_to(source).as_posix().encode()); digest.update(data)
    return digest.hexdigest()


def busy(root):
    for path in root.glob('server-*.lock'):
        try:
            with lock(path): pass
        except OSError:
            return True
    home = Path(os.environ.get('SAYGO_HOME_DIR', Path.home()/'.saygo'))
    database = Path(os.environ.get('SAYGO_RUNTIME_DIR', home/'runtime'))/'runtime.sqlite3'
    if database.exists():
        with contextlib.closing(sqlite3.connect(database.resolve().as_uri()+'?mode=ro', uri=True)) as db:
            for (snapshot,) in db.execute('SELECT snapshot FROM runs'):
                if json.loads(snapshot)['status'] not in ('succeeded', 'failed', 'cancelled'):
                    return True
    return False


def asset(release, name, directory):
    entry = next((a for a in release.get('assets', []) if a['name'] == name), None)
    expected_url = DOWNLOAD + release['tag_name'] + '/' + name
    if not entry or entry.get('browser_download_url') != expected_url:
        raise ValueError('Missing or unexpected release asset: '+name)
    digest = entry.get('digest', '')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
        raise ValueError('Release asset has no SHA256 digest: '+name)
    data = fetch(expected_url, timeout=60)
    if hashlib.sha256(data).hexdigest() != digest[7:]:
        raise ValueError('SHA256 mismatch: '+name)
    path = directory/name; path.write_bytes(data)
    return path


def activate(root, selected):
    installed = current(root)
    launcher = selected.get('launcher')
    if launcher:
        data = Path(launcher).read_bytes()
        compile(data, str(root/'update.py'), 'exec')
        fd, temporary = tempfile.mkstemp(dir=root, prefix='.launcher-')
        try:
            with os.fdopen(fd, 'wb') as stream: stream.write(data)
            os.replace(temporary, root/'update.py')
        finally:
            Path(temporary).unlink(missing_ok=True)
    write(root/'previous-runtime.json', {'python': installed['python'], 'version': installed['version']})
    write(root/'active-runtime.json', selected)
    (root/'pending-runtime.json').unlink(missing_ok=True)


def apply(root, state, stage_only=False):
    root = Path(root)
    if read(root/'installation.json').get('runtime_mode') == 'package':
        raise ValueError('This installation follows pipx. Run pipx upgrade saygo-agent-control.')
    if not state.get('available') or state.get('error'): return state
    if not stage_only and busy(root):
        state['deferred'] = 'Close other Agent sessions and finish or cancel unfinished tasks before updating.'
        write(root/'update-state.json', state); return state
    installed = current(root)
    release = state['release']; number = release['tag_name'][1:]
    with tempfile.TemporaryDirectory(prefix='saygo-update-') as temporary:
        temporary = Path(temporary)
        installer = asset(release, 'install-saygo-'+number+'.py', temporary)
        archive = asset(release, 'saygo-'+number+'.zip', temporary)
        # Inspect source before executing the verified installer.
        import zipfile
        with zipfile.ZipFile(archive) as bundle:
            for info in bundle.infolist():
                if not (temporary/info.filename).resolve().is_relative_to(temporary.resolve()):
                    raise ValueError('Unsafe source archive path')
            bundle.extractall(temporary)
        source = temporary/('saygo-'+number)
        if compatibility(source) != installed.get('compatibility'):
            state['deferred'] = 'Browser bridge or client Skill changed. Run the new full installer, then reload the browser extension.'
            write(root/'update-state.json', state); return state
        stage = root/'updates'/number
        command = [installed['python'], str(installer), '--archive', str(archive),
                   '--root', str(stage), '--prepare-only', '--client', 'all', '--browser', 'none']
        if installed.get('mobile'): command.append('--mobile')
        if installed.get('install_browser'): command.append('--install-browser')
        if installed.get('config_file'): command += ['--config-file', installed['config_file']]
        subprocess.run(command, check=True, stdout=sys.stderr, stderr=sys.stderr, timeout=900)
        candidate = read(stage/'installation.json')
        if candidate.get('version') != number:
            raise ValueError('Prepared runtime version differs from release')
        subprocess.run([candidate['python'], '-I', '-c', 'from saygo.mcp import server; from saygo.cli import build_parser; build_parser()'],
                       check=True, stdout=sys.stderr, stderr=sys.stderr, timeout=30)
        # Only a verified runtime becomes active; old environments are retained.
        selected = {'python': candidate['python'], 'version': number, 'launcher': str(stage/'update.py'),
                    'channel': state.get('channel', 'stable')}
        if stage_only:
            write(root/'pending-runtime.json', selected)
            state['deferred'] = 'Update downloaded and verified; it will activate at the next idle Agent startup.'
        else:
            activate(root, selected)
            state = {'checked_at': time.time(), 'current': number, 'available': False, 'updated': number}
        write(root/'update-state.json', state)
    return state


def run_server(python, args, env):
    process = subprocess.Popen([python, '-I', '-m', 'saygo.mcp.server', *args], env=env)
    def stop(signum, frame):
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    previous = signal.signal(signal.SIGTERM, stop)
    try:
        return process.wait()
    finally:
        signal.signal(signal.SIGTERM, previous)
        if process.poll() is None:
            stop(None, None)
        process.wait()


def synchronize_package_bridge(root, installed):
    """Stage native-host files for the next browser connection; never stop a host."""
    bridge = installed.get('bridge')
    if not bridge or installed.get('browser') == 'none':
        return
    try:
        with lock(root/'install.lock'):
            latest = read(root/'installation.json')
            if latest.get('version') == installed['version']:
                return
            command = [installed['python'], '-I', '-m', 'saygo.integrations.browser_setup',
                       '--extension-id', installed['extension_id'],
                       '--browser', installed.get('browser', 'chrome'),
                       '--directory', bridge['directory'], '--save-default']
            result = subprocess.check_output(command, text=True, timeout=120)
            latest.update(version=installed['version'], bridge=json.loads(result))
            write(root/'installation.json', latest)
            print('[Saygo] Native host files updated. An already connected browser keeps '
                  'its running host until the user reconnects.', file=sys.stderr)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('[Saygo] Native host update pending: ' + str(exc), file=sys.stderr)


def serve(root, args):
    root = Path(root)
    if read(root/'installation.json').get('runtime_mode') == 'package':
        # No source-checkout discovery and no managed-runtime pointer fallback.
        # The same venv that pipx upgrades is used at every client startup.
        installed = current(root)
        try:
            start_check(root, force=True)
        except Exception as exc:
            print('[Saygo update] Cannot start update check: '+str(exc), file=sys.stderr)
        # WSL/Windows provisioning must not consume the MCP startup deadline.
        threading.Thread(target=synchronize_package_bridge, args=(root, installed),
                         daemon=True, name='saygo-package-bridge').start()
        return run_server(installed['python'], args,
                          {**os.environ, 'SAYGO_INSTALL_ROOT': str(root)})
    marker = root/('server-'+str(os.getpid())+'.lock')
    with contextlib.ExitStack() as stack:
        # Serialize selection and marking so two starting clients cannot update each other.
        with lock(root/'update.lock', blocking=True):
            try:
                config = read(root/'updates.json')
                pending = read(root/'pending-runtime.json')
                if (config.get('automatic') and pending and not busy(root)
                        and pending.get('channel') == config.get('channel', 'stable')
                        and Path(pending['python']).is_file()
                        and version(pending['version']) > version(current(root)['version'])):
                    activate(root, pending)
                    write(root/'update-state.json', {'checked_at': time.time(), 'current': pending['version'], 'available': False})
                # Check on every MCP startup without delaying device connections.
                options = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {'start_new_session': True}
                with (root/'update.log').open('ab') as log:
                    subprocess.Popen([current(root)['python'], '-I', str(root/'update.py'),
                                      '--root', str(root), '--background'],
                                     stdin=subprocess.DEVNULL, stdout=log, stderr=log, **options)
            except Exception as exc:
                state = read(root/'update-state.json'); state['error'] = str(exc)
                write(root/'update-state.json', state)
            info = notice(root, refresh=False)
            if info.get('available') or info.get('error'):
                print('[Saygo update] '+json.dumps(info), file=sys.stderr)
            stack.enter_context(lock(marker))
            python = current(root)['python']
        try:
            env = {**os.environ, 'SAYGO_INSTALL_ROOT': str(root)}
            return run_server(python, args, env)
        finally:
            # ExitStack releases the file before cleanup on Windows.
            stack.close(); marker.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check or update a managed Saygo installation')
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('SAYGO_INSTALL_ROOT', Path.home()/'.local/share/saygo/agent-plugin')))
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--background', action='store_true', help=argparse.SUPPRESS)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--check', action='store_true')
    actions.add_argument('--apply', action='store_true')
    actions.add_argument('--auto', choices=['on', 'off'])
    parser.add_argument('--channel', choices=['stable', 'beta'])
    args, rest = parser.parse_known_args(argv)
    root = args.root.expanduser().resolve()
    installed = read(root/'installation.json')
    if not installed or installed.get('uninstalled'):
        parser.error('No managed installation found; run the current installer first')
    if args.serve:
        return serve(root, rest)
    if installed.get('runtime_mode') == 'package':
        if rest:
            parser.error('Unknown arguments: ' + ' '.join(rest))
        if args.apply or args.auto == 'on' or args.channel:
            parser.error('This installation follows pipx. Run pipx upgrade saygo-agent-control, '
                         'then restart the Agent client; setup is not required again.')
        if args.auto == 'off':
            config = update_data(root/'updates.json')
            config['automatic'] = False
            write(root/'updates.json', config)
        check(root, force=True)
        if not args.background:
            print(json.dumps(notice(root, refresh=False), ensure_ascii=False))
        return 0
    if rest: parser.error('Unknown arguments: '+' '.join(rest))
    if args.background:
        with lock(root/'download.lock'):
            try:
                state = check(root, force=True)
                if read(root/'updates.json').get('automatic'):
                    apply(root, state, stage_only=True)
            except Exception as exc:
                state = read(root/'update-state.json'); state['error'] = str(exc)
                write(root/'update-state.json', state)
        return 0
    with lock(root/'update.lock'), lock(root/'download.lock'):
        config = read(root/'updates.json', {'automatic': False, 'channel': 'stable'})
        if args.auto is not None: config['automatic'] = args.auto == 'on'
        if args.channel:
            config['channel'] = args.channel
            write(root/'update-state.json', {})
        write(root/'updates.json', config)
        if args.check or args.apply or (args.auto is None and not args.channel):
            state = check(root, force=True)
            if args.apply: apply(root, state)
        print(json.dumps(notice(root, refresh=False), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Saygo update failed: '+str(exc), file=sys.stderr)
        raise SystemExit(1)
