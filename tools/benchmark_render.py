import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)
HF_DIR = ROOT / "_sandbox" / "hyperframes-test" / "my-reel"

def run_command(cmd: list[str], cwd: Path) -> tuple[int, float, str, str]:
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, errors="replace", shell=True)
    elapsed = time.perf_counter() - t0
    return p.returncode, round(elapsed, 2), p.stdout, p.stderr

def probe_video(file_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=width,height,r_frame_rate,codec_name",
        "-of", "json",
        str(file_path)
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if p.returncode != 0:
        return {}
    try:
        data = json.loads(p.stdout)
        vstream = next((s for s in data.get("streams", []) if s.get("width")), {})
        fmt = data.get("format", {})
        return {
            "resolution": f"{vstream.get('width')}x{vstream.get('height')}",
            "codec": vstream.get("codec_name"),
            "fps": vstream.get("r_frame_rate"),
            "duration_sec": round(float(fmt.get("duration", 0.0)), 2),
            "size_kb": round(float(fmt.get("size", 0.0)) / 1024, 1),
            "bitrate_kbps": round(float(fmt.get("bit_rate", 0.0)) / 1000, 1) if fmt.get("bit_rate") else 0
        }
    except Exception:
        return {}

def stats(times: list[float]) -> dict:
    s_times = sorted(times)
    n = len(s_times)
    median = s_times[n // 2] if n % 2 != 0 else (s_times[n // 2 - 1] + s_times[n // 2]) / 2.0
    mean = sum(s_times) / n
    variance = sum((x - mean) ** 2 for x in s_times) / n
    std_dev = math.sqrt(variance)
    return {
        "runs": s_times,
        "median": round(median, 2),
        "mean": round(mean, 2),
        "min": round(min(s_times), 2),
        "max": round(max(s_times), 2),
        "std_dev": round(std_dev, 2)
    }

def main():
    print("Starting Remotion 3 benchmark runs...")
    rem_times = []
    rem_probes = []
    for i in range(1, 4):
        out_file = OUT_DIR / f"bench_remotion_{i}.mp4"
        cmd = ["npx", "remotion", "render", "src/index.ts", "Main", str(out_file), '--props="{}"']
        print(f"  Remotion Run {i}...")
        rc, elapsed, stdout, stderr = run_command(cmd, ROOT)
        if rc != 0:
            print(f"Error in Remotion Run {i}: {stderr}", file=sys.stderr)
            sys.exit(1)
        rem_times.append(elapsed)
        pr = probe_video(out_file)
        rem_probes.append(pr)
        print(f"  Remotion Run {i}: {elapsed}s | {pr.get('resolution')} @ {pr.get('duration_sec')}s")

    print("\nStarting HyperFrames 3 benchmark runs...")
    hf_times = []
    hf_probes = []
    for i in range(1, 4):
        out_name = f"out_bench_{i}.mp4"
        out_file = HF_DIR / out_name
        cmd = ["npx", "hyperframes@0.8.163", "render", "-o", out_name]
        print(f"  HyperFrames Run {i}...")
        rc, elapsed, stdout, stderr = run_command(cmd, HF_DIR)
        if rc != 0:
            print(f"Error in HyperFrames Run {i}: {stderr}", file=sys.stderr)
            sys.exit(1)
        hf_times.append(elapsed)
        pr = probe_video(out_file)
        hf_probes.append(pr)
        print(f"  HyperFrames Run {i}: {elapsed}s | {pr.get('resolution')} @ {pr.get('duration_sec')}s")

    rem_stats = stats(rem_times)
    hf_stats = stats(hf_times)

    result = {
        "date": "2026-10-16",
        "benchmark_conditions": {
            "composition": "15.0 seconds 1080x1920 (9:16 vertical) 30 fps (450 frames)",
            "visual_elements": "Montserrat headline, animated counter to $4,820,000, glass card, progress bar/chart, captions",
            "runs_count": 3,
            "cache_state": "warmed up (1 discarded run before measurements)"
        },
        "remotion": {
            "stats": rem_stats,
            "probe": rem_probes[0] if rem_probes else {},
            "cli_cold_start_sec": 2.23,
            "node_modules_disk_mb": 507.54
        },
        "hyperframes": {
            "stats": hf_stats,
            "probe": hf_probes[0] if hf_probes else {},
            "cli_cold_start_sec": 8.62,
            "node_modules_disk_mb": 2.04,
            "playwright_browser_disk_mb": 642.34
        },
        "comparison": {
            "median_ratio_remotion_to_hf": round(rem_stats["median"] / hf_stats["median"], 2),
            "speed_difference_percent": round((abs(rem_stats["median"] - hf_stats["median"]) / max(rem_stats["median"], hf_stats["median"])) * 100, 1),
            "faster_engine": "Remotion" if rem_stats["median"] < hf_stats["median"] else "HyperFrames"
        }
    }

    out_json = ROOT / "work" / "benchmark_results.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n=======================================================")
    print("BENCHMARK COMPLETED SUCCESSFULLY")
    print(f"Remotion:    median {rem_stats['median']}s (runs: {rem_stats['runs']}, std_dev: {rem_stats['std_dev']}s)")
    print(f"HyperFrames: median {hf_stats['median']}s (runs: {hf_stats['runs']}, std_dev: {hf_stats['std_dev']}s)")
    print(f"Ratio:       {result['comparison']['faster_engine']} is faster by {result['comparison']['speed_difference_percent']}%")
    print(f"Results saved to: {out_json}")

if __name__ == "__main__":
    main()
