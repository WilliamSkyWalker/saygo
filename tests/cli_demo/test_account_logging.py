"""账号值在普通日志及异常中脱敏，原始报告数据不被改写。"""
import io
import logging
import unittest

from saygo.logger import get_logger


class AccountLoggingTests(unittest.TestCase):
    def test_nested_account_values_and_tracebacks_are_redacted(self):
        from saygo.logger import redact_values
        logger = get_logger('account_test')
        output = io.StringIO()
        handler = logging.StreamHandler(output)
        logger.addHandler(handler)
        self.addCleanup(logger.removeHandler, handler)
        account = {'email': 'example@example.test', 'custom': {'token': 'example-secret'}}
        with redact_values(account):
            logger.info('Case uses %s', account['email'])
            try:
                raise RuntimeError(account['custom']['token'])
            except RuntimeError:
                logger.exception('request failed')
        self.assertNotIn('example@example.test', output.getvalue())
        self.assertNotIn('example-secret', output.getvalue())
        self.assertIn('[REDACTED]', output.getvalue())
        self.assertEqual(account['custom']['token'], 'example-secret')

    def test_redaction_scope_does_not_leak_to_other_runs(self):
        from saygo.logger import redact_values
        logger = get_logger('account_scope_test')
        output = io.StringIO()
        handler = logging.StreamHandler(output)
        logger.addHandler(handler)
        self.addCleanup(logger.removeHandler, handler)
        with redact_values({'token': 'example-secret'}):
            logger.info('example-secret')
        logger.info('public example text')
        self.assertEqual(output.getvalue(), '[REDACTED]\npublic example text\n')
