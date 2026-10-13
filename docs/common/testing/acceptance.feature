# language: zh-CN
功能: Saygo 跨模块及真实环境验收

# 这些场景需要指定运行环境、测试设备或隔离夹具；本轮未执行的场景不计为自动化通过。

  @AC-001 @CORE-001 @manual
  场景: AC-001 device profile 无模型凭据
    假如 干净环境仅安装 mcp extra，未设置模型 API Key
    当 从 checkout 外启动 device profile 并完成 initialize/list_tools
    那么 握手成功，设备工具可见，不加载 QA 模型

  @AC-002 @CORE-002 @manual
  场景: AC-002 GUI 与 CLI 共享任务
    假如 桌面版创建任务并保存 task ID
    当 关闭 GUI 后用 CLI 查询并 recover 同一任务
    那么 事件、绑定和状态一致，未知动作不会重复执行

  @AC-003 @CORE-005 @manual
  场景: AC-003 精简依赖帮助
    假如 环境只有核心依赖，不含 Appium、Selenium 或 OpenAI
    当 执行 saygo --help 和 saygo device --help
    那么 命令成功退出，不因无关依赖缺失失败

  @AC-004 @SESSION-001 @manual
  场景: AC-004 命名会话防误绑
    假如 mail 已绑定页面 A，页面 B 属于另一任务
    当 尝试用 mail 静默连接 B
    那么 拒绝或要求显式重新绑定，不能操作 B

  @AC-005 @SESSION-002 @manual
  场景: AC-005 设备多选边界
    假如 两台 Android 均在线
    当 省略 device 参数执行 connect
    那么 明确列出候选并要求选择，不猜测第一台

  @AC-006 @SESSION-004 @manual
  场景: AC-006 断开保留进程
    假如 已连接运行中的 Android 模拟器
    当 执行 device disconnect
    那么 Appium 会话关闭，模拟器进程和用户数据保留

  @AC-007 @SESSION-005 @manual
  场景: AC-007 人工接管阻止输入
    假如 手机会话处于 handoff
    当 尝试 tap、input 和 open_app 后执行 resume
    那么 接管时输入被拒绝，resume 返回新截图

  @AC-008 @SESSION-006 @manual
  场景: AC-008 空闲任务继续持锁
    假如 任务 A 已绑定 mail 且处于 idle
    当 任务 B 尝试绑定并操作 mail
    那么 B 收到资源占用错误，A 状态保持

  @AC-009 @SESSION-008 @manual
  场景: AC-009 桌面跨窗口串行
    假如 窗口 A 上 Saygo 输入锁已占用
    当 同时对窗口 B 请求输入
    那么 第二个请求不并发触发全局键鼠

  @AC-010 @OBS-004 @manual
  场景: AC-010 裁剪映射
    假如 400×200 屏幕的 200×100 截图裁剪 [20,10,80,60] 并放大两倍
    当 在 crop 坐标 [20,10] 点击
    那么 落点映射到屏幕 [60,30]，记录来源观察

  @AC-011 @OBS-005 @manual
  场景: AC-011 过期观察拒绝
    假如 观察生成于 31 秒前且画面未变
    当 用该观察提交 tap
    那么 输入未派发，提示重新观察

  @AC-012 @OBS-006 @manual
  场景: AC-012 目标区域细微变化
    假如 截图大部分未变但点击点附近按钮发生变化
    当 提交旧观察上的点击
    那么 局部变化触发拒绝，不能仅靠全局差异小而通过

  @AC-013 @OBS-009 @manual
  场景: AC-013 输入后截图失败
    假如 输入驱动已明确返回成功，后续截图抛异常
    当 读取动作结果并恢复任务
    那么 记录 evidence.error，不将已确认输入自动重放

  @AC-014 @OBS-010 @manual
  场景: AC-014 稳定不等于完成
    假如 页面持续稳定但业务仍显示处理中
    当 等待 stable 返回
    那么 condition_met 为真，业务结果仍待核验

  @AC-015 @TASK-002 @manual
  场景: AC-015 相同请求去重
    假如 第一次 request ID 为 submit-one 的输入已派发
    当 客户端丢失响应后重复提交 submit-one
    那么 驱动只收到一次输入，返回持久记录

  @AC-016 @TASK-003 @manual
  场景: AC-016 派发崩溃
    假如 任务已记录 action_dispatching，进程在输入回执前退出
    当 新进程 recover
    那么 标记 needs_review，不能自动继续原输入

  @AC-017 @TASK-005 @manual
  场景: AC-017 核对后新观察
    假如 任务处于 needs_review 且旧观察仍在磁盘
    当 resolve not_executed 后尝试用旧观察提交
    那么 旧观察失效，需获取新观察再决定输入

  @AC-018 @TASK-007 @manual
  场景: AC-018 取消释放资源
    假如 任务持有 phone、mail 并暂停人工接管
    当 带说明 cancel 后创建新任务绑定同资源
    那么 原任务记录取消，新任务可获得资源

  @AC-019 @TASK-008 @manual
  场景: AC-019 证据导出
    假如 任务有一次成功点击、一次截图错误和 Agent 注释
    当 导出 ZIP
    那么 操作事实、异常、截图与注释独立保留且可关联

  @AC-020 @TASK-010 @manual
  场景: AC-020 错误进程窗口修复
    假如 任务绑定进程 A，候选窗口属于进程 B
    当 repair select_window 指向 B
    那么 拒绝跨进程修复，绑定 A 保留

  @AC-021 @TASK-012 @manual
  场景: AC-021 真实跨端验收
    假如 指定测试手机、测试邮箱、测试后台及专用账号可用
    当 通过任务完成注册、邮箱激活、后台核对并导出证据
    那么 三端真实结果分别可核验，不能用模拟驱动通过代替

  @AC-022 @FLOW-009 @manual
  场景: AC-022 SQLite 写入阻止
    假如 只读资源注册一条企图 DELETE 的查询
    当 运行 tool 步骤
    那么 写入被 authorizer 拒绝，数据库内容不变

  @AC-023 @FLOW-010 @manual
  场景: AC-023 数据库行数上限
    假如 只读表有超过 1000 行
    当 运行不带 LIMIT 的注册查询
    那么 返回有界结果，不无限占用内存

  @AC-024 @FLOW-006 @manual
  场景: AC-024 人工确认后失败验证
    假如 human 的 verify_step 检查 paid，数据库仍为 pending
    当 用户 resume 并执行后续 check
    那么 任务失败而非将人工确认当支付成功

  @AC-025 @BROWSER-004 @manual
  场景: AC-025 关闭指定页留证
    假如 浏览器有 A、B 两页，任务绑定 A
    当 关闭 A 并查询当前绑定
    那么 记录 A 已关闭与截图不可用，不暗中改选 B

  @AC-026 @BROWSER-006 @manual
  场景: AC-026 后台休眠页截图
    假如 绑定页 A 在后台休眠，前台页为 B
    当 观察 A
    那么 在有界预热后截 A 或明确报错；不把 B 截图当 A

  @AC-027 @BROWSER-009 @manual
  场景: AC-027 嵌套面板滚动
    假如 测试页有外层列表和内层 600 CSS 像素列表
    当 对内层中心 scroll_at amount=-3
    那么 内层约向下移动半屏且保留重叠，外层不误滚

  @AC-028 @BROWSER-011 @manual
  场景: AC-028 桥升级保留连接
    假如 浏览器扩展正在使用旧 native host
    当 升级 Python 包并启动新 MCP
    那么 旧连接仍可用；新桥准备好供显式重连使用

  @AC-029 @BRIDGE-003 @manual
  场景: AC-029 协议不匹配
    假如 扩展与 host 协议版本不一致
    当 建立连接并请求输入
    那么 返回两端版本和修复说明，不派发输入

  @AC-030 @BRIDGE-004 @manual
  场景: AC-030 卸载注册所有权
    假如 安装 A 的 host 注册已由安装 B 接管
    当 卸载安装 A
    那么 保留 B 的 host 注册

  @AC-031 @BRIDGE-006 @manual
  场景: AC-031 网络流记录
    假如 测试页请求普通 JSON 及流式响应
    当 通过当前页读取网络记录
    那么 方法、状态、正文/流片段及受限内容说明对应正确请求

  @AC-032 @MOBILE-005 @manual
  场景: AC-032 Android dry-run
    假如 主机尚无完整 Android 工具链
    当 执行 install --dry-run
    那么 输出组件、磁盘和加速计划，不下载不修改系统

  @AC-033 @MOBILE-006 @manual
  场景: AC-033 下载完整性失败
    假如 下载的工具归档校验和与发布值不同
    当 执行安装
    那么 中止提取与执行，输出校验失败

  @AC-034 @MOBILE-007 @manual
  场景: AC-034 同名异镜像拒绝
    假如 名为 Saygo 的 AVD 使用 API 35
    当 请求同名 API 36 镜像安装
    那么 拒绝覆盖并提示使用其他名称

  @AC-035 @MOBILE-008 @manual
  场景: AC-035 缺少加速
    假如 Windows Hypervisor 未启用
    当 请求模拟器 boot
    那么 报告加速阻塞，不修改 BIOS、不重启宿主

  @AC-036 @MOBILE-009 @manual
  场景: AC-036 启动超时
    假如 模拟器启动后在期限内未完成 boot
    当 等待 boot 命令返回
    那么 返回超时及日志位置，保留模拟器供检查

  @AC-037 @MOBILE-010 @manual
  场景: AC-037 非 Mac iOS 安装
    假如 当前主机为 Linux 或原生 Windows
    当 请求本机 iOS simulator 安装
    那么 明确不支持，不报告安装完成

  @AC-038 @MOBILE-013 @manual
  场景: AC-038 WSL relay 回执丢失
    假如 Windows Appium 已收到输入但 relay 连接中断
    当 恢复 WSL 控制连接
    那么 不自动重发输入，要求新观察核对

  @AC-039 @NATIVE-003 @manual
  场景: AC-039 Windows 后台快捷键边界
    假如 后台窗口后端不支持目标 hotkey
    当 请求该组合键
    那么 返回不支持，前台窗口、鼠标和剪贴板不变

  @AC-040 @NATIVE-004 @manual
  场景: AC-040 截图失败不前台回退
    假如 Windows background 截图失败且 foreground 未授权
    当 执行 observe 和 diagnose
    那么 返回诊断，不能激活或还原窗口

  @AC-041 @NATIVE-005 @manual
  场景: AC-041 macOS 后台不抢焦点
    假如 隔离测试面板非前台且已授权辅助功能
    当 定向点击原生按钮并输入 Unicode
    那么 目标控件改变，前台 PID、指针和剪贴板保持

  @AC-042 @GUI-005 @manual
  场景: AC-042 无安全 keyring
    假如 选择记住 Key，但系统 keyring 不可用
    当 保存模型设置
    那么 明确失败或要求只存内存，磁盘没有明文 Key

  @AC-043 @GUI-006 @manual
  场景: AC-043 服务商错误脱敏
    假如 模型服务返回带回显 Token 的 401 body
    当 发起测试请求
    那么 界面显示认证错误，不显示 body 或 Token

  @AC-044 @GUI-008 @manual
  场景: AC-044 恢复循环有界
    假如 连续三次资源观察失败且无有效图像
    当 运行模型任务
    那么 转人工接管，不无限重试且不报告 done

  @AC-045 @GUI-009 @manual
  场景: AC-045 本机任务窗口行为
    假如 Windows 原生 GUI 已自动连接本机
    当 开始任务后请求人工接管
    那么 执行时 GUI 最小化，接管时恢复并显示指示

  @AC-046 @GUI-010 @manual
  场景: AC-046 应用清单约束
    假如 观察中应用清单仅包含测试应用 A
    当 模型请求启动不在清单中的入口 B
    那么 拒绝 B，不执行任意路径或命令

  @AC-047 @GUI-012 @manual
  场景: AC-047 闲置浏览器不阻塞
    假如 本机任务可用，浏览器绑定页休眠且尚未被模型选用
    当 开始本机任务
    那么 先观察本机，浏览器延迟加入观察循环

  @AC-048 @QA-006 @manual
  场景: AC-048 不可视断言
    假如 用例要求证明后台写入但没有 probe
    当 视觉模型仅看到完成页面
    那么 不能将后台写入标记为已验证 PASS

  @AC-049 @QA-007 @manual
  场景: AC-049 批量重复证据
    假如 两个不同断言的模型回复使用相同模板证据
    当 验证整个断言块
    那么 拒绝批量响应并提供逐条原因

  @AC-050 @QA-008 @manual
  场景: AC-050 现场弹窗重判
    假如 断言被测试页可关闭弹窗遮挡
    当 模型识别阻挡并尝试关闭后重判
    那么 保持当前现场，有界尝试；仍失败保留失败

  @AC-051 @PROBE-004 @manual
  场景: AC-051 延迟上报
    假如 probe 前两次无数据并返回 inconclusive，第三次 pass
    当 在预算内轮询
    那么 不把早期零行当失败，最终采纳插件证据

  @AC-052 @PROBE-008 @manual
  场景: AC-052 跳过检查标记
    假如 含 probe 的 case 以 --skip-probes 运行
    当 导出报告
    那么 probe 步为 skip 并列出未验证项，不能全部标 pass

  @AC-053 @CONFIG-001 @manual
  场景: AC-053 配置优先级
    假如 用户文件、项目文件和环境变量对同一键分别设置不同值
    当 加载配置
    那么 环境变量最终生效；其他未覆盖键仍从较低层继承

  @AC-054 @CONFIG-002 @manual
  场景: AC-054 显式配置缺失
    假如 SAYGO_CONFIG_FILE 指向不存在文件
    当 启动需要读取配置的入口
    那么 明确报错，不读取包目录中的其他 .env

  @AC-055 @INSTALL-001 @manual
  场景: AC-055 pipx 升级复用
    假如 安装包环境 0.4.12 已完成 setup
    当 升级相同 pipx 环境并重启 Agent
    那么 MCP 使用升级后的包，不要求重复 setup，不用旧复制运行时

  @AC-056 @INSTALL-004 @manual
  场景: AC-056 prepare-only 无副作用
    假如 已有客户端配置与浏览器 host 注册
    当 以临时 root 运行 prepare-only
    那么 只生成待安装文件，原配置和注册未变

  @AC-057 @INSTALL-005 @manual
  场景: AC-057 保留用户权限
    假如 客户端已有显式 deny/ask 及其他插件配置
    当 执行 Saygo setup
    那么 仅添加允许的 Saygo 设置，保留已有策略与备份

  @AC-058 @INSTALL-007 @manual
  场景: AC-058 开发用户隔离
    假如 全局用户插件已连接浏览器
    当 在 checkout 执行开发安装后从其他目录启动用户客户端
    那么 开发仅影响 checkout，其他目录继续使用用户包与原桥

  @AC-059 @INSTALL-009 @manual
  场景: AC-059 macOS 路径别名
    假如 同一安装目录可通过 /var 和 /private/var 访问
    当 分别执行首次和重复 setup
    那么 认出同一环境且复用，不因字符串路径不同误复制

  @AC-060 @RELEASE-001 @manual
  场景: AC-060 发布排除私密文件
    假如 源码树存在 .env、会话截图和私有客户测试
    当 构建源码 ZIP 与 wheel
    那么 归档不包含上述文件，仅包含白名单

  @AC-061 @RELEASE-005 @manual
  场景: AC-061 干净 wheel 验收
    假如 新建无 system-site-packages 的环境且 cwd 不在 checkout
    当 安装构建 wheel，运行 help、MCP 握手和重复 prepare-only
    那么 不借用仓库源码，资源完整，重复 setup 复用

  @AC-062 @RELEASE-006 @manual
  场景: AC-062 三平台验收
    假如 同一版本 wheel 与安装验收脚本已构建
    当 在 Linux、Windows、macOS 分别运行
    那么 分别留存结果；缺一平台不得写全平台通过

  @AC-063 @RELEASE-007 @manual
  场景: AC-063 发布状态分离
    假如 CI 成功且商店 submission 仍 pending review
    当 生成发布验收记录
    那么 分别列出产物、索引、提交和审核状态，不宣称已上线

  @AC-064 @OTHER-001 @manual
  场景: AC-064 设计稿参考
    假如 测试 Figma 节点或本地参考图可访问
    当 生成并执行带 ref 的视觉用例
    那么 保存参考图和当前截图，模型判定仍带证据

  @AC-065 @OTHER-003 @manual
  场景: AC-065 官网语言保持
    假如 首次打开官网选择中文
    当 刷新页面并访问安装文档链接
    那么 保留语言选择且链接指向 docs 中的有效说明

  @AC-066 @OTHER-008 @manual
  场景: AC-066 文档打包引用
    假如 普通说明已移至 docs，运行 Markdown 保留原位
    当 构建源码、wheel 与插件包并检查本地链接
    那么 包描述、发布 notes、插件文档链接均有效，Skill 加载路径不变
