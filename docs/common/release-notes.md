# Saygo 1.0.0：后台浏览器操作与 Android 设置指引

1.0.0 发布准备中，范围为 Python runtime、托管客户端插件和浏览器扩展。
已获得提交、推送、PyPI 与浏览器插件发布授权；构建、发布 CI、公开文件及商店审核状态
尚待核验，本说明不代表 1.0.0 已上线。原生桌面安装包不在本轮发布范围内。

## 行为变化

- **选页保留用户当前标签和桌面前台。** `select-page`、`select_page` 和显式页面连接
  只改变 Saygo 的控制目标。后续截图、输入仍作用于该目标，重复选页不激活可见标签。
  过期 page ID 仍须显式重选，不切换到其他业务会话。
- **新增后台链接动作 `open_link_background`。** Agent 根据截图给出坐标，驱动在
  隔离执行环境中命中节点、最多检查八层祖先，仅读取普通 HTTP(S) 链接 URL，然后
  在同窗口创建非活动标签并返回 `created_page_id`，保留原控制目标。模型不接收
  DOM、控件树或链接文本；此动作属于用户明确授权的窄范围驱动适配例外。
- **CLI、MCP、Runtime 和桌面决策共用动作语义。** 保留新观察、百分比/图像坐标映射、
  持久请求和未知结果不重放等保护；其他浏览器后端不自动获得该扩展能力。
- **Android 首次设置更清楚。** 纳入此前 `d58f6c8` 的依赖指引：连接前可用
  `doctor --platform android` 检查 macOS、原生 Windows 或 WSL/Windows 宿主。
  返回结构化缺失项及当前解释器的修复命令，不自动安装或替换环境。
- **已有 Android 真机可只准备工具链。** `device install --platform android --tools-only`
  准备 Java、SDK、Node/Appium/UiAutomator2，不下载模拟器/系统镜像或创建 AVD；
  保留显式主机、dry-run 与 SDK 许可确认，已有连接不自动重启。

后台链接动作是独立 URL 导航，不执行点击处理器、不保留 opener，也不承诺复制 referrer
和命名窗口语义。非链接、下载和非 HTTP(S) 链接明确拒绝。普通左键 `tap` 保留原行为，
网页新标签或脚本弹窗仍可能让浏览器前置；后台动作不会回退为普通点击或事后抢回焦点。
任意 JavaScript 弹窗、跨域 frame 和 Shadow DOM 不在本次真实验收范围。

## 升级与已有会话

发布完成后，按原安装方式升级 Python runtime，并重启 Agent 客户端。复制式插件安装
按原客户端与目录重新 setup，保留用户配置。新动作需要匹配的 runtime 和浏览器实际
加载的扩展；单独升级 Python 包不会更新已加载的扩展或在线 host。

已有会话和任务无需清空。逻辑选页现在保留当前可见标签，Agent 继续操作明确绑定页面。
浏览器重启后的旧 page ID 仍须重新选择，未知输入不重放。发布过程不主动重载/断开
用户扩展或结束在线 host，由用户决定重连及更新时机。商店提交、审核、实际分发和
用户已加载新版分别核实；源码修改与旧桌面二进制也分别记录。

## 已验证范围与待完成发布

升版前源码在 macOS arm64 上完成 90 项 JavaScript、20 项桥接、25 项共享服务及
10 项桌面决策检查；普通发现跳过的 macOS live 另行显式运行，1 项通过。
真实 Chrome 157 测试经过 CLI、native host 和实际扩展，在独立 profile/本地网页中
验证前台 PID/窗口顺序、选页、建页、后台链接、新页截图输入及非链接拒绝；连接弹窗
和结果 PNG 已查看。测试当时仍标记 0.4.21，不能写作 1.0.0 构建或安装验收。

2026-11-10 对已升版的 1.0.0 源码另行复验：macOS 27.0 arm64、Chrome
157.0.8103.50，真实扩展测试 1 通过、0 失败、0 跳过，用例耗时 85.637 秒。
前台焦点、后台建页/链接、输入和非链接拒绝全部通过；三张 PNG 分别确认扩展
`1.0.0 Connected` 和两页输入结果。此项是源码实机复验，仍不等于发布包安装验收。

Android 指引此前有 180 项单元/契约通过记录，设备和 Windows/WSL 宿主为模拟，
不是本轮真机重测。本机缺少 Claude CLI，两项插件 validator 未运行。新版 Windows、
Linux、Edge、Playwright 焦点/链接、Android/iOS 真机及原生桌面包尚未新增验收。

1.0.0 本地 sdist→wheel 构建、严格 twine 检查、macOS 干净安装及重复 setup 已通过。
发布 CI、PyPI/GitHub 公开下载核验、商店上传和审核状态待补录。[发布前商店核验](https://github.com/WilliamSkyWalker/saygo/actions/runs/42747930084)
确认当前为 0.4.21 `PUBLISHED` / 100%，`submitted: {}`；1.0.0 尚未公开发布。
详细变更、命令、兼容性和后续发布状态见
[1.0.0 发布记录](https://github.com/WilliamSkyWalker/saygo/blob/main/docs/common/history/release-1.0.0.md)。此前发布事实保留在
[0.4.21 历史记录](https://github.com/WilliamSkyWalker/saygo/blob/main/docs/common/history/release-0.4.21.md)。
