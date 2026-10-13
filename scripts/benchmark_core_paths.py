"""Measure isolated discovery, screenshot and history paths without devices or models."""

import argparse
import io
import json
from pathlib import Path
import platform
from statistics import median
import sys
import tempfile
from time import perf_counter
from unittest.mock import patch


def measure(operation, repeat):
    operation()  # Warm imports and filesystem caches before measuring.
    samples = []
    for _ in range(repeat):
        started = perf_counter()
        operation()
        samples.append((perf_counter() - started) * 1000)
    return {"median_ms": round(median(samples), 3), "min_ms": round(min(samples), 3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Checkout to import; use the same script/interpreter for both revisions")
    parser.add_argument("--repeat", type=int, default=9)
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be positive")
    source = args.source.resolve()
    if not (source / "saygo" / "__init__.py").is_file():
        parser.error("--source must contain the saygo package")
    sys.path.insert(0, str(source))

    from PIL import Image, ImageDraw, __version__ as pillow_version
    from saygo.qa import cases
    from saygo.runtime.interactive import InteractiveRuntime
    from saygo.runtime.store import Store
    from saygo.skills.visual_diff import _compute_diff
    from saygo.vision.settle import sample_then_frames

    results = {"source": str(source), "platform": platform.system(),
               "machine": platform.machine(), "python": platform.python_version(),
               "pillow": pillow_version, "repeat": args.repeat, "warmup": 1}
    with tempfile.TemporaryDirectory(prefix="saygo-core-benchmark-") as temporary:
        root = Path(temporary)
        target = root / "tests" / "example"
        case_dir = target / "cases"
        case_dir.mkdir(parents=True)
        for index in range(300):
            (target / f"section-{index:03d}").mkdir()
        (case_dir / "legacy.md").write_text("### TC-001\nCheck the example screen.", encoding="utf-8")
        with patch.object(cases, "TESTS_DIR", root / "tests"):
            results["discovery_300_directories"] = measure(
                lambda: cases._resolve_test_target(str(target)), args.repeat)

        images, frames = [], []
        for color in ("white", "white", "black"):
            image = Image.new("RGB", (1080, 1920), color)
            ImageDraw.Draw(image).rectangle((60, 200, 900, 260), fill="#2266aa")
            images.append(image)
            output = io.BytesIO()
            image.save(output, format="PNG")
            frames.append(output.getvalue())
        for name, operation in (
            ("sample_static", lambda: sample_then_frames([frames[0]] * 3)),
            ("sample_dynamic", lambda: sample_then_frames(frames)),
            ("visual_static", lambda: _compute_diff(images[0], images[1])),
            ("visual_dynamic", lambda: _compute_diff(images[0], images[2])),
        ):
            results[name] = measure(operation, args.repeat)

        store = Store(root / "runtime")
        state = store.create({"resources": {}, "steps": []}, mode="interactive")
        state["outputs"] = {f"step-{index}": {"note": "x" * 1000} for index in range(4000)}
        store.save(state, "fixture_ready")
        payload = json.dumps({"step": "example", "note": "evidence " * 50})
        with store.connect() as db:
            db.executemany("INSERT INTO events(run_id,at,kind,data) VALUES (?,?,?,?)",
                           ((state["id"], float(index), "agent_annotation", payload)
                            for index in range(2000)))
        runtime = InteractiveRuntime(store)
        results["snapshot_bytes"] = len(json.dumps(state).encode("utf-8"))
        results["event_count"] = len(store.events(state["id"]))
        results["events"] = measure(lambda: store.events(state["id"]), args.repeat)
        results["export"] = measure(lambda: runtime.export(state["id"], root / "evidence.zip"), args.repeat)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
