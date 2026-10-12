# 0.4.16 发布验证

本次获明确授权发布需要更新的模块并升级版本。Python 包、托管安装器、native host
和桌面产物采用 0.4.16；扩展文件未改，保持 0.4.13。0.4.15 曾撤回，不复用。

## 发布前已有证据

- 共享发现回归：WSL 与原生 Windows 各 14 项，通过真实 host 子进程和文件 IPC，
  扩展消息对端及系统注册布局为测试注入，不能当作真实 Chrome 验收。
- WSL bridge 16 项、package 更新 17 项、桌面 offscreen Qt 45 项通过。
- 隔离 Linux Chrome 的 3 项真实扩展用例已取得成功结果，包含 MCP 退出重启、
  页面恢复、实际截图与输入结果。此前本地运行使用 headless；本次发布 CI 使用 headed。
- 用户授权页面在实际 PyPI 安装的两个 MCP 进程中返回截图；现有连接未被断开。
  此项验证了现场配置恢复，不代表新版本已发布或安装。

## 本次发布检查

以下项目以本次执行和远端工作流结果更新；待执行不能计为通过。

| 项目 | 状态 |
| --- | --- |
| 完整 Python/Node 回归 | Python 928 项：922 通过、6 项环境测试跳过；Node 4 个扩展测试文件通过 |
| Windows 原生补充复核 | bridge 16 项、共享发现 14 项、桌面 offscreen 45 项均通过 |
| sdist → wheel、严格元数据检查、Linux 干净安装及重复 setup | 候选构建通过；包括 MCP 导入、共享发现资源和 native host 版本检查；最终标签由 CI 重建验收 |
| 标签 CI：核心、Windows bridge、真实 Chrome 和 CLI Playwright | 待执行 |
| 标签 CI：Linux/Windows/macOS wheel 安装 | 待执行 |
| 原生桌面三平台构建、Qt 启动及产物 | 待执行 |
| PyPI 文件、simple 索引及下载哈希 | 待发布后核实 |
| GitHub 源码、安装器、校验和与桌面附件 | 待发布后核实 |

没有执行 macOS/Android/iOS 的完整真实设备业务流程。桌面构建是未签名的 beta
产物；构建成功不等于六端端到端全部通过。浏览器商店状态与 Python 包发布分别核实。

本地完整回归首次受沙箱权限影响停在 MCP SDK 异步用例；该用例在正常本地 IPC
权限下通过，随后完整套件通过。6 项 skip 是两项 Windows 真桌面场景、三项 Chrome
扩展场景和一项 CLI Playwright 场景；真实浏览器部分由独立发布 CI 执行。

## 首次远端预检发现

- Windows runner 的 TEMP 包含 8.3 短路径别名；测试注入的目录未规范化，而生产
  发现结果已规范化，导致路径比较与标准目录模拟失败。测试夹具改为规范化根目录，
  保留原断言及真实 host IPC，不放宽连接选择规则。
- Linux runner 缺少 `libEGL.so.1`，导致 9 项 Qt 测试跳过且源码 Qt 启动失败。
  核心与桌面 CI 安装 `libegl1`、`libopengl0`，并先强制导入 Qt，避免依赖缺失静默跳过。
- macOS 首次预检已经通过实际冻结程序 Qt 启动、native host 握手/IPC 与 DMG 打包。
  最终产物仍须来自最终发布提交，不能混用较早候选的附件。
