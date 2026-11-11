"""An action preflight runs after deduplication and before durable dispatch intent."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from saygo.devices import requests, service
from saygo.platforms import device_session as ds
from saygo.runtime.locking import session_keys


class RequestPreflightTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        state_patch = patch.object(ds, 'STATE_DIR', self.root / 'sessions')
        state_patch.start()
        self.addCleanup(state_patch.stop)
        ds.save_state('web', {'kind': 'browser', 'browser_backend': 'extension',
                              'bridge_directory': str(self.root / 'bridge')})
        self.keys = session_keys('web')
        self.rejection = {'ok': False, 'outcome': 'not_dispatched', 'dispatched': False,
                          'requires_user_decision': True}

    def test_preflight_rejection_does_not_consume_request_id(self):
        before = Mock(return_value=self.rejection)
        dispatch = Mock(return_value={'ok': True, 'dispatched': True})
        result = requests.run('web', 'one', {'action': 'example'}, self.keys, dispatch,
                              before_dispatch=before)
        self.assertEqual(result, self.rejection)
        dispatch.assert_not_called()
        with requests._store().connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM device_requests').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM resources').fetchone()[0], 0)
        before.return_value = None
        accepted = requests.run('web', 'one', {'action': 'example'}, self.keys, dispatch,
                                before_dispatch=before)
        self.assertTrue(accepted['ok'])
        self.assertEqual(before.call_count, 2)
        dispatch.assert_called_once()

    def test_cached_result_returns_without_running_preflight_or_dispatch(self):
        dispatch = Mock(return_value={'ok': False, 'outcome': 'uncertain'})
        first = requests.run('web', 'lost-response', {'action': 'example'}, self.keys, dispatch)
        before = Mock(return_value=self.rejection)
        repeated = requests.run('web', 'lost-response', {'action': 'example'}, self.keys, dispatch,
                                before_dispatch=before)
        self.assertEqual(repeated, first)
        before.assert_not_called()
        dispatch.assert_called_once()

    def test_service_preflight_is_not_part_of_request_signature_or_device_options(self):
        before = Mock(return_value=None)
        options = {'action': {'type': 'tap', 'x': 20, 'y': 30}, 'observation_id': 'example'}
        with patch.object(service, '_request', return_value={'ok': True, 'dispatched': True}) as execute:
            first = service.execute('act', 'web', request_id='one', preflight=before, **options)
            self.assertTrue(first['ok'], first)
            self.assertNotIn('preflight', execute.call_args.kwargs)
            before.assert_called_once_with()
            before.reset_mock()
            before.return_value = self.rejection
            repeated = service.execute('act', 'web', request_id='one', preflight=before, **options)
        self.assertEqual(repeated, first)
        before.assert_not_called()
        execute.assert_called_once()

    def test_service_rejection_does_not_journal_or_dispatch_and_reads_remain_available(self):
        before = Mock(return_value=self.rejection)
        with patch.object(service, '_request') as execute:
            result = service.execute('act', 'web', preflight=before,
                                     action={'type': 'tap', 'x': 20, 'y': 30})
            self.assertEqual(result, self.rejection)
            execute.assert_not_called()
        self.assertFalse((self.root / 'operations').exists())
        before.reset_mock()
        listing = service.execute('operations', 'web', preflight=before)
        self.assertTrue(listing['ok'])
        before.assert_not_called()


if __name__ == '__main__':
    unittest.main()
