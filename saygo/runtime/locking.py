"""Global resource ownership and OS locks shared by all execution entrances."""
from contextlib import contextmanager, ExitStack
import hashlib
import threading
from saygo.platforms import device_session as ds
from .store import Store, BusyError

_held = threading.local()


@contextmanager
def _resource_lock(store, key, allow_nested=False):
    """A QA case may call the shared dispatcher while holding its resource lock."""
    held = getattr(_held, 'keys', None)
    if held is None:
        held = _held.keys = {}
    token = (str(store.root), key)
    if held.get(token):
        yield
        return
    with store.guard(hashlib.sha256(key.encode()).hexdigest()[:32]):
        held[token] = allow_nested
        try:
            yield
        finally:
            del held[token]


def registry():
    return Store(ds.STATE_DIR.parent / "control-locks")


def reserve(owner, keys):
    registry().reserve(owner, keys)


def release(owner):
    with registry().connect() as db:
        db.execute("DELETE FROM resources WHERE run_id=?", (owner,))


@contextmanager
def resource_guard(keys, owner=None, *, allow_nested=False):
    locks = registry()
    keys = sorted(set(keys))
    with ExitStack() as stack:
        for key in keys:
            stack.enter_context(_resource_lock(locks, key, allow_nested))
        with locks.connect() as db:
            for key in keys:
                row = db.execute("SELECT run_id FROM resources WHERE key=?", (key,)).fetchone()
                if row and row[0] != owner:
                    if row[0].startswith('operation:'):
                        raise BusyError(f"resource {key} has an uncertain operation {row[0][10:]}; inspect device operations and resolve before input")
                    if row[0].startswith("human:"):
                        raise BusyError(f"resource {key} is waiting for human control; resume session {row[0][6:]}")
                    raise BusyError(f"resource {key} is owned by task/workflow {row[0]}; use that task or finish/cancel it first")
        yield


def session_keys(session, state=None):
    state = state if state is not None else ds.load_state(session) or {}
    keys = ["device-session:" + ds._key(session)]
    if state.get("kind") == "desktop":
        keys.append("desktop:local")
    if state.get("device_id"):
        keys.append("mobile:" + state["device_id"])
    if state.get("browser_backend") == "extension":
        from pathlib import Path
        keys.append("browser-extension:" + str(Path(state["bridge_directory"]).resolve()))
    if state.get("debugger_address"):
        keys.append("browser:" + state["debugger_address"])
    return keys
