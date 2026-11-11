# 1.0.1 发布与验证记录

日期：2026-11-11。用户明确授权提交、推送和 PyPI 1.0.1 发布。
范围为 Python runtime 和客户端插件；扩展沿用 1.0.0，浏览器协议不变。
不创建新的公开 GitHub Release、不提交商店、不发布原生桌面包。

## 修改与兼容性

- `devices/observations.py`、`actions.py`：仅用当前观察绑定的少量已有帧，
  为浏览器单点动作验证有限、远离目标的重复局部画面；保存拒绝时实际比较帧、
  变化比例与边界。保持目标身份、上下文和新内容拒绝，候选证据缺失时不放宽。
- `devices/service.py`：正确返回重新观察标志；等待后复用最后采样帧及其时间，
  操作日志复用观察。无长期学习、额外模型调用或自动重放。
- `mcp/update_policy.py`、`server.py`：发现更新后要求用户选择升级/本次继续，
  异步刷新旧缓存；选择仅限当前 MCP 进程。选择升级不会执行安装。
- `devices/requests.py`、`runtime/interactive.py`：新增可信调用方的派发前钩子，
  位于去重后、持久意图前；更新拒绝不占用请求 ID，历史结果及人工核对仍可访问。
- 操作协议、安装说明和回归测试同步；Python、内嵌发行元数据、native host 与
  两种客户端插件 manifest 升为 1.0.1。浏览器扩展 manifest 仍为 1.0.0。

已有会话和记录无需清空。旧观察无候选证据时保持严格比较。
包用户升级后须重启 Agent 客户端；复制式插件按原配置重复 setup。
当前用户安装未升级，在线浏览器和 native host 未被重载或断开。

## 本地验证

环境：Linux/WSL x86_64、Python 3.12。所有自动输入回归使用隔离状态目录和模拟驱动。

- 修复前回归已复现局部变化拒绝、错误恢复标志与缺少图片；修复后定向回归通过。
- 两项 `claude plugin validate`（仓库根及 `plugins/saygo-device`）通过。
- 现场已保存图片的离线回放验证重复局部画面规则，未发送真实输入，私有图片不入库。
- `python3 scripts/check_core_tests.py`：需求用例同步检查通过；control 850 通过/2 跳过，runtime 43 通过，desktop 37 通过/9 跳过，CLI 23 通过，mobile 136 通过/1 失败。脚本在 mobile 停止。
- mobile 失败为 `test_worker_discovery_does_not_import_client_dependency_guidance`：本 WSL 环境的隔离 worker 导入缺少 `mobile_host`。在修改前 `f505ed8` 的隔离源码上复现同一失败；未将其修复或记为通过。
- 随后独立运行剩余套件：browser 14 通过/1 跳过，extension 34 通过/6 跳过，vision 10 通过。合计 1,147 通过、18 跳过、1 项基线同样失败；不声称整个核心脚本通过。
- `/tmp/saygo-release-101-env/bin/python -m build --no-isolation --outdir /tmp/saygo-pypi-1.0.1`：sdist 及由该 sdist 构建的 wheel 成功；隔离发布环境中的 build/setuptools 后端已独立安装。
- `python -m twine check --strict`：wheel/sdist 均通过。包清单检查确认新升级策略、操作 Skill、内嵌插件齐全，五处 runtime/插件版本均为 1.0.1，扩展为 1.0.0；没有混入配置、会话、截图或私有测试。
- `scripts/check_python_package.py`：Linux/WSL 的新临时 venv 中安装 wheel `[mcp]`、CLI/setup help、首次 prepare-only setup、插件 doctor、MCP 导入/版本与重复 setup 全部通过。仅验证包安装和导入，不等于 stdio 握手或真实设备验收。
- 本地构建产生既有 license table/classifier 弃用警告；严格元数据检查仍通过，本次未扩展修改打包许可证声明。
- MCP stdio：修改后在 SDK 1.27.2 / 2.2.0 下初始化 45 秒超时；隔离的修改前
  HEAD 在 SDK 1.27.2 下同样超时。本次不把既有基线超时描述为通过。
- Windows、macOS、Android、iOS、真实 Chrome 扩展与 Playwright 本次均未新增实机验收。
  真实浏览器测试缺少独立浏览器和 Playwright 依赖，依赖安装请求被中止。

## 发布状态

准备中。采用非 `v*` 的 `pypi-1.0.1` 标签固定源码，并通过已有 Python package
工作流的 `workflow_dispatch` / `publish=pypi` 发布。这样不会触发 `v*` 对应的
GitHub Release 和 Chrome Web Store 自动提交。云端只构建/发布，不重新加入已移除的云测试。
发布后分别核对远端提交、固定标签、工作流结果、公开 wheel/sdist 与 SHA256。
