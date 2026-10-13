# common：公共能力

[返回文档入口](../README.md)

先阅读需求和共用操作，再按 [Windows](../windows/README.md)、[macOS](../macos/README.md)、[Android](../android/README.md)、[iOS](../ios/README.md)、[浏览器扩展](../browser-extension/README.md)、[Playwright](../playwright/README.md) 处理端特有要求。

## 使用与操作

| 文档 | 解决的问题 |
| --- | --- |
| [需求总索引](requirements.md) | 公共需求及六端独立清单；功能归属、实现和验收状态 |
| [代码核对记录](requirements-audit.md) | 从源码补出的需求、代码定位、已知缺口与验收边界 |
| [安装与客户端](installation.md) | pipx、源码开发、托管安装器、升级卸载、客户端权限与配置 |
| [统一操作](operations.md) | 会话、观察坐标、动作、任务、接管、诊断及恢复 |
| [声明式工作流](workflows.md) | JSON 资源/步骤、数据传递、只读查询、人工步骤和崩溃恢复 |
| [桌面应用](desktop-app.md) | 模型配置、对话任务、本机/浏览器连接、凭据与原生打包 |
| [BDD QA](qa.md) | 用例组织、模型判定、报告、辅助工具与旧报告渲染 |
| [非视觉断言](probes.md) | 数据库/埋点检查、插件注册、三态结果与轮询 |

## 开发、测试与交付

| 文档 | 解决的问题 |
| --- | --- |
| [架构](architecture.md) | 模块职责与执行路径 |
| [测试与验收](testing/README.md) | 自动化用例映射、执行命令与真实环境验收 |
| [桌面回归](testing/desktop.md) | 模拟模型/系统依赖的测试范围 |
| [构建与发布](release.md) | 源码/扩展/桌面/Python 包、安装验证与发布核对 |
| [当前版本发布说明](release-notes.md) | 供发布流程读取的版本说明 |
| [性能实现与计划](performance.md) | 已实现优化、历史基准、后续计划和已否决方案 |
| [官网维护](website.md) | 静态站点、语言、资源和部署 |
| [历史记录](history/README.md) | 版本变更、历史验收和提交说明 |

浏览器商店材料与隐私说明归入[扩展端](../browser-extension/store.md)。开发约束统一见根目录 [AGENTS.md](../../AGENTS.md)。
