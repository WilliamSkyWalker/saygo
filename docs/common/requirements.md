# Saygo 需求基线

[公共文档](README.md) · [测试与验收](testing/README.md) · [历史证据](history/README.md)

整理日期：2026-10-12。依据仓库实现、现有需求、测试与归档记录整理，不推定仓库外历史对话，也不把代码缺陷当作正确需求。保留全部原需求编号，作为变更和测试追踪的稳定入口。

## 需求总索引

当前共 **483 条编号条目**：本文件 **256 条**（保留原 187 条并补充 69 条），六端独立清单 **227 条**。公共要求与端内细化有继承关系，数量用于维护定位，不代表独立功能数量或测试覆盖率。

本文件维护公共/历史模块需求和总索引；各端完整操作需求分别维护在下列文件，不能只看原 MOBILE/NATIVE/BROWSER 汇总就认为六端已经列全。

| 操作端 | 独立清单 | 编号范围 | 条目数 |
| --- | --- | --- | --- |
| Windows | [Windows需求](../windows/requirements.md) | WIN-001～WIN-036 | 36 |
| macOS | [macOS需求](../macos/requirements.md) | MAC-001～MAC-037 | 37 |
| Android | [Android需求](../android/requirements.md) | AND-001～AND-042 | 42 |
| iOS | [iOS需求](../ios/requirements.md) | IOS-001～IOS-034 | 34 |
| Chrome/Edge 扩展 | [Chrome/Edge 扩展需求](../browser-extension/requirements.md) | EXT-001～EXT-045 | 45 |
| Playwright | [Playwright需求](../playwright/requirements.md) | PW-001～PW-033 | 33 |

逐项核对的代码入口、遗漏补充和未满足要求见[代码核对记录](requirements-audit.md)。该记录给出源码与需求域/端清单的对应关系；没有单独自动化或真实证据的条目保持待验收。

## 范围与状态

“缺口”表示代码尚未满足表述的要求；“操作约束”须由调用方遵守，不能当作程序强制保证。“已有实现”表示仓库已有对应代码，不表示本次执行了测试或完整业务已验收。“部分完成”表示明确的能力限制；“待真实验收”表示仍缺指定环境证据。历史发布只按记录中的版本/日期成立，不意味着用户现有安装已升级。

原有 638 条自动化契约覆盖若干需求的输入矩阵及集成边界，不代表每条需求、每个操作端都完成验收。66 条人工验收场景另行记录；未执行和跳过均不算通过。需求、实现、测试场景、实际执行记录应分别维护。

| 归属 | 需求域或编号 | 操作入口与证据 |
| --- | --- | --- |
| common 公共协议 | CORE、SESSION、OBS、TASK、FLOW | [统一操作](operations.md)、[工作流](workflows.md)、control_demo/runtime_demo |
| common 产品与工程 | GUI、QA、PROBE、CONFIG、INSTALL、UPDATE、RELEASE、OTHER | [桌面应用](desktop-app.md)、[QA](qa.md)、[安装](installation.md)、[测试](testing/README.md) |
| Windows | NATIVE-001～004、007，GUI 整机要求 | [Windows](../windows/README.md)、隔离窗口与冻结包证据 |
| macOS | NATIVE-001、002、005～007，GUI 整机要求 | [macOS](../macos/README.md)、原生面板与 arm64 包证据 |
| Android | MOBILE-001～009、011～014 | [Android](../android/README.md)、WSL→Windows 模拟器记录；其他主机/真机另验 |
| iOS | MOBILE-001～004、009、010、014 | [iOS](../ios/README.md)、模拟契约；真机及完整安装链待验收 |
| Chrome/Edge 扩展 | BROWSER-001～011、BRIDGE、UPDATE-019 | [扩展](../browser-extension/README.md)、真实 Chrome 与共享桥记录 |
| Playwright | BROWSER-001、002、004、005、009、010、012 | [Playwright](../playwright/README.md)、CLI/Runtime 真浏览器记录 |

公共会话、观察、接管与不重放规则适用于所有支持的端；端特有能力仍以能力查询和独立验收为准。BROWSER-006～008 的不抢焦点后台截取只适用于扩展，不能套用到 Playwright。

## 功能目录

[产品](#core) · [会话](#session) · [观察](#obs) · [任务](#task) · [工作流](#flow) · [浏览器](#browser) · [桥与网络](#bridge) · [移动端](#mobile) · [桌面驱动](#native) · [桌面应用](#gui) · [QA](#qa) · [Probe](#probe) · [配置](#config) · [安装](#install) · [更新](#update) · [发布](#release) · [辅助功能](#other)

<a id="core"></a>

## CORE · 产品与入口

来源：[文档入口](../README.md)、[架构](architecture.md)；saygo/cli.py、saygo/mcp/server.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| CORE-001 | 外部 Agent 使用共享 CLI/MCP 操作层，无需 Saygo 模型 Key；device profile 可独立启动。 | 已有实现 |
| CORE-002 | 桌面应用由用户配置视觉模型；交互任务复用 Runtime，不建立另一套任务状态语义。 | 已有实现 |
| CORE-003 | 显式 JSON workflow 不要求模型规划；BDD QA 保留独立 run 入口。 | 已有实现 |
| CORE-004 | 视觉决策只向模型提供截图与操作元数据，不提供 DOM 或 UI 树。 | 已有实现 |
| CORE-005 | CLI help 和直接设备控制不得强制加载 QA、OpenAI、Appium 等无关可选依赖。 | 已有实现 |
| CORE-006 | CLI/MCP 同名会话在相同 SAYGO_HOME_DIR 下绑定相同目标；任务库允许 SAYGO_RUNTIME_DIR 覆盖。 | 已有实现 |
| CORE-007 | 输入派发成功、画面稳定和业务成功必须分开表达；成功回执不得代替结果验证。 | 已有实现 |
| CORE-008 | 不支持的平台、动作和能力明确报错；不得偷偷换后端或创建默认手机会话。 | 部分实现；能力声明过宽见 OBS-013 |
| CORE-009 | MCP 的 full/device profile 各有明确工具白名单；device 模式无 QA 密钥/用例目录也可握手，裁剪失败不能静默暴露 full。来源：`mcp/server._apply_profile`。 | 已有实现 |
| CORE-010 | MCP 工具 stdout 只输出协议，辅助日志转 stderr；图片返回 Content 图像块，SDK 兼容范围逐版本验证。来源：`mcp/server._silenced_stdout/_image_result`。 | 已有实现；SDK 全范围不是本次验收 |
| CORE-011 | `device list/sessions`、任务状态、QA run ID 与 workflow run ID 分别解释；命令失败给错误类型/退出码，不混成统一业务通过。来源：`commands/*`、`runtime/cli.py`。 | 已有实现；各入口错误结构仍不同 |
| CORE-012 | API/MCP/CLI、桌面模型循环与 QA 的功能集合有差异，文档需说明实际入口；驱动有方法不等于桌面模型已允许该动作。来源：`desktop/runner.ALLOWED`、`mcp/server`、`commands/device`。 | 持续约束；已有部分入口限制 |

<a id="session"></a>

## SESSION · 会话与资源

来源：[统一操作](operations.md)；saygo/devices/control.py、saygo/runtime/locking.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| SESSION-001 | 命名会话持久化平台、设备、浏览器页或桌面窗口绑定，重连不得暗中改绑。 | 部分实现；macOS 前台重连按应用重新选窗，见 MAC-004 |
| SESSION-002 | 设备发现区分在线、离线、未授权；多候选要求选择，单候选才允许自动选择。 | 已有实现 |
| SESSION-003 | 会话列表区分保存记录、明确断开和后端策略不可用；真实在线状态通过实际请求诊断，不能由文件存在推定。 | 已有列表/诊断实现；sessions 本身不探活 |
| SESSION-004 | 连接、断开与停止分开；断开控制器不得默认关闭用户浏览器或模拟器。 | 已有实现 |
| SESSION-005 | 会话 handoff 阻止自动输入，resume 获取新观察，接管不代表业务已完成。 | 已有实现 |
| SESSION-006 | 任务在 idle、waiting_for_human、needs_review 状态持续持有资源。 | 已有实现 |
| SESSION-007 | 普通 device 命令与任务入口遵守同一资源归属和 OS 操作锁。 | 已有实现 |
| SESSION-008 | 本地桌面窗口共享输入锁；锁的保证范围仅限 Saygo 自身。 | 已有实现 |
| SESSION-009 | 项目别名保存在 .saygo/resources.json；别名与物理设备 ID 区分。 | 已有实现 |
| SESSION-010 | 调用方使用与任务匹配的独立浏览器会话；失效显式选页，不借用其他业务会话。程序维持目标绑定，但不识别业务目的。 | 操作约束；程序不能独立证明任务与会话匹配 |
| SESSION-011 | 命名会话校验路径安全，持久绑定通过临时文件和原子替换写入；损坏状态不能作为可用会话。来源：`platforms/device_session._key/save_state/load_state`。 | 已有实现 |
| SESSION-012 | `resources list/bind` 原子维护项目资源别名，bind 要求已有会话，未提供 task bindings 时从项目配置读取。来源：`commands/doctor.resources`、`commands/task.dispatch`。 | 已有实现 |
| SESSION-013 | `doctor --session` 返回诊断、能力与真实截图可读性；未给显式 probe-action 时不得派发输入，必须标 input_check 未测试。来源：`commands/doctor.diagnose`。 | 已有实现 |
| SESSION-014 | 相同物理设备、桌面或共享扩展桥不能因换别名、任务库目录或入口而绕过资源占用；拒绝原因指出占用者。来源：`runtime/locking.py`。 | 已有实现；QA 的等价覆盖未承诺 |

<a id="obs"></a>

## OBS · 观察与动作

来源：[观察与动作](operations.md#观察坐标和动作)；saygo/devices/observations.py、saygo/devices/actions.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| OBS-001 | 观察包含唯一 ID、时间、会话、目标、截图与屏幕尺寸以及坐标映射。 | 已有实现 |
| OBS-002 | 支持 screen、percent、image、crop 坐标；image/crop 必须有来源观察。 | 已有实现 |
| OBS-003 | 百分比坐标 0–100，边缘落在最后有效像素；拒绝布尔值、非数、无穷和越界。 | 已有实现 |
| OBS-004 | 裁剪保留原图映射及放大倍率；不把截图像素当作 CSS 或设备逻辑像素。 | 已有实现 |
| OBS-005 | 依赖画面的动作使用来源观察，并拒绝超过 30 秒或已失效的目标；设备旧接口与 task 的强制程度须区分。 | 部分实现；详见 OBS-014 |
| OBS-006 | 带观察动作派发前核对页面、URL、窗口、进程、边界、尺寸和像素变化；局部目标变化须拒绝。 | 已有实现；不代表无观察参数的旧入口同样校验 |
| OBS-007 | 动作能力由实际后端公布，含指针、触摸、文字、按键、滚动及页面操作。 | 已有实现 |
| OBS-008 | 输入、URL、按键、应用及页面 ID 必须非空；长按时间与滚动幅度须有界。 | 已有实现 |
| OBS-009 | 动作可请求后截图；截图失败记录为证据错误，不重放已确认输入。 | 已有实现 |
| OBS-010 | 稳定/变化等待有时间上限并返回 condition_met/timed_out，不宣称业务成功。 | 已有实现 |
| OBS-011 | 每次滚动观察目标区域，首次约半屏校准，连续浏览按可见高度 85–90% 保留重叠，接近目标 10–20%，无变化先诊断再决定。 | 已有提示与桌面前后图；不是所有驱动强制的位移算法 |
| OBS-012 | MCP 观察及有观察的动作返回图像内容；CLI 返回图像路径和元数据。 | 已有实现 |
| OBS-013 | 输入能力应按端和模式公布：手机只启动应用、浏览器只导航页面，不能由统一 BASE 集合推导所有端均支持 open_url/open_app。来源：`devices/actions.capabilities`、各驱动 open_target。 | 缺口：BASE 仍普遍包含两类动作 |
| OBS-014 | 依赖画面的操作须携带原观察；明确说明旧 tap/input/key/type-send 及无 observation_id 的 act 没有相同的来源观察保护。来源：`devices/service._execute`。 | 部分实现：task 强制，低级设备接口未统一强制 |
| OBS-015 | 每次观察保存独立源图、SHA256 与元数据，自定义输出路径覆盖不得破坏已保存观察证据；裁剪扩大 2 倍仍能映射回原坐标。来源：`devices/observations.capture/load`。 | 已有实现 |
| OBS-016 | 变化检测比较尺寸和超过强度阈值的像素；stable 连续约 0.6 秒不超阈值、change 相对初图检测，1 次稳定不等于业务结果。来源：`devices/observations.change_fraction/wait`。 | 已有实现；底层截图耗时仍取决于驱动 |
| OBS-017 | 普通 device 操作记录 operation_id、请求、派发意图、结果及后截图，落盘失败应可见；日志不等同 task 的跨调用去重。来源：`devices/service.execute/_record`。 | 已有实现；普通 device 无调用方 request_id 去重 |
| OBS-018 | type-send 明确草稿/提交、替换/追加、发送坐标与等待时间；异常返回是否尝试提交，结果未知先观察，不能直接再调用。来源：`commands/device`、`devices/service`。 | 已有实现；复合步骤不是逐动作核验 |
| OBS-019 | 跨端滚动统一描述内容方向与手势方向，公开定点单位、幅度和默认位置；应用未滚动不能判成功。来源：`devices/scrolling.py`、各驱动滚动方法。 | 部分实现：移动手势与桌面方向名称不同 |
| OBS-020 | 所有图像源必须检查新鲜度，帧流中断不得无限复用旧帧，回落截图失败则报告不可观察。来源：`platforms/mjpeg.latest`、`appium.screenshot_raw`。 | 缺口：MJPEG 无帧龄检查且断流不清缓存 |
| OBS-021 | 输入发生不确定异常时停止并核对，不能在同一调用中换驱动路径再次输入。来源：`platforms/appium.input_text`。 | 缺口：Android/iOS 均有异常后备输入路径 |

<a id="task"></a>

## TASK · 交互任务与恢复

来源：[交互任务](operations.md#跨端交互任务)；saygo/runtime/interactive.py、saygo/runtime/store.py。

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
| TASK-012 | 完整手机注册→邮箱激活→桌面确认需要真实业务验收；模拟测试不构成通过证明。 | 待真实跨端业务验收 |
| TASK-013 | task list/status/events/timeline 提供持久任务与时间顺序事实；annotation 作为解释单独记录，不能覆盖原始动作结果。来源：`runtime/interactive.call/timeline`、`runtime/store`。 | 已有实现 |
| TASK-014 | 同一 request_id 携带不同资源、动作或观察须拒绝；同请求即使进程重启也不重复派发。来源：`runtime/interactive.submit`。 | 已有实现 |
| TASK-015 | 任务导出包含状态、时间线、事件及存在的观察文件；导出中截图/输入可能有敏感内容，位置由调用方指定。来源：`runtime/interactive.export`。 | 已有实现 |
| TASK-016 | 交互任务默认存于 SAYGO_HOME_DIR/runtime，可用 SAYGO_RUNTIME_DIR 覆盖；不得误写成显式 workflow 默认也相同。来源：`runtime/interactive.default_store`。 | 已有实现 |

<a id="flow"></a>

## FLOW · 声明式工作流

来源：[工作流](workflows.md)；saygo/runtime/schema.py、engine.py、resources.py。

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
| FLOW-011 | 没有通用数据库写入、任意 API/MCP 连接器及远程接管 UI。 | 当前不支持；后续计划 |
| FLOW-012 | create 仅校验保存，start 先输出持久 run ID 再执行；run/recover/status/events/pause/cancel/resume/resolve 各自不混用。来源：`runtime/cli.dispatch`。 | 已有实现 |
| FLOW-013 | 显式 workflow 默认库为当前目录 .saygo_runs/runtime；state-dir 参数优先，SAYGO_RUNTIME_DIR 为环境默认，跨进程操作需选择同一库。来源：`runtime/cli.register`。 | 已有实现；与交互任务默认不同 |
| FLOW-014 | 暂停/取消是协作请求，不撤销已派发输入；取消优先级高于暂停，恢复不能自动重放未知动作。来源：`runtime/store.request`、`runtime/engine`。 | 已有实现 |
| FLOW-015 | 检查点与事件在 SQLite 事务中保存，独立 OS 文件锁防止双执行器，崩溃后可核对持久意图。来源：`runtime/store.py`。 | 已有实现 |
| FLOW-016 | SQLite 查询使用只读 URI 和 authorizer，拒绝扩展/文件读写函数；执行约 3 秒预算、最多 1000 行，超限报错。来源：`runtime/resources.SQLiteResource.call`。 | 已有实现 |
| FLOW-017 | 桌面资源支持保存会话或内联应用，移动/浏览器需明确会话；人工 resume 数据保持 JSON 类型，验证步骤仍执行。来源：`runtime/schema.py`、`runtime/engine.py`。 | 已有实现 |

<a id="browser"></a>

## BROWSER · 浏览器会话与视觉操作

来源：[扩展](../browser-extension/README.md)、[Playwright](../playwright/README.md)；saygo/platforms/browser_extension.py、browser_playwright.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| BROWSER-001 | MCP 与桌面版默认扩展后端；Playwright 仅 CLI/Runtime，QA 可用 Selenium。 | 已有实现 |
| BROWSER-002 | MCP 对 Playwright 的连接、观察、动作及可执行任务恢复拒绝，审计与取消仍可用。 | 已有实现 |
| BROWSER-003 | 扩展使用当前浏览器登录状态，不读取 DOM 为视觉决策提供语义。 | 已有实现 |
| BROWSER-004 | 浏览器按稳定 page ID 绑定，创建、列出、选择、关闭页面都保留证据。 | 已有实现 |
| BROWSER-005 | 关闭已选页后明确无截图，不擅自选择其他页。 | 已有实现 |
| BROWSER-006 | 扩展后端：后台截图针对绑定页，不要求手动前置；失败返回结构化诊断及超时信息。 | 已有实现 |
| BROWSER-007 | 扩展后端：首次后台截取允许页面绘制预热，截图期限有界，失败不自动断开扩展。 | 已有实现 |
| BROWSER-008 | 扩展后台截图和普通视觉输入不主动激活标签/窗口；显式 select-page 会前置；受保护页面明确失败。 | 已有实现；不把选页描述成不抢焦点 |
| BROWSER-009 | scroll_at 命中指定滚动区域，单位 100 CSS 像素，正数向上且允许小数。 | 已有实现 |
| BROWSER-010 | 指针支持 hover、双击、右键、长按、拖动和能力允许的 hotkey。 | 已有实现 |
| BROWSER-011 | 已连接扩展更新不强行踢掉现有连接；显式重连后使用新桥。 | 已有实现 |
| BROWSER-012 | Playwright/CDP 控制器退出只断开连接，浏览器和稳定 target ID 会话可恢复。 | 已有实现 |

<a id="bridge"></a>

## BRIDGE · 扩展桥与网络记录

来源：[扩展桥和网络](../browser-extension/README.md)；saygo/integrations/browser_bridge.py、extensions/saygo-browser/。

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

<a id="mobile"></a>

## MOBILE · 移动端与模拟器

来源：[Android](../android/README.md)、[iOS](../ios/README.md)；saygo/devices/mobile.py、simulator.py、mobile_host.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| MOBILE-001 | Android/iOS 视觉动作通过 Appium；adb/simctl 用于发现与生命周期，不旁路视觉控制。 | 已有实现；按端记录硬件验收 |
| MOBILE-002 | 连接现有手机不默认重置设备或打开应用，设备授权由用户完成。 | 已有实现；按端记录硬件验收 |
| MOBILE-003 | Android 使用 UiAutomator2 与 Unicode 输入；iOS 使用 XCUITest 与已有签名配置。 | 已有实现；按端记录硬件验收 |
| MOBILE-004 | MJPEG 无可用新帧时回落 Appium 截图，不把旧帧或无帧作为当前画面。 | 部分实现：无帧/解码失败可回落，帧龄检查缺失，见 OBS-020 |
| MOBILE-005 | Android 安装计划包含主机、磁盘、加速与工具组件，dry-run 不安装或下载。 | 已有实现；按端记录硬件验收 |
| MOBILE-006 | 安装复用 SDK/Java/AVD，直接下载文件校验 SHA256，失败返回真实错误。 | 已有实现；按端记录硬件验收 |
| MOBILE-007 | 同名 AVD 异镜像拒绝覆盖；已有运行 AVD 按名称复用，不随意选择别台设备。 | 已有实现；按端记录硬件验收 |
| MOBILE-008 | Android SDK license 显式接受；空间不足、加速缺失不假成功，不修改 BIOS。 | 已有实现；按端记录硬件验收 |
| MOBILE-009 | boot 等待启动完成；超时保留模拟器与日志供诊断。 | 已有实现；按端记录硬件验收 |
| MOBILE-010 | iOS 模拟器依赖 macOS/full Xcode；Windows/Linux/WSL 不伪装本地支持。 | 已有实现；按端记录硬件验收 |
| MOBILE-011 | WSL 无可用 KVM 时可选 Windows host；显式 local/windows 选择优先。 | 已有实现；按端记录硬件验收 |
| MOBILE-012 | Windows 私有 Python/Node/Appium 不替换全局 PATH；只复制允许的 worker 文件。 | 已有实现；按端记录硬件验收 |
| MOBILE-013 | Windows Appium 仅 loopback，WSL token relay 不添加防火墙规则，不重放失败请求。 | 已有实现；按端记录硬件验收 |
| MOBILE-014 | 手机真机和完整 iOS 配置链需设备验证；不得把模拟测试报告为硬件已验收。 | 已有实现；按端记录硬件验收 |

<a id="native"></a>

## NATIVE · 本地与后台桌面驱动

来源：[Windows](../windows/README.md)、[macOS](../macos/README.md)；saygo/platforms/desktop*。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| NATIVE-001 | Windows 原生及 WSL runner、macOS 原生窗口驱动共享动作语义。 | 已有实现；应用及模式兼容有限 |
| NATIVE-002 | 窗口绑定核对窗口 ID、PID 和边界，目标改变时拒绝旧坐标。 | 已有实现；应用及模式兼容有限 |
| NATIVE-003 | Windows background 不支持动作明确失败，不回落全局键鼠或快捷键。 | 已有实现；应用及模式兼容有限 |
| NATIVE-004 | Windows foreground 恢复/前置必须显式选择，不因截图失败自动启用。 | 已有实现；应用及模式兼容有限 |
| NATIVE-005 | macOS background 不激活/启动应用、不用全局键鼠或剪贴板、不前台回退。 | 已有实现；应用及模式兼容有限 |
| NATIVE-006 | macOS 内部 AX 仅做坐标命中与原生执行，不给模型控件树或文本定位。 | 已有实现；应用及模式兼容有限 |
| NATIVE-007 | macOS 后台拒绝锁屏、非当前桌面及身份不明窗口；Windows 需按捕获和输入方式独立核验，单面板不代表任意应用兼容。 | macOS 后台已有保护；Windows 不承诺相同系统状态检测 |
| NATIVE-008 | Linux 本地窗口自动化未实现；RDP 为独立实验性远程会话，不是 Linux 原生桌面支持。 | Linux 未实现；RDP 实验实现，见 OTHER-014 |

<a id="gui"></a>

## GUI · 桌面产品与模型

来源：[桌面应用](desktop-app.md)、[桌面回归](testing/desktop.md)；saygo/desktop/app.py、runner.py、model.py、connections.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| GUI-001 | Qt 6 对话界面含任务历史、消息输入、截图、模型设置和连接管理。 | 已有实现；完整模型任务待验收 |
| GUI-002 | 支持任务开始、暂停、人工回复继续、取消、恢复、证据导出。 | 已有实现；完整模型任务待验收 |
| GUI-003 | 模型配置为 OpenAI-compatible 视觉 API，连接测试发送测试图而非只测文本。 | 已有实现；完整模型任务待验收 |
| GUI-004 | HTTPS 端点或本机 HTTP；拒绝凭据 URL、查询串、片段、远程明文及重定向。 | 已有实现；完整模型任务待验收 |
| GUI-005 | Key 仅内存或受支持 OS keyring，禁止明文 fallback，desktop.json 不含 Key。 | 已有实现；完整模型任务待验收 |
| GUI-006 | 模型错误输出不回显 provider body 或密钥，超时和 HTTP 错误给可用提示。 | 已有实现；完整模型任务待验收 |
| GUI-007 | 每轮模型一个动作；截图失败不可用旧帧代替，不可在观察失败时宣称完成。 | 已有实现；完整模型任务待验收 |
| GUI-008 | 连续观察失败或诊断修复达到界限后 handoff，避免无限恢复循环。 | 已有实现；完整模型任务待验收 |
| GUI-009 | 原生 Windows/macOS 自动连接本机；任务时最小化，接管或结束恢复界面。 | 已有实现；完整模型任务待验收 |
| GUI-010 | 可发现本机应用入口；启动校验已列出的入口和本机绑定，记录 durable intent。 | 已有实现；完整模型任务待验收 |
| GUI-011 | 应用启动可不依赖桌面像素保持不变；点击输入仍要完整观察校验。 | 已有实现；完整模型任务待验收 |
| GUI-012 | 自动检测浏览器不激活标签页，不在任务/人工接管期间改绑；浏览器按需加入观察。 | 已有实现；完整模型任务待验收 |
| GUI-013 | 高级连接保留窗口/手机，用户可取消本次任务不用的目标。 | 已有实现；完整模型任务待验收 |
| GUI-014 | Windows 便携包无需 Python/WSL，GUI 无控制台，host 使用独立 stdio 可执行文件。 | 已有实现；完整模型任务待验收 |
| GUI-015 | macOS DMG、签名、公证、干净机器及真实模型任务必须分别记录验收，不能仅凭打包脚本宣称完成。 | arm64 DMG 有历史验收；签名/公证及用户真机任务待验收 |
| GUI-016 | 模型决策只能引用绑定资源并使用受支持 kind/action；坐标须百分比，note 必填，格式错误最多三次后接管。来源：`desktop/runner.decision/TaskLoop.run`。 | 已有实现；真实模型验收另计 |
| GUI-017 | 模型请求过程中发生用户暂停/停止，返回后须先处理停止信号再派发动作。来源：`desktop/runner.TaskLoop.run`。 | 已有实现 |
| GUI-018 | 循环默认每次最多 30 轮，连续观察/恢复失败有界接管；不能无限重试同一故障或在观察失败时宣布完成。来源：`desktop/runner.TaskLoop.run`。 | 已有实现 |
| GUI-019 | 默认先观察整机，浏览器按模型显式观察请求加入；滚动保留前图和动作供比较，避免滚动后失去定位依据。来源：`desktop/runner.py`。 | 已有实现 |
| GUI-020 | 应用清单来自 Windows 开始菜单/应用目录、macOS 应用包目录，不是完整软件资产清单，也不把清单文字当指令。来源：`devices/applications.py`、`desktop/runner.SYSTEM`。 | 已有实现 |
| GUI-021 | 连接 Chrome 可安装桥并打开商店，在线检测做真实 pages 请求，手动重试/高级连接不在运行任务中更换绑定。来源：`desktop/connections.py`、`desktop/app.py`。 | 已有实现；商店/实际安装需另核验 |
| GUI-022 | 桌面产品默认中文界面，后台线程执行模型/连接任务，历史任务、截图、继续和导出应关联所选任务。来源：`desktop/app.py`、`desktop/theme.py`。 | 已有实现；UI 自动化不等于真实模型任务 |
| GUI-023 | 取消记住密钥不自动删除旧凭据；显式删除成功后清空输入，显示/隐藏状态在关闭设置后恢复遮罩，配置变化使旧测试反馈失效。来源：`desktop/app.py`、`desktop/model.py`。 | 已有实现；OS 凭据后端分别验收 |
| GUI-024 | 模型调用会发送截图、任务文字与应用入口清单，用户选择提供方；当前只实现 OpenAI-compatible 协议，不宣称支持其他供应商的原生协议。来源：`desktop/model.py`、`desktop/runner.py`。 | 已有实现；真实端点需单独测试 |
| GUI-025 | 示例任务只填入输入框不自动执行；Enter 提交、Shift+Enter 换行，人工接管时回复继续当前任务，运行中禁止改绑。来源：`desktop/app.py`。 | 已有实现 |
| GUI-026 | 桌面内置自动更新、流式聊天、图形化手机工具链向导和签名安装器分别列为未提供；托管 Agent 更新和命令行安装不能代替这些桌面能力。来源：`desktop/app.py`、`desktop/model.py`、`updates.py`。 | 当前未实现；签名/公证亦未完成 |

<a id="qa"></a>

## QA · BDD QA 与判定

来源：[QA](qa.md)、[性能实现与计划](performance.md)；saygo/qa/gherkin.py、agent.py、step_validator.py。

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
| QA-015 | 性能优化同时衡量墙钟、调用量与通过率；OCR 确定性交叉核验与对抗复核仍属计划。 | 已有部分性能实现；交叉核验/复核未实现 |
| QA-016 | run 接受单文件、目录、目标名、Markdown TC 块、文本及 Gherkin 用例；new/list 提供目标模板与发现，创建时保护已有文件。来源：`commands/targets`、`qa/cases._resolve_test_target`。 | 已有实现 |
| QA-017 | 平台标签是集合且只做筛选，manual/partial/skip/wip 不伪装通过；不因一个 android/ios 标签自动切换驱动。来源：`qa/gherkin`、`qa/cases`。 | 已有实现；旧 both 仍作为兼容无限制值 |
| QA-018 | 前置条件 prepend 到每条用例，账号占位符按 worker 替换，运行时 epoch/uuid 数据逐场景生成；普通输入变体用 Examples。来源：`qa/cases`、`commands/run`。 | 已有实现 |
| QA-019 | 并行设备需要足够独立账号，账号不足应拒绝或明确提示共享，不能静默复用首账号导致干扰。来源：`qa/execution._run_dispatched_devices`。 | 缺口：当前不足时回退 accounts[0] |
| QA-020 | 多 Android 设备用共享动态队列，各 worker 固定设备与账号，部分设备初始化失败可降级并记录，全部失败则终止。来源：`qa/execution._run_dispatched_devices`。 | 已有实现；账号不足例外见 QA-019 |
| QA-021 | 手动 shard N/M 使用 0 起始连续切片，校验范围；非法分片终止，不能默默跑全集。来源：`commands/run.cmd_run`。 | 已有实现 |
| QA-022 | Selenium Grid 并发复用有限 Agent 池并聚合结果；只清理本任务所有的会话，不能删除共享 Grid 上其他用户会话。来源：`qa/execution._run_concurrent`、`platforms/selenium_grid.py`。 | 部分实现；清理无所有权过滤，见代码核对记录 |
| QA-023 | 后台 QA 返回 run ID、PID、日志和元数据，status/MCP 查询区分运行、完成、异常退出及产物路径，不把陈旧元数据当活进程。来源：`commands/background.py`、`mcp/server`。 | 已有实现 |
| QA-024 | MCP full 提供目标/用例分页、启动目标/单例、取消、状态、日志尾部与 JSON/HTML 报告；设备模式不混入这些跑测工具。来源：`mcp/server.py`。 | 已有实现 |
| QA-025 | 报告支持 JSON 与含截图 HTML，汇总 pass/fail/skipped/error 并保留用例、步骤、耗时、设备和 probe 未验证项。来源：`qa/report.py`。 | 已有实现 |
| QA-026 | 分层模型独立选择 Brain/Planner/Locator 与定位端点；空配置回落规则明确，桌面模型客户端与 QA 模型客户端分别配置。来源：`config.py`、`qa/brain.py`、`vision/locator.py`。 | 已有实现 |
| QA-027 | QA 的外部 MCP 工具来自私有配置，可调用声明的工具并保存上下文；这不是 workflow 已提供通用 API/MCP 连接器。来源：`mcp/client.py`、`qa/brain._call_with_tools`。 | 已有实现；工具效果需单独核验 |
| QA-028 | QA 直接平台动作和重置路径与 device 服务分别核验，不声称自动享有相同持久去重、资源锁和观察 ID 保护。来源：`qa/agent.py`、`qa/device_setup.py`。 | 实现边界；统一保护待补齐 |
| QA-029 | 参考图从用例 ref 元数据加载并参与视觉比对；图像差、OCR 提示或文本证据校验不能代替独立的业务事实验证。来源：`qa/agent._load_reference_images`、`qa/step_validator`。 | 已有实现；确定性交叉核验仍是计划 |

<a id="probe"></a>

## PROBE · 非视觉断言

来源：[非视觉断言](probes.md)；saygo/probes/spec.py、base.py、subprocess_probe.py。

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
| PROBE-009 | 注册表可展开环境变量；子进程插件可使用独立依赖，Python 类插件在当前 Python 中导入；配置和客户插件不公开。 | 已有实现；不能把依赖隔离保证套到 Python 类插件 |
| PROBE-010 | probes list/check 可不执行 UI，支持目标上下文、since-s 时间窗、wait/timeout 与 JSON 结果；不将纯查询混成 only-probes 的运行语义。来源：`commands/probes.py`。 | 已有实现 |
| PROBE-011 | 每个 case 的插件 setup/check/teardown 和 session 缓存有生命周期；未知注册名直接 fail，插件自身异常为 inconclusive。来源：`probes/ProbeRunner`。 | 已有实现 |
| PROBE-012 | 子进程按 JSON 传请求/上下文并读取结果，限制单次超时；崩溃、空输出和非法 verdict 保留错误，不能算 pass。来源：`probes/subprocess_probe.py`、`probes/base.py`。 | 已有实现 |
| PROBE-013 | probe 轮询有总预算及最大尝试次数，报告中的大块数据受长度限制，截断必须可见。来源：`probes/__init__.py`、`qa/agent._run_probe_step`。 | 已有实现 |

<a id="config"></a>

## CONFIG · 配置与凭据

来源：[私有配置](installation.md#私有配置)；saygo/config.py。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| CONFIG-001 | 优先级 defaults→用户 config.env→项目 .env 或显式文件→进程环境。 | 已有实现 |
| CONFIG-002 | 显式 SAYGO_CONFIG_FILE 缺失必须报错，不从包目录搜配置。 | 已有实现 |
| CONFIG-003 | init/init --user 创建模板不覆盖原文件，POSIX 权限仅 owner。 | 已有实现 |
| CONFIG-004 | 安装只保存配置文件引用，不复制密钥内容，升级保留引用。 | 已有实现 |
| CONFIG-005 | 公开代码、测试、示例与提交记录使用脱敏数据，客户用例独立私有管理。 | 已有实现 |
| CONFIG-006 | 日志、报告与网络记录用途清晰，敏感资料不进入发布白名单。 | 已有实现 |
| CONFIG-007 | 环境变量分组覆盖模型、Appium、浏览器、桌面、RDP、QA、图像技能和 probes；入口专用参数需说明，不因同名字段就推定所有入口都读取。来源：`config.py`、各 commands。 | 已有实现；入口存在差异 |
| CONFIG-008 | 外部 MCP 配置支持 command/args/env 与工具名映射，环境占位符在启动时展开；未配置文件时视为空注册表。来源：`mcp/client.load_clients_config`。 | 已有实现 |
| CONFIG-009 | 日志可按 worker/case 区分、verbose 提供诊断；凭据脱敏需包括所有敏感字段，不能仅屏蔽名称含 pass/secret 的账号字段。来源：`logger.py`、`qa/execution.py`。 | 部分实现：其他账号字段可能入日志 |

<a id="install"></a>

## INSTALL · 安装、客户端与隔离

来源：[安装](installation.md)、[包验收](release.md)；scripts/install_agent_plugin.py、scripts/check_python_package.py。

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
| INSTALL-011 | 安装可选 chrome/edge/none、mobile 依赖、Playwright 浏览器、配置引用和独立根目录；未选组件不得强制下载。来源：`scripts/install_agent_plugin.py`。 | 已有实现 |
| INSTALL-012 | 包安装入口与开发源码入口分开，插件 launcher 在客户端缓存目录外也能定位 runtime，不依赖源码相对路径。来源：`saygo/setup.py`、`plugins/saygo-device/scripts/saygo_mcp.py`。 | 已有实现 |
| INSTALL-013 | 客户端安装生成对应 MCP/Skill/命令入口；Claude marketplace 兼容入口保留，更新后客户端需重启加载。来源：`scripts/install_agent_plugin.py`、`plugins/saygo-device`。 | 已有实现；实际客户端加载另验 |

<a id="update"></a>

## UPDATE · 独立检查与更新通知

来源：[更新机制](installation.md#更新通知与托管升级)；saygo/updates.py；[0.4.14 记录](history/release-0.4.14.md)、[0.4.16 记录](history/release-0.4.16.md)。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| UPDATE-001 | 检查、通知、应用升级三个职责分离；automatic=false 不关闭检查和通知。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-002 | package 与 managed 每次 MCP 启动均异步检查，不阻塞 MCP 连接，不向 stdout 写诊断。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-003 | package 返回实际包版本，并报告已知可用版本、链接、pipx 升级命令和重启提示。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-004 | package 禁止 Saygo 自动下载/切换 managed runtime；旧 automatic=true 配置也不得触发应用。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-005 | package 的手动 --check 及无动作 update 实际查询；后台模式也实际查询。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-006 | MCP device_sessions 返回结构化 updates；客户端无需依赖启动日志才能看到结果。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-007 | 读取提醒遇空/过期缓存可触发后台检查，避免仅靠启动器；首次未完成明确 checking 状态。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-008 | 正常近期结果读取使用缓存，不每次工具调用查询网络；错误记录与陈旧结果可区分。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-009 | 比较语义版本数值，默认 stable 排除草稿/预发布；managed beta 保留既有行为。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-010 | package 查默认公共升级源 PyPI 的稳定可用版本，不能仅凭 GitHub 标签宣称 pipx 可升级。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-011 | 外部升级后丢弃同版/旧版提醒；缓存不能让已升级用户继续收到旧提醒。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-012 | 离线、超时、无有效版本保留现运行时，检查错误可见且不阻止设备操作。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-013 | 并发检查用锁与原子写入保护状态；同进程重复通知合并后台请求。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-014 | 损坏/缺失检查缓存不影响 MCP；不能凭损坏状态报告已是最新版。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-015 | package --apply/--auto on 解释 pipx 管理边界；--auto off 可明确保持仅提醒。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-016 | managed 更新保留 SHA256、来源、兼容性检查、独立准备、空闲切换与旧环境留存。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-017 | 修复源码不会自动改变已安装 0.4.12 的 launcher/模块；需交付升级或迁移才能生效。 | 已有实现；历史包验收见 0.4.14 |
| UPDATE-018 | 每次发布前取得当次明确授权，并验证真实安装布局及三平台产物；历史 0.4.14 授权不延伸至后续发布。 | 持续约束；每次发布独立验收 |
| UPDATE-019 | Windows 桌面版与 WSL 按浏览器所在系统发现共享 bridge；启动同步检查包版本、在线目录、实际注册和安装记录，发现失败时保留现有配置，不因同版本跳过修复或另建 bridge。 | 已有实现；历史发布验收见 0.4.16 |

<a id="release"></a>

## RELEASE · 分发与发布验收

来源：[发布流程](release.md)；scripts/build_release.py、.github/workflows/；每次发布独立留证。

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

<a id="other"></a>

## OTHER · 辅助功能、官网与规划边界

来源：[QA 辅助工具](qa.md)、[官网](website.md)、[性能计划](performance.md)；saygo/integrations/figma*、drive、skills。

| 编号 | 验收需求 | 实现状态 |
| --- | --- | --- |
| OTHER-001 | Figma 用例生成、参考图视觉审查及 QA drive 渲染入口继续保留。 | 按条目区分现有能力与计划 |
| OTHER-002 | 图像预处理技能包含 loading、keyboard、scroll、diff、toast，OCR 等按需启用。 | 按条目区分现有能力与计划 |
| OTHER-003 | 官网展示真实产品入口与支持边界，中英文切换并保存语言偏好。 | 按条目区分现有能力与计划 |
| OTHER-004 | 官网链接安装说明、隐私说明与发布入口，不把未通过审核当商店已发布。 | 按条目区分现有能力与计划 |
| OTHER-005 | 站点部署与包发布区分；自定义域名和跳转按既有配置验证。 | 按条目区分现有能力与计划 |
| OTHER-006 | 全平台支持是目标：完整 macOS、iOS 真机/模拟器、签名公证等未验收项保持待办。 | 待验收/后续计划；macOS 部分能力已有实测 |
| OTHER-007 | 异步离屏 Then 方案已否决，不作为待实现需求；OCR 与弱证据复核是后续计划。 | 异步方案已否决；OCR/复核未实现 |
| OTHER-008 | docs 使用中文并按 common 与六端组织；根目录统一为 AGENTS.md；有效的统一 Skill、命令模板、运行时用例/前置条件保留加载路径，移除旧 Claude 专用 saygo-drive Skill。 | 本次文档结构调整；运行资源保留原位 |
| OTHER-009 | Figma frames 支持 URL/文件键与页面过滤，gen-tests 生成用例，review 可用现有截图或现场截图并导出 JSON/HTML。来源：`commands/figma.py`、`integrations/figma_ops.py`。 | 已有实现；外部服务验收另计 |
| OTHER-010 | Figma 可通过私有 MCP 工具映射或 REST 获取设计数据/PNG；设计稿元数据不等于向设备视觉操作提供 DOM/UI 树。来源：`integrations/figma.py`、`figma_via_mcp.py`。 | 已有实现；CLI 当前仍预检 FIGMA_TOKEN |
| OTHER-011 | 旧 drive JSONL 渲染器保留步骤、截图、状态及错误生成 HTML，删除旧专用 Skill 不删除该可执行能力。来源：`drive/render.py`。 | 已有实现 |
| OTHER-012 | 图像技能按配置顺序执行：加载、键盘、滚动、图像差、提示检测及可选裁剪/OCR/颜色/布局；不适用可跳过，异常记录且不直接判业务成功。来源：`skills/__init__.py` 及各技能。 | 已有实现；OCR 自动交叉裁决未实现 |
| OTHER-013 | Selenium QA 保留本地/远程 Grid、窗口尺寸、截图与坐标鼠标键盘；不能把它的生命周期、页面管理与扩展/Playwright 混用。来源：`platforms/browser.py`。 | 已有实现；共享 Grid 清理存在缺口 |
| OTHER-014 | RDP 通过独立 Xvfb/FreeRDP 会话提供截图、点击、拖动、滚动、映射按键及程序启动；当前输入仅 ASCII，缺依赖/连接失败明确报错。来源：`platforms/rdp.py`。 | 实验实现；Unicode 及完整业务未承诺 |
| OTHER-015 | 官网中的安装入口、六端边界、商店状态和版本说明与实际交付一致，语言偏好持久保存；部署不等于软件发布。来源：`website-project/index.html`、发布配置。 | 已有页面；线上状态未在本次核验 |

## 待验收与后续计划

| 项目 | 当前边界 | 完成条件 |
| --- | --- | --- |
| 六端完整跨设备业务 | 有分端实现/局部实测，无手机注册→邮箱激活→桌面确认的完整证据 | 指定应用、账号和真实设备，通过公共入口保存前后截图、事件与业务核验 |
| iOS 与更多移动组合 | 模拟契约已有；iPhone、完整 Xcode 配置及其他主机组合待实测 | 首次安装、复用、签名、输入、断连恢复分别记录 |
| Windows/macOS 应用兼容 | Windows 隔离窗口、macOS 原生面板已有局部实测 | 对目标应用验证捕获/输入；不将后台能力推广到任意自绘应用 |
| 桌面产品交付 | 0.4.16 三平台冻结包已有历史记录；用户机器权限、完整模型任务、签名/公证仍待验收 | 构建、干净安装、用户权限、真实任务和发布逐项核验 |
| 通用工作流连接器 | 当前仅已注册 SQLite 只读查询，没有通用写入/API/MCP 连接器 | 后续设计幂等写入、持久等待/重试和单独验收 |
| QA 后续优化 | OCR/模板预筛、确定性交叉核验、弱证据复核未完成 | 同设备同用例对照耗时、调用量、通过率；不能以提速弱化判定 |
| 异步离屏断言 | 已否决，不在待实现列表 | 保持同步现场处理与重判 |

上次文档重排统一了旧文档中普通设备命令的资源锁、setup 入口、后台截取适用端及发布状态表述。更新提醒的 0.4.14 和共享桥/桌面的 0.4.16 交付证据已归档；本次不重新声明远端在线状态，不改变用户安装或版本号。

本轮补全按代码入口增加公共条目和六端独立清单，并修正过度概括的状态；具体缺口见[代码核对记录](requirements-audit.md)。本轮未修复这些运行时代码，也未新增真机或发布结论。
