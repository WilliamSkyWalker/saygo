# 0219ef3：桌面连接、应用启动与交互改动说明

原提交：`0219ef3 desktop: add native computer connection and application launch workflow`。
本说明补充该提交的全部 19 个文件及修改目的。它描述已提交的桌面功能，不代表后续 bridge 共用缺陷已经在该提交中修复。

## 问题与目标

此前桌面版需要用户提前指定窗口和会话，模型缺少可启动应用信息；浏览器即使与任务无关也可能被纳入截图循环，休眠页面会阻塞本机任务。模型配置的错误反馈、Token 管理和首次使用入口也不够清晰。

这次改动让原生桌面客户端能接入整台电脑、发现应用、按任务需要使用浏览器，并加强配置反馈、任务恢复和启动动作的检查。

## 修改点及目的

| 文件 | 具体修改 | 目的 |
| --- | --- | --- |
| `saygo/desktop/app.py` | 增加欢迎页、模型/连接入口和只填入输入框的示例任务；任务区、侧栏和目标选择使用可读名称。 | 让首次使用步骤清晰，避免示例按钮直接执行任务。 |
| 同上：模型配置 | Token 默认遮罩，可临时显示，关闭对话框重新遮罩；校验地址和 Token，提供保存/测试/删除的内联反馈，修改配置清除旧测试反馈；删除成功后才清空输入。 | 防止误认为修改后的配置已通过测试，以及存储删除失败时丢失输入内容。 |
| 同上：连接 | 启动和定时检测本机/浏览器，连接工作在独立线程；任务及人工接管期间不自动重绑；保留高级窗口/手机连接。 | 减少手动配置，并防止后台检测改变正在执行任务的目标。 |
| 同上：任务窗口 | 全桌面任务开始时最小化 Saygo，执行结束或返回人工处理时恢复窗口；尊重目标取消选择，保存会话仅显示为已保存。 | 避免控制界面遮挡任务画面，也不把保存状态冒充在线状态。 |
| `saygo/desktop/theme.py` | 统一主窗口、对话框、欢迎页、输入框、按钮、提示及滚动条样式。 | 统一可读性、焦点状态和禁用状态。 |
| `saygo/desktop/model.py` | 去除服务地址首尾空白；分别解释 401、403、404、429、服务端错误和网络超时；错误不回显服务商响应体。 | 提供可处理的失败原因，避免错误文本泄露凭据。 |
| `saygo/desktop/connections.py` | 封装本机自动连接、真实 bridge 页面探测、浏览器绑定、安装 bridge 和打开 Chrome 商店入口。 | 将连接逻辑从界面中分离，便于复用和独立测试。此提交仍存在桌面/WSL 默认目录不一致，后续单独修复。 |
| `saygo/devices/applications.py` | Windows 读取开始菜单快捷方式与 Get-StartApps；macOS 遍历系统及用户应用目录；不进入应用包内部，不追踪目录软链接。 | 给模型提供可启动入口，减少猜测路径；这是启动清单，不是完整软件资产清单。 |
| `saygo/platforms/desktop_local.py` | 增加原生 Windows/macOS 全桌面驱动、显示器范围、截图、前台窗口身份验证、坐标换算和应用启动；检查 macOS 权限，拒绝将 WSL 当作原生桌面。 | 支持整台电脑操作，并对焦点或显示布局变化进行检查。 |
| `saygo/devices/control.py` | 增加 `--desktop-scope computer`；拒绝窗口绑定与全桌面绑定混用；支持初始浏览器观察绑定；读取会话显式使用 UTF-8。 | 持久化清晰的授权范围，处理中文会话，同时避免连接时激活标签页。 |
| `saygo/platforms/device_session.py` | 根据 `desktop_scope` 恢复全桌面驱动，拒绝冲突的前台/后台/窗口覆盖；初始化失败释放控制器；会话读取使用 UTF-8。 | 让跨进程恢复保留原始范围，并兼容 Windows 非 UTF-8 默认编码。 |
| `saygo/platforms/browser_extension.py` | 新增 `bind_page`，先核验页面存在，只保存选择，不发送激活页面动作。 | 允许桌面版建立初始观察绑定而不抢浏览器焦点。 |
| `saygo/devices/observations.py` | 截图目标元数据包含 `desktop_scope`。 | 后续动作能够判断截图对应整台电脑还是指定窗口。 |
| `saygo/devices/actions.py` | 应用目录启动交由驱动验证目标与绑定；坐标操作仍执行原来的观察有效期和画面验证。 | 命名应用启动不应依赖旧桌面像素，但点击输入必须继续依赖当前画面。 |
| `saygo/desktop/runner.py` | 提供可用资源和应用目录；添加 `observe` 决策，按需启用浏览器并保存选择；支持应用启动、页面选择等动作，更新模型反馈格式。 | 防止未使用的浏览器截图失败阻塞本机任务，支持重启后延续资源选择。 |
| `scripts/desktop_windows.spec` | 打包加入 Windows runner PowerShell 和无控制台启动辅助脚本。 | 避免源码环境可运行、冻结后的 Windows 包却缺运行资源。 |
| `tests/desktop_demo/test_chat_ui.py` | 测试欢迎入口、Token 遮罩与删除失败、配置反馈、目标选择及任务期间禁止自动重绑。 | 固定交互行为和凭据处理边界。 |
| `tests/desktop_demo/test_desktop.py` | 测试模型地址处理、HTTP/网络错误分类及敏感响应不回显。 | 验证新错误反馈不会引入凭据泄露。 |
| `tests/desktop_demo/test_connections.py` | 测试全桌面绑定及资源锁、窗口绑定冲突、bridge 在线探测、无激活页面绑定和应用清单。 | 验证连接服务的状态与范围契约；这些模拟测试不能替代真实浏览器验收。 |
| `tests/desktop_demo/test_launch.py` | 测试目录启动与像素/焦点无关、未知应用和绑定变化被拒绝、坐标操作仍拒绝过期观察、无关浏览器不截图。 | 仅放宽不依赖坐标的应用启动条件。 |
| `tests/desktop_demo/test_launch_runtime.py` | 通过持久任务运行时测试启动响应丢失不重放、暂停/停止、应用移除、浏览器按需观察及重启保留、中文状态读取。 | 覆盖实际运行时的故障恢复和状态持久化，而非仅检查函数返回。 |
| `docs/desktop.md` | 更新欢迎流程、Token 管理、自动连接、应用发现、目标选择、按需浏览器观察及平台验证边界。 | 使用户说明与新行为一致，并保留尚未验证项。 |

## 本次提交前重新执行的验证

- WSL：`/tmp/saygo-desktop-polish-env/bin/python -m unittest discover -s tests/desktop_demo -v`，45 项通过，Qt 使用 offscreen。
- Windows：原生 Python 3.13 在独立临时状态目录运行同一套 `tests/desktop_demo`，45 项通过，Qt 使用 offscreen。
- `tests/control_demo/test_control.py`：17 项通过。
- `tests/extension_demo/test_bridge.py`：14 项通过。
- `git diff --cached --check` 通过，提交已推送 `origin/main`。

上述 45 项桌面测试包含模拟设备/模型依赖和持久运行时测试，并不是 45 项真实桌面点击测试。本次没有重新执行 macOS、Android、iOS 的真实设备验收，没有发布新的 PyPI 包或桌面安装包。浏览器 bridge 共存缺陷不在本提交的修复范围内。
