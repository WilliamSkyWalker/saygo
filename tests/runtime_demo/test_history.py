"""Offline history and export contracts using an isolated SQLite store."""

from contextlib import contextmanager
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from saygo.runtime.interactive import InteractiveRuntime
from saygo.runtime.store import Store


class HistoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root / "runtime")
        self.state = self.store.create({"resources": {}, "steps": []}, mode="interactive")
        self.run_id = self.state["id"]
        self.runtime = InteractiveRuntime(self.store)

    def test_events_preserve_order_and_data_without_loading_snapshot(self):
        self.store.save(self.state, "agent_annotation", {"note": "已核对结果", "business_success": None})
        other = self.store.create({"resources": {}, "steps": []})
        self.store.save(other, "unrelated", {"note": "another run"})
        self.store.save(self.state, "action_resolved", {"outcome": "not_executed"})
        statements = []
        connect = self.store.connect

        @contextmanager
        def traced_connection():
            with connect() as db:
                db.set_trace_callback(statements.append)
                yield db

        with patch.object(self.store, "connect", side_effect=traced_connection) as connections:
            events = self.store.events(self.run_id)

        self.assertEqual([event["kind"] for event in events],
                         ["created", "agent_annotation", "action_resolved"])
        self.assertEqual(events[1]["data"], {"note": "已核对结果", "business_success": None})
        self.assertEqual(events[2]["data"], {"outcome": "not_executed"})
        self.assertEqual([event["seq"] for event in events], sorted(event["seq"] for event in events))
        self.assertTrue(all(isinstance(event["at"], float) for event in events))
        self.assertEqual(connections.call_count, 1)
        self.assertFalse(any("snapshot" in statement.lower() for statement in statements))

    def test_events_distinguish_missing_run_from_empty_history(self):
        with self.store.connect() as db:
            db.execute("DELETE FROM events WHERE run_id=?", (self.run_id,))
        self.assertEqual(self.store.events(self.run_id), [])
        with self.assertRaisesRegex(ValueError, "^unknown run: missing$"):
            self.store.events("missing")

    def test_export_reuses_one_history_for_events_and_timeline(self):
        self.state.update(status="needs_review", pending={"id": "pending-action"})
        self.store.save(self.state, "action_dispatching", {
            "step": "first", "resource": "phone", "action": {"type": "tap", "x_pct": 50},
        })
        self.store.save(self.state, "agent_annotation", {"step": "first", "note": "Awaiting review"})
        directory = self.store.root / "artifacts" / self.run_id
        directory.mkdir(parents=True)
        (directory / "observation.png").write_bytes(b"test artifact")
        (directory / "unrelated.txt").write_text("not an observation")

        with patch.object(self.store, "events", wraps=self.store.events) as read_events:
            result = self.runtime.export(self.run_id, self.root / "evidence.zip")

        with zipfile.ZipFile(result["path"]) as archive:
            self.assertEqual(set(archive.namelist()), {
                "task.json", "events.json", "timeline.json", "artifacts/observation.png",
            })
            self.assertEqual(json.loads(archive.read("task.json")), self.state)
            self.assertEqual(archive.read("artifacts/observation.png"), b"test artifact")
            events = json.loads(archive.read("events.json"))
            timeline = json.loads(archive.read("timeline.json"))

        expected = [{key: event[key] for key in ("seq", "at", "kind")} for event in events]
        expected[1].update(step="first", resource="phone", action="tap")
        expected[2].update(step="first", note="Awaiting review")
        self.assertEqual(timeline, {"task_id": self.run_id, "timeline": expected})
        self.assertEqual(self.runtime.timeline(self.run_id), timeline)
        read_events.assert_called_once_with(self.run_id)


if __name__ == "__main__":
    unittest.main()
