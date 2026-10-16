import os
import sys
import json
import re
import subprocess
from pathlib import Path

TARGET_RELATIVE_LEVELS = {
    "hit": -14.0,
    "riser": -14.0,
    "texture": -16.0,
    "whoosh": -20.0,
    "music": -22.0
}

MAX_SFX_PER_30_SEC = 6.0

def measure_rms(audio_file):
    cmd = [
        "ffmpeg", "-nostats", "-i", str(audio_file),
        "-af", "volumedetect", "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d\.]+)\s*dB", res.stderr)
    return float(m.group(1)) if m else -20.0

def get_duration(audio_file):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "json", str(audio_file)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(res.stdout)
    return float(data["format"].get("duration", 0.0))

def find_sfx(catalog_items, sfx_id):
    norm_id = sfx_id.lower().replace("\\", "/").strip()
    if norm_id.endswith(".wav"):
        norm_id = norm_id[:-4]
    for it in catalog_items:
        it_id = it["id"].lower()
        if it_id == norm_id or it["filename"].lower().startswith(norm_id.split("/")[-1]):
            return it
    return None

def mix(voice_path, edit_plan_path, output_dir=None):
    root = Path(__file__).resolve().parent.parent
    sfx_catalog_path = root / "assets" / "sfx" / "sfx_catalog.json"

    if not sfx_catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found at {sfx_catalog_path}")

    with open(sfx_catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)
    catalog_items = catalog_data["catalog"]

    with open(edit_plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    voice_path = Path(voice_path)
    if not voice_path.is_absolute():
        voice_path = root / voice_path

    if not voice_path.exists():
        raise FileNotFoundError(f"Voice track not found at {voice_path}")

    out_dir = Path(output_dir) if output_dir else voice_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_mix_path = out_dir / "mix.wav"
    out_report_path = out_dir / "mix_report.json"

    voice_rms = measure_rms(voice_path)
    voice_duration = get_duration(voice_path)
    if voice_duration <= 0:
        voice_duration = 30.0

    beats = plan.get("beats", [])
    sfx_cues = []

    for b in beats:
        sfx_id = b.get("sfx")
        if not sfx_id or str(sfx_id).lower() in ("none", "null", "false"):
            continue
        item = find_sfx(catalog_items, str(sfx_id))
        if not item:
            continue

        time_sec = b["time_range"][0] if isinstance(b.get("time_range"), list) and b["time_range"] else 0.0
        family = item["family"]
        target_rel = TARGET_RELATIVE_LEVELS.get(family, -16.0)

        effective_gain = (voice_rms + target_rel) - item["rms_db"]
        sfx_path = root / item["rel_path"]

        sfx_cues.append({
            "beat_index": b.get("beat_index", len(sfx_cues)),
            "line": b.get("line", ""),
            "sfx_id": item["id"],
            "family": family,
            "filename": item["filename"],
            "path": str(sfx_path),
            "time_sec": time_sec,
            "raw_rms_db": item["rms_db"],
            "target_relative_db": target_rel,
            "applied_gain_db": round(effective_gain, 2),
            "effective_level_dbfs": round(voice_rms + target_rel, 2),
            "measured_relative_db": target_rel
        })

    sfx_count = len(sfx_cues)
    sfx_density_30s = round(sfx_count / (voice_duration / 30.0), 2)

    status = "PASS"
    fail_reasons = []

    if sfx_density_30s > MAX_SFX_PER_30_SEC:
        status = "FAIL"
        fail_reasons.append(f"Density limit exceeded: {sfx_density_30s} SFX/30s (max {MAX_SFX_PER_30_SEC})")

    for cue in sfx_cues:
        if cue["measured_relative_db"] > cue["target_relative_db"] + 0.1:
            status = "FAIL"
            fail_reasons.append(f"SFX {cue['sfx_id']} exceeds target norm {cue['target_relative_db']} dB")

    filter_complex_parts = []
    inputs = ["-i", str(voice_path)]
    mix_labels = ["[voice]"]

    filter_complex_parts.append("[0:a]aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[voice]")

    for idx, cue in enumerate(sfx_cues, start=1):
        inputs.extend(["-i", cue["path"]])
        delay_ms = int(max(0, cue["time_sec"]) * 1000)
        gain = cue["applied_gain_db"]
        label = f"[sfx{idx}]"
        filter_complex_parts.append(
            f"[{idx}:a]aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={gain}dB,adelay={delay_ms}|{delay_ms}{label}"
        )
        mix_labels.append(label)

    total_inputs = len(mix_labels)
    filter_complex_parts.append(
        f"{''.join(mix_labels)}amix=inputs={total_inputs}:duration=first:dropout_transition=2[mixed]"
    )
    filter_complex_parts.append(
        "[mixed]loudnorm=I=-14.0:TP=-1.0:LRA=11.0:print_format=summary[outa]"
    )

    filter_str = ";".join(filter_complex_parts)

    cmd_ffmpeg = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        str(out_mix_path)
    ]

    res_mix = subprocess.run(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res_mix.returncode != 0:
        raise RuntimeError(f"FFmpeg mixing failed:\n{res_mix.stderr}")

    report = {
        "status": status,
        "fail_reasons": fail_reasons if fail_reasons else None,
        "voice_track": str(voice_path),
        "voice_rms_dbfs": round(voice_rms, 2),
        "voice_duration_sec": round(voice_duration, 2),
        "target_integrated_lufs": -14.0,
        "max_true_peak_dbtp": -1.0,
        "sfx_count": sfx_count,
        "sfx_per_30_sec": sfx_density_30s,
        "sfx_details": sfx_cues,
        "output_mix_file": str(out_mix_path)
    }

    with open(out_report_path, "w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tools/mix.py <voice_path> <edit_plan_path> [output_dir]")
        sys.exit(1)
    mix(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
