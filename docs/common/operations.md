# 统一操作、会话与任务

[公共文档](README.md) · [需求基线](requirements.md)

适用需求：CORE、SESSION、OBS、TASK。六端共用 CLI/MCP 的会话、观察、动作及错误语义；连接前提和特有能力见各端指南。外部 Agent 自行决策，设备服务无需模型密钥。MCP 拒绝 Playwright 的连接、观察、动作及执行任务，将这类保存的绑定列入 `unavailable_sessions`；浏览器默认使用扩展。

## 会话与目标

```sh
saygo device list
saygo device sessions
saygo device connect --platform android --device DEVICE_ID --session phone
saygo device connect --platform browser --backend extension --session web
saygo device connect --platform windows --app 'Example App' --session desktop
saygo device capabilities --session web
saygo doctor --session web
```

`list` 返回 JSON，发现设备和窗口并列出保存的浏览器绑定；它不会连接所有目标或自动截图。某个平台缺少依赖不会隐藏其他平台结果。`sessions` 中存在记录不等于当前在线，必须用真实请求、截图和图像解码核验。

`--session` 是持久别名，旧参数 `--serial` 仍为别名；它不一定是设备序列号。会话保存设备、服务器、页面或窗口身份。多个目标需要显式选择，绑定缺失或过期不自动创建默认 Android 会话，也不暗中更换业务目标。

CLI/MCP 使用相同 `SAYGO_HOME_DIR`（默认 `~/.saygo`）才能共享会话和操作锁。交互 `task` 默认位于其 `runtime` 子目录；显式 `workflow` 默认位于当前目录的 `.saygo_runs/runtime`。`SAYGO_RUNTIME_DIR` 可统一指定任务库；不同客户端和后续命令必须使用一致配置。

`disconnect` 阻止后续自动重连，须显式 `connect` 恢复；它结束 Appium 会话、释放本进程控制器，但保留浏览器/模拟器/应用及重连配置。它不能撤销其他进程已派发的输入，也不全局撤销扩展访问。`device stop` 对托管浏览器具有结束进程的更强语义；扩展访问由用户在弹窗主动释放。

## 观察、坐标和动作

```sh
saygo device screenshot --session web
# 读取返回的图片，以实际观察 ID 和画面坐标替换示例值。
saygo device act '{"type":"tap","x":50,"y":40,"coordinate_space":"percent"}' \
  --session web --observation-id OBSERVATION_ID --observe-after
saygo device wait --session web --mode stable --timeout 5
```

MCP 的 `device_observe`、含后续观察的 `device_act`，以及任务 observe/submit/recover/resume 返回图像内容。旧 `device_screenshot` 与 CLI 返回图像路径和元数据，调用方必须实际读取图片。

观察包含唯一 ID、时间、会话、目标、图像尺寸、屏幕尺寸与坐标映射。支持 `screen`、`percent`、`image`、`crop`；后两种必须引用来源观察。`crop` 使用图像像素矩形 `[left,top,right,bottom]`，返回放大两倍的图像并保留映射。Retina 和缩放截图像素不等于设备逻辑像素；使用服务转换，不手动猜倍率。

动作词汇包括 `tap/swipe/input/press_key/open_url/open_app/scroll_up/scroll_down`；`double_click/right_click/hover/hotkey/long_press/scroll_at` 取决于后端和运行模式。`swipe` 在鼠标后端表示拖动，`hotkey` 用 `keys: ["ctrl","a"]`，长按 `duration` 单位为秒。各端真实支持清单见[需求总索引](requirements.md#需求总索引)。能力表按端区分：浏览器公布 open_url，手机公布 open_app；不支持的动作在派发前拒绝。

传统命令 `tap/input/key/scroll/open` 仍可用；其中直接点击使用逻辑坐标。`open` 对浏览器表示 URL，对手机/桌面表示应用。所有输入命令都必须带 `--observation-id`，并推荐使用 `--request-id` 保存调用身份。先查询能力，再使用可见按钮或菜单；后台不支持的快捷键不能自动改为前台执行。

## 观察有效性与滚动

带来源观察的动作拒绝超过 30 秒的观察。派发前核对目标身份、URL、尺寸、窗口 ID、进程及边界，并比较解码后的像素变化。远离目标的细微变化可以容忍；点击附近变化须重新观察。task 强制使用最新观察；普通 device（包括旧输入命令）也要求来源观察，并拒绝早于上次输入或人工核对的观察。像素阈值是启发式保护，不能证明业务目标未变，也不能阻止人或其他软件在输入期间抢焦点。

滚动先定位正确区域：未知区域先约半屏校准；连续浏览可用可见高度的 85–90%，保留 1–2 行重叠；接近目标或末尾减至 10–20%。每次滚动都读取新截图、对比可见标志物再决定下一步。没有移动时先检查区域、加载和边界，不能盲目加大或重放。

浏览器 `scroll_at` 每单位请求 100 CSS 像素，允许小数；正数向上、负数向下。其他后端可能是滚轮刻度或原生步进。所有端的 scroll_up/down 统一表示视口朝内容顶部/底部移动；移动端分别用手指向下/向上滑动。旧脚本若按手指方向理解名称，需要调整。半屏、重叠和小步接近是操作指导，驱动不会自动按该比例滚动。桌面模型会收到前次滚动截图与当前图像，自行决定下一次幅度。

`wait` 支持 `stable/change`；超时返回 `condition_met: false, timed_out: true`，截图本身仍受后端 I/O 超时限制。画面稳定、`dispatched: true` 或 `business_success: null` 都不能作为业务完成证明，必须核验结果。

## 普通设备请求与核对

普通设备请求也有持久去重和核对入口：

```sh
saygo device screenshot --session web
saygo device input '测试文字' --session web --observation-id OBSERVATION_ID --request-id input-001
saygo device operations --session web
# 先观察并核对结果，再明确记录是否已生效；核对不会重放输入。
saygo device resolve --session web --request-id input-001 --resolution applied --note '已核对画面'
```

`resolve` 仅用于结果不确定的请求，确认未生效时使用 `not_applied`。核对后旧观察失效。MCP 使用 `device_command(command="operations", session=...)` 查询；核对用 `command="resolve"`，在 `options` 中传 `request_id/resolution/note`。调用方重查丢失回执时须保持原请求 ID、会话和全部有效参数；同 ID 异参会被拒绝。未传请求 ID 时服务生成 ID，不能因此把新调用当作安全重试。

## 跨端交互任务

命名 task 另提供跨步骤恢复、接管和证据导出：

```sh
saygo resources bind phone phone
saygo resources bind web web
saygo task create '{"phone":"phone","web":"web"}'
saygo task observe TASK_ID --resource phone
saygo task submit TASK_ID --resource phone --request-id focus-form \
  --observation-id OBSERVATION_ID \
  --action '{"type":"tap","x_pct":50,"y_pct":40}' --note '聚焦测试表单'
saygo task handoff TASK_ID --instructions '请完成测试账号登录'
saygo task resume TASK_ID --note '用户已交还控制'
saygo task recover TASK_ID
saygo task timeline TASK_ID
saygo task events TASK_ID
saygo task finish TASK_ID --note '已核验最终画面'
saygo task export TASK_ID --out evidence.zip
```

项目别名保存在 `.saygo/resources.json`，配置后可直接 `saygo task create`。调用方保存返回的任务 ID。MCP 使用 `agent_task(command, task_id, options)`：create 接收 `bindings`；submit 接收 `resource/action/observation_id/request_id` 及可选 `note`。

派发输入前持久记录动作意图，同一请求 ID 不能派发两次。回执丢失不能触发自动重放；输入是否发生不明时进入 `needs_review`。观察实际结果后执行 `resolve --outcome completed|not_executed --note ...`；两种结果都会使旧观察失效，新输入必须重新观察并明确提交。

Appium 输入异常不再切换输入方法重发；device 与 QA 使用独立于 task 的持久请求记录，同样保留结果不确定时的资源归属。普通请求的核对参数与 task 不同，见下节。

`idle` 且带错误可能表示派发前拒绝，应查事件。已确认输入后的截图失败单独记入 `evidence.error`，不能因此重复输入。任务在空闲、接管或待核对期间仍持有资源，普通 device 命令与其他任务会报告占用。使用所属任务接口；`task list` 查未结束任务，finish 或显式 `cancel --note ...` 释放资源。

全局 OS 锁还串行化各入口的在途操作，所有本地桌面窗口共享输入资源。这些锁只约束 Saygo，不约束人工、其他软件，也不能未经核对就推定 QA 路径有完全相同的锁覆盖。

## 人工接管与证据

单会话也支持 `device handoff/resume` 及 MCP `device_handoff/device_resume`。接管期间禁止自动输入；恢复成功截图后交由调用方核验。登录、支付或系统授权由用户处理，恢复说明不是业务已完成的证明。

设备操作事实写入 `$SAYGO_HOME_DIR/operations` 的 JSONL。可用时保留输入前后截图；建页、切页、关页保存页面列表和目标，关闭选中页时明确记录截图不可用，不换到其他页。

交互任务与声明式工作流保存派发前 `action_dispatching.before`、派发后 `action_evidence` 或截图错误；Agent 说明另存为 `agent_annotation`。导出包含状态、事件和截图，可能含应用资料、输入内容和消息，应按对应业务数据管理。

交互任务的 ZIP 包包含 `task.json`、`events.json`、`timeline.json` 和 `artifacts/*.png`。事件列表与时间线使用同一次历史读取；导出保留待核对状态，不会核对或重放动作。

## 诊断与修复

`saygo doctor --session NAME` 默认只检查连接、截图和图像解码；只有明确提供 `--probe-action` 才验证输入，且结果仍需视觉核验。

`device diagnose --session NAME` / MCP `device_command("diagnose", NAME)` 返回窗口身份、同进程候选（含被排除的辅助窗口）、截图模式、能力和修复提示。某次截图失败不能推导所有窗口都不支持。

任务使用 `task diagnose/repair` 或 `agent_task` 的同名操作；repair 的 `operation` 仅为 `reobserve/select_window`。窗口选择限定已绑定进程的合格可见窗口，可传 `window_id`，须附 `note`。修复写事件、使旧图失效且不重放输入；未核对的输入不能借修复绕过。

任务外的 `device_observe/device_act` 可显式传 `window_id` 和 Windows `foreground`（CLI 对应 `--window-id/--foreground`）。前台截图需要明确选择，不能由 background=false 或截图失败推导。

桌面模型连续三次观察失败或六次诊断/恢复决策后转人工接管；失败期间不能用旧图替代、在无观察资源上操作或宣称完成。

## 验收范围

离线测试覆盖会话共享、坐标映射、资源归属、接管、去重及不确定动作；它们不能替代真机。历史 Playwright 本机页面、Windows 隔离窗口、macOS 原生面板和浏览器桥的实测范围分别记录在六端指南及[测试目录](testing/README.md)。

完整“手机注册 → 邮箱激活 → 桌面确认”仍需指定测试应用、账号和真实设备单独验收。包安装验收与设备业务验收也须分开记录。
