# Saygo 开发规范

本文件是仓库唯一的 Agent 开发规范，合并原有开发说明与强制约束。
产品需求和操作说明见 [文档入口](docs/README.md)；客户端操作协议见
[统一设备 Skill](plugins/saygo-device/skills/device/SKILL.md)。

## 用户约束与任务边界

- 处理仓库、版本发布或浏览器任务前，读取当前用户的 `~/.codex/memories/MEMORY.md`，遵守用户约束及失误记录；用户指定了绝对路径时使用该路径。
- 用户要求停止时立即停止操作；后续只在重新授权的范围内继续。
- 修改前检查工作区和分支，保留已有改动；按功能划分提交，不混入无关修改。
- commit、push 和发布授权不等于升版授权。未经明确授权不得修改版本、创建发布标签或发布新版本。

## 提交说明必须完整

禁止给包含多项行为修改的提交只写一句标题。commit 标题和正文使用英语，至少说明：

1. **问题与目的**：用户在什么条件下遇到什么问题，本次要改善什么行为。
2. **全部修改点**：按模块或文件列出实际修改，逐项解释为什么改；包括接口、状态、错误处理、界面、打包、文档和测试。不得只写“优化”“完善”“修复若干问题”。
3. **行为与兼容性**：新旧行为的差别、安装和升级迁移、旧会话处理及需要人工操作的部分。
4. **验证**：实际执行的命令、运行平台、测试数与结果。单元测试、模拟测试、真实设备端到端测试分别记录；跳过和未运行项目不能算通过。
5. **限制**：尚未验证的平台、已知缺陷和未完成的部署。源码修复、安装版验证、构建产物和发布状态分别说明。

正文内容必须与最终 staged diff 一致。提交前检查 `git diff --cached --stat` 和 `git diff --cached --check`；提交后核对提交正文，push 后核实远端结果。长正文先写临时文件，通过 `git commit -F` 提交，保留真实换行。

示例结构：

```text
fix(browser): share browser bridge discovery across desktop and WSL

Problem and purpose:
- Describe the trigger, failure and intended behavior.

Changes:
- Explain each module change and the problem it addresses.
- Include tests, documentation and packaging changes with their purpose.

Validation:
- Record platforms, commands, actual results and real-device versus simulated coverage.

Compatibility and limitations:
- Describe migration, verified scope, unpublished artifacts and untested paths.
```

## 浏览器连接与升级

- Windows 桌面版、Windows Python 安装版和 WSL 是同一浏览器 bridge 的客户端，不能因各自运行环境不同而默认建立独立 IPC 目录。
- 默认目录和已有连接通过共享的 browser OS 发现逻辑解析。升级要检查实际注册、在线 host 与客户端配置的一致性，不能仅比较 Python 包版本。
- 不主动断开、重载用户的插件，也不杀掉正在工作的 native host。更新后应保持现有连接，后续连接使用同一目录。
- 保留会话的明确目标；旧 page ID 失效须显式重新选择，禁止暗中切换到别的页面或业务会话。
- 状态文件或会话列表存在不代表在线；必须有真实请求响应。截图成功必须实际返回并检查图片，动作成功还需核验结果。
- 超时或响应丢失不自动重放输入；先观察并核对结果。

## 测试与验收

- 修复缺陷先补能复现原问题的回归测试，再验证修复；避免用重复、无断言的用例凑数量。
- 连接、安装、升级改动必须覆盖：全新安装、重复 setup、旧配置、桌面版/WSL 共存、客户端退出与重启、断连、过期页面、多连接冲突。
- 真实浏览器端到端测试应经过 CLI/MCP、native host 和实际扩展，验证页面发现、截图、输入及结果；直接调用被模拟的适配器不能代替它。
- Windows、macOS、Android、iOS、Chrome 扩展和 Playwright 分别列验收结果。根据变更影响运行相关平台；声称六端全部可用时，必须具备六项实际端到端证据。
- 测试使用独立目录、浏览器 profile、命名会话和自有测试页面；不能借用业务会话进行测试输入。用户现场的诊断应限制在已授权的目标和动作内。
- 缺少设备、权限或依赖时准确报告阻塞，不把 skip、mock 通过或单平台通过描述为全平台通过。
- 发布前验证构建产物、干净环境安装和重复 setup；PyPI 可见、GitHub 产物、商店提交及商店审核通过分别核实。

## 进度与证据

- 先说明已确认事实，再说明推断和待验证项；不能在未截图、未测试或未部署时声称已经完成。
- 发现此前结论错误时直接纠正，给出新证据及影响范围。
- 完成说明应包含提交、变更目的、实际测试结果、用户安装状态和剩余限制。

## 产品与入口

Saygo 为外部编程 Agent 提供跨手机、浏览器和桌面窗口的视觉控制服务。CLI/MCP 共享命名会话、观察、动作和错误语义；`saygo task` 支持逐步提交、人工接管、持久化恢复和证据导出。
桌面版 `saygo/desktop/` 使用 Qt 6 / PySide6，用户配置视觉模型 API，决策循环复用 InteractiveRuntime。BDD QA 引擎仍提供 `.feature` / `.md` 用例运行、报告和 Figma 集成。
视觉决策使用截图，不向模型提供 UI 树或 DOM。MCP 和桌面版浏览器使用扩展后端；Playwright 保留在 CLI/Runtime，Selenium 保留用于 QA。

## 🔒 铁律（违反过，务必守）

- **saygo 主仓是 Public(GitHub)**。写进代码/注释/docstring/README/AGENTS.md/示例的一切都**必须脱敏**：禁止真实包名/bundle id、产品名、Apple team-id、公司名、真账号/邮箱、API key/token。一律用占位符：`com.example.app` / `你的 team id` / `${EMAIL}` / 通用描述。commit **message 本身**也脱敏。
- 真值只放 **gitignored** 文件：`.env` / `tests/<t>/_accounts.json` / `.saygo/mcp_clients.json` —— 从未入库，保持如此。
- 私有 `tests/<target>/` 默认被 .gitignore 排除；公开 `*_demo` 和 `_template` 是例外。**客户测试用例是独立私有仓**(嵌套在 `tests/<target>/`，自己的 .git，push 用普通 `git push`，别 force)——它是客户内容不适用上面的公开脱敏，但**别和 saygo 主仓搞混**。
- saygo 主仓默认分支为 `main`；按用户授权执行提交和推送。标题清楚、正文完整，必须解释全部修改点及目的，不能仅写一句标题。不得添加虚假的模型身份或固定某个供应商的协作者署名。

## 统一操作服务与 Runtime


- `saygo/devices/service.py` 是 CLI/MCP 的共享操作入口；会话绑定由 `devices/control.py`、`platforms/device_session.py` 管理。不要在新入口复制平台分派和错误处理。
- `saygo/runtime/interactive.py` 支持动态任务；`saygo task` 和 MCP `agent_task` 使用同一实现。显式 JSON 工作流走 `saygo workflow`，独立于 QA 引擎。桌面自然语言任务由 `desktop/runner.py` 决策，不在 Runtime 内另建模型循环。
- 动作先保存 durable intent 再派发；中断且结果未知标记 `needs_review`，禁止自动重放。request ID 用于防止重复派发。核对后 `resolve`，新动作须重新观察。
- observations 带 ID、会话、目标身份、尺寸和坐标映射；优先用百分比坐标。图像/裁剪坐标必须绑定原观察，调用方无需自行算缩放。旧观察、目标区域或窗口身份变化必须拒绝或重新观察定位。
- `observe_after`、有超时的变化/稳定等待只返回观察事实；`business_success: null` 不能改写成业务成功。能力缺失、输入异常必须明确报错。
- 优先可见按钮和菜单，尽量不用快捷键。Windows 后台不支持的快捷键不得静默切换前台；前台操作必须显式选择。
- 手机、浏览器和桌面均支持 handoff/resume。暂停阻止自动操作，交还控制权后截图，业务完成仍须另行验证。显式 workflow 的 human 步还要执行声明的验证步骤。
- 任务/工作流在 idle、handoff、needs_review 期间保留资源归属；普通 device 命令遵守这套锁。所有本地桌面窗口共享前台输入资源。锁不能阻止人或其他软件改变焦点。QA 经 `qa/control.py` 复用物理资源锁、观察检查与持久请求记录；模拟测试不等于真机验收，也不等于 task 的完整接管恢复生命周期。
- 实际操作、异常、前后截图和接管事件由程序记录；Agent 解释单独存为 annotation。导出包可能包含应用数据、输入文本和截图。
- 默认状态在 `$SAYGO_HOME_DIR`（`~/.saygo`），交互 task 在其 `runtime` 子目录；显式 workflow 默认使用当前目录的 `.saygo_runs/runtime`。`SAYGO_RUNTIME_DIR` 可覆盖两者的任务库，workflow 的 `--state-dir` 优先。CLI/MCP 要共享相同配置。项目资源别名在 `.saygo/resources.json`。

详见 [Agent 操作](docs/common/operations.md)、[Runtime](docs/common/workflows.md)。离线测试使用模拟驱动和真实 SQLite，不代表完整跨端任务通过真机验收。

## 桌面版、安装与分发


- `desktop/app.py`：Qt UI、后台工作线程、连接与任务管理；`desktop/model.py`：OpenAI-compatible 视觉 API 和凭据；`desktop/runner.py`：每次一个动作的模型循环，复用 InteractiveRuntime。
- 不使用 pyenv。打包用户无需安装 Python；Windows 原生直连，不依赖 WSL。开发者按需安装 `desktop`、`windows`、`mac` 等 extras。
- Key 只在内存或支持的 OS keyring；不得退回明文保存。`desktop.json` 不含 Key。截图和任务内容会发送到用户配置的模型提供方。
- 配置优先级：defaults → `$SAYGO_HOME_DIR/config.env` → 当前项目 `.env` 或 `SAYGO_CONFIG_FILE` → 环境变量。显式配置文件缺失时报错，不扫描 site-packages 下的 `.env`。
- `scripts/install_agent_plugin.py` 安装托管 runtime、客户端接入和浏览器桥；支持 Claude/Codex/Qoder/QoderCN CLI。新增客户端共用操作 Skill，只保留接入差异。
- `scripts/build_release.py` 按白名单生成源码、带 SHA256 的版本化安装器和扩展 ZIP；不得混入 `.env`、本机会话、截图或客户用例。
- `scripts/build_desktop.py` 生成原生目录包；`scripts/package_desktop.py` 在目标 OS 生成 Windows ZIP / macOS DMG / Linux tar.gz 与校验和。`.github/workflows/desktop.yml` 手动构建，不自动发布。
- 0.4.16 已通过 Windows x64、macOS arm64、Linux x86_64 的桌面测试、实际冻结 Qt 启动、native-host 版本/握手/IPC 和归档检查；Windows 本地另有 45 项 offscreen 桌面测试。IPC 使用模拟扩展对端，完整真实模型业务任务、签名与公证仍不在通过范围内。实际证据见 `docs/common/history/release-0.4.16.md`，不得混称为六端真机验收。

使用和验证边界见 [desktop](docs/common/desktop-app.md)、[distribution](docs/common/installation.md)。

## QA 架构（数据流）

用例 → `gherkin.py` 解析 → `render_case()`(step + metadata) → `planner.py`(1 LLM call/case，拆 intent/expected/hint) → `agent.py` step 主循环 → fail/timeout/error 时 `healer.py`(根因五分类) → `report.py`(HTML+base64截图)。

`agent.py` 按 Scenario step 推进。当前 `PER_STEP_SUB_ACTION_LIMIT=-1`（禁用动作次数上限），`AGENT_MAX_STEPS=0`（默认禁用整个 scenario 的循环轮数上限）；主要保护是 `MAX_TURNS_WITHOUT_PROGRESS=15`。预算内主动 wait 与 probe 轮询不计入该无进展计数。普通路径只有当前 step 判 pass 才由框架推进；`current_step_index` 必须严格等于待执行步骤，LLM 不得自行 +1。pass/fail 必带 evidence（≥15 字符且引用屏幕元素），fail 还需 fail_reason（≥10 字符），in_progress 必带 action。连续 3 次校验拒绝判 fail；拒绝不执行动作、不耗 sub-action 配额，但计入循环轮数和无进展计数。

连续断言合并使用独立的 `validate_assertion_batch()`，逐条检查 verdict/evidence/where、重复证据和负向断言；整块通过才一次推进多步，probe 步不参与合并。证据校验是文本启发式检查，不会独立验证截图内容，不能保证模型没有误判。不可视断言禁 PASS 是模型提示约束；要做代码层验证需使用 probe。

`healer.py` 在 fail/timeout/error 后提供根因分类与建议，附加到报告，不自动修复用例或应用，也不改写原测试结果。

`brain.py` LLM 决策：发**原始截图** + 最近 1-3 张历史截图 + planner hint + step 列表 + 已过 step 的 evidence 锚点 + 上次 reject 理由 → 返回带 `step_progress` 的 JSON。**不可视觉验证的断言禁 PASS**(埋点/后端/系统时间/通知抽屉/跨App deeplink → 必须 fail，不许「假设通过/推断成立」蒙混)。

**分级模型 / 元素定位 / 多帧断言 / 参考图**（借鉴 midscene）：

- **分级模型**：`LLM_MODEL_BRAIN/PLANNER` 留空时回落 `LLM_MODEL`；`LLM_MODEL_LOCATOR` 留空时关闭定位。Locator 端点/密钥留空则复用主 LLM 配置。
- **元素定位**(`locator.py`，默认关)：配置 `LLM_MODEL_LOCATOR` 后，普通路径中带 `target` 的 tap/long_press 在执行前定位，成功则替换 Brain 坐标，失败则沿用原坐标。也供分层执行定位目标。旧的像素差 no_effect 检测已停用，对应 `AGENT_LOCATE_RETRY` 与网格升级路径目前不会由该检测触发。「grounding」保留指更大的定位策略，不作为定位小模型的别名。
- **稳定帧与多帧断言**：默认 `AGENT_SETTLE_ENABLED=true`，`settle.py` 用像素差、状态栏 mask 和超时采样；操作决策用末帧，断言按窗口变化量选择静态 1 帧或动态最多 3 帧。`AGENT_ASSERT_BURST_FRAMES=3` 用于关闭 settle 或缺少窗口帧时的回退路径；采样不保证捕获所有短暂提示。
- **参考图断言**(默认关)：case 声明 `@ref:<path>` / `# saygo-ref:` → 渲染成绝对路径 → brain 拿设计稿做视觉走查对比。供 Figma 走查。

## 执行优化（当前实现）


- `AGENT_WAIT_MAX_S=45`：每步累计主动等待预算；预算内 wait 轮不计无进展，耗尽后恢复计数，不是整个步骤的 45 秒超时。
- `AGENT_MERGE_ASSERTS=true`：连续断言同步合并；失败时可在现场识别、关闭拦截弹窗并重新判定。
- `AGENT_SPLIT_ACT_CHECK=false`：可选操作步批量执行。开启后 Brain 看截图拆原子动作序列，Locator 按需定位执行，下一轮 Brain 验证步骤；连续两次序列执行失败回退普通路径。不是零大模型调用，也不以 visual-diff 作为动作成功证明。

## 视觉操作约束

- macOS 显式后台模式见 `platforms/desktop_mac_background.py`。模型仍只看截图；驱动内部可对已选坐标做应用内 AX 命中、窗口身份校验和有限祖先查询，以执行原生控件动作，不向模型提供树、控件文本或语义定位。该路径禁止激活/启动 App、全局鼠标键盘、剪贴板和前台回退。原生按键定向到已绑定进程且须验证其已有焦点控件归属；不支持的动作明确失败。锁屏、非当前桌面或身份不明的窗口拒绝操作。实机验证范围和命令见 `docs/macos/README.md` 的后台模式；不能将独立测试面板的通过宣称为全应用兼容。

- **不喂 UI 树给 LLM**。QA 感知与定位不使用树(无 snap-to-clickable / element_marker / dialog_dismisser / _compact_xml)。决策只靠截图；macOS 后台驱动内部的原生动作适配范围见上条。
- **优先百分比坐标**：QA 模型使用 `x_pct/y_pct`（0–100），`brain._pct_to_px` 换算；统一服务还支持像素、图像与裁剪空间。元数据中的图像尺寸和映射不能省略，不能假设截图像素等于设备逻辑坐标。
- 移动端视觉控制经 Appium（截图可用 mjpeg 帧流回退到 `get_screenshot_as_png`）。设备需可交互，锁屏或受保护页面可能无法截图。adb 用于发现和生命周期管理，不作为视觉控制的旁路。

## 平台（`saygo/platforms/`）

- `base.py` 抽象接口(screenshot/tap/swipe/input_text/press_key/is_ime_visible…)。
- `appium.py` **iOS+Android 统一驱动**：`AppiumServerManager` 自动起 server(带 ANDROID_HOME、锁定装了 appium 的 node)；os 由 `config["appium"]["os"]` 选 xcuitest/uiautomator2。`create_platform("ios"/"android"/"appium")` 全 → AppiumPlatform。
- **mjpeg 帧流截图**(`platforms/mjpeg.py`，默认开)：起 session 时开 driver `mjpegServerPort`，`screenshot_raw` 从常驻流取缓存帧(JPEG→PNG)省 HTTP 往返；没有帧或解码失败时回落 `get_screenshot_as_png`。帧龄超过 0.5 秒回落 Appium，断流和停止清缓存；普通 device 重连没有自动恢复帧流，详见需求 OBS-020。`APPIUM_MJPEG_*` 控。
- `browser.py` 保留 Selenium QA/local/Grid。CLI/显式 Runtime 的 managed browser 使用 `browser_playwright.py`，CDP 接入常驻 Chromium，按 target ID 绑定页面；关闭控制器只断开，不关 Chrome。CLI `device start --backend playwright`、`pages/select-page/close-page`；详见 `docs/playwright/README.md`。测试 `tests/browser_demo`（真实浏览器测试需 `SAYGO_TEST_CHROME`）。
- 桌面：`desktop_mac.py` / `desktop_win.py` 是前台窗口级驱动；Windows `--background` 使用 PowerShell/Win32 runner，支持范围取决于控件，不支持操作必须报错。WSL 显式选 `PLATFORM=windows`，由 `windows_runner.py` + PowerShell/Win32 runner 操作宿主。`PLATFORM=desktop` 仅在原生 Windows 选 Windows 驱动，其余系统选 macOS。桌面通过环境变量配置；`run --platform` 当前只接受 ios/android/browser/rdp。
- `rdp.py` 为实验性远程 Windows 驱动，尚不应视为稳定接口。
- **文字输入**：Android 走 `mobile: type`，由 Appium 的 `io.appium.settings` 在动作期间临时使用 UnicodeIME，完成后恢复原输入法；连接不默认设置 `unicodeKeyboard/resetKeyboard`，不能假设驱动支持 `resetKeyboard` 或断开会自动恢复。handoff/resume 经共享实现保存、恢复并核验用户输入法；旧会话缺失原选择时明确列出候选，由用户选择，不能硬编码键盘或执行 `ime reset`。恢复失败保持暂停，成功后重新观察。过期的人工接管会话须显式 connect 原绑定，只有 `InvalidSessionId` 才新建 Appium 会话，保留原暂停及资源归属；网络失败不创建替代会话。新建后的准备失败也保留绑定，供显式恢复。IME 管理使用 Appium 会话接口，不通过 adb 输入或重启应用绕过。原生 EditText 与 Flutter 自绘均走同一输入路径；iOS 保持聚焦元素 send_keys，不使用 Android 自动化输入法。iOS 新连接默认将 `connectHardwareKeyboard` 和 `forceSimulatorSoftwareKeyboardPresence` 均设为 false，保留模拟器当前键盘偏好；显式 caps 可覆盖，旧偏好无历史记录时由用户恢复。实际人工输入与各端真机验收须另行记录，iOS 尚无本次真实验收证据。
- **iOS 签名**：Appium 走 xcodebuild/CoreDevice(非 go-ios 隧道)自动签 WDA，需 `IOS_TEAM_ID` + Xcode 登录该 team + 设备在其开发列表 + login 钥匙串解锁(codesign)。`android.py`/`ios.py`/`hands.py` 旧驱动已删。

## Skills（`saygo/skills/`，截图→LLM 间预处理，默认开的都不碰树）

`loading_detector`/`keyboard_detector`(靠 platform.is_ime_visible)/`scroll_map`/`visual_diff`（图像差异，不作业务成功证明）/`toast_detector`；按需：`ocr`/`color_validator`/`layout_checker`/`smart_crop`。

## Probes（`saygo/probes/`，非视觉断言插件 —— 埋点/后端落库/上报日志）

纯视觉判不了的断言开的**代码层**通道，铁律「不可视断言禁 PASS」由此有了正解（不是放宽）：

- 用例在某 Then 下面挂 `# saygo-probe: <name> k=v` → **该 step 的 verdict 由插件决定**，agent 不调用 Brain 对它做视觉裁决。完整用例和步骤列表仍可能传给 Planner/Brain，因此这不是数据隔离机制。
- **用例只写意图**（`check=首页曝光`），真实事件名/表名/期望属性在插件 config 里映射 —— 改埋点方案时用例零改动。
- **三态 verdict**：`pass`/`fail`/`inconclusive(+retry_after_s)`。埋点批量上报有分钟级延迟，**查太早的 0 行不算证据**（我据此造过假 bug），saygo 按 probe 节奏轮询到 `PROBE_TIMEOUT_S`(默认 300s) 才判 fail；重试轮不计 no-progress（同 wait 语义）。插件抛异常/子进程崩 = inconclusive 继续重试，预算耗尽 fail 并把 error 写报告，**绝不因「查不了」放过断言**。
- 两种形态：**Python 类**（继承 `probes.base.Probe`，实现 `check(ctx,args)`）/ **子进程**（stdin JSON → stdout JSON，任何语言、依赖不污染 saygo 环境）。
- 注册表 `.saygo/probes.json`（gitignored，同 mcp_clients.json 一档；`.example` 入库，`${VAR}` 展开）。**插件代码放 `tests/<target>/probes/`**（客户私有仓；事件名/表名/查询逻辑不进主仓）。示例见 `tests/_template/probes/*.example`。
- ctx 给插件的锚点：`case_started_at/step_started_at/now`(时间窗) + `account`(多设备按 worker 绑) + `device/app_package/platform` + `attempt/elapsed_s/timeout_s` + `session`(同 case 内缓存) + `artifacts_dir`。
- **偏置跑法**：`saygo run --skip-probes`(probe step 标 **skip 不是 pass**，reason 点名哪几步没验证 + 结果带 `probes_skipped_steps`，防静默全绿) / `--only-probes`(**case 级筛选**：只跑声明了 probe 的 case，其 UI 步照跑——埋点得靠操作触发；纯查库用 `saygo probes check`)。走 env `PROBES_MODE=skip|only`，故 `--bg`/多设备 worker/MCP `run_target(probes=…)` 全通。
- 边界：一 step 一条 probe（多断言拆多 Then）；probe 步自动被排除出「连续断言合并」块；probe 名没注册 = fail（要跳过用 `@manual`）。CLI 调试 `saygo probes list` / `saygo probes check <name> k=v --target t --wait`。全文 `docs/common/probes.md`。

## CLI / MCP / 客户端接入


所有能运行 shell 的 Agent 都可调用 `saygo`；安装后无需从仓库根运行。`saygo device` 提供连接、观察和动作，`saygo task` 提供交互任务，`saygo run` 提供 QA。不要混用它们的状态或结果语义。

`saygo-mcp --profile device`（或 `python3 -m saygo.mcp.server --profile device`）启动设备模式，不需模型 Key 或 tests 目录。以 `server.py` 中 `_DEVICE_PROFILE_KEEP` / `_RUN_PROFILE_ONLY` 为准，文档不硬编码工具数量。新增工具必须登记正确 profile，并验证 stdio 握手和工具列表。

- `device_connect`、`device_sessions`、`device_command` 调用统一会话服务。
- `device_observe` 与带观察的 `device_act` 返回 MCP 图像内容；旧 `device_screenshot` 返回元数据/文件路径。
- `agent_task` 暴露逐步提交、接管、恢复和导出。
- MCP 浏览器默认 extension；拒绝 Playwright 连接、观察、动作以及使用它的任务，已保存绑定列入 `unavailable_sessions`，不能静默创建替代页面。
- `mcp/client.py` 是另一条能力：QA brain 可调用外部 MCP，私有配置为 `.saygo/mcp_clients.json`。
- 保持仓库声明的 MCP SDK 兼容范围；改动注册/握手时检查兼容分支与对应版本，不能只凭本机版本通过就宣称整个范围已验证。

`plugins/saygo-device/` 提供共享 device Skill、doctor 命令和 MCP 接入。托管安装器负责客户端差异；Claude marketplace 入口仍存在。插件缓存只包含插件自身目录，launcher 必须能找到已安装 runtime 或显式 checkout，不依赖缓存外相对路径。

公开插件文案用英文；skill/command/server 名不重复插件前缀。修改插件时检查 manifest、SKILL frontmatter 和客户端加载；Claude 插件改动运行 `claude plugin validate .` 和 `claude plugin validate plugins/saygo-device`。客户端权限配置只限 Saygo，保留无关设置和用户自定义项。客户端需要重启才能加载新工具。

通用操作协议在 [device Skill](plugins/saygo-device/skills/device/SKILL.md)；本文件 是开发说明，不代替客户端的操作 Skill。

## 用例格式

**`.feature`(Gherkin，推荐)**：Feature/Background/Scenario(Outline)+Examples 全解析。Tag：

- `@P0/@P1/@P2` 优先级；`@auto/@partial/@manual`(后两个自动 skip)；`@skip/@wip` 跳过。
- **平台标签是集合，可扩展，不用 both**：`@android`/`@ios`/`@browser`/`@mac`/`@windows`/`@desktop`/`@rdp` 等；`@android @ios` 表示允许这两个平台。标签只筛选用例，不切换驱动、不自动发起双端运行。跑测平台不在集合里则 skip。
- `@TC-XXX` case ID；`@reset:pm_clear|relaunch|none` Android 重置(覆盖 feature 级 `# saygo-reset-default`)。
- 文件头信息元数据：`# saygo-target/platform/package/reset-default`(值行别写行内 `#` 注释)。

**`.md`(TDD)**：`### TC-XXX` 块 + `- **Priority/Reset before/Platform/Mode/Steps**`。

## Per-target 文件（私有 `tests/<target>/` gitignored；公开 `*_demo` 和模板例外）

- `cases/*.feature|*.md` 用例；`_preconditions.md`(auto-prepend，教 LLM 从异常态恢复到 Background 前置态——降 false-fail 最关键)；`_accounts.json`(账号/密钥池，`${EMAIL}`/`${PASSWORD}` 占位，**别 commit 真账号**，多设备按 worker i 绑 accounts[i])；`reports/<ts>/*.html`。
- 用例约定：**自包含**(前置态进 Background，进子页操作明示，不依赖前置 case)；Hints 写方位不写坐标；Then 拆成逐条可验证 bullet；不可视断言改写或 skip。

## 开发安装与 CLI


```sh
# 开发：按需增加 desktop/mobile/windows/mac/qa 等 extras。
python3 -m pip install -e '.[mcp]'
saygo --help
# 终端 Agent：自动检测客户端，安装托管集成和浏览器桥。
python3 scripts/install_agent_plugin.py

saygo device sessions
saygo device list --platform android
saygo device connect --platform android --device DEVICE_ID --session phone
# 先安装浏览器桥并在扩展内 Connect。
saygo device connect --platform browser --backend extension --session web
saygo device capabilities --session web
saygo doctor --session web
saygo device screenshot --session web
saygo device act '{"type":"tap","x":50,"y":40,"coordinate_space":"percent"}' --session web --observation-id OBSERVATION_ID --observe-after
saygo task create '{"phone":"phone","web":"web"}'
saygo task recover TASK_ID
saygo task timeline TASK_ID

# QA 独立配置模型和目标；密钥只留本地。
saygo init
saygo run tests/my-app/login.feature --report
saygo probes list --json
saygo probes check NAME check=home_impression --target my-app --wait
```

按改动选择检查：`tests/control_demo`、`tests/runtime_demo`、`tests/desktop_demo`、`tests/extension_demo`、`tests/mobile_demo`。优先离线单元/契约测试；带 live 标记的测试需对应主机、授权和测试目标。未运行的真机路径必须明确说明。

## .env 关键项（真值在此，勿入库）
```
PLATFORM=android|ios|browser|mac|windows|desktop|rdp
LLM_PROVIDER=openrouter  LLM_API_KEY=…  LLM_BASE_URL=https://openrouter.ai/api/v1  LLM_MODEL=<vision-model-id>
LLM_MODEL_BRAIN=  LLM_MODEL_PLANNER=  LLM_MODEL_LOCATOR=   # 分级模型，空→回落 LLM_MODEL(locator 空=关)
LLM_LOCATOR_BASE_URL=  LLM_LOCATOR_API_KEY=   # 定位模型独立端点(空→复用主 LLM)
ANDROID_PACKAGE=com.example.app   # 被测包名(必填)；填真值别提交
APPIUM_DEVICE=  APPIUM_SERVER_URL=  # 设备 udid/serial；空则默认
APPIUM_MJPEG_ENABLED=true  APPIUM_MJPEG_PORT=  APPIUM_MJPEG_QUALITY=90   # mjpeg 帧流截图(多设备需各给端口)
AGENT_MAX_STEPS=0   # scenario 循环轮数上限，<=0 禁用
AGENT_SETTLE_ENABLED=true  AGENT_WAIT_MAX_S=45  AGENT_MERGE_ASSERTS=true
AGENT_SPLIT_ACT_CHECK=false
AGENT_ASSERT_BURST_FRAMES=3  AGENT_LOCATE_RETRY=2   # 回退路径多帧数 / 已停用 no_effect 检测的旧阈值
IOS_TEAM_ID=  IOS_WDA_BUNDLE_ID=com.example.wda  IOS_BUNDLE_ID=   # iOS 真机签名
PROBES_CONFIG=  PROBE_TIMEOUT_S=  PROBE_POLL_INTERVAL_S=   # 非视觉断言插件(空→注册表 defaults / 300s / 20s)
PROBES_MODE=all|skip|only    # = saygo run --skip-probes / --only-probes
BROWSER_HEADLESS / VIEWPORT_* / SELENIUM_GRID_URL ; FIGMA_TOKEN ; SKILLS_ENABLED
```

## 已知限制 / 行为

- 坐标不准的头号真因是**分辨率标定**(截图px↔设备px 换算)；标定对了 + 用百分比协议基本落中。
- 不可视断言(埋点/后端/系统时间/launcher badge/通知抽屉/跨App)**视觉层**一律 fail，不许蒙混；要真验证挂 probe 插件(见上)，那条 step 由插件裁决。
- iOS 真机若非专用设备(如私人手机)会反复 `unavailable`(锁屏/休眠/拔线)——按需插+解锁，规模化用专用设备或云真机(云上 iOS 只有 Appium 一条路，且免签名代管)。
- 依赖按 `pyproject.toml` extras 选择，不要求浏览器用户安装移动端工具链。桌面模型客户端与 QA 模型客户端独立，修改时注意各自协议。

## 现有浏览器扩展后端


`extensions/saygo-browser/` + `saygo/integrations/browser_bridge.py` + `platforms/browser_extension.py`：Native Messaging + 私有共享目录 IPC，Windows host 可与 WSL Saygo 通信，不监听网络端口。默认当前浏览器配置文件内所有 HTTP(S) 标签页（含新弹窗），操作目标仍显式选择；browser session UUID + tab ID 防重启误选；不提取 DOM。Runtime browser resource 必须写 `backend: extension`；先安装桥，再用 `device connect` 连接，见 `docs/browser-extension/README.md`。仅能声称已执行的平台测试，Windows/WSL 桥接、导航和截图已实机验证。测试：`tests/extension_demo`，可选 `SAYGO_TEST_CHROME`。

## 移动设备发现与模拟器安装

`saygo/devices/mobile.py` 实现 device list/connect/install/boot 的移动适配器，通过 adb、devicectl、simctl 分别发现 Android、iOS 真机和模拟器。物理 ID 与持久别名分开；本地 iOS 需要 macOS 完整 Xcode，远程连接明确指定 Appium URL 和 ID。

安装器不强制覆盖 AVD，驱动安装失败必须向调用方返回。SDK 许可在下载前交互确认，无人值守必须显式 --accept-licenses。adb 仅用于发现/生命周期，不旁路视觉控制。测试在 tests/mobile_demo；前提与验收见 [Android](docs/android/README.md) 和 [iOS](docs/ios/README.md)。

mobile_host.py 选择主机并执行只读预检；WSL 无可用 KVM 时默认 Windows，--host local/windows 显式覆盖，--dry-run 不得安装。只复制标准库 worker 文件到 Windows，不复制配置/凭据，不自动启用系统功能或重启。

Windows Appium 只监听回环；mobile_relay.py 经 Windows worker stdio 转发 WSL HTTP，使用带令牌本地 URL，传输结果不明时不重放。连接后使用真实截图验收，模拟主机测试不能代替模拟器实测。

Windows 工具必须使用 toolchain.background_options()；私有 Appium Node 预加载 windows_no_console.cjs，避免 adb/logcat 弹控制台。使用私有 adb 端口并通过 Appium adbPort 传递，避免 WSL 转发默认 5037。历史 WSL→Windows API 35 安装、截图、设置启动、点击和输入已实测；iOS 仍只有模拟测试证据。

## 统一控制入口

saygo/devices/control.py 为 saygo device 提供 list/connect/sessions/disconnect、install/boot 及共用 open/scroll，--session 与 --serial 为别名。桌面绑定持久保存应用和 OS，短生命周期控制器可重连；Runtime 支持 session 及内联 app 桌面资源。

disconnect 保留端点配置，后续须显式重连；它不是跨进程取消，也不全局撤销扩展访问。测试在 tests/control_demo，操作说明见 [统一操作](docs/common/operations.md)。

## 包目录

模块职责见[架构](docs/common/architecture.md)。QA 在 saygo/qa，图像处理在 saygo/vision，设备生命周期/工具链/Windows worker 在 saygo/devices，Figma/浏览器桥在 saygo/integrations。

命令族在 saygo/commands，cli.py 只注册/分派；共享用例发现、准备和调度分别在 qa/cases.py、qa/device_setup.py、qa/execution.py。MCP 直接导入所属模块，不保留旧 CLI 私有辅助函数别名。根 CLI/config/logger 及浏览器桥兼容入口保留。

Windows worker bundle 必须保留嵌套包结构，tests/mobile_demo/test_bundle.py 验证隔离导入。
