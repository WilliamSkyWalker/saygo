# language: zh-CN
# 由 scripts/render_requirement_cases.py 生成；请修改来源用例后重新生成。
# 每个场景对应一个独立命名的 unittest，不用场景大纲展开虚增数量。
功能: Saygo 全项目需求自动化契约

  @TC-0001 @OBS-003 @auto
  # 对应测试：test_TC_0001_coordinates
  场景: TC-0001 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0002 @OBS-003 @auto
  # 对应测试：test_TC_0002_coordinates
  场景: TC-0002 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0003 @OBS-003 @auto
  # 对应测试：test_TC_0003_coordinates
  场景: TC-0003 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0004 @OBS-003 @auto
  # 对应测试：test_TC_0004_coordinates
  场景: TC-0004 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0005 @OBS-003 @auto
  # 对应测试：test_TC_0005_coordinates
  场景: TC-0005 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0006 @OBS-003 @auto
  # 对应测试：test_TC_0006_coordinates
  场景: TC-0006 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0007 @OBS-003 @auto
  # 对应测试：test_TC_0007_coordinates
  场景: TC-0007 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0008 @OBS-003 @auto
  # 对应测试：test_TC_0008_coordinates
  场景: TC-0008 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "tap", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0009 @OBS-003 @auto
  # 对应测试：test_TC_0009_coordinates
  场景: TC-0009 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0010 @OBS-003 @auto
  # 对应测试：test_TC_0010_coordinates
  场景: TC-0010 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0011 @OBS-003 @auto
  # 对应测试：test_TC_0011_coordinates
  场景: TC-0011 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0012 @OBS-003 @auto
  # 对应测试：test_TC_0012_coordinates
  场景: TC-0012 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0013 @OBS-003 @auto
  # 对应测试：test_TC_0013_coordinates
  场景: TC-0013 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0014 @OBS-003 @auto
  # 对应测试：test_TC_0014_coordinates
  场景: TC-0014 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0015 @OBS-003 @auto
  # 对应测试：test_TC_0015_coordinates
  场景: TC-0015 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0016 @OBS-003 @auto
  # 对应测试：test_TC_0016_coordinates
  场景: TC-0016 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "hover", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0017 @OBS-003 @auto
  # 对应测试：test_TC_0017_coordinates
  场景: TC-0017 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0018 @OBS-003 @auto
  # 对应测试：test_TC_0018_coordinates
  场景: TC-0018 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0019 @OBS-003 @auto
  # 对应测试：test_TC_0019_coordinates
  场景: TC-0019 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0020 @OBS-003 @auto
  # 对应测试：test_TC_0020_coordinates
  场景: TC-0020 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0021 @OBS-003 @auto
  # 对应测试：test_TC_0021_coordinates
  场景: TC-0021 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0022 @OBS-003 @auto
  # 对应测试：test_TC_0022_coordinates
  场景: TC-0022 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0023 @OBS-003 @auto
  # 对应测试：test_TC_0023_coordinates
  场景: TC-0023 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0024 @OBS-003 @auto
  # 对应测试：test_TC_0024_coordinates
  场景: TC-0024 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "double_click", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0025 @OBS-003 @auto
  # 对应测试：test_TC_0025_coordinates
  场景: TC-0025 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0026 @OBS-003 @auto
  # 对应测试：test_TC_0026_coordinates
  场景: TC-0026 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0027 @OBS-003 @auto
  # 对应测试：test_TC_0027_coordinates
  场景: TC-0027 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0028 @OBS-003 @auto
  # 对应测试：test_TC_0028_coordinates
  场景: TC-0028 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0029 @OBS-003 @auto
  # 对应测试：test_TC_0029_coordinates
  场景: TC-0029 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0030 @OBS-003 @auto
  # 对应测试：test_TC_0030_coordinates
  场景: TC-0030 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0031 @OBS-003 @auto
  # 对应测试：test_TC_0031_coordinates
  场景: TC-0031 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0032 @OBS-003 @auto
  # 对应测试：test_TC_0032_coordinates
  场景: TC-0032 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "right_click", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0033 @OBS-003 @auto
  # 对应测试：test_TC_0033_coordinates
  场景: TC-0033 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0034 @OBS-003 @auto
  # 对应测试：test_TC_0034_coordinates
  场景: TC-0034 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0035 @OBS-003 @auto
  # 对应测试：test_TC_0035_coordinates
  场景: TC-0035 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0036 @OBS-003 @auto
  # 对应测试：test_TC_0036_coordinates
  场景: TC-0036 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0037 @OBS-003 @auto
  # 对应测试：test_TC_0037_coordinates
  场景: TC-0037 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0038 @OBS-003 @auto
  # 对应测试：test_TC_0038_coordinates
  场景: TC-0038 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0039 @OBS-003 @auto
  # 对应测试：test_TC_0039_coordinates
  场景: TC-0039 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0040 @OBS-003 @auto
  # 对应测试：test_TC_0040_coordinates
  场景: TC-0040 坐标映射
    假如 屏幕为 400×200，操作参数为 {"coordinate_space": "percent", "type": "long_press", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0041 @OBS-003 @auto
  # 对应测试：test_TC_0041_coordinates
  场景: TC-0041 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 0, "y": 0}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0042 @OBS-003 @auto
  # 对应测试：test_TC_0042_coordinates
  场景: TC-0042 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 100, "y": 100}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0043 @OBS-003 @auto
  # 对应测试：test_TC_0043_coordinates
  场景: TC-0043 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 50, "y": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0044 @OBS-003 @auto
  # 对应测试：test_TC_0044_coordinates
  场景: TC-0044 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 25, "y": 75}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0045 @OBS-003 @auto
  # 对应测试：test_TC_0045_coordinates
  场景: TC-0045 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 75, "y": 25}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0046 @OBS-003 @auto
  # 对应测试：test_TC_0046_coordinates
  场景: TC-0046 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 0.25, "y": 0.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0047 @OBS-003 @auto
  # 对应测试：test_TC_0047_coordinates
  场景: TC-0047 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 99.75, "y": 99.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0048 @OBS-003 @auto
  # 对应测试：test_TC_0048_coordinates
  场景: TC-0048 坐标映射
    假如 屏幕为 400×200，操作参数为 {"amount": -0.5, "coordinate_space": "percent", "type": "scroll_at", "x": 12.5, "y": 37.5}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0049 @OBS-003 @auto
  # 对应测试：test_TC_0049_coordinates
  场景: TC-0049 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 0, "x2_pct": 50, "y1_pct": 0, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (0, 0)，原始参数不被修改

  @TC-0050 @OBS-003 @auto
  # 对应测试：test_TC_0050_coordinates
  场景: TC-0050 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 100, "x2_pct": 50, "y1_pct": 100, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0051 @OBS-003 @auto
  # 对应测试：test_TC_0051_coordinates
  场景: TC-0051 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 50, "x2_pct": 50, "y1_pct": 50, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (200, 100)，原始参数不被修改

  @TC-0052 @OBS-003 @auto
  # 对应测试：test_TC_0052_coordinates
  场景: TC-0052 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 25, "x2_pct": 50, "y1_pct": 75, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (100, 150)，原始参数不被修改

  @TC-0053 @OBS-003 @auto
  # 对应测试：test_TC_0053_coordinates
  场景: TC-0053 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 75, "x2_pct": 50, "y1_pct": 25, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (300, 50)，原始参数不被修改

  @TC-0054 @OBS-003 @auto
  # 对应测试：test_TC_0054_coordinates
  场景: TC-0054 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 0.25, "x2_pct": 50, "y1_pct": 0.5, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (1, 1)，原始参数不被修改

  @TC-0055 @OBS-003 @auto
  # 对应测试：test_TC_0055_coordinates
  场景: TC-0055 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 99.75, "x2_pct": 50, "y1_pct": 99.5, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (399, 199)，原始参数不被修改

  @TC-0056 @OBS-003 @auto
  # 对应测试：test_TC_0056_coordinates
  场景: TC-0056 坐标映射
    假如 屏幕为 400×200，操作参数为 {"type": "swipe", "x1_pct": 12.5, "x2_pct": 50, "y1_pct": 37.5, "y2_pct": 50}
    当 准备操作但不派发输入
    那么 屏幕坐标为 (50, 75)，原始参数不被修改

  @TC-0057 @OBS-003 @auto
  # 对应测试：test_TC_0057_invalid_action
  场景: TC-0057 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0058 @OBS-003 @auto
  # 对应测试：test_TC_0058_invalid_action
  场景: TC-0058 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0059 @OBS-003 @auto
  # 对应测试：test_TC_0059_invalid_action
  场景: TC-0059 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0060 @OBS-003 @auto
  # 对应测试：test_TC_0060_invalid_action
  场景: TC-0060 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0061 @OBS-003 @auto
  # 对应测试：test_TC_0061_invalid_action
  场景: TC-0061 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0062 @OBS-003 @auto
  # 对应测试：test_TC_0062_invalid_action
  场景: TC-0062 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0063 @OBS-003 @auto
  # 对应测试：test_TC_0063_invalid_action
  场景: TC-0063 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0064 @OBS-003 @auto
  # 对应测试：test_TC_0064_invalid_action
  场景: TC-0064 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "tap", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0065 @OBS-003 @auto
  # 对应测试：test_TC_0065_invalid_action
  场景: TC-0065 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0066 @OBS-003 @auto
  # 对应测试：test_TC_0066_invalid_action
  场景: TC-0066 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0067 @OBS-003 @auto
  # 对应测试：test_TC_0067_invalid_action
  场景: TC-0067 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0068 @OBS-003 @auto
  # 对应测试：test_TC_0068_invalid_action
  场景: TC-0068 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0069 @OBS-003 @auto
  # 对应测试：test_TC_0069_invalid_action
  场景: TC-0069 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0070 @OBS-003 @auto
  # 对应测试：test_TC_0070_invalid_action
  场景: TC-0070 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0071 @OBS-003 @auto
  # 对应测试：test_TC_0071_invalid_action
  场景: TC-0071 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0072 @OBS-003 @auto
  # 对应测试：test_TC_0072_invalid_action
  场景: TC-0072 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "hover", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0073 @OBS-003 @auto
  # 对应测试：test_TC_0073_invalid_action
  场景: TC-0073 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0074 @OBS-003 @auto
  # 对应测试：test_TC_0074_invalid_action
  场景: TC-0074 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0075 @OBS-003 @auto
  # 对应测试：test_TC_0075_invalid_action
  场景: TC-0075 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0076 @OBS-003 @auto
  # 对应测试：test_TC_0076_invalid_action
  场景: TC-0076 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0077 @OBS-003 @auto
  # 对应测试：test_TC_0077_invalid_action
  场景: TC-0077 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0078 @OBS-003 @auto
  # 对应测试：test_TC_0078_invalid_action
  场景: TC-0078 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0079 @OBS-003 @auto
  # 对应测试：test_TC_0079_invalid_action
  场景: TC-0079 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0080 @OBS-003 @auto
  # 对应测试：test_TC_0080_invalid_action
  场景: TC-0080 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "double_click", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0081 @OBS-003 @auto
  # 对应测试：test_TC_0081_invalid_action
  场景: TC-0081 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0082 @OBS-003 @auto
  # 对应测试：test_TC_0082_invalid_action
  场景: TC-0082 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0083 @OBS-003 @auto
  # 对应测试：test_TC_0083_invalid_action
  场景: TC-0083 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0084 @OBS-003 @auto
  # 对应测试：test_TC_0084_invalid_action
  场景: TC-0084 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0085 @OBS-003 @auto
  # 对应测试：test_TC_0085_invalid_action
  场景: TC-0085 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0086 @OBS-003 @auto
  # 对应测试：test_TC_0086_invalid_action
  场景: TC-0086 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0087 @OBS-003 @auto
  # 对应测试：test_TC_0087_invalid_action
  场景: TC-0087 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0088 @OBS-003 @auto
  # 对应测试：test_TC_0088_invalid_action
  场景: TC-0088 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "right_click", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0089 @OBS-003 @auto
  # 对应测试：test_TC_0089_invalid_action
  场景: TC-0089 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0090 @OBS-003 @auto
  # 对应测试：test_TC_0090_invalid_action
  场景: TC-0090 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0091 @OBS-003 @auto
  # 对应测试：test_TC_0091_invalid_action
  场景: TC-0091 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0092 @OBS-003 @auto
  # 对应测试：test_TC_0092_invalid_action
  场景: TC-0092 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0093 @OBS-003 @auto
  # 对应测试：test_TC_0093_invalid_action
  场景: TC-0093 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0094 @OBS-003 @auto
  # 对应测试：test_TC_0094_invalid_action
  场景: TC-0094 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0095 @OBS-003 @auto
  # 对应测试：test_TC_0095_invalid_action
  场景: TC-0095 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0096 @OBS-003 @auto
  # 对应测试：test_TC_0096_invalid_action
  场景: TC-0096 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "long_press", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0097 @OBS-003 @auto
  # 对应测试：test_TC_0097_invalid_action
  场景: TC-0097 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": -1, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0098 @OBS-003 @auto
  # 对应测试：test_TC_0098_invalid_action
  场景: TC-0098 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": 100.01, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0099 @OBS-003 @auto
  # 对应测试：test_TC_0099_invalid_action
  场景: TC-0099 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": true, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0100 @OBS-003 @auto
  # 对应测试：test_TC_0100_invalid_action
  场景: TC-0100 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": false, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0101 @OBS-003 @auto
  # 对应测试：test_TC_0101_invalid_action
  场景: TC-0101 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": null, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0102 @OBS-003 @auto
  # 对应测试：test_TC_0102_invalid_action
  场景: TC-0102 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": "50", "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0103 @OBS-003 @auto
  # 对应测试：test_TC_0103_invalid_action
  场景: TC-0103 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": Infinity, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0104 @OBS-003 @auto
  # 对应测试：test_TC_0104_invalid_action
  场景: TC-0104 无效动作拒绝
    假如 屏幕为 400×200，操作参数为 {"amount": 1, "coordinate_space": "percent", "type": "scroll_at", "x": NaN, "y": 50}
    当 校验动作
    那么 拒绝输入且返回 ValueError

  @TC-0105 @OBS-008 @auto
  # 对应测试：test_TC_0105_invalid_action
  场景: TC-0105 无效动作拒绝
    假如 动作参数为 {"text": "", "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0106 @OBS-008 @auto
  # 对应测试：test_TC_0106_invalid_action
  场景: TC-0106 无效动作拒绝
    假如 动作参数为 {"text": null, "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0107 @OBS-008 @auto
  # 对应测试：test_TC_0107_invalid_action
  场景: TC-0107 无效动作拒绝
    假如 动作参数为 {"text": [], "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0108 @OBS-008 @auto
  # 对应测试：test_TC_0108_invalid_action
  场景: TC-0108 无效动作拒绝
    假如 动作参数为 {"text": {}, "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0109 @OBS-008 @auto
  # 对应测试：test_TC_0109_invalid_action
  场景: TC-0109 无效动作拒绝
    假如 动作参数为 {"text": 1, "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0110 @OBS-008 @auto
  # 对应测试：test_TC_0110_invalid_action
  场景: TC-0110 无效动作拒绝
    假如 动作参数为 {"text": false, "type": "input"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0111 @OBS-008 @auto
  # 对应测试：test_TC_0111_invalid_action
  场景: TC-0111 无效动作拒绝
    假如 动作参数为 {"key": "", "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0112 @OBS-008 @auto
  # 对应测试：test_TC_0112_invalid_action
  场景: TC-0112 无效动作拒绝
    假如 动作参数为 {"key": null, "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0113 @OBS-008 @auto
  # 对应测试：test_TC_0113_invalid_action
  场景: TC-0113 无效动作拒绝
    假如 动作参数为 {"key": [], "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0114 @OBS-008 @auto
  # 对应测试：test_TC_0114_invalid_action
  场景: TC-0114 无效动作拒绝
    假如 动作参数为 {"key": {}, "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0115 @OBS-008 @auto
  # 对应测试：test_TC_0115_invalid_action
  场景: TC-0115 无效动作拒绝
    假如 动作参数为 {"key": 1, "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0116 @OBS-008 @auto
  # 对应测试：test_TC_0116_invalid_action
  场景: TC-0116 无效动作拒绝
    假如 动作参数为 {"key": false, "type": "press_key"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0117 @OBS-008 @auto
  # 对应测试：test_TC_0117_invalid_action
  场景: TC-0117 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": ""}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0118 @OBS-008 @auto
  # 对应测试：test_TC_0118_invalid_action
  场景: TC-0118 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": null}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0119 @OBS-008 @auto
  # 对应测试：test_TC_0119_invalid_action
  场景: TC-0119 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": []}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0120 @OBS-008 @auto
  # 对应测试：test_TC_0120_invalid_action
  场景: TC-0120 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": {}}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0121 @OBS-008 @auto
  # 对应测试：test_TC_0121_invalid_action
  场景: TC-0121 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": 1}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0122 @OBS-008 @auto
  # 对应测试：test_TC_0122_invalid_action
  场景: TC-0122 无效动作拒绝
    假如 动作参数为 {"type": "open_url", "url": false}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0123 @OBS-008 @auto
  # 对应测试：test_TC_0123_invalid_action
  场景: TC-0123 无效动作拒绝
    假如 动作参数为 {"target": "", "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0124 @OBS-008 @auto
  # 对应测试：test_TC_0124_invalid_action
  场景: TC-0124 无效动作拒绝
    假如 动作参数为 {"target": null, "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0125 @OBS-008 @auto
  # 对应测试：test_TC_0125_invalid_action
  场景: TC-0125 无效动作拒绝
    假如 动作参数为 {"target": [], "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0126 @OBS-008 @auto
  # 对应测试：test_TC_0126_invalid_action
  场景: TC-0126 无效动作拒绝
    假如 动作参数为 {"target": {}, "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0127 @OBS-008 @auto
  # 对应测试：test_TC_0127_invalid_action
  场景: TC-0127 无效动作拒绝
    假如 动作参数为 {"target": 1, "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0128 @OBS-008 @auto
  # 对应测试：test_TC_0128_invalid_action
  场景: TC-0128 无效动作拒绝
    假如 动作参数为 {"target": false, "type": "open_app"}
    当 校验动作
    那么 因必需字段不是非空字符串而拒绝

  @TC-0129 @FLOW-001 @auto
  # 对应测试：test_TC_0129_workflow
  场景: TC-0129 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0130 @FLOW-003 @auto
  # 对应测试：test_TC_0130_workflow
  场景: TC-0130 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0131 @FLOW-003 @auto
  # 对应测试：test_TC_0131_workflow
  场景: TC-0131 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": ""}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0132 @FLOW-003 @auto
  # 对应测试：test_TC_0132_workflow
  场景: TC-0132 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": 123}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0133 @FLOW-001 @auto
  # 对应测试：test_TC_0133_workflow
  场景: TC-0133 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0134 @FLOW-001 @auto
  # 对应测试：test_TC_0134_workflow
  场景: TC-0134 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "android", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0135 @FLOW-001 @auto
  # 对应测试：test_TC_0135_workflow
  场景: TC-0135 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0136 @FLOW-001 @auto
  # 对应测试：test_TC_0136_workflow
  场景: TC-0136 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0137 @FLOW-001 @auto
  # 对应测试：test_TC_0137_workflow
  场景: TC-0137 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0138 @FLOW-001 @auto
  # 对应测试：test_TC_0138_workflow
  场景: TC-0138 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0139 @FLOW-001 @auto
  # 对应测试：test_TC_0139_workflow
  场景: TC-0139 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0140 @FLOW-001 @auto
  # 对应测试：test_TC_0140_workflow
  场景: TC-0140 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "android", "session": "fixture"}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0141 @FLOW-001 @auto
  # 对应测试：test_TC_0141_workflow
  场景: TC-0141 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0142 @FLOW-003 @auto
  # 对应测试：test_TC_0142_workflow
  场景: TC-0142 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0143 @FLOW-003 @auto
  # 对应测试：test_TC_0143_workflow
  场景: TC-0143 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": ""}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0144 @FLOW-003 @auto
  # 对应测试：test_TC_0144_workflow
  场景: TC-0144 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": 123}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0145 @FLOW-001 @auto
  # 对应测试：test_TC_0145_workflow
  场景: TC-0145 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0146 @FLOW-001 @auto
  # 对应测试：test_TC_0146_workflow
  场景: TC-0146 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "ios", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0147 @FLOW-001 @auto
  # 对应测试：test_TC_0147_workflow
  场景: TC-0147 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0148 @FLOW-001 @auto
  # 对应测试：test_TC_0148_workflow
  场景: TC-0148 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0149 @FLOW-001 @auto
  # 对应测试：test_TC_0149_workflow
  场景: TC-0149 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0150 @FLOW-001 @auto
  # 对应测试：test_TC_0150_workflow
  场景: TC-0150 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0151 @FLOW-001 @auto
  # 对应测试：test_TC_0151_workflow
  场景: TC-0151 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0152 @FLOW-001 @auto
  # 对应测试：test_TC_0152_workflow
  场景: TC-0152 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "ios", "session": "fixture"}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0153 @FLOW-001 @auto
  # 对应测试：test_TC_0153_workflow
  场景: TC-0153 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0154 @FLOW-003 @auto
  # 对应测试：test_TC_0154_workflow
  场景: TC-0154 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0155 @FLOW-003 @auto
  # 对应测试：test_TC_0155_workflow
  场景: TC-0155 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": ""}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0156 @FLOW-003 @auto
  # 对应测试：test_TC_0156_workflow
  场景: TC-0156 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": 123}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0157 @FLOW-001 @auto
  # 对应测试：test_TC_0157_workflow
  场景: TC-0157 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0158 @FLOW-001 @auto
  # 对应测试：test_TC_0158_workflow
  场景: TC-0158 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "browser", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0159 @FLOW-001 @auto
  # 对应测试：test_TC_0159_workflow
  场景: TC-0159 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0160 @FLOW-001 @auto
  # 对应测试：test_TC_0160_workflow
  场景: TC-0160 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0161 @FLOW-001 @auto
  # 对应测试：test_TC_0161_workflow
  场景: TC-0161 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0162 @FLOW-001 @auto
  # 对应测试：test_TC_0162_workflow
  场景: TC-0162 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0163 @FLOW-001 @auto
  # 对应测试：test_TC_0163_workflow
  场景: TC-0163 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0164 @FLOW-001 @auto
  # 对应测试：test_TC_0164_workflow
  场景: TC-0164 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "browser", "session": "fixture"}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0165 @FLOW-001 @auto
  # 对应测试：test_TC_0165_workflow
  场景: TC-0165 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0166 @FLOW-003 @auto
  # 对应测试：test_TC_0166_workflow
  场景: TC-0166 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0167 @FLOW-003 @auto
  # 对应测试：test_TC_0167_workflow
  场景: TC-0167 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": ""}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0168 @FLOW-003 @auto
  # 对应测试：test_TC_0168_workflow
  场景: TC-0168 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": 123}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0169 @FLOW-001 @auto
  # 对应测试：test_TC_0169_workflow
  场景: TC-0169 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0170 @FLOW-001 @auto
  # 对应测试：test_TC_0170_workflow
  场景: TC-0170 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "mac", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0171 @FLOW-001 @auto
  # 对应测试：test_TC_0171_workflow
  场景: TC-0171 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0172 @FLOW-001 @auto
  # 对应测试：test_TC_0172_workflow
  场景: TC-0172 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0173 @FLOW-001 @auto
  # 对应测试：test_TC_0173_workflow
  场景: TC-0173 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0174 @FLOW-001 @auto
  # 对应测试：test_TC_0174_workflow
  场景: TC-0174 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0175 @FLOW-001 @auto
  # 对应测试：test_TC_0175_workflow
  场景: TC-0175 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0176 @FLOW-001 @auto
  # 对应测试：test_TC_0176_workflow
  场景: TC-0176 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "mac", "session": "fixture"}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0177 @FLOW-001 @auto
  # 对应测试：test_TC_0177_workflow
  场景: TC-0177 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0178 @FLOW-003 @auto
  # 对应测试：test_TC_0178_workflow
  场景: TC-0178 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0179 @FLOW-003 @auto
  # 对应测试：test_TC_0179_workflow
  场景: TC-0179 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": ""}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0180 @FLOW-003 @auto
  # 对应测试：test_TC_0180_workflow
  场景: TC-0180 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": 123}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0181 @FLOW-001 @auto
  # 对应测试：test_TC_0181_workflow
  场景: TC-0181 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0182 @FLOW-001 @auto
  # 对应测试：test_TC_0182_workflow
  场景: TC-0182 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "windows", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0183 @FLOW-001 @auto
  # 对应测试：test_TC_0183_workflow
  场景: TC-0183 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0184 @FLOW-001 @auto
  # 对应测试：test_TC_0184_workflow
  场景: TC-0184 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0185 @FLOW-001 @auto
  # 对应测试：test_TC_0185_workflow
  场景: TC-0185 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0186 @FLOW-001 @auto
  # 对应测试：test_TC_0186_workflow
  场景: TC-0186 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0187 @FLOW-001 @auto
  # 对应测试：test_TC_0187_workflow
  场景: TC-0187 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0188 @FLOW-001 @auto
  # 对应测试：test_TC_0188_workflow
  场景: TC-0188 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "windows", "session": "fixture"}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0189 @FLOW-001 @auto
  # 对应测试：test_TC_0189_workflow
  场景: TC-0189 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 接受并返回独立副本

  @TC-0190 @FLOW-003 @auto
  # 对应测试：test_TC_0190_workflow
  场景: TC-0190 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0191 @FLOW-003 @auto
  # 对应测试：test_TC_0191_workflow
  场景: TC-0191 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0192 @FLOW-003 @auto
  # 对应测试：test_TC_0192_workflow
  场景: TC-0192 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": 123, "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0193 @FLOW-001 @auto
  # 对应测试：test_TC_0193_workflow
  场景: TC-0193 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "unsupported", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0194 @FLOW-001 @auto
  # 对应测试：test_TC_0194_workflow
  场景: TC-0194 工作流结构
    假如 工作流为 {"resources": {"../target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0195 @FLOW-001 @auto
  # 对应测试：test_TC_0195_workflow
  场景: TC-0195 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0196 @FLOW-001 @auto
  # 对应测试：test_TC_0196_workflow
  场景: TC-0196 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}, {"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0197 @FLOW-001 @auto
  # 对应测试：test_TC_0197_workflow
  场景: TC-0197 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"id": "shot", "kind": "observe", "resource": "missing"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0198 @FLOW-001 @auto
  # 对应测试：test_TC_0198_workflow
  场景: TC-0198 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 2}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0199 @FLOW-001 @auto
  # 对应测试：test_TC_0199_workflow
  场景: TC-0199 工作流结构
    假如 工作流为 {"inputs": [], "resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"actual": 1, "equals": 1, "id": "check", "kind": "check"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0200 @FLOW-001 @auto
  # 对应测试：test_TC_0200_workflow
  场景: TC-0200 工作流结构
    假如 工作流为 {"resources": {"target": {"kind": "sqlite", "path": "fixture.sqlite", "queries": {"lookup": "SELECT 1"}}}, "steps": [{"id": "act", "kind": "action", "resource": "target"}], "version": 1}
    当 验证工作流
    那么 拒绝并返回 ValueError

  @TC-0201 @FLOW-007 @auto
  # 对应测试：test_TC_0201_reference
  场景: TC-0201 引用与类型保持
    假如 上下文为 {"inputs": {"value": null}}
    当 解析精确引用 inputs.value
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0202 @FLOW-007 @auto
  # 对应测试：test_TC_0202_reference
  场景: TC-0202 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": null}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0203 @FLOW-007 @auto
  # 对应测试：test_TC_0203_reference
  场景: TC-0203 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0204 @FLOW-007 @auto
  # 对应测试：test_TC_0204_reference
  场景: TC-0204 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": null}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0205 @FLOW-007 @auto
  # 对应测试：test_TC_0205_reference
  场景: TC-0205 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": null}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0206 @FLOW-007 @auto
  # 对应测试：test_TC_0206_reference
  场景: TC-0206 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": null}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 null，保留 JSON 类型和副本隔离

  @TC-0207 @FLOW-007 @auto
  # 对应测试：test_TC_0207_reference
  场景: TC-0207 引用与类型保持
    假如 上下文为 {"inputs": {"value": false}}
    当 解析精确引用 inputs.value
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0208 @FLOW-007 @auto
  # 对应测试：test_TC_0208_reference
  场景: TC-0208 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": false}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0209 @FLOW-007 @auto
  # 对应测试：test_TC_0209_reference
  场景: TC-0209 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [false]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0210 @FLOW-007 @auto
  # 对应测试：test_TC_0210_reference
  场景: TC-0210 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": false}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0211 @FLOW-007 @auto
  # 对应测试：test_TC_0211_reference
  场景: TC-0211 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": false}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0212 @FLOW-007 @auto
  # 对应测试：test_TC_0212_reference
  场景: TC-0212 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": false}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 false，保留 JSON 类型和副本隔离

  @TC-0213 @FLOW-007 @auto
  # 对应测试：test_TC_0213_reference
  场景: TC-0213 引用与类型保持
    假如 上下文为 {"inputs": {"value": true}}
    当 解析精确引用 inputs.value
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0214 @FLOW-007 @auto
  # 对应测试：test_TC_0214_reference
  场景: TC-0214 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": true}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0215 @FLOW-007 @auto
  # 对应测试：test_TC_0215_reference
  场景: TC-0215 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [true]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0216 @FLOW-007 @auto
  # 对应测试：test_TC_0216_reference
  场景: TC-0216 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": true}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0217 @FLOW-007 @auto
  # 对应测试：test_TC_0217_reference
  场景: TC-0217 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": true}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0218 @FLOW-007 @auto
  # 对应测试：test_TC_0218_reference
  场景: TC-0218 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": true}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 true，保留 JSON 类型和副本隔离

  @TC-0219 @FLOW-007 @auto
  # 对应测试：test_TC_0219_reference
  场景: TC-0219 引用与类型保持
    假如 上下文为 {"inputs": {"value": 0}}
    当 解析精确引用 inputs.value
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0220 @FLOW-007 @auto
  # 对应测试：test_TC_0220_reference
  场景: TC-0220 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": 0}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0221 @FLOW-007 @auto
  # 对应测试：test_TC_0221_reference
  场景: TC-0221 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [0]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0222 @FLOW-007 @auto
  # 对应测试：test_TC_0222_reference
  场景: TC-0222 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": 0}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0223 @FLOW-007 @auto
  # 对应测试：test_TC_0223_reference
  场景: TC-0223 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": 0}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0224 @FLOW-007 @auto
  # 对应测试：test_TC_0224_reference
  场景: TC-0224 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": 0}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 0，保留 JSON 类型和副本隔离

  @TC-0225 @FLOW-007 @auto
  # 对应测试：test_TC_0225_reference
  场景: TC-0225 引用与类型保持
    假如 上下文为 {"inputs": {"value": -3}}
    当 解析精确引用 inputs.value
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0226 @FLOW-007 @auto
  # 对应测试：test_TC_0226_reference
  场景: TC-0226 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": -3}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0227 @FLOW-007 @auto
  # 对应测试：test_TC_0227_reference
  场景: TC-0227 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [-3]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0228 @FLOW-007 @auto
  # 对应测试：test_TC_0228_reference
  场景: TC-0228 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": -3}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0229 @FLOW-007 @auto
  # 对应测试：test_TC_0229_reference
  场景: TC-0229 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": -3}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0230 @FLOW-007 @auto
  # 对应测试：test_TC_0230_reference
  场景: TC-0230 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": -3}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 -3，保留 JSON 类型和副本隔离

  @TC-0231 @FLOW-007 @auto
  # 对应测试：test_TC_0231_reference
  场景: TC-0231 引用与类型保持
    假如 上下文为 {"inputs": {"value": 1.25}}
    当 解析精确引用 inputs.value
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0232 @FLOW-007 @auto
  # 对应测试：test_TC_0232_reference
  场景: TC-0232 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": 1.25}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0233 @FLOW-007 @auto
  # 对应测试：test_TC_0233_reference
  场景: TC-0233 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [1.25]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0234 @FLOW-007 @auto
  # 对应测试：test_TC_0234_reference
  场景: TC-0234 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": 1.25}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0235 @FLOW-007 @auto
  # 对应测试：test_TC_0235_reference
  场景: TC-0235 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": 1.25}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0236 @FLOW-007 @auto
  # 对应测试：test_TC_0236_reference
  场景: TC-0236 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": 1.25}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 1.25，保留 JSON 类型和副本隔离

  @TC-0237 @FLOW-007 @auto
  # 对应测试：test_TC_0237_reference
  场景: TC-0237 引用与类型保持
    假如 上下文为 {"inputs": {"value": "001"}}
    当 解析精确引用 inputs.value
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0238 @FLOW-007 @auto
  # 对应测试：test_TC_0238_reference
  场景: TC-0238 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": "001"}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0239 @FLOW-007 @auto
  # 对应测试：test_TC_0239_reference
  场景: TC-0239 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": ["001"]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0240 @FLOW-007 @auto
  # 对应测试：test_TC_0240_reference
  场景: TC-0240 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": "001"}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0241 @FLOW-007 @auto
  # 对应测试：test_TC_0241_reference
  场景: TC-0241 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": "001"}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0242 @FLOW-007 @auto
  # 对应测试：test_TC_0242_reference
  场景: TC-0242 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": "001"}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 "001"，保留 JSON 类型和副本隔离

  @TC-0243 @FLOW-007 @auto
  # 对应测试：test_TC_0243_reference
  场景: TC-0243 引用与类型保持
    假如 上下文为 {"inputs": {"value": "中文"}}
    当 解析精确引用 inputs.value
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0244 @FLOW-007 @auto
  # 对应测试：test_TC_0244_reference
  场景: TC-0244 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": "中文"}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0245 @FLOW-007 @auto
  # 对应测试：test_TC_0245_reference
  场景: TC-0245 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": ["中文"]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0246 @FLOW-007 @auto
  # 对应测试：test_TC_0246_reference
  场景: TC-0246 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": "中文"}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0247 @FLOW-007 @auto
  # 对应测试：test_TC_0247_reference
  场景: TC-0247 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": "中文"}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0248 @FLOW-007 @auto
  # 对应测试：test_TC_0248_reference
  场景: TC-0248 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": "中文"}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 "中文"，保留 JSON 类型和副本隔离

  @TC-0249 @FLOW-007 @auto
  # 对应测试：test_TC_0249_reference
  场景: TC-0249 引用与类型保持
    假如 上下文为 {"inputs": {"value": []}}
    当 解析精确引用 inputs.value
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0250 @FLOW-007 @auto
  # 对应测试：test_TC_0250_reference
  场景: TC-0250 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": []}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0251 @FLOW-007 @auto
  # 对应测试：test_TC_0251_reference
  场景: TC-0251 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [[]]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0252 @FLOW-007 @auto
  # 对应测试：test_TC_0252_reference
  场景: TC-0252 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": []}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0253 @FLOW-007 @auto
  # 对应测试：test_TC_0253_reference
  场景: TC-0253 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": []}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0254 @FLOW-007 @auto
  # 对应测试：test_TC_0254_reference
  场景: TC-0254 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": []}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 []，保留 JSON 类型和副本隔离

  @TC-0255 @FLOW-007 @auto
  # 对应测试：test_TC_0255_reference
  场景: TC-0255 引用与类型保持
    假如 上下文为 {"inputs": {"value": {"count": [1, null]}}}
    当 解析精确引用 inputs.value
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0256 @FLOW-007 @auto
  # 对应测试：test_TC_0256_reference
  场景: TC-0256 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"value": {"count": [1, null]}}}}
    当 解析精确引用 steps.lookup.value
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0257 @FLOW-007 @auto
  # 对应测试：test_TC_0257_reference
  场景: TC-0257 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"count": [1, null]}]}}}
    当 解析精确引用 steps.lookup.rows.0
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0258 @FLOW-007 @auto
  # 对应测试：test_TC_0258_reference
  场景: TC-0258 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [null, {"value": {"count": [1, null]}}]}}}
    当 解析精确引用 steps.lookup.rows.1.value
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0259 @FLOW-007 @auto
  # 对应测试：test_TC_0259_reference
  场景: TC-0259 引用与类型保持
    假如 上下文为 {"inputs": {"nested": {"value": {"count": [1, null]}}}}
    当 解析精确引用 inputs.nested.value
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0260 @FLOW-007 @auto
  # 对应测试：test_TC_0260_reference
  场景: TC-0260 引用与类型保持
    假如 上下文为 {"steps": {"lookup": {"rows": [{"value": {"count": [1, null]}}]}}}
    当 解析精确引用 steps.lookup.rows.0.value
    那么 返回 {"count": [1, null]}，保留 JSON 类型和副本隔离

  @TC-0261 @FLOW-007 @auto
  # 对应测试：test_TC_0261_missing_reference
  场景: TC-0261 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 'inputs.missing'
    那么 报告无法解析，不能替换为空值

  @TC-0262 @FLOW-007 @auto
  # 对应测试：test_TC_0262_missing_reference
  场景: TC-0262 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 'steps.lookup.rows.1'
    那么 报告无法解析，不能替换为空值

  @TC-0263 @FLOW-007 @auto
  # 对应测试：test_TC_0263_missing_reference
  场景: TC-0263 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 'steps.unknown'
    那么 报告无法解析，不能替换为空值

  @TC-0264 @FLOW-007 @auto
  # 对应测试：test_TC_0264_missing_reference
  场景: TC-0264 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 'steps.lookup.rows.bad'
    那么 报告无法解析，不能替换为空值

  @TC-0265 @FLOW-007 @auto
  # 对应测试：test_TC_0265_missing_reference
  场景: TC-0265 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 'inputs.value.x'
    那么 报告无法解析，不能替换为空值

  @TC-0266 @FLOW-007 @auto
  # 对应测试：test_TC_0266_missing_reference
  场景: TC-0266 缺失引用拒绝
    假如 上下文只有 inputs.value=1 与 steps.lookup.rows=[0]
    当 解析引用 ''
    那么 报告无法解析，不能替换为空值

  @TC-0267 @QA-002 @auto
  # 对应测试：test_TC_0267_gherkin
  场景: TC-0267 用例解析
    假如 Feature 含 Background 和一个带 @android @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0268 @QA-002 @auto
  # 对应测试：test_TC_0268_gherkin
  场景: TC-0268 用例解析
    假如 Feature 含 Background 和一个带 @android @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0269 @QA-002 @auto
  # 对应测试：test_TC_0269_gherkin
  场景: TC-0269 用例解析
    假如 Feature 含 Background 和一个带 @android @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0270 @QA-002 @auto
  # 对应测试：test_TC_0270_gherkin
  场景: TC-0270 用例解析
    假如 Feature 含 Background 和一个带 @android @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0271 @QA-002 @auto
  # 对应测试：test_TC_0271_gherkin
  场景: TC-0271 用例解析
    假如 Feature 含 Background 和一个带 @android @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0272 @QA-002 @auto
  # 对应测试：test_TC_0272_gherkin
  场景: TC-0272 用例解析
    假如 Feature 含 Background 和一个带 @android @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0273 @QA-002 @auto
  # 对应测试：test_TC_0273_gherkin
  场景: TC-0273 用例解析
    假如 Feature 含 Background 和一个带 @android @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0274 @QA-002 @auto
  # 对应测试：test_TC_0274_gherkin
  场景: TC-0274 用例解析
    假如 Feature 含 Background 和一个带 @android @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0275 @QA-002 @auto
  # 对应测试：test_TC_0275_gherkin
  场景: TC-0275 用例解析
    假如 Feature 含 Background 和一个带 @android @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0276 @QA-002 @auto
  # 对应测试：test_TC_0276_gherkin
  场景: TC-0276 用例解析
    假如 Feature 含 Background 和一个带 @ios @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0277 @QA-002 @auto
  # 对应测试：test_TC_0277_gherkin
  场景: TC-0277 用例解析
    假如 Feature 含 Background 和一个带 @ios @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0278 @QA-002 @auto
  # 对应测试：test_TC_0278_gherkin
  场景: TC-0278 用例解析
    假如 Feature 含 Background 和一个带 @ios @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0279 @QA-002 @auto
  # 对应测试：test_TC_0279_gherkin
  场景: TC-0279 用例解析
    假如 Feature 含 Background 和一个带 @ios @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0280 @QA-002 @auto
  # 对应测试：test_TC_0280_gherkin
  场景: TC-0280 用例解析
    假如 Feature 含 Background 和一个带 @ios @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0281 @QA-002 @auto
  # 对应测试：test_TC_0281_gherkin
  场景: TC-0281 用例解析
    假如 Feature 含 Background 和一个带 @ios @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0282 @QA-002 @auto
  # 对应测试：test_TC_0282_gherkin
  场景: TC-0282 用例解析
    假如 Feature 含 Background 和一个带 @ios @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0283 @QA-002 @auto
  # 对应测试：test_TC_0283_gherkin
  场景: TC-0283 用例解析
    假如 Feature 含 Background 和一个带 @ios @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0284 @QA-002 @auto
  # 对应测试：test_TC_0284_gherkin
  场景: TC-0284 用例解析
    假如 Feature 含 Background 和一个带 @ios @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0285 @QA-002 @auto
  # 对应测试：test_TC_0285_gherkin
  场景: TC-0285 用例解析
    假如 Feature 含 Background 和一个带 @browser @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0286 @QA-002 @auto
  # 对应测试：test_TC_0286_gherkin
  场景: TC-0286 用例解析
    假如 Feature 含 Background 和一个带 @browser @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0287 @QA-002 @auto
  # 对应测试：test_TC_0287_gherkin
  场景: TC-0287 用例解析
    假如 Feature 含 Background 和一个带 @browser @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0288 @QA-002 @auto
  # 对应测试：test_TC_0288_gherkin
  场景: TC-0288 用例解析
    假如 Feature 含 Background 和一个带 @browser @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0289 @QA-002 @auto
  # 对应测试：test_TC_0289_gherkin
  场景: TC-0289 用例解析
    假如 Feature 含 Background 和一个带 @browser @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0290 @QA-002 @auto
  # 对应测试：test_TC_0290_gherkin
  场景: TC-0290 用例解析
    假如 Feature 含 Background 和一个带 @browser @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0291 @QA-002 @auto
  # 对应测试：test_TC_0291_gherkin
  场景: TC-0291 用例解析
    假如 Feature 含 Background 和一个带 @browser @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0292 @QA-002 @auto
  # 对应测试：test_TC_0292_gherkin
  场景: TC-0292 用例解析
    假如 Feature 含 Background 和一个带 @browser @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0293 @QA-002 @auto
  # 对应测试：test_TC_0293_gherkin
  场景: TC-0293 用例解析
    假如 Feature 含 Background 和一个带 @browser @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0294 @QA-002 @auto
  # 对应测试：test_TC_0294_gherkin
  场景: TC-0294 用例解析
    假如 Feature 含 Background 和一个带 @web @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0295 @QA-002 @auto
  # 对应测试：test_TC_0295_gherkin
  场景: TC-0295 用例解析
    假如 Feature 含 Background 和一个带 @web @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0296 @QA-002 @auto
  # 对应测试：test_TC_0296_gherkin
  场景: TC-0296 用例解析
    假如 Feature 含 Background 和一个带 @web @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0297 @QA-002 @auto
  # 对应测试：test_TC_0297_gherkin
  场景: TC-0297 用例解析
    假如 Feature 含 Background 和一个带 @web @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0298 @QA-002 @auto
  # 对应测试：test_TC_0298_gherkin
  场景: TC-0298 用例解析
    假如 Feature 含 Background 和一个带 @web @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0299 @QA-002 @auto
  # 对应测试：test_TC_0299_gherkin
  场景: TC-0299 用例解析
    假如 Feature 含 Background 和一个带 @web @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0300 @QA-002 @auto
  # 对应测试：test_TC_0300_gherkin
  场景: TC-0300 用例解析
    假如 Feature 含 Background 和一个带 @web @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0301 @QA-002 @auto
  # 对应测试：test_TC_0301_gherkin
  场景: TC-0301 用例解析
    假如 Feature 含 Background 和一个带 @web @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0302 @QA-002 @auto
  # 对应测试：test_TC_0302_gherkin
  场景: TC-0302 用例解析
    假如 Feature 含 Background 和一个带 @web @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0303 @QA-002 @auto
  # 对应测试：test_TC_0303_gherkin
  场景: TC-0303 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0304 @QA-002 @auto
  # 对应测试：test_TC_0304_gherkin
  场景: TC-0304 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0305 @QA-002 @auto
  # 对应测试：test_TC_0305_gherkin
  场景: TC-0305 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0306 @QA-002 @auto
  # 对应测试：test_TC_0306_gherkin
  场景: TC-0306 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0307 @QA-002 @auto
  # 对应测试：test_TC_0307_gherkin
  场景: TC-0307 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0308 @QA-002 @auto
  # 对应测试：test_TC_0308_gherkin
  场景: TC-0308 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0309 @QA-002 @auto
  # 对应测试：test_TC_0309_gherkin
  场景: TC-0309 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0310 @QA-002 @auto
  # 对应测试：test_TC_0310_gherkin
  场景: TC-0310 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0311 @QA-002 @auto
  # 对应测试：test_TC_0311_gherkin
  场景: TC-0311 用例解析
    假如 Feature 含 Background 和一个带 @desktop @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0312 @QA-002 @auto
  # 对应测试：test_TC_0312_gherkin
  场景: TC-0312 用例解析
    假如 Feature 含 Background 和一个带 @mac @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0313 @QA-002 @auto
  # 对应测试：test_TC_0313_gherkin
  场景: TC-0313 用例解析
    假如 Feature 含 Background 和一个带 @mac @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0314 @QA-002 @auto
  # 对应测试：test_TC_0314_gherkin
  场景: TC-0314 用例解析
    假如 Feature 含 Background 和一个带 @mac @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0315 @QA-002 @auto
  # 对应测试：test_TC_0315_gherkin
  场景: TC-0315 用例解析
    假如 Feature 含 Background 和一个带 @mac @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0316 @QA-002 @auto
  # 对应测试：test_TC_0316_gherkin
  场景: TC-0316 用例解析
    假如 Feature 含 Background 和一个带 @mac @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0317 @QA-002 @auto
  # 对应测试：test_TC_0317_gherkin
  场景: TC-0317 用例解析
    假如 Feature 含 Background 和一个带 @mac @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0318 @QA-002 @auto
  # 对应测试：test_TC_0318_gherkin
  场景: TC-0318 用例解析
    假如 Feature 含 Background 和一个带 @mac @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0319 @QA-002 @auto
  # 对应测试：test_TC_0319_gherkin
  场景: TC-0319 用例解析
    假如 Feature 含 Background 和一个带 @mac @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0320 @QA-002 @auto
  # 对应测试：test_TC_0320_gherkin
  场景: TC-0320 用例解析
    假如 Feature 含 Background 和一个带 @mac @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0321 @QA-002 @auto
  # 对应测试：test_TC_0321_gherkin
  场景: TC-0321 用例解析
    假如 Feature 含 Background 和一个带 @windows @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0322 @QA-002 @auto
  # 对应测试：test_TC_0322_gherkin
  场景: TC-0322 用例解析
    假如 Feature 含 Background 和一个带 @windows @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0323 @QA-002 @auto
  # 对应测试：test_TC_0323_gherkin
  场景: TC-0323 用例解析
    假如 Feature 含 Background 和一个带 @windows @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0324 @QA-002 @auto
  # 对应测试：test_TC_0324_gherkin
  场景: TC-0324 用例解析
    假如 Feature 含 Background 和一个带 @windows @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0325 @QA-002 @auto
  # 对应测试：test_TC_0325_gherkin
  场景: TC-0325 用例解析
    假如 Feature 含 Background 和一个带 @windows @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0326 @QA-002 @auto
  # 对应测试：test_TC_0326_gherkin
  场景: TC-0326 用例解析
    假如 Feature 含 Background 和一个带 @windows @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0327 @QA-002 @auto
  # 对应测试：test_TC_0327_gherkin
  场景: TC-0327 用例解析
    假如 Feature 含 Background 和一个带 @windows @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0328 @QA-002 @auto
  # 对应测试：test_TC_0328_gherkin
  场景: TC-0328 用例解析
    假如 Feature 含 Background 和一个带 @windows @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0329 @QA-002 @auto
  # 对应测试：test_TC_0329_gherkin
  场景: TC-0329 用例解析
    假如 Feature 含 Background 和一个带 @windows @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0330 @QA-002 @auto
  # 对应测试：test_TC_0330_gherkin
  场景: TC-0330 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P0 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0331 @QA-002 @auto
  # 对应测试：test_TC_0331_gherkin
  场景: TC-0331 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P0 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0332 @QA-002 @auto
  # 对应测试：test_TC_0332_gherkin
  场景: TC-0332 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P0 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0333 @QA-002 @auto
  # 对应测试：test_TC_0333_gherkin
  场景: TC-0333 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P1 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0334 @QA-002 @auto
  # 对应测试：test_TC_0334_gherkin
  场景: TC-0334 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P1 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0335 @QA-002 @auto
  # 对应测试：test_TC_0335_gherkin
  场景: TC-0335 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P1 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0336 @QA-002 @auto
  # 对应测试：test_TC_0336_gherkin
  场景: TC-0336 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P2 @auto 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0337 @QA-002 @auto
  # 对应测试：test_TC_0337_gherkin
  场景: TC-0337 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P2 @partial 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0338 @QA-002 @auto
  # 对应测试：test_TC_0338_gherkin
  场景: TC-0338 用例解析
    假如 Feature 含 Background 和一个带 @rdp @P2 @manual 的场景
    当 解析并渲染场景
    那么 保留三个标签的独立语义、Background 和 When/Then 顺序

  @TC-0339 @QA-003 @auto
  # 对应测试：test_TC_0339_progress
  场景: TC-0339 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0340 @QA-003 @auto
  # 对应测试：test_TC_0340_progress
  场景: TC-0340 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0341 @QA-003 @auto
  # 对应测试：test_TC_0341_progress
  场景: TC-0341 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0342 @QA-003 @auto
  # 对应测试：test_TC_0342_progress
  场景: TC-0342 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0343 @QA-003 @auto
  # 对应测试：test_TC_0343_progress
  场景: TC-0343 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 0, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0344 @QA-003 @auto
  # 对应测试：test_TC_0344_progress
  场景: TC-0344 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0345 @QA-003 @auto
  # 对应测试：test_TC_0345_progress
  场景: TC-0345 步骤进度校验
    假如 共 12 步，待执行第 1 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0346 @QA-003 @auto
  # 对应测试：test_TC_0346_progress
  场景: TC-0346 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0347 @QA-003 @auto
  # 对应测试：test_TC_0347_progress
  场景: TC-0347 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0348 @QA-003 @auto
  # 对应测试：test_TC_0348_progress
  场景: TC-0348 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0349 @QA-003 @auto
  # 对应测试：test_TC_0349_progress
  场景: TC-0349 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0350 @QA-003 @auto
  # 对应测试：test_TC_0350_progress
  场景: TC-0350 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 1, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0351 @QA-003 @auto
  # 对应测试：test_TC_0351_progress
  场景: TC-0351 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0352 @QA-003 @auto
  # 对应测试：test_TC_0352_progress
  场景: TC-0352 步骤进度校验
    假如 共 12 步，待执行第 2 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0353 @QA-003 @auto
  # 对应测试：test_TC_0353_progress
  场景: TC-0353 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0354 @QA-003 @auto
  # 对应测试：test_TC_0354_progress
  场景: TC-0354 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0355 @QA-003 @auto
  # 对应测试：test_TC_0355_progress
  场景: TC-0355 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0356 @QA-003 @auto
  # 对应测试：test_TC_0356_progress
  场景: TC-0356 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0357 @QA-003 @auto
  # 对应测试：test_TC_0357_progress
  场景: TC-0357 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 2, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0358 @QA-003 @auto
  # 对应测试：test_TC_0358_progress
  场景: TC-0358 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0359 @QA-003 @auto
  # 对应测试：test_TC_0359_progress
  场景: TC-0359 步骤进度校验
    假如 共 12 步，待执行第 3 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0360 @QA-003 @auto
  # 对应测试：test_TC_0360_progress
  场景: TC-0360 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0361 @QA-003 @auto
  # 对应测试：test_TC_0361_progress
  场景: TC-0361 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0362 @QA-003 @auto
  # 对应测试：test_TC_0362_progress
  场景: TC-0362 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0363 @QA-003 @auto
  # 对应测试：test_TC_0363_progress
  场景: TC-0363 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0364 @QA-003 @auto
  # 对应测试：test_TC_0364_progress
  场景: TC-0364 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 3, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0365 @QA-003 @auto
  # 对应测试：test_TC_0365_progress
  场景: TC-0365 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0366 @QA-003 @auto
  # 对应测试：test_TC_0366_progress
  场景: TC-0366 步骤进度校验
    假如 共 12 步，待执行第 4 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0367 @QA-003 @auto
  # 对应测试：test_TC_0367_progress
  场景: TC-0367 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0368 @QA-003 @auto
  # 对应测试：test_TC_0368_progress
  场景: TC-0368 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0369 @QA-003 @auto
  # 对应测试：test_TC_0369_progress
  场景: TC-0369 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0370 @QA-003 @auto
  # 对应测试：test_TC_0370_progress
  场景: TC-0370 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0371 @QA-003 @auto
  # 对应测试：test_TC_0371_progress
  场景: TC-0371 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 4, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0372 @QA-003 @auto
  # 对应测试：test_TC_0372_progress
  场景: TC-0372 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0373 @QA-003 @auto
  # 对应测试：test_TC_0373_progress
  场景: TC-0373 步骤进度校验
    假如 共 12 步，待执行第 5 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0374 @QA-003 @auto
  # 对应测试：test_TC_0374_progress
  场景: TC-0374 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0375 @QA-003 @auto
  # 对应测试：test_TC_0375_progress
  场景: TC-0375 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0376 @QA-003 @auto
  # 对应测试：test_TC_0376_progress
  场景: TC-0376 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0377 @QA-003 @auto
  # 对应测试：test_TC_0377_progress
  场景: TC-0377 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0378 @QA-003 @auto
  # 对应测试：test_TC_0378_progress
  场景: TC-0378 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 5, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0379 @QA-003 @auto
  # 对应测试：test_TC_0379_progress
  场景: TC-0379 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0380 @QA-003 @auto
  # 对应测试：test_TC_0380_progress
  场景: TC-0380 步骤进度校验
    假如 共 12 步，待执行第 6 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0381 @QA-003 @auto
  # 对应测试：test_TC_0381_progress
  场景: TC-0381 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0382 @QA-003 @auto
  # 对应测试：test_TC_0382_progress
  场景: TC-0382 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0383 @QA-003 @auto
  # 对应测试：test_TC_0383_progress
  场景: TC-0383 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0384 @QA-003 @auto
  # 对应测试：test_TC_0384_progress
  场景: TC-0384 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0385 @QA-003 @auto
  # 对应测试：test_TC_0385_progress
  场景: TC-0385 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 6, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0386 @QA-003 @auto
  # 对应测试：test_TC_0386_progress
  场景: TC-0386 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0387 @QA-003 @auto
  # 对应测试：test_TC_0387_progress
  场景: TC-0387 步骤进度校验
    假如 共 12 步，待执行第 7 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0388 @QA-003 @auto
  # 对应测试：test_TC_0388_progress
  场景: TC-0388 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0389 @QA-003 @auto
  # 对应测试：test_TC_0389_progress
  场景: TC-0389 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0390 @QA-003 @auto
  # 对应测试：test_TC_0390_progress
  场景: TC-0390 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0391 @QA-003 @auto
  # 对应测试：test_TC_0391_progress
  场景: TC-0391 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0392 @QA-003 @auto
  # 对应测试：test_TC_0392_progress
  场景: TC-0392 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 7, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0393 @QA-003 @auto
  # 对应测试：test_TC_0393_progress
  场景: TC-0393 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0394 @QA-003 @auto
  # 对应测试：test_TC_0394_progress
  场景: TC-0394 步骤进度校验
    假如 共 12 步，待执行第 8 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0395 @QA-003 @auto
  # 对应测试：test_TC_0395_progress
  场景: TC-0395 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0396 @QA-003 @auto
  # 对应测试：test_TC_0396_progress
  场景: TC-0396 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0397 @QA-003 @auto
  # 对应测试：test_TC_0397_progress
  场景: TC-0397 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0398 @QA-003 @auto
  # 对应测试：test_TC_0398_progress
  场景: TC-0398 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0399 @QA-003 @auto
  # 对应测试：test_TC_0399_progress
  场景: TC-0399 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 8, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0400 @QA-003 @auto
  # 对应测试：test_TC_0400_progress
  场景: TC-0400 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0401 @QA-003 @auto
  # 对应测试：test_TC_0401_progress
  场景: TC-0401 步骤进度校验
    假如 共 12 步，待执行第 9 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0402 @QA-003 @auto
  # 对应测试：test_TC_0402_progress
  场景: TC-0402 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0403 @QA-003 @auto
  # 对应测试：test_TC_0403_progress
  场景: TC-0403 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "fail", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。", "fail_reason": "目标输入框未显示预期内容，需要检查当前页面状态"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0404 @QA-003 @auto
  # 对应测试：test_TC_0404_progress
  场景: TC-0404 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "in_progress", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 接受当前步骤判定

  @TC-0405 @QA-003 @auto
  # 对应测试：test_TC_0405_progress
  场景: TC-0405 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 11, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0406 @QA-003 @auto
  # 对应测试：test_TC_0406_progress
  场景: TC-0406 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 9, "current_step_status": "pass", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0407 @QA-003 @auto
  # 对应测试：test_TC_0407_progress
  场景: TC-0407 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "pass", "evidence": "已完成"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0408 @QA-003 @auto
  # 对应测试：test_TC_0408_progress
  场景: TC-0408 步骤进度校验
    假如 共 12 步，待执行第 10 步，模型返回 {"action": {"type": "wait"}, "step_progress": {"current_step_index": 10, "current_step_status": "success", "evidence": "屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。"}}
    当 验证步骤进度
    那么 拒绝且不能推进或派发动作

  @TC-0409 @PROBE-001 @auto
  # 对应测试：test_TC_0409_probe
  场景: TC-0409 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=0 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=0 且类型保持，enabled=true

  @TC-0410 @PROBE-001 @auto
  # 对应测试：test_TC_0410_probe
  场景: TC-0410 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=0 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=0 且类型保持，enabled=true

  @TC-0411 @PROBE-001 @auto
  # 对应测试：test_TC_0411_probe
  场景: TC-0411 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=0 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=0 且类型保持，enabled=true

  @TC-0412 @PROBE-001 @auto
  # 对应测试：test_TC_0412_probe
  场景: TC-0412 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=0 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=0 且类型保持，enabled=true

  @TC-0413 @PROBE-001 @auto
  # 对应测试：test_TC_0413_probe
  场景: TC-0413 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=-3 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=-3 且类型保持，enabled=true

  @TC-0414 @PROBE-001 @auto
  # 对应测试：test_TC_0414_probe
  场景: TC-0414 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=-3 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=-3 且类型保持，enabled=true

  @TC-0415 @PROBE-001 @auto
  # 对应测试：test_TC_0415_probe
  场景: TC-0415 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=-3 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=-3 且类型保持，enabled=true

  @TC-0416 @PROBE-001 @auto
  # 对应测试：test_TC_0416_probe
  场景: TC-0416 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=-3 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=-3 且类型保持，enabled=true

  @TC-0417 @PROBE-001 @auto
  # 对应测试：test_TC_0417_probe
  场景: TC-0417 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=1.25 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=1.25 且类型保持，enabled=true

  @TC-0418 @PROBE-001 @auto
  # 对应测试：test_TC_0418_probe
  场景: TC-0418 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=1.25 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=1.25 且类型保持，enabled=true

  @TC-0419 @PROBE-001 @auto
  # 对应测试：test_TC_0419_probe
  场景: TC-0419 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=1.25 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=1.25 且类型保持，enabled=true

  @TC-0420 @PROBE-001 @auto
  # 对应测试：test_TC_0420_probe
  场景: TC-0420 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=1.25 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=1.25 且类型保持，enabled=true

  @TC-0421 @PROBE-001 @auto
  # 对应测试：test_TC_0421_probe
  场景: TC-0421 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=true enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=true 且类型保持，enabled=true

  @TC-0422 @PROBE-001 @auto
  # 对应测试：test_TC_0422_probe
  场景: TC-0422 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=true enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=true 且类型保持，enabled=true

  @TC-0423 @PROBE-001 @auto
  # 对应测试：test_TC_0423_probe
  场景: TC-0423 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=true enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=true 且类型保持，enabled=true

  @TC-0424 @PROBE-001 @auto
  # 对应测试：test_TC_0424_probe
  场景: TC-0424 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=true enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=true 且类型保持，enabled=true

  @TC-0425 @PROBE-001 @auto
  # 对应测试：test_TC_0425_probe
  场景: TC-0425 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=FALSE enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=false 且类型保持，enabled=true

  @TC-0426 @PROBE-001 @auto
  # 对应测试：test_TC_0426_probe
  场景: TC-0426 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=FALSE enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=false 且类型保持，enabled=true

  @TC-0427 @PROBE-001 @auto
  # 对应测试：test_TC_0427_probe
  场景: TC-0427 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=FALSE enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=false 且类型保持，enabled=true

  @TC-0428 @PROBE-001 @auto
  # 对应测试：test_TC_0428_probe
  场景: TC-0428 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=FALSE enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=false 且类型保持，enabled=true

  @TC-0429 @PROBE-001 @auto
  # 对应测试：test_TC_0429_probe
  场景: TC-0429 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=null enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=null 且类型保持，enabled=true

  @TC-0430 @PROBE-001 @auto
  # 对应测试：test_TC_0430_probe
  场景: TC-0430 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=null enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=null 且类型保持，enabled=true

  @TC-0431 @PROBE-001 @auto
  # 对应测试：test_TC_0431_probe
  场景: TC-0431 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=null enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=null 且类型保持，enabled=true

  @TC-0432 @PROBE-001 @auto
  # 对应测试：test_TC_0432_probe
  场景: TC-0432 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=null enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=null 且类型保持，enabled=true

  @TC-0433 @PROBE-001 @auto
  # 对应测试：test_TC_0433_probe
  场景: TC-0433 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=007 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="007" 且类型保持，enabled=true

  @TC-0434 @PROBE-001 @auto
  # 对应测试：test_TC_0434_probe
  场景: TC-0434 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=007 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="007" 且类型保持，enabled=true

  @TC-0435 @PROBE-001 @auto
  # 对应测试：test_TC_0435_probe
  场景: TC-0435 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=007 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="007" 且类型保持，enabled=true

  @TC-0436 @PROBE-001 @auto
  # 对应测试：test_TC_0436_probe
  场景: TC-0436 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=007 enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="007" 且类型保持，enabled=true

  @TC-0437 @PROBE-001 @auto
  # 对应测试：test_TC_0437_probe
  场景: TC-0437 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=\"hello world\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="hello world" 且类型保持，enabled=true

  @TC-0438 @PROBE-001 @auto
  # 对应测试：test_TC_0438_probe
  场景: TC-0438 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=\"hello world\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="hello world" 且类型保持，enabled=true

  @TC-0439 @PROBE-001 @auto
  # 对应测试：test_TC_0439_probe
  场景: TC-0439 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=\"hello world\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="hello world" 且类型保持，enabled=true

  @TC-0440 @PROBE-001 @auto
  # 对应测试：test_TC_0440_probe
  场景: TC-0440 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=\"hello world\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="hello world" 且类型保持，enabled=true

  @TC-0441 @PROBE-001 @auto
  # 对应测试：test_TC_0441_probe
  场景: TC-0441 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=\"中文\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="中文" 且类型保持，enabled=true

  @TC-0442 @PROBE-001 @auto
  # 对应测试：test_TC_0442_probe
  场景: TC-0442 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=\"中文\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="中文" 且类型保持，enabled=true

  @TC-0443 @PROBE-001 @auto
  # 对应测试：test_TC_0443_probe
  场景: TC-0443 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=\"中文\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="中文" 且类型保持，enabled=true

  @TC-0444 @PROBE-001 @auto
  # 对应测试：test_TC_0444_probe
  场景: TC-0444 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=\"中文\" enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="中文" 且类型保持，enabled=true

  @TC-0445 @PROBE-001 @auto
  # 对应测试：test_TC_0445_probe
  场景: TC-0445 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=[1, false, null] enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=[1, false, null] 且类型保持，enabled=true

  @TC-0446 @PROBE-001 @auto
  # 对应测试：test_TC_0446_probe
  场景: TC-0446 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=[1, false, null] enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=[1, false, null] 且类型保持，enabled=true

  @TC-0447 @PROBE-001 @auto
  # 对应测试：test_TC_0447_probe
  场景: TC-0447 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=[1, false, null] enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=[1, false, null] 且类型保持，enabled=true

  @TC-0448 @PROBE-001 @auto
  # 对应测试：test_TC_0448_probe
  场景: TC-0448 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=[1, false, null] enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value=[1, false, null] 且类型保持，enabled=true

  @TC-0449 @PROBE-001 @auto
  # 对应测试：test_TC_0449_probe
  场景: TC-0449 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value={\"name\":\"a b\"} enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value={"name": "a b"} 且类型保持，enabled=true

  @TC-0450 @PROBE-001 @auto
  # 对应测试：test_TC_0450_probe
  场景: TC-0450 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value={\"name\":\"a b\"} enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value={"name": "a b"} 且类型保持，enabled=true

  @TC-0451 @PROBE-001 @auto
  # 对应测试：test_TC_0451_probe
  场景: TC-0451 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value={\"name\":\"a b\"} enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value={"name": "a b"} 且类型保持，enabled=true

  @TC-0452 @PROBE-001 @auto
  # 对应测试：test_TC_0452_probe
  场景: TC-0452 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value={\"name\":\"a b\"} enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value={"name": "a b"} 且类型保持，enabled=true

  @TC-0453 @PROBE-001 @auto
  # 对应测试：test_TC_0453_probe
  场景: TC-0453 非视觉断言声明
    假如 步骤后声明 "# saygo-probe: fixture value=plain enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="plain" 且类型保持，enabled=true

  @TC-0454 @PROBE-001 @auto
  # 对应测试：test_TC_0454_probe
  场景: TC-0454 非视觉断言声明
    假如 步骤后声明 "  # saygo-probe: fixture value=plain enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="plain" 且类型保持，enabled=true

  @TC-0455 @PROBE-001 @auto
  # 对应测试：test_TC_0455_probe
  场景: TC-0455 非视觉断言声明
    假如 步骤后声明 "\t#saygo-probe: fixture value=plain enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="plain" 且类型保持，enabled=true

  @TC-0456 @PROBE-001 @auto
  # 对应测试：test_TC_0456_probe
  场景: TC-0456 非视觉断言声明
    假如 步骤后声明 "#  saygo-probe: fixture value=plain enabled"
    当 解析指令并检测 case 是否包含 probe
    那么 插件名 fixture，value="plain" 且类型保持，enabled=true

  @TC-0457 @GUI-004 @auto
  # 对应测试：test_TC_0457_model_url
  场景: TC-0457 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1", "model": "vision-model"}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0458 @GUI-004 @auto
  # 对应测试：test_TC_0458_model_url
  场景: TC-0458 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1", "model": " 模型 "}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0459 @GUI-004 @auto
  # 对应测试：test_TC_0459_model_url
  场景: TC-0459 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com:8443/v1/", "model": "vision-model"}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0460 @GUI-004 @auto
  # 对应测试：test_TC_0460_model_url
  场景: TC-0460 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com:8443/v1/", "model": " 模型 "}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0461 @GUI-004 @auto
  # 对应测试：test_TC_0461_model_url
  场景: TC-0461 模型地址校验
    假如 模型配置为 {"base_url": "http://localhost:8080/v1", "model": "vision-model"}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0462 @GUI-004 @auto
  # 对应测试：test_TC_0462_model_url
  场景: TC-0462 模型地址校验
    假如 模型配置为 {"base_url": "http://localhost:8080/v1", "model": " 模型 "}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0463 @GUI-004 @auto
  # 对应测试：test_TC_0463_model_url
  场景: TC-0463 模型地址校验
    假如 模型配置为 {"base_url": "http://127.0.0.1:8080/v1", "model": "vision-model"}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0464 @GUI-004 @auto
  # 对应测试：test_TC_0464_model_url
  场景: TC-0464 模型地址校验
    假如 模型配置为 {"base_url": "http://127.0.0.1:8080/v1", "model": " 模型 "}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0465 @GUI-004 @auto
  # 对应测试：test_TC_0465_model_url
  场景: TC-0465 模型地址校验
    假如 模型配置为 {"base_url": "http://[::1]:8080/v1", "model": "vision-model"}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0466 @GUI-004 @auto
  # 对应测试：test_TC_0466_model_url
  场景: TC-0466 模型地址校验
    假如 模型配置为 {"base_url": "http://[::1]:8080/v1", "model": " 模型 "}
    当 校验模型配置
    那么 接受并规范化空白及尾斜线

  @TC-0467 @GUI-004 @auto
  # 对应测试：test_TC_0467_model_url
  场景: TC-0467 模型地址校验
    假如 模型配置为 {"base_url": "http://example.com/v1", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0468 @GUI-004 @auto
  # 对应测试：test_TC_0468_model_url
  场景: TC-0468 模型地址校验
    假如 模型配置为 {"base_url": "http://example.com/v1", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0469 @GUI-004 @auto
  # 对应测试：test_TC_0469_model_url
  场景: TC-0469 模型地址校验
    假如 模型配置为 {"base_url": "https://user:secret@example.com/v1", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0470 @GUI-004 @auto
  # 对应测试：test_TC_0470_model_url
  场景: TC-0470 模型地址校验
    假如 模型配置为 {"base_url": "https://user:secret@example.com/v1", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0471 @GUI-004 @auto
  # 对应测试：test_TC_0471_model_url
  场景: TC-0471 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1?key=secret", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0472 @GUI-004 @auto
  # 对应测试：test_TC_0472_model_url
  场景: TC-0472 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1?key=secret", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0473 @GUI-004 @auto
  # 对应测试：test_TC_0473_model_url
  场景: TC-0473 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1#secret", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0474 @GUI-004 @auto
  # 对应测试：test_TC_0474_model_url
  场景: TC-0474 模型地址校验
    假如 模型配置为 {"base_url": "https://example.com/v1#secret", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0475 @GUI-004 @auto
  # 对应测试：test_TC_0475_model_url
  场景: TC-0475 模型地址校验
    假如 模型配置为 {"base_url": "file:///tmp/model", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0476 @GUI-004 @auto
  # 对应测试：test_TC_0476_model_url
  场景: TC-0476 模型地址校验
    假如 模型配置为 {"base_url": "file:///tmp/model", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0477 @GUI-004 @auto
  # 对应测试：test_TC_0477_model_url
  场景: TC-0477 模型地址校验
    假如 模型配置为 {"base_url": "https:///v1", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0478 @GUI-004 @auto
  # 对应测试：test_TC_0478_model_url
  场景: TC-0478 模型地址校验
    假如 模型配置为 {"base_url": "https:///v1", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0479 @GUI-004 @auto
  # 对应测试：test_TC_0479_model_url
  场景: TC-0479 模型地址校验
    假如 模型配置为 {"base_url": "ftp://example.com/v1", "model": "vision-model"}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0480 @GUI-004 @auto
  # 对应测试：test_TC_0480_model_url
  场景: TC-0480 模型地址校验
    假如 模型配置为 {"base_url": "ftp://example.com/v1", "model": " 模型 "}
    当 校验模型配置
    那么 在发出请求前拒绝不安全的地址

  @TC-0481 @BROWSER-002 @auto
  # 对应测试：test_TC_0481_backend
  场景: TC-0481 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": null, "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0482 @BROWSER-002 @auto
  # 对应测试：test_TC_0482_backend
  场景: TC-0482 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": null, "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0483 @BROWSER-002 @auto
  # 对应测试：test_TC_0483_backend
  场景: TC-0483 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": null, "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0484 @BROWSER-002 @auto
  # 对应测试：test_TC_0484_backend
  场景: TC-0484 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": "extension", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0485 @BROWSER-002 @auto
  # 对应测试：test_TC_0485_backend
  场景: TC-0485 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": "extension", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0486 @BROWSER-002 @auto
  # 对应测试：test_TC_0486_backend
  场景: TC-0486 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": "extension", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0487 @BROWSER-002 @auto
  # 对应测试：test_TC_0487_backend
  场景: TC-0487 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": "playwright", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0488 @BROWSER-002 @auto
  # 对应测试：test_TC_0488_backend
  场景: TC-0488 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": "playwright", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0489 @BROWSER-002 @auto
  # 对应测试：test_TC_0489_backend
  场景: TC-0489 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": "playwright", "kind": "browser"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0490 @BROWSER-002 @auto
  # 对应测试：test_TC_0490_backend
  场景: TC-0490 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": null, "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0491 @BROWSER-002 @auto
  # 对应测试：test_TC_0491_backend
  场景: TC-0491 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": null, "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0492 @BROWSER-002 @auto
  # 对应测试：test_TC_0492_backend
  场景: TC-0492 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": null, "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0493 @BROWSER-002 @auto
  # 对应测试：test_TC_0493_backend
  场景: TC-0493 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": "extension", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0494 @BROWSER-002 @auto
  # 对应测试：test_TC_0494_backend
  场景: TC-0494 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": "extension", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0495 @BROWSER-002 @auto
  # 对应测试：test_TC_0495_backend
  场景: TC-0495 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": "extension", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0496 @BROWSER-002 @auto
  # 对应测试：test_TC_0496_backend
  场景: TC-0496 后端访问限制
    假如 保存绑定和请求后端为 {"backend": null, "state": {"browser_backend": "playwright", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0497 @BROWSER-002 @auto
  # 对应测试：test_TC_0497_backend
  场景: TC-0497 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "extension", "state": {"browser_backend": "playwright", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 允许进入操作层

  @TC-0498 @BROWSER-002 @auto
  # 对应测试：test_TC_0498_backend
  场景: TC-0498 后端访问限制
    假如 保存绑定和请求后端为 {"backend": "playwright", "state": {"browser_backend": "playwright", "kind": "android"}}
    当 通过 MCP 检查后端策略
    那么 在操作前拒绝 Playwright 并提示扩展后端

  @TC-0499 @UPDATE-001 @auto
  # 对应测试：test_TC_0499_update_notice
  场景: TC-0499 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0500 @UPDATE-001 @auto
  # 对应测试：test_TC_0500_update_notice
  场景: TC-0500 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0501 @UPDATE-001 @auto
  # 对应测试：test_TC_0501_update_notice
  场景: TC-0501 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0502 @UPDATE-001 @auto
  # 对应测试：test_TC_0502_update_notice
  场景: TC-0502 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0503 @UPDATE-001 @auto
  # 对应测试：test_TC_0503_update_notice
  场景: TC-0503 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.4.13；automatic=false 并使用 pipx 升级说明

  @TC-0504 @UPDATE-001 @auto
  # 对应测试：test_TC_0504_update_notice
  场景: TC-0504 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.4.13；automatic=false 并使用 pipx 升级说明

  @TC-0505 @UPDATE-001 @auto
  # 对应测试：test_TC_0505_update_notice
  场景: TC-0505 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0506 @UPDATE-001 @auto
  # 对应测试：test_TC_0506_update_notice
  场景: TC-0506 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0507 @UPDATE-001 @auto
  # 对应测试：test_TC_0507_update_notice
  场景: TC-0507 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0508 @UPDATE-001 @auto
  # 对应测试：test_TC_0508_update_notice
  场景: TC-0508 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0509 @UPDATE-001 @auto
  # 对应测试：test_TC_0509_update_notice
  场景: TC-0509 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0510 @UPDATE-001 @auto
  # 对应测试：test_TC_0510_update_notice
  场景: TC-0510 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.4.12", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0511 @UPDATE-001 @auto
  # 对应测试：test_TC_0511_update_notice
  场景: TC-0511 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0512 @UPDATE-001 @auto
  # 对应测试：test_TC_0512_update_notice
  场景: TC-0512 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0513 @UPDATE-001 @auto
  # 对应测试：test_TC_0513_update_notice
  场景: TC-0513 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0514 @UPDATE-001 @auto
  # 对应测试：test_TC_0514_update_notice
  场景: TC-0514 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0515 @UPDATE-001 @auto
  # 对应测试：test_TC_0515_update_notice
  场景: TC-0515 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0516 @UPDATE-001 @auto
  # 对应测试：test_TC_0516_update_notice
  场景: TC-0516 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0517 @UPDATE-001 @auto
  # 对应测试：test_TC_0517_update_notice
  场景: TC-0517 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0518 @UPDATE-001 @auto
  # 对应测试：test_TC_0518_update_notice
  场景: TC-0518 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0519 @UPDATE-001 @auto
  # 对应测试：test_TC_0519_update_notice
  场景: TC-0519 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0520 @UPDATE-001 @auto
  # 对应测试：test_TC_0520_update_notice
  场景: TC-0520 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0521 @UPDATE-001 @auto
  # 对应测试：test_TC_0521_update_notice
  场景: TC-0521 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0522 @UPDATE-001 @auto
  # 对应测试：test_TC_0522_update_notice
  场景: TC-0522 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.4.13", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0523 @UPDATE-001 @auto
  # 对应测试：test_TC_0523_update_notice
  场景: TC-0523 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0524 @UPDATE-001 @auto
  # 对应测试：test_TC_0524_update_notice
  场景: TC-0524 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0525 @UPDATE-001 @auto
  # 对应测试：test_TC_0525_update_notice
  场景: TC-0525 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0526 @UPDATE-001 @auto
  # 对应测试：test_TC_0526_update_notice
  场景: TC-0526 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0527 @UPDATE-001 @auto
  # 对应测试：test_TC_0527_update_notice
  场景: TC-0527 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0528 @UPDATE-001 @auto
  # 对应测试：test_TC_0528_update_notice
  场景: TC-0528 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0529 @UPDATE-001 @auto
  # 对应测试：test_TC_0529_update_notice
  场景: TC-0529 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0530 @UPDATE-001 @auto
  # 对应测试：test_TC_0530_update_notice
  场景: TC-0530 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；automatic=false 并使用 pipx 升级说明

  @TC-0531 @UPDATE-001 @auto
  # 对应测试：test_TC_0531_update_notice
  场景: TC-0531 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0532 @UPDATE-001 @auto
  # 对应测试：test_TC_0532_update_notice
  场景: TC-0532 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0533 @UPDATE-001 @auto
  # 对应测试：test_TC_0533_update_notice
  场景: TC-0533 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0534 @UPDATE-001 @auto
  # 对应测试：test_TC_0534_update_notice
  场景: TC-0534 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.9.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0535 @UPDATE-001 @auto
  # 对应测试：test_TC_0535_update_notice
  场景: TC-0535 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0536 @UPDATE-001 @auto
  # 对应测试：test_TC_0536_update_notice
  场景: TC-0536 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0537 @UPDATE-001 @auto
  # 对应测试：test_TC_0537_update_notice
  场景: TC-0537 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0538 @UPDATE-001 @auto
  # 对应测试：test_TC_0538_update_notice
  场景: TC-0538 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0539 @UPDATE-001 @auto
  # 对应测试：test_TC_0539_update_notice
  场景: TC-0539 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0540 @UPDATE-001 @auto
  # 对应测试：test_TC_0540_update_notice
  场景: TC-0540 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0541 @UPDATE-001 @auto
  # 对应测试：test_TC_0541_update_notice
  场景: TC-0541 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0542 @UPDATE-001 @auto
  # 对应测试：test_TC_0542_update_notice
  场景: TC-0542 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0543 @UPDATE-001 @auto
  # 对应测试：test_TC_0543_update_notice
  场景: TC-0543 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0544 @UPDATE-001 @auto
  # 对应测试：test_TC_0544_update_notice
  场景: TC-0544 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；automatic=false 并使用 pipx 升级说明

  @TC-0545 @UPDATE-001 @auto
  # 对应测试：test_TC_0545_update_notice
  场景: TC-0545 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0546 @UPDATE-001 @auto
  # 对应测试：test_TC_0546_update_notice
  场景: TC-0546 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "1.0.0", "mode": "package"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；automatic=false 并使用 pipx 升级说明

  @TC-0547 @UPDATE-001 @auto
  # 对应测试：test_TC_0547_update_notice
  场景: TC-0547 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0548 @UPDATE-001 @auto
  # 对应测试：test_TC_0548_update_notice
  场景: TC-0548 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0549 @UPDATE-001 @auto
  # 对应测试：test_TC_0549_update_notice
  场景: TC-0549 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0550 @UPDATE-001 @auto
  # 对应测试：test_TC_0550_update_notice
  场景: TC-0550 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0551 @UPDATE-001 @auto
  # 对应测试：test_TC_0551_update_notice
  场景: TC-0551 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.4.13；保留 managed 升级说明

  @TC-0552 @UPDATE-001 @auto
  # 对应测试：test_TC_0552_update_notice
  场景: TC-0552 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.4.13；保留 managed 升级说明

  @TC-0553 @UPDATE-001 @auto
  # 对应测试：test_TC_0553_update_notice
  场景: TC-0553 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0554 @UPDATE-001 @auto
  # 对应测试：test_TC_0554_update_notice
  场景: TC-0554 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0555 @UPDATE-001 @auto
  # 对应测试：test_TC_0555_update_notice
  场景: TC-0555 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0556 @UPDATE-001 @auto
  # 对应测试：test_TC_0556_update_notice
  场景: TC-0556 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0557 @UPDATE-001 @auto
  # 对应测试：test_TC_0557_update_notice
  场景: TC-0557 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0558 @UPDATE-001 @auto
  # 对应测试：test_TC_0558_update_notice
  场景: TC-0558 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.4.12", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0559 @UPDATE-001 @auto
  # 对应测试：test_TC_0559_update_notice
  场景: TC-0559 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0560 @UPDATE-001 @auto
  # 对应测试：test_TC_0560_update_notice
  场景: TC-0560 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0561 @UPDATE-001 @auto
  # 对应测试：test_TC_0561_update_notice
  场景: TC-0561 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0562 @UPDATE-001 @auto
  # 对应测试：test_TC_0562_update_notice
  场景: TC-0562 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0563 @UPDATE-001 @auto
  # 对应测试：test_TC_0563_update_notice
  场景: TC-0563 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0564 @UPDATE-001 @auto
  # 对应测试：test_TC_0564_update_notice
  场景: TC-0564 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0565 @UPDATE-001 @auto
  # 对应测试：test_TC_0565_update_notice
  场景: TC-0565 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0566 @UPDATE-001 @auto
  # 对应测试：test_TC_0566_update_notice
  场景: TC-0566 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0567 @UPDATE-001 @auto
  # 对应测试：test_TC_0567_update_notice
  场景: TC-0567 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0568 @UPDATE-001 @auto
  # 对应测试：test_TC_0568_update_notice
  场景: TC-0568 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0569 @UPDATE-001 @auto
  # 对应测试：test_TC_0569_update_notice
  场景: TC-0569 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0570 @UPDATE-001 @auto
  # 对应测试：test_TC_0570_update_notice
  场景: TC-0570 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.4.13", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0571 @UPDATE-001 @auto
  # 对应测试：test_TC_0571_update_notice
  场景: TC-0571 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0572 @UPDATE-001 @auto
  # 对应测试：test_TC_0572_update_notice
  场景: TC-0572 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0573 @UPDATE-001 @auto
  # 对应测试：test_TC_0573_update_notice
  场景: TC-0573 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0574 @UPDATE-001 @auto
  # 对应测试：test_TC_0574_update_notice
  场景: TC-0574 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0575 @UPDATE-001 @auto
  # 对应测试：test_TC_0575_update_notice
  场景: TC-0575 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0576 @UPDATE-001 @auto
  # 对应测试：test_TC_0576_update_notice
  场景: TC-0576 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0577 @UPDATE-001 @auto
  # 对应测试：test_TC_0577_update_notice
  场景: TC-0577 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0578 @UPDATE-001 @auto
  # 对应测试：test_TC_0578_update_notice
  场景: TC-0578 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 0.10.0；保留 managed 升级说明

  @TC-0579 @UPDATE-001 @auto
  # 对应测试：test_TC_0579_update_notice
  场景: TC-0579 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0580 @UPDATE-001 @auto
  # 对应测试：test_TC_0580_update_notice
  场景: TC-0580 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 1.0.0；保留 managed 升级说明

  @TC-0581 @UPDATE-001 @auto
  # 对应测试：test_TC_0581_update_notice
  场景: TC-0581 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0582 @UPDATE-001 @auto
  # 对应测试：test_TC_0582_update_notice
  场景: TC-0582 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "0.9.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0583 @UPDATE-001 @auto
  # 对应测试：test_TC_0583_update_notice
  场景: TC-0583 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.11", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0584 @UPDATE-001 @auto
  # 对应测试：test_TC_0584_update_notice
  场景: TC-0584 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.11", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0585 @UPDATE-001 @auto
  # 对应测试：test_TC_0585_update_notice
  场景: TC-0585 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.12", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0586 @UPDATE-001 @auto
  # 对应测试：test_TC_0586_update_notice
  场景: TC-0586 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.12", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0587 @UPDATE-001 @auto
  # 对应测试：test_TC_0587_update_notice
  场景: TC-0587 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.4.13", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0588 @UPDATE-001 @auto
  # 对应测试：test_TC_0588_update_notice
  场景: TC-0588 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.4.13", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0589 @UPDATE-001 @auto
  # 对应测试：test_TC_0589_update_notice
  场景: TC-0589 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "0.10.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0590 @UPDATE-001 @auto
  # 对应测试：test_TC_0590_update_notice
  场景: TC-0590 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "0.10.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0591 @UPDATE-001 @auto
  # 对应测试：test_TC_0591_update_notice
  场景: TC-0591 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "1.0.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0592 @UPDATE-001 @auto
  # 对应测试：test_TC_0592_update_notice
  场景: TC-0592 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "1.0.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 不提示同版或旧版；保留 managed 升级说明

  @TC-0593 @UPDATE-001 @auto
  # 对应测试：test_TC_0593_update_notice
  场景: TC-0593 更新提醒
    假如 安装与缓存为 {"automatic": false, "candidate": "2.0.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0594 @UPDATE-001 @auto
  # 对应测试：test_TC_0594_update_notice
  场景: TC-0594 更新提醒
    假如 安装与缓存为 {"automatic": true, "candidate": "2.0.0", "current": "1.0.0", "mode": "managed"}
    当 读取已完成的更新检查结果
    那么 报告可用版本 2.0.0；保留 managed 升级说明

  @TC-0595 @UPDATE-009 @auto
  # 对应测试：test_TC_0595_update_check
  场景: TC-0595 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 newer
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0596 @UPDATE-009 @auto
  # 对应测试：test_TC_0596_update_check
  场景: TC-0596 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 older
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0597 @UPDATE-009 @auto
  # 对应测试：test_TC_0597_update_check
  场景: TC-0597 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 same
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0598 @UPDATE-009 @auto
  # 对应测试：test_TC_0598_update_check
  场景: TC-0598 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 offline
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0599 @UPDATE-009 @auto
  # 对应测试：test_TC_0599_update_check
  场景: TC-0599 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 invalid_json
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0600 @UPDATE-009 @auto
  # 对应测试：test_TC_0600_update_check
  场景: TC-0600 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 empty
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0601 @UPDATE-009 @auto
  # 对应测试：test_TC_0601_update_check
  场景: TC-0601 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 prerelease
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0602 @UPDATE-009 @auto
  # 对应测试：test_TC_0602_update_check
  场景: TC-0602 版本检查
    假如 package 安装版本 0.4.12，版本源响应场景为 withdrawn
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0603 @UPDATE-009 @auto
  # 对应测试：test_TC_0603_update_check
  场景: TC-0603 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 newer
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0604 @UPDATE-009 @auto
  # 对应测试：test_TC_0604_update_check
  场景: TC-0604 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 older
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0605 @UPDATE-009 @auto
  # 对应测试：test_TC_0605_update_check
  场景: TC-0605 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 same
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0606 @UPDATE-009 @auto
  # 对应测试：test_TC_0606_update_check
  场景: TC-0606 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 offline
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0607 @UPDATE-009 @auto
  # 对应测试：test_TC_0607_update_check
  场景: TC-0607 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 invalid_json
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0608 @UPDATE-009 @auto
  # 对应测试：test_TC_0608_update_check
  场景: TC-0608 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 empty
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0609 @UPDATE-009 @auto
  # 对应测试：test_TC_0609_update_check
  场景: TC-0609 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 prerelease
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0610 @UPDATE-009 @auto
  # 对应测试：test_TC_0610_update_check
  场景: TC-0610 版本检查
    假如 managed 安装版本 0.4.12，版本源响应场景为 withdrawn
    当 强制检查版本
    那么 只有可安装的更高稳定版本才能报告 available；错误不改变运行时

  @TC-0611 @UPDATE-005 @auto
  # 对应测试：test_TC_0611_package_cli
  场景: TC-0611 包模式更新命令
    假如 package 安装为 0.4.12，PyPI 存在 0.4.13，旧配置 automatic=true
    当 执行更新入口 []
    那么 查询版本并报告或缓存 0.4.13，不调用 apply，后台模式不污染 stdout

  @TC-0612 @UPDATE-005 @auto
  # 对应测试：test_TC_0612_package_cli
  场景: TC-0612 包模式更新命令
    假如 package 安装为 0.4.12，PyPI 存在 0.4.13，旧配置 automatic=true
    当 执行更新入口 ["--check"]
    那么 查询版本并报告或缓存 0.4.13，不调用 apply，后台模式不污染 stdout

  @TC-0613 @UPDATE-005 @auto
  # 对应测试：test_TC_0613_package_cli
  场景: TC-0613 包模式更新命令
    假如 package 安装为 0.4.12，PyPI 存在 0.4.13，旧配置 automatic=true
    当 执行更新入口 ["--background"]
    那么 查询版本并报告或缓存 0.4.13，不调用 apply，后台模式不污染 stdout

  @TC-0614 @UPDATE-005 @auto
  # 对应测试：test_TC_0614_package_cli
  场景: TC-0614 包模式更新命令
    假如 package 安装为 0.4.12，PyPI 存在 0.4.13，旧配置 automatic=true
    当 执行更新入口 ["--auto", "off"]
    那么 查询版本并报告或缓存 0.4.13，不调用 apply，后台模式不污染 stdout

  @TC-0615 @UPDATE-015 @auto
  # 对应测试：test_TC_0615_package_reject
  场景: TC-0615 包模式升级限制
    假如 package 安装由 pipx 管理
    当 执行 ["--apply"]
    那么 拒绝自动应用并明确提示 pipx upgrade saygo-agent-control

  @TC-0616 @UPDATE-015 @auto
  # 对应测试：test_TC_0616_package_reject
  场景: TC-0616 包模式升级限制
    假如 package 安装由 pipx 管理
    当 执行 ["--auto", "on"]
    那么 拒绝自动应用并明确提示 pipx upgrade saygo-agent-control

  @TC-0617 @UPDATE-007 @auto
  # 对应测试：test_TC_0617_notice_refresh
  场景: TC-0617 提醒刷新
    假如 package 更新缓存状态为 missing
    当 客户端读取通知
    那么 过期、缺失、损坏缓存触发后台刷新；近期缓存不重复查网络

  @TC-0618 @UPDATE-007 @auto
  # 对应测试：test_TC_0618_notice_refresh
  场景: TC-0618 提醒刷新
    假如 package 更新缓存状态为 expired
    当 客户端读取通知
    那么 过期、缺失、损坏缓存触发后台刷新；近期缓存不重复查网络

  @TC-0619 @UPDATE-007 @auto
  # 对应测试：test_TC_0619_notice_refresh
  场景: TC-0619 提醒刷新
    假如 package 更新缓存状态为 corrupt
    当 客户端读取通知
    那么 过期、缺失、损坏缓存触发后台刷新；近期缓存不重复查网络

  @TC-0620 @UPDATE-007 @auto
  # 对应测试：test_TC_0620_notice_refresh
  场景: TC-0620 提醒刷新
    假如 package 更新缓存状态为 fresh
    当 客户端读取通知
    那么 过期、缺失、损坏缓存触发后台刷新；近期缓存不重复查网络

  @TC-0621 @UPDATE-002 @auto
  # 对应测试：test_TC_0621_package_start
  场景: TC-0621 包模式启动检查
    假如 package 安装使用 pipx 解释器
    当 启动 MCP
    那么 在返回 MCP 子进程前调度独立后台检查，stdout 保持协议专用

  @UP-001 @UPDATE-007 @auto
  # 对应测试：test_notice_refresh_nonblocking
  场景: UP-001 更新集成：读取 notice 后再释放版本源
    假如 无更新缓存，版本源响应被闸门阻塞
    当 读取 notice 后再释放版本源
    那么 首次立即返回 checking，完成后返回 v0.4.13；所有网络工作发生在后台线程

  @UP-002 @UPDATE-013 @auto
  # 对应测试：test_notice_coalesces_inflight_requests
  场景: UP-002 更新集成：并发读取同一安装的 notice
    假如 版本检查正在进行，另有八次客户端通知请求
    当 并发读取同一安装的 notice
    那么 只启动一次版本查询，所有请求返回而不等待网络

  @UP-003 @UPDATE-006 @auto
  # 对应测试：test_mcp_sessions_repairs_old_launcher_gap
  场景: UP-003 更新集成：两次调用 device_sessions，中间等待新模块后台检查完成
    假如 MCP 仍由跳过检查的旧 package launcher 启动且没有缓存
    当 两次调用 device_sessions，中间等待新模块后台检查完成
    那么 第一次包含 checking，第二次 updates 明确包含新版本及 pipx 命令

  @UP-004 @UPDATE-012 @auto
  # 对应测试：test_offline_preserves_known_release_and_reports_error
  场景: UP-004 更新集成：再次强制检查并读取提醒
    假如 已有 v0.4.13 检查结果，版本源随后离线
    当 再次强制检查并读取提醒
    那么 保留已知新版本并同时报告离线错误，安装信息不变

  @UP-005 @UPDATE-011 @auto
  # 对应测试：test_upgrade_invalidates_cache
  场景: UP-005 更新集成：读取更新通知
    假如 旧缓存提示 0.4.13，实际包已升级为 0.4.13
    当 读取更新通知
    那么 不再提示同版本，并触发与新版本匹配的缓存更新

  @UP-006 @UPDATE-012 @auto
  # 对应测试：test_version_read_error_is_nonfatal
  场景: UP-006 更新集成：客户端读取 notice
    假如 包版本元数据读取失败
    当 客户端读取 notice
    那么 返回结构化错误而非抛异常阻断设备工具

  @UP-007 @UPDATE-004 @auto
  # 对应测试：test_apply_cannot_bypass_package_policy
  场景: UP-007 更新集成：直接调用 apply(stage_only=True)
    假如 package 安装有可用更新且旧配置 automatic=true
    当 直接调用 apply(stage_only=True)
    那么 明确拒绝且不下载资源、不创建 managed runtime 指针

  @UP-008 @UPDATE-002 @auto
  # 对应测试：test_startup_offline_does_not_block_or_pollute_stdout
  场景: UP-008 更新集成：启动 MCP 并等待后台失败
    假如 package 启动且版本源离线
    当 启动 MCP 并等待后台失败
    那么 MCP 子进程仍启动，stdout 没有诊断文本，stderr 有更新错误

  @UP-009 @UPDATE-012 @auto
  # 对应测试：test_thread_start_failure_clears_marker
  场景: UP-009 更新集成：读取通知后重试调度
    假如 线程资源耗尽导致 Thread.start 失败
    当 读取通知后重试调度
    那么 通知返回错误，未遗留阻止未来重试的运行标记

  @UP-010 @UPDATE-014 @auto
  # 对应测试：test_readonly_cache_failure_is_contained
  场景: UP-010 更新集成：后台刷新版本检查
    假如 缓存文件可读取，但原子写入因只读文件系统失败
    当 后台刷新版本检查
    那么 线程正常结束并记录错误，MCP 通知不抛异常

  @UP-011 @UPDATE-009 @auto
  # 对应测试：test_pypi_files_and_numeric_ordering
  场景: UP-011 更新集成：强制检查 package 更新
    假如 PyPI 高版本只有 yanked 文件，中间版本有可用 wheel，预发布和空文件版本并存
    当 强制检查 package 更新
    那么 选择最高有未撤回文件的稳定版本，不选择空文件或预发布版本

  @UP-012 @UPDATE-003 @auto
  # 对应测试：test_package_current_uses_installed_interpreter
  场景: UP-012 更新集成：读取实际 package 版本
    假如 installation.json 版本陈旧且残留 active-runtime.json
    当 读取实际 package 版本
    那么 版本取自 pipx 解释器的包元数据，忽略 managed 指针

  @UP-013 @UPDATE-019 @auto
  # 对应测试：test_same_package_version_still_repairs_a_changed_shared_directory
  场景: UP-013 更新集成：同步 package bridge
    假如 Python 包版本相同，但桌面版在线 bridge 与安装记录不同
    当 同步 package bridge
    那么 先发现共享目录再修复注册与安装记录，不因版本相同跳过

  @UP-014 @UPDATE-019 @auto
  # 对应测试：test_matching_shared_directory_and_package_version_do_not_reinstall
  场景: UP-014 更新集成：同步 package bridge
    假如 包版本、共享目录、实际注册与安装记录全部一致
    当 同步 package bridge
    那么 只执行只读发现，不重复安装 native host 或改写安装记录

  @UP-015 @UPDATE-019 @auto
  # 对应测试：test_matching_version_and_live_directory_still_repair_stale_registration
  场景: UP-015 更新集成：同步 package bridge
    假如 包版本与在线目录一致，但浏览器实际注册指向另一目录
    当 同步 package bridge
    那么 修复实际注册，避免下次插件连接进入另一套 bridge

  @UP-016 @UPDATE-019 @auto
  # 对应测试：test_package_upgrade_updates_host_even_when_directory_is_unchanged
  场景: UP-016 更新集成：同步 package bridge
    假如 外部升级 Python 包后共享 bridge 目录不变
    当 同步 package bridge
    那么 更新 host 安装及版本记录，不因目录相同漏掉升级

  @UP-017 @UPDATE-019 @auto
  # 对应测试：test_discovery_failure_preserves_installation_and_reports_pending
  场景: UP-017 更新集成：同步 package bridge
    假如 共享 bridge 发现失败或繁忙
    当 同步 package bridge
    那么 保留原安装记录并报告更新待完成，不擅自建立第二套 bridge
