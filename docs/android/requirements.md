# Android 操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

初始核对日期：2026-10-12；本次修复状态更新：2026-10-13。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围包含 Android 真机、Android 模拟器、本地主机、WSL→Windows 托管主机与已配置的远程 Appium。`device install` 安装的是模拟器及工具链；QA 的 `--apk`/MCP `install_apk` 才是向设备安装被测 APK。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 发现与安装 | [saygo/devices/mobile.py](../../saygo/devices/mobile.py) |
| 主机 | [saygo/devices/mobile_host.py](../../saygo/devices/mobile_host.py) |
| Windows worker | [saygo/devices/mobile_host_worker.py](../../saygo/devices/mobile_host_worker.py) |
| 转发 | [saygo/devices/mobile_relay.py](../../saygo/devices/mobile_relay.py) |
| 工具链 | [saygo/devices/toolchain.py](../../saygo/devices/toolchain.py) |
| 驱动 | [saygo/platforms/appium.py](../../saygo/platforms/appium.py) |
| 服务器 | [saygo/platforms/appium_server.py](../../saygo/platforms/appium_server.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 帧流 | [saygo/platforms/mjpeg.py](../../saygo/platforms/mjpeg.py) |
| QA 准备 | [saygo/qa/device_setup.py](../../saygo/qa/device_setup.py) |

## 发现与连接

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| AND-001 | 发现区分真机、模拟器、离线和未授权设备，返回物理 ID、名称与是否可连接，另列 AVD 和诊断。 | `device list --platform android`；发现与安装.discover/android_devices | 已有实现 |
| AND-002 | 本地 connect 只有一个在线候选才自动选择，多候选要求设备 ID；不能以未授权或离线设备代替目标。 | 发现与安装.connect | 已有实现 |
| AND-003 | 命名会话与物理 ID 分离，保存设备、平台、Appium 地址和 session ID；已有别名绑定不同设备/服务时拒绝覆盖。 | 发现与安装.connect；会话.start | 已有实现 |
| AND-004 | 已有 Appium session 重连先通过真实窗口尺寸请求探活；过期后普通动作报错，重新 start/connect 才建会话。 | 会话.attach/start/_attach_driver | 已有实现 |
| AND-005 | 连接默认 noReset、autoLaunch=false，不清空数据、不启动被测应用；明确 launch/open 才切换应用。 | 驱动.setup；发现与安装.connect | 已有实现 |
| AND-006 | 远程 Appium 必须给服务地址与设备 ID，不执行本地设备猜测，不自动安装远端工具或开放防火墙。 | `--server-url`、`--device`；发现与安装.connect | 已有实现 |
| AND-007 | 服务器可复用已有端点，缺失时按配置启动本地 Appium；会话退出只停止自身拥有的服务，不杀其他实例。 | 服务器.AppiumServerManager；驱动.teardown | 已有实现 |
| AND-008 | 短命令退出保留持久会话和服务，disconnect 结束 Appium session 并保存断开配置，stop 清除绑定但不关模拟器。 | 会话.release_controller/stop；devices/control._disconnect | 已有实现 |

## 截图与视觉动作

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| AND-009 | 截图使用 Appium PNG 或可用 MJPEG 帧转换为 PNG，帧流缺失、过期或解码失败必须回到真实 Appium 截图。 | 驱动.screenshot_raw；帧流.latest | 已修复：帧龄 0.5 秒；断流/停止清缓存；本轮为离线测试 |
| AND-010 | 观察区分截图像素和设备逻辑尺寸；检测横竖屏变化，旧图与尺寸不能继续用于定位。 | 驱动._note_screenshot_size/scale；devices/observations | 已有实现；旋转需设备验收 |
| AND-011 | MJPEG 为可选加速，多设备需不同端口；远程端口不通时仍能截图，不能把所有 device 重连说成持续帧流。 | 驱动._pick_mjpeg_port/_start_mjpeg；会话._platform_from_driver | 部分路径：普通重连未恢复帧流 |
| AND-012 | 点击和长按使用 W3C 触摸坐标；长按通过统一动作校验时限制 0.1–30 秒，不读取 UI 树定位。 | 驱动._w3c_tap/tap/long_press；devices/actions | 已有实现 |
| AND-013 | 滑动支持起止坐标和设备命令的 duration_ms，范围 1–30000；时长字段不应被误写为恒定轨迹运动时间。 | 驱动._w3c_swipe；devices/service swipe 分支 | 已有实现；当前时长用于触摸动作中的停留 |
| AND-014 | 上下滚动使用中央纵向手势；scroll_up 朝内容顶部，手指上→下；scroll_down 朝内容底部，手指下→上。 | 驱动.scroll_up/scroll_down | 已统一方向；实际设备滚动待验收 |
| AND-015 | 文字输入经 UnicodeIME 的 mobile:type，支持中文和自绘输入框；异常报告结果未知，不换路径重发。 | 驱动.setup/input_text | 已有实现；目标应用另验 |
| AND-016 | 输入返回异常但可能已生效时，不得自动改路径再次输入；应先观察核对。 | 驱动.input_text | 已修复；模拟回执丢失验证仅派发一次 |
| AND-017 | Android 按键支持 enter/delete/tab/space/escape/back/home/recent/wakeup/power/sleep/menu 及数字 keycode，未知名称拒绝。 | 驱动.press_key | 已有实现；设备权限仍适用 |
| AND-018 | 打开应用须明确包名，通过 Appium activate_app；非法包名拒绝，不把 URL 当作已支持的系统深链。 | 驱动.open_target；devices/actions.BASE | 已修复能力声明；仅公布 open_app |
| AND-019 | 支持 relaunch 保留数据重启、pm_clear 清数据再启动和 none 激活；破坏数据的重置须由用例或用户明确选择。 | 驱动.reset_app；QA 准备 | 已有实现；不是连接默认行为 |
| AND-020 | 软键盘可见性通过驱动查询供截图提示；无法检测时不能以 false 证明没有键盘。 | 驱动.is_ime_visible；skills/keyboard_detector | 已有实现；失败回 false 的边界 |
| AND-021 | 本端不宣称支持 hover、double_click、right_click、scroll_at、hotkey、多指缩放或任意应用内语义定位。 | 驱动方法集；devices/actions.capabilities | 当前未提供这些统一动作 |

## 模拟器安装与启动

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| AND-022 | 安装先给主机、路径、组件、空闲空间与加速条件；dry-run 只预检，不下载、安装或修改系统功能。 | `device install --dry-run`；主机.plan/execute | 已有实现 |
| AND-023 | 安装要求至少 12 GiB 空闲空间和可用硬件加速；缺 KVM/WHPX 时报告阻塞，不自动改 BIOS、启系统功能或重启。 | 主机.plan | 已有实现 |
| AND-024 | 下载前交互接受 Android SDK 许可；无人值守必须显式 accept-licenses，拒绝许可就停止。 | 主机.confirm_licenses；发现与安装.install_android | 已有实现 |
| AND-025 | 复用现有 SDK/Java 或使用私有目录，安装命令行工具、平台、build-tools、模拟器、镜像和 UiAutomator2 工具链。 | 发现与安装.sdk_root/ensure_java/install_android；工具链 | 已有实现 |
| AND-026 | 安装器支持 x64 Windows/Linux 和 Intel/Apple silicon macOS；API 参数校验 30–99，但实际镜像能否安装由 SDK 仓库决定。 | 发现与安装.install_android | 已有实现；不能承诺区间内所有镜像存在 |
| AND-027 | 直接下载校验 SHA256，归档拒绝路径越界；SDK 命令失败保留真实错误，进度写 stderr，最终结果写 stdout。 | 发现与安装.download/unpack/run | 已有实现 |
| AND-028 | AVD 名称须合法；同名同镜像复用，同名异镜像拒绝覆盖，已有不完整工具目录要求检查。 | 发现与安装.safe_name/install_android | 已有实现 |
| AND-029 | boot 按 AVD 名复用已运行实例，选择空闲端口并等候 sys.boot_completed；再次核对该端口仍是目标 AVD。 | 发现与安装.boot_device | 已有实现 |
| AND-030 | 支持 headless，connect 隐含 boot；连接后保存实际截图作为可用证据，不以启动进程成功代替连接成功。 | 主机.execute；发现与安装.provision_runtime | 已有实现 |
| AND-031 | 启动失败或超时保留模拟器及日志供诊断，不换另一设备、不重放未知输入。 | 发现与安装.boot_device | 已有实现 |

## WSL 与 Windows 托管

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| AND-032 | WSL 自动主机选择在无可读写 KVM 时选择 Windows；local/windows 显式选项优先，其他系统不可伪装 WSL。 | 主机.select_host | 已有实现 |
| AND-033 | WSL 本地无在线 Android 时发现逻辑尝试 Windows worker；失败返回诊断，不能将本地 adb 列表描述成全部设备。 | 发现与安装.discover | 已有实现；USB 可达性需现场配置 |
| AND-034 | Windows worker 使用私有嵌入 Python、Node、Appium，只复制白名单源码并保持包结构，不复制配置密钥或改系统 PATH。 | 主机.prepare_windows；Windows worker | 已有实现 |
| AND-035 | Windows Appium 仅监听回环；WSL 经令牌保护的本地 HTTP 与 Windows stdio 转发连接，失败不自动重发请求。 | 转发.relay_request/ensure_relay；Windows worker | 已有实现 |
| AND-036 | 私有 adb 端口写入 Appium adbPort，避免占用或重启默认 adb 服务；旧端口重连必须核对身份。 | Windows worker；驱动.setup | 已有实现 |
| AND-037 | Windows 辅助进程与 Appium 子进程隐藏控制台；不隐藏用户选择显示的模拟器 GUI。 | 工具链.background_options；devices/windows_no_console.cjs | 已有实现；历史局部实测 |
| AND-038 | 重启后重新发现/boot/connect，旧服务地址不符须明确新绑定，不能把陈旧状态当在线。 | 发现与安装.connect；转发.healthy | 已有实现 |

## QA、接管与验收

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| AND-039 | QA 可在指定设备上安装 APK、重连网络设备、清状态/重启；安装失败设备不得继续作为成功设备派发用例。 | `run --device --apk`；QA 准备 | 已有实现；生命周期走 adb 的范围须区分 |
| AND-040 | 多设备 QA 共用动态任务队列，每个 worker 独占设备及相应账号，报告保留设备归属；不是自动同时跑 Android+iOS。 | qa/execution._run_dispatched_devices | 已修复：非空账号池不足时启动前拒绝；未知输入停止该 worker |
| AND-041 | 普通设备与交互任务共享设备锁和 handoff/resume；恢复要新截图，不确定输入要 resolve 后新观察。 | runtime/locking；devices/control；runtime/interactive | 已有实现 |
| AND-042 | 分别验收真机/模拟器、本地/Windows 托管/远程、首次安装/复用、中文输入、旋转、断线和锁屏；不能用一台模拟器代表全部组合。 | `tests/mobile_demo`、`tests/control_demo/test_agent_service.py` | Windows 托管模拟器有历史实测；其余待验收 |

## 验收范围

离线入口：[移动发现与连接](../../tests/mobile_demo/test_mobile.py)、[安装](../../tests/mobile_demo/test_provision.py)、[主机](../../tests/mobile_demo/test_hosts.py)、[worker 包结构](../../tests/mobile_demo/test_bundle.py)、[共享操作](../../tests/control_demo/test_agent_service.py)。历史 WSL→Windows API 35 模拟器安装、截图、设置启动、点击和搜索输入见[操作指南](README.md#验收与待办)。未获得所有主机及真机完整业务证据。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。

本轮源码修复与迁移、六端分别验证的范围见[修复记录](../common/requirements-audit.md#升级与兼容性)。未更新用户安装或发布版本。
