"""Offline checks for conversation rendering and safe task interaction."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import unittest
import tempfile
from unittest.mock import patch

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
except ImportError:
    QApplication = None


@unittest.skipIf(QApplication is None, 'PySide6 is optional')
class ChatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        from saygo.desktop.app import make_window
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.patches = [patch.dict(os.environ, {'SAYGO_HOME_DIR': self.temp.name}),
                        patch('saygo.devices.control.sessions', return_value=[]),
                        patch('saygo.runtime.interactive.call', return_value={'tasks': []}),
                        patch('saygo.desktop.model.load_settings', side_effect=ValueError('not configured'))]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)
        self.window = make_window(auto_connect=False)
        self.addCleanup(self.window.close)

    def test_messages_escape_markup_and_include_human_reply(self):
        state = {'desktop_goal': '<b>literal task</b>', 'status': 'waiting_for_human',
                 'human': {'instructions': 'Please sign in'}}
        self.window.render_conversation(state, [
            {'kind': 'agent_annotation', 'note': 'Opening settings'},
            {'kind': 'human_returned', 'note': 'Signed in, continue'}])
        text = self.window.timeline.toPlainText()
        for expected in ('<b>literal task</b>', 'Opening settings', 'Signed in, continue', 'Please sign in'):
            self.assertIn(expected, text)
        self.assertNotIn('agent_annotation', text)

    def test_reply_resumes_and_uncertain_action_does_not_dispatch(self):
        self.window.goal.setPlainText('I have signed in')
        self.window.task_state = {'status': 'waiting_for_human'}
        with patch.object(self.window, 'resume_task') as resume:
            self.window.send_message()
            resume.assert_called_once_with('I have signed in')
        self.window.task_state = {'status': 'needs_review'}
        with patch.object(self.window, 'start_task') as start, patch('PySide6.QtWidgets.QMessageBox.information'):
            self.window.send_message()
            start.assert_not_called()

    def test_enter_sends_and_shift_enter_inserts_newline(self):
        self.window.goal.setPlainText('Task')
        calls = []
        self.window.goal.submitted.connect(lambda: calls.append(True))
        QTest.keyClick(self.window.goal, Qt.Key.Key_Return, Qt.KeyboardModifier.ShiftModifier)
        self.assertEqual(calls, [])
        self.assertIn('\n', self.window.goal.toPlainText())
        QTest.keyClick(self.window.goal, Qt.Key.Key_Return)
        self.assertEqual(calls, [True])

    def configure_model(self):
        self.window.base.setText('https://example.com/v1')
        self.window.model.setText('vision-model')
        self.window.key.setText('test-token')

    def wait_for_job(self):
        import time
        deadline = time.monotonic() + 5
        while self.window.worker is not None and time.monotonic() < deadline:
            self.app.processEvents()
            QTest.qWait(10)
        self.assertIsNone(self.window.worker)

    def test_invalid_token_is_reported_without_request(self):
        self.configure_model()
        self.window.key.setText('broken token')
        with patch('saygo.desktop.model.VisionModel.test') as request:
            self.window.test_model()
            request.assert_not_called()
        self.assertIn('空白', self.window.model_feedback.text())

    def test_token_is_masked_again_when_dialog_closes(self):
        from PySide6.QtWidgets import QLineEdit
        self.configure_model()
        self.window.dialogs['模型设置'].show()
        self.window.reveal_key.setChecked(True)
        self.assertEqual(self.window.key.echoMode(), QLineEdit.EchoMode.Normal)
        self.window.dialogs['模型设置'].close()
        self.assertEqual(self.window.key.echoMode(), QLineEdit.EchoMode.Password)

    def test_failed_save_keeps_token_and_shows_inline_error(self):
        self.configure_model()
        self.window.remember.setChecked(True)
        with patch('saygo.desktop.model.secure_backend', side_effect=RuntimeError('secure store unavailable')):
            self.window.save_model()
            self.assertFalse(self.window.key.isEnabled())
            self.wait_for_job()
        self.assertIn('secure store unavailable', self.window.model_feedback.text())
        self.assertEqual(self.window.key.text(), 'test-token')
        self.assertTrue(self.window.key.isEnabled())

    def test_delete_clears_credentials_only_after_success(self):
        from unittest.mock import Mock
        self.configure_model()
        self.window.remember.setChecked(True)
        backend = Mock()
        with patch('saygo.desktop.model.secure_backend', return_value=backend), patch('saygo.desktop.model.save_settings'):
            self.window.delete_key()
            self.wait_for_job()
        backend.delete_password.assert_called_once()
        self.assertEqual(self.window.key.text(), '')
        self.assertFalse(self.window.remember.isChecked())
        self.assertIn('删除', self.window.model_feedback.text())

    def test_managed_targets_are_readable_and_restore_after_disconnect(self):
        from saygo.desktop.connections import COMPUTER, BROWSER
        rows=[{'session':COMPUTER,'platform':'windows','desktop_scope':'computer'},
              {'session':BROWSER,'platform':'browser','backend':'extension','page_id':'p1'}]
        with patch('saygo.devices.control.sessions',return_value=rows):
            self.window.computer_ready=True; self.window.browser_ready=True
            self.window.browser_pages=[{'page_id':'p1'}]; self.window.refresh_sessions()
            self.assertEqual(len(self.window.sessions.selectedItems()),2)
            self.assertIn('本机电脑',self.window.target_label.text())
            self.assertEqual(self.window.sessions.item(0).data(Qt.ItemDataRole.UserRole),COMPUTER)
            self.window.browser_ready=False; self.window.refresh_sessions()
            self.window.browser_ready=True; self.window.refresh_sessions()
            self.assertEqual(len(self.window.sessions.selectedItems()),2)
            self.window.sessions.item(1).setSelected(False)
            self.window.refresh_sessions()
            self.assertEqual(len(self.window.sessions.selectedItems()),1)

    def test_connection_poll_never_rebinds_active_task(self):
        self.window.task_state={'status':'waiting_for_human'}
        with patch.object(self.window,'start_connection_job') as start:
            self.window.poll_connections()
            start.assert_not_called()
