# 0.4.17 发布验证

用户于 2026-10-13 明确授权提交、推送、发布与升版，后续补充网络采集“不限制长度”。发布标签为 `v0.4.17`，提交 `d0f97beef9ff4ba170ec911a57fa6323a6fcdc3b`。用户随后又明确要求升级至 0.4.18，后续状态见[0.4.18 记录](release-0.4.18.md)。

## 发布结果

- [GitHub 正式发布](https://github.com/WilliamSkyWalker/saygo/releases/tag/v0.4.17)：12 个附件齐全，包括源码、带摘要安装器、商店/开发扩展 ZIP、发布清单、校验文件和三平台桌面包及摘要。实际下载的小型产物与 SHA-256 一致；三平台桌面公开摘要与 GitHub 上传摘要一致。
- [PyPI 0.4.17](https://pypi.org/project/saygo-agent-control/0.4.17/)：wheel 与 sdist 的版本 JSON 均已核实可用，未撤回；[发布流水线](https://github.com/WilliamSkyWalker/saygo/actions/runs/38363558695)成功。
- [三平台桌面构建](https://github.com/WilliamSkyWalker/saygo/actions/runs/38363659634)与[附件发布](https://github.com/WilliamSkyWalker/saygo/actions/runs/38364165008)成功，上传前核实与标签相同提交并逐个校验摘要。
- [源码和商店流水线](https://github.com/WilliamSkyWalker/saygo/actions/runs/38363558702)成功。商店返回 0.4.17 为 `PENDING_REVIEW`；当时公开版本仍为 0.4.13，不能声称新扩展已审核上线。
- [官网部署](https://github.com/WilliamSkyWalker/saygo/actions/runs/38363493534)成功；主页及更新后的隐私页 HTTP 200，已核实无固定正文/事件保留上限的说明。

## 实际验证

| 范围 | 结果 |
| --- | --- |
| 七组离线核心回归 | 968 项中 961 通过、7 跳过：两项 Windows、四项真实扩展、一项 Playwright 由独立环境检查 |
| Node 扩展测试 | 49 项通过 |
| Linux 真实 Chrome 扩展、native host、CLI/MCP | 4 项通过，包括后台输入、截图、重启、请求去重及大正文 |
| Linux 真实 Playwright | 1 项通过，包括 CLI、持久会话、工作流与人工接管 |
| MCP SDK | 1.2.0/Pydantic 2.13.5 与 2.3.0 的 device/full stdio、工具集合与输入参数通过；非全中间版本逐一验证 |
| Windows 桥接 | 17 项 host/分帧及 14 项共享发现通过；包含超过 32 MiB 回执的模拟扩展 |
| Linux/Windows/macOS wheel 安装 | 干净环境、仓库外安装与重复 setup 全部通过 |
| 三平台桌面 | 各 45 项测试；冻结 Qt 启动、host 版本/握手/模拟扩展 IPC 与归档检查通过 |

真实大响应通过 Chrome 扩展 → native host → CLI 返回超过 33 MiB 的完整正文，字节长度、SHA-256、中文/emoji 尾部一致，实际从流恢复浏览器已淘汰的正文缓存，并验证大 POST 正文。全部使用自有测试页面；不代表现有业务 CSV 或历史清单已经完整。

## 验证期间修正与边界

预检发现 MCP 最低版本缺少 remove_tool，补受检查的注册表兼容分支；SDK 2.x 测试读取协议字段别名；最低 SDK 固定兼容 Pydantic。另修正测试 Chromium 退出与临时目录删除的先后顺序。

PyPI 流水线首次 Windows 测试遇到错误回执已发布、诊断状态尚未写完的读取竞态。同标签另一条 Windows 检查已通过；只重跑失败作业后通过，未重放业务输入。后续 0.4.18 测试改为有界等待状态发布，产品逻辑不变。

桌面包为 Windows x64、macOS arm64、Linux x86_64，未签名/公证，不含 Intel macOS。四端真机业务与完整真实模型任务未运行。未升级用户本机安装、未断开或重载现有扩展；完整网络修复需要新版扩展及新版 native host 配套使用。
