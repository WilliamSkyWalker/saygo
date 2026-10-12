"""Explicit whole-computer visual control, independent of application windows."""
import io
import platform
import subprocess

from .desktop import DesktopPlatform


class LocalDesktopPlatform(DesktopPlatform):
    def setup(self, config):
        self.kind = config['os']
        if platform.system() != {'windows': 'Windows', 'mac': 'Darwin'}[self.kind]:
            raise RuntimeError('本机桌面控制需要在 Windows 或 macOS 原生运行 Saygo')
        if self.kind == 'windows':
            from .desktop_win import DesktopWinPlatform
            DesktopWinPlatform._set_dpi_aware(self)
            import win32gui
            self._w32 = win32gui
        else:
            import Quartz
            import AppKit
            self._Q, self._AK = Quartz, AppKit
            if not Quartz.CGPreflightScreenCaptureAccess() or not Quartz.AXIsProcessTrusted():
                raise RuntimeError('请在系统设置 → 隐私与安全性中，为 Saygo 开启屏幕录制和辅助功能权限，然后重新连接')
            self.paste_modifier = 'command'
        import pyautogui
        self._pg = pyautogui
        self._bounds()
        self.connection = {'scope': 'computer'}

    def _bounds(self):
        if self.kind == 'windows':
            import ctypes
            user = ctypes.windll.user32
            bounds = [user.GetSystemMetrics(i) for i in (76, 77, 78, 79)]
        else:
            error, displays, count = self._Q.CGGetActiveDisplayList(32, None, None)
            if error or not count:
                raise RuntimeError('无法读取显示器布局')
            rects = [self._Q.CGDisplayBounds(d) for d in displays[:count]]
            x = min(r.origin.x for r in rects); y = min(r.origin.y for r in rects)
            bounds = [x, y, max(r.origin.x+r.size.width for r in rects)-x,
                      max(r.origin.y+r.size.height for r in rects)-y]
        self._win_x, self._win_y, self._win_w, self._win_h = map(int, bounds)
        return list(map(int, bounds))

    def observation_metadata(self):
        bounds = self._bounds()
        if self.kind == 'windows':
            import win32process
            window = self._w32.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(window)[1] if window else 0
        else:
            front = self._AK.NSWorkspace.sharedWorkspace().frontmostApplication()
            pid = int(front.processIdentifier()) if front else 0
            windows = self._Q.CGWindowListCopyWindowInfo(self._Q.kCGWindowListOptionOnScreenOnly, 0)
            window = next((w['kCGWindowNumber'] for w in windows or []
                           if w.get('kCGWindowOwnerPID') == pid and w.get('kCGWindowLayer') == 0), 0)
        return {'window_id': str(window), 'process_id': pid, 'window_bounds': bounds,
                'capture_mode': 'computer', 'desktop_scope': 'computer'}

    def _validate_window(self, expected):
        current = self.observation_metadata()
        if any(current.get(k) != v for k, v in expected.items()):
            raise RuntimeError('桌面焦点或显示器布局已改变，请重新观察')

    def screenshot_raw(self):
        before = self.observation_metadata()
        x, y, w, h = before['window_bounds']
        if self.kind == 'windows':
            from PIL import ImageGrab
            image = ImageGrab.grab(bbox=(x, y, x+w, y+h), all_screens=True)
            out = io.BytesIO(); image.save(out, format='PNG'); png = out.getvalue()
        else:
            Q = self._Q
            image = Q.CGWindowListCreateImage(Q.CGRectMake(x, y, w, h), Q.kCGWindowListOptionOnScreenOnly,
                                            Q.kCGNullWindowID, Q.kCGWindowImageDefault)
            if image is None:
                raise RuntimeError('无法截取桌面，请检查屏幕录制权限')
            rep = self._AK.NSBitmapImageRep.alloc().initWithCGImage_(image)
            png = bytes(rep.representationUsingType_properties_(self._AK.NSBitmapImageFileTypePNG, None))
        self._validate_window({k: before[k] for k in ('window_id', 'process_id', 'window_bounds')})
        return png

    def _to_global(self, x, y):
        return self._win_x + int(x), self._win_y + int(y)

    def _set_clipboard(self, text):
        if self.kind == 'windows':
            from .desktop_win import DesktopWinPlatform
            DesktopWinPlatform._set_clipboard(self, text)
        else:
            subprocess.run(['/usr/bin/pbcopy'], input=text.encode('utf-8'), check=True, timeout=5)

    def prepare_application_launch(self, target, observation):
        from saygo.devices.applications import installed_applications
        from saygo.platforms import device_session as ds
        state = ds.load_state(observation.get('session')) or {}
        if (state.get('desktop_scope') != 'computer' or state.get('os') != self.kind
                or state.get('disconnected') or state.get('handoff')
                or observation.get('target', {}).get('desktop_scope') != 'computer'):
            raise ValueError('Computer binding changed; reconnect and observe again')
        if target not in {item['target'] for item in installed_applications()}:
            raise ValueError('Application is not in the installed application catalog; refresh discovery')
        # Launching a named app does not depend on pixels or foreground focus.
        self._expected_window = None
        self._prepared_launch = target

    def open_target(self, target):
        if getattr(self, '_prepared_launch', None) != target:
            self._check_window()
        self._prepared_launch = None
        if self.kind == 'windows':
            import os
            os.startfile(target)
        else:
            from urllib.parse import urlsplit
            command = ['open', target] if urlsplit(target).scheme in {'http', 'https'} or target.endswith('.app') else ['open', '-a', target]
            subprocess.run(command, check=True, timeout=15)

    def teardown(self):
        self._pg = None

    @property
    def platform_name(self):
        return self.kind

    def get_system_prompt_segment(self):
        return '截图为本机完整桌面；可打开应用、切换窗口并操作系统。坐标相对整个截图。'
