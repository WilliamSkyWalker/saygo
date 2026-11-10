# 1.0.0 发布准备与验证

记录日期：2026-11-10。用户已授权升至 1.0.0、提交推送、发布 PyPI 和浏览器插件。
本记录保存升版前及 1.0.0 源码验证；版本构建、发布 CI、公开文件核验及 1.0.0 商店状态尚待补录，
不能将以下源码测试写作 1.0.0 构建产物已通过或已上线。原生桌面安装包不在本轮发布范围内。

## 修改范围

| 模块 | 问题与行为变化 |
| --- | --- |
| 浏览器扩展选页 | `select-page`、`select_page` 和显式页面连接只改变 Saygo 控制绑定，不再激活可见标签；保留原活动标签和桌面前台。过期页面仍明确拒绝，截图与输入使用所选目标 |
| 后台链接动作 | 新增 `open_link_background`：按有效观察的坐标，在驱动隔离执行环境中命中节点并最多检查八层祖先，仅取普通 HTTP(S) 链接 URL，在同窗口创建非活动标签，返回 `created_page_id`，保留原控制目标 |
| 共享入口与桌面决策 | 扩展 Python 适配器、共享动作能力与派发、桌面模型动作白名单共用上述动作；保留观察、坐标映射、请求记录和结果未知时不重放的保护。其他后端不宣称具备此能力 |
| 操作协议与需求 | 记录用户授权的窄范围驱动 DOM 命中例外；模型仍按截图决定坐标，不接收 DOM、控件树或链接文本。明确普通点击与后台 URL 导航的差别 |
| Android 首次设置 | 纳入此前本地提交 `d58f6c8`：为 macOS、原生 Windows、WSL/Windows 宿主返回结构化依赖检查和针对当前解释器的修复命令；增加连接前 `doctor --platform android` 与 `--tools-only` 安装模式 |

后台链接动作不执行点击处理器、不保留 opener，也不承诺复制链接的 referrer、命名窗口或下载语义。
非链接、下载和非 HTTP(S) 链接明确拒绝；不自动回退为普通点击，不事后切回其他应用掩盖抢焦点。
普通左键 `tap` 保留原语义，`target="_blank"` 或网页脚本仍可能让浏览器前置。
任意 JavaScript 弹窗、跨域 frame 和 Shadow DOM 不在本次真实验收范围。

Android 指引只诊断并给出命令，不自动安装或替换 Python 环境。WSL 客户端依赖与 Windows
宿主工具链分别检查，远程 Appium 只检查客户端依赖。`--tools-only` 准备 Java、SDK、
Node/Appium/UiAutomator2，不下载模拟器或系统镜像、不创建 AVD；保留 dry-run、许可确认、
显式主机选择和已有会话。检查通过不代表设备在线。

## 已完成的源码验证

### 升版前源码

以下浏览器修改在升版前的源码上验证，当时 manifest/runtime 仍标记 0.4.21。
本地环境为 macOS arm64、Python 3.15.2、Node 24.22.1；真实浏览器为 Chrome 157.0.8103.39。
这些结果与后续 1.0.0 归档、干净安装和发布 CI 分开记录。

| 命令或用例 | 实际结果与范围 |
| --- | --- |
| `node --test tests/extension_demo/test_*.mjs` | 90 项通过；Chrome API 模拟回归，覆盖逻辑选页、后台建页、链接命中/拒绝和已有连接、捕获、输入、网络保护。macOS live 在普通发现中跳过，不计为通过 |
| `python3 -m unittest discover -s tests/extension_demo -p test_bridge.py -v` | 20 项通过；适配器能力、坐标、返回新页 ID、原目标保留，以及真实 native-host 子进程配合模拟扩展的协议检查 |
| `python3 -m unittest discover -s tests/control_demo -p test_agent_service.py -v` | 25 项通过；共享服务、会话、观察、MCP 与持久请求契约，不是所有设备真实操作 |
| `python3 -m unittest discover -s tests/desktop_demo -p test_desktop.py -v` | 10 项通过；桌面决策及后台链接百分比坐标约束等离线检查，不是原生桌面包验收 |
| 显式启用 `test_focus_mac_live.mjs` | 1 项真实 macOS 测试通过，经过 CLI → native host → 实际扩展；独立 profile、本地自有网页、随机独立 host 和 AppKit 前台窗口 |
| Claude 插件校验 | 本机缺少 `claude` 命令，`claude plugin validate .` 与 `claude plugin validate plugins/saygo-device` 未运行，不能计为通过 |

macOS live 检查初始 debugger 就绪、无浏览器请求的一秒前台基线、选择/重复选择、新建页、
后台截图及输入、后台读取链接 URL 建页、选择新页后的截图及输入，以及非链接按钮拒绝后
页面集合不变。持续采样前台进程 PID 和相关窗口顺序；验证新页 ID、原控制目标及输入结果。
连接弹窗、输入页和后台新页的 PNG 已实际返回并查看。截图文件保留在本地临时目录，
不纳入公开源码或发布包。

测试读取标签状态使用扩展 worker；未暴露 worker 时明确指定 CDP `userGesture:false`，
页面 DOM 结果校验放在全部焦点检查之后。早期用页面 `evaluate` 作测试观察会附带用户手势，
污染前台判定，已纠正该测试方法，不能把那次失败归因于生产截图路径。修正观察方法后，
普通左键打开新标签仍实际触发前置；它作为独立失败复现保留，不计入通过。截图实现没有因此改写。

Android 的 `d58f6c8` 提交此前在同一 macOS 环境记录了 180 项单元/契约测试通过，
包括 mobile_demo、控制、接管、MCP profile 和 CLI；设备、Windows/WSL 宿主为模拟。
缺失的 Appium/Selenium 测试依赖曾仅从临时 wheel 路径载入，没有全局安装。
源码 doctor 和 tools-only dry-run 的只读检查已执行，没有安装 Android 工具或操作设备。
这 180 项是该提交的已有证据，不冒充本次重新运行或 1.0.0 包安装结果。

### 1.0.0 源码真实 macOS 复验

2026-11-10 另行运行同一隔离测试，manifest 和 Python 包版本均已确认为 1.0.0。
环境为 macOS 27.0 arm64、Python 3.15.2、Node 24.22.1、Chrome 157.0.8103.50。
`SAYGO_TEST_HEADED=1` 配合明确的浏览器、Python、Playwright 模块和截图路径，执行
`node --test tests/extension_demo/test_focus_mac_live.mjs`：**1 通过、0 失败、0 跳过，
用例耗时 85.637 秒，总耗时 85.711 秒，退出码 0**。

复验经过真实 CLI → 独立 native host → 实际 1.0.0 扩展；选择、重复选择、新建页、
后台截图/输入、后台链接 URL 建页、新页截图/输入和非链接拒绝全部通过。
全过程的前台进程 PID、相关窗口顺序及瞬时变化断言通过；新页 ID、原目标保留、
点击处理器未执行与非链接拒绝后页面集合不变均已核对。
测试只关闭自己的临时 profile、host 和前台测试窗口，没有操作用户已有扩展或 host。

三张实际 PNG 已在 03:28 UTC 完成查看：扩展弹窗显示 `Saygo 1.0.0`、`Connected`；
新建页显示 `Background input verified`；后台链接页显示 `Popup input verified`。
以下为本地证据文件的 SHA256，图片不进入公开包：

| 本地文件名 | SHA256 |
| --- | --- |
| `saygo-focus-result-popup.png` | `f401ab1a56179e164e28f60676b6fa872090f99d02182062b9ec6a8fe3211a45` |
| `saygo-focus-result.png` | `8a34561280b099b3417404eaae44fdad04b89cefef989f7c45062721044a5beb` |
| `saygo-focus-result-webpage-popup.png` | `da6a92740efd34339fbce76765d00d1591f86930d5c0e279a46364ca407e55f0` |

这次是升版后的仓库源码复验，不是 wheel/sdist、发布 ZIP、商店安装或用户现有环境升级验收。
此前标记 0.4.21 的测试结果仍保留在上一节，不合并为同一次测试。

## 1.0.0 本地包验证

在独立临时 Python 3.15.2 venv 中执行 `python -m build --outdir ...`，成功构建
sdist 及由 sdist 构建的 wheel；`python -m twine check --strict` 两项均通过。
`python scripts/check_python_package.py <wheel>` 在仓库外的新 venv 完成 wheel 安装、
CLI/setup 帮助、首次 prepare-only setup、插件资源/版本与 doctor、MCP 导入和重复 setup，
退出码 0。没有向用户客户端注册或更新其安装。

升版后另行执行 Node 全部回归：90 通过、1 项 opt-in live 跳过；Python 桥接 20、
共享服务 25、桌面决策 10 项均通过。`render_requirement_cases.py --check` 确认
638 个独立 BDD / unittest 用例同步，`git diff --check` 通过。
本地包仅作预检，正式发布产物仍由匹配标签的 CI 重新构建和检验。

## 升级与兼容性

1.0.0 发布完成后，按原安装方式升级 Python runtime，并重启 Agent 客户端加载动作协议。
复制式插件安装需要按原客户端及目录重新 setup，以更新共享 Skill；保留无关客户端配置。
后台链接动作需要匹配的 runtime 与实际加载的扩展，Python 包升级不能替代浏览器扩展更新。
核对磁盘注册、在线 host 与浏览器实际加载版本，不能仅比较包版本。

逻辑选页与此前可见标签切换不同：用户可继续停留在当前标签，Agent 的观察和输入作用于
明确绑定的另一页。会话和任务数据库不要求清空；浏览器重启导致旧 page ID 失效时仍须显式重选。
不重放未知结果的输入，不自动重载或断开用户扩展，不结束在线 native host；由用户选择升级、
重连或手动加载开发包的时机。商店送审、审核通过、实际分发和用户已加载新版必须分别确认。

## 发布检查与状态

本轮[发布前只读商店核验](https://github.com/WilliamSkyWalker/saygo/actions/runs/42747930084)
确认当前发布版本为 0.4.21，状态 `PUBLISHED`、分发比例 100%，`submitted` 为 `{}`。
这是旧版本的当前分发状态，不表示 1.0.0 已上传、提交审核或上线。

| 项目 | 当前记录 |
| --- | --- |
| 1.0.0 版本元数据、提交与标签 | 六处版本元数据统一为 1.0.0；浏览器修复提交 `0874dd1`，发布提交及标签待远端核对 |
| 1.0.0 本地构建、文件白名单与 SHA256 | sdist→wheel 构建、两项严格 twine 检查通过；六处版本、四项产物摘要、源码/扩展 ZIP 文件排除规则及商店包无 key 均核对通过 |
| 发布 CI、Windows/macOS/Linux 干净安装及重复 setup | 本地 macOS wheel 干净安装、doctor、MCP 和重复 setup 通过；三平台 CI 待执行 |
| PyPI wheel/sdist | 待发布；公开索引、下载摘要及构建产物一致性待核验 |
| GitHub 发布产物 | 待构建/发布及公开下载核验 |
| 浏览器商店上传与提交审核 | 待执行；未记录 1.0.0 送审成功 |
| 浏览器商店审核与分发 | 发布前核验为 0.4.21 `PUBLISHED` / 100%，`submitted: {}`；1.0.0 审核与分发尚未发生，不以流程成功代替上线 |
| 用户安装环境 | 本轮源码验证未升级当前用户安装、重载其扩展或关闭已有 host |
| 原生桌面二进制 | 不在本轮发布范围；源码/离线桌面决策检查不等于桌面安装包更新 |

本轮尚无 Windows、Linux、Edge 或 Playwright 的新版焦点/链接真实验收；也未新增 Android、
iOS 真实设备验收。完整平台矩阵、构建产物安装与分发状态须依据后续实际结果补录，不能宣称六端全部通过。
