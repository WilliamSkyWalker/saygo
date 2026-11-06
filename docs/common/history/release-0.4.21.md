# 0.4.21 发布验证

用户于 2026-11-06 明确授权提交、推送全部本地改动，发布 Python 包和浏览器
插件，并明确两者均升级为 0.4.21。正式标签 `v0.4.21` 已推送，指向
`ce4201137d36ac09954efd8116220618884cb195`；annotated tag object 为
`ffc6d6faea973b3c298d8a38429c479f5ecb4e5a`。

截至 2026-11-06 本次记录，预检及正式发布流程均已成功，PyPI wheel/sdist 和
GitHub Release 六个附件已公开，下载摘要、原标签内容和正式构建产物比对通过。
扩展 0.4.21 已成功送审，状态为 `PENDING_REVIEW`；当前商店分发仍为 0.4.17
（`PUBLISHED`、100%）。流程重跑使用同一标签和源码，没有升版、移动标签或
修改产品代码。旧版本记录保持原样。

## 范围与版本

六处版本声明统一为 0.4.21：`pyproject.toml`、`distribution/release.json`、
`saygo/integrations/browser_bridge.py`、Claude/Codex 两份插件 manifest，
以及 `extensions/saygo-browser/manifest.json`。桥协议仍为 1，扩展仍要求
Chrome 118 或更高版本，没有因本次修改提高运行环境门槛。

Python package 流程负责 wheel/sdist；Build release 流程负责源码 ZIP、
带摘要安装器、开发/商店扩展 ZIP、发布清单及校验文件，以及扩展商店提交。
发布、上传和审核状态分别记录。本轮不触发原生桌面构建，不把旧桌面包标为 0.4.21。

| 本轮提交 | 内容 |
| --- | --- |
| `ef989ba` | 成功的动作后观察复用于操作日志 |
| `66919f1` | 普通控制和显式 Runtime 共用 60 秒阈值及边界回归 |
| `0467e02` | 选页保留标签激活、取消窗口聚焦，增加 Node 和 live 回归 |
| `b30d6a1` | 收录个人 Agent 与任务知识库设计草案 |
| `70218a9` | 六处版本声明统一为 0.4.21，准备发布文档 |
| `ce42011` | 修正发布说明中的设计草案链接，避免分发源码缺少目标文件 |

## 产品修改

| 修改 | 目的和最终行为 |
| --- | --- |
| `devices/observations.py`、`devices/actions.py`、`runtime/engine.py` | 观察最大年龄共用 60 秒阈值，普通 device 动作及显式 Runtime 一致；超过阈值仍拒绝派发，身份、图像、区域、观察消费和资源归属检查保留 |
| `devices/service.py` | 成功的 `act observe_after` 观察同时写入操作日志，避免为日志再截图；未请求观察和观察失败时仍采集证据，未知输入不重放 |
| 扩展 `select` 操作 | 保留激活目标标签页的行为，移除窗口 `focused:true` 请求；普通选页、重复选页及显式 page ID 连接均不再主动抢系统前台 |
| 浏览器启动连接 | 将此前 `main` 上的启动连接修复纳入本版，保存同配置文件的连接选择，成功连接后下次浏览器启动尝试一次；Release/Cancel 撤销后续重连，旧配置默认关闭 |
| 网络采集计数 | 清空采集时将 `pending_bodies` 归零，旧请求结束不再减少新一代采集计数 |
| 测试及操作文档 | 同步 60 秒边界、日志证据复用、选页/窗口焦点语义和真实验收边界 |
| `PERSONAL_AGENT_PLAN.md` | 收录个人通用 Agent、任务知识库、动作复用与未来云同步的审查草案；没有实现这些规划能力 |

## 浏览器扩展从 0.4.17 到本版的实际差异

扩展上一发布版本为 0.4.17，Git 标签 `v0.4.17` 指向 `d0f97be`；该标签已经
包含完整网络正文、流恢复及 Unicode 分帧。0.4.18 继续分发同一扩展版本，
0.4.19/0.4.20 的 Python 包中虽包含后续源码，但没有提交新的扩展商店版本。
因此必须同时比较扩展版本和实际代码，不能将 Python 发布等同扩展上线。

本次核对 `git diff v0.4.17 -- extensions/saygo-browser` 及相关提交记录，差异为：

- `2be5d1d`：`network.js` 清空时重置 pending 计数，并以采集 ID 隔离旧请求的
  finally 计数更新；不是再次引入 0.4.17 已有的完整正文能力。
- `3f4d774`：`background.js`、`popup.html`、`popup.js` 保存并显示启动连接偏好；
  串行化并发连接及旧 debugger 清理，释放时立即撤销在途连接，拒绝旧握手、
  迟到页面查询、网络挂接和动作恢复控制。首次/旧配置需手动连接，偏好保存失败
  明确报告，host 失败保留选择但不立即重试，旧 page ID 仍需显式重选。
- 本轮焦点修复：`background.js` 的 `select` 不再调用
  `chrome.windows.update(..., {focused:true})`，保留标签激活。
- 本轮版本变更：manifest 从 0.4.17 升至 0.4.21；既有权限、开发扩展身份和
  最低 Chrome 版本保持不变。

## 本地源码与构建检查

以下为 Linux 本地验证；跳过项单独列出，不计为通过。

| 检查 | 结果与证据范围 |
| --- | --- |
| `python3 scripts/check_core_tests.py` | 共 1,060 项：1,042 通过、18 跳过；离线驱动、真实 SQLite、安装和协议契约等，不代表所有设备真实操作 |
| `node --test --test-isolation=none --test-reporter=tap tests/extension_demo/test_*.mjs` | 77 项通过；真实扩展脚本配合 Chrome API 模拟，包括启动、释放、截图、网络、滚动和选页 |
| 观察年龄回归 | 先验证旧实现拒绝 45/60 秒，改后 45 秒及恰好 60 秒可执行；60.001 秒拒绝且未派发，45 秒但画面变化也拒绝 |
| 动作后证据回归 | 返回观察与 journal 使用同一 ID/图片；不复用操作前图片；未启用 observe_after 和截图异常路径保留各自证据行为 |
| 选页前台回归 | 旧代码在模拟普通、最大化、最小化窗口条件下触发窗口聚焦；修改后四项定向回归通过，并入上述 77 项 |
| Claude 插件校验 | `claude plugin validate .` 和 `claude plugin validate plugins/saygo-device` 均通过，退出码 0；使用隔离配置目录 |
| 版本、语法与空白 | TOML/JSON/AST 核对六处 0.4.21 一致；新 live 测试 `py_compile` 及改动 `git diff --check` 通过 |

本地构建检查覆盖源码包的 187 个白名单条目，以及插件 LICENSE、doctor.py、
saygo_mcp.py、60 秒、观察复用、选页焦点、启动连接和网络计数修复。敏感配置、
账户、会话、截图、日志、数据库、私有测试和缓存未混入产物。开发/商店扩展各
10 个文件，版本均为 0.4.21。

## GitHub 公开产物核验

六个正式附件均已匿名下载得到 HTTP 200，实际 SHA256 与 GitHub API digest
一致；`SHA256SUMS` 的四个产物摘要、release manifest 和安装器固定的源码摘要
也全部对应公开文件。

源码 ZIP 的 187 个文件逐一与 `ce42011` 原始 Git blob 字节比对一致。开发扩展
10 个文件与原标签一致；商店包仅按构建规则移除 manifest 开发公钥并重新序列化，
其余内容一致，两个扩展版本均为 0.4.21。核心修复和白名单检查均通过。

| 公开附件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `saygo-0.4.21.zip` | 682344 | `67cd13e1a072d979f1cfcbe5c81d405a5e194829460ae7daecd4f44f24ec9ed0` |
| `install-saygo-0.4.21.py` | 28403 | `f08b82c40040707884f1e7f16f11e97280b054d512b35d057c4d46f4a89290bb` |
| `saygo-browser-0.4.21-development.zip` | 20773 | `fa0de14105487667df8ec228ce306d0d10f33ede5c3cd5de22a3994211f70278` |
| `saygo-browser-0.4.21-store.zip` | 20431 | `d13702a04988ef35881c1e178ae116c6fbb21e5e06bcbb06bac695548e7b6d08` |
| `release-manifest.json` | 587 | `e532bee21031daeb123b9fa593555d3dec91cd6b142d9381cc4c38d1d6bf0b7e` |
| `SHA256SUMS` | 373 | `85fab3145bbe62b427ad6c7c4a2eef15ac8fd078ac7f57055280b3ec1f1331aa` |

此前把本地归档称为“原始 LF 规范构建”不准确，其中仍有 CRLF 文件。本地与
公开归档无文件增删，内容差异仅为换行；安装器和 manifest 随源码摘要变化。
本表以公开下载及原标签 Git blob 为准，不使用本地归档摘要替代公开证据。

## 发布预检 CI

[预检 42155682870](https://github.com/WilliamSkyWalker/saygo/actions/runs/42155682870)
全部成功，publish 按预检设计跳过。运行提交 `70218a9` 到正式标签 `ce42011`
只有发布说明中的一个链接变更，产品源码一致。

| 检查 | 环境和实际结果 |
| --- | --- |
| 核心 | Ubuntu 26.04.1 LTS x64、Python 3.11.18、Qt offscreen；`python scripts/check_core_tests.py`：1,060 项，1,051 通过、9 跳过 |
| Node | Node 22.23.4；`node --test tests/extension_demo/test_*.mjs`：77 通过、0 失败、0 跳过 |
| MCP | MCP 1.2.0 / Pydantic 2.13.5，以及 MCP 2.3.0 / Pydantic 2.14.3；device/full 的 stdio 握手、工具集合、输入 schema、请求查询均通过 |
| Windows bridge | Windows Server 2025 x64、Python 3.12.10；`test_bridge.py` 17 通过，`test_shared_bridge.py` 14 通过，0 跳过；包含真实 native-host 子进程和模拟扩展对端，不是 Windows GUI 验收 |
| 真实浏览器 | Ubuntu 26.04.1 LTS x64、Python 3.11.18、Chrome for Testing 156.0.8078.4、Xvfb 1600×1000×24、Openbox；7 通过、0 跳过 |

浏览器命令为
`xvfb-run -a -s "-screen 0 1600x1000x24" python scripts/check_browser_tests.py`：
`test_live.py` 5 通过（211.314 秒），`test_startup_live.py` 1 通过（37.652 秒），
`test_playwright_live.py` 1 通过（13.369 秒）；共 6 项扩展/native-host 和 1 项
Playwright 真实浏览器测试。

新增 `test_cli_page_selection_preserves_foreground_window` 已在该 Linux CI 实际
通过。它使用独立 profile、真实扩展、native host 和 CLI，覆盖选择非活动页、
重复选择同一页、connect 显式页；验证标签仍激活、另一窗口保持焦点，并核对
X11 实际活动窗口和堆叠顺序。本地缺少浏览器及窗口管理器而跳过的结果仍单独
保留。核心检查跳过的 7 项浏览器用例在此单独执行，另 2 项 Windows live
桌面用例未执行。真实 Windows/macOS 窗口焦点本轮未验收，模拟最小化窗口的
结果也不代表最小化浏览器截图受支持。

预检构建出的 wheel 通过三平台干净安装与重复 setup：

| 平台 | Python / job | 结果 |
| --- | --- | --- |
| Windows Server 2025 Datacenter 10.0.26100 x64 | 3.11.9 / `127690993528` | 干净安装、setup、打包资源、plugin doctor、MCP import、重复 setup 全部通过 |
| macOS 26.7.2 (25G332) arm64 | 3.11.9 / `127690993580` | 同上，全部通过 |
| Ubuntu 26.04.1 LTS x64 | 3.11.18 / `127690993593` | 同上，全部通过 |

三平台均调用 `scripts.check_python_package.check` 检查生成的 wheel。这些结果
不代表真实手机控制、用户安装环境升级或公开 PyPI 文件验收；两套 MCP 组合也
不代表每个中间 SDK 版本均已测试。

## 正式发布尝试与状态

[GitHub/Chrome Web Store 流程 42156455355](https://github.com/WilliamSkyWalker/saygo/actions/runs/42156455355)
首次 attempt 的 core、Windows bridge 和两项 MCP 检查成功，browser 得到
4 通过、1 error、0 跳过（176.809 秒）。错误发生于
`test_background_tab_input_after_manual_tab_switch` 的共有 `run_live` 准备截图
（`tests/extension_demo/test_live.py:204`），在网络检查和初始输入之后、后台输入
专属回调之前，CDP 返回 `-32000: Unable to capture screenshot`。
新选页焦点用例通过，其余 startup/Playwright 套件因前组失败未执行。
该次 package/store 被跳过，没有上传扩展或提交审核。当前证据只定位到截图
错误，根因未确定，不能归因于焦点修改或 CI 抖动。

读取失败日志后，在同一标签重跑失败 job 一次。attempt 2 全部成功，正式
browser job `127693531438` 的 7 项真实浏览器测试全部通过；package job
`127695194309` 在 [GitHub Release](https://github.com/WilliamSkyWalker/saygo/releases/tag/v0.4.21)
于 2026-11-06 03:36:42 UTC 公开六个附件。公开文件审计已通过，见上表；
重跑成功不抹去首次失败记录。

商店 job `127695359423` 于 2026-11-06 03:37:03 UTC 成功送审。API 确认
submitted 0.4.21 为 `PENDING_REVIEW`，published 0.4.17 为 `PUBLISHED`、
分发比例 100%；`warned` 和 `taken_down` 均为 false。随后于 03:46:19 UTC
执行[最终只读商店状态核对](https://github.com/WilliamSkyWalker/saygo/actions/runs/42158526590/job/127698347063)，
再次确认 published 0.4.17 为 `PUBLISHED` / 100%，submitted 0.4.21 为
`PENDING_REVIEW` / 100%，两项标记仍为 false。submitted 的 100% 是部署设置，
不表示已分发。0.4.21 尚未审核通过或成为当前分发版本，不能把流程成功或送审
成功写作商店已上线；此次只读检查没有重复提交审核。

[Python 流程 42156455273](https://github.com/WilliamSkyWalker/saygo/actions/runs/42156455273)
首次 attempt 的 browser job 因 Ubuntu 依赖下载耗时，在 10 分钟作业限制触发后
取消。日志显示停在安装 Xvfb/Openbox 等依赖阶段，尚未启动产品测试，不能将其
记作产品测试失败。读取日志后仅重跑该失败 job，attempt 2 总体成功：browser
job `127695378996`、build job `127697158615`、三平台安装 smoke 和 publish
job `127697731569` 全部通过，publish 于 03:44:44 UTC 成功完成。正式浏览器
`test_live.py` 5 通过（217.131 秒）、`test_startup_live.py` 1 通过（38.963 秒）、
`test_playwright_live.py` 1 通过（15.499 秒），共 7 通过、0 跳过。
两个流程均保持 `v0.4.21` 和 `ce42011` 不变，没有修改 CI 或产品来绕过检查。

正式 Python 构建产物再次完成三平台安装验收，与上面的预检分别记录：

| 平台 | Python / 正式 smoke job | 结果 |
| --- | --- | --- |
| macOS 26.6.2 (25G83) arm64 | 3.11.9 / `127697331596` | 干净 wheel 安装、setup、打包资源、plugin doctor、MCP import、重复 setup 全部通过 |
| Ubuntu 26.04.1 LTS x64 | 3.11.18 / `127697331606` | 同上，全部通过 |
| Windows Server 2025 Datacenter 10.0.26100 x64 | 3.11.9 / `127697331610` | 同上，全部通过 |

2026-11-06 已核对 [PyPI 0.4.21](https://pypi.org/project/saygo-agent-control/0.4.21/)
的版本 JSON 和 [simple 索引](https://pypi.org/simple/saygo-agent-control/)：
wheel/sdist 均可见、未 yank，实际下载 SHA256 与官方摘要相同，且两个公开文件
均与上述正式 CI artifacts 逐字节一致。wheel 内嵌的 187 个 setup 源码文件、
111 个 runtime 文件，以及 sdist 的 187 个源码文件，均与 `v0.4.21` 原始
Git blob 逐字节一致。

| PyPI 公开文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `saygo_agent_control-0.4.21-py3-none-any.whl` | 1092526 | `bf91dde2fb7d77944b08c61c6d48be138d46343df4e18add6e12ee023e59f52d` |
| `saygo_agent_control-0.4.21.tar.gz` | 586591 | `eea6ec7984c0280588f98f5f145802d7b6cdab3e56293db0e0c217b2b4b4cbb5` |

这里将正式 CI 的三平台安装证据与公开文件字节一致性相连；未把文件内容检查
写成又执行了一轮公开下载包安装，也没有升级用户当前运行环境。

| 项目 | 当前状态 |
| --- | --- |
| 源码与标签 | `v0.4.21` 已推送并绑定 `ce42011`；正式产物保持该不可变源码 |
| GitHub Release | 六附件匿名下载、API digest、SHA256SUMS、manifest/安装器源码摘要及原标签内容审计全部通过 |
| PyPI wheel/sdist | 正式 attempt 2 成功；版本 JSON/simple 索引可见，均未 yank；公开下载哈希、正式 CI 产物和原标签内容比对通过 |
| 三平台干净安装与重复 setup | 预检及正式 Python 流程的 Windows/macOS/Linux 均全部通过；公开文件与正式受测产物逐字节相同 |
| 真实浏览器回归 | 预检 Linux 7 项全部通过；正式 GitHub/扩展首轮截图失败，同标签重跑检查通过 |
| Chrome 商店 | 03:37:03 UTC 成功送审 0.4.21，`PENDING_REVIEW`；当前分发仍为 0.4.17，`PUBLISHED` / 100%，不是 0.4.21 已上线 |
| 原生桌面包 | 不在本轮构建范围，没有 0.4.21 桌面二进制 |
| 用户安装环境 | 未自动升级安装、重载用户扩展或关闭在线 host；磁盘版本、活动进程与浏览器实际加载版本仍须分别核验 |

此前版本的 Android、iOS、桌面冻结启动等验收仍见各历史记录，不能计作本版
重测。本次发布证据补录不移动标签或覆盖不可变产物。扩展仍待商店审核，
用户当前安装和真实 Windows/macOS 窗口焦点仍不在已验证范围内。

此前曾在现有 Python 安装应用 60 秒观察阈值相关的局部热修复；这不等于完成
0.4.21 整包升级，也不能证明所有正在运行的 Agent/MCP 进程已加载新代码。

## 升级与兼容性

Python 包升级后需要重启使用它的 Agent 客户端以加载新阈值和日志行为；托管
插件副本需要更新时，按原客户端和安装参数重复 setup。既有任务数据库、页面
绑定及操作记录不需要迁移或清空，失效页面仍需显式重选，未知输入不得自动重放。

焦点、启动连接及网络计数变更需要浏览器实际加载新版扩展。商店审核/分发与
Python 包安装分开进行；不主动重载现有扩展、关闭在线 native host 或借用业务
会话验收。已运行 host/客户端何时加载新版须另行核验，不仅比较磁盘版本号。
