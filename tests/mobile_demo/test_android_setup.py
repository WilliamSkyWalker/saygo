"""Android first-use guidance stays read-only and respects the selected host."""
import contextlib
import copy
import sys
import unittest
from unittest.mock import patch

from saygo.devices import android_setup, mobile, mobile_host, toolchain


def ready_check(identifier):
    return {"id": identifier, "status": "ready", "message": "Available"}


class AndroidSetupTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.python = self.stack.enter_context(patch.object(
            android_setup, "mobile_python_check", return_value=ready_check("python_mobile")))
        self.local = self.stack.enter_context(patch.object(
            android_setup, "local_checks", return_value=[ready_check("android_sdk")]))
        self.windows = self.stack.enter_context(patch.object(
            android_setup, "windows_checks", return_value=[ready_check("android_sdk")]))
        self.no_mutation = []
        for module, name in ((mobile, "install_android"), (mobile, "ensure_java"),
                             (mobile, "boot_device"), (mobile, "connect"),
                             (toolchain, "ensure_node"), (toolchain, "install_appium"),
                             (toolchain, "install_drivers"), (mobile_host, "prepare_windows")):
            call = self.stack.enter_context(patch.object(
                module, name, side_effect=AssertionError("Diagnostics must not call " + name)))
            self.no_mutation.append(call)

    def assert_read_only(self):
        for call in self.no_mutation:
            call.assert_not_called()

    def assert_ready_not_online(self, result, host):
        self.assertTrue(result["ok"])
        self.assertEqual(result["platform"], "android")
        self.assertEqual(result["host"], host)
        self.assertIn("client_os", result)
        self.assertIsNone(result["device_online"])
        self.assertIn("notes", result)
        self.assert_read_only()

    def test_native_windows_and_mac_check_local_host(self):
        for system in ("Windows", "Darwin"):
            with self.subTest(system=system), \
                    patch.object(mobile_host.platform, "system", return_value=system), \
                    patch.object(mobile_host, "is_wsl", return_value=False):
                self.local.reset_mock()
                self.windows.reset_mock()
                result = android_setup.diagnose()
                self.assert_ready_not_online(result, "local")
                self.local.assert_called_once_with()
                self.windows.assert_not_called()

    def test_wsl_auto_without_kvm_checks_windows_without_bootstrap(self):
        with patch.object(mobile_host.platform, "system", return_value="Linux"), \
                patch.object(mobile_host, "is_wsl", return_value=True), \
                patch.object(mobile_host, "has_kvm", return_value=False):
            result = android_setup.diagnose()
        self.assert_ready_not_online(result, "windows")
        self.windows.assert_called_once_with()
        self.local.assert_not_called()

    def test_wsl_explicit_local_keeps_local_even_without_kvm(self):
        with patch.object(mobile_host.platform, "system", return_value="Linux"), \
                patch.object(mobile_host, "is_wsl", return_value=True), \
                patch.object(mobile_host, "has_kvm", return_value=False):
            result = android_setup.diagnose(host="local")
        self.assert_ready_not_online(result, "local")
        self.local.assert_called_once_with()
        self.windows.assert_not_called()

    def test_wsl_explicit_windows_keeps_windows_even_with_kvm(self):
        with patch.object(mobile_host.platform, "system", return_value="Linux"), \
                patch.object(mobile_host, "is_wsl", return_value=True), \
                patch.object(mobile_host, "has_kvm", return_value=True):
            result = android_setup.diagnose(host="windows")
        self.assert_ready_not_online(result, "windows")
        self.windows.assert_called_once_with()
        self.local.assert_not_called()

    def test_missing_local_components_are_reported_without_installing(self):
        checks = [{"id": name, "status": "missing", "message": name + " is missing"}
                  for name in ("android_sdk", "java", "appium", "uiautomator2")]
        self.local.return_value = copy.deepcopy(checks)
        with patch.object(mobile_host, "select_host", return_value="local"):
            result = android_setup.diagnose(host="local")
        self.assertFalse(result["ok"])
        self.assertIsNone(result["device_online"])
        for check in checks:
            self.assertIn(check, result["checks"])
        self.assertTrue(result["commands"], "Missing local tools need actionable setup commands")
        self.assert_read_only()

    def test_unknown_windows_check_cannot_claim_ready(self):
        check = {"id": "windows_host", "status": "unknown", "message": "PowerShell inspection failed"}
        self.windows.return_value = [check]
        with patch.object(mobile_host, "select_host", return_value="windows"):
            result = android_setup.diagnose(host="windows")
        self.assertFalse(result["ok"])
        self.assertEqual(result["host"], "windows")
        self.assertIn(check, result["checks"])
        self.assertIsNone(result["device_online"])
        self.assert_read_only()

    def test_missing_python_merges_repair_command_with_host_guidance(self):
        command = {"argv": [sys.executable, "-m", "pip", "install", "saygo-agent-control[mobile]"],
                   "command": "python -m pip install 'saygo-agent-control[mobile]'",
                   "shell": "posix", "run_on": "client", "label": "Install mobile Python dependencies"}
        self.python.return_value = {"id": "python_mobile", "status": "missing",
                                    "message": "Appium Python client is missing", "commands": [command]}
        self.local.return_value = [{"id": "java", "status": "missing", "message": "Java is missing"}]
        with patch.object(mobile_host, "select_host", return_value="local"):
            result = android_setup.diagnose(host="local")
        self.assertFalse(result["ok"])
        self.assertIn(command, result["commands"])
        self.assertTrue(any("--tools-only" in item["argv"] for item in result["commands"]))
        self.assert_read_only()

    def test_remote_server_does_not_select_or_inspect_local_host(self):
        with patch.object(mobile_host, "select_host", side_effect=AssertionError("Remote must not select a host")), \
                patch.object(mobile, "discover", side_effect=AssertionError("Remote must not discover local devices")):
            result = android_setup.diagnose(host="windows", server_url="https://appium.example.test")
        self.assert_ready_not_online(result, "remote")
        self.python.assert_called_once_with()
        self.local.assert_not_called()
        self.windows.assert_not_called()
        self.assertFalse(any("--tools-only" in item["argv"] for item in result["commands"]))

    def test_remote_server_still_reports_missing_python_client(self):
        command = {"argv": [sys.executable, "-m", "pip", "install", "saygo-agent-control[mobile]"],
                   "command": "python -m pip install 'saygo-agent-control[mobile]'",
                   "shell": "posix", "run_on": "client", "label": "Install mobile Python dependencies"}
        self.python.return_value = {"id": "python_mobile", "status": "missing",
                                    "message": "Appium Python client is missing", "commands": [command]}
        with patch.object(mobile_host, "select_host", side_effect=AssertionError("Remote must not select a host")):
            result = android_setup.diagnose(server_url="http://127.0.0.1:4723")
        self.assertFalse(result["ok"])
        self.assertEqual(result["host"], "remote")
        self.assertIn(command, result["commands"])
        self.assertIsNone(result["device_online"])
        self.local.assert_not_called()
        self.windows.assert_not_called()
        self.assert_read_only()

    def test_toolchain_commands_keep_host_and_require_explicit_license_consent(self):
        for host in ("local", "windows"):
            with self.subTest(host=host):
                commands = android_setup.toolchain_commands(host)
                self.assertEqual(len(commands), 2)
                self.assertEqual(sum("--dry-run" in item["argv"] for item in commands), 1)
                for item in commands:
                    argv = item["argv"]
                    self.assertEqual(argv[:5], [sys.executable, "-m", "saygo.cli", "device", "install"])
                    self.assertEqual(argv[argv.index("--platform") + 1], "android")
                    self.assertEqual(argv[argv.index("--host") + 1], host)
                    self.assertIn("--tools-only", argv)
                    self.assertNotIn("--accept-licenses", argv)
                    self.assertNotIn("--boot", argv)
                    self.assertNotIn("--connect", argv)
                    for key in ("command", "shell", "run_on", "label"):
                        self.assertTrue(item[key])
        self.assert_read_only()

    def test_setup_error_payload_preserves_guidance_and_original_error(self):
        setup = {"ok": False, "platform": "android", "checks": [
            {"id": "java", "status": "missing", "message": "Java is missing"}]}
        error = android_setup.MobileSetupError("Android setup is incomplete", setup)
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(error.setup, setup)
        payload = android_setup.error_payload(error)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"], str(error))
        self.assertEqual(payload["setup"], setup)
        ordinary = android_setup.error_payload(ValueError("Select an explicit device"))
        self.assertEqual(ordinary["error"], "Select an explicit device")
        self.assertNotIn("setup", ordinary)

    def test_import_failure_preserves_blocked_environment_explanation(self):
        self.python.return_value = dict(id='python_mobile', status='blocked',
                                        message='Packaged application cannot run pip', commands=[], notes=[])
        error = android_setup.python_dependency_error(ImportError('appium import failed'))
        check = error.setup['checks'][0]
        self.assertEqual(check['status'], 'blocked')
        self.assertIn('cannot run pip', check['message'])
        self.assertIn('appium import failed', str(error))


if __name__ == "__main__":
    unittest.main()
