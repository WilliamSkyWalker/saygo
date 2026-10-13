"""Durable input survives process death and excludes concurrent dispatch."""
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch

from saygo.devices import requests
from saygo.platforms import device_session as ds
from saygo.runtime.locking import resource_guard
from saygo.runtime.store import BusyError


class RequestRecoveryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        patcher = patch.object(ds, 'STATE_DIR', self.root / 'sessions')
        patcher.start()
        self.addCleanup(patcher.stop)
        self.keys = ['mobile:example-device']

    def test_process_death_retains_ownership_and_retry_never_dispatches(self):
        code = '''
import os, sys
from pathlib import Path
from saygo.platforms import device_session as ds
from saygo.devices import requests
ds.STATE_DIR = Path(sys.argv[1]) / 'sessions'
def dispatch(_):
    (ds.STATE_DIR.parent / 'sent').write_text('input sent')
    os._exit(23)
requests.run('example', 'request-a', {'text': 'example'}, ['mobile:example-device'], dispatch)
'''
        child = subprocess.run([sys.executable, '-c', code, str(self.root)],
                               capture_output=True, text=True, timeout=30)
        self.assertEqual(child.returncode, 23, child.stderr)
        self.assertEqual((self.root / 'sent').read_text(), 'input sent')
        callback = Mock()
        result = requests.run('example', 'request-a', {'text': 'example'}, self.keys, callback)
        self.assertEqual(result['outcome'], 'uncertain')
        callback.assert_not_called()
        with self.assertRaises(BusyError), resource_guard(self.keys):
            pass
        before_review = time.time()
        requests.resolve('example', 'request-a', 'applied', 'Observed the example input')
        with self.assertRaises(ValueError):
            requests.validate_observation({'at': before_review}, self.keys)
        requests.run('example', 'request-a', {'text': 'example'}, self.keys, callback)
        callback.assert_not_called()
        requests.validate_observation({'at': time.time()}, self.keys)
        with resource_guard(self.keys):
            pass
        self.assertTrue(requests.list_operations('example')['operations'][0]['resolved'])

    def test_concurrent_request_is_excluded_then_returns_cached_result(self):
        entered, finish = threading.Event(), threading.Event()
        calls = []
        def dispatch(_):
            calls.append('sent')
            entered.set()
            self.assertTrue(finish.wait(5))
            return {'ok': True, 'dispatched': True}
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(requests.run, 'example', 'request-a', {}, self.keys, dispatch)
            try:
                self.assertTrue(entered.wait(5))
                with self.assertRaises(BusyError):
                    requests.run('example', 'request-a', {}, self.keys, dispatch)
            finally:
                finish.set()
            original = pending.result()
        self.assertEqual(requests.run('example', 'request-a', {}, self.keys, dispatch), original)
        self.assertEqual(calls, ['sent'])

    def test_blank_request_id_rejected_before_input(self):
        callback = Mock()
        with self.assertRaises(ValueError):
            requests.run('example', '', {}, self.keys, callback)
        callback.assert_not_called()

    def test_mobile_start_checks_physical_device_lock_before_starting_session(self):
        from saygo.devices import service
        from saygo.runtime.locking import reserve, release
        reserve('example-task', ['mobile:example-device'])
        self.addCleanup(release, 'example-task')
        with patch.object(ds, 'start') as start:
            result = service.execute('start', 'example-device', os='android')
        self.assertFalse(result['ok'])
        self.assertIn('owned', result['error'])
        start.assert_not_called()
