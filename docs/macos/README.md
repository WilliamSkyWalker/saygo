# macOS 操作

[文档入口](../README.md) · [本端完整需求](requirements.md) · [统一操作](../common/operations.md)

## 需求与前提

适用 NATIVE-001、002、005～007 及 SESSION、OBS、TASK；桌面产品与整机模式还适用 GUI。编号和状态见[需求基线](../common/requirements.md#native)。

Python 环境安装 `mac` 扩展依赖，包含 ApplicationServices 的 PyObjC 绑定。向实际运行 Saygo 的进程授予屏幕录制和辅助功能权限，保持控制台解锁。安装包、模型和“重新检测本机”见[桌面应用](../common/desktop-app.md)。

## 前台窗口与整机连接

```sh
saygo device list --platform mac
saygo device connect --platform mac --app 'Example App' --session mac-test
saygo device capabilities --session mac-test
saygo device screenshot --session mac-test
```

前台驱动可能打开或前置应用。命名会话保存 PID 与窗口 ID；多窗口时须从 `device list` 选择并在连接时指定 `--window-id WINDOW_ID`。原窗口关闭或所属进程改变时拒绝操作，须显式选择新窗口；旧绑定没有窗口 ID 时也须重新连接。

Retina 截图像素与逻辑坐标可能不同，使用返回映射或百分比动作，不直接用截图像素估算。原生整机控制使用：

```sh
saygo device connect --platform desktop --desktop-scope computer --session local-computer
```

窗口和整机任务共用本地桌面锁，不能阻止人工或其他应用改变焦点。iOS 模拟器与真机另见 [iOS](../ios/README.md)。

## 后台模式

后台模式为实验功能。先手动打开目标应用，将窗口保留在当前桌面，再显式连接：

```sh
saygo device connect --platform mac --app 'Example App' --background --session mac-bg
# 有多个候选窗口时，从 device list 获取 ID，并增加 --window-id。
saygo device capabilities --session mac-bg
saygo device screenshot --session mac-bg
saygo device act '{"type":"tap","x":50,"y":40,"coordinate_space":"percent"}' --session mac-bg --observation-id OBSERVATION_ID --observe-after
```

MCP 使用 `device_connect(platform="mac", session="mac-bg", options={"app":"Example App","background":true})`。CLI、MCP、交互任务保存同一个后台标志、进程和窗口身份；新控制器必须回到原窗口，窗口消失后不能静默换绑。选择前台模式使用新会话，桌面连接对话框也提供后台选项。

后台截图不激活或启动应用。模型只看截图：坐标点击执行原生控件的 `AXPress`，右键需要 `AXShowMenu`。驱动仅在应用范围做坐标命中及有限窗口/祖先归属校验，不向模型返回控件树、控件文字或语义定位。不支持的自绘控件直接失败，不发送全局鼠标事件。

## 输入、滚动与限制

文字使用定向到进程的 Unicode 按键，不使用剪贴板。`input` 和无修饰键的 `press_key` 要求恰好一个合格应用窗口，且已有焦点控件属于该窗口。后台模式不会为聚焦输入框而激活应用。可打印文字走 input，控制键走 press_key。

快捷键、拖动、双击、悬停、长按和打开应用/URL 不支持；包括旧命令在内都不能回退为全局输入或前台操作。

滚动需要原生垂直滚动条。`scroll_at` 选择坐标下的区域，`scroll_up/down` 使用窗口中心。能力返回 `scroll_at_unit: native_steps`：正数向上、负数向下，优先调用原生增减动作；仅有可写归一化值时，每步改变 0.05 并限制在 [0,1]。这不保证对应固定像素或滚轮刻度。

锁屏/不活跃控制台、最小化/隐藏窗口、其他桌面 Space 及不明确的原生窗口映射都会被拒绝。应用回调仍可能自行激活，人工输入也可能竞争；操作期间前台或鼠标变化会报告结果不确定，不恢复焦点、不重放输入、不宣称成功。

## 验收

```sh
python3 -m unittest discover -s tests/control_demo -p test_mac_background.py -v
SAYGO_TEST_MAC_BACKGROUND=1 python3 -m unittest discover -s tests/mac_demo -p test_background_live.py -v
```

历史实测环境为 Intel Mac、macOS 12.7.6、Python 3.14.8：隔离原生面板通过后台按钮、中文/表情输入与删除、原生滚动；前台 PID、鼠标和剪贴板计数保持不变。独立 CLI 进程及 MCP stdio 的连接、观察、带观察动作共五项真实测试通过。测试只创建/关闭自有面板，不打开用户文档，输入断言期间应保持解锁且不移动鼠标。

该范围不覆盖任意应用、其他系统版本、最小化窗口或其他 Space。0.4.16 的 macOS arm64 DMG 与冻结包检查见[发布验收](../common/history/release-0.4.16.md)，不能替代用户机器的权限、真实 GUI 任务或 Intel 安装包验收；签名与公证仍未完成。
