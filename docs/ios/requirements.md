# iOS 操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

初始核对日期：2026-10-12；本次修复状态更新：2026-10-13。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围包含 iPhone/iPad 真机、Xcode iOS 模拟器与远程 Mac 上的 Appium。当前有代码和模拟测试，不将 macOS 桌面通过或 Android 通过算作 iOS 真机通过。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 发现与安装 | [saygo/devices/mobile.py](../../saygo/devices/mobile.py) |
| 主机 | [saygo/devices/mobile_host.py](../../saygo/devices/mobile_host.py) |
| 工具链 | [saygo/devices/toolchain.py](../../saygo/devices/toolchain.py) |
| 驱动 | [saygo/platforms/appium.py](../../saygo/platforms/appium.py) |
| 服务器 | [saygo/platforms/appium_server.py](../../saygo/platforms/appium_server.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 模拟器辅助 | [saygo/devices/simulator.py](../../saygo/devices/simulator.py) |
| 帧流 | [saygo/platforms/mjpeg.py](../../saygo/platforms/mjpeg.py) |

## 主机、发现与连接

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| IOS-001 | 本地发现、安装、启动依赖 macOS 和完整 Xcode，单独命令行工具不足；Windows/Linux/WSL 只能连接远程服务。 | 发现与安装.require_mac；主机.select_host | 已有实现；真机链待验收 |
| IOS-002 | 模拟器发现返回名称、UDID、运行时、启动状态，只列可用 iOS 模拟器；未启动的设备不能直接自动选为在线。 | 发现与安装.ios_simulators | 已有实现；模拟测试 |
| IOS-003 | 真机发现使用 devicectl，返回 UDID、配对、连接状态和开发者模式；只把已配对且在线候选列为可连接。 | 发现与安装.ios_physical | 已有实现；真实设备待验收 |
| IOS-004 | 本地只有一个在线候选才自动选中；多个模拟器/真机时要求明确设备 ID，发现错误给诊断。 | 发现与安装.discover/connect | 已有实现 |
| IOS-005 | 连接前由用户完成信任、开发者模式、解锁和权限，不绕过系统确认；状态文件不能证明设备可交互。 | 发现与安装.connect；会话.attach | 环境前提；需要真实响应验收 |
| IOS-006 | 会话保存设备、服务地址、平台与 Appium ID，拒绝覆盖其他设备/服务器，远程连接必须显式 UDID。 | 发现与安装.connect；会话.start | 已有实现 |
| IOS-007 | 远程服务由 Mac 负责 USB、Xcode、签名和模拟器；客户端不安装远端工具、不自动开放服务端口。 | `device connect --server-url` | 已有实现 |
| IOS-008 | 默认连接不清数据，统一 connect 未指定 bundle 时附着当前状态；显式配置 bundle/launch 属于另一种应用选择。 | 驱动.setup；发现与安装.connect | 已有实现 |

## 签名、工具链与模拟器

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| IOS-009 | XCUITest 使用 WDA；真机签名可传 team ID、签名身份、WDA bundle ID，真实值留在私有配置。 | 驱动.setup；工具链.setup_ios_wda | 已有实现；真实签名待验收 |
| IOS-010 | 有 team 配置时支持 Xcode provisioning 更新/设备注册；账号、开发列表与钥匙串仍须有效，不承诺无条件自动签成功。 | 驱动.setup 的 iOS capabilities | 已有实现；外部前提待验收 |
| IOS-011 | 工具初始化安装/复用 Node、Appium、XCUITest，保留 skip-ios 和指定设备能力；驱动安装失败向调用方报错。 | `saygo mcp init`；工具链.install_drivers/setup_ios_wda | 已有实现 |
| IOS-012 | 安装预检提供组件、路径和空间，dry-run 不执行 Xcode 下载/安装；不能选择 Windows 本地主机安装 iOS。 | 主机.plan/select_host/execute | 已有实现 |
| IOS-013 | 模拟器安装调用 Xcode 首次初始化并下载 iOS 运行时；不代装 Xcode、登录 Apple 账号或隐式通过管理员许可。 | 发现与安装.install_ios | 已有实现；完整安装待验收 |
| IOS-014 | 从可用运行时选最新版本，使用运行时支持的 iPhone 类型；同名同运行时复用，多候选要求显式 UDID。 | 发现与安装.install_ios | 已有实现 |
| IOS-015 | boot 使用唯一名称/UDID，已 Booted 时复用，等待 simctl bootstatus；默认显示模拟器，headless 不打开 Simulator 界面。 | 发现与安装.boot_device | 已有实现 |
| IOS-016 | connect 隐含启动并在连接后保存实际截图；超时或签名失败必须明确失败，不更换设备。 | 主机.execute；发现与安装.provision_runtime | 已有实现；模拟测试 |
| IOS-017 | 现有模拟器辅助代码可安装 .app、启动、截图和关闭模拟器；应与统一视觉动作和 Android APK 安装接口区分。 | 模拟器辅助；MCP setup_simulator | 兼容辅助入口；不构成完整 iOS 应用分发 |

## 观察与输入

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| IOS-018 | 截图优先可用新鲜 MJPEG 帧，否则回落 Appium PNG；保留 Retina 比例、逻辑尺寸和旋转后的映射。 | 驱动.screenshot_raw/_note_screenshot_size/scale；帧流 | 已修复帧龄与断流失效；真机待验收 |
| IOS-019 | 多设备帧流端口不能冲突，远程端口不通不阻断普通截图；普通 device 重连目前不自动恢复 MJPEG。 | 驱动._pick_mjpeg_port；会话._platform_from_driver | 部分路径支持帧流 |
| IOS-020 | 支持坐标单击和长按，统一 act 长按 0.1–30 秒；实际行为由设备 Appium 触摸链验证。 | 驱动.tap/long_press；devices/actions | 已有实现；真机待验收 |
| IOS-021 | 支持起止坐标滑动和可配置 duration_ms；不把触摸链中的停留时间承诺为精确手指移动时间。 | 驱动._w3c_swipe；devices/service | 已有实现；手势时序待设备验收 |
| IOS-022 | 上下滚动使用中央触摸手势；scroll_up 朝内容顶部，手指上→下；scroll_down 朝内容底部，手指下→上。 | 驱动.scroll_up/scroll_down | 已统一方向；iOS 真机待验收 |
| IOS-023 | 文字写入当前聚焦元素，支持中文；输入前须通过截图确认焦点，不向模型返回元素树。 | 驱动.input_text | 已有实现；实际键盘/控件待验收 |
| IOS-024 | 输入超时且是否生效未知时先核对，不可改用 mobile:keys 自动重复派发。 | 驱动.input_text | 已修复：send_keys 异常后停止，模拟测试仅派发一次 |
| IOS-025 | 按键仅提供 home、enter、delete；Home 调系统按钮、Enter 输入换行、Delete 向焦点元素发退格，其他名称明确拒绝。 | 驱动.press_key | 已有实现；Delete 焦点查找需真机验证 |
| IOS-026 | iOS 返回动作应点可见返回按钮或做返回手势，不提供 Android back/recent/power 或桌面组合键。 | 驱动.press_key；iOS 提示协议 | 当前不支持这些系统键 |
| IOS-027 | 打开应用通过 bundle ID 激活；relaunch 可终止再激活，Android pm_clear 不应宣称为 iOS 清数据。 | 驱动.open_target/reset_app | 已有实现；iOS 未实现清数据重置 |
| IOS-028 | 本端不提供通用 open_url/deeplink、hover、双击、右键、定点滚轮、hotkey 或多指缩放承诺。 | 驱动方法集；devices/actions.BASE | 已修复：能力表不再包含 open_url |
| IOS-029 | 锁屏、休眠、拔线或受保护内容导致截图失败时报告不可用；iOS 键盘检测返回 false 不能证明键盘已关闭。 | 驱动.screenshot_raw/is_ime_visible | 环境限制；键盘检测未实现 |

## 会话、任务与验收

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| IOS-030 | 短命令退出保留 Appium session；探活失败要求重新 connect/start，不能暗中切到 Android 或别的设备。 | 会话.attach/start/release_controller | 已有实现 |
| IOS-031 | disconnect 结束 Appium 会话并保留断开配置，stop 清除绑定；不默认关闭模拟器或删除设备数据。 | devices/control._disconnect；会话.stop | 已有实现 |
| IOS-032 | 任务与普通设备共享锁、观察、接管和不确定结果恢复；resume 必须新截图，不能等同登录成功。 | runtime/interactive；devices/control | 已有实现；真实跨端待验收 |
| IOS-033 | QA 可按 @ios 标签执行场景并保留截图证据；平台标签只筛选，不自动调度 iOS 与 Android 双端。 | qa/gherkin；qa/execution | 已有实现；模型与设备任务待验收 |
| IOS-034 | 分别验证真机签名、模拟器首装/复用、远程连接、中文输入/删除/手势、旋转、断连与任务恢复；缺设备即标待验收。 | `tests/mobile_demo`、`docs/common/testing/acceptance.feature` | 尚无完整 iOS 硬件验收证据 |

## 验收范围

离线入口：[移动设备测试](../../tests/mobile_demo/test_mobile.py)、[安装测试](../../tests/mobile_demo/test_provision.py)、[主机测试](../../tests/mobile_demo/test_hosts.py)、[共享动作测试](../../tests/control_demo/test_agent_service.py)。真机和完整 Xcode 配置链仍待验收，见[操作指南](README.md#验收与待办)。iOS 每项硬件验收须单列，不能从共享驱动或模拟响应推导通过。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。

本轮源码修复与迁移、六端分别验证的范围见[修复记录](../common/requirements-audit.md#升级与兼容性)。未更新用户安装或发布版本。
