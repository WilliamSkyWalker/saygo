# Chrome/Edge 扩展操作

[文档入口](../README.md) · [本端完整需求](requirements.md) · [统一操作](../common/operations.md) · [商店材料](store.md) · [隐私说明](privacy.md)

## 需求与架构

适用 BROWSER-001～011、BRIDGE、UPDATE-019 和公共会话/观察/任务规则，见[需求基线](../common/requirements.md#browser)。此后端控制当前 Chrome/Edge 配置文件中的 HTTP(S) 标签页，保留登录状态；无需远程调试端口或 Playwright，不向视觉模型提取 DOM 或 cookie。网络记录可能包含 cookie 等敏感信息，见下文。

```text
CLI / MCP / 桌面应用 / Runtime
             ↕ 私有共享目录中的 JSON 请求
Native Messaging host（运行在浏览器所在系统）
             ↕ 浏览器原生消息 / stdio
Saygo Browser 扩展 → 当前配置文件内的网站标签页
```

WSL 经 Windows 路径的 `/mnt/...` 映射访问同一目录，不监听网络端口。桥用于可信的单一本机用户，不适用于网络共享或多用户远程控制。有写权限者可发命令，有读权限者可读取传输中的截图/输入；使用私有目录和限制性 ACL，不放仓库或云同步目录。正常请求会清理，进程中断可能遗留敏感文件。

## 安装与共享桥

在 Chrome 或 Edge 安装 [Saygo Browser](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo)，商店 ID 为 `ehomcchjfomfkcmbeinlcmpbaamdhfbo`，无需开发者模式。在 Agent 所在环境执行（包括 WSL）：

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --client codex --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo
```

可选择 claude、both、qoder、qodercn 等客户端，Edge 增加 `--browser edge`。安装器在浏览器所在 OS 注册 native host，WSL 会准备 Windows host。

Windows 桌面版、Windows Python 与 WSL 共用同一浏览器桥。新安装默认 `%LOCALAPPDATA%/Saygo/browser-bridge`；发现已有在线桥时保留其目录，包括旧 `%USERPROFILE%/.saygo/browser-bridge`。安装和默认连接检查注册及历史目录，更新原位置启动器，不断开在线 host。发现多个在线桥或 host 无响应时明确报错，不改连另一浏览器。

保存的会话保留桥目录与页面绑定。历史分裂安装应显式建立新的命名会话，并选择正确的在线页面，不能重定向过期绑定。只读检查实际目录：

```sh
python -m saygo.integrations.browser_setup --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo --resolve-only
```

打开普通网页，在扩展弹窗点击 **Connect local bridge（连接本地桥）**，再重启 Agent 客户端。连接后所有现有及新增网站标签页都可发现，不需逐页分享。Chrome 可能显示正常的调试控制提示条。

## 升级与开发版本

```sh
pipx upgrade saygo-agent-control
# 仅迁移历史开发扩展 ID 或修复注册时需要显式 setup。
saygo setup --client codex --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo
```

日常包升级后重启 Agent 即可，在线 host 继续运行旧代码直到用户重连。开发版切换商店版时，由用户在旧扩展弹窗释放连接并禁用/删除旧副本，再连接商店扩展；Saygo 不主动断开或重载。包升级不会自动覆盖历史开发 ID，需显式指定。商店更新须经过 Google 审核及浏览器分发。

仅开发或明确测试未上架版本时加载 `extensions/saygo-browser`：进入 `chrome://extensions` / `edge://extensions`，开启开发者模式并“加载已解压的扩展程序”，保留整个目录。开发 ID 为 `oifpojkdkggpmdfbbochlclhjahkkmpc`，setup 必须指定该 ID。

手动注册要求 Python 3.11+，在浏览器所在 OS 执行并使用长期保留的 host 文件：

```sh
python3 -m saygo.integrations.browser_bridge install --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo --directory "$HOME/.saygo/browser-bridge"
```

```powershell
py -3 C:\Saygo\browser_bridge.py install --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo --directory "$env:LOCALAPPDATA\Saygo\browser-bridge"
```

Edge 增加 `--browser edge`。Windows 使用 HKCU 用户注册，不需管理员；Linux/macOS 默认注册普通 Chrome/Edge 配置目录，自定义 `--user-data-dir` 需将 `com.saygo.browser.json` 放入其 `NativeMessagingHosts/`。浏览器管理策略仍可能禁止 native messaging。

## 连接并选择目标

```sh
saygo device connect --platform browser --backend extension --session browser-test
saygo device pages --session browser-test
saygo device select-page PAGE_ID --session browser-test
saygo device screenshot --session browser-test
```

默认使用发现的共享桥；指定目录时使用 `--bridge-directory`，WSL 必须传 Windows 目录对应的 WSL 路径，例如 `/mnt/c/Users/YOUR_USER/AppData/Local/Saygo/browser-bridge`。仅在 WSL 内注册 Linux host 无法连接 Windows Chrome。连接拒绝覆盖其他平台或其他桥的会话。

首次连接仅在恰好一个网站标签页时自动选择，否则显式选页。页面身份包含浏览器会话 UUID 和 tab ID；Chrome 重启后不能把旧任务绑定到复用的数字 ID。选页会将页面带到前面，截图本身不会。

## 后台截图与超时

截图/尺寸请求不激活标签页、不聚焦或恢复最小化窗口。截图使用 `Page.captureScreenshot` 返回视口 PNG。扩展 0.4.13 在截图前短暂启动 `Page.startScreencast` 保持隐藏页渲染，确认并丢弃其帧，截图结束/超时后停止；返回图片始终来自 captureScreenshot，尺寸查询不启动流。

支持验收范围含非活动标签、后台窗口和完全遮挡窗口；最小化不在当前支持或发布门槛内。短时空闲测试保持窗口普通状态和目标标签不活跃，不自动前台回退。

每页最多一个未完成视口请求。超时不会取消 Chrome 底层命令，后续同页请求报告“截图仍在进行”，不堆积任务；其他页面及只读诊断仍可用。原请求完成后解除等待，其过期图像被丢弃。导航（含同 URL 重载）、关闭、调试器分离或人工释放都会使在途图像失效。永久不返回的命令持续显示待完成，扩展不会主动分离调试器清理它。

`saygo device diagnose --session browser-test` 返回窗口状态、焦点、tab 活跃性、调试器连接及截图阶段/耗时。使用新诊断需更新运行时和扩展；超时错误也会携带状态。`user_notice` 说明 Chrome 截图接口未响应、连接仍保留，应等待原请求完成后重新观察；它不证明 Chrome 内部根因，也不授权重复点击或发送。

native messaging 连接与活动调试会话可维持扩展 worker 生命周期（后者适用于 Chrome 118+），但不保证截图返回或进程不退出；没有心跳超时主动关桥。参见 [Chrome worker 生命周期](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle)。

## 定点滚动与指针

```sh
saygo device act '{"type":"scroll_at","x":30,"y":60,"coordinate_space":"percent","amount":-3}' --session browser-test --observation-id OBSERVATION_ID --observe-after
```

每单位请求 100 CSS 像素，允许小数，正上负下。坐标决定滚轮事件发送区域；实际滚动容器和位移由浏览器决定，边界可能触发祖先滚动链。scroll_up/down 使用视口中心，swipe 是鼠标拖动。每次观察实际位移并按[公共滚动规则](../common/operations.md#观察有效性与滚动)调整。

滚轮期间临时启用 CDP 逻辑焦点模拟，可能触发页面 focus/visibility 处理器，但不选中标签或前置窗口；结束及超时时尝试关闭模拟。超时滚轮保持输入锁直到 Chrome 返回，绝不自动重放。

还支持 hover、double_click、right_click、long_press。hover 只移动指针，可在出现菜单后重新观察；长按按指定时长保持主键。旧扩展缺动作时需用户更新并手动重载后重连。

## 页面、任务与接管

```sh
saygo device new-page https://example.com --session browser-test
saygo device pages --session browser-test
saygo device select-page PAGE_ID --session browser-test
saygo device close-page PAGE_ID --session browser-test
```

new-page 仅接受 HTTP(S)，返回 `created_page_id`，保留原目标，需 select-page 切换。关闭选中页后须显式另选；即使无选中页也可建页。扩展建页返回时可能仍在加载，超时先检查页面列表再决定，不能盲目重复创建。禁止通过扩展关闭最后一个浏览器标签。

工作流资源指定 `{"web":{"kind":"browser","session":"browser-test","backend":"extension"}}`。页面动作使用 `new_page/select_page/close_page`；后续步骤可引用 `{"$ref":"steps.create.created_page_id"}`。动作仍需新观察及持久意图，结果不明须人工核对。

新标签/弹窗自动可发现但不替换已选目标。人工步骤让用户在原页面工作，之后显式 resume 并独立检查结果。见[扩展接管示例](../../examples/workflows/extension_handoff.json)和[工作流](../common/workflows.md)；示例 URL 检查只证明导航，不证明支付成功。

扩展弹窗的 **Release browser and disconnect（释放浏览器并断开）** 由用户主动撤销控制并清空内存网络记录，不能撤销已派发动作。Chrome 调试器的 Cancel 会禁止该页，须用户断开后重连。释放/断连后重连，浏览器重启后还须重新选页。

CLI 退出只断开适配器，不关闭 Chrome；device stop 移除保存的扩展绑定，全局撤销访问仍通过扩展。超时、无效响应和握手错误不得关闭 native port，迟到回执按请求 ID 忽略。在途输入结束前拒绝第二次输入，但查询和截图可继续。普通 device 与任务共用资源锁，人工仍可能在观察和输入之间改变页面。

不支持浏览器内部页、其他配置文件、非 HTTP(S)、任意脚本执行、DOM 自动化、下载管理、系统对话框及 Firefox。

## 网络记录

连接后自动为可控网站标签页（含新页/弹窗）启动被动记录，不额外弹 Saygo 授权框；浏览器自身调试标记仍显示。查询对象为当前会话所选页：

```sh
saygo device network --session browser-test
saygo device network read --session browser-test --url /api --kind http
saygo device network read --session browser-test --kind ws --after 100 --capture-id CAPTURE_ID
saygo device network read --session browser-test --kind sse
saygo device network read --session browser-test --kind stream
saygo device network stop --session browser-test
saygo device network start --session browser-test
saygo device network clear --session browser-test
```

| 类型 | 内容 |
| --- | --- |
| `http.*` | URL、方法、头、请求数据、状态、耗时、错误、响应正文或不可用原因；重定向是共享 CDP request ID 的独立事件 |
| `ws.*` | 建连、握手、收发帧、错误与关闭；二进制保留 opcode 和 base64 |
| `sse.message` | 原生 EventSource 消息、事件名及 ID |
| `stream.chunk` | fetch 的 text/event-stream 或 NDJSON base64 分块；按顺序解码合并，分块不一定是完整 SSE；不支持时返回 stream.unavailable |

普通 HTTP 长轮询记为 HTTP。轮询将 `next_cursor` 作为下次 after，并携带 capture_id；ID 改变表示清空/重启，从 0 开始。limit 为 1–200，过滤先于分页。`dropped/oldest_cursor` 表示淘汰，`untracked_requests` 表示丢失的请求关联，`truncated` 表示字段裁剪。

每页最多 1,000 事件/1 MiB，总计 8 MiB；字段最多 32 Ki 字符，每页活动请求关联最多 512。响应正文为尽力获取，缓存淘汰、重定向、目标变化或完成请求过多时可能不可用。

stop 只暂停记录、保留旧数据，不断开网络或视觉控制；start 新建采集，clear 清空已存事件但保留记录状态。释放、重载、浏览器退出丢弃内存记录。采集不追溯历史，挂接竞争可能漏新页首批请求；已有 socket 不保证历史，独立 worker/跨进程 iframe 目标尚未挂接。此接口仅适用于扩展，不适用于独立 Playwright/Selenium。

头、正文可能含凭据。记录先留在扩展有限内存，查询后经本地桥返回，不自动加入视觉模型提示或 QA 报告。按授权导出到合适位置，隐私见[隐私说明](privacy.md)。

## 验收

```sh
python3 -m unittest discover -s tests/extension_demo -v
SAYGO_TEST_CHROME=/path/to/chromium python3 -m unittest discover -s tests/extension_demo -v
```

可选真实测试用 Playwright 仅作测试工具，使用临时浏览器配置、native-host 注册和本机页面，不访问个人配置文件。原记录含真实 Windows host 注册、Windows↔WSL 传输和导航/截图；共享桥修复的发布检查见 [0.4.16](../common/history/release-0.4.16.md)。源码、冻结 host 的模拟 IPC、真实浏览器、商店安装/更新须分别验收。

实现参考：[Native Messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging)、[Chrome debugger](https://developer.chrome.com/docs/extensions/reference/api/debugger)、[CDP Network](https://chromedevtools.github.io/devtools-protocol/tot/Network/)。
