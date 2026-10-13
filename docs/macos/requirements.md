# macOS 操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

核对日期：2026-10-12。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围包含 macOS 前台窗口、原生整机和实验性原生后台控制。后台是应用内的原生控件动作与定向键盘输入，不能当作任意应用都支持的后台鼠标。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 连接 | [saygo/devices/control.py](../../saygo/devices/control.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 前台 | [saygo/platforms/desktop_mac.py](../../saygo/platforms/desktop_mac.py) |
| 共用桌面 | [saygo/platforms/desktop.py](../../saygo/platforms/desktop.py) |
| 后台 | [saygo/platforms/desktop_mac_background.py](../../saygo/platforms/desktop_mac_background.py) |
| 整机 | [saygo/platforms/desktop_local.py](../../saygo/platforms/desktop_local.py) |
| 应用发现 | [saygo/devices/applications.py](../../saygo/devices/applications.py) |

## 发现、权限与连接

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| MAC-001 | 发现当前桌面的应用窗口，返回应用名、标题、PID、窗口 ID 和边界，供显式选择。 | 连接.desktop_windows | 已有实现 |
| MAC-002 | 本地控制要求 macOS 和所需 PyObjC/Quartz 依赖；屏幕录制、辅助功能权限授予实际运行进程，缺权限要说明。 | 前台.setup；后台.setup/validate_action；整机.setup | 已有实现；前台部分错误由系统接口返回 |
| MAC-003 | 前台窗口连接按应用名打开/激活应用并等候窗口，超时明确失败；不能宣称此模式不影响用户焦点。 | 前台.setup/_open_app | 已有实现 |
| MAC-004 | 前台命名会话重连应保持明确窗口与进程；当前按应用名重新取最大窗口，不能声称跨进程窗口身份固定。 | 前台._find_window；会话.attach_desktop | 缺口：前台多窗口/重启可能重新选窗 |
| MAC-005 | 后台连接只绑定已打开且位于当前桌面的窗口，禁止启动、激活或恢复最小化应用。 | 后台.setup/_windows/_ensure_frontmost | 已有实现 |
| MAC-006 | 后台多候选要求 `--window-id`，保存后台标志、PID、窗口 ID；重连找不到原窗口必须报错。 | 连接._connect；后台._find_window/connection | 已有实现 |
| MAC-007 | 整机模式仅原生 macOS，不能与 app/background 混合；与窗口模式使用不同会话。 | 连接._connect；整机.setup | 已有实现 |
| MAC-008 | 断开与退出临时控制器不关闭被控应用；断开后需显式重连，stop 只清设备绑定。 | 连接._disconnect；会话.release_controller/stop | 已有实现 |

## 截图与坐标

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| MAC-009 | 窗口截图包含真实图像尺寸、逻辑点尺寸和比例，Retina 与多屏负坐标经映射处理。 | 前台.screenshot_raw/scale/_to_global | 已有实现；多显示器组合待验收 |
| MAC-010 | 前台截图可能激活应用；每次刷新窗口边界，输入前比较窗口 ID、PID、边界和前台窗口。 | 前台._validate_window/screenshot_raw | 已有实现；不补足重连选窗缺口 |
| MAC-011 | 后台截图不激活目标；缺屏幕录制权限、锁屏、不活跃控制台、最小化/非当前桌面时报错。 | 后台.screenshot_raw/_require_unlocked/_windows | 已有实现 |
| MAC-012 | 后台原生控件必须能唯一映射到已观察窗口；同边界的多个原生窗口、错进程或错窗口拒绝。 | 后台._check_native_window | 已有实现 |
| MAC-013 | 整机截图覆盖活动显示器联合区域，前台应用/窗口或显示布局变化使旧观察失效。 | 整机._bounds/observation_metadata/screenshot_raw | 已有实现；真实组合待验收 |
| MAC-014 | 截图失败返回诊断与失败原因，不以旧图冒充当前图；后台失败不自动改前台。 | devices/diagnostics；后台.diagnose；desktop/runner | 已有实现 |

## 前台操作

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| MAC-015 | 前台窗口与整机支持单击、双击、右键、悬停、长按和拖动；全局输入会影响用户鼠标焦点。 | 共用桌面的指针方法 | 已有实现 |
| MAC-016 | 前台 Unicode 输入使用系统剪贴板和 Command+V；失败仅可回退 ASCII 键入，不能把后台无剪贴板保证套到此路径。 | 前台._set_clipboard；共用桌面.input_text | 已有实现 |
| MAC-017 | 前台支持映射的普通键和合法组合键；非法键名拒绝，Command 与 Control 不可混淆。 | 共用桌面.press_key/hotkey；前台.paste_modifier | 已有实现 |
| MAC-018 | 前台上下滚动作用于当前指针区域，定点滚动先定位指针；滚动量取整数，需截图核验方向和位移。 | 共用桌面.scroll_up/scroll_down/scroll_at | 已有实现 |
| MAC-019 | 前台/整机可打开应用；整机任务应优先使用已发现且验证的应用入口，不能让后台会话借此启动应用。 | 前台.open_target；整机.open_target/prepare_application_launch | 已有实现 |

## 后台原生操作

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| MAC-020 | 后台只公布 tap、right_click、input、press_key、scroll_at、scroll_up、scroll_down，不暴露继承的全局输入方法。 | 后台.ACTIONS/supported_actions | 已有实现 |
| MAC-021 | 后台点击按截图坐标在绑定应用命中控件，再执行 AXPress；目标没有原生动作时拒绝，不改用全局点击。 | 后台._native_target/_click | 已有实现；原生控件限定 |
| MAC-022 | 后台右键要求 AXShowMenu；仅按坐标命中与归属校验，不向模型提供 UI 树或控件文字定位。 | 后台.right_click/_native_target | 已有实现；原生控件限定 |
| MAC-023 | 后台输入只允许最多 4096 个可打印字符，拒绝控制字符和无效代理项，按完整 Unicode 字符分块派发。 | 后台.validate_action/input_text | 已有实现 |
| MAC-024 | 后台输入和按键要求恰好一个合格应用窗口，已有焦点控件属于绑定窗口，不主动改变系统焦点。 | 后台.validate_action/_check_native_window | 已有实现 |
| MAC-025 | 后台支持 Enter、Tab、Space、Delete/Backspace、Escape、Home/End、PageUp/PageDown 和方向键；修饰键/快捷键拒绝。 | 后台.KEYS/press_key | 已有实现 |
| MAC-026 | 后台键盘定向到进程和窗口，使用私有事件源；不用全局事件、剪贴板、光标跳转或自动重试。 | 后台._source/_target/_post | 已有实现；应用可忽略事件 |
| MAC-027 | 后台定点滚动只找原生垂直滚动条，有限跟随命中控件的祖先，禁止全树搜索或全局滚轮回退。 | 后台._native_scrollbar | 已有实现 |
| MAC-028 | 后台滚动幅度须为 [-100,100] 整数，正上负下；优先原生增减动作，可写归一化值回退每步 0.05 并夹紧。 | 后台.scroll_at/capability_details | 已有实现；不承诺像素位移 |
| MAC-029 | 后台上下滚动默认在窗口中心执行 5 步；无合格原生滚动区明确失败。 | 后台.scroll_up/scroll_down | 已有实现 |
| MAC-030 | 后台明确拒绝拖动、悬停、双击、长按、组合键、启动应用和打开 URL，包括直接调用旧方法的路径。 | 后台._unsupported 绑定 | 当前不支持；已有拒绝保护 |
| MAC-031 | 原生超时或派发中前台/鼠标改变必须标为结果不确定；不能自动重试、恢复焦点或报告业务完成。 | 后台._click/_post/scroll_at；共享操作服务 | 已有实现 |
| MAC-032 | 后台锁屏、其他 Space、隐藏/最小化、无法确定身份的窗口不属于承诺支持范围；自绘控件单独验收。 | 后台._require_unlocked/_windows/_check_native_window | 支持边界；不可推广到任意应用 |

## 任务、恢复与交付

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| MAC-033 | macOS 窗口与整机共用本地桌面输入锁；handoff 暂停操作，resume 获取新截图后才能继续业务核验。 | runtime/locking；连接.handoff/resume | 已有实现 |
| MAC-034 | 诊断展示权限、窗口可用性、前台 PID、指针与输入方式；不能仅据能力字段认定拥有输入权限。 | 后台.diagnose；commands/doctor | 已有实现 |
| MAC-035 | 整机应用发现用于启动与任务规划；用户截图及任务内容发送到所配置视觉模型，凭据规则继承公共 GUI 需求。 | 应用发现；desktop/model；desktop/runner | 已有实现；真实模型任务待验收 |
| MAC-036 | macOS 安装包区分架构、冻结启动、权限、签名、公证；已有 arm64 包证据不能代替 Intel 包和用户权限验收。 | `scripts/build_desktop.py`、`scripts/package_desktop.py` | 历史 arm64 包证据；签名/公证待完成 |
| MAC-037 | 验收覆盖前台/后台/整机、Retina、多窗口、焦点竞争、权限撤销和重连；原生测试面板通过不能代表全部应用。 | `tests/mac_demo`、`tests/desktop_demo` | 局部实测；其余待真实验收 |

## 验收范围

现有入口：[后台契约测试](../../tests/control_demo/test_mac_background.py)、[原生面板实测](../../tests/mac_demo/test_background_live.py)、[桌面产品测试](../../tests/desktop_demo/)。历史 Intel Mac 原生面板点击、输入、滚动及 CLI/MCP 实测范围见[操作指南](README.md#验收)；arm64 冻结包见[0.4.16](../common/history/release-0.4.16.md)。前台固定窗口恢复缺口不能因后台面板通过而标为完成。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。
