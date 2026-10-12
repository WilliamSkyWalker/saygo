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

以下结果核对于 2026-10-12。发布标签 `v0.4.16` 对应
`b7ecbd28cf31cc761dc4b96171cceeba3b27ad1a`，未改动已验证标签。

| 项目 | 状态 |
| --- | --- |
| 完整 Python/Node 回归 | Python 928 项：922 通过、6 项环境测试跳过；Node 4 个扩展测试文件通过 |
| Windows 原生补充复核 | bridge 16 项、共享发现 14 项、桌面 offscreen 45 项均通过 |
| sdist → wheel、严格元数据检查、Linux 干净安装及重复 setup | 候选与干净提交导出构建均通过；最终标签由 CI 重建，含 MCP/共享发现资源/native host 版本检查 |
| 标签 CI：核心、Windows bridge、真实 Chrome 和 CLI Playwright | 全部通过；Chrome 扩展 3 项及 CLI Playwright 1 项为独立真实浏览器验收 |
| 标签 CI：Linux/Windows/macOS wheel 安装 | 全部通过，包含仓库外干净安装和重复 setup |
| 原生桌面三平台构建、Qt 启动及产物 | 全部通过；实际冻结程序 Qt 启动、native host 版本/握手/IPC 与归档检查 |
| PyPI 文件、simple 索引及下载哈希 | 0.4.16 wheel/sdist 均未 yank；JSON 索引与实际文件哈希一致，wheel 关键修复代码与标签逐字节一致 |
| GitHub 源码、安装器、校验和与桌面附件 | 正式公开、非 draft/prerelease，共 12 个附件；3 个桌面归档哈希与验证构建一致 |

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

## 正式发布与产物证据

- [Python package 38209220447](https://github.com/WilliamSkyWalker/saygo/actions/runs/38209220447)：标签回归、真实浏览器、构建、三平台安装及 PyPI 发布全部成功。
- [Build release 38209220482](https://github.com/WilliamSkyWalker/saygo/actions/runs/38209220482)：源码/安装器发布成功；商店日志确认扩展 0.4.13 已为 `PUBLISHED`，未重复上传或提交。
- [Desktop build 38208607638](https://github.com/WilliamSkyWalker/saygo/actions/runs/38208607638)：Windows x64、macOS arm64、Linux x86_64 三平台构建和实际冻结产物验收成功，提交与标签一致。
- [Desktop publish 38209742540](https://github.com/WilliamSkyWalker/saygo/actions/runs/38209742540)：再次核对构建来源与三个 SHA256 后，发布六个桌面归档/校验附件，没有重新构建或覆盖附件。
- [GitHub v0.4.16](https://github.com/WilliamSkyWalker/saygo/releases/tag/v0.4.16) 与 [PyPI 0.4.16](https://pypi.org/project/saygo-agent-control/0.4.16/) 均已核实。

| 产物 | SHA256 |
| --- | --- |
| `saygo_agent_control-0.4.16-py3-none-any.whl` | `27fccb7483a88c485a3964acdd4888424f0abebd831e8d1d45b528f3f721121f` |
| `saygo_agent_control-0.4.16.tar.gz` | `e6d82d263aabb3ec6529aca12671b6c784498d6c0c2ea2151cf432c6aca93ce5` |
| `SaygoDesktop-0.4.16-win32-AMD64.zip` | `4980819945b71973ca9635e432e5be276f1a54a728cf45dec6527de8d2f26698` |
| `SaygoDesktop-0.4.16-darwin-arm64.dmg` | `765deac639a56dd9c989afad9a965cd5b1b508c4c589eb17400a365f453aed39` |
| `SaygoDesktop-0.4.16-linux-x86_64.tar.gz` | `720266175e7c0f331227300f63d811ee847c6eb8679de95fa859b82b19b54712` |

发布后曾出现版本 API 与 simple 索引不同步，未以此重复发布或升版；等待索引传播后，
`pip download --index-url https://pypi.org/simple --no-cache-dir --no-deps saygo-agent-control==0.4.16`
实际下载成功，wheel 哈希与 PyPI 元数据一致。下载的 wheel 内 `browser_location.py`、`browser_bridge.py` 和
`updates.py` 与发布标签逐字节相同。本轮没有修改用户现有 pipx 环境或断开插件。
