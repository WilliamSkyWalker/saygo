"""Image observations with explicit input mapping and bounded visual waits."""
import hashlib
import io
import json
import math
from pathlib import Path
import time
import uuid

from PIL import Image, ImageChops

from saygo.platforms import device_session as ds

MAX_AGE_SECONDS = 60
IDENTITY_FIELDS = ('screen_size', 'page_id', 'url', 'target', 'window_id', 'process_id', 'window_bounds')


class ObservationChangedError(ValueError):
    """Input was rejected; the caller must inspect evidence and decide again."""
    requires_observation = True

    def __init__(self, message, observation=None, visual_change=None):
        super().__init__(message)
        self.observation = observation
        self.visual_change = visual_change


class WaitResult(dict):
    """Keep a few sampled bytes local; JSON serialization exposes only facts."""
    def __init__(self, result, frames, identity, captured_at=None):
        super().__init__(result)
        self.frames = tuple(frames)
        self.identity = identity
        self.captured_at = time.time() if captured_at is None else captured_at


def metadata(platform, png, session=None):
    from .actions import capabilities
    with Image.open(io.BytesIO(png)) as im:
        size = list(im.size)
    result = dict(session=session or "default", width=size[0], height=size[1],
                  screen_size=list(platform.screen_size), coordinate_space="screen",
                  image_sha256=hashlib.sha256(png).hexdigest(),
                  image_to_screen=[platform.screen_size[0] / size[0], platform.screen_size[1] / size[1]])
    if hasattr(platform, "observation_metadata"):
        result.update(platform.observation_metadata())
    if hasattr(platform, "page_id"):
        result["page_id"] = platform.page_id
    state = ds.load_state(session) or {}
    result["target"] = {key: state[key] for key in ("os", "kind", "app", "desktop_scope", "device_id", "session_id", "process_id", "background", "window_id") if key in state}
    result['capabilities'] = capabilities(platform)
    return result


def capture(platform, session=None, out=None, crop=None):
    png = platform.screenshot_raw()
    return save(platform, png, session, out, crop)


def save(platform, png, session=None, out=None, crop=None, *, description=None, captured_at=None):
    """Persist the exact image used for a decision, including its target identity."""
    result = dict(description) if description is not None else metadata(platform, png, session)
    oid = uuid.uuid4().hex
    root = ds.STATE_DIR.parent / "observations"
    root.mkdir(parents=True, exist_ok=True)
    path = Path(out).expanduser().resolve() if out else root / f"{oid}.png"
    result.update(id=oid, observation_id=oid, at=time.time() if captured_at is None else captured_at,
                  path=str(path), scale=getattr(platform, "scale", 1))
    source = root / f"{oid}.png"
    source.write_bytes(png)
    if path != source:
        path.write_bytes(png)
    result["source_path"] = str(source)
    if crop is not None:
        if len(crop) != 4 or any(isinstance(n, bool) or not isinstance(n, int) for n in crop):
            raise ValueError("crop must be [left, top, right, bottom] in image pixels")
        left, top, right, bottom = crop
        if not 0 <= left < right <= result["width"] or not 0 <= top < bottom <= result["height"]:
            raise ValueError("crop is outside the observation")
        with Image.open(io.BytesIO(png)) as im:
            cropped = im.crop(crop)
            cropped = cropped.resize((cropped.width * 2, cropped.height * 2))
            crop_path = root / f"{oid}-crop.png"
            cropped.save(crop_path)
        result["crop"] = dict(path=str(crop_path), source_rect=crop, zoom=2,
                              to_screen_scale=[n / 2 for n in result["image_to_screen"]],
                              to_screen_offset=[left * result["image_to_screen"][0], top * result["image_to_screen"][1]])
    (root / f"{oid}.json").write_text(__import__('json').dumps(result), encoding="utf-8")
    return result


def capture_after_wait(platform, result, session=None, out=None, crop=None):
    """Reuse the last sampled image and retain local phases for this observation only."""
    frames = getattr(result, 'frames', ())
    if not frames:
        return capture(platform, session, out, crop)
    description = metadata(platform, frames[-1], session)
    identity = getattr(result, 'identity', None)
    if identity is not None and any(description.get(k) != identity.get(k) for k in IDENTITY_FIELDS):
        raise ObservationChangedError('Target changed during wait; observe and locate again')
    shot = save(platform, frames[-1], session, out, crop, description=description,
                captured_at=result.captured_at)
    if getattr(platform, 'platform_name', None) != 'browser' or identity is None:
        return shot
    # A phase must differ visibly from the delivered frame. Store at most three
    # candidates, under this observation's ID; no cross-observation learning.
    root = ds.STATE_DIR.parent / 'observations'
    try:
        phases = []
        for png in frames[:-1]:
            change = describe_change(frames[-1], png)
            digest = hashlib.sha256(png).hexdigest()
            if not _small_local_change(change, shot['width'], shot['height']) or digest in phases:
                continue
            path = root / f"{shot['id']}-phase-{len(phases)}.png"
            path.write_bytes(png)
            phases.append(digest)
        if phases:
            (root / f"{shot['id']}-phases.json").write_text(json.dumps({
                'image_sha256': shot['image_sha256'], 'phases': phases}), encoding='utf-8')
    except OSError:
        pass  # Optional local phases must not discard an otherwise usable observation.
    return shot


def describe_change(before, after):
    """Describe the same >24-per-channel pixel test used by the input guard."""
    with Image.open(io.BytesIO(before)) as first, Image.open(io.BytesIO(after)) as second:
        if first.size != second.size:
            return {'change_fraction': 1.0, 'changed_bounds': [0, 0, *second.size]}
        bands = ImageChops.difference(first.convert('RGB'), second.convert('RGB')).split()
        maximum = ImageChops.lighter(ImageChops.lighter(bands[0], bands[1]), bands[2])
        mask = maximum.point(lambda value: 255 if value > 24 else 0)
        return {'change_fraction': mask.histogram()[255] / max(1, mask.width * mask.height),
                'changed_bounds': list(mask.getbbox()) if mask.getbbox() else None}


def _small_local_change(change, width, height):
    box = change['changed_bounds']
    return bool(box and .002 < change['change_fraction'] <= .01
                and (box[2] - box[0]) * (box[3] - box[1]) <= width * height * .05
                and box[2] - box[0] <= width * .35
                and box[3] - box[1] <= height * .35)


def known_local_phase(observation, current, change, x, y):
    """Accept only a previously sampled full frame, far from the target context."""
    width, height = observation['width'], observation['height']
    if not _small_local_change(change, width, height):
        return False
    sx, sy = observation['image_to_screen']
    px, py = x / sx, y / sy
    rx, ry = max(96 / sx, width * .15), max(96 / sy, height * .20)
    left, top, right, bottom = change['changed_bounds']
    if left < px + rx and right > px - rx and top < py + ry and bottom > py - ry:
        return False
    oid = observation.get('id', '')
    if len(oid) != 32 or any(c not in '0123456789abcdef' for c in oid):
        return False
    root = ds.STATE_DIR.parent / 'observations'
    try:
        saved = json.loads((root / f'{oid}-phases.json').read_text(encoding='utf-8'))
        if saved['image_sha256'] != observation['image_sha256']:
            return False
        for index, digest in enumerate(saved['phases'][:3]):
            png = (root / f'{oid}-phase-{index}.png').read_bytes()
            if hashlib.sha256(png).hexdigest() == digest and change_fraction(png, current) == 0:
                return True
    except (OSError, ValueError, KeyError, TypeError):
        pass  # Missing/corrupt optional evidence never relaxes the normal guard.
    return False


def load(oid, session):
    if not isinstance(oid, str) or len(oid) != 32 or any(c not in "0123456789abcdef" for c in oid):
        raise ValueError("Invalid observation ID")
    import json
    result = json.loads((ds.STATE_DIR.parent / "observations" / f"{oid}.json").read_text())
    if result["session"] != (session or "default"):
        raise ValueError("Observation belongs to another session")
    return result


def change_fraction(before, after, region=None):
    """Fraction of pixels changing by >24 intensity; ignore compression and small noise."""
    with Image.open(io.BytesIO(before)) as first, Image.open(io.BytesIO(after)) as second:
        if first.size != second.size:
            return 1.0
        first, second = first.convert("RGB"), second.convert("RGB")
        if region:
            first, second = first.crop(region), second.crop(region)
        diff = ImageChops.difference(first, second)
        bands = diff.split()
        maximum = ImageChops.lighter(ImageChops.lighter(bands[0], bands[1]), bands[2])
        histogram = maximum.histogram()
        return sum(histogram[25:]) / max(1, maximum.width * maximum.height)


def wait(platform, mode="stable", timeout=5, threshold=.002, interval=.2, *, session=None):
    if mode not in {"stable", "change"} or not math.isfinite(timeout) or not 0 < timeout <= 60:
        raise ValueError("wait requires stable/change and timeout in (0,60]")
    start = time.monotonic()
    previous = platform.screenshot_raw()
    captured_at = time.time()
    identity = metadata(platform, previous, session)
    frames = [previous]
    baseline = previous
    stable_since = start
    while time.monotonic() - start < timeout:
        time.sleep(min(interval, max(0, timeout - (time.monotonic() - start))))
        current = platform.screenshot_raw()
        captured_at = time.time()
        frames.append(current)
        frames = frames[-4:]
        fraction = change_fraction(baseline if mode == "change" else previous, current)
        now = time.monotonic()
        if mode == "change" and fraction > threshold:
            return WaitResult(dict(condition_met=True, timed_out=False, mode=mode, change_fraction=fraction), frames, identity, captured_at)
        if fraction > threshold:
            stable_since = now
        if mode == "stable" and now - stable_since >= .6:
            return WaitResult(dict(condition_met=True, timed_out=False, mode=mode, change_fraction=fraction), frames, identity, captured_at)
        previous = current
    return WaitResult(dict(condition_met=False, timed_out=True, mode=mode), frames, identity, captured_at)
