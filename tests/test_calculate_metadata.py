import math

def calculate_metadata_logic(plan: dict) -> dict:
    fps = plan.get("fps") or 30
    width = plan.get("width") or 1080
    height = plan.get("height") or 1920
    target_duration = plan.get("target_duration_sec") if plan.get("target_duration_sec") is not None else 15
    duration_in_frames = max(1, round(target_duration * fps))

    return {
        "fps": fps,
        "width": width,
        "height": height,
        "durationInFrames": duration_in_frames,
    }

def test_calculate_metadata_defaults():
    meta = calculate_metadata_logic({})
    assert meta["width"] == 1080
    assert meta["height"] == 1920
    assert meta["fps"] == 30
    assert meta["durationInFrames"] == 450

def test_calculate_metadata_custom_duration():
    meta = calculate_metadata_logic({
        "target_duration_sec": 10.2,
        "fps": 30
    })
    assert meta["fps"] == 30
    assert meta["durationInFrames"] == round(10.2 * 30)
    assert meta["durationInFrames"] == 306

def test_calculate_metadata_custom_dimensions_and_fps():
    meta = calculate_metadata_logic({
        "target_duration_sec": 5.0,
        "fps": 60,
        "width": 720,
        "height": 1280
    })
    assert meta["fps"] == 60
    assert meta["width"] == 720
    assert meta["height"] == 1280
    assert meta["durationInFrames"] == 300
