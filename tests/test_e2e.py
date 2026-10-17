import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent

@pytest.mark.slow
def test_full_pipeline_e2e(tmp_path):
    ffprobe_bin = shutil.which("ffprobe")
    ffmpeg_bin = shutil.which("ffmpeg")
    assert ffprobe_bin is not None, "ffprobe must be installed"
    assert ffmpeg_bin is not None, "ffmpeg must be installed"

    raw_video = tmp_path / "test_raw_input.mp4"
    cmd_gen = [
        ffmpeg_bin, "-y",
        "-f", "lavfi", "-i", "testsrc=duration=10:size=1080x1920:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=10",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(raw_video)
    ]
    subprocess.run(cmd_gen, check=True, capture_output=True)
    assert raw_video.exists(), "Raw test video generation failed"

    ingest_dir = tmp_path / "work" / "ingest"
    ingest_dir.mkdir(parents=True, exist_ok=True)
    ingest_py = ROOT / "tools" / "ingest.py"
    subprocess.run([
        sys.executable, str(ingest_py),
        str(raw_video),
        "--output_dir", str(ingest_dir)
    ], check=True, capture_output=True)

    sdr_video = ingest_dir / "test_raw_input_sdr_cfr30.mp4"
    assert sdr_video.exists(), "Ingest failed to produce SDR CFR30 video"

    words_file = tmp_path / "words.json"
    words_data = [
        {"text": "Привет,", "startMs": 0, "endMs": 1500},
        {"text": "это", "startMs": 1600, "endMs": 2800},
        {"text": "первый", "startMs": 2900, "endMs": 4000},
        {"text": "тестовый", "startMs": 4100, "endMs": 5200},
        {"text": "бит.", "startMs": 5300, "endMs": 6000},
        {"text": "А", "startMs": 6100, "endMs": 7000},
        {"text": "это", "startMs": 7100, "endMs": 8000},
        {"text": "второй", "startMs": 8100, "endMs": 9000},
        {"text": "финал.", "startMs": 9100, "endMs": 10000},
    ]
    with open(words_file, "w", encoding="utf-8") as wf:
        json.dump(words_data, wf)

    plan_dir = tmp_path / "work" / "plan"
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_file = plan_dir / "edit_plan.json"

    scaffold_py = ROOT / "tools" / "plan_scaffold.py"
    subprocess.run([
        sys.executable, str(scaffold_py),
        str(words_file),
        "--sdr", str(sdr_video),
        "--output", str(plan_file),
        "--project_id", "test_e2e"
    ], check=True, capture_output=True)
    assert plan_file.exists(), "plan_scaffold.py failed to produce edit_plan.json"

    with open(plan_file, "r", encoding="utf-8") as pf:
        plan_data = json.load(pf)

    plan_data["approved"] = True
    plan_data["target_duration_sec"] = 10.0
    for idx, beat in enumerate(plan_data.get("beats", [])):
        beat["visual"] = "speaker"
        beat["camera"] = "push-in"
        beat["sfx"] = "hits/sub_bass_thud" if idx == 0 else None

    with open(plan_file, "w", encoding="utf-8") as pf:
        json.dump(plan_data, pf, indent=2, ensure_ascii=False)

    out_mp4 = tmp_path / "test_e2e_final.mp4"
    render_clip_py = ROOT / "tools" / "render_clip.py"
    res_render = subprocess.run([
        sys.executable, str(render_clip_py),
        str(plan_file),
        "--output", str(out_mp4)
    ], capture_output=True, text=True)

    if res_render.returncode != 0:
        pytest.fail(f"render_clip.py failed with returncode {res_render.returncode}:\nSTDERR:\n{res_render.stderr}\nSTDOUT:\n{res_render.stdout}")

    assert out_mp4.exists(), f"Render output not created: {out_mp4}"

    cmd_probe = [
        ffprobe_bin,
        "-v", "error",
        "-show_entries", "stream=codec_type,width,height,r_frame_rate,duration:format=duration",
        "-of", "json",
        str(out_mp4)
    ]
    res_probe = subprocess.run(cmd_probe, capture_output=True, text=True, check=True)
    probe_data = json.loads(res_probe.stdout)

    streams = probe_data.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    assert video_stream is not None, "Rendered MP4 has no video stream"
    assert audio_stream is not None, "Rendered MP4 has no audio stream"

    assert video_stream.get("width") == 1080, f"Expected width 1080, got {video_stream.get('width')}"
    assert video_stream.get("height") == 1920, f"Expected height 1920, got {video_stream.get('height')}"

    r_rate = video_stream.get("r_frame_rate", "30/1")
    num, den = [float(x) for x in r_rate.split("/")]
    fps = num / den
    assert abs(fps - 30.0) < 0.1, f"Expected ~30 fps, got {fps}"

    duration = float(probe_data.get("format", {}).get("duration", 0.0))
    assert abs(duration - 10.0) <= 0.2, f"Expected duration 10.0s ± 0.2s, got {duration:.3f}s"
