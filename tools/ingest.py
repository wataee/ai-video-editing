import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image

def parse_rate(rate_str):
    if not rate_str or rate_str == "0/0":
        return 0.0
    if "/" in rate_str:
        num, den = rate_str.split("/")
        return float(num) / float(den) if float(den) != 0 else 0.0
    return float(rate_str)

def probe_video(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=width,height,pix_fmt,color_space,color_transfer,color_primaries,r_frame_rate,avg_frame_rate,duration:stream_tags=rotate:stream_side_data_list",
        "-show_entries", "format=duration",
        "-of", "json", str(video_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data["streams"][0] if data.get("streams") else {}
    fmt = data.get("format", {})

    r_fps = parse_rate(stream.get("r_frame_rate", "30/1"))
    avg_fps = parse_rate(stream.get("avg_frame_rate", "30/1"))
    duration = float(stream.get("duration") or fmt.get("duration") or 0.0)

    color_transfer = stream.get("color_transfer", "unknown")
    color_primaries = stream.get("color_primaries", "unknown")
    pix_fmt = stream.get("pix_fmt", "unknown")
    
    rotate = stream.get("tags", {}).get("rotate", "0")
    if rotate == "0" and "side_data_list" in stream:
        for sd in stream["side_data_list"]:
            if "rotation" in sd:
                rotate = str(int(sd["rotation"]))

    is_hdr = (
        color_transfer in ["arib-std-b67", "smpte2084"]
        or "bt2020" in color_primaries
        or "10le" in pix_fmt
    )
    is_vfr = abs(r_fps - avg_fps) > 0.05

    raw_w = stream.get("width", 1920)
    raw_h = stream.get("height", 1080)
    is_rotated = rotate in ["90", "-90", "270", "-270"]
    eff_w = raw_h if is_rotated else raw_w
    eff_h = raw_w if is_rotated else raw_h
    is_horizontal = eff_w > eff_h

    return {
        "width": raw_w,
        "height": raw_h,
        "effective_width": eff_w,
        "effective_height": eff_h,
        "is_horizontal": is_horizontal,
        "aspect_ratio": f"{round(eff_w / max(1, eff_h), 2)}:1",
        "pix_fmt": pix_fmt,
        "color_transfer": color_transfer,
        "color_primaries": color_primaries,
        "r_frame_rate": stream.get("r_frame_rate"),
        "avg_frame_rate": stream.get("avg_frame_rate"),
        "r_fps": round(r_fps, 3),
        "avg_fps": round(avg_fps, 3),
        "is_vfr": is_vfr,
        "is_hdr": is_hdr,
        "duration": round(duration, 3),
        "rotate": rotate
    }

def convert_hdr_to_sdr(input_file, out_sdr, out_proxy, probe_info, denoise=False):
    vf_libplacebo = (
        "libplacebo=tonemapping=bt.2390:colorspace=bt709:color_primaries=bt709:"
        "color_trc=bt709:range=tv:format=yuv420p,fps=fps=30"
    )
    
    audio_filters = []
    if denoise:
        audio_filters.append("highpass=f=80,lowpass=f=12000,afftdn=nf=-25")
    
    cmd_sdr = [
        "ffmpeg", "-y", "-i", str(input_file),
        "-vf", vf_libplacebo,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
    ]
    if audio_filters:
        cmd_sdr.extend(["-af", ",".join(audio_filters), "-c:a", "aac", "-b:a", "192k"])
    else:
        cmd_sdr.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd_sdr.extend(["-fps_mode", "cfr", "-r", "30", str(out_sdr)])

    res = subprocess.run(cmd_sdr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        vf_zscale = (
            "zscale=tin=arib-std-b67:t=linear:pin=bt2020:p=bt709,"
            "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,fps=fps=30"
        )
        cmd_sdr_fallback = [
            "ffmpeg", "-y", "-i", str(input_file),
            "-vf", vf_zscale,
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        ]
        if audio_filters:
            cmd_sdr_fallback.extend(["-af", ",".join(audio_filters), "-c:a", "aac", "-b:a", "192k"])
        else:
            cmd_sdr_fallback.extend(["-c:a", "aac", "-b:a", "192k"])
        cmd_sdr_fallback.extend(["-fps_mode", "cfr", "-r", "30", str(out_sdr)])
        res_fb = subprocess.run(cmd_sdr_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res_fb.returncode != 0:
            raise RuntimeError(f"HDR to SDR conversion failed:\n{res.stderr}\nFallback:\n{res_fb.stderr}")

    cmd_proxy = [
        "ffmpeg", "-y", "-i", str(out_sdr),
        "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        str(out_proxy)
    ]
    res_prx = subprocess.run(cmd_proxy, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res_prx.returncode != 0:
        raise RuntimeError(f"Proxy generation failed:\n{res_prx.stderr}")

def analyze_exposure(video_path, duration):
    timestamps = np.linspace(0.5, max(1.0, duration - 1.0), min(20, max(3, int(duration * 2))))
    overexp_center_list = []
    underexp_center_list = []
    overexp_full_list = []
    underexp_full_list = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        for idx, ts in enumerate(timestamps):
            frame_path = Path(tmp_dir) / f"frame_{idx:02d}.png"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{ts:.2f}",
                "-i", str(video_path),
                "-vframes", "1",
                str(frame_path)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not frame_path.exists():
                continue

            img = Image.open(frame_path).convert("L")
            arr = np.array(img, dtype=np.float32)
            h, w = arr.shape

            y1, y2 = int(h * 0.20), int(h * 0.70)
            x1, x2 = int(w * 0.25), int(w * 0.75)
            center = arr[y1:y2, x1:x2]

            overexp_full = np.mean(arr > 250) * 100.0
            underexp_full = np.mean(arr < 5) * 100.0
            overexp_center = np.mean(center > 250) * 100.0
            underexp_center = np.mean(center < 5) * 100.0

            overexp_full_list.append(overexp_full)
            underexp_full_list.append(underexp_full)
            overexp_center_list.append(overexp_center)
            underexp_center_list.append(underexp_center)

    mean_over_center = float(np.mean(overexp_center_list)) if overexp_center_list else 0.0
    mean_under_center = float(np.mean(underexp_center_list)) if underexp_center_list else 0.0
    mean_over_full = float(np.mean(overexp_full_list)) if overexp_full_list else 0.0
    mean_under_full = float(np.mean(underexp_full_list)) if underexp_full_list else 0.0

    warning = mean_over_center > 2.0
    status = "WARN" if warning else "PASS"

    return {
        "status": status,
        "warning": warning,
        "threshold_overexposed_percent": 2.0,
        "center_face_region": {
            "overexposed_percent": round(mean_over_center, 2),
            "underexposed_percent": round(mean_under_center, 2)
        },
        "full_frame": {
            "overexposed_percent": round(mean_over_full, 2),
            "underexposed_percent": round(mean_under_full, 2)
        },
        "sampled_frames_count": len(overexp_center_list)
    }

def generate_comparison_sheet(raw_path, sdr_path, out_compare_path, duration):
    timestamps = [2.0, duration * 0.33, duration * 0.66, max(3.0, duration - 3.0)]
    rows = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        for idx, ts in enumerate(timestamps):
            raw_frame = Path(tmp_dir) / f"raw_{idx}.png"
            sdr_frame = Path(tmp_dir) / f"sdr_{idx}.png"

            cmd_raw = ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", str(raw_path), "-vframes", "1", str(raw_frame)]
            cmd_sdr = ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", str(sdr_path), "-vframes", "1", str(sdr_frame)]
            subprocess.run(cmd_raw, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(cmd_sdr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if raw_frame.exists() and sdr_frame.exists():
                img_r = Image.open(raw_frame).resize((540, 960))
                img_s = Image.open(sdr_frame).resize((540, 960))
                row = Image.new("RGB", (1080, 960))
                row.paste(img_r, (0, 0))
                row.paste(img_s, (540, 0))
                rows.append(row)

    if rows:
        final_sheet = Image.new("RGB", (1080 * 2, 960 * 2))
        final_sheet.paste(rows[0], (0, 0))
        if len(rows) > 1:
            final_sheet.paste(rows[1], (1080, 0))
        if len(rows) > 2:
            final_sheet.paste(rows[2], (0, 960))
        if len(rows) > 3:
            final_sheet.paste(rows[3], (1080, 960))
        final_sheet.save(out_compare_path)

def ingest(input_file, output_dir=None, denoise=False, compare=False):
    root = Path(__file__).resolve().parent.parent
    in_path = Path(input_file).resolve()

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found at {in_path}")

    base_name = in_path.stem
    if output_dir:
        out_dir = Path(output_dir).resolve()
    else:
        out_dir = root / "work" / "ingest"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_sdr = out_dir / f"{base_name}_sdr_cfr30.mp4"
    out_proxy = out_dir / f"{base_name}_proxy.mp4"
    out_report = out_dir / "ingest_report.json"
    out_compare = out_dir / "compare.png"

    probe = probe_video(in_path)

    if probe["is_hdr"] or probe["is_vfr"]:
        convert_hdr_to_sdr(in_path, out_sdr, out_proxy, probe, denoise=denoise)
    else:
        cmd_copy = [
            "ffmpeg", "-y", "-i", str(in_path),
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-fps_mode", "cfr", "-r", "30",
        ]
        if denoise:
            cmd_copy.extend(["-af", "highpass=f=80,lowpass=f=12000,afftdn=nf=-25", "-c:a", "aac", "-b:a", "192k"])
        else:
            cmd_copy.extend(["-c:a", "copy"])
        cmd_copy.append(str(out_sdr))
        subprocess.run(cmd_copy, check=True)

        cmd_proxy = [
            "ffmpeg", "-y", "-i", str(out_sdr),
            "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "128k",
            str(out_proxy)
        ]
        subprocess.run(cmd_proxy, check=True)

    exposure_data = analyze_exposure(out_sdr, probe["duration"])

    if compare and probe["duration"] >= 3.0:
        generate_comparison_sheet(in_path, out_sdr, out_compare, probe["duration"])

    report = {
        "source_file": str(in_path),
        "source_metadata": probe,
        "denoise_applied": denoise,
        "ingest_outputs": {
            "sdr_cfr30": str(out_sdr),
            "proxy_720p": str(out_proxy),
            "comparison_sheet": str(out_compare) if out_compare.exists() else None
        },
        "exposure_audit": exposure_data
    }

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report

def main():
    parser = argparse.ArgumentParser(description="Hardware-calibrated SDR Rec.709 Ingest and Proxy Generator")
    parser.add_argument("input_file", help="Path to raw video")
    parser.add_argument("--output_dir", "--output-dir", "-o", default=None, help="Directory for output files")
    parser.add_argument("--denoise", action="store_true", help="Apply gentle audio denoise filter")
    parser.add_argument("--compare", action="store_true", help="Generate HDR vs SDR comparison contact sheet")
    args = parser.parse_args()

    ingest(args.input_file, output_dir=args.output_dir, denoise=args.denoise, compare=args.compare)

if __name__ == "__main__":
    main()
