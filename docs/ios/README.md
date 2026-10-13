# iOS 操作

[文档入口](../README.md) · [本端完整需求](requirements.md) · [统一操作](../common/operations.md)

## 需求与前提

适用 MOBILE-001～004、009、010、014 和 SESSION、OBS、TASK，见[需求基线](../common/requirements.md#mobile)。iOS 视觉操作使用 Appium + XCUITest；devicectl/simctl 用于设备发现与模拟器生命周期。

本地执行需要 macOS 和完整 Xcode，命令行工具目录须选择正确。Windows/Linux/WSL 不能本地安装或运行 iOS 模拟器，可连接已有远程 Mac Appium 服务。Python 安装选择 `mobile` 扩展依赖，工具初始化使用 `saygo mcp init`。

## 连接真机

```sh
saygo mcp init
saygo device list --platform ios
saygo device connect --platform ios --device DEVICE_UDID --session iphone
saygo device capabilities --session iphone
saygo device screenshot --session iphone
```

发现区分可用模拟器与已配对 iPhone/iPad；真机发现需要 Xcode devicectl。真机需信任电脑、开发者模式和有效的 Xcode 签名配置，按需设置 `IOS_TEAM_ID/IOS_WDA_BUNDLE_ID` 或传 `--team-id`。真实签名值只放本地私有配置。

截图前解锁设备。锁屏、休眠或拔线会使连接不可用，不能跳过权限或用旧图假装成功。连接不默认重置手机或启动应用。仅一个在线候选时才可省略 device；会话别名与 UDID 不同，不能覆盖其他设备/服务器的绑定。

## 安装与启动模拟器

```sh
saygo device install --platform ios --name Saygo --boot --connect
saygo device boot --platform ios SIMULATOR_UDID
```

安装流程执行 Xcode 首次初始化，通过 `xcodebuild -downloadPlatform iOS` 下载运行时，在最新可用运行时上创建或复用 iPhone 模拟器，选择运行时声明支持的设备类型，安装 Appium/XCUITest 后启动并连接。模拟器不需要真机 WDA 签名。

Xcode 本身、Apple 账号、许可接受或需管理员的首次组件安装可能需要用户处理；命令不承诺安装 Xcode，错误会直接返回。参见 [Apple 组件安装说明](https://developer.apple.com/documentation/xcode/downloading-and-installing-additional-xcode-components)。

boot 复用已启动的指定模拟器，返回成功须观察到启动就绪；超时保留设备供检查，不能暗中选择其他设备。后续操作与[统一观察和任务协议](../common/operations.md)相同。

## 远程 Mac

```sh
saygo device connect --platform ios --device DEVICE_UDID --server-url http://mac-host.example:4723 --session iphone
```

在 Mac 端先启动 Appium 并配置可达地址。远程连接必须指定设备 ID，服务器负责 USB、模拟器状态及签名；Saygo 客户端不安装远程工具、不从本地发现猜设备，也不自动将 Appium 暴露到网络。

工作流使用保存的同一别名：

```json
{"iphone": {"kind": "ios", "session": "iphone"}}
```

## 验收与待办

```sh
python3 -m unittest discover -s tests/mobile_demo -v
```

现有自动化通过模拟命令和 Appium 适配器覆盖发现、选择、安装编排及错误处理。原记录没有 iPhone 真机和完整 iOS 配置链的硬件验收证据；不能用 macOS 桌面测试、打包通过或 Android 模拟器通过替代。

待验收范围包括真机信任与签名、实际 XCUITest 会话、模拟器首次安装/复用、截图和输入、断连/恢复，以及指定应用的完整业务任务。具备设备与权限后按[人工验收场景](../common/testing/acceptance.feature)记录环境和实际结果。
