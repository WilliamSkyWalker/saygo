# Saygo

[简体中文](#简体中文) · [English](#english)

[官网 / Website](https://saygo.work/) · [源码 / Source](https://github.com/WilliamSkyWalker/saygo) · [MIT License](../LICENSE)

## 简体中文

**你说，它做。** Saygo 为外部编程 Agent 提供跨电脑、浏览器和手机的视觉控制服务：观察截图、执行动作，再核验结果。也可以通过独立桌面应用描述任务，或运行 BDD 用例生成测试报告。

### 选择使用方式

| 入口 | 用途 | 模型配置 |
| --- | --- | --- |
| **CLI / MCP** | 让已有 Agent 连接设备、查看截图并操作；CLI 与 MCP 共享命名会话和操作语义 | 外部 Agent 自行决策，无需配置 Saygo 模型密钥 |
| **桌面应用** | 使用图形界面描述任务、管理连接、接管和恢复 | 配置兼容 OpenAI 接口的视觉模型；打包版无需安装 Python 或 Agent |
| **BDD QA** | 执行 `.feature` / `.md` 用例，生成报告；通过 probe 验证后端等非视觉结果 | 单独配置 QA 模型与测试目标 |

`saygo device` 提供连接、观察和单步动作；`saygo task` 在此基础上支持跨步骤持久化、人工接管、恢复与证据导出。固定 JSON 流程使用 `saygo workflow`，BDD 测试使用 `saygo run`。

视觉决策使用截图，不向视觉模型提供 UI 树或 DOM。操作遵循“观察 → 决定一个动作 → 执行 → 再观察”：输入必须引用有效观察，结果不明的动作不会自动重放。人工接管保留目标和任务资源归属；用户交还控制后重新观察，业务结果仍需核验。详见[统一操作](common/operations.md)。

### 快速开始

使用外部 Agent 时，准备 **Python 3.10+、pipx 和所选 Agent 客户端 CLI**：

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --client codex
```

客户端还可选 `claude`、`both`（Claude + Codex）、`qoder`、`qodercn` 或 `all`。Edge 用户在 setup 命令后增加 `--browser edge`；移动端可增加 `--mobile` 安装 Python 依赖，SDK、Appium 和系统权限按各端指南准备。

浏览器任务还需完成以下步骤：

1. 安装 [Saygo Browser](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo)，打开要操作的普通 HTTP(S) 网页。
2. 在扩展弹窗点击 **Connect local bridge（连接本地桥）**。
3. 重启 Agent 客户端以加载工具，然后让 Agent 连接并选择目标页面。

也可以直接使用 CLI。在扩展已连接后，逐步执行：

```sh
saygo device connect --platform browser --backend extension --session web
saygo device pages --session web
# 将 PAGE_ID 替换为上一步返回的目标页面 ID。
saygo device select-page PAGE_ID --session web
saygo device screenshot --session web
```

读取返回路径中的截图后再决定动作；输入示例和观察 ID 的用法见[统一操作](common/operations.md)。浏览器重启后页面 ID 会失效，需要重新列出并明确选页。

MCP 和桌面应用的浏览器控制使用扩展；Playwright 用于 CLI/Runtime，Selenium 保留用于 QA。完整步骤见[安装指南](common/installation.md)、[桌面应用](common/desktop-app.md)和[扩展指南](browser-extension/README.md)。

升级 Python 包：

```sh
pipx upgrade saygo-agent-control
```

升级后重启 Agent 客户端。Python 包、桌面应用和浏览器扩展分别分发；包升级不会更新浏览器扩展，普通包升级无需重复 setup，旧安装迁移见安装指南。

### 文档结构

文档按 **公共能力 + 六端操作** 编排。Windows 与 macOS 指被操作的系统；桌面应用是公共入口。Linux 可运行服务和桌面应用并连接浏览器、手机，目前不支持本地 Linux 窗口控制。WSL 是 Windows 的连接环境，Selenium 是 QA 兼容后端，均不另算一端。

| 指南 | 主要内容与前提 | 需求 |
| --- | --- | --- |
| [公共能力](common/README.md) | 安装、会话、任务、工作流、桌面应用、QA、架构与发布 | [总索引](common/requirements.md) |
| [Windows](windows/README.md) | 原生或 WSL 连接；窗口、后台与显式前台操作 | [Windows 需求](windows/requirements.md) |
| [macOS](macos/README.md) | 屏幕录制与辅助功能权限；窗口、整机与实验性后台操作 | [macOS 需求](macos/requirements.md) |
| [Android](android/README.md) | 真机或模拟器；SDK/Appium、设备授权、Windows 与 WSL 主机 | [Android 需求](android/requirements.md) |
| [iOS](ios/README.md) | 本地需 macOS 与完整 Xcode，或连接远程 Appium；真机签名与模拟器 | [iOS 需求](ios/requirements.md) |
| [Chrome/Edge 扩展](browser-extension/README.md) | 已登录标签页、本地桥、后台截图、页面与网络记录 | [扩展需求](browser-extension/requirements.md) |
| [Playwright](playwright/README.md) | CLI/Runtime 托管 Chromium、CDP、页面绑定与恢复 | [Playwright 需求](playwright/requirements.md) |

更多入口：[交互任务与接管](common/operations.md) · [声明式工作流](common/workflows.md) · [BDD QA](common/qa.md) · [非视觉断言 / Probes](common/probes.md) · [架构](common/architecture.md)。

### 数据与隐私

桌面应用和 QA 会将截图、任务或用例内容发送给用户配置的模型服务；外部 Agent 接收的观察由其自身配置处理。任务记录和导出可能包含输入文字、截图及应用数据。

浏览器扩展连接后默认记录当前配置文件内网站标签页的 HTTP、WebSocket 和 SSE 流量，包括可获取的正文与请求头，可能含 cookie、token 或个人信息。记录默认保留在扩展内存，查询和导出会将数据交给调用方。分享证据前请检查内容。详见[扩展隐私说明](browser-extension/privacy.md)。

### 开发、测试与维护

开发前阅读 [AGENTS.md](../AGENTS.md)；项目隔离安装见[安装指南](common/installation.md)。按修改范围运行[测试与验收](common/testing/README.md)中的检查，Python 核心离线测试入口为：

```sh
python3 scripts/check_core_tests.py
```

离线模拟、真实设备端到端、干净环境安装和发布检查分别记录；跳过不等于通过，单平台测试不代表六端均已验证。[代码核对记录](common/requirements-audit.md)说明实现与缺口，[更新历史](common/history/CHANGELOG.md)和[发布记录](common/history/README.md)保留对应版本的证据。源码实现、正式发布和用户安装状态分别确认。

本 README 在同一文件维护中英文，详细指南目前主要为中文。共用行为写入 `common`，端特有行为写入对应目录；需求变更保留编号并更新操作、测试链接，历史结论按日期归档。开发规范统一维护在根目录的 `AGENTS.md`；客户端 Skill、命令模板和可执行测试资料保留原加载位置。

## English

**You say it. Saygo does it.** Saygo gives external coding agents visual control of computers, browsers, and phones: observe a screenshot, perform an action, and verify the result. It also offers a standalone desktop app for natural-language tasks and a BDD runner for test cases and reports.

### Choose an entry point

| Entry point | Use it for | Model configuration |
| --- | --- | --- |
| **CLI / MCP** | Let an existing agent connect to devices, inspect screenshots, and act; CLI and MCP share named sessions and operation semantics | The external agent makes decisions; no Saygo model API key is required |
| **Desktop app** | Describe tasks, manage connections, and hand control to a person through a GUI | Configure a vision model with an OpenAI-compatible API; packaged apps need neither Python nor an agent installation |
| **BDD QA** | Run `.feature` / `.md` cases and generate reports; use probes for backend and other nonvisual checks | Configure a separate QA model and test target |

`saygo device` handles connections, observations, and individual actions. `saygo task` adds persistent progress, human handoff, recovery, and evidence export. Use `saygo workflow` for declared JSON workflows and `saygo run` for BDD tests.

Visual decisions use screenshots, without supplying UI trees or DOM data to the vision model. The loop is **observe → choose one action → execute → observe again**. Input requires a valid observation; actions with uncertain outcomes are not automatically replayed. Human handoff preserves the target and task resource ownership. Returning control triggers a fresh observation; the business outcome still needs verification. See [operations and tasks](common/operations.md).

### Quick start

For an external agent, prepare **Python 3.10+, pipx, and your chosen agent CLI**:

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --client codex
```

Other client choices are `claude`, `both` (Claude + Codex), `qoder`, `qodercn`, and `all`. For Edge, append `--browser edge` to the setup command. For mobile devices, `--mobile` installs Python dependencies; follow the platform guides for SDKs, Appium, and system permissions.

Browser tasks also require these steps:

1. Install [Saygo Browser](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo) and open the HTTP(S) page you want to use.
2. Click **Connect local bridge** in the extension popup.
3. Restart your agent client to load the tools, then ask it to connect and select the target page.

You can also use the CLI directly. With the extension connected, run these commands one at a time:

```sh
saygo device connect --platform browser --backend extension --session web
saygo device pages --session web
# Replace PAGE_ID with the target page ID returned above.
saygo device select-page PAGE_ID --session web
saygo device screenshot --session web
```

Open the screenshot at the returned path before deciding on an action. See [operations](common/operations.md) for input examples and observation IDs. Restarting the browser invalidates page IDs: list pages again and explicitly select the target.

MCP and desktop browser control use the extension. Playwright is available through CLI/Runtime; Selenium remains the QA backend. See the [installation guide](common/installation.md), [desktop guide](common/desktop-app.md), and [extension guide](browser-extension/README.md).

To upgrade the Python package:

```sh
pipx upgrade saygo-agent-control
```

Restart the agent client afterward. The Python package, desktop app, and browser extension are distributed separately; upgrading the package does not update the extension. Routine package upgrades do not require setup again; see the installation guide for migration from older installations.

### Documentation

Documentation is organized into **common features and six control targets**. Windows and macOS refer to the systems being controlled; the desktop app is a shared entry point. Linux can run the service and desktop app to connect to browsers and phones, but local Linux window control is not supported. WSL is a Windows connection environment, and Selenium is a QA compatibility backend; neither is counted as a separate target.

| Guide | Scope and prerequisites | Requirements |
| --- | --- | --- |
| [Common features](common/README.md) | Installation, sessions, tasks, workflows, desktop app, QA, architecture, and releases | [Index](common/requirements.md) |
| [Windows](windows/README.md) | Native or WSL connections; windows, background operations, and explicit foreground control | [Windows requirements](windows/requirements.md) |
| [macOS](macos/README.md) | Screen Recording and Accessibility permissions; windows, full desktop, and experimental background control | [macOS requirements](macos/requirements.md) |
| [Android](android/README.md) | Devices or emulators; SDK/Appium, device authorization, and Windows/WSL hosts | [Android requirements](android/requirements.md) |
| [iOS](ios/README.md) | Local macOS with full Xcode, or a remote Appium server; device signing and simulators | [iOS requirements](ios/requirements.md) |
| [Chrome/Edge extension](browser-extension/README.md) | Signed-in tabs, local bridge, background screenshots, page management, and network records | [Extension requirements](browser-extension/requirements.md) |
| [Playwright](playwright/README.md) | Chromium managed through CLI/Runtime, CDP, page binding, and recovery | [Playwright requirements](playwright/requirements.md) |

More guides: [interactive tasks and handoff](common/operations.md) · [declared workflows](common/workflows.md) · [BDD QA](common/qa.md) · [nonvisual checks / probes](common/probes.md) · [architecture](common/architecture.md).

### Data and privacy

The desktop app and QA send screenshots and task or test-case content to the configured model provider. Observations returned to an external agent are handled under that agent's configuration. Task records and exports may contain input text, screenshots, and application data.

While connected, the browser extension records HTTP, WebSocket, and SSE traffic from website tabs in the current browser profile by default, including available bodies and headers. These records may contain cookies, tokens, or personal information. Records are held in extension memory by default; queries and exports pass data to the caller. Review evidence before sharing it. See the [extension privacy notice](browser-extension/privacy.md).

### Development, testing, and maintenance

Read [AGENTS.md](../AGENTS.md) before making changes. The [installation guide](common/installation.md) covers an isolated development setup. Select checks from the [testing guide](common/testing/README.md) according to the change. To run the offline Python core suites:

```sh
python3 scripts/check_core_tests.py
```

Offline simulations, real-device end-to-end tests, clean installations, and release checks have separate results. Skipped tests are not passes, and one platform passing does not establish coverage of all six targets. The [implementation audit](common/requirements-audit.md) documents code and gaps; the [changelog](common/history/CHANGELOG.md) and [release records](common/history/README.md) preserve evidence for specific versions. Source implementation, publication, and the user's installed version are verified separately.

This README keeps Chinese and English in one file; detailed guides are currently mainly in Chinese. Shared behavior belongs in `common`, and platform-specific behavior in its target directory. Preserve requirement IDs, update operation and test links, and date historical conclusions. Development rules live in the root `AGENTS.md`; client skills, command templates, and executable test material retain their loading locations.
