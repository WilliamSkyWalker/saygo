"""Check the actual desktop executable and frozen native host in isolated state."""
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from saygo.integrations.browser_bridge import Client, PROTOCOL, read_frame, write_frame


def frame(process):
    result = queue.Queue()
    def read():
        try:
            result.put(read_frame(process.stdout))
        except Exception as exc:
            result.put(exc)
    threading.Thread(target=read, daemon=True).start()
    value = result.get(timeout=15)
    if isinstance(value, Exception):
        raise value
    return value


def check():
    directory = ROOT / 'dist/desktop'
    if sys.platform == 'darwin':
        executable = directory / 'SaygoDesktop.app/Contents/MacOS/SaygoDesktop'
    else:
        executable = directory / 'SaygoDesktop' / ('SaygoDesktop.exe' if os.name == 'nt' else 'SaygoDesktop')
    host = executable.with_name('SaygoNativeHost.exe') if os.name == 'nt' else executable
    version = json.loads((ROOT / 'distribution/release.json').read_text())['version']
    with tempfile.TemporaryDirectory(prefix='saygo-frozen-check-') as temporary:
        root = Path(temporary)
        env = {**os.environ, 'QT_QPA_PLATFORM':'offscreen', 'SAYGO_HOME_DIR':str(root / 'state'),
               'SAYGO_RUNTIME_DIR':str(root / 'runtime')}
        subprocess.run([str(executable), '--smoke-test'], cwd=root, env=env, check=True, timeout=45)
        print('Packaged Qt startup: passed', flush=True)
        bridge = root / 'bridge'
        process = subprocess.Popen([str(host), '--native-host', '--directory', str(bridge)],
            cwd=root, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            hello = frame(process)
            assert hello == {'type':'hello', 'protocol':PROTOCOL, 'version':version}, hello
            write_frame(process.stdin, {'type':'hello', 'protocol':PROTOCOL, 'version':'test-peer'})
            deadline = time.monotonic() + 10
            while True:
                status = bridge / 'status.json'
                if status.exists() and json.loads(status.read_text(encoding='utf-8')).get('connected'):
                    break
                if process.poll() is not None or time.monotonic() >= deadline:
                    raise RuntimeError('Frozen native host did not become connected')
                time.sleep(.02)
            result = queue.Queue()
            def client():
                try:
                    result.put(Client(bridge, timeout=5).call('pages'))
                except Exception as exc:
                    result.put(exc)
            threading.Thread(target=client, daemon=True).start()
            request = frame(process)
            assert request['operation'] == 'pages', request
            pages = [{'page_id':'fixture:1', 'url':'https://example.test/'}]
            write_frame(process.stdin, {'id':request['id'], 'last':True,
                                       'chunk':json.dumps({'result':pages})})
            actual = result.get(timeout=10)
            assert actual == pages, actual
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            errors = process.stderr.read().decode('utf-8', errors='replace')
            process.stdout.close()
            process.stderr.close()
            if process.returncode:
                raise RuntimeError('Frozen native host failed: ' + errors)
        print('Packaged native host version, handshake and file IPC: passed (synthetic extension peer)', flush=True)


if __name__ == '__main__':
    check()
