# Saygo 文档

**你说，它做。** Saygo 让外部编程 Agent 通过截图、动作和结果核验操作电脑、浏览器和手机，也提供使用自选视觉模型的桌面应用，以及独立的 BDD 测试入口。

[官网](https://saygo.work/) · [源码](https://github.com/WilliamSkyWalker/saygo) · [MIT 许可证](../LICENSE) · [开发规范](../AGENTS.md)

## 文档结构

文档按 **common 公共能力 + 六端操作** 编排。公共规则只在 common 维护，各端说明安装前提、连接方式、特有操作和验收边界。Windows 与 macOS 指操作目标；桌面应用本身属于公共入口。WSL 是 Windows 的连接环境，Selenium 是 QA 的兼容后端，均不另算一端。

| 入口 | 主要内容 |
| --- | --- |
| [common 公共能力](common/README.md) | 需求基线、安装、会话、观察、任务、工作流、桌面应用、QA、架构、测试与发布 |
| [Windows](windows/README.md) | 原生/WSL 窗口连接、应用生命周期、后台和显式前台操作 |
| [macOS](macos/README.md) | 系统权限、窗口/整机连接、实验性后台操作 |
| [Android](android/README.md) | 真机、模拟器、SDK/Appium、Windows 与 WSL 主机 |
| [iOS](ios/README.md) | 真机签名、Xcode 模拟器、远程 Appium 连接 |
| [Chrome/Edge 扩展](browser-extension/README.md) | 已登录标签页、共享浏览器桥、后台截图、页面与网络记录 |
| [Playwright](playwright/README.md) | CLI/Runtime 托管 Chromium、CDP、页面绑定与恢复 |

## 快速开始

安装前准备 Python 3.10+、pipx 和所选 Agent 客户端：

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --client codex
# 其他客户端：claude / both / qoder / qodercn / all
```

重启 Agent 客户端，再按对应端的指南连接目标。浏览器任务先安装 [Saygo Browser](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo)，在扩展弹窗点击 **Connect local bridge（连接本地桥）**。外部 Agent 使用设备操作时不需要配置 Saygo 模型密钥。

- 安装、升级、卸载和客户端配置：[安装指南](common/installation.md)。
- 独立桌面应用及模型配置：[桌面应用](common/desktop-app.md)。
- 会话、截图、单步动作和跨端恢复：[统一操作](common/operations.md)。
- 固定 JSON 流程：[声明式工作流](common/workflows.md)。
- 回归用例及报告：[BDD QA](common/qa.md)。

MCP 和桌面应用的浏览器控制使用扩展；Playwright 仅用于 CLI/Runtime。六端共用“观察 → 决定一个动作 → 再观察”的协议，但各端权限、能力和输入方式不同。

## 需求与验收怎么读

[需求总索引](common/requirements.md)维护公共要求与六端入口；各端独立列出完整操作需求：[Windows](windows/requirements.md)、[macOS](macos/requirements.md)、[Android](android/requirements.md)、[iOS](ios/requirements.md)、[扩展](browser-extension/requirements.md)、[Playwright](playwright/requirements.md)。[代码核对记录](common/requirements-audit.md)列明源码对应关系和缺口；[测试说明](common/testing/README.md)区分自动化契约、隔离集成和真实设备验收。已有实现、测试通过、构建成功、正式发布和用户安装状态是不同事实。

[更新历史](common/history/CHANGELOG.md)与[发布记录](common/history/README.md)保留当时的版本、测试范围和证据。文档整理不代表重新验证了远端发布或商店状态。各端指南列出仍需验收的限制；不能从某一平台或模拟测试通过推导六端全部可用。

## 维护约定

新增共用行为写入 common，端特有行为写入对应端目录；需求变更保留原编号并更新操作与测试链接。历史结论按日期归档，不作为持续有效的发布授权。文档使用中文，命令、接口、配置键、产品名和必要的协议标识保留原文。

根目录仅保留一份 [AGENTS.md](../AGENTS.md)。客户端 Skill、命令模板、测试运行器需要的 README、前置条件和可执行用例保留原加载位置。
