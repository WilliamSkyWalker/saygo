"""Offline task handoff contracts using isolated bindings and fake resources."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from saygo.platforms import device_session as ds
from saygo.platforms.android_ime import InputMethodError
from saygo.runtime.interactive import InteractiveRuntime
from saygo.runtime.locking import resource_guard, session_keys
from saygo.runtime.resources import VisualResource
from saygo.runtime.store import BusyError, Store


class TaskResource(VisualResource):
    def __init__(self, name, trace):
        super().__init__({"session": name, "kind": "android" if name == "phone" else "ios"})
        self.name = name
        self.trace = trace
        self.fail = False
        self.frame = 0
        self.input_error = None
        self.manual_keyboard = True

    def _attach(self):
        return self

    def prepare_resume(self):
        self.trace.append((self.name, "prepare_resume"))
        self.manual_keyboard = True

    def prepare(self, action, observation):
        return action

    def execute(self, action):
        self.trace.append((self.name, "execute"))
        if self.input_error:
            raise self.input_error
        return {"dispatched": True}

    def observe(self):
        self.trace.append((self.name, "observe"))
        if self.fail:
            raise RuntimeError(f"{self.name} capture failed")
        return b"local test image", {"frame": self.frame, "screen_size": [100, 200]}

    def close(self):
        pass


class InteractiveHandoffTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        state_patch = patch.object(ds, "STATE_DIR", self.root / "sessions")
        state_patch.start()
        self.addCleanup(state_patch.stop)
        self.trace = []
        self.resources = {name: TaskResource(name, self.trace) for name in ("phone", "tablet")}
        for name, kind in (("phone", "android"), ("tablet", "ios")):
            ds.save_state(name, {"os": kind, "device_id": "test-" + name})
        self.store = Store(self.root / "runtime")
        self.runtime = InteractiveRuntime(self.store, lambda spec: self.resources[spec["session"]])
        self.task = self.runtime.create_task({"phone": "phone", "tablet": "tablet"})
        self.task_id = self.task["id"]
        self.fail_handoff = None
        self.fail_resume = None
        handoff_patch = patch("saygo.devices.control._handoff", side_effect=self.handoff)
        resume_patch = patch("saygo.devices.control._resume", side_effect=self.resume)
        self.handoff_mock = handoff_patch.start()
        self.resume_mock = resume_patch.start()
        self.addCleanup(handoff_patch.stop)
        self.addCleanup(resume_patch.stop)

    def handoff(self, args):
        self.trace.append((args.session, "handoff"))
        checkpoint = self.store.get(self.task_id)
        self.assertEqual(checkpoint["status"], "waiting_for_human")
        self.assertEqual(checkpoint["observations"], {})
        self.assertEqual(args.task, self.task_id)
        self.assertIsNone(args.input_method)
        state = ds.load_state(args.session)
        state["handoff"] = {"status": "waiting_for_human", "task": args.task,
                            "instructions": args.instructions}
        ds.save_state(args.session, state)
        if self.fail_handoff == args.session:
            raise RuntimeError(f"{args.session} manual keyboard unavailable")
        return {"session": args.session, **state["handoff"]}

    def resume(self, args):
        self.trace.append((args.session, "resume"))
        if self.fail_resume == args.session:
            raise RuntimeError(f"{args.session} keyboard resume failed")
        state = ds.load_state(args.session)
        state.pop("handoff")
        ds.save_state(args.session, state)
        return {"session": args.session, "status": "needs_observation"}

    def assert_owned(self):
        for session in self.resources:
            with self.assertRaises(BusyError):
                with resource_guard(session_keys(session)):
                    pass

    def test_task_handoff_prepares_all_platforms_through_common_device_lifecycle(self):
        self.runtime.observe(self.task_id, "phone")
        state = self.runtime.handoff_task(self.task_id, "Use the local test input page")
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(state["observations"], {})
        self.assertEqual(self.trace[-2:], [("phone", "handoff"), ("tablet", "handoff")])
        self.assertEqual(self.handoff_mock.call_count, 2)
        self.assert_owned()

    def test_failed_handoff_still_prepares_other_devices_and_can_be_retried(self):
        self.fail_handoff = "phone"
        with self.assertRaisesRegex(RuntimeError, "phone manual keyboard unavailable"):
            self.runtime.handoff_task(self.task_id, "Use test input")
        state = self.store.get(self.task_id)
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIn("phone manual keyboard unavailable", state["error"])
        self.assertEqual(self.trace, [("phone", "handoff"), ("tablet", "handoff")])
        self.assert_owned()
        self.fail_handoff = None
        state = self.runtime.handoff_task(self.task_id, "Keyboard selected; retry")
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIsNone(state["error"])
        self.assertEqual(self.handoff_mock.call_count, 4)

    def test_repeated_handoff_retains_ownership_and_uses_new_instructions(self):
        self.runtime.handoff_task(self.task_id, "First handoff")
        state = self.runtime.handoff_task(self.task_id, "Continue manual input")
        self.assertEqual(state["human"]["instructions"], "Continue manual input")
        self.assertEqual(self.handoff_mock.call_count, 4)
        self.assert_owned()

    def test_resume_rejects_non_success_status_from_device_lifecycle(self):
        self.runtime.handoff_task(self.task_id, "Use test input")
        self.resume_mock.side_effect = None
        self.resume_mock.return_value = {"status": "waiting_for_human", "reason": "keyboard_unavailable"}
        with self.assertRaisesRegex(RuntimeError, "resume"):
            self.runtime.resume_task(self.task_id, "Ready")
        state = self.store.get(self.task_id)
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertIn("resume", state["error"])
        self.assertEqual(state["observations"], {})
        self.assert_owned()

    def test_partial_resume_failure_preserves_pause_and_retry_observes_every_device(self):
        self.runtime.handoff_task(self.task_id, "Use test input")
        self.fail_resume = "tablet"
        self.trace.clear()
        with self.assertRaisesRegex(RuntimeError, "tablet keyboard resume failed"):
            self.runtime.resume_task(self.task_id, "Ready")
        state = self.store.get(self.task_id)
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(state["observations"], {})
        self.assertIn("tablet keyboard resume failed", state["error"])
        self.assert_owned()
        self.assertNotIn("handoff", ds.load_state("phone"))
        self.assertIn("handoff", ds.load_state("tablet"))
        self.resources["phone"].frame = 1
        self.resources["phone"].manual_keyboard = False
        self.fail_resume = None
        runtime = InteractiveRuntime(self.store, self.runtime.factory)
        state = runtime.resume_task(self.task_id, "Ready again")
        self.assertEqual(state["status"], "idle")
        self.assertIsNone(state["error"])
        self.assertEqual(set(state["observations"]), {"phone", "tablet"})
        self.assertEqual(state["observations"]["phone"]["frame"], 1)
        self.assertTrue(self.resources["phone"].manual_keyboard)
        self.assertIn(("phone", "prepare_resume"), self.trace)
        self.assertIsNone(self.store.events(self.task_id)[-1]["data"]["business_success"])

    def test_resume_screenshot_failure_clears_partial_observations_and_keeps_pause(self):
        self.runtime.handoff_task(self.task_id, "Use test input")
        self.resources["tablet"].fail = True
        with self.assertRaisesRegex(RuntimeError, "tablet capture failed"):
            self.runtime.resume_task(self.task_id, "Ready")
        state = self.store.get(self.task_id)
        self.assertEqual(state["status"], "waiting_for_human")
        self.assertEqual(state["observations"], {})
        self.assertIn("tablet capture failed", state["error"])
        self.assert_owned()

    def test_cancel_preserves_other_owners_handoff_and_does_not_resume_input(self):
        self.runtime.handoff_task(self.task_id, "Use test input")
        binding = ds.load_state("tablet")
        binding["handoff"]["task"] = "another-task"
        ds.save_state("tablet", binding)
        self.runtime.cancel_task(self.task_id, "End test")
        self.assertNotIn("handoff", ds.load_state("phone"))
        self.assertEqual(ds.load_state("tablet")["handoff"]["task"], "another-task")
        self.resume_mock.assert_not_called()

    def test_keyboard_preparation_failure_requires_new_observation_without_uncertain_input(self):
        state = self.runtime.observe(self.task_id, "phone")
        observation = state["observations"]["phone"]["id"]
        action = {"type": "input", "text": "Example input"}
        self.resources["phone"].input_error = InputMethodError("Keyboard unavailable before input")
        state = self.runtime.submit(self.task_id, "phone", action, observation, "request-one")
        self.assertEqual(state["status"], "idle")
        self.assertIsNone(state["pending"])
        self.assertEqual(state["observations"], {})
        event = next(event for event in self.store.events(self.task_id)
                     if event["kind"] == "action_not_dispatched")
        self.assertFalse(event["data"]["dispatched"])
        self.runtime.submit(self.task_id, "phone", action, observation, "request-one")
        self.assertEqual(self.trace.count(("phone", "execute")), 1)
        with self.assertRaisesRegex(ValueError, "latest observation"):
            self.runtime.submit(self.task_id, "phone", action, observation, "request-two")
        self.resources["phone"].input_error = None
        state = self.runtime.observe(self.task_id, "phone")
        state = self.runtime.submit(self.task_id, "phone", action,
                                    state["observations"]["phone"]["id"], "request-two")
        self.assertEqual(state["status"], "idle")
        self.assertEqual(self.trace.count(("phone", "execute")), 2)


if __name__ == "__main__":
    unittest.main()
