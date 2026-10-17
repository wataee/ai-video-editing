import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from render_clip import resolve_file_path, verify_output_mp4, check_voice_has_audio

def test_resolve_file_path(tmp_path):
    plan_dir = tmp_path / "work" / "plan"
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_file = plan_dir / "edit_plan.json"
    plan_file.touch()

    # 1. Absolute existing path
    abs_file = tmp_path / "sample.mp4"
    abs_file.touch()
    resolved = resolve_file_path(str(abs_file), plan_file)
    assert resolved == abs_file

    # 2. Relative to plan directory
    local_file = plan_dir / "sibling.mp4"
    local_file.touch()
    resolved = resolve_file_path("sibling.mp4", plan_file)
    assert resolved == local_file

    # 3. Relative to ROOT
    resolved_root = resolve_file_path("package.json", plan_file)
    assert resolved_root == (ROOT / "package.json").resolve()

    # 4. Non-existent path
    non_existent = resolve_file_path("does_not_exist_file.mp4", plan_file)
    assert not non_existent.exists()

def test_verify_output_mp4_valid(tmp_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffmpeg_bin is not None

    valid_mp4 = tmp_path / "valid.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=duration=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(valid_mp4)
    ], check=True, capture_output=True)

    verify_output_mp4(valid_mp4, expected_duration=1.0, tolerance=0.5)

def test_verify_output_mp4_missing_audio_fails(tmp_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffmpeg_bin is not None

    no_audio_mp4 = tmp_path / "no_audio.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-an",
        str(no_audio_mp4)
    ], check=True, capture_output=True)

    with pytest.raises(SystemExit) as exc_info:
        verify_output_mp4(no_audio_mp4, expected_duration=1.0)
    assert exc_info.value.code == 1

def test_verify_output_mp4_duration_mismatch_fails(tmp_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffmpeg_bin is not None

    short_mp4 = tmp_path / "short.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=duration=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(short_mp4)
    ], check=True, capture_output=True)

    with pytest.raises(SystemExit) as exc_info:
        verify_output_mp4(short_mp4, expected_duration=10.0, tolerance=0.5)
    assert exc_info.value.code == 1

def test_check_voice_has_audio(tmp_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffmpeg_bin is not None

    audio_file = tmp_path / "with_audio.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-f", "lavfi", "-i", "sine=duration=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(audio_file)
    ], check=True, capture_output=True)

    assert check_voice_has_audio(audio_file) is True

    silent_file = tmp_path / "without_audio.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-an",
        str(silent_file)
    ], check=True, capture_output=True)

    assert check_voice_has_audio(silent_file) is False

def test_render_clip_source_guessing_guard(tmp_path):
    render_clip_py = ROOT / "tools" / "render_clip.py"
    plan_file = tmp_path / "edit_plan.json"
    plan_content = {
        "project_id": "guard_test",
        "approved": True,
        "target_duration_sec": 5.0,
        "sdr_path": "non_existent_sdr.mp4",
        "beats": []
    }
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan_content, f)

    # When fallback candidate exists in work/ingest, fails without --allow-source-guess
    res = subprocess.run([
        sys.executable, str(render_clip_py),
        str(plan_file)
    ], capture_output=True, text=True)
    assert res.returncode == 1
    assert "Fallback to guessed video is disabled by default" in res.stderr

def test_render_clip_voice_without_audio_stream_fails(tmp_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffmpeg_bin is not None
    silent_source = tmp_path / "silent_source.mp4"
    subprocess.run([
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-an",
        str(silent_source)
    ], check=True, capture_output=True)

    plan_file = tmp_path / "edit_plan.json"
    plan_content = {
        "project_id": "silent_voice_test",
        "approved": True,
        "target_duration_sec": 1.0,
        "sdr_path": str(silent_source),
        "beats": []
    }
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan_content, f)

    render_clip_py = ROOT / "tools" / "render_clip.py"
    res = subprocess.run([
        sys.executable, str(render_clip_py),
        str(plan_file)
    ], capture_output=True, text=True)
    assert res.returncode == 1
    assert "has no audio stream" in res.stderr
