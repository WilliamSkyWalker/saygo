"""QA adapters use shared observation checks, resource locks and durable input records."""
from contextlib import contextmanager
import time
import uuid

from saygo.devices import observations, requests, service
from saygo.platforms.base import ActionOutcomeUnknown, Platform
from saygo.runtime.locking import resource_guard


def resource_keys(config):
    kind = config.get('platform', 'ios')
    if kind in {'mac', 'macos', 'windows', 'win', 'desktop'}:
        return ['desktop:local']
    if kind in {'android', 'ios', 'appium'}:
        device = (config.get('appium') or {}).get('device')
        if not device:
            raise ValueError('QA mobile execution requires an explicit APPIUM_DEVICE to lock the physical device')
        return ['mobile:' + str(device)]
    if kind == 'rdp':
        return ['rdp:' + str((config.get('rdp') or {}).get('host', 'default'))]
    # QA Selenium creates its own session; unrelated Grid sessions remain independent.
    return ['qa-browser:' + uuid.uuid4().hex]


class QAPlatform:
    def __init__(self, platform, keys):
        self.raw = platform
        self.keys = keys
        self.session = 'qa-' + uuid.uuid4().hex
        self.observation = None
        self.uncertain = None
        self.last_operation = None

    def __getattr__(self, name):
        return getattr(self.raw, name)

    @contextmanager
    def case_guard(self):
        self._check_review()
        with resource_guard(self.keys, allow_nested=True):
            yield

    def _check_review(self):
        if self.uncertain:
            raise ActionOutcomeUnknown(self.uncertain)

    def screenshot_raw(self):
        with resource_guard(self.keys, owner=requests.review_owner(self.keys) if self.uncertain else None):
            png = self.raw.screenshot_raw()
            self.observation = observations.save(self.raw, png, self.session)
            return png

    def screenshot_png(self):
        return self.screenshot_raw()

    def screenshot_burst(self, count=3, interval=.25):
        return Platform.screenshot_burst(self, count, interval)

    def _execute(self, action, dispatch=None):
        self._check_review()
        result = service.execute_observed(self.raw, self.session, action, self.observation,
                                          self.keys, dispatch=dispatch)
        self.last_operation = result
        if result.get('outcome') == 'uncertain':
            self.uncertain = (f"QA input outcome unknown; inspect evidence {result.get('record')} then "
                              f"device resolve --session {self.session} --request-id {result['request_id']} "
                              '--resolution applied|not_applied --note REVIEW_NOTE')
            raise ActionOutcomeUnknown(self.uncertain)
        if not result.get('ok'):
            raise ValueError(result.get('error', 'QA input rejected'))
        self.observation = result.get('observation')
        return result

    def execute_action(self, action):
        action = dict(action)
        if action.get('type') == 'wait':
            self._check_review()
            time.sleep(max(0, min(float(action.get('seconds', 2)), 5)))
            return
        action['type'] = {'swipe_up': 'scroll_up', 'swipe_down': 'scroll_down'}.get(action.get('type'), action.get('type'))
        if action['type'] == 'open_app':
            action['target'] = action.get('target') or action.get('package') or action.get('bundle_id')
        # Brain has already converted its percentage coordinates to logical pixels.
        if 'x' in action or 'x1' in action:
            action = {k: v for k, v in action.items() if not k.endswith('_pct')}
            action['coordinate_space'] = 'screen'
        return self._execute(action)

    def tap(self, x, y): return self.execute_action({'type': 'tap', 'x': x, 'y': y})
    def input_text(self, text): return self.execute_action({'type': 'input', 'text': text})
    def press_key(self, key): return self.execute_action({'type': 'press_key', 'key': key})
    def scroll_up(self): return self.execute_action({'type': 'scroll_up'})
    def scroll_down(self): return self.execute_action({'type': 'scroll_down'})
    def swipe(self, x1, y1, x2, y2):
        return self.execute_action({'type': 'swipe', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

    def open_target(self, target):
        self.screenshot_raw()
        return self.execute_action({'type': 'open_url', 'url': target} if self.platform_name == 'browser'
                                   else {'type': 'open_app', 'target': target})

    def reset_app(self, target, mode):
        self.screenshot_raw()
        return self._execute({'type': 'open_app', 'target': target, 'reset_mode': mode},
                             dispatch=lambda _: self.raw.reset_app(target, mode))

    def prepare_browser_case(self, target):
        self.screenshot_raw()
        def reset(_action):
            driver = self.raw._driver
            driver.delete_all_cookies()
            driver.execute_script('window.localStorage.clear(); window.sessionStorage.clear();')
            self.raw.open_target(target)
        return self._execute({'type': 'open_url', 'url': target,
                              'qa_reset': {'cookies': True, 'storage': True}}, dispatch=reset)

    def teardown(self):
        # Uncertain input must remain inspectable; do not close its browser/phone session.
        if not self.uncertain:
            with resource_guard(self.keys):
                self.raw.teardown()
