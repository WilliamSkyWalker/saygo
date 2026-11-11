"""An available update requires a user choice before new MCP input."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from saygo import updates
from saygo.mcp import server
from saygo.platforms import device_session as ds
from saygo.runtime.interactive import InteractiveRuntime
from saygo.runtime.store import Store


class UpdateDecisionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        installed = {'python': sys.executable, 'version': '0.4.19', 'runtime_mode': 'package'}
        updates.write(self.root / 'installation.json', installed)
        self.store = Store(self.root / 'runtime')
        for mocker in (
                patch.object(ds, 'STATE_DIR', self.root / 'sessions'),
                patch('saygo.runtime.interactive.default_store', return_value=self.store),
                patch.dict('os.environ', {'SAYGO_INSTALL_ROOT': str(self.root)}),
                patch.object(updates, 'current', return_value=installed),
                patch.object(updates, 'fetch', return_value=json.dumps(
                    {'releases': {'1.0.0': [{'yanked': False}]}}).encode()),
                patch('saygo.devices.control.sessions', return_value=[])):
            mocker.start()
            self.addCleanup(mocker.stop)
        errors = contextlib.redirect_stderr(io.StringIO())
        errors.__enter__()
        self.addCleanup(errors.__exit__, None, None, None)
        self.addCleanup(self.join_workers)

    def join_workers(self):
        update_policy = sys.modules.get('saygo.mcp.update_policy')
        worker = None
        if update_policy:
            with update_policy._LOCK:
                state = update_policy._STATES.get(str(self.root))
                worker = state.get('worker') if state else None
        if worker:
            worker.join(3)
            self.assertFalse(worker.is_alive())
        with updates._CHECK_THREADS_LOCK:
            worker = updates._CHECK_THREADS.get(str(self.root))
        if worker:
            worker.join(3)
            self.assertFalse(worker.is_alive())

    def known_update(self):
        updates.check(self.root, force=True)
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            info = server.device_sessions()['updates']
            if info.get('available') and not info.get('checking'):
                return info
            time.sleep(.01)
        self.fail('Update check did not complete')

    def test_known_update_blocks_new_input_but_not_observation(self):
        self.known_update()
        with patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            result = server.device_command('act', 'web', {'action': {'type': 'tap', 'x': 1, 'y': 2}})
            self.assertEqual(result.get('outcome'), 'not_dispatched')
            self.assertTrue(result['requires_user_decision'])
            self.assertEqual(result['updates']['available'], 'v1.0.0')
            execute.assert_not_called()
            server.device_screenshot('web')
            execute.assert_called_once()

    def test_continue_is_explicit_and_applies_to_current_mcp_process(self):
        self.known_update()
        with patch.object(updates, 'apply') as apply, \
                patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            result = server.device_command('update-decision', 'web',
                                           {'decision': 'continue', 'version': 'v1.0.0'})
            self.assertEqual(result.get('decision'), 'continue')
            self.assertTrue(server.device_tap(1, 2, 'another-session')['ok'])
            execute.assert_called_once()
            apply.assert_not_called()

    def test_upgrade_choice_keeps_input_paused_and_review_available(self):
        self.known_update()
        with patch.object(updates, 'apply') as apply, \
                patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            result = server.device_command('update-decision', 'web',
                                           {'decision': 'upgrade', 'version': 'v1.0.0'})
            self.assertEqual(result.get('decision'), 'upgrade')
            blocked = server.device_tap(1, 2, 'web')
            self.assertEqual(blocked['outcome'], 'not_dispatched')
            with patch('saygo.devices.requests.resolve', return_value={'ok': True}) as resolve:
                server.device_command('resolve', 'web', {'request_id': 'example', 'resolution': 'applied'})
                resolve.assert_called_once()
            execute.assert_not_called()
            apply.assert_not_called()

    def test_stale_or_invalid_choice_does_not_clear_gate(self):
        self.known_update()
        for options in ({'decision': 'continue', 'version': 'v0.4.21'},
                        {'decision': 'skip', 'version': 'v1.0.0'}):
            result = server.device_command('update-decision', 'web', options)
            self.assertFalse(result['ok'])
        with patch('saygo.devices.service._request') as execute:
            self.assertTrue(server.device_tap(1, 2, 'web')['requires_user_decision'])
            execute.assert_not_called()

    def make_task(self):
        ds.save_state('web', {'kind': 'browser', 'browser_backend': 'extension',
                             'bridge_directory': str(self.root / 'bridge')})
        state = InteractiveRuntime(self.store).create_task({'web': 'web'})
        state['observations']['web'] = {'id': 'example-observation'}
        self.store.save(state, 'test_observation')
        return state

    @staticmethod
    def payload(result):
        return json.loads(result[0].text) if isinstance(result, list) else result

    def test_task_submission_and_connect_obey_gate_but_cancel_is_available(self):
        self.known_update()
        state = self.make_task()
        options = {'resource': 'web', 'action': {'type': 'tap', 'x': 1, 'y': 2},
                   'observation_id': 'example-observation', 'request_id': 'new-input'}
        with patch.object(InteractiveRuntime, '_action') as action, \
                patch('saygo.devices.control.connect') as connect:
            result = self.payload(server.agent_task('submit', state['id'], options))
            self.assertEqual(result.get('outcome'), 'not_dispatched')
            action.assert_not_called()
            self.assertEqual(self.store.get(state['id'])['requests'], {})
            result = server.device_connect('browser', 'web')
            self.assertEqual(result.get('outcome'), 'not_dispatched')
            connect.assert_not_called()
            result = server.agent_task('cancel', state['id'], {'note': 'End isolated test'})
            self.assertEqual(result['status'], 'cancelled')

    def test_task_previous_request_is_readable_without_acknowledging_update(self):
        state = self.make_task()
        options = {'resource': 'web', 'action': {'type': 'tap', 'x': 1, 'y': 2},
                   'observation_id': 'example-observation', 'request_id': 'prior-input'}
        with patch.object(InteractiveRuntime, '_action') as action:
            InteractiveRuntime(self.store).submit(state['id'], **options)
            action.assert_called_once()
            self.known_update()
            returned = self.payload(server.agent_task('submit', state['id'], options))
            self.assertEqual(returned['id'], state['id'])
            self.assertTrue(returned['updates']['requires_user_decision'])
            action.assert_called_once()
        self.assertEqual(len(self.store.get(state['id'])['requests']), 1)

    def test_first_use_refreshes_recent_but_old_release_cache(self):
        updates.write(self.root / 'update-state.json', {
            'checked_at': time.time(), 'current': '0.4.19', 'available': True,
            'release': {'tag_name': 'v0.4.21'}})
        info = server.device_sessions()['updates']
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline and info.get('available') != 'v1.0.0':
            time.sleep(.01)
            info = server.device_sessions()['updates']
        self.assertEqual(info.get('available'), 'v1.0.0')

    def test_unknown_version_check_does_not_block_input_or_run_network_on_request_thread(self):
        entered, release = threading.Event(), threading.Event()
        self.addCleanup(release.set)
        def fetch(url):
            self.assertIsNot(threading.current_thread(), threading.main_thread())
            entered.set()
            release.wait(3)
            return json.dumps({'releases': {}}).encode()
        with patch.object(updates, 'fetch', side_effect=fetch), \
                patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            info = server.device_sessions()['updates']
            self.assertTrue(info['checking'])
            self.assertTrue(entered.wait(1))
            result = server.device_tap(1, 2, 'web')
            self.assertTrue(result['ok'])
            execute.assert_called_once()
            release.set()
            self.join_workers()

    def test_offline_unknown_version_does_not_block_operations(self):
        with patch.object(updates, 'fetch', side_effect=OSError('offline')):
            server.device_sessions()
            self.join_workers()
        info = server.device_command('update-status', 'web')['updates']
        self.assertIn('offline', info['error'])
        self.assertNotIn('requires_user_decision', info)
        with patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            self.assertTrue(server.device_tap(1, 2, 'web')['ok'])
            execute.assert_called_once()

    def test_read_result_keeps_existing_outcome_and_prompts_before_next_action(self):
        self.known_update()
        original = {'ok': False, 'outcome': 'uncertain', 'requires_observation': True}
        with patch('saygo.devices.service._request', return_value=original):
            result = server.device_command('diagnose', 'web')
        self.assertEqual(result['outcome'], 'uncertain')
        self.assertTrue(result['requires_observation'])
        self.assertTrue(result['updates']['requires_user_decision'])
        self.assertNotIn('updates', original)

    def test_repeated_calls_use_cached_check_and_continue_does_not_repeat_prompt(self):
        self.known_update()
        server.device_command('update-decision', 'web', {'decision': 'continue', 'version': 'v1.0.0'})
        with patch.object(updates, 'check') as check, \
                patch('saygo.devices.service._request', return_value={'ok': True}):
            for unused in range(5):
                result = server.device_tap(1, 2, 'web')
                self.assertTrue(result['ok'])
                self.assertNotIn('updates', result)
            check.assert_not_called()

    def test_refresh_metadata_failure_preserves_unanswered_known_update(self):
        from saygo.mcp import update_policy
        self.known_update()
        state = update_policy._STATES[str(self.root)]
        with patch.object(updates, 'current', side_effect=OSError('metadata unavailable')):
            update_policy._refresh(self.root, state, False)
        with patch('saygo.devices.service._request') as execute:
            blocked = server.device_tap(1, 2, 'web')
            self.assertTrue(blocked['requires_user_decision'])
            self.assertEqual(blocked['updates']['available'], 'v1.0.0')
            self.assertIn('metadata unavailable', blocked['updates']['error'])
            execute.assert_not_called()

    def test_worker_start_failure_preserves_unanswered_known_update(self):
        from saygo.mcp import update_policy
        self.known_update()
        state = update_policy._STATES[str(self.root)]
        state['next_poll'] = 0
        with patch.object(threading.Thread, 'start', side_effect=RuntimeError('worker unavailable')):
            blocked = update_policy.before_action()
        self.assertTrue(blocked['requires_user_decision'])
        self.assertEqual(blocked['updates']['available'], 'v1.0.0')
        self.assertIn('worker unavailable', blocked['updates']['error'])

    def test_choice_cannot_race_a_newly_reported_version(self):
        from saygo.mcp import update_policy
        old = self.known_update()
        def stale_status():
            with update_policy._LOCK:
                update_policy._STATES[str(self.root)]['info']['available'] = 'v1.0.1'
            return old
        with patch.object(update_policy, 'status', side_effect=stale_status):
            result = update_policy.decide('continue', 'v1.0.0')
        self.assertFalse(result['ok'])
        self.assertIsNone(update_policy._STATES[str(self.root)]['decision'])

    def test_user_can_change_upgrade_choice_to_continue_without_consuming_request_id(self):
        self.known_update()
        server.device_command('update-decision', 'web', {'decision': 'upgrade', 'version': 'v1.0.0'})
        with patch('saygo.devices.service._request', return_value={'ok': True}) as execute:
            blocked = server.device_tap(1, 2, 'web', request_id='pending-input')
            self.assertEqual(blocked['outcome'], 'not_dispatched')
            server.device_command('update-decision', 'web', {'decision': 'continue', 'version': 'v1.0.0'})
            self.assertTrue(server.device_tap(1, 2, 'web', request_id='pending-input')['ok'])
            execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
