"""Durable device requests sharing the task/workflow ownership registry."""
import hashlib
import json
import time
import uuid

from saygo.runtime.locking import registry, release, reserve, resource_guard


def _store():
    store = registry()
    with store.connect() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS device_requests (
                id TEXT PRIMARY KEY, session TEXT NOT NULL, request_id TEXT NOT NULL,
                signature TEXT NOT NULL, resource_keys TEXT NOT NULL, started REAL NOT NULL,
                result TEXT, resolution TEXT
            );
            CREATE TABLE IF NOT EXISTS observation_floors (key TEXT PRIMARY KEY, at REAL NOT NULL);
        ''')
    return store


def identity(session, request_id):
    if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 200:
        raise ValueError('request_id must be a nonempty string of at most 200 characters')
    return hashlib.sha256(json.dumps([session or 'default', request_id]).encode()).hexdigest()[:32]


def _floor(db, keys, at):
    for key in keys:
        db.execute('INSERT INTO observation_floors(key,at) VALUES (?,?) '
                   'ON CONFLICT(key) DO UPDATE SET at=max(at,excluded.at)', (key, at))


def validate_observation(observation, keys):
    with _store().connect() as db:
        for key in keys:
            row = db.execute('SELECT at FROM observation_floors WHERE key=?', (key,)).fetchone()
            if row and observation['at'] <= row[0]:
                raise ValueError('Observation predates an action or review; observe again')


def review_owner(keys):
    """Allow observation of an uncertain operation, never input or task takeover."""
    owners = set()
    with _store().connect() as db:
        for key in keys:
            row = db.execute('SELECT run_id FROM resources WHERE key=?', (key,)).fetchone()
            if row:
                owners.add(row[0])
    if len(owners) == 1 and next(iter(owners)).startswith('operation:'):
        return next(iter(owners))
    return None


def run(session, request_id, payload, keys, callback):
    request_id = uuid.uuid4().hex if request_id is None else request_id
    operation_id = identity(session, request_id)
    owner = 'operation:' + operation_id
    signature = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    store = _store()
    with resource_guard(keys, owner=owner):
        with store.connect() as db:
            row = db.execute('SELECT signature,result,resolution FROM device_requests WHERE id=?',
                             (operation_id,)).fetchone()
        if row:
            if row[0] != signature:
                raise ValueError('request_id already used with different arguments')
            result = json.loads(row[1]) if row[1] else {
                'ok': False, 'outcome': 'uncertain', 'requires_observation': True,
                'error': 'Previous request was interrupted; inspect and resolve, never replay',
                'operation_id': operation_id, 'request_id': request_id, 'session': session}
            if row[2] or result.get('outcome') != 'uncertain':
                release(owner)
            return result
        started = time.time()
        with store.connect() as db:
            db.execute('INSERT INTO device_requests VALUES (?,?,?,?,?,?,NULL,NULL)',
                       (operation_id, session or 'default', request_id, signature, json.dumps(keys), started))
        reserve(owner, keys)
        try:
            result = callback(operation_id)
        except Exception as exc:
            result = {'ok': False, 'error': str(exc), 'error_type': type(exc).__name__,
                      'outcome': 'uncertain', 'requires_observation': True}
        result.update(operation_id=operation_id, request_id=request_id, session=session or 'default')
        with store.connect() as db:
            db.execute('UPDATE device_requests SET result=? WHERE id=?', (json.dumps(result), operation_id))
            if result.get('dispatched') or result.get('outcome') == 'uncertain':
                _floor(db, keys, started)
        if result.get('outcome') != 'uncertain':
            release(owner)
        return result


def resolve(session, request_id, resolution, note):
    if resolution not in {'applied', 'not_applied'} or not isinstance(note, str) or not note.strip():
        raise ValueError('resolve requires applied/not_applied and a review note')
    operation_id = identity(session, request_id)
    store = _store()
    with store.connect() as db:
        row = db.execute('SELECT resource_keys,result,resolution FROM device_requests WHERE id=?',
                         (operation_id,)).fetchone()
    if not row:
        raise ValueError('Unknown request_id for this session')
    keys = json.loads(row[0])
    owner = 'operation:' + operation_id
    with resource_guard(keys, owner=owner):
        if row[1] and json.loads(row[1]).get('outcome') != 'uncertain':
            raise ValueError('Only an uncertain request requires resolution')
        if not row[2]:
            with store.connect() as db:
                db.execute('UPDATE device_requests SET resolution=? WHERE id=?',
                           (json.dumps({'outcome': resolution, 'note': note, 'at': time.time()}), operation_id))
                _floor(db, keys, time.time())
        release(owner)
    return {'ok': True, 'operation_id': operation_id, 'request_id': request_id,
            'resolved': True, 'requires_observation': True, 'business_success': None}


def list_operations(session=None):
    with _store().connect() as db:
        rows = db.execute('SELECT id,session,request_id,started,result,resolution FROM device_requests '
                          + ('WHERE session=? ' if session else '') + 'ORDER BY started DESC LIMIT 100',
                          (session,) if session else ()).fetchall()
    return {'ok': True, 'operations': [
        {'operation_id': row[0], 'session': row[1], 'request_id': row[2], 'at': row[3],
         'outcome': (json.loads(row[4]).get('outcome', 'completed') if row[4] else 'uncertain'),
         'resolved': bool(row[5])} for row in rows]}
