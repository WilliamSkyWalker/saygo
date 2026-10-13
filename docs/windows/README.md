# Windows 操作

[文档入口](../README.md) · [本端完整需求](requirements.md) · [统一操作](../common/operations.md)

## 需求与前提

本端负责原生 Windows 及 WSL 到 Windows 的窗口操作，适用 NATIVE-001～004、SESSION、OBS、TASK；整机模式与桌面产品还适用 GUI。完整编号见[需求基线](../common/requirements.md#native)。

原生 Python 环境按需安装 `windows` 扩展依赖；WSL 使用 PowerShell/Win32 runner。原生桌面安装包不要求 Python、WSL 或 pyenv，运行时须保留整个解压目录中的 `SaygoDesktop.exe`、`SaygoNativeHost.exe` 和 `_internal`。模型设置及桌面交互见[桌面应用](../common/desktop-app.md)。

## 连接窗口或整台电脑

```sh
saygo device list --platform windows
saygo device connect --platform windows --app 'Example App' --session win-test
saygo device capabilities --session win-test
saygo device screenshot --session win-test
```

窗口连接支持应用名或窗口标题子串。原生 Windows 与 WSL 共用按进程解析的连接逻辑：优先复用进程，恢复已有隐藏/最小化窗口，仅在没有匹配进程时启动。已运行但无可访问窗口返回 `waiting_for_human`，不反复拉起。连接返回进程/窗口身份及 `launched/restored`，不代表登录已完成。

应用显示名、窗口标题和进程名不一致时可显式指定：

```powershell
saygo device connect --platform windows --app Example --process Example --launch 'C:\Example\Example.exe' --session win-test
```

本地化应用名尽可能通过开始菜单元数据解析。显式新窗口请求使用 `--new-window`、`--launch` 和应用支持的 `--new-window-arg=VALUE`；缺参数先拒绝，只尝试一次并验证确实出现新窗口。启动新进程不等于新增窗口，后续截图不会重放启动请求。

整机模式仅在原生 Windows/macOS 可用：

```sh
saygo device connect --platform desktop --desktop-scope computer --session local-computer
```

WSL 不会被视为原生本机桌面。窗口与整机绑定不能混用；所有本地桌面资源共用操作锁。连接、截图和输入可能改变前台焦点，须按所选模式理解。

## 后台操作

后台模式为实验功能，显式指定 `--background`：

```sh
saygo device connect --platform windows --app 'Example App' --session win-bg --background
saygo device screenshot --session win-bg
saygo device act '{"type":"tap","x":50,"y":40,"coordinate_space":"percent"}' --session win-bg --observation-id OBSERVATION_ID --observe-after
saygo device input '测试文字' --session win-bg --observation-id AFTER_TAP_OBSERVATION_ID --request-id input-001
```

原生 Windows 后台与 WSL 都使用 PowerShell/Win32 runner，通过 PrintWindow 截图和窗口定向控件操作，不注入全局鼠标、键盘或剪贴板。缺 PowerShell、窗口关闭或截图不可用时报错，不自动切换前台或整屏截图。

标准 Edit 控件按坐标放置光标而不设置 OS 焦点；标准/WinForms 按钮通过窗口所属的原生可访问动作执行。其他控件使用窗口消息，应用可能忽略消息或自行激活。GPU、自绘应用尤其需要单独验收，派发成功不等于画面变化。最小化窗口可能需要恢复，后台模式不等于无界面或锁屏控制。

输入前先点击目标字段。会话跨进程保存控件绑定，重连校验窗口/进程/类归属；失效时拒绝猜测其他输入框。句柄可能复用，界面变化后须重新观察并点击。Ctrl+A 仅支持 Edit/RichEdit；其他修饰键快捷键明确拒绝，使用可见按钮或人工接管。

## 显式前台操作

自绘应用无法可靠后台控制时，可在已授权前台操作的前提下显式使用 `--foreground`。它只影响本条命令，不改变保存的后台偏好。

```sh
saygo device focus --session win-bg --out /tmp/window.png
# 先填写并检查草稿，不点击发送。
saygo device type-send '测试消息' --session win-bg --foreground --replace --prepare-only --input-x 400 --input-y 620 --out /tmp/draft.png --observation-id FOCUS_OBSERVATION_ID --request-id draft-001
# 按新截图确认目标与草稿后，使用真实坐标提交并核验。
saygo device tap 800 690 --session win-bg --foreground --out /tmp/result.png --observation-id DRAFT_OBSERVATION_ID --request-id submit-001
```

上述坐标仅为格式示例；Windows 原生终端将 `/tmp` 换成可写的 Windows 路径。`--replace` 先选中输入字段内容。没有 `--prepare-only` 时，type-send 必须有发送坐标，在同一控制器连接内完成授权提交。

结果中的 `submitted/requires_observation` 只代表派发与截图，不是送达证明。尝试提交后出错会携带 `submission_attempted: true`，须先观察，不能重复发送。

前台动作派发前核对窗口位于前台，拒绝被覆盖的点击点；Unicode 输入不改变剪贴板，但会移动鼠标/焦点。截图为实际可见像素，可能包含覆盖物。后台失败不会自动触发前台回退，Saygo 也不绕过调用方或 OS 的审批。

## 接管与恢复

```sh
saygo device handoff --session win-test --reason login --instructions '请在现有窗口完成登录'
saygo device resume --session win-test --note '用户已完成登录'
saygo device diagnose --session win-test
```

接管期间动作和重连均被阻止；resume 必须成功获取新图后解除暂停，返回 `needs_observation`。窗口元数据不能判断登录是否完成。任务内使用所属任务的接管、诊断和修复接口，详见[统一操作](../common/operations.md)。

## 验收与限制

```sh
python3 -m unittest discover -s tests/control_demo -p test_desktop.py -v
SAYGO_TEST_WINDOWS=1 python3 -m unittest discover -s tests/control_demo -p test_background_live.py -v
```

真实后台测试创建独立测试窗口和遮挡窗口，检查遮挡截图、两个文本字段、Unicode、按钮、坐标、跨进程绑定、无效目标及不激活目标。设置 `SAYGO_TEST_WINDOWS_IDLE=1` 时还断言前台、鼠标和剪贴板不变，需要桌面无人操作。前台测试仅在显式 `SAYGO_TEST_WINDOWS_FOREGROUND=1` 时运行。

历史 WSL 隔离窗口后台操作已有实测；前台替换输入路径在原记录中仍待最新实测。原生 Windows 的 Qt 测试、整机截图/应用清单检查及冻结包检查见 [0.4.16 验收](../common/history/release-0.4.16.md)，不能当成任意应用、干净机器安装或完整模型业务任务通过。

后台捕获的候选改进与许可证约束见[后台研究](background-research.md)，研究方案不等于已实现能力。Windows/WSL 控制浏览器应阅读[扩展端](../browser-extension/README.md)；Android 模拟器应阅读 [Android](../android/README.md)。
