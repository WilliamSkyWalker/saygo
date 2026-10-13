# 测试与验收

[公共文档](../README.md) · [需求基线](../requirements.md) · [历史记录](../history/README.md)

## 需求与场景映射

当前总索引含 **483 条编号条目**：公共/历史模块 256 条，六端细化 227 条。六端细化继承公共规则，不用总数推算功能数。[requirements.feature](requirements.feature) 有 **638 条独立中文 BDD 场景**，对应 [test_requirements.py](../../../tests/control_demo/test_requirements.py) 的 621 个 unittest 和 [test_updates_package.py](../../../tests/control_demo/test_updates_package.py) 的 17 个集成测试。场景保留 ID、需求标签、假如/当/那么与断言，并在注释中给出精确测试方法名。

本次补全需求未增加或重新执行这些自动化/人工场景；新增条目按源码定位，相关测试文件见六端清单和[代码核对记录](../requirements-audit.md)，尚未建立逐条自动化映射的条目不能称为已覆盖。这些矩阵覆盖若干需求的边界组合，不能将场景数理解成需求覆盖率，也不把 subTest 或重复执行算成额外用例。[acceptance.feature](acceptance.feature) 另有 **66 条**人工/真实环境场景；@manual 表示需要指定主机、设备或隔离夹具及证据，未执行不计通过。

```sh
python3 scripts/render_requirement_cases.py --check
python3 -m unittest discover -s tests/control_demo -p test_requirements.py -v
python3 -m unittest discover -s tests/control_demo -p test_updates_package.py -v
```

修改自动化用例后运行生成器（去掉 --check），再审阅中文 BDD。生成器不执行用例、不修改测试结果。TC 方法名为 test_TC_编号_功能，可用 unittest -k TC_编号筛选；UP 场景的注释直接指向集成方法。

## 按改动选择验证

| 范围 | 自动化检查 | 真实验收入口 |
| --- | --- | --- |
| 观察与动作 | control_demo 的 agent_service/control/requirements | 各端实际截图、输入及结果 |
| 任务/工作流 | runtime_demo 的持久化、去重、恢复、SQLite | 指定跨端业务与断连恢复 |
| QA | cli_demo 的解析、执行、证据与命令 | 独立测试目标及模型调用 |
| 截图计算 | vision_demo 的阈值、状态栏遮罩、帧复用、采样路由和差异区域 | 实际设备截图时延、动画及短暂提示捕获 |
| 非视觉断言 | 指令、JSON、裸参数、用例检出 | 自有数据库/日志与授权数据 |
| 桌面产品 | [桌面回归](desktop.md) | 原生系统权限、真实模型任务 |
| MCP/安装 | control_demo 的后端限制、插件/发布安装 | 客户端真实加载、干净环境及重复 setup |
| 更新/共享桥 | updates、updates_package、browser_location/bridge | 包版本、注册、在线目录及多客户端共存 |
| 扩展 | extension_demo 的 Python/Node 检查 | [扩展端](../../browser-extension/README.md#验收)的 CLI/MCP→host→实际扩展 |
| Playwright | browser_demo、runtime_demo | [Playwright](../../playwright/README.md#验证与边界)的本机测试页 |
| 移动端 | mobile_demo 的命令/Appium 模拟与 bundle | [Android](../../android/README.md#验收与待办)、[iOS](../../ios/README.md#验收与待办) |
| 原生窗口 | control_demo 与 mac_demo | [Windows](../../windows/README.md#验收与限制)、[macOS](../../macos/README.md#验收) |

完整离线套件：

```sh
python3 scripts/check_core_tests.py
```

该脚本分进程和临时状态运行各套件，关闭真实设备测试开关；Qt 使用 offscreen。环境跳过不是通过。真实浏览器另用 scripts/check_browser_tests.py 及对应主机依赖，不将模拟扩展 IPC 当 Chrome 验收。

用例发现、截图与历史查询的定向回归：

```sh
python3 -m unittest discover -s tests/cli_demo -p test_cases.py -v
python3 -m unittest discover -s tests/vision_demo -v
python3 -m unittest discover -s tests/runtime_demo -p test_history.py -v
python3 scripts/benchmark_core_paths.py
```

基准脚本只使用临时目录、合成截图和 SQLite，不连接设备或模型；输出中位数，不设置容易受机器负载影响的耗时断言。回归测试检查结果和重复扫描/解码/读取次数。工作负载及实测边界见[性能记录](../performance.md)。

2026-10-13 源码重构验证：Linux x86_64 / WSL2、Python 3.12.3 下执行 `python3 scripts/check_core_tests.py`，共 985 项，969 通过、16 跳过、0 失败；其中新增 17 项回归全部通过。跳过项为 9 项缺少 PySide6 的 Qt 检查、2 项 Windows 实机、1 项 Playwright 和 4 项真实扩展检查。需求场景生成检查、Python 语法及修改文档的本地链接检查通过。Windows、macOS、Android、iOS、真实扩展及 Playwright 均未在本轮进行端到端验收；安装环境及发布产物未更新。

## 证据标准

修复缺陷先有能复现原问题的断言；验收记录命令、提交、平台、通过/失败/跳过数量和设备类型。安装/连接/升级至少覆盖新装、重复 setup、旧配置、桌面/WSL 共存、客户端退出/重启、断连、过期页面及多连接冲突。

真实端到端必须经过公共 CLI/MCP、实际传输和设备/扩展，实际返回并读取截图，输入后检查结果。使用独立目录、profile、命名会话和测试页，不向业务会话输入测试内容。六端分别留证，不把包安装、单平台、mock 或 skip 说成六端通过。

产物检查另见[发布流程](../release.md)。历史首次缺陷复现的 621 条中有 63 失败、1 错误，其余 557 通过；0.4.14 后续 633 条通过是[当时的记录](../history/release-0.4.14.md)，不能替代当前 638 条的实际执行结果。
