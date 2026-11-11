"""Pause new MCP input for an explicit update choice; never install an update."""
import os
from pathlib import Path
import threading
import time

from saygo import updates

_LOCK = threading.Lock()
_STATES = {}
# Re-read installation/cache off the request thread; network checks retain the
# updater's 24-hour cache after the first forced check of this MCP process.
_POLL_SECONDS = 60


def _refresh(root, state, force):
    try:
        updates.check(root, force=force)
        info = updates.notice(root, refresh=False)
    except Exception as exc:
        info = {'automatic': False, 'error': 'Update check failed: ' + str(exc)}
    with _LOCK:
        # A temporary metadata failure is not evidence that a known update went
        # away. Keep an unanswered prompt until a successful comparison clears it.
        if info.get('error') and not info.get('current'):
            info = {**state['info'], **info}
        state.update(info=info, worker=None, next_poll=time.monotonic() + _POLL_SECONDS)


def status():
    """Return cached status immediately; all version/subprocess/network work is async."""
    configured = os.environ.get('SAYGO_INSTALL_ROOT')
    if not configured:
        return None
    root = Path(configured).expanduser().resolve()
    with _LOCK:
        state = _STATES.setdefault(str(root), {'info': {}, 'worker': None,
                                              'next_poll': 0, 'decision': None})
        if state['worker'] is None and time.monotonic() >= state['next_poll']:
            worker = threading.Thread(target=_refresh,
                                      args=(root, state, not bool(state['info'])),
                                      daemon=True, name='saygo-mcp-update-check')
            state['worker'] = worker
            try:
                worker.start()
            except Exception as exc:
                state.update(worker=None, next_poll=time.monotonic() + _POLL_SECONDS,
                             info={**state['info'], 'error': 'Cannot start update check: ' + str(exc)})
        info = dict(state['info'])
        if state['worker'] is not None:
            info['checking'] = True
        if state['decision']:
            info.update(decision=state['decision'], decision_scope='mcp_process')
        if info.get('available') and state['decision'] is None:
            info.update(requires_user_decision=True, choices=['upgrade', 'continue'],
                        guidance='Pause before the next business action and ask the user whether to '
                                 'upgrade or continue this session. Do not choose for the user. '
                                 'Record their choice with device_command update-decision, '
                                 'options={decision: upgrade|continue, version: available}.')
        if state['decision'] == 'upgrade':
            info['business_actions_paused'] = True
        return info


def decorate(result, info=None):
    """Surface a pending choice on read/results without changing an action's outcome."""
    info = status() if info is None else info
    if info and (info.get('requires_user_decision') or info.get('business_actions_paused')):
        return {**result, 'updates': info}
    return result


def before_action():
    info = status()
    if info and (info.get('requires_user_decision') or info.get('business_actions_paused')):
        pending = info.get('business_actions_paused', False)
        return {'ok': False, 'error_type': 'UpgradePending' if pending else 'UpdateDecisionRequired',
                'error': ('Upgrade selected; business actions remain paused until the Agent client restarts.'
                          if pending else 'Ask the user whether to upgrade Saygo or continue this session.'),
                'outcome': 'not_dispatched', 'dispatched': False, 'business_success': None,
                'requires_user_decision': not pending, 'updates': info}
    return None


def decide(decision, version):
    info = status()
    if decision not in {'upgrade', 'continue'}:
        return {'ok': False, 'error': 'decision must be upgrade or continue'}
    if not info or not info.get('available') or version != info['available']:
        return {'ok': False, 'error': 'Choice must name the currently reported available version',
                'updates': info}
    root = str(Path(os.environ['SAYGO_INSTALL_ROOT']).expanduser().resolve())
    with _LOCK:
        state = _STATES[root]
        if version != state['info'].get('available'):
            return {'ok': False, 'error': 'Available version changed; read update-status before choosing'}
        state['decision'] = decision
    return {'ok': True, 'decision': decision, 'decision_scope': 'mcp_process',
            'business_actions_paused': decision == 'upgrade', 'updates': status(),
            'message': ('Continue this MCP session without another update interruption.'
                        if decision == 'continue' else
                        'Business actions are paused. Follow the update instructions, then restart '
                        'the Agent client. No update has been installed by this choice.')}
