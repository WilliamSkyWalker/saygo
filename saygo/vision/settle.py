"""Settle 闸 + 帧采样（性能优化 Phase 1 地基）—— 全程零 LLM。

判断屏幕是否"加载完/稳定"（settle），并为不同 step 类型采样帧：
- **When（操作步）**：消费**稳态 1 帧**——决策 + locator 定位都在稳定帧上做，避免在
  加载中/过渡动画的帧上定坐标导致点空点错。
- **Then（断言步）**：从"触发 → settle"窗口采 **首 / 中 / 稳** 三点（横跨窗口，不是挤在
  末尾——否则漏掉早期就消失的 toast），再用 **2% visual_diff 路由**：三点两两最大变化
  < 2% → 窗口没动 = 静态断言 → 只送稳态 1 帧；≥ 2% → 有过程/动画/瞬态 → 送 3 帧。

只用像素差（downscale + 状态栏 mask，histogram 快速统计），不调大模型。详见
docs/common/performance.md 的 Phase 1。
"""

from __future__ import annotations

import io
import time

from PIL import Image, ImageChops

from saygo.logger import get_logger

log = get_logger("settle")

# 判"相邻帧没动"的变化阈值（change_ratio 分数，0-1）。低于视为稳定。
STABLE_CHANGE_RATIO = 0.01     # 1%
# Then 静态/动态路由阈值：窗口内最大帧间变化 < 此 → 静态 → 只送稳态 1 帧。
STATIC_ROUTE_RATIO = 0.02      # 2%
# 顶部状态栏高度占比（屏蔽时钟/电量/信号这类每帧微动的噪声）。
STATUS_BAR_FRAC = 0.04
# 计算帧间差时把图缩到这个宽度（稳定性判定不需要全分辨率，缩图快一个量级）。
_DIFF_WIDTH = 360
# 单像素判"变了"的灰度阈值（对齐 visual_diff.DIFF_THRESHOLD）。
_PIXEL_THRESHOLD = 30


def _prep(png: bytes) -> Image.Image | None:
    """PNG bytes → 去状态栏 + 缩小的 RGB 图；无效帧保留为 None。"""
    try:
        with Image.open(io.BytesIO(png)) as source:
            im = source.convert("RGB")
        w, h = im.size
        top = int(h * STATUS_BAR_FRAC)      # 裁掉顶部状态栏带（噪声 mask）
        im = im.crop((0, top, w, h))
        w2, h2 = im.size
        if w2 > _DIFF_WIDTH:
            im = im.resize((_DIFF_WIDTH, max(1, int(h2 * _DIFF_WIDTH / w2))))
        return im
    except Exception:
        return None


def _change_ratio(a_png: bytes, b_png: bytes) -> float:
    """两帧变化像素占比（0-1）。histogram 走 C 层，比逐像素 Python 循环快得多。"""
    return _prepared_change_ratio(_prep(a_png), _prep(b_png))


def _prepared_change_ratio(a: Image.Image | None, b: Image.Image | None) -> float:
    """Compare already prepared frames without decoding either PNG again."""
    if a is None or b is None:
        return 1.0                          # 解析失败当"变了"，宁可多等
    if a.size != b.size:
        b = b.resize(a.size)
    diff = ImageChops.difference(a, b).convert("L")
    changed = sum(diff.histogram()[_PIXEL_THRESHOLD + 1:])
    total = a.size[0] * a.size[1]
    return changed / total if total else 0.0


def wait_settled(platform, timeout_s: float = 6.0, interval: float = 0.3,
                 stable_needed: int = 2) -> tuple[bool, list[bytes]]:
    """轮询帧直到连续 stable_needed 对相邻帧变化 < STABLE_CHANGE_RATIO，或超时。

    返回 (settled, frames)：frames 是窗口内按时间顺序的 PNG 帧序列（供采样用）；
    settled=False 表示到超时仍在动（调用方应回退同步判，见 perf-plan 红线）。
    全程 platform.screenshot_raw()（mjpeg 下近零成本），不调大模型。
    """
    frames: list[bytes] = []
    try:
        frames.append(platform.screenshot_raw())
    except Exception as e:
        log.debug("settle 首帧截图失败: %s", e)
        return False, frames

    t0 = time.monotonic()
    previous = None
    stable_run = 0
    while time.monotonic() - t0 < timeout_s:
        time.sleep(max(0.0, interval))
        try:
            cur = platform.screenshot_raw()
        except Exception as e:
            log.debug("settle 轮询截图失败: %s", e)
            break
        if len(frames) == 1:
            previous = _prep(frames[0])
        current = _prep(cur)
        r = _prepared_change_ratio(previous, current)
        previous = current
        frames.append(cur)
        if r < STABLE_CHANGE_RATIO:
            stable_run += 1
            if stable_run >= stable_needed:
                return True, frames
        else:
            stable_run = 0
    return False, frames


def steady_frame(frames: list[bytes]) -> bytes | None:
    """When 消费：窗口最后一帧 = 稳态帧。"""
    return frames[-1] if frames else None


def sample_then_frames(frames: list[bytes]) -> tuple[list[bytes], bool]:
    """Then 消费：采首/中/稳三点 + 2% 路由。

    返回 (chosen, dynamic)：
      dynamic=False → 窗口基本没动（静态断言）→ chosen = [稳态帧]（只送 1 图）；
      dynamic=True  → 有过程/动画/瞬态 → chosen = [首, 中, 稳]（送 3 图判过程）。
    """
    if not frames:
        return [], False
    if len(frames) <= 2:
        return [frames[-1]], False          # 帧太少，等同静态
    first, steady = frames[0], frames[-1]
    mid = frames[len(frames) // 2]
    three = [first, mid, steady]
    prepared = [_prep(frame) for frame in three]
    for i in range(len(prepared)):
        for j in range(i + 1, len(prepared)):
            if _prepared_change_ratio(prepared[i], prepared[j]) >= STATIC_ROUTE_RATIO:
                return three, True         # 动态 → 首/中/稳
    return [steady], False                  # 静态 → 只送稳态
