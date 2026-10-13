# 0.4.19 发布验证

用户于 2026-10-14 在 Android 人工接管修复与独立输入验收后，明确授权提交、
推送、升级版本并发布 PyPI。该授权不代表用户安装环境已经升级，也不把包发布、
桌面构建和扩展商店审核混为同一结果。

本文先记录已完成的源码验证，发布与安装结果在实际执行后补充。版本元数据已
更新为 0.4.19，更新后核心回归、本地构建及 Linux 干净安装通过；标签、最终
推送、CI 三平台验证及公共索引验证仍待执行，不能声称已发布。本轮仅发布 PyPI，不创建 GitHub 公开 Release、不构建
新桌面包、不向扩展商店上传。

## 相对 0.4.18 的完整变更范围

对照基线为 0.4.18 标签提交 `ff9d622`。此前已合入 `main` 的六个提交均纳入核查：

| 提交 | 本版涉及内容 |
| --- | --- |
| `2be5d1d` | 修复网络采集清空后的 `pending_bodies` 计数及迟到请求污染；补充大规模分页、缓存/流回退测试、网络保留和隐私文档 |
| `4ef5c2a` | 补齐 0.4.18 实际发布、安装、浏览器及商店证据，明确上述计数修复当时仍不在 0.4.18 附件中 |
| `fdb3e45` | QA 统一目标归属与路径解析，避免绝对 Markdown 目录重复扫描；补充路径、feature 优先级和上下文回归及 QA 文档 |
| `b9f6f45` | 稳定帧/多帧采样复用图像，视觉差异直方图统计、零变化快捷返回及 deque 区域遍历；补充十项图像回归并纳入核心检查 |
| `fc8bae6` | Runtime 事件查询不再读取解析完整快照，ZIP 导出复用同一次事件历史；补充真实 SQLite 查询/排序/导出回归 |
| `183e4a7` | 提供隔离数据性能基准，记录基线/重构后耗时与局限，更新架构、采样实现和离线验证文档 |

本轮新增 Android/iOS 人工接管修改：

- `platforms/android_ime.py` 经 Appium 会话 IME 接口读取、保存、恢复和核验普通
  键盘，拒绝把自动化 IME 当用户选择；缺失或已卸载的原选择明确报错。
- `platforms/appium.py` 删除永久 UnicodeIME 能力设置；自动输入前后核验普通
  键盘，派发后恢复失败标记结果未知且不重发。iOS 新连接默认保留模拟器键盘偏好。
- `platforms/device_session.py` 持久保存输入法与连接参数，保持接管状态和所有权；
  仅明确失效的 Appium 会话允许在显式重连中重建，后续准备失败也保留已创建绑定。
- `devices/control.py`、`devices/service.py`、`runtime/interactive.py`、
  `runtime/engine.py` 与 `runtime/resources.py` 共享接管准备、失败暂停、新观察和
  资源归属逻辑，覆盖普通 device、MCP、交互 task 和显式 workflow。
- control/mobile/runtime 测试增加连接、重复接管、旧状态、用户改选键盘、恢复
  失败、会话过期与错误回执等回归；提供无权限/无网络自有 Android 输入夹具。
- 更新 AGENTS、Android 指南、统一操作和[输入验收记录](../../android/handoff-validation.md)。

## 已完成的本轮源码验证

| 项目 | 已执行结果与边界 |
| --- | --- |
| 核心离线检查 | 更新 0.4.19 元数据后，WSL/Linux 重跑 `python3 scripts/check_core_tests.py`：1,050 总数，1,034 通过、16 跳过、0 失败；分组明细见输入验收记录 |
| Android 驱动审计 | 正式安装版 0.4.18 对应现场为 Appium 3.8.0、UiAutomator2 8.7.0、Android driver 14.2.0、ADB library 16.0.5、Settings 8.0.9；日志证实 `resetKeyboard` 未识别，默认 UnicodeIME 持续占用 |
| 独立 Android 普通 device | 使用独立 API 35 模拟器和自有输入页，经源码共用连接 API 建立会话，CLI 完成自动中英文输入、handoff、用户确认软键盘/电脑键盘输入、resume 新截图及再次自动输入 |
| 普通 device 旧残留/重复/重连 | 在测试机经 Appium 标准 IME 接口模拟 UnicodeIME 残留，两次 handoff 恢复已保存普通键盘；暂停态 connect 原绑定后 resume，保持同一 Appium 会话、页面和文字 |
| 真实 MCP Runtime | CLI 创建/观察任务，真实 MCP stdio `agent_task` 提交中英文、handoff，用户再次确认两种键盘输入；resume 返回新图且实际查看，再自动输入并截图确认；重复接管和暂停态重连均保持原会话与内容 |
| 资源与观察保护 | 接管期间实际查询 SQLite 确认资源仍属于原任务；过期观察在输入前拒绝，随后使用新观察和新 request ID，无未知结果重放 |
| 输入夹具 | 已有 Windows SDK 35/build-tools 35.0.0/JDK 离线构建；ZIP CRC 与 APK v1/v2/v3 签名验证通过，产物不入公开仓库 |
| iOS | 能力参数、聚焦元素输入和共享接管逻辑通过离线契约；无本次真实 iPhone/iPad 或 Simulator 验收 |

这些 Android 结果来自仓库源码连接真实 Appium 和模拟器，未改正式安装环境的
site-packages；用户实际输入确认与 Agent 自动注入分开记录，业务登录页未用于测试。

## 先前提交的验证证据

以下为 2026-10-13 的历史结果，本次未重跑的项目不计作 0.4.19 产物通过：

- 网络计数修复：51 项 Node、33 项 Python 桥接/网络测试及一项真实独立 Chrome
  大正文链路通过；真实链路覆盖缓存淘汰后的 33 MiB 响应和完整 Unicode POST。
- QA/视觉/Runtime 重构：17 项新增回归，核心离线 969 通过、16 跳过；同环境
  合成基准中静态三帧采样约 156→70 ms、零变化视觉差异约 583→16 ms、事件
  读取约 9.7→4.3 ms。详细负载与完整数字见[性能记录](../performance.md)。

局部性能数据不衡量设备截图、模型时延、完整任务耗时或业务通过率。
旧 0.4.18 的三平台安装、桌面构建和商店审核结果也不能充当本版验收。

## 发布检查中的测试修正

首次标签流程 [38434890955](https://github.com/WilliamSkyWalker/saygo/actions/runs/38434890955)
在真实 Playwright 检查中失败，因此 build、smoke 和 publish 均未执行。
四项真实扩展测试通过，但旧 Playwright 用例在 workflow 暂停后仍通过
`device_session.attach_browser` 改变选页，被新增的持久接管保护正确拒绝；
本地独立 Chromium 也复现了同一错误。

修正只涉及验证：用例先断言自动连接被拒绝，再经独立原生 Playwright/CDP
模拟外部页面变化，检查原绑定、暂停状态及 resume 的新观察。它是自动化模拟，
不计作用户人工输入验收。人工输入证据仍来自前述独立 Android 测试中的两次
用户确认。

手动重验既有标签时，浏览器 job 仅从调用方固定 SHA 取修正的
`tests/browser_demo/test_playwright_live.py`；产品源码与独立构建 job 仍使用
不可变 `v0.4.19`。没有移动标签、追加产品版本或跳过回归/安装门禁。

## 0.4.19 发布与安装状态

| 项目 | 当前状态 |
| --- | --- |
| 源码提交、推送、标签 | 输入修复提交 `f1cb82f` 已完成并核对正文；版本提交、推送及标签待执行 |
| wheel / sdist / 发布白名单与校验 | 本地 `python -m build` 从 sdist 构建 wheel、`twine check --strict` 均通过；已核验修复源码完整且无会话/截图/私有测试；CI 最终产物待核实 |
| 干净环境安装与重复 setup | 本地 Linux `scripts/check_python_package.py` 通过：独立环境 wheel 安装、CLI/setup、内嵌资源/MCP 导入及重复 prepare-only setup；CI Linux/Windows/macOS 待执行 |
| PyPI | 待发布；wheel/sdist、未撤回状态、下载哈希与 simple 索引均需实际核实 |
| GitHub 产物 | 本轮不创建公开 Release；发布标签与 Python 流程产物不等于 GitHub Release 附件 |
| 桌面包 | 本轮不构建或发布；0.4.18 桌面包不会自动包含本轮源码修复 |
| 浏览器扩展与商店 | 包内源码含网络计数修复，manifest 仍为 0.4.17；本轮不上传商店，不将旧商店审核结果计为修复已上线，也不主动重载在线扩展 |
| 用户安装环境 | 仍为正式安装版 0.4.18，未修改 site-packages、未直接升级；源码验收不代表安装版已修复 |

## 迁移与剩余限制

QA 发现优先级、截图/采样语义、CLI/MCP 参数、Runtime 数据库与导出格式保持兼容。
输入法记录为可选新增状态；旧会话不会凭空产生历史键盘选择。若当前只剩 UnicodeIME
且没有记录，用户须在系统输入法设置中选择普通键盘后重试；远程 Appium 禁用
IME 接口会明确报错，不要求开放不安全 shell。

暂停态显式 connect 必须使用原设备/服务器/别名；仅 `InvalidSessionId` 允许新建，
网络异常不换会话。重连不结束接管，也不释放设备/任务资源；resume 成功后重新
观察，旧观察失效。准备失败保留当前绑定并报告错误，不重启应用或清空数据。

iOS 新连接默认将 `connectHardwareKeyboard` 与
`forceSimulatorSoftwareKeyboardPresence` 均设为 false，保留 Simulator 当前设置；
显式 `appium.caps` 仍可覆盖。旧设置已经改变且没有原值时需用户在 Simulator
键盘菜单恢复。不能从离线测试推导 iOS 两种键盘和自动输入已通过实机验收。

真实过期会话重建、多普通键盘切换、故障注入、显式 workflow human 步仍只有
离线覆盖。未进行六端完整业务、真实模型任务、桌面签名/公证或各云设备提供方
兼容性验收。发布不会自动重载在线浏览器扩展或关闭 host；包内扩展代码与
浏览器实际加载代码、商店审核状态必须分开确认。
