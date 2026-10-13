"""Device profile stays restricted across supported MCP registration APIs."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from saygo.mcp import server


class ProfilesTests(unittest.TestCase):
    def legacy_server(self, extra=()):
        entries = {name: SimpleNamespace(name=name)
                   for name in server._DEVICE_PROFILE_KEEP | server._RUN_PROFILE_ONLY | set(extra)}
        manager = SimpleNamespace(_tools=entries, list_tools=lambda: list(entries.values()))
        return SimpleNamespace(_tool_manager=manager)

    def test_sdk_1_2_without_remove_tool_keeps_only_device_tools(self):
        instance = self.legacy_server()
        with patch.object(server, 'mcp', instance):
            server._apply_profile('device')
        self.assertEqual(set(instance._tool_manager._tools), server._DEVICE_PROFILE_KEEP)

    def test_unknown_registration_api_fails_closed(self):
        with patch.object(server, 'mcp', SimpleNamespace()):
            with self.assertRaises(SystemExit):
                server._apply_profile('device')

    def test_legacy_profile_rejects_unregistered_extra_tools(self):
        with patch.object(server, 'mcp', self.legacy_server({'unexpected_tool'})):
            with self.assertRaisesRegex(SystemExit, 'unexpected_tool'):
                server._apply_profile('device')
