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

0.4.20 已于 2026-10-14 01:36（UTC+8）发布到 PyPI。以下为本版实际执行结果，
未沿用 0.4.19 的产物验证作为本版通过证据。

| 项目 | 当前状态 |
| --- | --- |
| 缺陷回归 | 先以加强后的产物检查验证公开 0.4.19 wheel，准确拒绝三个缺失文件；修复后 0.4.20 本地产物通过 |
| sdist 与 wheel 构建 | 本地及 CI 均从 sdist 构建 wheel，`twine check --strict` 两产物通过 |
| 三文件完整性 | 上传前已下载 CI 产物严格审计：sdist 与内嵌源码双白名单精确相等、无缺项；全部打包源码逐字节对应 `v0.4.20`，三个插件文件和八个输入修复文件齐全，RECORD 与隐私路径排除通过 |
| 插件实际诊断与配置 | Linux/Windows/macOS 安装后的隔离解释器实际运行 `doctor.py --platform browser --profile device --json`，均通过 `blocking=0`、已安装包可用及 Claude/MCP server 一致检查 |
| 干净安装与重复 setup | CI Linux/Windows/macOS 全通过，首次及重复 setup 均检查插件资源；公开下载 wheel 在 Linux 再次通过完整脚本。插件准备与诊断不等于实际 Agent 客户端加载验收 |
| 核心、插件与兼容性检查 | 本地安装回归 5 项、两处 `claude plugin validate` 和五处版本声明检查通过；CI 核心 1,043 通过/7 跳过、Node 51 通过、Windows 桥接 31 通过、两套 MCP SDK 兼容检查通过 |
| 提交、推送及标签 | 打包修复 `ec45aef`、版本/文档准备 `0e18964` 已推送；不可变 `v0.4.20` 指向 `0e18964`，与远端核对一致 |
| PyPI | [0.4.20](https://pypi.org/project/saygo-agent-control/0.4.20/) wheel/sdist 已公开、均未撤回；版本 JSON、simple 索引、实际下载与 CI 哈希一致，核实当时 latest 为 0.4.20 |
| GitHub / 桌面 / 扩展商店 | 不在本轮发布范围内；不创建公开 Release、不发布新桌面包、不上传商店 |
| 用户安装环境 | 发布收尾只读复核时本地运行时已为 0.4.19，八个输入修复源码与该公开 wheel 完全一致；本轮未执行其升级或修改 site-packages。尚未安装 0.4.20，也未确认已运行客户端重新加载新代码 |

## CI 运行与范围

[Python package 流程 38439172717](https://github.com/WilliamSkyWalker/saygo/actions/runs/38439172717)
由 `v0.4.20` 推送触发。产品源码和所有验证脚本均来自 `0e18964`，无需覆盖
旧标签的浏览器测试。`saygo/platforms`、`saygo/devices`、`saygo/runtime` 与
0.4.19 的源码没有变化，本轮包装了相同的输入修复实现。

| CI 项目 | 实际结果 |
| --- | --- |
| 核心回归 | `scripts/check_core_tests.py`：1,050 项，1,043 通过、7 跳过、0 失败 |
| 扩展 JavaScript | 51 项通过、0 跳过 |
| Windows 桥接 | 原生桥接 17 项、共享发现 14 项，共 31 项通过 |
| MCP SDK | MCP 1.2.0/Pydantic 2.13.5 与 MCP 2.3.0/Pydantic 2.14.1 的 device/full stdio、工具集、schema 与 request query 检查通过 |
| 真实浏览器 | 独立 Chromium 的扩展/native host/后台截图滚动 4 项通过（186.426 秒）；Playwright 1 项通过（12.228 秒），无跳过 |
| 构建附加回归 | 安装 33、升级 14、桥接 17，共 64 项通过；Node 51 项也通过 |
| Ubuntu | 24.04.5 x64、Python 3.11.17：wheel 安装、资源、doctor、MCP 与重复 setup 通过 |
| Windows | Server 2025（10.0.26100）x64、Python 3.11.9：同上全部通过 |
| macOS | 26.6.2 arm64、Python 3.11.9：同上全部通过，无路径别名导致的 doctor 重执行超时 |

## 公开产物与分发核对

| 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `saygo_agent_control-0.4.20-py3-none-any.whl` | 1074842 | `dfbcdfd916689d6252c34a6582cb94081b546b496afbfd0a20d11ac7b7d729e6` |
| `saygo_agent_control-0.4.20.tar.gz` | 573196 | `afe83cb42a0f5386d68a7fd810b703a9eed3336c83d1b86fe0b4e4c4e48ac878` |

上传前 CI 产物审计通过；发布后公开下载的两文件与 CI、PyPI JSON 和 simple
索引一致。186 个内嵌源码、sdist 中 186 个标签文件及 wheel 的 111 个直接
源码文件均完成原始字节比对。公开 wheel 又在独立 Linux 环境完成
`scripts/check_python_package.py`，包括实际 doctor JSON 诊断和重复 setup。

推送标签时暂时停用会额外发布 GitHub Release/商店包的 `release.yml`，随后
已恢复 `active`；核实该标签无该流程运行、无公开 GitHub Release。Python
发布检查始终启用，完整流水线一次通过，用时 6 分 12 秒。

## 升级和已有插件修复

PyPI 0.4.20 已核实公开可用，按原安装方式升级，例如
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
