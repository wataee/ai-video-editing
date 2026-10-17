import os
import sys
import json
import shutil
import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def check_approval(plan_data: dict, plan_path: Path):
    if not plan_data.get("approved", False):
        print(f"\n[APPROVAL GATE BLOCKED] Final render blocked because 'approved' is false in {plan_path}!", file=sys.stderr)
        print("Please review beat_table.md and contact_sheet_plan.png, and set 'approved': true to proceed.\n", file=sys.stderr)
        sys.exit(1)

def resolve_file_path(p_str: str | None, plan_file: Path) -> Path | None:
    if not p_str:
        return None
    p = Path(p_str)
    if p.is_absolute() and p.exists():
        return p
    candidates = [
        plan_file.parent / p,
        ROOT / p,
        plan_file.parent.parent / p,
        plan_file.parent.parent.parent / p,
    ]
    for cand in candidates:
        if cand.exists():
            return cand.resolve()
    return (ROOT / p).resolve()

def validate_proofs(plan_data: dict, plan_file: Path):
    beats = plan_data.get("beats", [])
    for b in beats:
        if b.get("visual") == "proof":
            ps = b.get("proof_source")
            if not ps or not str(ps).strip():
                print(f"\n[PROOF VALIDATION ERROR] Beat #{b.get('beat_index')} visual is 'proof' but proof_source is missing!", file=sys.stderr)
                sys.exit(1)
            p_path = resolve_file_path(ps, plan_file)
            if not p_path or not p_path.exists():
                print(f"\n[PROOF VALIDATION ERROR] Beat #{b.get('beat_index')} proof_source file not found on disk: {p_path}!", file=sys.stderr)
                sys.exit(1)

def get_npx_executable() -> str:
    npx_bin = shutil.which("npx.cmd") if sys.platform == "win32" else None
    if not npx_bin:
        npx_bin = shutil.which("npx")
    if not npx_bin:
        print("Error: 'npx' executable not found in PATH.", file=sys.stderr)
        sys.exit(1)
    return npx_bin

def verify_output_mp4(mp4_path: Path, expected_duration: float, tolerance: float = 0.5):
    ffprobe_bin = shutil.which("ffprobe")
    if not ffprobe_bin:
        print("Warning: ffprobe not found in PATH, skipping stream verification.", file=sys.stderr)
        return

    cmd = [
        ffprobe_bin,
        "-v", "error",
        "-show_entries", "stream=codec_type,duration:format=duration",
        "-of", "json",
        str(mp4_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: ffprobe failed on {mp4_path}:\n{res.stderr}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(res.stdout)
    streams = data.get("streams", [])
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    has_video = any(s.get("codec_type") == "video" for s in streams)

    if not has_video:
        print(f"Error: Output {mp4_path} has no video stream!", file=sys.stderr)
        sys.exit(1)
    if not has_audio:
        print(f"Error: Output {mp4_path} has no audio stream!", file=sys.stderr)
        sys.exit(1)

    actual_dur = float(data.get("format", {}).get("duration", 0.0))
    if expected_duration > 0 and abs(actual_dur - expected_duration) > tolerance:
        print(
            f"Error: Output duration {actual_dur:.2f}s differs from expected {expected_duration:.2f}s by > {tolerance}s!",
            file=sys.stderr
        )
        sys.exit(1)

    print(f"Verification passed: audio and video streams present, duration {actual_dur:.2f}s matches expected {expected_duration:.2f}s (±{tolerance}s).")

def main():
    parser = argparse.ArgumentParser(description="Render final clip from edit_plan.json using Remotion + audio mix mux")
    parser.add_argument("target", nargs="?", default="work/plan/edit_plan.json", help="Path to edit_plan.json or client dir")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 file path")
    parser.add_argument("--allow-voice-fallback", action="store_true", help="Allow fallback to raw voice if tools/mix.py fails")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if target_path.is_dir():
        plan_file = target_path / "edit_plan.json"
    else:
        plan_file = target_path

    if not plan_file.exists():
        print(f"Error: edit_plan.json not found at {plan_file}", file=sys.stderr)
        sys.exit(1)

    with open(plan_file, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    check_approval(plan_data, plan_file)
    validate_proofs(plan_data, plan_file)

    proj_id = plan_data.get("project_id", "final_clip")
    if args.output:
        out_mp4 = Path(args.output).resolve()
    else:
        out_mp4 = plan_file.parent / f"{proj_id}_final.mp4"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    target_duration = float(plan_data.get("target_duration_sec", 15.0))

    resolved_video = resolve_file_path(plan_data.get("sdr_path") or plan_data.get("proxy_path"), plan_file)
    if not resolved_video or not resolved_video.exists():
        fallback_candidates = [
            ROOT / "work" / "ingest" / f"{proj_id}_sdr_cfr30.mp4",
            *list((ROOT / "work" / "ingest").glob("*.mp4")),
        ]
        if plan_file.parent.parent.exists():
            fallback_candidates.extend(list((plan_file.parent.parent / "ingest").glob("*.mp4")))
        for cand in fallback_candidates:
            if cand.exists():
                resolved_video = cand.resolve()
                break

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tmp_public = tmp_path / "public"
        tmp_public.mkdir(parents=True, exist_ok=True)

        assets_dir = ROOT / "assets"
        if assets_dir.exists():
            assets_sub = tmp_public / "assets"
            try:
                os.symlink(assets_dir, assets_sub, target_is_directory=True)
            except OSError:
                shutil.copytree(assets_dir, assets_sub)

            for item in assets_dir.iterdir():
                dst = tmp_public / item.name
                if not dst.exists():
                    if item.is_dir():
                        try:
                            os.symlink(item, dst, target_is_directory=True)
                        except OSError:
                            shutil.copytree(item, dst)
                    else:
                        try:
                            os.link(item, dst)
                        except OSError:
                            shutil.copyfile(item, dst)

        video_src_prop = None
        if resolved_video and resolved_video.exists():
            video_dst = tmp_public / "source_video.mp4"
            try:
                os.link(resolved_video, video_dst)
            except OSError:
                try:
                    os.symlink(resolved_video, video_dst)
                except OSError:
                    shutil.copyfile(resolved_video, video_dst)
            video_src_prop = "source_video.mp4"

        props_file = tmp_path / "props.json"
        props_data = {
            "plan": plan_data,
        }
        if video_src_prop:
            props_data["videoSrc"] = video_src_prop

        with open(props_file, "w", encoding="utf-8") as pf:
            json.dump(props_data, pf, ensure_ascii=False)

        silent_video = tmp_path / "silent_render.mp4"
        npx_bin = get_npx_executable()

        cmd_remotion = [
            npx_bin, "remotion", "render",
            "src/index.ts", "ReelFromPlan", str(silent_video),
            f"--props={str(props_file)}",
            f"--public-dir={str(tmp_public)}",
            "--muted",
            "--log=error"
        ]
        print("Rendering video layer with Remotion (ReelFromPlan)...")
        res_r = subprocess.run(cmd_remotion, cwd=str(ROOT), capture_output=True, text=True)
        if res_r.returncode != 0 or not silent_video.exists():
            print("Error: Remotion render failed.", file=sys.stderr)
            if res_r.stderr:
                print(res_r.stderr, file=sys.stderr)
            if res_r.stdout:
                print(res_r.stdout, file=sys.stderr)
            sys.exit(1)

        voice_source = resolved_video if resolved_video and resolved_video.exists() else silent_video

        audio_tmp_dir = tmp_path / "audio"
        audio_tmp_dir.mkdir(parents=True, exist_ok=True)
        mix_py = ROOT / "tools" / "mix.py"
        cmd_mix = [sys.executable, str(mix_py), str(voice_source), str(plan_file), str(audio_tmp_dir)]
        print("Building calibrated audio mix with tools/mix.py...")
        res_m = subprocess.run(cmd_mix, cwd=str(ROOT), capture_output=True, text=True)
        mix_wav = audio_tmp_dir / "mix.wav"

        if res_m.returncode != 0 or not mix_wav.exists():
            print(f"Error: Audio mix failed with exit code {res_m.returncode}.", file=sys.stderr)
            if res_m.stderr:
                print(res_m.stderr, file=sys.stderr)
            if args.allow_voice_fallback:
                print("Warning: --allow-voice-fallback enabled, falling back to voice audio.", file=sys.stderr)
                mix_wav = voice_source
            else:
                sys.exit(1)

        print("Muxing video and audio streams without video re-encoding...")
        cmd_mux = [
            "ffmpeg", "-y",
            "-i", str(silent_video),
            "-i", str(mix_wav),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out_mp4)
        ]
        res_x = subprocess.run(cmd_mux, capture_output=True, text=True)
        if res_x.returncode != 0 or not out_mp4.exists():
            print("Error: FFmpeg muxing failed.", file=sys.stderr)
            if res_x.stderr:
                print(res_x.stderr, file=sys.stderr)
            sys.exit(1)

        verify_output_mp4(out_mp4, expected_duration=target_duration)

    print(f"\nFinal clip successfully rendered: {out_mp4}")

if __name__ == "__main__":
    main()
