"""Preserve Android keyboard choice through Appium's session IME endpoints.

No device shell or UI inspection is needed. A missing historical choice is never
inferred from installed engines: a voice service can also appear in that list.
"""


class InputMethodError(RuntimeError):
    """Keyboard preparation failed before an input action was dispatched."""

    dispatched = False


def _component(value):
    if not isinstance(value, str) or "/" not in value:
        return ""
    package, name = value.strip().split("/", 1)
    if not package or not name:
        return ""
    return package + "/" + (package + name if name.startswith(".") else name)


def _automation(value):
    # Appium Settings ships UnicodeIME, AppiumIME and EmptyIME; none is a
    # user keyboard. Ordinary keyboard IDs always come from the device/user.
    return _component(value).startswith("io.appium.settings/")


class AndroidInputMethod:
    def __init__(self, driver, state, save=None):
        self.driver, self.state, self.save = driver, state, save
        for action, method in (("active_engine", "GET"), ("available_engines", "GET"), ("activate", "POST")):
            driver.command_executor.add_command(
                "saygo_ime_" + action, method, "/session/$sessionId/ime/" + action)

    def _request(self, action, params=None):
        try:
            response = self.driver.execute("saygo_ime_" + action, params or {})
            return response["value"]
        except Exception as exc:
            raise InputMethodError(
                f"Android input method {action} failed: {exc}") from exc

    def current(self):
        current = self._request("active_engine")
        if not _component(current):
            raise InputMethodError("Android input method could not be determined; inspect the system keyboard settings")
        return current

    def _remember(self, current):
        if self.state.get("manual_ime") == current:
            return
        state = {**self.state, "manual_ime": current}
        try:
            if self.save is not None:
                self.save(state)
        except Exception as exc:
            raise InputMethodError(f"Could not save Android input method before changing it: {exc}") from exc
        self.state.update(state)

    def record_current(self):
        """Observe a new connection without switching a legacy session's IME."""
        current = self.current()
        if not _automation(current):
            self._remember(current)
        return current

    def ensure_manual(self, input_method=None):
        current = self.current()
        if input_method is None and not _automation(current):
            self._remember(current)
            return self._result(current, False)

        engines = self._request("available_engines")
        if not isinstance(engines, list) or not all(_component(engine) for engine in engines):
            raise InputMethodError("Android input method list is invalid; inspect the system keyboard settings")
        candidates = [engine for engine in engines if not _automation(engine)]
        desired = input_method if input_method is not None else self.state.get("manual_ime")
        target = next((engine for engine in candidates if _component(engine) == _component(desired)), None)
        if target is None:
            raise InputMethodError(
                "The original Android keyboard is unavailable or unknown. Select a normal keyboard in "
                "Android system settings and retry handoff or resume. Installed non-Appium input methods: "
                + (", ".join(candidates) or "(none installed)"))

        # Save the chosen recovery target before touching the remote setting.
        # A lost response must not lose this choice or trigger an automatic retry.
        self._remember(target)
        changed = _component(current) != _component(target)
        if changed:
            self._request("activate", {"engine": target})
            current = self.current()
            if _component(current) != _component(target):
                raise InputMethodError("Android keyboard restoration verification failed; the requested input method is not active")
        return self._result(current, changed)

    def _result(self, current, changed):
        return {"platform": "android", "current_input_method": current,
                "manual_input_method": self.state.get("manual_ime"), "changed": changed}
