# BDD QA、用例与报告

[公共文档](README.md) · [QA 需求](requirements.md#qa) · [非视觉断言](probes.md)

QA 用于 .feature/.md 回归用例，独立于外部 Agent 的逐步设备任务。它使用自己的模型配置、测试目标、规划器和判定循环。无需预写步骤的跨端操作使用[统一任务](operations.md)，固定 JSON 流程使用[工作流](workflows.md)。

## 开始跑测

```sh
python3 -m pip install -e '.[qa,mobile]'
saygo init
# 在私有 .env 中配置模型和目标，密钥不要入库。
saygo run tests/my-app/login.feature --report
```

按目标选择 mobile、browser、selenium 等依赖。QA 浏览器保留 Selenium/本地/Grid 路径，与 MCP 的扩展后端限制分开。

```gherkin
# language: zh-CN
# saygo-platform: android
# saygo-package: com.example.app
功能: 登录入口
  @auto @android
  场景: 展示登录表单
    假如 应用已启动
    当 用户点击登录入口
    那么 邮箱和密码字段可见
```

## 用例与私有目标

Gherkin 支持 Feature/Background/Scenario/Scenario Outline/Examples 及中文关键字，参数化用例展开后执行。标签：

| 标签 | 语义 |
| --- | --- |
| @P0/@P1/@P2 | 优先级 |
| @auto/@partial/@manual | 自动化程度，后两类由自主 QA 跳过 |
| @skip/@wip | 跳过 |
| @android/@ios/@browser/@mac/@windows/@desktop/@rdp | 平台集合，只筛选，不切换驱动或自动双端运行 |
| @TC-XXX | 用例 ID |
| @reset:pm_clear、@reset:relaunch、@reset:none | Android 重置策略，覆盖文件默认值 |
| @ref:路径 或 saygo-ref 指令 | 参考图视觉走查 |

文件头使用 saygo-target/platform/package/reset-default 元数据，值后不写行内注释。Markdown 用例以 `### TC-XXX` 分块，使用 Priority/Reset before/Platform/Mode/Steps 字段。

私有目标放在 tests/目标/，公开 *_demo 与 _template 是例外。cases 存用例，_preconditions.md 提供恢复到前置态的说明，_accounts.json 提供账号池，reports 保存报告。真实账号用私有配置，公开用例使用 `${EMAIL}`、`${PASSWORD}` 等占位符；多设备按 worker 索引选择账号。当前账号不足会回退首账号，不能保证独占，见 [QA-019](requirements.md#qa)。

Selenium Grid 启动清理目前会遍历并删除服务器列出的已有会话，尚无本次任务所有权过滤；共享 Grid 场景不能宣称已隔离，见 [QA-022](requirements.md#qa)。QA 直接调用驱动的保护范围也不等同于 device/task，细项见[代码核对记录](requirements-audit.md)。

每条用例自包含：前置态写入 Background，进入子页需明确步骤，不依赖上一条用例结果。提示写方位而非固定坐标，Then 拆为独立可验证断言。锁屏、后台写入、埋点等不可视事实不能靠猜测判通过。

## 执行与证据

解析 → 渲染步骤与元数据 → planner 每用例一次规划 → agent 按步骤循环 → 失败分析 → HTML 报告。当前步骤索引必须匹配待执行步骤，模型不能自行跳步。

pass/fail 需至少 15 字符并引用屏幕元素的证据，fail 还需至少 10 字符原因；in_progress 必须给动作。连续三次响应校验拒绝收敛为失败，拒绝不派发、不占子动作额度，但计入循环与无进展计数。

默认 PER_STEP_SUB_ACTION_LIMIT=-1、AGENT_MAX_STEPS=0 禁用对应次数上限；主要无进展限制为 15 轮。主动等待预算内的 wait/probe 轮询不计无进展，AGENT_WAIT_MAX_S=45 为每步累计主动等待预算，不是整步总超时。

连续断言同步合并，逐条检查 verdict/evidence/where、重复证据和负向断言，整块通过后推进。probe 步不合并。文本证据校验是启发式检查，不能独立保证模型判断准确；不可视事实使用 probe 或明确未验证。

healer 只追加根因分类与建议，不修复应用、不修改原判定。失败后离开页面再异步补判的方案已否决。

## 模型、定位与性能

LLM_MODEL_BRAIN/PLANNER 留空回落 LLM_MODEL；LLM_MODEL_LOCATOR 留空关闭定位，定位端点/密钥可复用主模型。普通 tap/long_press 有 target 时定位成功可替换坐标，失败沿用原坐标；旧 no_effect 像素差重试路径已停用。

默认稳定帧采样结合像素差、状态栏 mask 与超时：操作用末帧，断言根据变化选静态一帧或动态最多三帧；不保证捕获所有短暂提示。参考图断言按用例明确启用。

AGENT_MERGE_ASSERTS=true 为同步断言合并；AGENT_SPLIT_ACT_CHECK=false 默认不启用批量操作。启用后拆原子动作、按需定位、下一轮视觉核验，连续两次序列失败回退普通路径，不等于零模型调用或以像素差证明成功。详见[性能实现与计划](performance.md)。

## 辅助工具与旧日志

Figma 用例生成和视觉审查保留 `saygo figma`；配置和模块见 [AGENTS.md](../../AGENTS.md) 及 [.env.example](../../.env.example)。

已移除旧 Claude 专用 saygo-drive Skill。日常操作使用[统一设备 Skill](../../plugins/saygo-device/skills/device/SKILL.md)，批量 QA 使用 saygo run；现有 journal 的报告渲染仍可用：

```sh
python3 -m saygo.drive.render --journal /path/to/journal.json --output /path/to/report.html
```

日志结构以 [render.py](../../saygo/drive/render.py) 为准，保留场景、逐步结果和截图；生成 HTML 不表示重新执行或重新验收用例。报告可能包含敏感输入和图像，不应放入公开发布包。
