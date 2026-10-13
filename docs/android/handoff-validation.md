# Android 人工接管输入验证

[Android 操作](README.md) · [统一操作](../common/operations.md) · [自有输入夹具](../../tests/mobile_demo/ime_fixture/README.md)

## 已确认的诊断

2026-10-14 检查正式安装版 Saygo 0.4.18 的 Android 虚拟机现场。
只读查询确认系统默认输入法为 `io.appium.settings/.UnicodeIME`，
`show_ime_with_hard_keyboard` 为 `1`；普通键盘仍在可用列表内。
业务页面未用于输入测试，未记录账户或页面数据。

实际运行组件版本：

| 组件 | 版本 |
| --- | --- |
| Appium | 3.8.0 |
| appium-uiautomator2-driver | 8.7.0 |
| appium-android-driver | 14.2.0 |
| appium-adb | 16.0.5 |
| io.appium.settings | 8.0.9 |

现场驱动日志明确报告 `resetKeyboard` 不被识别；`unicodeKeyboard` 已废弃，
仍会将默认输入法切为 UnicodeIME。日志中的首次切换前为普通键盘，后续重连时
原输入法已是 UnicodeIME。旧 Saygo handoff 只保存暂停状态，没有恢复键盘。
这些证据确认了自动化输入法持续占用的原因。修复后的人工输入已在独立测试模拟器
验收，具体路径与未覆盖范围见下文；原业务模拟器没有用于输入验收。

实际安装源码的关键调用关系：

- Android driver 的 `initDevice` 调用 `initUnicodeKeyboard`，丢弃返回的原输入法。
- UiAutomator2 仅在 `hideKeyboard=true` 时保存 `_originalIme`。虽然删除会话代码
  包含恢复分支，本现场不满足该条件，不能依靠断开恢复。
- `mobile: type` 调用 `settingsApp.typeUnicode`，后者调用
  `adb.runInImeContext`，在 `finally` 中恢复动作开始前的输入法。
- `hideKeyboard=false` 会执行 `ime reset`，同样不适合保留用户原选择。
- Appium 会话仍提供 `ime/active_engine`、`ime/available_engines` 和
  `ime/activate` 接口；无需开放 `mobile: shell` 或直接用 adb 输入。

[旧版 Appium Unicode 文档](https://appium.github.io/appium.io/docs/en/writing-running-appium/other/unicode/)
描述的 `resetKeyboard` 行为不适用于上述实际驱动版本。以后升级驱动须重新核查，
不能只依据旧文档或 Saygo 包版本推断恢复行为。

## 源码行为

连接保存普通输入法，不默认永久启用 UnicodeIME。接管先暂停自动操作，再恢复和
核验已保存的选择；恢复控制前再次核验输入法并观察当前页面。输入法管理不改变
当前应用、不结束会话、不释放任务资源。用户在接管期间主动更换的普通键盘成为
下一次保存的选择，自动中英文输入仍通过 `mobile: type`。

旧会话缺少记录、记录的键盘已卸载、当前已是自动化输入法，或者多个候选无法
确定用户选择时，明确报告候选及处理方法。用户在系统设置中选择键盘后重试。
语音输入服务也可能出现在列表中，不能自动选择首项。远端接口不可用、切换核验
失败、保存失败和恢复后的截图失败都必须明确报错并保持暂停。

接管期间过期的 Appium 会话，可显式 `device connect` 原有绑定。只有明确的
`InvalidSessionId` 才允许新建 Appium 会话，网络失败不会触发新建；暂停状态、
用户输入法记录和设备/任务资源归属继续保留。创建成功但后续准备失败时保留
已创建的会话绑定，便于显式恢复。重连成功不等于恢复自动控制，仍需 resume。

## 独立验收步骤

使用独立 Android 模拟器/设备、命名会话和临时状态目录；不得借用业务会话或
登录页面。自有夹具包为 `com.example.saygo.imefixture`，没有网络、权限或账号。
已有 SDK/JDK 可离线构建，构建脚本不安装依赖；APK 与临时签名保存在仓库外。

1. 记录环境、真实 Appium/驱动版本和原输入法。打开夹具，通过 CLI 或 MCP
   连接测试会话，核验连接后仍使用原键盘。
2. 观察并点击自动输入框，输入无业务含义的中文与英文样例；读取返回截图，
   核验内容和动作后的默认输入法。
3. 执行 handoff，确认暂停状态、设备/任务资源归属与键盘恢复结果。让用户实际
   点击人工输入框，用软键盘和电脑键盘分别输入样例，明确等待用户确认。
   Agent 注入文本、发送按键或直接设置输入框都不能替代这一步。
4. 用户交还控制后执行 resume，确认返回当前页面的新观察，再自动输入中英文，
   核验内容及输入法。恢复说明本身不是输入成功证据。
5. 重复接管；在人工阶段选择另一已安装普通键盘，验证后续保存该选择。
   重连时验证设备绑定、键盘选择和输入内容保留，不重启或清空应用。
6. 分别通过普通 device 与 Runtime task 执行上述链路；显式 workflow 的 human
   步还须执行声明的业务验证。保存错误路径和未验证项，不能以 mock 通过代替。

## 本次验证状态

| 项目 | 状态与边界 |
| --- | --- |
| 现场默认输入法、驱动支持核查 | 已确认上述状态和实际安装源码；未操作业务输入框 |
| 自有 APK 离线构建 | 已使用现有 SDK 35/build-tools 35.0.0 构建；ZIP CRC、APK v1/v2/v3 签名通过 |
| 独立 Android 验收环境 | 已使用现有 API 35 Google APIs 镜像新建临时 AVD 并安装夹具，未复制业务 userdata；已启用其硬件键盘并将软键盘共存设置从 0 改为 1，原业务模拟器未变 |
| 离线回归 | `python3 scripts/check_core_tests.py`：共 1,050 项，1,034 通过、16 跳过、0 失败；分组见下表 |
| 普通 device 的 Android 接管链路 | 源码共用连接 API 建立会话，CLI 打开夹具、点击和自动中英文输入后 handoff；用户确认人工输入成功，resume 返回新截图并核验人工内容；恢复后的自动中英文输入也已截图确认 |
| 人工软键盘与电脑键盘输入 | 用户分别在普通 device 和 Runtime task 接管阶段明确确认两种键盘均能输入；未将 Agent 注入文字计为人工验收 |
| 普通 device 重复接管与重连 | 在自有测试机经标准 Appium IME 接口设置 UnicodeIME，模拟旧会话残留；两次 handoff 均恢复保存的普通键盘。暂停期间 CLI connect 原绑定，再 resume 取得新图；Appium 会话、页面及文字保持不变 |
| Runtime task 的 Android 接管链路 | CLI 创建并观察任务；真实 MCP stdio `agent_task` 提交中英文并 handoff，用户第二次确认软/电脑键盘正常；MCP resume 返回一张实际查看的新图，再次提交自动中英文并检查截图通过；普通键盘选择保留 |
| Runtime task 重复接管与重连 | 两次 MCP handoff、暂停态 CLI connect 原绑定、MCP resume 均完成；实际读取 SQLite 确认资源继续归属原任务，恢复后的新截图已查看，Appium 会话和原页面内容保持不变 |
| 资源归属及观察保护 | 接管期间实际读取 SQLite 核验锁仍属于原任务；两次过期观察在派发前被拒绝，重新观察后以新 request ID 提交，没有重放结果不明的动作 |
| 未执行的 Android 真实路径 | 过期 Appium 会话重建、多种普通键盘切换、故障注入和显式 workflow human 步；这些路径仅有离线覆盖 |
| iOS 真机/模拟器接管输入 | 未执行，当前环境无 XCUITest/iOS 验收设备 |
| 正式安装版及源码状态 | 验证对象为工作区源码；用户原安装在验收期间仍为 0.4.18，未含本修复。后续发布状态见 [0.4.19 记录](../common/history/release-0.4.19.md) |

离线检查在 WSL/Linux 执行，使用模拟平台、隔离状态目录和真实本地存储。
其中包含 iOS 参数/共享接管契约检查；不构成任何 iOS 真机通过。
跳过项不计为通过：

| 分组 | 总数 | 通过 | 跳过 |
| --- | ---: | ---: | ---: |
| control | 808 | 806 | 2 |
| runtime | 41 | 41 | 0 |
| desktop | 45 | 36 | 9 |
| cli | 23 | 23 | 0 |
| mobile | 73 | 73 | 0 |
| browser | 15 | 14 | 1 |
| extension | 35 | 31 | 4 |
| vision | 10 | 10 | 0 |
| 合计 | 1,050 | 1,034 | 16 |

iOS 的 Saygo 输入路径为聚焦元素 `send_keys`，没有 Android UnicodeIME。
XCUITest 模拟器另有软/硬键盘偏好：官方文档说明默认
`forceSimulatorSoftwareKeyboardPresence=true` 会关闭硬件键盘；与
`connectHardwareKeyboard` 均为 false 时保留模拟器现有偏好。本修复在新建 iOS
会话时显式设置这两项为 false，避免驱动默认值覆盖用户原来的键盘选择；
显式 `appium.caps` 仍可覆盖默认设置。旧会话若已经被驱动修改偏好，Saygo 没有
历史值可供还原，需要用户在 Simulator 的键盘菜单中重新选择。iOS handoff/resume
不会发送 Android IME 指令，输入仍由聚焦元素 `send_keys` 执行。
目前仅验证能力参数及共享接管流程的离线契约，未执行真实 iOS 设备或模拟器验收，
不能声称 iOS 人工软键盘、电脑键盘或恢复后的自动输入已经通过。
参见 [XCUITest 键盘能力说明](https://appium.github.io/appium-xcuitest-driver/10.43/reference/capabilities/)。
