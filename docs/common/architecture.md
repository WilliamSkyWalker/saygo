# 架构与模块职责

[公共文档](README.md) · [开发规范](../../AGENTS.md)

Saygo 以共享设备服务连接 CLI、MCP、交互任务与桌面应用。视觉决策使用截图，平台驱动执行操作；显式工作流与 QA 模型循环分别维护自己的入口，避免将测试判定语义套进通用任务。

## 模块划分

| 模块 | 职责 |
| --- | --- |
| saygo/cli.py、config.py、logger.py | 稳定 CLI 入口、共享配置与日志；构建帮助不加载 QA 或可选平台依赖 |
| commands/ | 各命令族的参数、分派和输出 |
| devices/ | 共享服务、会话、观察/动作、设备发现、模拟器/工具链及 Windows worker/relay |
| platforms/ | Appium、浏览器、桌面及实验性 RDP 驱动；持久绑定与控制器重连 |
| runtime/ | 交互任务、声明式工作流、SQLite 状态/只读查询、锁、接管与不确定动作 |
| desktop/ | Qt 界面、视觉模型客户端、每轮一个决策的任务执行器 |
| qa/ | 用例发现、准备、调度、Gherkin、规划、逐步执行、证据校验、失败分析及报告 |
| vision/ | 图像网格、元素定位及稳定帧采样 |
| integrations/ | Figma API/MCP 与浏览器 native messaging 桥 |
| skills/ | 可选截图分析组件 |
| probes/ | 非视觉断言及子进程协议 |
| mcp/ | MCP 服务入口与外部 MCP 客户端 |
| drive/ | 已有 Agent 执行日志的 HTML 报告渲染 |

## 执行路径

- 公共设备：CLI/MCP → devices.service → 观察/动作与资源守卫 → platforms.device_session → 驱动；连接和生命周期由 devices.control/mobile 管理。
- 交互任务：CLI task / MCP agent_task / desktop.runner → runtime.interactive → 共享视觉资源；意图先持久化，结果不明须核对。
- 固定工作流：runtime.engine → runtime.resources → 驱动或 SQLite；独立于 QA 模型规划，保留步骤检查点和人工验证。
- QA：commands.run → qa.cases/execution → gherkin/planner → agent/brain → platforms；使用 vision、skills、probes，report 输出报告，healer 分析失败。
- 扩展：platforms.browser_extension → integrations.browser_bridge → native messaging → 浏览器扩展。

## 共享边界

desktop.app 管理界面和后台工作线程，model 处理兼容视觉 API 与凭据，runner 复用交互运行时而不复制任务状态。CLI/MCP 新入口应调用 devices.service，不复制平台分派与错误处理。

platforms.desktop 共享指针、滚动、按键别名、剪贴板输入和长按；原生子类负责窗口、截图、坐标、剪贴板与粘贴修饰键。后台模式另有禁止全局输入的约束，见各端文档。

platforms.device_session.release_controller 负责临时控制器释放：桌面释放、Playwright/扩展断开、Selenium 临时服务清理，同时保留持久会话。QA Grid 的共享清理在 platforms.selenium_grid.cleanup_grid_sessions。

vision.settle 在一次稳定等待中复用上一帧的预处理图，断言采样对首/中/末三帧各预处理一次；缓存仅限本次调用，返回的仍是原始截图。skills.visual_diff 用直方图统计变化，零变化时直接返回当前 RGB 图，区域聚合使用队列。阈值、状态栏遮罩与尺寸对齐语义保持一致。

runtime.store.events 只查询任务是否存在并读取事件，不加载完整 checkpoint。interactive 的时间线格式化共用 _timeline_from_events；导出包中的事件和时间线来自同一次事件读取。写入事务、执行锁、意图持久化和数据库结构保持不变。

devices.mobile.provision_runtime 复用 SDK、Appium 与启动编排，mobile_host 选择本地/Windows 主机，适配器负责连接。Windows 移动 bundle 仅包含包初始化、日志、安装、工具链、worker 和隐藏控制台 Node 脚本，排除配置及凭据；tests/mobile_demo/test_bundle.py 在隔离进程检查不依赖已安装包的导入。

## 兼容入口

`python -m saygo.cli`、`python -m saygo.mcp.server`、`python -m saygo.drive.render`、`python -m saygo.browser_bridge` 保留。桥实现也可通过 integrations.browser_bridge 或单文件运行。内部导入使用所属模块，不在包根目录保留旧私有辅助函数别名。

CLI 只构建参数和分派命令；工作流注册保留在 runtime.cli。qa.cases 统一发现/筛选，qa.device_setup 管设备准备、APK 和重置，qa.execution 管顺序/Grid/多设备调度，共用跳过判定、空结果与平台准备逻辑。MCP 直接导入职责模块。

qa.cases 复用当前目录/TESTS_DIR 的候选路径，绝对目录只遍历一次 feature 文件。账号池、前置条件和显式 Markdown 文件共用 tests 下顶层目标归属；feature 的报告目标仍由最近的 README 决定，保留原有发现优先级与外部文件行为。

对应验证见[测试目录](testing/README.md)。模拟适配器或单一平台检查不能证明六端设备兼容。
