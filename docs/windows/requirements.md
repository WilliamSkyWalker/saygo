# Windows 操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

核对日期：2026-10-12。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围包含原生 Windows 窗口、WSL→Windows 窗口和原生整机控制。普通原生前台驱动、后台 runner、显式 `--foreground` runner 是不同路径，支持动作与剪贴板行为分别列出。RDP 为公共兼容功能，不算本端已通过的后台实现。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 连接 | [saygo/devices/control.py](../../saygo/devices/control.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 前台窗口 | [saygo/platforms/desktop_win.py](../../saygo/platforms/desktop_win.py) |
| 共用桌面 | [saygo/platforms/desktop.py](../../saygo/platforms/desktop.py) |
| runner | [saygo/platforms/windows_runner.py](../../saygo/platforms/windows_runner.py) |
| Win32 | [saygo/platforms/windows_runner.ps1](../../saygo/platforms/windows_runner.ps1) |
| 整机 | [saygo/platforms/desktop_local.py](../../saygo/platforms/desktop_local.py) |
| 操作服务 | [saygo/devices/service.py](../../saygo/devices/service.py) |
| 应用发现 | [saygo/devices/applications.py](../../saygo/devices/applications.py) |

## 发现、连接与生命周期

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| WIN-001 | 发现应用窗口时返回标题、进程名和 PID；发现失败给诊断，不据此宣称无窗口。 | `device list --platform windows`；连接.desktop_windows | 已有实现 |
| WIN-002 | 命名连接保存应用和进程身份；已有别名属于其他平台、应用或整机范围时拒绝覆盖。 | `device connect`；连接._connect | 已有实现 |
| WIN-003 | 连接优先复用应用进程，支持 `--process` 与 `--launch`；无进程才启动，隐藏或最小化窗口按连接策略恢复。 | Win32.Resolve-DesktopApp | 已有实现；恢复可能影响桌面 |
| WIN-004 | 应用已运行但没有可用窗口时进入人工接管，返回原因和指示，不能重复启动制造窗口。 | Win32.Resolve-DesktopApp；连接._connect | 已有实现 |
| WIN-005 | 只有明确 `--new-window`、启动程序及应用支持的参数才请求新窗口；验证新增窗口并清除一次性启动意图。 | 连接._connect；Win32.Resolve-DesktopApp | 已有实现；按应用验收 |
| WIN-006 | 原生 Windows 和 WSL 共用窗口解析规则；WSL 依赖 PowerShell 互操作，缺失时报错。 | 会话.attach_desktop；runner.setup | 已有实现 |
| WIN-007 | 普通命令释放临时控制器，不关闭被控应用；disconnect 保留配置并阻止隐式重连，stop 清除绑定。 | 会话.release_controller/stop；连接._disconnect | 已有实现 |
| WIN-008 | 整机模式只允许原生 Windows，拒绝 WSL 和同时指定 app/background；与窗口会话分别命名。 | `--desktop-scope computer`；整机.setup | 已有实现 |

## 截图、目标与坐标

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| WIN-009 | 前台窗口截图使用目标可见边界和物理像素；启用 DPI 感知，优先 DWM 边界以减少缩放及隐形边框偏差。 | 前台窗口._set_dpi_aware/_visible_bounds | 已有实现；多屏缩放需实测 |
| WIN-010 | 观察保存窗口 ID、PID、边界和图像映射；移动、缩放、进程退出或窗口身份变化后拒绝沿用旧观察。 | 前台窗口.observation_metadata；共用桌面.expect_window | 已有实现；带观察的动作路径 |
| WIN-011 | 前台输入前核对焦点与目标窗口，不能仅凭同样的截图把输入发给另一窗口。 | 前台窗口._validate_window；Win32.Assert-Foreground | 已有实现 |
| WIN-012 | 后台按 PrintWindow 捕获绑定窗口；失败或均匀图像报错，不自动切到全屏或前台截图。 | Win32.Capture-Window | 已有实现；GPU/自绘兼容有限 |
| WIN-013 | runner 大图缩至最大宽 1280，逻辑窗口尺寸保持原值，调用方通过映射换算坐标。 | runner._shrink/screen_size | 已有实现 |
| WIN-014 | 整机捕获覆盖虚拟桌面与负坐标显示器，保存前台窗口/PID/显示布局；捕获期间布局或焦点改变报错。 | 整机._bounds/screenshot_raw | 已有实现；多显示器待分场景验收 |
| WIN-015 | 诊断读取可用窗口、排除原因与截图失败线索；任务修复仅选同进程合格窗口，不能借修复重放业务输入。 | `device diagnose`、`task diagnose/repair` | 已有实现 |

## 前台操作

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| WIN-016 | 普通原生前台支持单击、双击、右键、悬停、长按和鼠标拖动；坐标相对窗口或整机观察。 | 共用桌面.tap/double_click/right_click/hover/long_press/swipe | 已有实现 |
| WIN-017 | 普通前台文字输入支持 Unicode 剪贴板粘贴；剪贴板失败只允许 ASCII 键入回退，非 ASCII 失败必须报告。 | 共用桌面.input_text；前台窗口._set_clipboard | 已有实现；会改变剪贴板 |
| WIN-018 | 普通前台支持已映射按键和合法组合键；非法键名拒绝，优先用可见按钮。 | 共用桌面.press_key/hotkey | 已有实现 |
| WIN-019 | 普通前台支持滚轮上下滚动和定点滚动；普通滚动沿用当前指针位置，定点滚动先移动指针，不能承诺固定像素位移。 | 共用桌面.scroll_up/scroll_down/scroll_at | 已有实现；小数幅度会取整 |
| WIN-020 | 显式 `focus` 或 `--foreground` 使用 runner 恢复并前置目标，只影响本次调用，不改保存的后台偏好。 | 操作服务._execute；会话.attach_desktop | 已有实现 |
| WIN-021 | 显式前台 runner 点击必须确认目标点未被其他窗口覆盖；文字通过 Unicode 输入事件，不使用剪贴板。 | Win32 的 tap/input 分支 | 已有实现；真实应用待验收 |
| WIN-022 | 显式前台 runner 的可用动作按自身能力公布，不能把普通原生驱动的双击、悬停、定点滚动等直接套用。 | runner 方法集；devices/actions.capabilities | 部分能力；未实现这些可选方法 |

## 后台操作

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| WIN-023 | 后台模式必须显式选择；不使用全局鼠标、键盘、剪贴板，不因失败自动改成前台模式。 | `--background`；Win32 后台分支 | 已有实现；应用仍可能自行激活 |
| WIN-024 | 后台单击标准 Edit 时按坐标确定字段和插入点；标准或 WinForms 按钮使用所属原生动作，其余控件按窗口消息处理。 | Win32 的 tap 分支 | 已有实现；需逐控件验收 |
| WIN-025 | 后台输入前先点击目标；跨进程保存输入控件绑定并复核句柄、进程、窗口和控件类，失效时不能猜测别的输入框。 | runner._call；会话.attach_desktop；Win32.Get-InputTarget | 已有实现 |
| WIN-026 | 后台 Unicode 输入、拖动和上下滚动使用定向消息；消息派发不等于控件处理完成，应截图确认。 | Win32 的 input/swipe/scroll 分支 | 已有实现；自绘控件可能忽略 |
| WIN-027 | 后台 `Ctrl+A` 只用于 Edit/RichEdit 选择全文，其他修饰键组合明确拒绝；普通按键限定 runner 键表。 | Win32 的 key 分支 | 已有实现 |
| WIN-028 | 后台能力不宣称支持 hover、double_click、right_click、long_press、scroll_at 或独立 hotkey 动作；不可从其他端继承支持承诺。 | runner 方法集；devices/actions.capabilities | 当前不支持这些可选动作 |
| WIN-029 | 后台窗口最小化、受保护或无法捕获时提供诊断/接管，不声称支持锁屏、任意隐藏窗口或 GPU 应用。 | Win32.Refresh-TargetWindow/Capture-Window | 部分能力；应用兼容待验收 |

## 复合操作、任务与交付

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| WIN-030 | `type-send --prepare-only` 只聚焦、可选全选、输入并截图；不提交，缺发送坐标时只有草稿模式可继续。 | 操作服务 type-send 分支 | 已有实现 |
| WIN-031 | 明确提交的 type-send 保存是否尝试发送；截图失败或结果未知不得重复发送，submitted 不能表示送达。 | 操作服务._execute | 已有实现；复合动作不具逐动作观察保障 |
| WIN-032 | 窗口/整机使用同一桌面资源锁；任务和人工接管期间阻止其他 Saygo 操作，不能阻止用户改变焦点。 | runtime/locking.session_keys；连接.handoff/resume | 已有实现 |
| WIN-033 | 恢复接管必须获取新截图；窗口关闭、进程退出或不确定输入分别处理，不能用重连替代结果核对。 | 连接._resume；runtime/interactive | 已有实现 |
| WIN-034 | 整机任务可发现本机应用，启动前验证清单和整机绑定；启动不依赖旧像素，随后必须重新观察。 | 应用发现.installed_applications；整机.prepare_application_launch | 已有实现 |
| WIN-035 | Windows 桌面包保留 GUI、独立 native host 和资源目录，无需 Python/WSL；运行冻结包与用户真实任务分别验收。 | `scripts/build_desktop.py`、`scripts/package_desktop.py` | 历史包证据；真实模型任务待验收 |
| WIN-036 | 完整验收覆盖原生/WSL、普通前台/显式前台/后台/整机、DPI、多窗口、焦点竞争、进程退出和重复连接。 | `tests/control_demo`、`tests/desktop_demo` | 局部历史实测；组合未全部验收 |

## 验收范围

回归入口：[窗口控制](../../tests/control_demo/test_desktop.py)、[显式前台命令](../../tests/control_demo/test_foreground_cli.py)、[独立 Windows 窗口实测](../../tests/control_demo/test_background_live.py)、[桌面产品测试](../../tests/desktop_demo/)。历史隔离窗口、整机截图/应用发现、三平台冻结包的范围见[操作指南](README.md#验收与限制)和[0.4.16 记录](../common/history/release-0.4.16.md)。这些证据不涵盖所有 Windows 应用。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。
