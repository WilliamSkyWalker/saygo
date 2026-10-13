# Android 操作

[文档入口](../README.md) · [本端完整需求](requirements.md) · [统一操作](../common/operations.md)

## 需求与前提

公共归属为 MOBILE、SESSION、OBS、TASK；本端全部细项见 [AND 需求清单](requirements.md)。视觉截图、触摸和输入使用 Appium + UiAutomator2；adb 用于发现和生命周期。MJPEG 帧超过 0.5 秒、无帧或解码失败时回落 Appium 截图；断流和停止立即清缓存。帧龄只约束采集缓存，不证明业务状态。

真机需开启 USB 调试、确认信任并解锁；Saygo 不绕过设备权限。连接现有手机不会默认清空数据或启动应用。Python 依赖选择 `mobile`；Appium 服务器还需完整 Android SDK，只有 platform-tools 的引导安装不等于 SDK 齐全。

## 发现与连接真机

```sh
saygo mcp init --skip-ios
saygo device list --platform android
saygo device connect --platform android --device DEVICE_ID --session phone
saygo device capabilities --session phone
saygo device screenshot --session phone
```

发现结果包含 `devices/android_avds/diagnostics`。未授权或离线设备仍会列出，但不自动选择。仅有一台在线设备时才可省略 `--device`；多个候选须指定，关机的模拟器须先 boot。

`--session` 是别名，与设备 ID 不同；已绑定其他设备或 Appium 服务器的别名不能覆盖。输入使用统一观察协议，完成后核验图像。

## 安装和启动模拟器

```sh
saygo device install --platform android --host auto --dry-run
saygo device install --platform android --host auto --name Saygo --boot --connect --session phone
saygo device boot --platform android Saygo
saygo device boot --platform android --host windows Saygo --connect --session phone
```

安装准备 Java（复用 17+ 或下载私有 Temurin JDK 21）、Android 命令行工具、platform-tools、平台/build-tools、模拟器、API 35 Google APIs 镜像、AVD 及隔离 Node/Appium/UiAutomator2。boot 等待 Android 启动完成，再连接并将验证截图保存到调用方运行目录。

计划显示主机、路径、组件、磁盘和加速阻塞；`--dry-run` 不下载或安装。需至少 12 GiB 空闲空间，下载通常数 GB。进度写 stderr，最终 JSON 写 stdout；下载/SDK 失败明确报错。Saygo 直接下载的归档校验 SHA256，Node 使用官方校验清单，部分 SDK 下载由 SDK Manager 管理。

先审阅并接受 [Android SDK 许可](https://developer.android.com/studio/terms)，无人值守安装需显式 `--accept-licenses`。`--api 36` 可选其他已发布镜像（安装器支持 API 30+），`--headless` 不显示模拟器窗口。不传 boot/connect 只安装；connect 隐含 boot。

优先复用 `ANDROID_HOME/ANDROID_SDK_ROOT` 或发现的 SDK，否则使用 `~/.saygo/runtime/android-sdk`。Java、Node、Appium 私有安装，不替换系统 Node/npm。AVD 使用 Android 配置/默认位置，同名同镜像复用，同名不同镜像拒绝覆盖。失败后可重试安装，boot 超时保留模拟器和 `~/.saygo/runtime/emulator-NAME.log` 供诊断。

安装器支持 x64 Linux/Windows、Intel/Apple silicon macOS，镜像 ABI 跟随主机。需预先启用 KVM、Windows Hypervisor Platform 或 Apple hypervisor；不自动改 BIOS 或重启。参见[加速要求](https://developer.android.com/studio/run/emulator-acceleration)。

## Windows 与 WSL 主机

WSL 没有可用 `/dev/kvm` 时，`--host auto` 选择 Windows；`--host local/windows` 显式覆盖。这是本机 WSL 互操作，不是任意远程安装。Windows 路径要求 x64 Windows、WSL 互操作和 PowerShell。

worker 在 `%LOCALAPPDATA%/Saygo/mobile` 安装私有嵌入 Python 和工具，优先复用 Windows SDK，否则放在该私有目录。不修改全局 PATH，只复制标准库 worker 源码，不复制项目配置或密钥。下载前检查加速；启用 Windows 功能、BIOS 或重启需要用户处理。

Windows Appium 仅监听 Windows 回环地址。带令牌的 WSL 回环转发通过 Windows Python stdio 通信，不改防火墙或镜像网络设置；失败请求不重放。私有 adb 使用独立持久端口并传给 Appium，避免争用默认 5037，不停止其他 adb 服务。

后台工具隐藏控制台，私有 Appium 预加载 Node 辅助程序隐藏 adb/logcat 子控制台；模拟器 GUI 保持可见。自动启动禁用模拟器统计/崩溃提示，错误写入日志。

Appium 和转发服务保留供后续命令复用；disconnect 结束 Appium 会话，不关闭模拟器/主机服务。重启后 boot/connect 重建连接；旧别名绑定旧服务器时使用新的明确别名。WSL 本地没有在线 Android 时，`device list` 会尝试 Windows worker 发现；Windows USB 是否可达仍需实际配置与授权。`device sessions` 只列保存绑定，不代表在线。

## 远程 Appium 与任务

```sh
saygo device connect --platform android --device DEVICE_ID --server-url http://windows-host.example:4723 --session phone
```

先在远端启动 Appium，提供可达地址和明确设备 ID，不用本地发现猜测远端设备。远端负责 USB、SDK 和模拟器；此命令不安装远程工具或自动开放网络服务。工作流资源使用：

```json
{"phone": {"kind": "android", "session": "phone"}}
```

## 验收与待办

```sh
python3 -m unittest discover -s tests/mobile_demo -v
```

离线测试模拟命令和 Appium，验证发现、选择、许可拒绝、前置检查、安装顺序、主机路由、会话身份、截图验证与传输失败，不是硬件通过。

原记录已实测 WSL→Windows 的 SDK/工具安装、API 35 模拟器启动、Appium 连接、截图、打开系统设置、坐标点击和搜索输入。隐藏控制台修复后做过 21 次 Windows helper 调用及独立 45 秒观察，未出现可见辅助控制台。其他主机、真机组合与完整跨端业务流程仍需单独验收。
