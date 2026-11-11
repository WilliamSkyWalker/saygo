"""One action vocabulary shared by interactive agents and workflow resources."""
import math
from pathlib import Path
from . import observations

BASE = {"tap", "swipe", "input", "press_key", "scroll_up", "scroll_down"}
OPTIONAL = {"hover", "double_click", "right_click", "long_press", "scroll_at", "hotkey", "open_link_background"}


def capabilities(platform):
    actions = BASE | {name for name in OPTIONAL if callable(getattr(type(platform), name, None))}
    kind = getattr(platform, 'platform_name', None)
    if kind == 'browser':
        actions.add('open_url')
    elif kind in {'android', 'ios', 'mac', 'windows', 'desktop', 'rdp'}:
        actions.add('open_app')
    if callable(getattr(type(platform), "supported_actions", None)):
        actions = set(platform.supported_actions())
    if callable(getattr(type(platform), "list_pages", None)):
        actions |= {"select_page", "close_page", "new_page", "go_back", "go_forward"}
    result = {"actions": sorted(actions), "coordinate_spaces": ["screen", "percent", "image", "crop"],
              "business_verification": "external_agent", "scroll_at_unit": "wheel_notches",
              "scroll_direction": "viewport", "scroll_up": "toward_top", "scroll_down": "toward_bottom"}
    if getattr(platform, 'platform_name', None) == 'browser' and 'scroll_at' in actions:
        result.update(scroll_at_pixels_per_unit=100, scroll_at_positive_direction='up',
                      scroll_at_fractional=True)
    if callable(getattr(type(platform), "capability_details", None)):
        result.update(platform.capability_details())
    return result


def number(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be finite and in [{low},{high}]")
    return value


def prepare(platform, action, observation=None):
    if not isinstance(action, dict):
        raise ValueError("action must be an object")
    action = dict(action)
    kind = action.get("type")
    if kind not in capabilities(platform)["actions"]:
        raise ValueError(f"Unsupported action: {kind}; query capabilities")
    w, h = platform.screen_size
    coordinates = []
    if kind in {"tap", "hover", "double_click", "right_click", "long_press", "scroll_at", "open_link_background"}:
        coordinates = [("x", w), ("y", h)]
    elif kind == "swipe":
        coordinates = [("x1", w), ("y1", h), ("x2", w), ("y2", h)]
    space = action.get("coordinate_space", "percent" if any(k.endswith("_pct") for k in action) else "screen")
    if space not in {"screen", "percent", "image", "crop"}:
        raise ValueError("Unknown coordinate_space")
    if space in {"image", "crop"} and observation is None:
        raise ValueError("image/crop coordinates require an observation_id")
    for name, size in coordinates:
        axis = 0 if name.startswith("x") else 1
        value = action.get(name + "_pct", action.get(name))
        if space == "percent":
            value = min(size - 1, round(number(value, name, 0, 100) * size / 100))
        elif space in {"image", "crop"}:
            if space == "crop":
                crop = observation.get("crop")
                if not crop:
                    raise ValueError("observation has no crop")
                limit = (crop["source_rect"][axis + 2] - crop["source_rect"][axis]) * crop["zoom"]
                value = number(value, name, 0, limit - 1) * crop["to_screen_scale"][axis] + crop["to_screen_offset"][axis]
            else:
                limit = observation["width" if axis == 0 else "height"]
                value = number(value, name, 0, limit - 1) * observation["image_to_screen"][axis]
        action[name] = int(number(value, name, 0, size - 1))
    if kind in {"input", "press_key", "open_url", "open_app", "new_page", "select_page", "close_page"}:
        field = {"input":"text", "press_key":"key", "open_url":"url", "open_app":"target", "new_page":"url"}.get(kind, "page_id")
        if not isinstance(action.get(field), str) or not action[field]:
            raise ValueError(f"{field} must be a nonempty string")
    if kind == "hotkey":
        if not isinstance(action.get("keys"), list) or not action["keys"] or not all(isinstance(k, str) and k for k in action["keys"]):
            raise ValueError("hotkey requires a list of key names")
    if kind == "long_press":
        action["duration"] = number(action.get("duration", 1), "duration", .1, 30)
    if kind == "scroll_at":
        action["amount"] = number(action.get("amount"), "amount", -100, 100)
    if callable(getattr(type(platform), "validate_action", None)):
        platform.validate_action(action)
    if (kind == 'open_app' and observation
            and callable(getattr(type(platform), 'prepare_application_launch', None))):
        platform.prepare_application_launch(action['target'], observation)
        action['coordinate_space'] = 'screen'
        return action
    if observation:
        import time
        if time.time() - observation.get("at", time.time()) > observations.MAX_AGE_SECONDS:
            raise observations.ObservationChangedError(f"Observation expired; observe again (maximum age {observations.MAX_AGE_SECONDS}s)")
        current = platform.screenshot_raw()
        captured_at = time.time()
        meta = observations.metadata(platform, current, observation.get("session"))

        def reject(message, change=None):
            try:
                evidence = observations.save(platform, current, observation.get('session'),
                                             description=meta, captured_at=captured_at)
            except OSError as exc:
                # Retain the guard's recovery semantics even when disk is full.
                raise observations.ObservationChangedError(message, visual_change=change) from exc
            raise observations.ObservationChangedError(message, evidence, change)

        if any(meta.get(k) != observation.get(k) for k in observations.IDENTITY_FIELDS):
            reject("Target changed; observe and locate again")
        before = Path(observation.get("source_path", observation["path"])).read_bytes()
        change = observations.describe_change(before, current)
        if change['change_fraction'] > .002:
            single_point = kind in {'tap', 'hover', 'double_click', 'right_click', 'long_press',
                                    'scroll_at', 'open_link_background'}
            known_phase = (getattr(platform, 'platform_name', None) == 'browser' and single_point
                           and observations.known_local_phase(observation, current, change, action['x'], action['y']))
            if not known_phase:
                reject("Screen changed; observe and locate again", change)
            action['visual_validation'] = dict(change, known_local_phase=True)
        # Even a small change near the target invalidates its location.
        if coordinates:
            from PIL import Image
            import io
            with Image.open(io.BytesIO(current)) as im:
                sx, sy = im.width / w, im.height / h
                for index in range(0, len(coordinates), 2):
                    x, y = action[coordinates[index][0]] * sx, action[coordinates[index + 1][0]] * sy
                    region = (max(0, int(x - 24)), max(0, int(y - 24)), min(im.width, int(x + 25)), min(im.height, int(y + 25)))
                    if observations.change_fraction(before, current, region) > .002:
                        reject("Target region changed; observe and locate again", change)
    if observation and observation.get("window_id") is not None and callable(getattr(type(platform), "expect_window", None)):
        platform.expect_window(observation)
    for name, _ in coordinates:
        action.pop(name + "_pct", None)
    action["coordinate_space"] = "screen"
    return action


def dispatch(platform, action):
    kind = action["type"]
    if kind in {"hover", "double_click", "right_click"}:
        getattr(platform, kind)(action["x"], action["y"])
    elif kind == "open_link_background":
        page_id = platform.open_link_background(action["x"], action["y"])
        return {"dispatched": True, "created_page_id": page_id,
                "business_success": None, "requires_observation": True}
    elif kind == "long_press":
        platform.long_press(action["x"], action["y"], action["duration"])
    elif kind == "scroll_at":
        platform.scroll_at(action["x"], action["y"], action["amount"])
    elif kind == "hotkey":
        platform.hotkey(action["keys"])
    elif kind == "new_page":
        return {"dispatched": True, "created_page_id": platform.new_page(action["url"])}
    else:
        platform.execute_action(action)
    return {"dispatched": True, "business_success": None, "requires_observation": True}
