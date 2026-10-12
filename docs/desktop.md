# Saygo Desktop (first development build)

Saygo Desktop uses **Qt 6 Widgets + PySide6 (Python)**. Qt is the UI framework;
Python is the implementation language. This directly reuses the existing control
service and durable InteractiveRuntime. It does not depend on pyenv. Packaged users
do not install Python, pip or a programming Agent.

## Technology choice

| Choice | Fit for this repository |
|---|---|
| Qt + PySide6 | Native desktop widgets; one Python codebase; direct Runtime reuse. Chosen for the first version. |
| Tauri + web UI | Attractive web UI ecosystem; also needs Rust and a separately packaged Python sidecar for each architecture. |
| pywebview | Python-friendly HTML shell; adds web assets and platform-specific webview deployment to maintain. |

References: [Qt for Python](https://doc.qt.io/qtforpython-6),
[Tauri sidecars](https://v2.tauri.app/develop/sidecar/),
[pywebview packaging](https://pywebview.flowrl.com/guide/freezing).

## Start from source (developers)

```sh
python3 -m pip install '.[desktop]'
saygo-desktop
```

No pyenv is required. An isolated environment is optional for development. On
Windows add the `windows` extra; on macOS add `mac` to install input drivers. Mobile
dependencies remain optional. WSL can run the Linux GUI through WSLg; the intended
Windows distribution is a native Windows build.

## User flow

The main window is a conversation: recent tasks live in the left sidebar,
messages and progress appear in the center, and the composer stays at the bottom.
Open model settings and device connections from the sidebar. Enter sends a task;
Shift+Enter inserts a newline. During human handoff, reply in the composer to
continue the current task. Uncertain actions still require explicit review.
The latest device screenshot is available through the observation button.

The welcome screen provides model setup, device connection, and a sample-task
entry point; selecting the sample only fills the composer and never starts a task.
Model settings support masked/revealable API Tokens, input validation, and inline
save/test results. Closing the settings dialog masks the Token again. Connection
tests send a generated image and may incur provider charges. Editing configuration
invalidates the displayed test feedback. Deleting a stored Token clears the input
only after the credential-store operation succeeds. Unchecking secure storage does
not delete credentials saved previously; use the explicit delete action for that.

1. Enter an OpenAI-compatible API base URL, vision model name and API Key. Test
   image input. HTTP is allowed only for local loopback endpoints; remote providers
   must use HTTPS. The client never automatically retries a model request.
2. Choose session-only credentials or the OS credential store. Keys never enter
   `desktop.json`, task records or exported reports. If a secure keyring backend
   is unavailable, uncheck Remember and use a session-only key. Other provider
   settings live under `SAYGO_HOME_DIR` or `~/.saygo`.
3. The native Windows/macOS app automatically connects the whole computer.
   For browser control, click Connect Chrome / Install extension. This registers
   the store extension's local bridge and opens its Chrome Web Store page. Install
   the extension and click Connect local bridge in its popup; the desktop app
   detects the connection. Named windows and mobile sessions remain in Advanced.
4. The computer and connected browser are selected by default. Describe the task;
   the model receives launchable application entries, screenshots and browser tab
   metadata and chooses the resource and application. You can deselect targets.
   Operations retain percent coordinates, action validation, resource locks,
   durable dispatch intent and record export.
5. Pause for human control, resume with a note, or stop. Pause/stop waits for the
   current API/device call to return and blocks the next dispatch; it cannot undo
   input already sent. A model request has a 30-second timeout and a run is capped
   at 30 steps before handoff. An uncertain action stops automatic execution.
6. Reopen the app, load the task and re-observe. Resolve uncertain actions manually
   with evidence before continuing. No automatic action replay happens at startup.

Completion is a model judgement based on screenshots, recorded as agent evidence;
it is not an independent business-system assertion. Screenshots, launchable application entries and task text are
sent to the configured model provider. The first build does not implement native
Anthropic/Gemini API formats (use an OpenAI-compatible endpoint), streaming chat,
automatic updates, signed installers or a graphical mobile toolchain wizard.

## Build for distribution

```sh
python3 -m pip install pyinstaller
python3 scripts/build_desktop.py
python3 scripts/package_desktop.py
```

Build on each target OS; do not rename a Linux executable to `.exe`. Outputs are
in `dist/desktop/SaygoDesktop` (macOS also produces an `.app`). Distribute the whole
folder, not just the executable. Qt, Python and extension assets are included.
Windows uses a windowed `SaygoDesktop.exe` and a separate `SaygoNativeHost.exe`
for Chrome native messaging over stdio. Keep both executables and `_internal`
together. Opening the desktop app does not open a console window.

`package_desktop.py` creates a verified DMG with an Applications shortcut on macOS,
a ZIP containing the executable and dependencies on Windows, and tar.gz on Linux.
Each archive has a SHA256 checksum. Output is in `dist/installers`.

The manual desktop workflow builds Windows/macOS/Linux artifacts. This does not
sign or notarize them. Before public distribution, include dependency license
notices, test fresh machines and package/sign per platform. Qt's license choices
and obligations still apply; see the official Qt documentation.

## Verification boundary

Linux/WSL: Qt offscreen startup, screenshot rendering, core pause/recovery tests
and local standalone packaging are checked during development.
Windows x64: a native Python 3.13 build passed 32 desktop tests including chat
interaction and connection tests. Automatic local connection, full-desktop capture
and launchable application discovery passed native checks. The frozen GUI passed visible Qt startup; PE headers confirm
a windowed GUI and a separate console host, which passed the native-messaging handshake. A
portable ZIP was produced. Clean-machine installation and live task execution
remain unverified. Windows users do not need WSL, Python or pyenv.
macOS: the DMG packaging script and CI workflow are prepared, but no macOS build
or runtime test has been performed yet. DMG support is not yet validated.
The app can run on Linux, but Linux local-window automation is not implemented by
the current Saygo drivers; browser extension and supported mobile paths remain
available. A live provider task needs a user-supplied model and connected test app.


### 自动连接与本机操作

桌面版在原生 Windows / macOS 启动后自动连接“本机电脑”，默认允许操作整个桌面，
不需要填写窗口标题。开始任务时 Saygo 自动最小化，避免遮挡操作画面；需要人工接管或
本轮结束时恢复窗口。运行期间可从任务栏恢复 Saygo，点击暂停或停止。
macOS 需要在系统设置中授予屏幕录制和辅助功能权限，再点击“重新检测本机”。

模型获得本机可启动应用的名称和入口：Windows 扫描开始菜单快捷方式及 Get-StartApps，
macOS 扫描系统及用户应用目录。此清单不包含所有便携程序，也不读取应用内容。
模型可选择打开应用、操作系统桌面，以及切换已连接浏览器的标签页。
截图和应用清单会发送给用户配置的模型服务。

“设备与连接 → 连接 Chrome / 安装扩展”会注册本地桥并打开 Chrome 网上应用店的
Saygo Browser 页面。安装扩展后，在扩展中点击 Connect local bridge；桌面版自动检测
连接并加入浏览器目标。应用店安装仍需要用户确认；桥在线但没有网页时提示打开网页。
检测不会激活标签页；任务执行及人工接管期间不会自动更换绑定。
用户可以在“选择操作目标”中取消本次任务不需要的电脑或浏览器。
窗口级及手机连接保留在“高级连接”中。

全桌面模式还可以通过 `saygo device connect --platform desktop --session local-computer --desktop-scope computer`
显式创建，和原有窗口会话共用本地桌面资源锁。此模式要求原生 Windows 或 macOS，
不会把 WSL 自动当作本机桌面。

本机任务首先观察电脑；已连接浏览器作为可用资源提供给模型，只有模型请求使用时才加入
截图循环，避免无关的休眠标签页阻塞本机操作。通过应用清单启动程序时，校验清单入口和
本机绑定，保留 durable intent，不要求桌面像素或焦点保持不变。启动后仍需重新截图验证。
点击、输入和其他依赖当前画面的操作继续使用原有的观察有效期、目标及画面变化校验。
