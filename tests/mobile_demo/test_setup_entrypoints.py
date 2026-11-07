"""First-use setup guidance survives CLI/MCP boundaries without device actions."""
import builtins
import contextlib
import inspect
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from saygo.cli import main
from saygo.commands import doctor
from saygo.devices import android_setup, control, dependency_commands, mobile, mobile_host, service, toolchain
from saygo.platforms import device_session as ds
from saygo.platforms.appium import AppiumPlatform
from saygo.platforms import appium_server


def setup_result(ok=False):
    return {"ok": ok, "platform": "android", "client_os": "macos", "host": "local",
            "checks": [{"id": "java", "status": "ready" if ok else "missing",
                        "message": "Available" if ok else "Java is missing"}],
            "commands": [], "notes": [], "device_online": None}


class SetupEntrypointTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="saygo-setup-entrypoints-")
        self.addCleanup(temporary.cleanup)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(ds, "STATE_DIR", Path(temporary.name) / "sessions"))
        self.execute = self.stack.enter_context(patch.object(
            service, "execute", side_effect=AssertionError("Setup diagnostics must not operate a device")))

    def test_doctor_android_defaults_to_read_only_auto_host(self):
        expected = setup_result(ok=True)
        signature = inspect.signature(android_setup.diagnose)
        with patch.object(android_setup, "diagnose", return_value=expected) as diagnose, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            main(["doctor", "--platform", "android"])
        diagnose.assert_called_once()
        arguments = signature.bind(*diagnose.call_args.args, **diagnose.call_args.kwargs)
        arguments.apply_defaults()
        self.assertEqual(arguments.arguments, {"host": "auto", "server_url": None})
        self.assertEqual(json.loads(output.getvalue()), expected)
        self.execute.assert_not_called()

    def test_doctor_passes_explicit_host_and_server_to_shared_diagnostics(self):
        expected = setup_result(ok=True)
        expected["host"] = "remote"
        signature = inspect.signature(android_setup.diagnose)
        with patch.object(android_setup, "diagnose", return_value=expected) as diagnose, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            main(["doctor", "--platform", "android", "--host", "windows",
                  "--server-url", "https://appium.example.test"])
        diagnose.assert_called_once()
        arguments = signature.bind(*diagnose.call_args.args, **diagnose.call_args.kwargs)
        arguments.apply_defaults()
        self.assertEqual(arguments.arguments, {"host": "windows", "server_url": "https://appium.example.test"})
        self.assertEqual(json.loads(output.getvalue()), expected)
        self.execute.assert_not_called()

    def test_doctor_missing_prerequisite_returns_json_and_failure_exit(self):
        expected = setup_result()
        with patch.object(android_setup, "diagnose", return_value=expected) as diagnose, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as stopped:
                main(["doctor", "--platform", "android", "--host", "local"])
        self.assertEqual(stopped.exception.code, 2)
        diagnose.assert_called_once()
        self.assertEqual(json.loads(output.getvalue()), expected)
        self.execute.assert_not_called()

    def test_doctor_platform_rejects_session_or_probe_before_dispatch(self):
        for extra in (["--session", "phone"], ["--probe-action", '{"type":"tap","x":1,"y":1}']):
            with self.subTest(extra=extra), patch.object(android_setup, "diagnose") as diagnose, \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises((ValueError, SystemExit)) as rejected:
                    main(["doctor", "--platform", "android", *extra])
                if isinstance(rejected.exception, SystemExit):
                    self.assertEqual(rejected.exception.code, 2)
                diagnose.assert_not_called()
                self.execute.assert_not_called()

    def test_existing_doctor_without_platform_keeps_session_path(self):
        expected = {"sessions": [], "python_dependencies": {"appium": False}}
        with patch.object(doctor, "diagnose", return_value=expected) as old_diagnose, \
                patch.object(android_setup, "diagnose") as setup_diagnose, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            main(["doctor"])
        old_diagnose.assert_called_once()
        setup_diagnose.assert_not_called()
        self.assertEqual(json.loads(output.getvalue()), expected)
        self.execute.assert_not_called()

    def test_device_connect_cli_preserves_structured_setup_error(self):
        setup = setup_result()
        error = android_setup.MobileSetupError("Android setup is incomplete", setup)
        with patch.object(control, "connect", side_effect=error) as connect, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as stopped:
                main(["device", "connect", "--platform", "android", "--device", "example-device",
                      "--session", "phone"])
        self.assertEqual(stopped.exception.code, 2)
        payload = json.loads(output.getvalue())
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"], str(error))
        self.assertEqual(payload.get("setup"), setup)
        connect.assert_called_once()
        self.assertEqual(connect.call_args.args[0].session, "phone")
        self.execute.assert_not_called()

    def test_device_connect_mcp_preserves_setup_without_stdout_noise(self):
        from saygo.mcp import server
        setup = setup_result()
        error = android_setup.MobileSetupError("Android setup is incomplete", setup)
        with patch.object(control, "connect", side_effect=error) as connect, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            payload = server.device_connect("android", "phone", {"device": "example-device"})
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"], str(error))
        self.assertEqual(payload.get("setup"), setup)
        self.assertEqual(output.getvalue(), "")
        connect.assert_called_once()
        self.assertEqual(connect.call_args.args[0].session, "phone")
        self.execute.assert_not_called()

    def test_unrelated_connection_error_is_not_replaced_with_setup_guidance(self):
        from saygo.mcp import server
        message = "Session belongs to a different device/server; use another --session"
        with patch.object(control, "connect", side_effect=ValueError(message)), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as stopped:
                main(["device", "connect", "--platform", "android", "--device", "example-device",
                      "--session", "phone"])
            mcp_result = server.device_connect("android", "phone", {"device": "example-device"})
        self.assertEqual(stopped.exception.code, 2)
        for payload in (json.loads(output.getvalue()), mcp_result):
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"], message)
            self.assertNotIn("setup", payload)
        self.execute.assert_not_called()

    def test_saved_binding_import_failure_includes_repair_commands_and_preserves_state(self):
        state = {"os": "android", "device_id": "example-device", "session_id": "saved-session",
                 "server_url": "http://127.0.0.1:4723", "screen_width": 200, "screen_height": 100}
        ds.save_state("phone", state)
        missing = ModuleNotFoundError("No module named appium", name="appium")
        with patch.object(ds, "_attach_driver", side_effect=missing), \
                patch.object(dependency_commands, "_available", return_value=True), \
                patch.object(dependency_commands, "_mobile_requirements", return_value=["Appium-Python-Client>=4"]), \
                patch.object(ds, "start") as start:
            with self.assertRaises(android_setup.MobileSetupError) as failed:
                ds.attach("phone", strict=True)
        self.assertTrue(failed.exception.setup["commands"])
        self.assertIn("Appium-Python-Client>=4", failed.exception.setup["commands"][0]["argv"])
        self.assertIn(str(missing), failed.exception.setup["checks"][0]["message"])
        self.assertEqual(ds.load_state("phone"), state)
        start.assert_not_called()

    def test_initial_appium_import_failure_explains_manual_repair_without_starting_server(self):
        original_import = builtins.__import__

        def import_without_appium(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "appium" or name.startswith("appium."):
                raise ModuleNotFoundError("No module named appium", name="appium")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(dependency_commands, "_available", return_value=True), \
                patch.object(dependency_commands, "_mobile_requirements", return_value=["Appium-Python-Client>=4"]), \
                patch("saygo.platforms.appium_server.AppiumServerManager") as manager, \
                patch("builtins.__import__", side_effect=import_without_appium):
            with self.assertRaises(android_setup.MobileSetupError) as failed:
                AppiumPlatform().setup({"appium": {"os": "android", "device": "example-device"}})
        self.assertTrue(failed.exception.setup["commands"])
        self.assertIn("Appium-Python-Client>=4", failed.exception.setup["commands"][0]["argv"])
        self.assertIn("No module named appium", failed.exception.setup["checks"][0]["message"])
        self.assertIsNone(ds.load_state("phone"))
        manager.assert_not_called()


class DiscoverySetupTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="saygo-discovery-setup-")
        self.addCleanup(temporary.cleanup)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        root = Path(temporary.name)
        self.stack.enter_context(patch.object(ds, "STATE_DIR", root / "sessions"))
        self.stack.enter_context(patch.object(mobile, "sdk_root", return_value=root / "empty-sdk"))
        self.python = self.stack.enter_context(patch.object(android_setup, "mobile_python_check", return_value={
            "id": "python_mobile", "status": "ready", "message": "Available", "commands": [], "notes": []}))
        self.forbidden = []
        for module, name in ((mobile, "run"), (mobile, "install_android"), (mobile, "ensure_java"),
                             (mobile, "download"), (toolchain, "_run"), (toolchain, "install_appium"),
                             (toolchain, "install_drivers")):
            call = self.stack.enter_context(patch.object(
                module, name, side_effect=AssertionError("Unexpected real tool or installation: " + name)))
            self.forbidden.append(call)

    def tearDown(self):
        for call in self.forbidden:
            call.assert_not_called()

    def test_native_discovery_failure_keeps_diagnostic_and_adds_local_guidance(self):
        expected = setup_result()
        for system in ("Windows", "Darwin"):
            with self.subTest(system=system), \
                    patch.object(mobile.platform, "system", return_value=system), \
                    patch.object(mobile, "android_devices", side_effect=RuntimeError("adb is unavailable")), \
                    patch.object(android_setup, "diagnose", return_value=expected) as diagnose:
                result = mobile.discover("android")
            self.assertEqual(result["devices"], [])
            self.assertEqual(result["setup"], expected)
            self.assertIn({"source": "android", "message": "adb is unavailable"}, result["diagnostics"])
            diagnose.assert_called_once_with(host="local")

    def test_failed_windows_discovery_keeps_windows_guidance_even_with_wsl_kvm(self):
        check = {"id": "appium", "status": "missing", "message": "Windows Appium is missing"}
        with patch.object(mobile.platform, "system", return_value="Linux"), \
                patch.object(mobile.platform, "release", return_value="microsoft-WSL2"), \
                patch.object(mobile_host, "has_kvm", return_value=True), \
                patch.object(mobile, "android_devices", return_value=[]), \
                patch.object(mobile_host, "windows_info", return_value={}), \
                patch.object(mobile_host, "prepare_windows", return_value={}) as prepare, \
                patch.object(mobile_host, "call_windows", side_effect=RuntimeError("Windows discovery failed")) as call, \
                patch.object(android_setup, "windows_checks", return_value=[check]) as windows, \
                patch.object(android_setup, "local_checks", side_effect=AssertionError("Wrong host inspected")) as local:
            result = mobile.discover("android")
        self.assertEqual(result["setup"]["host"], "windows")
        self.assertFalse(result["setup"]["ok"])
        self.assertIn(check, result["setup"]["checks"])
        self.assertIn({"source": "windows_android", "message": "Windows discovery failed"}, result["diagnostics"])
        prepare.assert_called_once()
        call.assert_called_once_with({}, "discover")
        windows.assert_called_once_with()
        local.assert_not_called()

    def test_windows_online_devices_survive_missing_client_python_guidance(self):
        devices = [{"id": "example-device", "platform": "android", "connectable": True,
                    "type": "physical", "state": "device"}]
        self.python.return_value = {"id": "python_mobile", "status": "missing",
                                    "message": "Client Appium Python dependency is missing", "commands": [], "notes": []}
        with patch.object(mobile.platform, "system", return_value="Linux"), \
                patch.object(mobile.platform, "release", return_value="microsoft-WSL2"), \
                patch.object(mobile, "android_devices", return_value=[]), \
                patch.object(mobile_host, "windows_info", return_value={}), \
                patch.object(mobile_host, "prepare_windows", return_value={}), \
                patch.object(mobile_host, "call_windows", return_value={
                    "devices": devices, "android_avds": [], "diagnostics": []}), \
                patch.object(android_setup, "windows_checks", return_value=[
                    {"id": "appium", "status": "ready", "message": "Windows host available"}]), \
                patch.object(android_setup, "local_checks", side_effect=AssertionError("Wrong host inspected")):
            result = mobile.discover("android")
        self.assertEqual(result["devices"], devices)
        self.assertEqual(result["diagnostics"], [])
        self.assertEqual(result["host"], "windows")
        self.assertEqual(result["setup"]["host"], "windows")
        self.assertFalse(result["setup"]["ok"])
        self.assertTrue(any(check["id"] == "python_mobile" and check["status"] == "missing"
                            for check in result["setup"]["checks"]))

    def test_remote_connection_failure_diagnoses_remote_and_preserves_transport_error(self):
        url = "https://appium.example.test"
        failure = RuntimeError("Remote Appium endpoint is unreachable")
        with patch.object(ds, "start", side_effect=failure) as start, \
                patch.object(mobile, "discover", side_effect=AssertionError("Remote must not discover local devices")), \
                patch.object(mobile_host, "select_host", side_effect=AssertionError("Remote must not select local host")), \
                patch.object(android_setup, "local_checks", side_effect=AssertionError("Remote must not inspect local tools")), \
                patch.object(android_setup, "windows_checks", side_effect=AssertionError("Remote must not inspect Windows tools")), \
                patch.object(android_setup, "diagnose", wraps=android_setup.diagnose) as diagnose:
            with self.assertRaises(RuntimeError) as failed:
                mobile.connect("android", "example-device", "phone", server_url=url)
        self.assertIs(failed.exception, failure)
        self.assertNotIsInstance(failed.exception, android_setup.MobileSetupError)
        self.assertEqual(diagnose.call_args.kwargs["server_url"], url)
        self.assertFalse(start.call_args.kwargs["appium_config"]["auto_start"])
        self.assertIsNone(ds.load_state("phone"))

    def test_empty_or_unauthorized_discovery_is_not_reported_as_missing_dependencies(self):
        unauthorized = [{"id": "example-device", "platform": "android", "connectable": False,
                         "state": "unauthorized", "type": "physical"}]
        for devices in ([], unauthorized):
            with self.subTest(devices=devices), \
                    patch.object(mobile.platform, "system", return_value="Darwin"), \
                    patch.object(mobile, "android_devices", return_value=devices), \
                    patch.object(android_setup, "diagnose", side_effect=AssertionError("No dependency failure to diagnose")) as diagnose, \
                    patch.object(ds, "start") as start:
                result = mobile.discover("android")
                self.assertEqual(result["devices"], devices)
                self.assertEqual(result["diagnostics"], [])
                self.assertNotIn("setup", result)
                with self.assertRaisesRegex(RuntimeError, "Select exactly one online device") as failed:
                    mobile.connect("android", session="phone")
                self.assertNotIsInstance(failed.exception, android_setup.MobileSetupError)
                diagnose.assert_not_called()
                start.assert_not_called()
                self.assertIsNone(ds.load_state("phone"))

    def test_service_attach_setup_error_is_not_dispatched_and_keeps_binding(self):
        state = {"os": "android", "device_id": "example-device", "session_id": "saved-session",
                 "server_url": "http://127.0.0.1:4723"}
        ds.save_state("phone", state)
        setup = setup_result()
        error = android_setup.MobileSetupError("Mobile client dependency is missing", setup)
        with patch.object(ds, "attach", side_effect=error) as attach, \
                patch.object(ds, "start") as start:
            result = service.execute("screenshot", "phone")
        self.assertFalse(result["ok"])
        self.assertEqual(result["outcome"], "not_dispatched")
        self.assertEqual(result["error"], str(error))
        self.assertEqual(result["setup"], setup)
        self.assertFalse(result.get("dispatched", False))
        self.assertEqual(ds.load_state("phone"), state)
        attach.assert_called_once_with("phone")
        start.assert_not_called()

    def test_missing_appium_binary_exposes_setup_without_spawning_server(self):
        setup = setup_result()
        setup["checks"] = [{"id": "appium", "status": "missing", "message": "Appium is missing"}]
        manager = appium_server.AppiumServerManager("http://127.0.0.1:4723", {"os": "android"})
        with patch.object(manager, "_status_ok", return_value=False), \
                patch.object(appium_server, "find_appium_binary", return_value=None), \
                patch.object(android_setup, "diagnose", return_value=setup) as diagnose, \
                patch.object(appium_server.subprocess, "Popen") as spawn:
            with self.assertRaises(android_setup.MobileSetupError) as failed:
                manager.ensure_running()
        self.assertEqual(failed.exception.setup, setup)
        self.assertIn("Appium", str(failed.exception))
        diagnose.assert_called_once_with(host="local")
        spawn.assert_not_called()
        self.assertFalse(manager._owned)


if __name__ == "__main__":
    unittest.main()
