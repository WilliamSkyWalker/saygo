# 安装、升级与客户端接入

[公共文档](README.md) · [需求基线](requirements.md#install)

适用 INSTALL、UPDATE、CONFIG。Saygo 提供 PyPI 包、独立托管安装器和项目开发安装；桌面应用另见[桌面指南](desktop-app.md)。外部 Agent 控制设备无需 Saygo 模型密钥，桌面模型与 QA 则需要各自配置。

## PyPI 安装

准备 Python 3.10+、pipx 和所选客户端 CLI：

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --client codex
# 可选 claude / both（Claude + Codex）/ qoder / qodercn / all
```

默认安装会解析当前兼容的 MCP SDK。若维护环境明确固定 `mcp==1.2.0`，须同时使用兼容的 Pydantic；发布检查验证的组合是 `pydantic==2.13.5`。Pydantic 2.14 删除了该旧 SDK 导入的私有接口，直接组合会在 SDK 导入阶段失败。

无需克隆仓库或手写 MCP 路径。setup 使用包内安装器、插件、共享 Skill 与扩展资源，MCP 直接绑定当前包的 Python 环境；客户端重启后加载工具，MCP 启动不下载依赖。

Codex/Claude 使用 `saygo-device@saygo-managed` 插件；Qoder/QoderCN 配置 MCP、Skill 和服务信任。管理文件默认在 `~/.local/share/saygo/agent-plugin`，会话和任务在 `~/.saygo`。可用 `--root PATH` 指定安装目录；`--prepare-only` 只准备文件，不注册客户端或 host。

浏览器安装 [Saygo Browser](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo)，在弹窗点击 Connect local bridge，再重启客户端。MCP 不支持 Playwright；`--install-browser` 仅为额外 CLI 工作安装 Playwright/Chromium。`--mobile` 增加移动 Python 依赖，Android/iOS 工具链及桌面权限仍需按各端指南准备。

不要同时启用旧 `saygo-device@saygo-plugins` 或手写的重复 Saygo MCP 服务。安装器保留无关配置，不替用户删除其他集成。

更新与卸载：

```sh
pipx upgrade saygo-agent-control
# 更新后重启 Agent；普通包升级不要求再次 setup。
saygo setup --uninstall
# 确认接入注册已清理后，可再删除 pipx 应用。
pipx uninstall saygo-agent-control
```

旧版复制运行时安装需要在升级到含修复的包后执行一次 `saygo setup --client ...` 迁移。新包启动 MCP 时准备新版 host 文件，已有连接继续运行直到用户重连，不主动断开扩展。卸载只删除本安装拥有且未被用户改动的注册，保留运行时、扩展文件、任务和截图；扩展本体通过浏览器删除。

## 项目开发安装

```sh
git clone https://github.com/WilliamSkyWalker/saygo.git
cd saygo
python3 scripts/install_development.py
```

原生 Windows 使用 `py -3`。开发安装只写当前项目的 `.codex/config.toml` 和 `.saygo-dev/`，在项目范围禁用用户 Saygo 插件，安装本地设备 Skill；开发入口拒绝在仓库外启动。状态在 `.saygo-dev/state`，不注册 native host、不改变商店扩展连接。其他目录继续使用用户插件。

直接 Python 开发也可在自己的隔离环境运行：

```sh
python3 -m pip install -e '.[mcp]'
saygo --help
saygo-mcp --profile device
```

按需选择 `mobile/windows/mac/desktop/browser/selenium/qa` 依赖。标识为 `saygo`、`saygo-device`、`~/.saygo`，不提供旧品牌兼容别名。不使用 pyenv。`--source` 不再将开发仓库装入全局用户插件；内部 `--package-python` 校验非 editable 发布包，普通用户不需传入。

## 独立 GitHub 安装器

此路径准备独立托管运行时，具有与 pipx 不同的更新通道。Python 3.10+ 与客户端已安装时，在可写目录执行：

```sh
curl -fL https://raw.githubusercontent.com/WilliamSkyWalker/saygo/main/scripts/install_saygo.py -o install-saygo.py && python3 install-saygo.py
```

Windows PowerShell：

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/WilliamSkyWalker/saygo/main/scripts/install_saygo.py -OutFile install-saygo.py -ErrorAction Stop
py -3 install-saygo.py
```

默认选择最新发布（含预发布），`--channel stable` 排除预发布，`--check` 只检查。安装器自动检测客户端，可显式 `--client`；其他选项包括 `--mobile`、`--browser edge/none`。

版本化安装器校验内嵌源码 ZIP 的 SHA256 后解压；也可将下载的匹配归档传给 `--archive`。依赖仍从 PyPI 获取，不是离线或完全锁定依赖包。WSL 另下载校验和固定的私有 Windows Python，并把扩展放到 Windows 文件系统，不要求用户在 Windows 手装 Python 或 Git。

运行时、桥和客户端配置的具体内容见[扩展指南](../browser-extension/README.md)。从解压开发扩展迁移商店扩展须显式覆盖 ID，由用户释放/禁用旧扩展再连接新扩展；不能自动重载正在工作的插件。

## 更新通知与托管升级

检查版本、通知用户、实际安装升级是三个独立动作。`automatic=false` 只关闭自动安装，不关闭检查与提醒。

| 安装模式 | 检查来源 | 升级方式 |
| --- | --- | --- |
| pipx/PyPI 包 | 公共 PyPI，稳定且有未撤回文件的版本 | 用户运行 pipx upgrade 并重启 Agent；Saygo 不替换包环境 |
| 独立托管安装器 | GitHub Releases，按 stable/beta 通道 | 默认只通知；可明确选择自动准备运行时，空闲启动时切换 |
| 源码开发 | 项目仓库 | 开发者更新代码与依赖，不切换托管指针 |
| 桌面应用 | 对应发布归档 | 手动下载，当前没有桌面自动更新 |

包模式每次 MCP 启动后台检查，device_sessions 也在缓存缺失、损坏、过期（24 小时）或版本不匹配时触发。首次可返回 `checking: true`，之后返回版本、链接、pipx 命令与重启提示。检查不阻塞 MCP、不写 stdout，同进程共用 worker，缓存原子写入。失败可保留已知新版并携带 error，checked_at 只是最近尝试时间。

`saygo update` 或 `saygo update --check` 强制包模式查询；`--auto off` 保持只提醒，`--apply/--auto on` 及托管通道选择会被拒绝并提示 pipx。升级后缓存按实际包版本比较，不再提醒同版/旧版。包检查不查询用户自定义 pip 索引。

独立托管安装默认 stable、只通知；可给安装器增加 `--auto-update --update-channel beta`。安装后管理：

```sh
python3 "$HOME/.local/share/saygo/agent-plugin/update.py" --check
python3 "$HOME/.local/share/saygo/agent-plugin/update.py" --auto on --channel beta
python3 "$HOME/.local/share/saygo/agent-plugin/update.py" --apply
python3 "$HOME/.local/share/saygo/agent-plugin/update.py" --auto off
```

Windows 用 py -3，自定义根目录须使用对应 update.py 并传 `--root PATH`。托管更新校验下载和源码摘要，准备并冒烟测试独立运行时，只在后续 MCP 启动且其他托管服务关闭、无未完成任务时激活。现有进程保留原环境；断网、下载失败或准备失败保留可用版本。旧运行时和 previous-runtime.json 不自动清理。

桥、扩展或 Skill 改动需完整安装，更新器只提示，不进行不完整升级。旧 0.4.0 安装需含更新启动器的版本做一次迁移。版本化安装器始终安装其指定版本。升级后现有会话保留，协议不匹配须更新两端；0.3.x 没有握手，不能假报连接成功。

托管卸载用其安装器 `--uninstall`，自定义根目录保持一致；只移除自身注册，不删其他安装的 host。

## 私有配置

优先级为：默认值 → `$SAYGO_HOME_DIR/config.env` → 工作项目 `.env` 或 `SAYGO_CONFIG_FILE` → 进程环境。显式配置文件缺失时报错，不搜索安装包目录。

`saygo init` / `saygo init --user` 创建项目/用户模板，不覆盖原文件，POSIX 权限仅所有者。安装器可接收 `--config-file /absolute/path/to/private.env`，只保存引用并在升级时保留，不复制密钥。另一个应用的数据库配置不会自动被 Saygo 消费。

## 客户端授权边界

安装器只配置 Saygo 范围，保留用户显式策略、无关配置与备份；沙箱、OS、组织策略或单工具覆盖仍可能要求确认。配置变化后重启客户端。

Codex 托管插件的服务级策略：

```toml
[plugins."saygo-device@saygo-managed".mcp_servers.saygo]
default_tools_approval_mode = "approve"
```

已存在表须合并，不能重复创建；直接 MCP 配置使用对应 `[mcp_servers.saygo]` 表。安装器只在没有显式服务策略时添加设置，尊重 CODEX_HOME，备份为 config.toml.before-saygo；卸载只删除自身未被修改的条目。恢复 prompt 可重新逐次确认，允许单个工具不等于允许全部工具。

- Claude：在用户 permissions.allow 中增加 `mcp__plugin_saygo-device_saygo__*` 与 `mcp__saygo__*`。
- Qoder：`~/.qoder/settings.json` 中配置 Saygo MCP 及 `trust: true`，共享 Skill 放在 `~/.qoder/skills/saygo-device/SKILL.md`。
- QoderCN：对应 `~/.qoder-cn`，使用 `--client qodercn`；这是 CLI 集成，不代表 IDE 已验收。

这些客户端设置备份为 settings.json.before-saygo，prepare-only 不修改。支持 CLAUDE_CONFIG_DIR、QODER_CONFIG_DIR、QODERCN_CONFIG_DIR；客户端启动时须使用同一目录。Qoder 可显式选择尚未加入 PATH 的客户端，自动检测也检查用户配置和私有 CLI 目录。

手动维护 Python 环境的旧 Claude marketplace 方式仍为 `/plugin marketplace add WilliamSkyWalker/saygo`、`/plugin install saygo-device@saygo-plugins`，但该方式不准备 Python 依赖。其他 MCP 客户端可启动 `saygo-mcp --profile device`。

参考：[Codex 插件](https://developers.openai.com/plugins/build/plugins)、[Claude 权限](https://code.claude.com/docs/en/permissions)、[Qoder MCP](https://docs.qoder.com/cli/mcp-reference)、[Qoder Skills](https://docs.qoder.com/cli/Skills)。

## 验收范围

[发布验收记录](history/README.md)分别保留 Linux/Windows/macOS 包安装、重复 setup、冻结包和浏览器测试。安装准备测试不等于真实客户端加载或业务操作；Qoder IDE、干净机器权限、商店首次安装等须单独验收。源码变化不会直接升级用户现有安装。
