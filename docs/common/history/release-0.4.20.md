# 0.4.20 发布验证

用户于 2026-10-14 明确授权补齐 PyPI 包遗漏的三个插件文件并升级发布。
0.4.19 已发布到 PyPI，包含人工接管输入法修复；本版仅修分发完整性，更新
相应检查、版本元数据与文档，不重新修改 Android/iOS 或 Runtime 产品逻辑。
本轮仍为 PyPI-only，不创建 GitHub 公开 Release、不构建新桌面包、不上传扩展商店。

## 问题与变更范围

`MANIFEST.in` 原插件递归规则仅收录 Markdown 和 JSON，遗漏以下现有文件：

| 文件（相对 `plugins/saygo-device/`） | 用途 |
| --- | --- |
| `scripts/doctor.py` | 插件 doctor 命令调用的诊断脚本 |
| `scripts/saygo_mcp.py` | 插件 MCP 启动辅助脚本 |
| `LICENSE` | 插件许可文件 |

遗漏先发生在 sdist；从 sdist 构建的 wheel 内嵌 `_setup_source.zip` 也缺少
相应文件，因此 setup 复制出的托管插件不完整。0.4.19 的主 CLI/MCP 输入法
代码已进入公开 wheel/sdist；该打包缺陷不能描述为输入法修复未发布或所有 MCP
入口不能启动。原 0.4.19 产物和标签保留不变，以新版本交付补全文件。

本版将这三个文件加入打包范围，补充从 sdist、wheel 内嵌安装资源到首次/重复
setup 插件副本的完整性检查；测试必须核验分发后的文件，不能仅检查工作区。

## 本版验证与发布状态

以下状态随实际结果更新；待执行项目不算通过，也不沿用 0.4.19 的产物结果。

| 项目 | 当前状态 |
| --- | --- |
| 缺陷回归 | 先以加强后的产物检查验证公开 0.4.19 wheel，准确拒绝三个缺失文件；修复后 0.4.20 本地产物通过 |
| sdist 与 wheel 构建 | 本地 `python -m build` 从 sdist 构建 wheel、`twine check --strict` 均通过；CI 最终产物待核实 |
| 三文件完整性 | 本地 sdist、wheel 内嵌源码与完整白名单全部一致，三个插件文件和八个输入修复文件完整，源码字节对应构建输入；CI 最终标签产物待核实 |
| 插件实际诊断与配置 | 本地隔离解释器实际运行 `doctor.py --platform browser --profile device --json`，核验 `blocking=0`、已安装包可用和 Claude/MCP server 一致；三平台 CI 待执行 |
| 干净安装与重复 setup | 本地 Linux 隔离 wheel 安装、资源/MCP 导入及重复 setup 通过；CI Linux/Windows/macOS 待执行，插件准备不等于实际客户端加载验收 |
| 核心、插件与兼容性检查 | 本地 release installation 5 项通过、两处 `claude plugin validate` 通过、五处版本声明一致；CI 完整回归和兼容性检查待执行 |
| 提交、推送及标签 | 本轮已获授权，最终提交、标签及远端一致性待核实 |
| PyPI | 待发布并核实 wheel/sdist、未撤回状态、simple 索引和下载 SHA-256 |
| GitHub / 桌面 / 扩展商店 | 不在本轮发布范围内；不创建公开 Release、不发布新桌面包、不上传商店 |
| 用户安装环境 | 仍为原安装的 0.4.18，未直接升级或修改 site-packages；发布与用户已升级分开记录 |

## 升级和已有插件修复

PyPI 0.4.20 发布核实后，按原安装方式升级，例如
`pipx upgrade saygo-agent-control`。若曾用遗漏文件的包执行 setup，需要对原
客户端重新执行一次 `saygo setup --client CLIENT`，保留原来的 `--root` 等选项，
补齐托管目录中的插件文件；再重启客户端加载更新。普通包升级不会自动重新
复制已经准备的插件目录，不能仅看到版本号变化就认定三个文件已恢复。

本版不迁移任务数据库，不清设备数据，不结束人工接管，也不替用户操作已有
业务页面。原生桌面包与实际加载的浏览器扩展不会因为 PyPI 更新而自动升级。

## 继承的输入验收与限制

Android/iOS 行为保持 0.4.19 实现。Android 证据来自
[0.4.19 输入验收记录](../../android/handoff-validation.md)：独立 API 35 模拟器
使用自有输入页，由源码共用 API 首次连接，后续普通 device CLI 与真实 MCP
Runtime 完成自动中英文输入、人工接管、用户明确确认软键盘/电脑键盘输入、
resume 新观察及再次自动输入；重复接管和暂停态重连也已验证。
本轮没有重新执行真实 Android 输入验收，不能把上述历史结果记为新测。

iOS 新连接保留 Simulator 键盘偏好，但仍只有离线契约验证，无本次真机或
Simulator 人工输入验收。真实过期 Appium 会话重建、多普通键盘切换、故障注入
及显式 workflow human 步仍只有离线覆盖。三平台干净安装和插件文件完整性
不代表六端业务、桌面签名/公证或所有 Agent 客户端加载均已通过。

0.4.19 的全部行为变更、实际发布证据和已知打包遗漏见
[上一版记录](release-0.4.19.md)。
