"""Android keyboard ownership regressions using a fake Appium endpoint."""

import unittest
from unittest.mock import Mock, patch

from saygo.platforms.appium import AppiumPlatform
from saygo.platforms.base import ActionOutcomeUnknown


MANUAL = "com.example.keyboard/.Keyboard"
ALTERNATIVE = "com.example.alternative/.Keyboard"
AUTOMATION = "io.appium.settings/.UnicodeIME"


class Driver:
    def __init__(self, current=MANUAL):
        self.current = current
        self.engines = [MANUAL, ALTERNATIVE, AUTOMATION]
        self.routes = {}
        self.calls = []
        self.texts = []
        self.command_executor = Mock()
        self.command_executor.add_command.side_effect = self.add_command
        self.activate_error = None
        self.ignore_activation = False
        self.type_error = None
        self.after_type = None

    def add_command(self, name, method, path):
        self.routes[name] = (method, path)

    def execute(self, name, params=None):
        method, path = self.routes[name]
        self.calls.append((method, path, params))
        if path.endswith("/active_engine"):
            return {"value": self.current}
        if path.endswith("/available_engines"):
            return {"value": self.engines}
        if path.endswith("/activate"):
            if self.activate_error:
                raise self.activate_error
            if not self.ignore_activation:
                self.current = params["engine"]
            return {"value": None}
        raise AssertionError(path)

    def execute_script(self, script, params):
        if script != "mobile: type":
            raise AssertionError(script)
        self.texts.append(params["text"])
        if self.after_type:
            self.current = self.after_type
        if self.type_error:
            raise self.type_error

    def get_window_size(self):
        return {"width": 400, "height": 800}


class AndroidImeTests(unittest.TestCase):
    def platform(self, current=MANUAL, state=None):
        platform = AppiumPlatform()
        platform._driver = Driver(current)
        platform._ime_state = dict(state or {})
        platform._ime_save = Mock()
        return platform

    def test_new_connection_preserves_and_records_user_keyboard(self):
        driver = Driver()
        with patch("saygo.platforms.appium_server.AppiumServerManager") as manager, \
                patch("appium.webdriver.Remote", return_value=driver) as remote:
            manager.return_value.ensure_running.return_value = "http://127.0.0.1:4723"
            platform = AppiumPlatform()
            platform.setup({"appium": {"os": "android"}})
        caps = remote.call_args.kwargs["options"].to_capabilities()
        self.assertNotIn("appium:unicodeKeyboard", caps)
        self.assertNotIn("appium:resetKeyboard", caps)
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)
        self.assertEqual(driver.current, MANUAL)

    def test_setup_retains_legacy_record_without_guessing_or_switching(self):
        driver = Driver(AUTOMATION)
        with patch("saygo.platforms.appium_server.AppiumServerManager") as manager, \
                patch("appium.webdriver.Remote", return_value=driver):
            manager.return_value.ensure_running.return_value = "http://127.0.0.1:4723"
            platform = AppiumPlatform()
            platform.setup({"appium": {"os": "android", "_ime_state": {"manual_ime": MANUAL}}})
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)
        self.assertEqual(driver.current, AUTOMATION)
        self.assertFalse(any(c[0] == "POST" for c in driver.calls))

    def test_ios_setup_preserves_existing_simulator_keyboard_preferences(self):
        driver = Mock()
        driver.get_window_size.return_value = {"width": 400, "height": 800}
        with patch("saygo.platforms.appium_server.AppiumServerManager") as manager, \
                patch("appium.webdriver.Remote", return_value=driver) as remote:
            manager.return_value.ensure_running.return_value = "http://127.0.0.1:4723"
            AppiumPlatform().setup({"appium": {"os": "ios"}})
        caps = remote.call_args.kwargs["options"].to_capabilities()
        for capability in ("unicodeKeyboard", "resetKeyboard"):
            self.assertNotIn("appium:" + capability, caps)
        self.assertIs(caps.get("appium:connectHardwareKeyboard"), False)
        self.assertIs(caps.get("appium:forceSimulatorSoftwareKeyboardPresence"), False)
        driver.execute.assert_not_called()

    def test_ios_explicit_keyboard_capabilities_override_preservation_defaults(self):
        driver = Mock()
        driver.get_window_size.return_value = {"width": 400, "height": 800}
        with patch("saygo.platforms.appium_server.AppiumServerManager") as manager, \
                patch("appium.webdriver.Remote", return_value=driver) as remote:
            manager.return_value.ensure_running.return_value = "http://127.0.0.1:4723"
            AppiumPlatform().setup({"appium": {"os": "ios", "caps": {
                "connectHardwareKeyboard": True,
                "forceSimulatorSoftwareKeyboardPresence": True,
            }}})
        caps = remote.call_args.kwargs["options"].to_capabilities()
        self.assertIs(caps["appium:connectHardwareKeyboard"], True)
        self.assertIs(caps["appium:forceSimulatorSoftwareKeyboardPresence"], True)

    def test_handoff_restores_saved_keyboard_and_verifies(self):
        platform = self.platform(AUTOMATION, {"manual_ime": MANUAL})
        result = platform.prepare_handoff()
        self.assertEqual(platform._driver.current, MANUAL)
        self.assertTrue(result["changed"])
        self.assertTrue(platform._driver.calls[-1][1].endswith("/active_engine"))

    def test_handoff_saves_before_keyboard_mutation(self):
        platform = self.platform(AUTOMATION)
        platform._ime_save.side_effect = lambda state: self.assertEqual(platform._driver.current, AUTOMATION)
        platform.prepare_handoff(input_method=MANUAL)
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)
        platform._ime_save.assert_called_once_with({"manual_ime": MANUAL})

    def test_live_user_choice_wins_over_saved_choice(self):
        platform = self.platform(ALTERNATIVE, {"manual_ime": MANUAL})
        platform.prepare_handoff()
        self.assertEqual(platform._ime_state["manual_ime"], ALTERNATIVE)
        self.assertEqual(platform._driver.current, ALTERNATIVE)
        self.assertFalse(any(c[0] == "POST" for c in platform._driver.calls))

    def test_missing_or_automation_record_never_guesses_keyboard(self):
        for state in ({}, {"manual_ime": AUTOMATION}, {"manual_ime": "com.example.removed/.Keyboard"}):
            with self.subTest(state=state):
                platform = self.platform(AUTOMATION, state)
                with self.assertRaisesRegex(RuntimeError, "system settings") as raised:
                    platform.prepare_handoff()
                self.assertIn(MANUAL, str(raised.exception))
                self.assertIn(ALTERNATIVE, str(raised.exception))
                self.assertEqual(platform._driver.current, AUTOMATION)

    def test_even_single_candidate_requires_explicit_choice(self):
        platform = self.platform(AUTOMATION)
        platform._driver.engines = [MANUAL, AUTOMATION]
        with self.assertRaisesRegex(RuntimeError, "system settings"):
            platform.prepare_handoff()
        self.assertEqual(platform._driver.current, AUTOMATION)

    def test_empty_and_alternate_appium_imes_are_never_manual_candidates(self):
        for current in ("io.appium.settings/.EmptyIME", "io.appium.settings/.AppiumIME"):
            with self.subTest(current=current):
                platform = self.platform(current)
                platform._driver.engines = [current]
                with self.assertRaisesRegex(RuntimeError, "none installed"):
                    platform.prepare_handoff(input_method=current)
                self.assertNotIn("manual_ime", platform._ime_state)

    def test_explicit_selection_rejects_unknown_and_automation_engines(self):
        for engine in (AUTOMATION, "com.example.absent/.Keyboard"):
            with self.subTest(engine=engine):
                platform = self.platform()
                with self.assertRaises(RuntimeError):
                    platform.prepare_handoff(input_method=engine)
                self.assertEqual(platform._driver.current, MANUAL)

    def test_equivalent_expanded_component_matches_installed_engine(self):
        platform = self.platform("io.appium.settings/io.appium.settings.UnicodeIME", {"manual_ime": MANUAL})
        platform._driver.engines = ["com.example.keyboard/com.example.keyboard.Keyboard", AUTOMATION]
        platform.prepare_handoff()
        self.assertEqual(platform._driver.current, "com.example.keyboard/com.example.keyboard.Keyboard")

    def test_repeated_handoff_resume_and_reconnect_keep_user_selection(self):
        platform = self.platform(AUTOMATION, {"manual_ime": MANUAL})
        platform.prepare_handoff()
        platform.prepare_handoff()
        platform._driver.current = ALTERNATIVE
        platform.prepare_resume()
        reconnected = self.platform(AUTOMATION, platform._ime_state)
        reconnected.prepare_handoff()
        self.assertEqual(reconnected._driver.current, ALTERNATIVE)
        self.assertEqual(sum(c[0] == "POST" for c in platform._driver.calls), 1)

    def test_failed_activation_preserves_restore_target(self):
        platform = self.platform(AUTOMATION)
        platform._driver.activate_error = TimeoutError("response lost")
        with self.assertRaisesRegex(RuntimeError, "input method|keyboard"):
            platform.prepare_handoff(input_method=MANUAL)
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)
        self.assertEqual(sum(c[0] == "POST" for c in platform._driver.calls), 1)

    def test_ignored_activation_is_failure(self):
        platform = self.platform(AUTOMATION, {"manual_ime": MANUAL})
        platform._driver.ignore_activation = True
        with self.assertRaisesRegex(RuntimeError, "verify|verification|still"):
            platform.prepare_handoff()

    def test_persistence_failure_prevents_keyboard_change_and_input(self):
        platform = self.platform()
        platform._ime_save.side_effect = OSError("disk unavailable")
        with self.assertRaises(RuntimeError) as raised:
            platform.input_text("English 中文")
        self.assertFalse(getattr(raised.exception, "dispatched", True))
        self.assertEqual(platform._driver.texts, [])

    def test_input_restores_automation_keyboard_left_by_driver(self):
        platform = self.platform()
        platform._driver.after_type = AUTOMATION
        platform.input_text("English 中文")
        self.assertEqual(platform._driver.texts, ["English 中文"])
        self.assertEqual(platform._driver.current, MANUAL)
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)

    def test_input_never_replays_after_lost_response_and_restores_keyboard(self):
        platform = self.platform()
        platform._driver.after_type = AUTOMATION
        platform._driver.type_error = TimeoutError("response lost")
        with self.assertRaises(ActionOutcomeUnknown):
            platform.input_text("English 中文")
        self.assertEqual(platform._driver.texts, ["English 中文"])
        self.assertEqual(platform._driver.current, MANUAL)

    def test_input_restore_failure_reports_no_replay(self):
        platform = self.platform()
        platform._driver.after_type = AUTOMATION
        platform._driver.activate_error = TimeoutError("device unavailable")
        with self.assertRaisesRegex(ActionOutcomeUnknown, "input method|keyboard"):
            platform.input_text("English 中文")
        self.assertEqual(platform._driver.texts, ["English 中文"])
        self.assertEqual(platform._ime_state["manual_ime"], MANUAL)

    def test_unknown_legacy_keyboard_blocks_input_before_dispatch(self):
        platform = self.platform(AUTOMATION)
        with self.assertRaises(RuntimeError) as raised:
            platform.input_text("English 中文")
        self.assertFalse(getattr(raised.exception, "dispatched", True))
        self.assertEqual(platform._driver.texts, [])

    def test_unsupported_or_malformed_ime_endpoints_block_input(self):
        for response in (TimeoutError("device unavailable"), {"value": "null"}, {"value": None}):
            with self.subTest(response=response):
                platform = self.platform()
                platform._driver.execute = Mock(
                    side_effect=response if isinstance(response, Exception) else None,
                    return_value=response)
                with self.assertRaises(RuntimeError) as raised:
                    platform.input_text("English 中文")
                self.assertFalse(getattr(raised.exception, "dispatched", True))
                self.assertEqual(platform._driver.texts, [])

    def test_empty_input_does_not_query_or_change_keyboard(self):
        platform = self.platform()
        platform.input_text("")
        self.assertEqual(platform._driver.calls, [])
        self.assertEqual(platform._driver.texts, [])

    def test_ios_handoff_resume_leave_keyboard_settings_and_input_unchanged(self):
        platform = AppiumPlatform()
        platform._os = "ios"
        platform._driver = Mock()
        platform.prepare_handoff()
        platform.prepare_resume()
        platform.input_text("English 中文")
        platform._driver.switch_to.active_element.send_keys.assert_called_once_with("English 中文")
        platform._driver.execute.assert_not_called()
        platform._driver.execute_script.assert_not_called()


if __name__ == "__main__":
    unittest.main()
