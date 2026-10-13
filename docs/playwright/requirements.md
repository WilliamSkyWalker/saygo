# Playwright 操作需求清单

[操作指南](README.md) · [公共需求与总索引](../common/requirements.md) · [代码核对记录](../common/requirements-audit.md)

初始核对日期：2026-10-12；本次修复状态更新：2026-10-13。以下按当前工作区代码整理，每条均给出入口或实现位置。已有实现不代表本次真机验收通过；缺口保留应达到的需求，并说明代码尚未满足的部分。

范围是 CLI/Runtime 使用 CDP 接入的独立 Chromium。它不是 MCP 后端，也不自动接管用户日常浏览器。Selenium 保留在 QA 兼容入口，不能混入 Playwright 验收。

公共要求同时适用：[会话与资源](../common/requirements.md#session)、[观察与动作](../common/requirements.md#obs)、[交互任务](../common/requirements.md#task)、[工作流](../common/requirements.md#flow)。本表将其落实到本端的具体操作，不以其他端通过代替本端验收。

## 代码索引

| 简称 | 实现文件 |
| --- | --- |
| 驱动 | [saygo/platforms/browser_playwright.py](../../saygo/platforms/browser_playwright.py) |
| 会话 | [saygo/platforms/device_session.py](../../saygo/platforms/device_session.py) |
| 连接 | [saygo/devices/control.py](../../saygo/devices/control.py) |
| 操作服务 | [saygo/devices/service.py](../../saygo/devices/service.py) |
| 资源 | [saygo/runtime/resources.py](../../saygo/runtime/resources.py) |
| MCP 策略 | [saygo/mcp/backend_policy.py](../../saygo/mcp/backend_policy.py) |

## 安装、入口与持久浏览器

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| PW-001 | 依赖缺失给 Playwright 安装提示；浏览器按显式路径、系统安装/PATH、Playwright Chromium 顺序查找。 | 会话._chrome_binary；驱动._acquire_playwright | 已有实现 |
| PW-002 | device start 应显式 backend=playwright；统一 connect 和 workflow 有各自默认值，不把旧 start 的 Selenium 默认写成已改。 | 会话._browser_start；连接._connect；资源 | 已有实现；入口默认值不同 |
| PW-003 | 启动命名独立 Chromium 进程和专用 profile，支持 headless、视口宽高，记录调试端点；人工接管使用有头模式。 | 会话._browser_start | 已有实现 |
| PW-004 | CDP 接入已有 Chromium，不要求 DOM selector；当前仅 Chromium，不能声称支持 Firefox/WebKit 或 Playwright 原生远程协议。 | 驱动.connect | 已有实现；支持范围限定 |
| PW-005 | 短命令退出只停止自身 Playwright 控制器，不关闭 browser/context；device stop 才停止命名浏览器并清状态。 | 驱动.teardown；会话._browser_stop | 已有实现 |
| PW-006 | disconnect 保留端点并阻止普通动作隐式复连；connect 不换 backend、不替换浏览器，失败恢复原断开标志。 | 连接._connect/_disconnect | 已有实现 |
| PW-007 | 已有托管 Selenium 会话可用显式 device start 切到 Playwright，复用 profile/浏览器；统一 connect 不允许这样更换 backend。 | 会话._browser_start；连接._connect | 已有实现 |
| PW-008 | MCP 拒绝本后端连接、动作、观察及会执行的任务恢复；仍允许状态审计/取消，不能自动回退扩展或另建页。 | MCP 策略.check/check_task | 已有实现 |

## 页面身份与生命周期

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| PW-009 | 页面 ID 使用 Chromium target ID，跨控制器进程保持稳定；不能用页面顺序或重复 URL 当身份。 | 驱动._target_info/_page_map | 已有实现 |
| PW-010 | 首次只有一页可自动绑定，多页或零页时先列页再明确选择；管理接口可在缺少有效目标时工作。 | 驱动.connect(manage_pages) | 已有实现 |
| PW-011 | 页面列表返回 ID、URL、标题、opener ID 和选中状态；选页持久保存并前置绑定页面。 | 驱动.list_pages/select_page/_bind | 已有实现 |
| PW-012 | new-page 只接受 HTTP(S)，使用选中页上下文，未选页时要求只有一个 context；返回 ID，保留原选择。 | 驱动.new_page | 已有实现 |
| PW-013 | 创建后导航失败保留已创建标签供核查，不自动重复创建或关闭证据。 | 驱动.new_page；操作服务 | 已有实现 |
| PW-014 | 关闭目标后保存失效选择，后续截图/输入报错；不自动选别页。当前 close 不执行 beforeunload 交互，也无扩展的最后页保护。 | 驱动.close_page | 已有实现；调用方需明确关闭意图 |
| PW-015 | 新页面/弹窗仅入事件列表，不替换目标；事件只在连接期间收集，离线期间靠页面列表重发现。 | 驱动._watch_contexts/_on_page/drain_events | 已有实现；非持续事件日志 |
| PW-016 | JS alert/confirm/prompt 不自动确认或关闭，记录对话框事件；阻塞时交用户处理后核对未知动作。 | 驱动._on_dialog；connect 事件订阅 | 部分能力；无通用对话框操作协议 |
| PW-017 | 浏览器重启导致 target ID 改变，旧任务绑定拒绝复用；恢复使用任务检查点的 page ID，不跟随其他 CLI 的默认页。 | 驱动._bind；资源；runtime/engine | 已有实现 |

## 观察与输入

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| PW-018 | 截图前会前置绑定页，截当前视口且 scale=css；不承诺扩展后端的后台无焦点影响。 | 驱动.screenshot_raw | 已有实现 |
| PW-019 | 观察包含 page ID、URL、尺寸及页面列表，读取视口几何不用于 DOM 语义定位；相同图像但换页/导航仍拒绝旧观察。 | 驱动.screen_size/observation_metadata；devices/actions | 已有实现 |
| PW-020 | 支持单击、悬停、双击、右键、长按和按住拖动；拖动释放鼠标有 finally 路径。 | 驱动指针方法 | 已有实现；真实页面逐操作核验 |
| PW-021 | 文字输入作用于已聚焦字段，支持 Unicode；不通过 selector 查找字段或直接执行脚本改值。 | 驱动.input_text | 已有实现 |
| PW-022 | 按键映射 enter/delete/tab/space/escape/select_all/backspace/arrow_up/arrow_down；其他合法 Playwright 键名交由库校验。 | 驱动.press_key | 已有实现 |
| PW-023 | 组合键将 ctrl/alt/shift/cmd/meta 映射到浏览器键盘，非法键必须由统一校验/库报告错误。 | 驱动.hotkey；devices/actions | 已有实现 |
| PW-024 | 定点滚动先移动浏览器指针，每单位 100 CSS 像素，支持小数，正上负下；实际容器和边界由页面决定。 | 驱动.scroll_at | 已有实现 |
| PW-025 | 普通上下滚动请求 300 CSS 像素，沿用当前指针位置；不能把扩展的视口中心规则写成本端行为。 | 驱动.scroll_up/scroll_down | 已有实现 |
| PW-026 | 导航、前进、后退等待 DOMContentLoaded；加载完成不证明业务成功，超时后先观察，不自动重试输入。 | 驱动.open_target/_handle_platform_action | 已有实现 |
| PW-027 | 截图/连接/导航设置超时，坐标动作不具 Locator 的可操作性自动等待；使用共享稳定/变化等待并核验截图。 | 驱动.connect/_watch_contexts/screenshot_raw | 已有实现 |
| PW-028 | 只声明明确的页面导航动作；通用能力表不应把 open_app 公布成浏览器启动本机应用的能力。 | devices/actions.BASE；驱动.open_target | 已修复：仅公布 open_url，不将 open_app 当导航别名 |

## 任务、接管与边界

| 编号 | 需求与验收条件 | 入口或代码位置 | 当前状态 |
| --- | --- | --- | --- |
| PW-029 | Runtime browser 资源支持 session、backend 和显式 page_id，动作携带最新观察；选页后要重新观察才能点击。 | 资源；runtime/schema；runtime/engine | 已有实现 |
| PW-030 | 同 session 的页面由单一任务占用，首版不支持按标签页分配并发任务；不同 context 控制器复用线程内 Playwright 循环。 | runtime/locking；驱动._acquire_playwright/_release_playwright | 已有实现 |
| PW-031 | 接管/恢复保留页面和登录存储；resume 新截图，结果未知的动作先 resolve，不能因重连自动重发。 | runtime/interactive；资源 | 已有实现；真实业务另验 |
| PW-032 | 不提供扩展 network 记录接口、通用下载管理、系统文件对话框或完整原生弹窗操作协议。 | devices/network.execute；驱动方法集 | 当前不支持 |
| PW-033 | 验收使用临时 profile 和自有页面，覆盖 CLI、多进程重连、Unicode、弹窗、页面关闭保护与控制器退出后浏览器存活。 | `tests/browser_demo/test_playwright_live.py` | 有历史真实 Chromium 证据；不是第三方登录/支付验收 |

## 验收范围

入口：[Playwright 契约](../../tests/browser_demo/test_playwright.py)、[真实 Chromium](../../tests/browser_demo/test_playwright_live.py)、[Runtime](../../tests/runtime_demo/test_runtime.py)。真实测试运行边界见[操作指南](README.md#验证与边界)。测试工具使用 Playwright 去验扩展，并不表示 MCP 可使用 Playwright 后端。

本次只核对源码和文档，不操作现有业务会话。完整验收必须记录环境、连接模式、命令、前后截图、输入结果、断连恢复和未通过项；存在代码的动作也必须在目标设备或应用上单独核验。

本轮源码修复与迁移、六端分别验证的范围见[修复记录](../common/requirements-audit.md#升级与兼容性)。未更新用户安装或发布版本。
