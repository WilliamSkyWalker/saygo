# 浏览器商店材料与发布

[扩展操作](README.md) · [隐私说明](privacy.md) · [公共发布流程](../common/release.md)

## 身份与状态

商店名称 Saygo Browser，ID 为 ehomcchjfomfkcmbeinlcmpbaamdhfbo，[安装入口](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo)。开发 ID 和 manifest key 不用于商店上传。扩展与 Python 运行时版本独立；定点滚动最低运行时为 Saygo 0.4.11、桥协议 1。

旧材料在 2026-10-03 记录 0.4.8 已公开、0.4.12 待审核；后续 [2026-10-12 发布记录](../common/history/release-0.4.16.md)记录 0.4.13 为 PUBLISHED。这些是历史证据，实际审核状态通过只读工作流查询，不以旧材料代替实时核对。

## 自动上传与状态查询

标签触发的 Build release 先运行核心/浏览器回归，再构建商店 ZIP，通过官方 Chrome Web Store v2 API 上传并提交。DEFAULT_PUBLISH 表示 Google 审核通过后发布，提交成功仅代表等待审核。已有可见性设置保留。

所需 GitHub Actions 配置：

| 类型 | 名称 | 来源 |
| --- | --- | --- |
| 变量 | CWS_PUBLISHER_ID | 商店开发者后台的发布者设置 |
| 密钥 | CWS_CLIENT_ID | Google OAuth 客户端 ID |
| 密钥 | CWS_CLIENT_SECRET | OAuth 客户端密钥 |
| 密钥 | CWS_REFRESH_TOKEN | 商店所有者授权的刷新令牌 |

Google Cloud 启用 Chrome Web Store API，创建 Web OAuth 客户端，将 https://developers.google.com/oauthplayground 配为重定向 URI。在 OAuth Playground 选择自有凭据，使用商店所有者账号授权 https://www.googleapis.com/auth/chromewebstore，再交换令牌。刷新令牌直接放 GitHub Secrets，不入库、不贴聊天或问题。

外部 OAuth 应用处于 Testing 时刷新令牌可能短期失效；历史配置使用生产模式。令牌撤销/过期须重新授权。参见[官方 API 配置](https://developer.chrome.com/docs/webstore/using-api)与[令牌过期规则](https://developers.google.com/identity/protocols/oauth2#expiration)。

查询时运行 GitHub Actions 的 Chrome Web Store status，摘要显示已发布/已提交版本、上传状态与政策标记。它只查询，不提交、取消或发布。

同版本已发布或待审核会跳过重复上传；不同版本待审、暂存、上传进行中或政策问题会停止并要求核查。上传处理最多轮询三分钟，审核异步进行。网络错误不自动重传/重提，结果未知先查状态和后台。实现位于 scripts/publish_chrome_store.py，只从环境读凭据，不记录令牌或 OAuth 错误响应体。

新增扩展版本需要明确升版授权且符合商店递增要求；仅 Python 改动不上传同一扩展。最小化窗口不在验收范围，保留正常窗口的非活动标签与短时空闲检查。

## 商店字段与中文介绍

| 字段 | 内容 |
| --- | --- |
| 名称 | Saygo Browser |
| 类别 | 开发者工具或最接近的工具类别 |
| 语言 | 按商店实际语言字段提交，本页提供中文文案 |
| 主页 | https://saygo.work/ |
| 支持 | https://github.com/WilliamSkyWalker/saygo/issues |
| 隐私 | https://saygo.work/privacy.html，提交前核验已部署 |
| 视频 | 无可公开演示时留空 |

Saygo Browser 将现有浏览器标签页连接到本机 Saygo，让 AI 编程助手协助操作和调试网站。支持截图、点击、文字输入、拖动、导航与指定区域滚动，也提供 HTTP 请求/响应、WebSocket 和服务器发送事件等网络观察。

用户点击“连接本地桥”开始，当前配置文件中的可控网站标签（包括新标签和弹窗）即可由本地 Agent 使用。点击“释放浏览器并断开”停止控制并清空扩展网络日志，网站登录状态仍保留在浏览器。

扩展需要单独安装 Saygo 与兼容 AI 客户端：从 PyPI 安装 saygo-agent-control，为客户端执行 saygo setup 并注册本扩展的桥。扩展不包含 AI 模型或订阅，项目按 MIT 开源。

连接期间可访问页面 URL、标题、截图、表单输入和网络内容，可能包括 cookie、令牌等敏感信息。数据交给本机运行时，AI 客户端可能再发送到其模型服务。Saygo 无开发者分析统计接口、不出售资料；断连后本地任务记录可能保留。仅连接愿意分享的浏览器配置文件，chrome:// 等受限制页面不支持。

## 隐私申报

单一用途为用户授权的浏览器操作与调试。权限理由：

- debugger：截图、指针/键盘/滚轮及 HTTP/WebSocket/SSE 观察；CDP 操作有固定白名单，不提供任意脚本工具，需用户连接，释放后分离调试器。
- tabs：发现 HTTP(S) 标签、读取 URL/标题、按用户请求选择/创建/导航/关闭，新页供显式选择。
- storage：保存会话级浏览器身份和已释放标签，避免取消失效或旧 ID 误绑，不建广告画像。
- nativeMessaging：与本机 com.saygo.browser host 交换有界 JSON，不开放远控服务器。

没有远程代码：JavaScript 随 ZIP 打包，消息是结构化命令，不是下载脚本。native host 是用户另装的本地软件，需向审核者说明依赖。

如实申报网站内容、浏览历史（URL/标题）和用户活动；截图/流量可能包含身份、认证、通信、支付财务、健康或位置，应按实际处理范围勾选。不能因首次接收者是本地就宣称不处理数据。没有广告、转售、信用或借贷用途，仅在实际做法与公开政策一致时作相应认证。

## 审核测试步骤

测试不需要 Saygo 账号或付款，使用干净浏览器配置与自有测试页：

1. 准备 Python 3.10+、pipx、所选客户端 CLI，安装待审扩展包。
2. 运行 `pipx install 'saygo-agent-control[mcp]>=0.4.12'`。
3. 运行 `saygo setup --client codex --extension-id ehomcchjfomfkcmbeinlcmpbaamdhfbo`，按需换客户端；WSL 从 WSL 安装以准备 Windows host，macOS/Linux 在浏览器所在系统执行。
4. 打开 https://example.com/，在扩展点击 Connect local bridge，检查已连接和测试页标题。测试商店 ID 时不要加载开发扩展。
5. `saygo device connect --platform browser --session store-review --backend extension` 后 pages，再 `select-page PAGE_ID` 选择目标。
6. `saygo device screenshot --session store-review --out /tmp/saygo-review.png`，Windows 使用可写 Windows 路径，实际读取图像。
7. 在可滚动测试页先观察，再用带 observation-id 的 scroll_at 动作，坐标为百分比，正上负下，并检查新图。
8. 用户点击 Release browser and disconnect，确认断开后控制失败，显式重连前不隐藏重建连接。

host 缺失表示需安装配套软件，不是网站登录错误。提交前还需核对联系人、隐私 URL、128×128 图标、真实 1280×800/640×400 截图、440×280 宣传图与分发字段；审核后实际商店安装、更新、删除独立验证。

参考：[发布指南](https://developer.chrome.com/docs/webstore/publish)、[隐私申报](https://developer.chrome.com/docs/webstore/cws-dashboard-privacy)、[图片要求](https://developer.chrome.com/docs/webstore/images)。
