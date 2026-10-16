import os
import sys
import json
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

def validate_proofs(plan_data: dict):
    beats = plan_data.get("beats", [])
    for b in beats:
        if b.get("visual") == "proof":
            ps = b.get("proof_source")
            if not ps or not str(ps).strip():
                print(f"\n[PROOF VALIDATION ERROR] Beat #{b.get('beat_index')} visual is 'proof' but proof_source is missing!", file=sys.stderr)
                sys.exit(1)
            p_path = Path(ps)
            if not p_path.is_absolute():
                p_path = ROOT / p_path
            if not p_path.exists():
                print(f"\n[PROOF VALIDATION ERROR] Beat #{b.get('beat_index')} proof_source file not found on disk: {p_path}!", file=sys.stderr)
                sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Render final clip from edit_plan.json using Remotion + audio mix mux")
    parser.add_argument("target", nargs="?", default="work/plan/edit_plan.json", help="Path to edit_plan.json or client dir")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 file path")
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
    validate_proofs(plan_data)

    proj_id = plan_data.get("project_id", "final_clip")
    if args.output:
        out_mp4 = Path(args.output).resolve()
    else:
        out_mp4 = plan_file.parent / f"{proj_id}_final.mp4"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        props_file = tmp_path / "props.json"
        with open(props_file, "w", encoding="utf-8") as pf:
            json.dump({"plan": plan_data}, pf, ensure_ascii=False)

        silent_video = tmp_path / "silent_render.mp4"

        cmd_remotion = [
            "cmd.exe", "/c", "npx", "remotion", "render",
            "src/index.ts", "ReelFromPlan", str(silent_video),
            f"--props={str(props_file)}",
            "--muted",
            "--log=error"
        ]
        print(f"Rendering video layer with Remotion (ReelFromPlan)...")
        res_r = subprocess.run(cmd_remotion, cwd=str(ROOT))
        if res_r.returncode != 0 or not silent_video.exists():
            print("Error: Remotion render failed.", file=sys.stderr)
            sys.exit(1)

        voice_source = plan_data.get("sdr_path") or plan_data.get("proxy_path")
        if not voice_source or not Path(voice_source).exists():
            voice_source = ROOT / "work" / "ingest" / f"{proj_id}_sdr_cfr30.mp4"
        if not Path(voice_source).exists():
            candidates = list((ROOT / "work" / "ingest").glob("*.mp4"))
            if candidates:
                voice_source = candidates[0]
            else:
                voice_source = silent_video

        audio_tmp_dir = tmp_path / "audio"
        audio_tmp_dir.mkdir(parents=True, exist_ok=True)
        mix_py = ROOT / "tools" / "mix.py"
        cmd_mix = [sys.executable, str(mix_py), str(voice_source), str(plan_file), str(audio_tmp_dir)]
        print(f"Building calibrated audio mix with tools/mix.py...")
        res_m = subprocess.run(cmd_mix, cwd=str(ROOT), capture_output=True, text=True)
        mix_wav = audio_tmp_dir / "mix.wav"
        if not mix_wav.exists():
            print(f"Warning: mix.wav not generated, falling back to voice audio.\n{res_m.stderr}", file=sys.stderr)
            mix_wav = voice_source

        print(f"Muxing video and audio streams without video re-encoding...")
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
        res_x = subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res_x.returncode != 0 or not out_mp4.exists():
            print("Error: FFmpeg muxing failed.", file=sys.stderr)
            sys.exit(1)

    print(f"\nFinal clip successfully rendered: {out_mp4}")

if __name__ == "__main__":
    main()
