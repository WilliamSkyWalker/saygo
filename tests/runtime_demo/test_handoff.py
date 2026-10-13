"""Offline workflow handoff contracts; no device or manual-input certification."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from saygo.platforms import device_session as ds
from saygo.platforms.android_ime import InputMethodError
from saygo.runtime import Runtime, Store
from saygo.runtime.locking import resource_guard, session_keys
from saygo.runtime.resources import VisualResource
from saygo.runtime.store import BusyError


class HumanResource:
    def __init__(self, name, trace):
        self.name = name
        self.trace = trace
        self.fail = None
        self.frame = 0

    def _call(self, method):
        self.trace.append((self.name, method))
        if self.fail == method:
            raise RuntimeError(f"{self.name} {method} failed")

    def observe(self):
        self._call("observe")
        return b"test frame", {"frame": self.frame, "screen_size": [100, 200]}

    def handoff(self, instructions, owner):
        self._call("handoff")
        return {"status": "waiting_for_human"}

    def resume(self, note):
        self._call("resume")
        return {"status": "needs_observation"}

    def close(self):
        pass


class WorkflowHandoffTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        state_patch = patch.object(ds, "STATE_DIR", self.root / "sessions")
        state_patch.start()
        self.addCleanup(state_patch.stop)
        self.store = Store(self.root / "runtime")
        self.trace = []
        self.resources = {name: HumanResource(name, self.trace) for name in ("phone", "tablet")}
        self.runtime = Runtime(self.store, lambda spec: self.resources[spec["session"]])
        self.workflow = {
            "version": 1,
            "resources": {
                "phone": {"kind": "android", "session": "phone"},
                "tablet": {"kind": "ios", "session": "tablet"},
            },
            "steps": [
                {"id": "manual", "kind": "human", "resource": "phone",
                 "instructions": "Use the local test input page", "verify_step": "verified"},
                {"id": "verified", "kind": "check", "actual": True, "equals": True},
            ],
        }

    def assert_owned(self):
        for session in self.resources:
            with self.assertRaises(BusyError):
                with resource_guard(session_keys(session)):
                    pass

    def test_human_step_prepares_android_and_ios_then_observes_after_resume(self):
        run = self.runtime.create(self.workflow)
        state = self.runtime.run(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIn(("phone", "handoff"), self.trace)
        self.assertIn(("tablet", "handoff"), self.trace)
        self.assertNotIn("verified", state["outputs"])
        self.assert_owned()
        self.resources["phone"].frame = 1
        self.trace.clear()
        runtime = Runtime(self.store, self.runtime.factory)
        state = runtime.resume(run["id"], "Manual input completed on the test page")
        self.assertEqual(self.trace[:2], [("phone", "resume"), ("tablet", "resume")])
        self.assertEqual(state["observations"]["phone"]["frame"], 1)
        self.assertEqual(state["status"], "succeeded")
        self.assertTrue(state["outputs"]["verified"]["verified"])

    def test_requested_pause_prepares_every_visual_resource_and_retains_locks(self):
        run = self.runtime.create(self.workflow)
        self.store.request(run["id"], "pause")
        state = self.runtime.run(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(self.trace, [("phone", "handoff"), ("tablet", "handoff")])
        self.assertIsNone(self.store.control(run["id"]))
        self.assert_owned()

    def test_partial_handoff_failure_preserves_pause_cursor_and_ownership(self):
        self.resources["phone"].fail = "handoff"
        run = self.runtime.create(self.workflow)
        state = self.runtime.run(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIn("phone handoff failed", state["error"])
        self.assertIn(("tablet", "handoff"), self.trace)
        self.assertEqual(state["cursor"], 0)
        self.assertNotIn("verified", state["outputs"])
        self.assertEqual(self.store.get(run["id"])["error"], state["error"])
        self.assert_owned()

    def test_failed_handoff_capture_still_prepares_manual_input_on_every_device(self):
        self.resources["phone"].fail = "observe"
        run = self.runtime.create(self.workflow)
        state = self.runtime.run(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIn("phone observe failed", state["error"])
        self.assertEqual(self.trace, [("phone", "observe"), ("phone", "handoff"),
                                      ("tablet", "handoff")])
        self.assert_owned()

    def test_resume_failure_keeps_pause_and_requires_all_fresh_observations_on_retry(self):
        run = self.runtime.create(self.workflow)
        self.runtime.run(run["id"])
        self.resources["tablet"].fail = "resume"
        self.trace.clear()
        with self.assertRaisesRegex(RuntimeError, "tablet resume failed"):
            self.runtime.resume(run["id"], "Ready")
        state = self.store.get(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(state["observations"], {})
        self.assertIn("tablet resume failed", state["error"])
        self.assertNotIn("verified", state["outputs"])
        self.assertNotIn(("phone", "observe"), self.trace)
        self.assert_owned()
        self.resources["tablet"].fail = None
        self.trace.clear()
        state = Runtime(self.store, self.runtime.factory).resume(run["id"], "Ready again")
        self.assertEqual(state["status"], "succeeded")
        self.assertEqual(self.trace, [("phone", "resume"), ("tablet", "resume"),
                                      ("phone", "observe"), ("tablet", "observe")])

    def test_failed_resume_screenshot_does_not_advance_human_verification(self):
        run = self.runtime.create(self.workflow)
        self.runtime.run(run["id"])
        self.resources["tablet"].fail = "observe"
        with self.assertRaisesRegex(RuntimeError, "tablet observe failed"):
            self.runtime.resume(run["id"], "Ready")
        state = self.store.get(run["id"])
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(state["observations"], {})
        self.assertIn("tablet observe failed", state["error"])
        self.assertNotIn("verified", state["outputs"])
        self.assert_owned()

    def test_cancel_clears_only_handoffs_owned_by_this_workflow(self):
        run = self.runtime.create(self.workflow)
        self.runtime.run(run["id"])
        ds.save_state("phone", {"os": "android", "handoff": {"task": run["id"]}})
        ds.save_state("tablet", {"os": "ios", "handoff": {"task": "different-owner"}})
        self.runtime.cancel(run["id"])
        self.assertNotIn("handoff", ds.load_state("phone"))
        self.assertEqual(ds.load_state("tablet")["handoff"]["task"], "different-owner")

    def test_keyboard_preparation_failure_records_no_dispatch_and_does_not_replay(self):
        self.workflow["steps"] = [
            {"id": "before", "kind": "observe", "resource": "phone"},
            {"id": "input", "kind": "action", "resource": "phone",
             "observation": {"$ref": "steps.before"},
             "action": {"type": "input", "text": "Example input"}},
        ]
        resource = self.resources["phone"]
        resource.prepare = lambda action, observation: action
        resource.execute = Mock(side_effect=InputMethodError("Keyboard unavailable before input"))
        run = self.runtime.create(self.workflow)
        state = self.runtime.run(run["id"])
        self.assertEqual(state["status"], "failed")
        self.assertIsNone(state["pending"])
        self.assertEqual(state["observations"], {})
        event = next(event for event in self.store.events(run["id"])
                     if event["kind"] == "action_not_dispatched")
        self.assertFalse(event["data"]["dispatched"])
        resource.execute.assert_called_once()
        with self.assertRaisesRegex(ValueError, "failed"):
            self.runtime.run(run["id"])
        resource.execute.assert_called_once()


class VisualHandoffAdapterTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        state_patch = patch.object(ds, "STATE_DIR", Path(temporary.name) / "sessions")
        state_patch.start()
        self.addCleanup(state_patch.stop)

    def test_session_handoff_uses_common_device_implementation(self):
        resource = VisualResource({"kind": "android", "session": "phone"})
        with patch("saygo.devices.control._handoff", return_value={"status": "waiting_for_human"}) as handoff:
            resource.handoff("Use test input", "workflow-owner")
        args = handoff.call_args.args[0]
        self.assertEqual(args.session, "phone")
        self.assertEqual(args.instructions, "Use test input")
        self.assertEqual(args.task, "workflow-owner")

    def test_session_resume_rejects_unsuccessful_common_device_result(self):
        ds.save_state("tablet", {"os": "ios", "handoff": {"status": "waiting_for_human"}})
        resource = VisualResource({"kind": "ios", "session": "tablet"})
        with patch("saygo.devices.control._resume", return_value={"status": "waiting_for_human"}):
            with self.assertRaisesRegex(RuntimeError, "resume"):
                resource.resume("Ready")

    def test_old_workflow_without_session_marker_prepares_existing_controller(self):
        ds.save_state("phone", {"os": "android"})
        resource = VisualResource({"kind": "android", "session": "phone"})
        platform = Mock()
        with patch.object(resource, "_attach", return_value=platform), \
                patch("saygo.devices.control._resume") as resume:
            resource.resume("Ready")
        platform.prepare_resume.assert_called_once_with()
        resume.assert_not_called()

    def test_inline_desktop_handoff_does_not_create_or_activate_a_platform(self):
        resource = VisualResource({"kind": "windows", "app": "Example"})
        with patch.object(resource, "_attach") as attach:
            resource.handoff("Use test input", "workflow-owner")
            resource.resume("Ready")
        attach.assert_not_called()


if __name__ == "__main__":
    unittest.main()
