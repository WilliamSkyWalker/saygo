# Saygo 全项目需求基线

本基线依据当前仓库文档、实现、提交历史、用户本轮要求及持久约束整理。覆盖产品全部现有功能域，不只更新机制；不声称恢复了仓库外不可见的历史对话。基线日期：2026-10-12。

需求为应满足的行为，不以当前代码的缺陷反向定义正确行为。表中“已有实现”仅指发现实现与已有测试，不能替代本次测试或真机验收；“部分实现”需查看边界。工作区原有桌面改动作为在研能力记录，不视为已发布。

每条编号是测试与变更追踪入口；细节链接下列来源和各功能指南。新增测试文字版见 [BDD 用例](testing/requirements.feature)，自动化映射与运行说明见 [测试目录](testing/README.md)。

## CORE · 产品与入口

来源：README.md、architecture.md；saygo/cli.py、mcp/server.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| CORE-001 | 外部 Agent 使用共享 CLI/MCP 操作层，无需 Saygo 模型 Key；device profile 可独立启动。 | 已有实现 |
| CORE-002 | 桌面应用由用户配置视觉模型；交互任务复用 Runtime，不建立另一套任务状态语义。 | 已有实现 |
| CORE-003 | 显式 JSON workflow 不要求模型规划；BDD QA 保留独立 run 入口。 | 已有实现 |
| CORE-004 | 视觉决策只向模型提供截图与操作元数据，不提供 DOM 或 UI 树。 | 已有实现 |
| CORE-005 | CLI help 和直接设备控制不得强制加载 QA、OpenAI、Appium 等无关可选依赖。 | 已有实现 |
| CORE-006 | CLI/MCP 同名会话在相同 SAYGO_HOME_DIR 下绑定相同目标；任务库允许 SAYGO_RUNTIME_DIR 覆盖。 | 已有实现 |
| CORE-007 | 输入派发成功、画面稳定和业务成功必须分开表达；成功回执不得代替结果验证。 | 已有实现 |
| CORE-008 | 不支持的平台、动作和能力明确报错；不得偷偷换后端或创建默认手机会话。 | 已有实现 |

## SESSION · 会话与资源

来源：agent-control.md、control.md；devices/control.py、runtime/locking.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| SESSION-001 | 命名会话持久化平台、设备、浏览器页或桌面窗口绑定，重连不得暗中改绑。 | 已有实现 |
| SESSION-002 | 设备发现区分在线、离线、未授权；多候选要求选择，单候选才允许自动选择。 | 已有实现 |
| SESSION-003 | 列出会话包含可用性；MCP 不可用后端单独返回原因。 | 已有实现 |
| SESSION-004 | 连接、断开与停止分开；断开控制器不得默认关闭用户浏览器或模拟器。 | 已有实现 |
| SESSION-005 | 会话 handoff 阻止自动输入，resume 获取新观察，接管不代表业务已完成。 | 已有实现 |
| SESSION-006 | 任务在 idle、waiting_for_human、needs_review 状态持续持有资源。 | 已有实现 |
| SESSION-007 | 普通 device 命令与任务入口遵守同一资源归属和 OS 操作锁。 | 已有实现 |
| SESSION-008 | 本地桌面窗口共享输入锁；锁的保证范围仅限 Saygo 自身。 | 已有实现 |
| SESSION-009 | 项目别名保存在 .saygo/resources.json；别名与物理设备 ID 区分。 | 已有实现 |
| SESSION-010 | 浏览器使用与任务匹配的独立命名会话；绑定失效显式重连，不借用其他业务会话。 | 已有实现 |

## OBS · 观察与动作

来源：agent-control.md；devices/observations.py、devices/actions.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| OBS-001 | 观察包含唯一 ID、时间、会话、目标、截图与屏幕尺寸以及坐标映射。 | 已有实现 |
| OBS-002 | 支持 screen、percent、image、crop 坐标；image/crop 必须有来源观察。 | 已有实现 |
| OBS-003 | 百分比坐标 0–100，边缘落在最后有效像素；拒绝布尔值、非数、无穷和越界。 | 已有实现 |
| OBS-004 | 裁剪保留原图映射及放大倍率；不把截图像素当作 CSS 或设备逻辑像素。 | 已有实现 |
| OBS-005 | 依赖画面的动作拒绝超过 30 秒的观察及已失效的目标。 | 已有实现 |
| OBS-006 | 派发前核对页面、URL、窗口、进程、边界、尺寸及像素变化；局部目标变化也须拒绝。 | 已有实现 |
| OBS-007 | 动作能力由实际后端公布，含指针、触摸、文字、按键、滚动及页面操作。 | 已有实现 |
| OBS-008 | 输入、URL、按键、应用及页面 ID 必须非空；长按时间与滚动幅度须有界。 | 已有实现 |
| OBS-009 | 动作可请求后截图；截图失败记录为证据错误，不重放已确认输入。 | 已有实现 |
| OBS-010 | 稳定/变化等待有时间上限并返回 condition_met/timed_out，不宣称业务成功。 | 已有实现 |
| OBS-011 | 每次滚动观察目标区域，首次约半屏、接近目标 10–20%，无变化先诊断再决定。 | 已有实现 |
| OBS-012 | MCP 观察及有观察的动作返回图像内容；CLI 返回图像路径和元数据。 | 已有实现 |

## TASK · 交互任务与恢复

来源：agent-control.md；runtime/interactive.py、runtime/store.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| TASK-001 | 创建跨设备任务绑定命名资源，返回可持久引用的 task ID。 | 已有实现 |
| TASK-002 | 每次 submit 使用 request ID 和观察 ID；相同请求不能重复派发。 | 已有实现 |
| TASK-003 | 派发前提交 durable intent，输入异常或中断后结果未知进入 needs_review。 | 已有实现 |
| TASK-004 | 恢复读取检查点、事件和资源状态，不自动重试未知动作。 | 已有实现 |
| TASK-005 | resolve 需明确 completed/not_executed 与说明，并使旧观察失效。 | 已有实现 |
| TASK-006 | handoff 保存人工指示，resume 重新观察资源，再由调用方验证。 | 已有实现 |
| TASK-007 | finish/cancel 释放资源；普通状态查询、时间线与事件查询不派发输入。 | 已有实现 |
| TASK-008 | 操作事实、截图、异常与 Agent 注释分别存储，导出保留关联。 | 已有实现 |
| TASK-009 | diagnose 返回窗口身份、候选、能力和截图失败原因，不伪造旧图。 | 已有实现 |
| TASK-010 | repair 仅允许重新观察或选择同进程的合格窗口，记录操作并使旧观察失效。 | 已有实现 |
| TASK-011 | 未核对的不确定输入不能借 repair 绕过；修复后仍需新观察。 | 已有实现 |
| TASK-012 | 完整手机注册→邮箱激活→桌面确认需要真实业务验收；模拟测试不构成通过证明。 | 已有实现 |

## FLOW · 声明式工作流

来源：runtime.md；runtime/schema.py、engine.py、resources.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| FLOW-001 | 工作流 version=1，资源和步骤非空，inputs 为对象；返回独立数据副本。 | 已有实现 |
| FLOW-002 | 资源名与步骤 ID 合法且步骤 ID 唯一；引用不存在资源须拒绝。 | 已有实现 |
| FLOW-003 | 资源支持 Android、iOS、browser、mac、windows、SQLite，按类型校验绑定字段。 | 已有实现 |
| FLOW-004 | 步骤支持 observe/action/tool/human/check/pages，按资源能力限制组合。 | 已有实现 |
| FLOW-005 | action 必须包含操作和来源观察；human 必须包含指示与后续 check ID。 | 已有实现 |
| FLOW-006 | check 必须有 actual/equals；resume 人工确认不能跳过 check。 | 已有实现 |
| FLOW-007 | 精确 $ref 保留 JSON 类型，支持嵌套对象和列表下标，缺失引用报错。 | 已有实现 |
| FLOW-008 | 浏览器 page ID 非空且不得用于 Selenium 页面资源。 | 已有实现 |
| FLOW-009 | SQLite 仅允许已注册参数化只读查询，阻止写入、ATTACH 和 PRAGMA。 | 已有实现 |
| FLOW-010 | 查询限制执行时间和返回行数；相对数据库路径按工作流文件目录解析。 | 已有实现 |
| FLOW-011 | 没有通用数据库写入、任意 API/MCP 连接器及远程接管 UI。 | 已有实现 |

## BROWSER · 浏览器会话与视觉操作

来源：browser.md、browser-extension.md；platforms/browser_extension.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| BROWSER-001 | MCP 与桌面版默认扩展后端；Playwright 仅 CLI/Runtime，QA 可用 Selenium。 | 已有实现 |
| BROWSER-002 | MCP 对 Playwright 的连接、观察、动作及可执行任务恢复拒绝，审计与取消仍可用。 | 已有实现 |
| BROWSER-003 | 扩展使用当前浏览器登录状态，不读取 DOM 为视觉决策提供语义。 | 已有实现 |
| BROWSER-004 | 浏览器按稳定 page ID 绑定，创建、列出、选择、关闭页面都保留证据。 | 已有实现 |
| BROWSER-005 | 关闭已选页后明确无截图，不擅自选择其他页。 | 已有实现 |
| BROWSER-006 | 后台截图针对绑定页，不要求手动前置；失败返回结构化诊断及超时信息。 | 已有实现 |
| BROWSER-007 | 首次后台截取允许页面绘制预热，截图期限有界，失败不自动断开扩展。 | 已有实现 |
| BROWSER-008 | 后台操作与截取不抢占用户前台页；浏览器受保护页面明确失败。 | 已有实现 |
| BROWSER-009 | scroll_at 命中指定滚动区域，单位 100 CSS 像素，正数向上且允许小数。 | 已有实现 |
| BROWSER-010 | 指针支持 hover、双击、右键、长按、拖动和能力允许的 hotkey。 | 已有实现 |
| BROWSER-011 | 已连接扩展更新不强行踢掉现有连接；显式重连后使用新桥。 | 已有实现 |
| BROWSER-012 | Playwright/CDP 控制器退出只断开连接，浏览器和稳定 target ID 会话可恢复。 | 已有实现 |

## BRIDGE · 扩展桥与网络记录

来源：browser-extension.md；integrations/browser_bridge.py、extensions/saygo-browser。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| BRIDGE-001 | Chrome/Edge native messaging 在浏览器所属 OS 注册；WSL 正确桥接 Windows。 | 已有实现 |
| BRIDGE-002 | 默认商店扩展 ID，开发 ID 必须显式覆盖，不能误用其他扩展连接。 | 已有实现 |
| BRIDGE-003 | 连接握手核验协议，不匹配提示升级两端，不报告成功。 | 已有实现 |
| BRIDGE-004 | 本地桥注册所有权明确，卸载不移除其他安装的 host。 | 已有实现 |
| BRIDGE-005 | 扩展连接和断开需可观察；丢失回执不自动重放输入请求。 | 已有实现 |
| BRIDGE-006 | HTTP 与流式网络记录按页面/会话查询，保留方法、状态和可用正文。 | 已有实现 |
| BRIDGE-007 | 网络记录不是截图业务结论；无法获取的内容、大小限制与丢失明确标识。 | 已有实现 |
| BRIDGE-008 | 网络证据、输入和截图可能含敏感信息，只保留在本地任务记录或授权导出。 | 已有实现 |

## MOBILE · 移动端与模拟器

来源：mobile.md；devices/mobile.py、simulator.py、mobile_host.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| MOBILE-001 | Android/iOS 视觉动作通过 Appium；adb/simctl 用于发现与生命周期，不旁路视觉控制。 | 部分实现/硬件待验收 |
| MOBILE-002 | 连接现有手机不默认重置设备或打开应用，设备授权由用户完成。 | 部分实现/硬件待验收 |
| MOBILE-003 | Android 使用 UiAutomator2 与 Unicode 输入；iOS 使用 XCUITest 与已有签名配置。 | 部分实现/硬件待验收 |
| MOBILE-004 | MJPEG 截图不可用时回落 Appium 截图，不把无帧作为成功。 | 部分实现/硬件待验收 |
| MOBILE-005 | Android 安装计划包含主机、磁盘、加速与工具组件，dry-run 不安装或下载。 | 部分实现/硬件待验收 |
| MOBILE-006 | 安装复用 SDK/Java/AVD，直接下载文件校验 SHA256，失败返回真实错误。 | 部分实现/硬件待验收 |
| MOBILE-007 | 同名 AVD 异镜像拒绝覆盖；已有运行 AVD 按名称复用，不随意选择别台设备。 | 部分实现/硬件待验收 |
| MOBILE-008 | Android SDK license 显式接受；空间不足、加速缺失不假成功，不修改 BIOS。 | 部分实现/硬件待验收 |
| MOBILE-009 | boot 等待启动完成；超时保留模拟器与日志供诊断。 | 部分实现/硬件待验收 |
| MOBILE-010 | iOS 模拟器依赖 macOS/full Xcode；Windows/Linux/WSL 不伪装本地支持。 | 部分实现/硬件待验收 |
| MOBILE-011 | WSL 无可用 KVM 时可选 Windows host；显式 local/windows 选择优先。 | 部分实现/硬件待验收 |
| MOBILE-012 | Windows 私有 Python/Node/Appium 不替换全局 PATH；只复制允许的 worker 文件。 | 部分实现/硬件待验收 |
| MOBILE-013 | Windows Appium 仅 loopback，WSL token relay 不添加防火墙规则，不重放失败请求。 | 部分实现/硬件待验收 |
| MOBILE-014 | 手机真机和完整 iOS 配置链需设备验证；不得把模拟测试报告为硬件已验收。 | 部分实现/硬件待验收 |

## NATIVE · 本地与后台桌面驱动

来源：control.md、windows-background-research.md；platforms/desktop*。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| NATIVE-001 | Windows 原生及 WSL runner、macOS 原生窗口驱动共享动作语义。 | 部分实现/平台有限 |
| NATIVE-002 | 窗口绑定核对窗口 ID、PID 和边界，目标改变时拒绝旧坐标。 | 部分实现/平台有限 |
| NATIVE-003 | Windows background 不支持动作明确失败，不回落全局键鼠或快捷键。 | 部分实现/平台有限 |
| NATIVE-004 | Windows foreground 恢复/前置必须显式选择，不因截图失败自动启用。 | 部分实现/平台有限 |
| NATIVE-005 | macOS background 不激活/启动应用、不用全局键鼠或剪贴板、不前台回退。 | 部分实现/平台有限 |
| NATIVE-006 | macOS 内部 AX 仅做坐标命中与原生执行，不给模型控件树或文本定位。 | 部分实现/平台有限 |
| NATIVE-007 | 锁屏、非当前桌面及身份不明窗口拒绝；已验证单面板不代表任意应用兼容。 | 部分实现/平台有限 |
| NATIVE-008 | Linux 本地窗口自动化未实现；RDP 保留实验性边界。 | 部分实现/平台有限 |

## GUI · 桌面产品与模型

来源：desktop.md；desktop/app.py、runner.py、model.py、connections.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| GUI-001 | Qt 6 对话界面含任务历史、消息输入、截图、模型设置和连接管理。 | 部分实现/工作区在研 |
| GUI-002 | 支持任务开始、暂停、人工回复继续、取消、恢复、证据导出。 | 部分实现/工作区在研 |
| GUI-003 | 模型配置为 OpenAI-compatible 视觉 API，连接测试发送测试图而非只测文本。 | 部分实现/工作区在研 |
| GUI-004 | HTTPS 端点或本机 HTTP；拒绝凭据 URL、查询串、片段、远程明文及重定向。 | 部分实现/工作区在研 |
| GUI-005 | Key 仅内存或受支持 OS keyring，禁止明文 fallback，desktop.json 不含 Key。 | 部分实现/工作区在研 |
| GUI-006 | 模型错误输出不回显 provider body 或密钥，超时和 HTTP 错误给可用提示。 | 部分实现/工作区在研 |
| GUI-007 | 每轮模型一个动作；截图失败不可用旧帧代替，不可在观察失败时宣称完成。 | 部分实现/工作区在研 |
| GUI-008 | 连续观察失败或诊断修复达到界限后 handoff，避免无限恢复循环。 | 部分实现/工作区在研 |
| GUI-009 | 原生 Windows/macOS 自动连接本机；任务时最小化，接管或结束恢复界面。 | 部分实现/工作区在研 |
| GUI-010 | 可发现本机应用入口；启动校验已列出的入口和本机绑定，记录 durable intent。 | 部分实现/工作区在研 |
| GUI-011 | 应用启动可不依赖桌面像素保持不变；点击输入仍要完整观察校验。 | 部分实现/工作区在研 |
| GUI-012 | 自动检测浏览器不激活标签页，不在任务/人工接管期间改绑；浏览器按需加入观察。 | 部分实现/工作区在研 |
| GUI-013 | 高级连接保留窗口/手机，用户可取消本次任务不用的目标。 | 部分实现/工作区在研 |
| GUI-014 | Windows 便携包无需 Python/WSL，GUI 无控制台，host 使用独立 stdio 可执行文件。 | 部分实现/工作区在研 |
| GUI-015 | macOS DMG、签名、公证、干净机器及真实模型任务必须分别记录验收，不能仅凭打包脚本宣称完成。 | 部分实现/工作区在研 |

## QA · BDD QA 与判定

来源：../agent.md、perf-plan.md；qa/gherkin.py、agent.py、step_validator.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| QA-001 | 解析 Feature/Background/Scenario/Outline/Examples，支持中英文关键字及参数展开。 | 已有实现 |
| QA-002 | 标签携带 priority、automation、platform、reset、ref，Background 应用于每个场景。 | 已有实现 |
| QA-003 | 规划与逐步执行分离；当前步骤 index 必须等于待执行项，模型不能跳步。 | 已有实现 |
| QA-004 | pass/fail 需具体可见证据且至少 15 字符，fail 还需充分原因。 | 已有实现 |
| QA-005 | in_progress 必须有 action；无效响应不执行动作，连续拒绝收敛为失败。 | 已有实现 |
| QA-006 | 不可视业务断言不得以视觉推断 PASS；使用 probe 或明确未验证。 | 已有实现 |
| QA-007 | 连续同屏断言同步合并，逐条 verdict/evidence/where，去重及负向断言检查。 | 已有实现 |
| QA-008 | 断言失败可现场处理阻挡弹窗并有界重判，不异步离屏后补判。 | 已有实现 |
| QA-009 | 主动等待预算与无进展计数分开，预算耗尽恢复计数；不得无限循环。 | 已有实现 |
| QA-010 | 稳定帧像素差与 mask 选择静态一帧/动态最多三帧；不保证捕获所有短暂提示。 | 已有实现 |
| QA-011 | 可选 locator 只输出坐标，失败回到原有坐标路径；不采用 DOM/UI 树定位。 | 已有实现 |
| QA-012 | 分层模型可配置，分批操作失败有界回退，视觉差异不等于业务成功。 | 已有实现 |
| QA-013 | healer 分类根因和建议，不能修改既有判定或自动修复被测应用。 | 已有实现 |
| QA-014 | 报告保存步骤结果、错误、截图、判定证据，兼容支持的 Python 版本。 | 已有实现 |
| QA-015 | 性能优化须同时衡量墙钟、调用量与通过率；OCR 交叉核验与对抗复核尚属计划。 | 已有实现 |

## PROBE · 非视觉断言

来源：probes.md；probes/spec.py、base.py、subprocess_probe.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| PROBE-001 | probe 指令绑定上一条步骤，参数支持字符串、数字、布尔、null、JSON 与裸 flag。 | 已有实现 |
| PROBE-002 | 用例只声明检查意图，真实事件名/表名映射保存在私有插件配置。 | 已有实现 |
| PROBE-003 | pass/fail/inconclusive 三态；无数据且未到上报期限不能立即当失败证据。 | 已有实现 |
| PROBE-004 | inconclusive 与插件异常按预算轮询，超时失败且保留错误，不能因查不了放过。 | 已有实现 |
| PROBE-005 | Python 与 stdin/stdout JSON 子进程插件均可用，未知注册名失败。 | 已有实现 |
| PROBE-006 | 上下文包含时间窗、账号、设备、平台、尝试次数、预算、session 与产物目录。 | 已有实现 |
| PROBE-007 | 一条 step 一个 probe，不参与视觉断言合并；完整用例仍可能传入模型。 | 已有实现 |
| PROBE-008 | skip-probes 明确标 skip 并记录未验证项；only-probes 按 case 筛选且保留触发 UI 步骤。 | 已有实现 |
| PROBE-009 | 注册表可展开环境变量，插件依赖不污染主运行环境，配置和客户插件不公开。 | 已有实现 |

## CONFIG · 配置与凭据

来源：README.md、distribution/README.md；config.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| CONFIG-001 | 优先级 defaults→用户 config.env→项目 .env 或显式文件→进程环境。 | 已有实现 |
| CONFIG-002 | 显式 SAYGO_CONFIG_FILE 缺失必须报错，不从包目录搜配置。 | 已有实现 |
| CONFIG-003 | init/init --user 创建模板不覆盖原文件，POSIX 权限仅 owner。 | 已有实现 |
| CONFIG-004 | 安装只保存配置文件引用，不复制密钥内容，升级保留引用。 | 已有实现 |
| CONFIG-005 | 公开代码、测试、示例与提交记录使用脱敏数据，客户用例独立私有管理。 | 已有实现 |
| CONFIG-006 | 日志、报告与网络记录用途清晰，敏感资料不进入发布白名单。 | 已有实现 |

## INSTALL · 安装、客户端与隔离

来源：distribution/README.md、distribution/PYPI.md、plugin.md；scripts/install_agent_plugin.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| INSTALL-001 | pipx 安装包后 setup 绑定同一 Python 环境，升级后重启客户端加载新包。 | 已有实现 |
| INSTALL-002 | 旧复制运行时安装需一次迁移；package 模式不得回落源码 checkout 或 managed 指针。 | 已有实现 |
| INSTALL-003 | 支持 Codex/Claude/Qoder/QoderCN CLI，客户端共用操作 Skill。 | 已有实现 |
| INSTALL-004 | 安装自动检测客户端，也支持显式选择；prepare-only 不修改用户注册。 | 已有实现 |
| INSTALL-005 | 客户端权限仅 Saygo 范围，保留用户已有策略、无关配置和备份。 | 已有实现 |
| INSTALL-006 | 卸载仅删自身未被修改的注册/权限，不删用户自定义条目与任务证据。 | 已有实现 |
| INSTALL-007 | 开发安装只写项目配置与 .saygo-dev，不改变用户插件或浏览器桥。 | 已有实现 |
| INSTALL-008 | 安装资源随 wheel/sdist 提供，无源码 checkout 也能 setup。 | 已有实现 |
| INSTALL-009 | 重复 setup 复用环境，正确处理 macOS /var 与 /private/var 路径别名。 | 已有实现 |
| INSTALL-010 | 可选 extras 按需要安装，不强制浏览器扩展用户安装移动工具链。 | 已有实现 |

## UPDATE · 独立检查与更新通知

来源：本次用户要求；updates.py；提交 0fa8e1f、7ff988d。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| UPDATE-001 | 检查、通知、应用升级三个职责分离；automatic=false 不关闭检查和通知。 | 已修复源码/安装交付待验收 |
| UPDATE-002 | package 与 managed 每次 MCP 启动均异步检查，不阻塞 MCP 连接，不向 stdout 写诊断。 | 已修复源码/安装交付待验收 |
| UPDATE-003 | package 返回实际包版本，并报告已知可用版本、链接、pipx 升级命令和重启提示。 | 已修复源码/安装交付待验收 |
| UPDATE-004 | package 禁止 Saygo 自动下载/切换 managed runtime；旧 automatic=true 配置也不得触发应用。 | 已修复源码/安装交付待验收 |
| UPDATE-005 | package 的手动 --check 及无动作 update 实际查询；后台模式也实际查询。 | 已修复源码/安装交付待验收 |
| UPDATE-006 | MCP device_sessions 返回结构化 updates；客户端无需依赖启动日志才能看到结果。 | 已修复源码/安装交付待验收 |
| UPDATE-007 | 读取提醒遇空/过期缓存可触发后台检查，避免仅靠启动器；首次未完成明确 checking 状态。 | 已修复源码/安装交付待验收 |
| UPDATE-008 | 正常近期结果读取使用缓存，不每次工具调用查询网络；错误记录与陈旧结果可区分。 | 已修复源码/安装交付待验收 |
| UPDATE-009 | 比较语义版本数值，默认 stable 排除草稿/预发布；managed beta 保留既有行为。 | 已修复源码/安装交付待验收 |
| UPDATE-010 | package 查默认公共升级源 PyPI 的稳定可用版本，不能仅凭 GitHub 标签宣称 pipx 可升级。 | 已修复源码/安装交付待验收 |
| UPDATE-011 | 外部升级后丢弃同版/旧版提醒；缓存不能让已升级用户继续收到旧提醒。 | 已修复源码/安装交付待验收 |
| UPDATE-012 | 离线、超时、无有效版本保留现运行时，检查错误可见且不阻止设备操作。 | 已修复源码/安装交付待验收 |
| UPDATE-013 | 并发检查用锁与原子写入保护状态；同进程重复通知合并后台请求。 | 已修复源码/安装交付待验收 |
| UPDATE-014 | 损坏/缺失检查缓存不影响 MCP；不能凭损坏状态报告已是最新版。 | 已修复源码/安装交付待验收 |
| UPDATE-015 | package --apply/--auto on 解释 pipx 管理边界；--auto off 可明确保持仅提醒。 | 已修复源码/安装交付待验收 |
| UPDATE-016 | managed 更新保留 SHA256、来源、兼容性检查、独立准备、空闲切换与旧环境留存。 | 已修复源码/安装交付待验收 |
| UPDATE-017 | 修复源码不会自动改变已安装 0.4.12 的 launcher/模块；需交付升级或迁移才能生效。 | 已修复源码/安装交付待验收 |
| UPDATE-018 | 用户已明确授权提交、推送并升到 0.4.14 发布；正式交付前需验证真实安装布局与三平台产物。 | 已修复源码/安装交付待验收 |
| UPDATE-019 | Windows 桌面版与 WSL 按浏览器所在系统发现共享 bridge；启动同步检查包版本、在线目录、实际注册和安装记录，发现失败时保留现有配置，不因同版本跳过修复或另建 bridge。 | 源码回归通过/新版安装产物未发布 |

## RELEASE · 分发与发布验收

来源：distribution/README.md、distribution/PYPI.md；scripts/build_release.py、.github/workflows。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| RELEASE-001 | 源码 ZIP、安装器、扩展包、wheel/sdist 采用白名单，禁止配置、会话、截图、客户资料入包。 | 已有实现/发布须独立验收 |
| RELEASE-002 | 安装器和源码校验 SHA256；拒绝非预期来源与 ZIP 路径穿越。 | 已有实现/发布须独立验收 |
| RELEASE-003 | 构建元数据、包版本与授权标签一致；未获明确授权不得提高版本号。 | 已有实现/发布须独立验收 |
| RELEASE-004 | 仅验收脚本/CI 修复使用原版本与产物，不用升版代替修复。 | 已有实现/发布须独立验收 |
| RELEASE-005 | wheel 在 checkout 外干净环境安装、CLI/MCP 启动与重复 setup 必须验证。 | 已有实现/发布须独立验收 |
| RELEASE-006 | Linux、Windows、macOS 分别验收，不把单平台通过说成全平台通过。 | 已有实现/发布须独立验收 |
| RELEASE-007 | 流水线成功、GitHub release、PyPI 索引可见、商店已提交/审核通过分别核实。 | 已有实现/发布须独立验收 |
| RELEASE-008 | 扩展版本独立，仅扩展文件变更才变更；商店包去除开发 key。 | 已有实现/发布须独立验收 |
| RELEASE-009 | 桌面包在目标系统构建且带校验和，Windows ZIP/macOS DMG/Linux tar.gz 独立验证。 | 已有实现/发布须独立验收 |
| RELEASE-010 | 用户叫停即停止提交、发布和设备操作；记录问题不构成恢复授权。 | 已有实现/发布须独立验收 |

## OTHER · 辅助功能、官网与规划边界

来源：README.md、website.md、perf-plan.md；integrations/figma*、drive、skills。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| OTHER-001 | Figma 用例生成、参考图视觉审查及 QA drive 渲染入口继续保留。 | 部分实现/计划分开 |
| OTHER-002 | 图像预处理技能包含 loading、keyboard、scroll、diff、toast，OCR 等按需启用。 | 部分实现/计划分开 |
| OTHER-003 | 官网展示真实产品入口与支持边界，中英文切换并保存语言偏好。 | 部分实现/计划分开 |
| OTHER-004 | 官网链接安装说明、隐私说明与发布入口，不把未通过审核当商店已发布。 | 部分实现/计划分开 |
| OTHER-005 | 站点部署与包发布区分；自定义域名和跳转按既有配置验证。 | 部分实现/计划分开 |
| OTHER-006 | 全平台支持是目标：完整 macOS、iOS 真机/模拟器、签名公证等未验收项保持待办。 | 部分实现/计划分开 |
| OTHER-007 | 异步离屏 Then 方案已否决，不作为待实现需求；OCR 与弱证据复核是后续计划。 | 部分实现/计划分开 |
| OTHER-008 | 普通说明文档集中 docs，根目录保留 agent.md；SKILL、命令模板、运行时用例/前置条件保留加载路径。 | 部分实现/计划分开 |

## 已知差异和交付顺序

1. 历史 runtime.md 中旧状态目录和精确图像摘要描述已落后于共享服务：以 agent-control.md 与当前 Runtime 为准，修正文档不能弱化观察校验。
2. package 安装此前在启动、notice、CLI 三处提前返回，使检查和提醒一起丢失；本轮补需求和测试后修复。
3. README 中旧商店状态为历史表述，当前审核/上线状态必须在实际发布验收时单独查询，文档整理不冒充在线核实。
4. 完整需求 → 不少于 500 条独立 BDD/自动化用例 → 更新逻辑修复 → 回归验证。真实设备、商店和跨平台未执行项明确保留，不伪造通过。
