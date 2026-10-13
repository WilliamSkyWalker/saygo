# Saygo 0.4.16：共享浏览器桥与原生桌面连接

Windows 桌面版和 WSL 曾选择不同 native-host 目录，扩展连接一端时另一端可能显示离线，单独升级 PyPI 包也无法解决。本版按浏览器所在系统发现注册及在线 host，使客户端共用连接。

## 浏览器连接与升级修复

- Windows 桌面版、Windows Python 与 WSL 共用桥；新安装使用 %LOCALAPPDATA%/Saygo/browser-bridge，保留已有可用旧目录。
- 报告连接前实际探测 host。多个在线 host、扩展身份不一致或无响应时明确报错，不静默改连浏览器。
- 包启动检查实际注册和在线目录，同版本也修复注册漂移，不断开现有扩展。
- 保留页面绑定，过期时显式建立命名会话并选择正确页面。
- 对 Windows 状态文件共享冲突做有界重试，避免并发读取使 host 退出；不重放浏览器动作。
- 展示真实连接失败原因，native-host 诊断版本为 0.4.16。

## 桌面应用

- 增加首次欢迎流程、Windows/macOS 自动连接本机、应用清单和整机操作。
- 仅在任务需要时观察浏览器，恢复后保留资源选择；任务占用期间暂停自动改绑。
- 改善模型设置、Token 遮罩/管理和连接错误。整机任务时最小化，结束或人工接管时恢复。
- 打包包含 Windows runner 资源，在目标系统生成原生归档，仍为未签名测试版。

## 升级与组件版本

```sh
pipx upgrade saygo-agent-control
```

重启 Agent 加载新代码，包安装保留 pipx 解释器。已有 host 持续运行，直到用户重连才加载新代码，不主动断开。桌面用户手动下载匹配的 SaygoDesktop-0.4.16-*（Windows x64、macOS arm64、Linux x86_64）。

Python 包、托管安装器与新构建 host 为 0.4.16。扩展仍为 0.4.13，协议和 ID 不变，文件未变所以不重新上传。0.4.15 曾撤回，不复用。

## 验证边界

回归覆盖真实 host 子进程与模拟扩展对端、共享目录发现、同版本修复、Windows 文件共享异常。隔离真实 Chrome 测试启动两个独立 MCP 服务，检查页面、实际 PNG 和重启后的输入结果；发布门槛另运行 CLI Playwright。

PyPI 发布前检查 Linux/Windows/macOS 的干净 wheel 安装与重复 setup；桌面执行 Qt 和冻结包启动检查。这些不代表所有系统的完整 GUI 任务通过，不包含 Android/iOS 硬件验收。

## 历史发布核对：2026-10-12

- [PyPI 与三平台安装工作流](https://github.com/WilliamSkyWalker/saygo/actions/runs/38209220447)通过；wheel/sdist 可见且未撤回，标准 pip 下载成功，关键桥接/更新代码与标签逐字节一致。
- [GitHub 0.4.16](https://github.com/WilliamSkyWalker/saygo/releases/tag/v0.4.16)公开，源码、安装器、扩展/元数据及三个桌面归档/摘要共 12 个附件齐全。
- [桌面构建](https://github.com/WilliamSkyWalker/saygo/actions/runs/38208607638)使用匹配标签提交；[产物发布](https://github.com/WilliamSkyWalker/saygo/actions/runs/38209742540)再次核对来源及三个摘要。
- 商店查询确认扩展 0.4.13 已发布，跳过重复上传/提交；未重载用户扩展。

上述为记录当时的核对，详细结果与归档摘要见[0.4.16 验收](history/release-0.4.16.md)。
