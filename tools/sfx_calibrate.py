import os
import sys
import json
import re
import subprocess
from pathlib import Path

def get_audio_info(file_path):
    cmd_probe = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=sample_rate,channels",
        "-of", "json", file_path
    ]
    res_probe = subprocess.run(cmd_probe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    probe_data = json.loads(res_probe.stdout)
    duration = float(probe_data["format"].get("duration", 0.0))

    cmd_vol = [
        "ffmpeg", "-nostats", "-i", file_path,
        "-af", "volumedetect", "-f", "null", "-"
    ]
    res_vol = subprocess.run(cmd_vol, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_vol = res_vol.stderr

    max_vol_match = re.search(r"max_volume:\s*(-?[\d\.]+)\s*dB", out_vol)
    mean_vol_match = re.search(r"mean_volume:\s*(-?[\d\.]+)\s*dB", out_vol)

    peak_db = float(max_vol_match.group(1)) if max_vol_match else 0.0
    rms_db = float(mean_vol_match.group(1)) if mean_vol_match else -20.0

    cmd_ebu = [
        "ffmpeg", "-nostats", "-i", file_path,
        "-af", "ebur128=peak=true", "-f", "null", "-"
    ]
    res_ebu = subprocess.run(cmd_ebu, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_ebu = res_ebu.stderr

    i_lufs_match = re.search(r"Integrated loudness:\s*I:\s*(-?[\d\.]+)\s*LUFS", out_ebu)
    i_lufs = float(i_lufs_match.group(1)) if i_lufs_match else rms_db

    return duration, peak_db, rms_db, i_lufs

def calibrate():
    root = Path(__file__).resolve().parent.parent
    sfx_dir = root / "assets" / "sfx"
    output_path = sfx_dir / "sfx_catalog.json"

    family_map = {
        "whooshes": "whoosh",
        "textures": "texture",
        "clicks": "texture",
        "pops": "texture",
        "glitches": "texture",
        "hits": "hit",
        "risers": "riser",
        "ambience": "ambience"
    }

    catalog = []
    by_family = {}

    for dirpath, _, filenames in os.walk(sfx_dir):
        for f in filenames:
            if f.endswith(".wav"):
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root).replace("\\", "/")
                cat_folder = os.path.basename(dirpath)
                family = family_map.get(cat_folder, "texture")
                fid = f"{cat_folder}/{os.path.splitext(f)[0]}"

                duration, peak_db, rms_db, i_lufs = get_audio_info(full_path)

                item = {
                    "id": fid,
                    "filename": f,
                    "family": family,
                    "category": cat_folder,
                    "rel_path": rel_path,
                    "duration": round(duration, 4),
                    "peak_db": round(peak_db, 2),
                    "rms_db": round(rms_db, 2),
                    "integrated_lufs": round(i_lufs, 2),
                    "gain_to_reference_db": 0.0
                }
                catalog.append(item)
                by_family.setdefault(family, []).append(item)

    family_reference_rms = {
        "hit": -16.0,
        "riser": -18.0,
        "texture": -22.0,
        "whoosh": -20.0,
        "ambience": -26.0
    }

    for family, items in by_family.items():
        ref_rms = family_reference_rms.get(family, -20.0)
        for it in items:
            gain = ref_rms - it["rms_db"]
            it["gain_to_reference_db"] = round(gain, 2)

    catalog.sort(key=lambda x: (x["family"], x["id"]))

    result = {
        "version": "2.0.0",
        "total_files": len(catalog),
        "families": list(family_reference_rms.keys()),
        "catalog": catalog
    }

    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=2, ensure_ascii=False)

    print(f"Calibrated {len(catalog)} SFX files into {output_path}")

if __name__ == "__main__":
    calibrate()
