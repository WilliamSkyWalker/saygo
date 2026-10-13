# 需求代码核对记录

[需求总索引](requirements.md) · [测试与验收](testing/README.md) · [架构](architecture.md)

核对日期：2026-10-12。范围为当前工作区的命令入口、共享设备服务、六端驱动、Runtime、桌面产品、QA、Probe、安装更新、发布及辅助功能。保留原 187 个需求编号，补充 69 个公共条目，并新增 227 个六端操作条目，共 483 个编号。公共要求与各端细化有继承关系，这不是 483 个互不重叠的功能，也不是 483 项测试通过。

本轮通过阅读入口注册、动作分派、驱动方法、状态保存、错误分支和现有测试定位需求。源码中存在的行为可标“已有实现”；不合理的现状保留为缺口，不能将其改写为正确产品需求。仓库没有表达的未来业务不凭空增加。未运行真实设备、安装、模型任务或线上发布验收。

## 六端独立清单

| 操作端 | 清单 | 条目数 | 本端边界 |
| --- | --- | --- | --- |
| Windows | [WIN-001～036](../windows/requirements.md) | 36 | 原生前台、后台 runner、显式前台 runner、WSL、原生整机分别描述 |
| macOS | [MAC-001～037](../macos/requirements.md) | 37 | 前台窗口、整机、原生后台；后台不等于任意自绘应用可操作 |
| Android | [AND-001～042](../android/requirements.md) | 42 | 真机、模拟器、远程 Appium、WSL→Windows 主机、QA 生命周期 |
| iOS | [IOS-001～034](../ios/requirements.md) | 34 | 真机签名、Xcode 模拟器、远程 Mac、触摸和有限按键 |
| Chrome/Edge 扩展 | [EXT-001～045](../browser-extension/requirements.md) | 45 | 当前 profile 的网页、共享桥、后台截图、网络记录、用户释放 |
| Playwright | [PW-001～033](../playwright/requirements.md) | 33 | CLI/Runtime 的独立 Chromium；MCP 禁用；截图会前置页面 |

每个清单包含代码索引、编号需求、入口或方法、实现状态与验收范围。WSL 是连接环境；Linux 桌面 GUI 能启动不等于 Linux 原生桌面驱动可用；Selenium、RDP 和模拟器辅助接口归入公共兼容需求。

## 入口与需求对应

以下是本轮按代码梳理的功能覆盖表。测试列表示已有相关检查入口，不表示该文件已覆盖整行所有要求，也不表示本轮重新运行通过。代码中的内部辅助函数归入相应用户行为，不以函数数量生成需求数量。

| 代码入口 | 已列入的行为 | 需求归属 | 相关检查入口 |
| --- | --- | --- | --- |
| [CLI 注册](../../saygo/cli.py)、[设备命令](../../saygo/commands/device.py)、[工具初始化](../../saygo/commands/toolchain.py) | setup/update/init、设备操作与生命周期、CLI 默认值/别名/错误；mcp init/doctor | CORE、INSTALL、六端清单 | [命令测试](../../tests/cli_demo/test_commands.py)、[控制入口](../../tests/control_demo/test_control.py) |
| [MCP 服务](../../saygo/mcp/server.py)、[后端策略](../../saygo/mcp/backend_policy.py) | device/full profile、图像内容、设备工具、交互任务、跑测/报告、Playwright 拒绝策略 | CORE、BROWSER、QA | [共享服务](../../tests/control_demo/test_agent_service.py) |
| [连接控制](../../saygo/devices/control.py)、[会话存储](../../saygo/platforms/device_session.py)、[诊断命令](../../saygo/commands/doctor.py) | 发现、绑定、重连、停止、接管、资源别名、只读诊断与显式输入探测 | SESSION、TASK、六端清单 | [控制入口](../../tests/control_demo/test_control.py)、[共享服务](../../tests/control_demo/test_agent_service.py) |
| [动作](../../saygo/devices/actions.py)、[观察](../../saygo/devices/observations.py)、[服务](../../saygo/devices/service.py)、[诊断](../../saygo/devices/diagnostics.py)、[滚动指导](../../saygo/devices/scrolling.py) | 坐标、裁剪、图像证据、能力、等待、来源观察、日志、复合提交、失败分类 | OBS、SESSION、TASK | [自动化契约](../../tests/control_demo/test_requirements.py)、[显式前台](../../tests/control_demo/test_foreground_cli.py) |
| [交互任务](../../saygo/runtime/interactive.py)、[任务命令](../../saygo/commands/task.py) | 创建、观察、提交、去重、恢复、核对、人工接管、结束、取消、时间线、导出 | TASK | [共享服务](../../tests/control_demo/test_agent_service.py)、[Runtime](../../tests/runtime_demo/test_runtime.py) |
| [工作流校验](../../saygo/runtime/schema.py)、[执行器](../../saygo/runtime/engine.py)、[资源](../../saygo/runtime/resources.py)、[CLI](../../saygo/runtime/cli.py)、[持久库](../../saygo/runtime/store.py)、[锁](../../saygo/runtime/locking.py) | 资源与步骤、引用、只读 SQL、人工验证、检查点、事件、占用、暂停/取消、默认目录 | FLOW、SESSION | [Runtime](../../tests/runtime_demo/test_runtime.py)、[自动化契约](../../tests/control_demo/test_requirements.py) |
| [Windows 驱动](../../saygo/platforms/desktop_win.py)、[runner](../../saygo/platforms/windows_runner.py)、[Win32](../../saygo/platforms/windows_runner.ps1)、[共用桌面](../../saygo/platforms/desktop.py) | 进程/窗口生命周期、DPI、捕获、前台/后台输入、控件绑定 | WIN、NATIVE | [窗口测试](../../tests/control_demo/test_desktop.py)、[真实后台夹具](../../tests/control_demo/test_background_live.py) |
| [macOS 前台](../../saygo/platforms/desktop_mac.py)、[macOS 后台](../../saygo/platforms/desktop_mac_background.py) | 权限、窗口、Retina、AX 坐标命中、原生动作、定向键盘与滚动 | MAC、NATIVE | [后台契约](../../tests/control_demo/test_mac_background.py)、[真实面板](../../tests/mac_demo/test_background_live.py) |
| [整机](../../saygo/platforms/desktop_local.py)、[应用发现](../../saygo/devices/applications.py)、[平台工厂](../../saygo/platforms/__init__.py)、[抽象接口](../../saygo/platforms/base.py) | 支持 OS、整机截图、多屏/焦点、应用清单、公共动作分派 | WIN、MAC、OBS、GUI | [桌面连接](../../tests/desktop_demo/test_connections.py)、[应用启动](../../tests/desktop_demo/test_launch_runtime.py) |
| [移动设备](../../saygo/devices/mobile.py)、[主机](../../saygo/devices/mobile_host.py)、[worker](../../saygo/devices/mobile_host_worker.py)、[转发](../../saygo/devices/mobile_relay.py)、[工具链](../../saygo/devices/toolchain.py)、[隐藏控制台](../../saygo/devices/windows_no_console.cjs) | 发现、主机选择、安装计划/许可、SDK/AVD/Xcode、启动、私有工具、远程接入、loopback 转发 | AND、IOS、MOBILE | [移动测试](../../tests/mobile_demo/) |
| [Appium](../../saygo/platforms/appium.py)、[服务器](../../saygo/platforms/appium_server.py)、[帧流](../../saygo/platforms/mjpeg.py)、[模拟器辅助](../../saygo/devices/simulator.py) | 截图、坐标、旋转、W3C 触摸、Unicode/IME、按键、应用激活/重置、WDA | AND、IOS、OBS | [移动测试](../../tests/mobile_demo/)、[共享服务](../../tests/control_demo/test_agent_service.py) |
| [扩展驱动](../../saygo/platforms/browser_extension.py)、[扩展 worker](../../extensions/saygo-browser/background.js)、[弹窗](../../extensions/saygo-browser/popup.js)、[网络日志](../../extensions/saygo-browser/network.js)、[网络命令](../../saygo/devices/network.py) | 连接/释放、目标 ID、后台截图、输入、页面生命周期、HTTP/WS/SSE/流式观察 | EXT、BROWSER、BRIDGE | [扩展测试](../../tests/extension_demo/)、[网络测试](../../tests/control_demo/test_network.py) |
| [本地桥](../../saygo/integrations/browser_bridge.py)、[发现](../../saygo/integrations/browser_location.py)、[注册](../../saygo/integrations/browser_setup.py)、[兼容入口](../../saygo/browser_bridge.py) | IPC、协议、超时、共享目录、安装所有权、在线 host 保留、升级同步 | EXT、BRIDGE、UPDATE | [桥测试](../../tests/extension_demo/test_bridge.py)、[共享桥](../../tests/extension_demo/test_shared_bridge.py) |
| [Playwright](../../saygo/platforms/browser_playwright.py) | 独立 Chromium/CDP、持久 target ID、页面管理、坐标输入、事件/对话框、控制器释放 | PW、BROWSER | [契约](../../tests/browser_demo/test_playwright.py)、[真实浏览器](../../tests/browser_demo/test_playwright_live.py) |
| [Selenium](../../saygo/platforms/browser.py)、[Grid 清理](../../saygo/platforms/selenium_grid.py)、[RDP](../../saygo/platforms/rdp.py) | QA 本地/Grid 兼容、实验 RDP、动作和生命周期边界 | QA-022、OTHER-013～014、NATIVE-008 | [Grid 测试](../../tests/browser_demo/test_selenium_grid.py)；RDP 无同等完整验收 |
| [桌面 UI](../../saygo/desktop/app.py)、[主题](../../saygo/desktop/theme.py)、[模型](../../saygo/desktop/model.py)、[循环](../../saygo/desktop/runner.py)、[连接](../../saygo/desktop/connections.py) | 对话、设置/Key、视觉连接测试、任务控制、按需观察、恢复、历史/导出与连接引导 | GUI、WIN、MAC | [桌面产品测试](../../tests/desktop_demo/) |
| [目标](../../saygo/commands/targets.py)、[run](../../saygo/commands/run.py)、[后台命令](../../saygo/commands/background.py)、[发现](../../saygo/qa/cases.py)、[设备准备](../../saygo/qa/device_setup.py)、[调度](../../saygo/qa/execution.py) | 模板、用例解析选择、账号/前置条件、APK、重置、分片、多设备、Grid、后台运行与状态 | QA、AND | [CLI 执行](../../tests/cli_demo/test_execution.py)、[CLI 命令](../../tests/cli_demo/test_commands.py) |
| [Gherkin](../../saygo/qa/gherkin.py)、[规划](../../saygo/qa/planner.py)、[执行](../../saygo/qa/agent.py)、[模型](../../saygo/qa/brain.py)、[证据校验](../../saygo/qa/step_validator.py)、[根因](../../saygo/qa/healer.py)、[报告](../../saygo/qa/report.py) | 标签/步骤/示例、逐步判定、预算、合并断言、分层执行、不可视断言边界、报告 | QA | [契约](../../tests/control_demo/test_requirements.py)、[CLI 执行](../../tests/cli_demo/test_execution.py)；真实模型另验 |
| [技能](../../saygo/skills/)、[稳定帧](../../saygo/vision/settle.py)、[定位](../../saygo/vision/locator.py)、[图像网格](../../saygo/vision/grid.py) | 加载/键盘/滚动/diff/toast、可选 OCR/裁剪/颜色/布局、稳定采样和定位 | QA、OTHER-002/012 | 相关契约不代表逐技能真实业务覆盖 |
| [Probe](../../saygo/probes/)、[Probe 命令](../../saygo/commands/probes.py) | 指令解析、注册/配置、上下文、Python/子进程、三态、轮询、生命周期与单独查询 | PROBE | [契约](../../tests/control_demo/test_requirements.py)；客户插件需自有证据 |
| [外部 MCP](../../saygo/mcp/client.py)、[Figma 命令](../../saygo/commands/figma.py)、[REST](../../saygo/integrations/figma.py)、[MCP 适配](../../saygo/integrations/figma_via_mcp.py)、[设计审查](../../saygo/integrations/figma_ops.py)、[旧报告渲染](../../saygo/drive/render.py) | 外部工具、设计帧/截图、生成用例/视觉审查、旧 JSONL→HTML | QA-027、OTHER-001/009～011、CONFIG-008 | 本轮源码核对；外部服务与客户数据未调用 |
| [配置](../../saygo/config.py)、[日志](../../saygo/logger.py)、[环境模板](../../.env.example) | 配置优先级、默认/显式文件、占位符、模型/平台参数、日志与敏感内容 | CONFIG | [配置安装](../../tests/control_demo/test_config_install.py) |
| [setup](../../saygo/setup.py)、[安装器](../../scripts/install_agent_plugin.py)、[开发安装](../../scripts/install_development.py)、[安装引导](../../scripts/install_saygo.py)、[插件](../../plugins/saygo-device/)、[Claude 入口](../../.claude-plugin/marketplace.json) | package/managed/dev、客户端接入、权限保留、资源打包、卸载、重启与兼容入口 | INSTALL | [安装/客户端测试](../../tests/control_demo/) |
| [更新](../../saygo/updates.py) | 检查/通知/应用分离、稳定/测试通道、缓存/锁、来源校验、空闲切换、旧运行时保留、包模式限制 | UPDATE | [更新](../../tests/control_demo/test_updates.py)、[包更新](../../tests/control_demo/test_updates_package.py)、[最新安装](../../tests/control_demo/test_latest_install.py) |
| [发行构建](../../scripts/build_release.py)、[桌面构建](../../scripts/build_desktop.py)、[打包](../../scripts/package_desktop.py)、[包检查](../../scripts/check_python_package.py)、[桌面检查](../../scripts/check_desktop_build.py)、[商店提交](../../scripts/publish_chrome_store.py)、[CI](../../.github/workflows/)、[包配置](../../pyproject.toml) | 白名单、版本/授权、校验和、源码/wheel/sdist/桌面/扩展、三系统安装与发布证据 | RELEASE、INSTALL、GUI、UPDATE | [发布安装](../../tests/control_demo/test_release_install.py)、构建检查脚本；当前发布未触发 |
| [官网](../../website-project/)、[分发元数据](../../distribution/) | 产品说明、中英切换、隐私/下载/商店入口、部署与版本记录 | OTHER、RELEASE | 源文件与链接核对；线上部署另验 |

## 代码尚未满足的要求

以下是静态代码核对所得；影响描述基于执行分支，不代表本次已经在真实设备上复现。表中“需要达到”是后续修复与验收的条件，本轮没有修改这些运行时代码。

| 关联编号 | 代码事实与影响 | 需要达到的要求 |
| --- | --- | --- |
| OBS-013、AND-018、IOS-028、PW-028 | [actions.BASE](../../saygo/devices/actions.py) 给所有普通后端加上 open_url/open_app；Appium 将目标当包名，浏览器将其当 URL。能力声明和含义不相符。 | 按端声明并校验动作语义；不支持在派发前拒绝 |
| OBS-014、OBS-017～018 | [service._execute](../../saygo/devices/service.py) 允许 act 不带 observation_id，多个旧命令直接调驱动；普通 device 记录日志，但无调用方 request ID 去重。 | 明确低级接口边界；需要可靠任务恢复时使用 task；进一步统一观察/去重保护 |
| SESSION-001、MAC-004 | [DesktopMacPlatform._find_window](../../saygo/platforms/desktop_mac.py) 按应用 ownerName 选最大窗口，前台 setup 没有按保存 PID/window ID 恢复。 | 保存并复核明确窗口，原窗口消失时拒绝或人工选窗，不暗中换窗 |
| MOBILE-004、OBS-020、AND-009、IOS-018 | [MjpegFrameReader.latest](../../saygo/platforms/mjpeg.py) 返回缓存帧，没有采集时间/帧龄校验，断流重连也不清掉已有帧。 | 旧帧失效后回落真实截图；验证断流、停止更新、重连与截图失败 |
| OBS-021、AND-016、IOS-024 | [AppiumPlatform.input_text](../../saygo/platforms/appium.py) 捕获输入异常后会调用另一输入方法；如果前次已生效但回执丢失，可能重复输入。 | 区分确定未派发与结果不明；不明时先观察，禁止自动换路径重发 |
| OBS-019、AND-014、IOS-022 | [Appium 滚动](../../saygo/platforms/appium.py) 的 scroll_up 表示手指上滑，桌面/浏览器表示滚轮向上；默认滚动位置和单位也各不同。 | 统一或显式标示方向含义，按端验证实际内容方向，不能照抄一端策略 |
| QA-019、AND-040 | [多设备调度](../../saygo/qa/execution.py) 账号不足时回退 accounts[0]，无法保证每个 worker 使用独立账号。 | 需要独立账号的运行在不足时拒绝/要求补齐，或明确选择共享策略 |
| QA-022、OTHER-013 | [Grid 清理](../../saygo/platforms/selenium_grid.py) 遍历 /status 中全部 session 并 DELETE；本地 QA 启动和并发启动均可调用。 | 仅清理本任务拥有的 session；共享 Grid 上验证其他会话不受影响 |
| QA-028、SESSION-014 | [QA agent](../../saygo/qa/agent.py) 直接调平台，未统一通过 device 服务/InteractiveRuntime 的动作检查和请求去重。 | QA 路径独立列验收；统一保护完成前不得说与 device/task 等价 |
| CONFIG-009 | [调度日志](../../saygo/qa/execution.py) 只过滤名称包含 pass/secret 的账号字段；其他敏感字段可能出现在日志中。 | 按明确敏感字段/最小日志策略脱敏，报告与日志分别验收 |

## 已修正文档中的过度概括

- `device sessions` 是保存记录，不做在线探活；MCP 的不可用后端列表也是策略判断。使用真实请求、截图和输入结果分别证明连接与操作。
- 显式 workflow 默认 `.saygo_runs/runtime`；交互 task 默认 `$SAYGO_HOME_DIR/runtime`。都可配置 `SAYGO_RUNTIME_DIR`，但不能误称默认目录相同。
- 扩展后台截图/普通视觉输入不前置目标，显式选页会激活标签/窗口；Playwright 截图会前置。
- macOS 后台有锁屏/当前控制台检查，Windows 不能未经独立核验继承该保证。
- 滚动的半屏校准、重叠和接近目标缩小步长是操作指导与模型提示，不是所有驱动自动执行的算法。
- Android WSL 本地无在线设备时会尝试 Windows worker 发现；普通 device 重连没有自动恢复 MJPEG，不能宣传每条命令都从帧流获取截图。
- iOS、签名公证、完整模型业务任务和六端完整跨设备业务仍保留待验收；现有代码不构成已通过证明。

## 维护与验收

后续新增功能同时修改公共要求或对应端清单，并注明入口、状态、负向限制和验收证据。公共原编号保留，端特有编号分别使用 WIN/MAC/AND/IOS/EXT/PW；变更已有语义时更新状态与证据，不通过删除需求掩盖缺口。

原 638 条自动化场景和 66 条人工场景保留。新增需求没有因“找到相关测试文件”就自动计为覆盖；应按需要建立逐条映射，记录真正运行的命令和结果。真实六端验收须使用独立 profile/会话/测试应用，不能对用户业务会话做测试输入。当前安装、商店审核、远端包版本和发布状态本轮均未改变。

本轮文档核验结果：483 个编号唯一且各域连续，原 187 个编号保留，需求引用和表格列数有效；555 个 Markdown 本地链接/锚点检查通过。`python3 scripts/render_requirement_cases.py --check` 确认原 638 条生成场景同步；638 条自动化与 66 条人工场景均可由仓库 Gherkin 解析器按原编号解析。`git -c core.safecrlf=false diff --check` 通过。这是文档、目录与解析检查，未重新执行 638 项功能测试，也未执行六端真机验收；上述代码缺口仍未修复。
