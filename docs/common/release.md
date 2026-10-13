# 构建、安装验收与发布

[公共文档](README.md) · [发布需求](requirements.md#release) · [开发规范](../../AGENTS.md)

源码修改、构建、安装、发布和商店审核分别核实。commit/push 授权不等于升版授权；只有明确授权才修改版本、创建发布标签或发布。仅修验收脚本/CI 时保留原版本和标签，用修正后的检查验证原产物。

## 构建对象

| 对象 | 来源与产物 |
| --- | --- |
| Python 包 | pyproject.toml 与 distribution/release.json；sdist、wheel，内含允许分发的 setup 源码 ZIP |
| 托管安装 | scripts/build_release.py；源码 ZIP、校验和固定的版本安装器、清单和 SHA256SUMS |
| 扩展 | extensions/saygo-browser/manifest.json 独立版本；开发 ZIP 带 key，商店 ZIP 去掉开发 key |
| 桌面应用 | 目标 OS 原生构建；Windows ZIP、macOS DMG、Linux tar.gz 及各自 SHA256 |

白名单不得包含 .env、会话、截图、用户配置、客户测试或账号。扩展文件没变不因 Python 发布而跟随升版；扩展变更也仍需明确的版本授权。

## 本地构建与检查

```sh
python3 scripts/build_release.py --out dist/release
python3 scripts/build_release.py --extension-only --out dist/browser-store
python -m pip install build twine
python -m build --outdir dist/python
python -m twine check --strict dist/python/*
python scripts/check_python_package.py dist/python/saygo_agent_control-0.4.16-py3-none-any.whl
```

版本文件名为现有 0.4.16 示例，执行时匹配获授权的实际产物。默认 Python 构建先生成 sdist，再从 sdist 构建 wheel，确认源码包含全部输入。wheel 的 setup 源码 ZIP 包含安装器、插件、Skill 和扩展；仍需要联网下载 Python 依赖，不是离线包。

check_python_package.py 在仓库外创建不继承系统包的临时环境，安装 wheel，检查 CLI/setup 帮助、资源和 MCP 导入，以 prepare-only 准备客户端后重复 setup 验证环境复用。该过程不注册用户客户端，不操作设备，不证明真实客户端加载。Linux、Windows、macOS 必须分别执行；路径比较须处理 macOS /var 与 /private/var 等别名。

托管安装器的 `--prepare-only --client both --root /tmp/saygo-package-check` 可检查文件准备，不注册客户端/host。开发安装采用[项目隔离路径](installation.md#项目开发安装)。

桌面构建和冻结包检查见[桌面应用](desktop-app.md#实现与构建)，必须在目标 OS 完成，不能重命名其他平台产物冒充。

## 发布流程

获授权后，推送与 distribution/release.json 匹配的版本标签触发回归、GitHub 构建发布和商店提交。Python package 工作流独立执行构建及三平台安装检查后上传 PyPI。普通分支推送不上传 Python 包；手动 Build release 仅生成构建产物。

浏览器商店使用独立状态与凭据，见[商店材料](../browser-extension/store.md)。上传、提交审核、Google 批准和浏览器实际收到更新是不同状态，不能以流水线成功代替审核通过。

桌面构建通过后，运行“Publish verified desktop artifacts”，选择既有发布标签和对应桌面构建运行 ID。要求三个平台均成功且构建提交等于标签提交，核验各归档 SHA256 后附加文件，不重建、不覆盖已有附件。

## PyPI 发布者

项目为 saygo-agent-control。原记录中生产 Trusted Publisher 已配置，恢复配置时使用：

| 字段 | 值 |
| --- | --- |
| 项目 | saygo-agent-control |
| 所有者/仓库 | WilliamSkyWalker / saygo |
| 工作流 | python-package.yml |
| GitHub 环境 | pypi，测试发布使用独立 testpypi |

Trusted Publishing 使用 GitHub OIDC，不提交长期 API token。GitHub 环境若启用 required reviewers，生产上传会等待审批；是否使用审批由实际发布授权和仓库设置决定。

手动仅验收选择 `publish: none`。手动发布支持 testpypi/pypi，生产必须选匹配标签。若只修验证脚本，在修正分支运行 `release_tag: v0.4.16` 和对应 publish：回归及包构建使用标签，安装冒烟使用工作流分支的检查脚本。不能覆盖已有 PyPI 文件或移动标签。

参考 [PyPA Trusted Publishing](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)。

## 发布后验收

分别记录：

1. 标签提交、CI 实际运行范围、通过与跳过数量。
2. GitHub 公开 release、预期源码/安装器/扩展/桌面文件及摘要。
3. PyPI JSON 与 simple 索引的目标版本、未撤回文件、实际下载哈希及安装。
4. 商店上传/提交/审核/实际安装状态，禁止重复上传不确定结果。
5. 用户安装环境是否已升级，在线 host 是否仍运行旧代码；不能因源码或发布完成而宣称用户安装已更新。

```sh
# 在独立环境从公开包验证，不借用仓库导入。
pipx install 'saygo-agent-control[mcp]'
saygo setup --help
saygo setup --client codex
```

实际设备输入与浏览器测试使用隔离目录、命名会话、profile 和自有页面。部署前应完成可审查构建与验证；未具备设备、权限或依赖的项目记录为未执行。

公开版本的既有结果见[历史记录](history/README.md)，当前发布正文保留在[release-notes.md](release-notes.md)。文档整理不构成新发布。
