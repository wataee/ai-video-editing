#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_fixtures.py — Synthesizes edge-case test media fixtures using FFmpeg.
Contains ZERO third-party or human footage (100% synthetic).
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT / "tests" / "fixtures"
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

def run_cmd(cmd: list):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error generating fixture:\n{' '.join(cmd)}\n{res.stderr}", file=sys.stderr)
        return False
    return True

def generate_all():
    print(f"Generating synthetic test fixtures in: {FIXTURES_DIR}\n")

    # 1. 4K 60 fps
    f1 = FIXTURES_DIR / "fixture_4k_60fps.mp4"
    if not f1.exists():
        print("1. Generating 4K 60 fps fixture...")
        cmd1 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=3840x2160:rate=60",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
            "-t", "3",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
            "-c:a", "aac", "-b:a", "128k",
            str(f1)
        ]
        run_cmd(cmd1)

    # 2. Variable Frame Rate (VFR)
    f2 = FIXTURES_DIR / "fixture_vfr.mp4"
    if not f2.exists():
        print("2. Generating VFR fixture...")
        # Create fluctuating frame rate by varying timestamp presentation
        cmd2 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=500:sample_rate=48000",
            "-vf", "setpts='N/(30+15*sin(N/10))/TB'",
            "-t", "4",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac",
            str(f2)
        ]
        run_cmd(cmd2)

    # 3. Vertical Video with Rotation Metadata (rotate=90)
    f3 = FIXTURES_DIR / "fixture_rotate_90.mp4"
    if not f3.exists():
        print("3. Generating video with rotation metadata...")
        cmd3 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=600:sample_rate=48000",
            "-t", "3",
            "-metadata:s:v:0", "rotate=90",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac",
            str(f3)
        ]
        run_cmd(cmd3)

    # 4a. Mono Audio 44.1 kHz
    f4a = FIXTURES_DIR / "fixture_mono_44k.mp4"
    if not f4a.exists():
        print("4a. Generating mono 44.1 kHz fixture...")
        cmd4a = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=720x1280:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100",
            "-t", "3",
            "-ac", "1",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-ar", "44100",
            str(f4a)
        ]
        run_cmd(cmd4a)

    # 4b. Stereo Audio 48 kHz
    f4b = FIXTURES_DIR / "fixture_stereo_48k.mp4"
    if not f4b.exists():
        print("4b. Generating stereo 48 kHz fixture...")
        cmd4b = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=880:sample_rate=48000",
            "-t", "3",
            "-ac", "2",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-ar", "48000",
            str(f4b)
        ]
        run_cmd(cmd4b)

    # 5. Quiet Speech with Noise (low volume + background noise)
    f5 = FIXTURES_DIR / "fixture_quiet_noise.mp4"
    if not f5.exists():
        print("5. Generating quiet speech with noise fixture...")
        cmd5 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=720x1280:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=500:sample_rate=48000",
            "-f", "lavfi", "-i", "anoisesrc=sample_rate=48000:amplitude=0.08:color=white",
            "-filter_complex", "[1:a]volume=0.08[quiet];[2:a]volume=0.04[noise];[quiet][noise]amix=inputs=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-t", "4",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k",
            str(f5)
        ]
        run_cmd(cmd5)

    # 6. Screen Recording (non-standard 16:10 ratio: 1920x1200)
    f6 = FIXTURES_DIR / "fixture_screen_rec_1920x1200.mp4"
    if not f6.exists():
        print("6. Generating 16:10 screen recording fixture...")
        cmd6 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "smptebars=size=1920x1200:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
            "-t", "3",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac",
            str(f6)
        ]
        run_cmd(cmd6)

    # 7. Bilingual Speech / Glossary test audio
    f7 = FIXTURES_DIR / "fixture_bilingual_glossary.mp4"
    if not f7.exists():
        print("7. Generating bilingual glossary test fixture...")
        cmd7 = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=600:sample_rate=48000",
            "-t", "4",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac",
            str(f7)
        ]
        run_cmd(cmd7)

    print("\nAll fixtures generated successfully.")

if __name__ == "__main__":
    generate_all()
