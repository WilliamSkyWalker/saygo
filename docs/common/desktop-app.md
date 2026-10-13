# Saygo 桌面应用

[公共文档](README.md) · [GUI 需求](requirements.md#gui)

桌面应用是六端共用入口，采用 Qt 6 Widgets + PySide6，复用统一控制服务与持久交互运行时。打包用户不需 Python、pip、编程 Agent 或 pyenv；需要自己配置兼容 OpenAI 接口的视觉模型。

仓库保留的 [0.4.16 下载](https://github.com/WilliamSkyWalker/saygo/releases/tag/v0.4.16)记录包含 Windows x64、macOS arm64、Linux x86_64 原生归档和摘要；实际发布证据见[历史验收](history/release-0.4.16.md)。

## 安装与启动

Windows 解压整个便携 ZIP，保留 SaygoDesktop.exe、SaygoNativeHost.exe 和 _internal，再运行主程序；GUI 不开控制台，独立 host 通过 stdio 服务浏览器。macOS 使用对应 DMG，屏幕录制和辅助功能权限由用户授予，再“重新检测本机”。Linux 可运行 GUI 并连接浏览器/手机，但不支持本地 Linux 窗口自动化。

开发者在源码目录运行：

```sh
python3 -m pip install '.[desktop]'
saygo-desktop
```

Windows/macOS 按需加 windows/mac 依赖，手机依赖仍可选。WSLg 可运行 Linux GUI，Windows 分发产品则是原生 Windows 包。

## 模型与凭据

首次欢迎界面提供模型设置、连接和示例任务；示例只填入输入框，不自动执行。配置 API 基础地址、视觉模型名和密钥；“测试”发送生成的测试图，可能产生提供方费用，不能只测文本。

远端必须 HTTPS，HTTP 仅允许本机回环；拒绝带凭据、查询串或片段的地址及不安全重定向。模型请求不自动重试。配置修改会使旧测试反馈失效，保存/测试结果在对话框内显示。

密钥仅存本次内存或受支持的 OS 凭据库，不写 desktop.json、任务记录或导出。安全存储不可用时取消“记住”，不会回落明文。取消记住不删除以前保存的凭据，须显式删除；删除成功后才清空输入。Token 可显隐，关闭对话框后重新遮罩。其他设置在 SAYGO_HOME_DIR 或 ~/.saygo。

截图、应用入口清单和任务文字会发给用户选定的模型服务。当前使用兼容 OpenAI 的格式，不直接实现 Anthropic/Gemini 原生格式。

## 对话任务

侧栏显示历史任务、模型与连接入口，中间为消息/进度，底部为输入框。Enter 发送，Shift+Enter 换行；人工接管时在输入框回复以继续当前任务。观察按钮可查看最新截图，不确定动作仍需显式核对。

1. 原生 Windows/macOS 自动连接“本机电脑”，无需窗口标题；窗口级/手机连接保留在高级设置。
2. 点击“连接 Chrome / 安装扩展”，注册商店扩展本地桥并打开商店页面。用户完成安装，在扩展弹窗点击 Connect local bridge；桌面应用检测连接，桥在线但没网页时提示打开网页。
3. 默认选择电脑及已连浏览器，可取消本次不用的目标。检测不激活标签，不在任务或人工接管期间自动更换绑定。
4. 描述任务。模型先观察本机，按需使用浏览器；未使用的休眠标签不阻塞本机观察。任务恢复保留资源选择。
5. 整机任务启动时应用最小化，接管/结束后恢复；运行中可从任务栏打开应用暂停或停止。
6. 重开应用可加载任务并重新观察；结果不明的输入需核对，启动时不重放。

Windows 从开始菜单快捷方式/Get-StartApps，macOS 从系统及用户应用目录提供启动清单，不读取应用内容或声称覆盖全部便携应用。启动前校验清单入口与本机绑定，先记持久意图，不要求旧桌面像素/焦点保持不变；启动后重新截图验证。点击与输入继续遵守 30 秒观察、身份、画面变化检查。

暂停/停止等待当前 API/设备调用返回，再阻止下一次派发，不能撤销已发送输入。模型请求超时 30 秒，一轮最多 30 步后接管；不确定动作停止自动执行。连续三次观察失败或六次诊断/修复决策后也接管，不能无图宣称完成。

任务完成是模型基于画面给出的判断并记录为证据，不是独立业务系统断言。当前没有流式聊天、桌面自动更新、已签名安装器或图形化手机工具链向导。

## 实现与构建

Qt/PySide6 能直接复用 Python 控制服务。Tauri 需 Rust 和各架构 Python sidecar，pywebview 需额外 web 资源及系统 WebView，原方案选型保留此取舍。参考 [Qt for Python](https://doc.qt.io/qtforpython-6)、[Tauri sidecar](https://v2.tauri.app/develop/sidecar/)、[pywebview 打包](https://pywebview.flowrl.com/guide/freezing)。

```sh
python3 -m pip install pyinstaller
python3 scripts/build_desktop.py
python3 scripts/check_desktop_build.py
python3 scripts/package_desktop.py
```

必须在目标系统构建。目录产物在 dist/desktop/SaygoDesktop，macOS 另有 .app；归档在 dist/installers：Windows ZIP、macOS 含 Applications 快捷方式的 DMG、Linux tar.gz，各有 SHA256。

工作流验收实际冻结程序的离屏 Qt 启动、host 版本/握手和私有文件 IPC，再归档；扩展对端为模拟夹具，不是 Chrome 端到端。发布附加匹配标签的 `SaygoDesktop-<version>-<platform>-<architecture>`。签名、公证、依赖许可说明及干净机器测试另行处理，Qt 许可义务仍适用。

## 已有证据与限制

历史 Windows 原生 Python 3.13 的 45 项桌面测试（离屏 Qt）通过；本机连接、整屏截图和应用发现有原生检查。冻结 GUI 曾通过可见启动，PE 类型确认主程序窗口模式和独立控制台 host，host 握手与 ZIP 构建通过。

0.4.16 标签的 Windows x64、macOS arm64、Linux x86_64 CI 分别通过桌面测试、冻结离屏 Qt、host 版本/握手/模拟 IPC 及归档；macOS 另通过 hdiutil verify。没有 Intel macOS 归档。详细记录见[发布验收](history/release-0.4.16.md)。

这些结果不证明干净用户机器的系统权限、真实模型完整任务、任意应用兼容、签名或公证。真实模型任务需要用户提供模型及指定测试应用；各操作端的限制仍分别生效。
