# 1.0.0 发布与验证记录

记录日期：2026-11-10。用户已授权升至 1.0.0、提交推送、发布 PyPI 和浏览器插件。
本记录保存源码、本地构建和安装证据，以及发布过程的实际状态。用户随后明确要求
“去掉所有云端检查”；云端改为只构建、上传和部署，测试脚本保留本地使用。
原生桌面安装包不在本轮发布范围内。

PyPI 和 GitHub 1.0.0 已公开发布并完成下载核对；浏览器扩展 1.0.0 已上传送审，
状态为 `PENDING_REVIEW`，商店正式分发版本仍为 0.4.21。用户现有安装未升级。

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
本地包仅作预检，正式发布产物由匹配标签的 CI 重新构建；公开产物的本地核对见下文。

## 云端流程调整与失败记录

[第一次预检](https://github.com/WilliamSkyWalker/saygo/actions/runs/42757601234)和
[第二次预检](https://github.com/WilliamSkyWalker/saygo/actions/runs/42783425922)均未通过。
核心 Python 1,128 项中 1,119 通过、9 跳过；Node 90 通过、1 跳过；Windows 桥接
34 项通过；MCP 1.2.0 / 2.3.0 的 stdio 契约通过。这些通过项不改变整轮失败结果。
Linux 实际扩展的五项用例均通过；持久安装/重启用例未完成安装，第二轮在确认扩展条目
出现时超时。后续 Playwright、包构建和三平台安装作业没有执行，不能计为通过。

本地实际焦点测试使用 macOS / Chrome 157 和 CDP 临时加载独立扩展；云端使用 Linux /
Chrome for Testing 158.0.8127.18、Playwright 1.65.0 和 GTK 原生文件框持久安装。
之前成功记录使用 Playwright 1.64.1 / Chrome for Testing 156.0.8078.4；依赖未固定导致
浏览器版本变化，但尚未证明它就是安装失败的根因。提交 `01f3aef` 增加了真实安装条目、
弹窗 ID/版本和状态验证，仍未使 Linux 安装流程通过，不能宣称本地和云端流程一致。

按用户明确指令移除全部云端检查：删除共享检查工作流及引用，删除 Python/扩展回归、
MCP/桥接/浏览器、三平台安装冒烟、桌面测试/冻结包检查、网站验证，以及独立发布前
标签/来源/摘要校验步骤和独立商店状态查询工作流。云端只构建并上传；相关本地测试脚本和产品自身的输入校验、
商店重复提交保护保留。新增构建成功只表示产物生成，不补足此前失败的 Linux 验收。

## 升级与兼容性

按原安装方式升级 Python runtime，并重启 Agent 客户端加载动作协议。
复制式插件安装需要按原客户端及目录重新 setup，以更新共享 Skill；保留无关客户端配置。
后台链接动作需要匹配的 runtime 与实际加载的扩展，Python 包升级不能替代浏览器扩展更新。
核对磁盘注册、在线 host 与浏览器实际加载版本，不能仅比较包版本。
商店扩展 1.0.0 仍待审核；需要新版扩展时可等待商店更新，或由用户明确选择手动加载
GitHub 上的 1.0.0 开发包。本轮未代用户执行升级、重连或重载。

逻辑选页与此前可见标签切换不同：用户可继续停留在当前标签，Agent 的观察和输入作用于
明确绑定的另一页。会话和任务数据库不要求清空；浏览器重启导致旧 page ID 失效时仍须显式重选。
不重放未知结果的输入，不自动重载或断开用户扩展，不结束在线 native host；由用户选择升级、
重连或手动加载开发包的时机。商店送审、审核通过、实际分发和用户已加载新版必须分别确认。

## 已发布产物与状态

本轮[发布前只读商店核验](https://github.com/WilliamSkyWalker/saygo/actions/runs/42747930084)
在上传前确认正式版本为 0.4.21，状态 `PUBLISHED`、分发比例 100%，`submitted` 为 `{}`。
随后从标签 `v1.0.0` 构建并发布：标签指向提交
`b7cc0e64c97908e16432e6cf07d68898f9b14352`，annotated tag 对象为
`5a9dcdf4c38820104fb07f22f65f1f06f52c1291`。

[Python package 发布流程](https://github.com/WilliamSkyWalker/saygo/actions/runs/42805101211)
和 [GitHub / 浏览器商店发布流程](https://github.com/WilliamSkyWalker/saygo/actions/runs/42805101224)
均成功。两者仅执行构建和发布，不含已删除的云端检查，不能据此声称三平台安装或 Linux
持久安装通过。GitHub Release 于 2026-11-10 11:09:23 UTC 公开，非草稿、非预发布。

公开 [PyPI 1.0.0](https://pypi.org/project/saygo-agent-control/1.0.0/) 的 JSON 和 simple
索引均确认 wheel/sdist 存在且未撤回；下载字节与标签 CI 产物一致。
[GitHub Release](https://github.com/WilliamSkyWalker/saygo/releases/tag/v1.0.0) 的六个文件
均公开可下载且字节匹配 CI；源码及两种扩展 ZIP 内容与本地发布源码一致。
`release-manifest.json` 和 `SHA256SUMS` 也已核对，主要文件摘要如下：

| 渠道 / 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| PyPI / `saygo_agent_control-1.0.0-py3-none-any.whl` | 1130616 | `420b4a2abab5380246fa003f126a9aace7c6c04a38eea62a65cc214845b5e159` |
| PyPI / `saygo_agent_control-1.0.0.tar.gz` | 609761 | `c454a360bfdc3e1d6e2cbe6845c68ca29b51427682fa87623d50b8af45afe8fb` |
| GitHub / `saygo-1.0.0.zip` | 709726 | `725534f289418103baf589dae3374819dfae1efaddcf816a1132b6561a670ac4` |
| GitHub / `install-saygo-1.0.0.py` | 28400 | `31f5701fcd86c16db2fc85cd4eee76118549b7399f4de4990f446351f022c310` |
| GitHub / `saygo-browser-1.0.0-development.zip` | 21847 | `71a5d94791bd137e65dd85a62f8566b9676500f05263a128f17c952b11e6d0de` |
| GitHub / `saygo-browser-1.0.0-store.zip` | 21506 | `9d068ea9d2ff9ce87aa61880761a073cc8d020bd17b61a56a0d994d5ed127a44` |

实际从 PyPI 下载并核对 SHA256 的 wheel 已在 macOS 27.0 arm64 / Python 3.15.2 的
独立临时 venv 中执行 `python scripts/check_python_package.py <downloaded-wheel>`：
安装、CLI/setup 帮助、首次 prepare-only setup、插件资源/doctor、MCP 导入及重复 setup
全部通过，退出码 0。该流程没有向用户客户端注册，也没有升级用户安装。
[线上隐私说明](https://saygo.work/privacy.html) 已核对与本地文件一致，SHA256 为
`466a3fd46fae3d0527bcec1ee19fc3ba11238fd9deb8a3d657577e172b18d6d9`。

[商店作业日志](https://github.com/WilliamSkyWalker/saygo/actions/runs/42805101224/job/129792205080)
在 2026-11-10 11:09:39 UTC 返回 `Submission response: PENDING_REVIEW`，随后状态中
`submitted` 为 1.0.0 / `PENDING_REVIEW` / 100%，`published` 仍为
0.4.21 / `PUBLISHED` / 100%。这证明新版已上传并送审，不代表审核通过或用户已获得新版。

| 项目 | 当前记录 |
| --- | --- |
| 1.0.0 版本元数据、提交与标签 | 六处版本元数据统一为 1.0.0；浏览器修复提交 `0874dd1`；远端 `v1.0.0` 指向 `b7cc0e6`，完整提交与 tag 对象见上文 |
| 1.0.0 本地构建、文件白名单与 SHA256 | sdist→wheel 构建、两项严格 twine 检查通过；六处版本、四项产物摘要、源码/扩展 ZIP 文件排除规则及商店包无 key 均核对通过 |
| 云端流程与安装验收 | 两轮 Linux 持久安装检查失败；按用户指令删除所有云端检查。本地预检 wheel 干净安装、doctor、MCP 和重复 setup 通过；公开 wheel 的独立本地干净安装及重复 setup 也通过；新版 Windows/Linux 包安装未验收 |
| PyPI wheel/sdist | 已公开，未撤回；JSON/simple 索引、公开下载与标签 CI 产物字节一致性已核对 |
| GitHub 发布产物 | 已正式发布六个文件，公开下载与 CI 字节一致；ZIP 内容与发布源码一致 |
| 浏览器商店上传与提交审核 | 1.0.0 上传和提交成功，`submitted.state=PENDING_REVIEW` |
| 浏览器商店审核与分发 | 正式分发仍为 0.4.21 `PUBLISHED` / 100%；1.0.0 待审核，不能以送审作业成功代替上线 |
| 用户安装环境 | 本轮源码验证未升级当前用户安装、重载其扩展或关闭已有 host |
| 原生桌面二进制 | 不在本轮发布范围；源码/离线桌面决策检查不等于桌面安装包更新 |

本轮 macOS 完成选页与后台链接全链路实测；Linux 五项实际扩展用例（含选页）通过，
持久安装/重启失败，后台链接未单独实测。Windows/Edge 后台链接、Playwright 焦点/链接、
Android/iOS 真机和原生桌面包未新增验收；商店后续审核结果仍须另行核对，不能宣称六端全部通过。
