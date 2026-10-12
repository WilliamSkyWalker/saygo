# 需求与测试

[完整需求](../requirements.md)覆盖整个项目。新增 [requirements.feature](requirements.feature) 有 **633 条独立 BDD 场景**，与 [test_requirements.py](../../tests/control_demo/test_requirements.py) 的 621 个独立 unittest，以及 [test_updates_package.py](../../tests/control_demo/test_updates_package.py) 的 12 个线程/MCP 集成测试一一对应。使用公开、脱敏输入；每个场景都有需求编号、Given、When、Then 和断言。矩阵覆盖不同边界与行为组合，不将 subTest 或一次重复执行算成多条测试。

[acceptance.feature](acceptance.feature) 另有 66 条跨模块/真实环境 BDD 验收场景，涉及资源锁、崩溃恢复、浏览器、移动端、桌面、安装和发布。`@manual` 表示需要指定环境并保存证据；尚未执行不计通过。自动化契约通过也不等于这些验收场景通过。

```sh
python3 -m unittest discover -s tests/control_demo -p test_requirements.py -v
python3 -m unittest discover -s tests/control_demo -p test_updates_package.py -v
python3 scripts/render_requirement_cases.py --check
python3 scripts/check_core_tests.py
```

编辑自动化用例后运行 `python3 scripts/render_requirement_cases.py`，再检查生成的 BDD；生成器不更改测试结果。TC 场景的 unittest 名称为 `test_TC_编号_功能`，可以通过 unittest `-k TC_编号` 单独执行。UP 场景名称直接包含对应 test_updates_package.py 的测试方法名。

| 范围 | 新增自动化断言 | 既有功能/集成测试 |
| --- | --- | --- |
| 动作与观察 | 坐标边界、非法数值、必需字段 | control_demo/test_agent_service.py、test_control.py |
| Workflow | 六类资源、无效结构、引用类型与副本隔离 | runtime_demo/test_runtime.py |
| QA | 平台/优先级/自动化标签、Background、禁止跳步与证据 | cli_demo/test_execution.py、test_commands.py |
| Probe | 指令、JSON/标量类型、裸参数、case 检出 | CLI/QA 执行回归及 acceptance.feature |
| GUI | 模型端点和凭据 URL 约束 | desktop_demo/test_desktop.py、test_recovery.py、test_chat_ui.py |
| MCP | 保存后端与显式后端双重限制 | control_demo/test_agent_service.py、test_plugin_install.py |
| 更新 | 安装模式×当前/目标版本×自动设置、源失败、CLI、启动、缓存 | control_demo/test_updates.py |
| 浏览器桥/网络 | 既有集成套件与新增 BDD 验收 | extension_demo Python/Node 测试 |
| 移动与桌面驱动 | 既有夹具与新增 BDD 真机场景 | mobile_demo、control_demo/test_desktop.py、mac_demo |
| 配置/安装/发布 | 既有安装测试与新增 BDD 验收 | control_demo/test_*install*.py、scripts/check_python_package.py |

新增测试首次执行（修复前）：621 条，63 failures、1 error，均在更新相关分支；其余 557 条通过。该结果保留缺陷复现证据，最终结果另见 [本轮验证记录](results.md)。不把包版本样例当作真实发布状态。
