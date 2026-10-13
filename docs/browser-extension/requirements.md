# Chrome/Edge 扩展操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

初始核对日期：2026-10-12；本次修复状态更新：2026-10-13。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围是已安装扩展的当前浏览器配置文件中的 HTTP(S) 标签页。CLI、MCP 和桌面应用通过同一个 Native Messaging 桥接入；后台截图与普通视觉输入不前置标签，显式选页会前置，必须区别。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 驱动 | [saygo/platforms/browser_extension.py](../../saygo/platforms/browser_extension.py) |
| 扩展 | [extensions/saygo-browser/background.js](../../extensions/saygo-browser/background.js) |
| 网络日志 | [extensions/saygo-browser/network.js](../../extensions/saygo-browser/network.js) |
| 弹窗 | [extensions/saygo-browser/popup.js](../../extensions/saygo-browser/popup.js) |
| 本地桥 | [saygo/integrations/browser_bridge.py](../../saygo/integrations/browser_bridge.py) |
| 桥安装 | [saygo/integrations/browser_setup.py](../../saygo/integrations/browser_setup.py) |
| 桥发现 | [saygo/integrations/browser_location.py](../../saygo/integrations/browser_location.py) |
| 网络命令 | [saygo/devices/network.py](../../saygo/devices/network.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 连接 | [saygo/devices/control.py](../../saygo/devices/control.py) |

## 安装、桥与连接

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| EXT-001 | Chrome/Edge 在浏览器所属 OS 安装 Native Messaging host；Windows 浏览器可供原生 Windows 与 WSL 客户端共用。 | 桥安装.setup；桥发现.default_directory | 已有实现；Edge 独立验收 |
| EXT-002 | 桥以私有目录请求/响应通信，不监听网络端口；目录和会话文件不能被解释成在线证明。 | 本地桥.Client/host；桥发现 | 已有实现 |
| EXT-003 | 安装默认绑定发行扩展 ID，开发 ID 显式指定；协议握手不兼容须提示两端版本，不报告已连接。 | 桥安装；本地桥；扩展.connect | 已有实现 |
| EXT-004 | 只有用户在扩展中连接后才可操作，当前配置文件的 HTTP(S) 页可发现；不延伸到其他 profile 或浏览器内部页。 | 弹窗；扩展.connect/pages/target | 已有实现 |
| EXT-005 | 连接保存桥目录和 backend；同名会话不可换桥、平台或后端，旧绑定失效须显式处理。 | 连接._connect；会话.attach_browser | 已有实现 |
| EXT-006 | Windows 桌面/包安装/WSL 发现实际在线目录、注册和安装记录，不因同版本省略检查或默认另建桥。 | 桥发现；桥安装；saygo/updates.py | 已有实现；历史 0.4.16 证据 |
| EXT-007 | 更新安装器不强制断开、重载扩展或杀在线 host；新连接使用一致目录，现有连接继续保留。 | 桥安装；本地桥；saygo/updates.py | 已有实现；升级组合逐项验收 |
| EXT-008 | 卸载仅移除自身拥有的 host 注册，保留用户修改和其他安装；源码更新不等于用户扩展已更新。 | 桥安装；scripts/install_agent_plugin.py | 已有实现 |

## 页面生命周期与目标

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| EXT-009 | 页面 ID 组合浏览器会话 UUID 和 tab ID；重启后旧 ID 失效，不能因 tab 数字重用选中别页。 | 扩展.state/pages/target | 已有实现 |
| EXT-010 | 页面列表返回 URL、标题、选中状态与可用的打开者关系；单页可初始绑定，多页需显式选择。 | 驱动.connect/list_pages；扩展.pages | 已有实现 |
| EXT-011 | 桌面版明确授予浏览器访问时允许初始自动绑定候选页但不激活；任务/接管期间不能借自动检测重新选页。 | 连接._connect(auto_page)；desktop/app.py | 已有实现；是默认显式选页规则的例外 |
| EXT-012 | 显式 select-page 校验目标并激活该标签和窗口，同时持久保存绑定；不能写成选页也不抢焦点。 | 驱动.select_page；扩展 select 分支 | 已有实现 |
| EXT-013 | new-page 只接受 HTTP(S)，创建非活动标签并返回 ID，保留原选中目标；后续要显式选择。 | 驱动.new_page；扩展 new_page 分支 | 已有实现 |
| EXT-014 | 关闭选中页后不能偷偷改绑；最后一个浏览器标签不能经扩展关闭；无选中页仍可列页/建页/选页。 | 驱动.close_page；扩展 close 分支；操作服务 | 已有实现 |
| EXT-015 | 新标签和弹窗可发现但不替换原目标；扩展驱动当前不提供跨进程持久页面事件队列，不能承诺完整事件历史。 | 扩展页面监听；驱动.drain_events | 页面发现已有；事件队列未提供 |
| EXT-016 | 导航限 HTTP(S)，支持回退与前进；URL 变化使旧观察失效，导航回执不等于加载或业务成功。 | 扩展 navigate/back/forward；devices/actions.prepare | 已有实现 |
| EXT-017 | 创建/关闭/选页保存派发前后页面证据，截图失败保留错误；创建超时先列表核对，不能盲目再建页。 | devices/service._page_evidence；runtime/resources | 已有实现 |

## 截图、诊断与普通输入

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| EXT-018 | 截图只取绑定页当前视口，转换到 CSS 像素并记录页面/URL/尺寸映射，不读取 DOM 做视觉定位。 | 驱动.screenshot_raw；扩展截图分支 | 已有实现 |
| EXT-019 | 后台截图不激活标签、不前置窗口或恢复最小化窗口；首次可通过短暂 screencast 唤醒绘制，完成后清理。 | 扩展 execute 的截图分支 | 已有实现；最小化可用性不保证 |
| EXT-020 | 截图期间视口位置或尺寸变化要重新采样；页面关闭/导航、控制权撤销及过期请求的迟到图像必须丢弃。 | 扩展 checkCapture/getLayoutMetrics | 已有实现 |
| EXT-021 | 截图和输入超时有界，保留阶段、时间线及连接诊断；失败不关闭用户 native port，不缓存旧图伪装成功。 | 扩展.runRequest/captureStatus/diagnose；本地桥 | 已有实现 |
| EXT-022 | 支持单击、悬停、双击、右键、长按和拖动；坐标对 CSS 视口校验，长按释放鼠标有清理路径。 | 驱动指针方法；扩展输入分支 | 已有实现；各手势须真实页面核验 |
| EXT-023 | 文字输入使用 Input.insertText 注入当前焦点，输入前观察并点击目标字段；不调用页面脚本写表单值。 | 驱动.input_text；扩展 input 分支 | 已有实现 |
| EXT-024 | 按键支持 enter/tab/escape/space/delete/backspace/arrow_up/arrow_down/select_all；select_all 按浏览器 OS 选 Ctrl 或 Meta。 | 扩展 key 分支 | 已有实现 |
| EXT-025 | 不宣称独立 hotkey、任意组合键、系统对话框和浏览器工具栏控制；不支持的键要报错。 | 驱动方法集；扩展键表 | 当前不支持通用快捷键 |
| EXT-026 | scroll_at 在指定 CSS 坐标发滚轮，每单位 100 CSS 像素，支持小数，正上负下；实际容器与位移须观察。 | 驱动.scroll_at；扩展 scroll_at 分支 | 已有实现 |
| EXT-027 | scroll_up/down 从视口中心请求 300 CSS 像素滚动；swipe 是鼠标拖动，不是触摸或滚轮的同义词。 | 扩展 scroll/swipe 分支 | 已有实现 |
| EXT-028 | 滚动临时模拟逻辑焦点以驱动后台页面，结束/超时尝试关闭；页面可触发 focus/visibility 处理器，但不选中标签。 | 扩展 wheel | 已有实现；页面副作用需核验 |
| EXT-029 | 底层输入未结束时阻止第二次输入，超时不能解除输入锁后重发；页面查询和观察仍可读取诊断。 | 扩展.runRequest；本地桥.Client.call | 已有实现 |

## HTTP、WebSocket 与流式记录

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| EXT-030 | 连接后被动记录可控页及新页/弹窗的网络，不额外增加 Saygo 授权框；浏览器自身调试提示仍保留。 | 扩展.startNetwork/autoNetwork/页面监听 | 已有实现 |
| EXT-031 | network read/start/stop/clear 只对当前所选扩展页生效；Playwright/Selenium 会话明确拒绝。 | 网络命令.execute；驱动.network | 已有实现 |
| EXT-032 | HTTP 记录请求 URL、方法、头、请求数据、响应状态、耗时、错误与可取正文；重定向独立记事件。 | 网络日志 HTTP 分支 | 已有实现；正文尽力获取 |
| EXT-033 | WebSocket 记录连接、握手、收发帧、错误与关闭，保留 opcode 和二进制 base64，不伪造连接前历史。 | 网络日志 WebSocket 分支 | 已有实现 |
| EXT-034 | 原生 EventSource 记录 SSE 消息、事件名与 ID；fetch 的 SSE/NDJSON 记录有序 base64 分块，能力不足明示 unavailable。 | 网络日志 SSE/stream 分支 | 已有实现；分块不一定是完整消息 |
| EXT-035 | 读取按 URL/kind 过滤后分页，limit 1–200、after 非负，返回 next_cursor 与 capture_id；旧采集游标不能静默套到新采集。 | 网络命令.register/execute；网络日志.read | 已有实现 |
| EXT-036 | 按每页 1000 事件/1 MiB、总 8 MiB、字段 32 Ki 字符和活动请求关联 512 上限淘汰/裁剪，并标出 dropped、truncated、untracked_requests。 | 网络日志的限额与事件存储 | 已有实现 |
| EXT-037 | stop 停止新增并保留旧数据，start 建新采集，clear 清数据且保留记录状态；这些不是断网或撤销视觉控制。 | 扩展 network 分支；网络日志 | 已有实现 |
| EXT-038 | 释放、扩展重载、浏览器退出会丢弃内存记录；首次挂接之前、新页竞争、独立 worker/跨进程 iframe 目标不保证完整采集。 | 扩展连接及网络生命周期 | 当前边界；非持久完整抓包 |
| EXT-039 | 网络可能含凭据和正文，只在本地有限内存留存并按显式查询返回；不自动塞入视觉模型、QA 报告或业务成功判定。 | 网络日志；驱动.network；隐私说明 | 已有实现；调用方另管导出权限 |

## 接管、断连与验收

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| EXT-040 | 人工 handoff 阻止 Saygo 自动操作，resume 获取新截图并独立核验；页面消失不能改借其他业务会话。 | devices/control；runtime/interactive | 已有实现 |
| EXT-041 | 扩展释放按钮撤销控制并清记录；Chrome 调试 Cancel 禁止自动重新附加该页，须用户断开重连。 | 弹窗；扩展.detachAll/onDetach | 已有实现 |
| EXT-042 | 普通 CLI/MCP 控制器退出只释放客户端，不关浏览器/host；device disconnect/stop 不等于全局撤销扩展权限。 | 驱动.teardown；会话._browser_stop；连接._disconnect | 已有实现 |
| EXT-043 | 跨任务互斥以共享桥/会话资源管理，不能保证用户或其他软件不改变页面；超时与迟到回执按请求 ID 核对。 | runtime/locking；本地桥.Client | 已有实现 |
| EXT-044 | 不支持其他 profile、非 HTTP(S)、任意脚本/DOM 自动化、下载管理、系统文件对话框或 Firefox；浏览器原生弹窗需人工。 | 扩展白名单；驱动 | 当前不支持 |
| EXT-045 | 分别验收 Chrome/Edge、各宿主 OS、WSL 共存、CLI/MCP 重启、后台截取、输入、网络与商店安装/更新；模拟 IPC 不能代替实际扩展。 | `tests/extension_demo`；`tests/control_demo/test_network.py` | Chrome/Windows↔WSL 有局部证据；其余逐项验收 |

## 验收范围

入口：[扩展桥](../../tests/extension_demo/test_bridge.py)、[共享桥](../../tests/extension_demo/test_shared_bridge.py)、[真实 Chrome](../../tests/extension_demo/test_live.py)、[网络命令](../../tests/control_demo/test_network.py)。历史真实 Chrome、Windows host/WSL 传输与冻结 host 模拟 IPC 的边界见[操作指南](README.md#验收)和[0.4.16](../common/history/release-0.4.16.md)。商店提交/审核、Edge、最小化环境不能据此一并标为通过。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。

本轮源码修复与迁移、六端分别验证的范围见[修复记录](../common/requirements-audit.md#升级与兼容性)。未更新用户安装或发布版本。
