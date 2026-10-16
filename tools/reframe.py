#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reframe.py — Intelligent Horizontal (16:9) to Vertical (9:16) Speaker Reframing.
Uses OpenCV Haar Cascade with deadband, exponential moving average, and pan speed limiting.
Outputs reframe.json for Remotion consumption and human override.
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parent.parent

def smooth_trajectory(raw_detections: list[dict], deadband: float = 0.03, alpha: float = 0.12, max_pan_speed: float = 0.025) -> list[dict]:
    """
    Applies deadband, EMA, and max pan velocity limiting to raw face detections.
    """
    smoothed = []
    current_x = 0.5
    current_y = 0.42

    for item in raw_detections:
        frame_idx = item["frame"]
        time_sec = item["time_sec"]
        detected = item["detected"]
        raw_x = item["raw_x"]
        raw_y = item["raw_y"]

        if detected:
            # 1. Deadband threshold: if delta is small, don't move camera
            dx = raw_x - current_x
            target_x = current_x if abs(dx) < deadband else raw_x

            dy = raw_y - current_y
            target_y = current_y if abs(dy) < deadband else raw_y

            # 2. Exponential Moving Average
            ema_x = current_x + alpha * (target_x - current_x)
            ema_y = current_y + alpha * (target_y - current_y)

            # 3. Max Pan Velocity Capping
            step_x = ema_x - current_x
            if abs(step_x) > max_pan_speed:
                ema_x = current_x + math.copysign(max_pan_speed, step_x)

            step_y = ema_y - current_y
            if abs(step_y) > max_pan_speed:
                ema_y = current_y + math.copysign(max_pan_speed, step_y)

            current_x = ema_x
            current_y = ema_y
        else:
            # Hold last position (don't snap back to 0.5 abruptly)
            pass

        # Clamp within visible bounds for 9:16 crop from 16:9
        # Horizontal crop fraction is (1080/1920) / (16/9) = (9/16)/(16/9) = 0.3164
        # Safe center margin is [0.16, 0.84]
        clamped_x = max(0.16, min(0.84, current_x))
        clamped_y = max(0.20, min(0.80, current_y))

        smoothed.append({
            "frame": frame_idx,
            "time_sec": round(time_sec, 3),
            "x_center": round(clamped_x, 4),
            "y_center": round(clamped_y, 4),
            "face_detected": detected
        })

    return smoothed

def analyze_video_faces(video_path: Path, step_frames: int = 5, cascade_path: Path = None) -> list[dict]:
    if cascade_path is None or not cascade_path.exists():
        cascade_path = ROOT / "tools" / "haarcascade_frontalface_default.xml"

    face_cascade = cv2.CascadeClassifier(str(cascade_path))
    if face_cascade.empty():
        raise RuntimeError(f"Failed to load Haar Cascade from: {cascade_path}")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    is_horizontal = width > height
    print(f"Video input: {video_path.name} ({width}x{height}, {fps:.1f} fps, {total_frames} frames, horizontal={is_horizontal})")

    if not is_horizontal:
        print("Note: Input video is already vertical (9:16 or square). Reframing is not strictly required.")

    raw_detections = []
    frame_idx = 0
    multiple_faces_warnings = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step_frames == 0:
            time_sec = frame_idx / fps
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4, minSize=(60, 60))

            if len(faces) == 0:
                raw_detections.append({
                    "frame": frame_idx,
                    "time_sec": time_sec,
                    "detected": False,
                    "raw_x": 0.5,
                    "raw_y": 0.42,
                    "face_area": 0
                })
            else:
                if len(faces) > 1:
                    multiple_faces_warnings += 1
                    if multiple_faces_warnings <= 3:
                        print(f"  [WARN] Frame {frame_idx} ({time_sec:.2f}s): {len(faces)} faces detected. Selecting largest face.")

                # Pick the largest face by area
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                fx, fy, fw, fh = largest_face
                center_x = (fx + fw / 2.0) / float(width)
                center_y = (fy + fh / 2.0) / float(height)

                raw_detections.append({
                    "frame": frame_idx,
                    "time_sec": time_sec,
                    "detected": True,
                    "raw_x": center_x,
                    "raw_y": center_y,
                    "face_area": fw * fh
                })

        frame_idx += 1

    cap.release()

    if multiple_faces_warnings > 3:
        print(f"  [WARN] Total {multiple_faces_warnings} frames had multiple faces. All reframed to largest speaker face.")

    return raw_detections

def reframe_video(video_path: str, out_json: str, step_frames: int = 5, deadband: float = 0.03, alpha: float = 0.12, max_pan_speed: float = 0.025):
    v_path = Path(video_path).resolve()
    if not v_path.exists():
        raise FileNotFoundError(f"Video not found: {v_path}")

    out_p = Path(out_json).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)

    raw = analyze_video_faces(v_path, step_frames=step_frames)
    smoothed = smooth_trajectory(raw, deadband=deadband, alpha=alpha, max_pan_speed=max_pan_speed)

    data = {
        "source_video": str(v_path),
        "aspect_ratio": "16:9",
        "target_aspect_ratio": "9:16",
        "crop_scale_factor": 1.778,
        "resolution_loss_notice": "Full HD 1080p horizontal (1920x1080) cropped to 9:16 yields 608x1080 px, upscaled ~1.78x. Recommend 4K source (3840x2160) for native 1080x1920 delivery.",
        "settings": {
            "step_frames": step_frames,
            "deadband": deadband,
            "alpha": alpha,
            "max_pan_speed": max_pan_speed
        },
        "keyframes_count": len(smoothed),
        "keyframes": smoothed
    }

    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Reframe trajectory saved to: {out_p} ({len(smoothed)} keyframes)")
    return data

def main():
    parser = argparse.ArgumentParser(description="Reframe 16:9 Horizontal Video to 9:16 Vertical with Face Tracking & Smoothing")
    parser.add_argument("input_video", help="Path to input video file")
    parser.add_argument("--out", "-o", required=True, help="Path to output reframe.json")
    parser.add_argument("--step", type=int, default=5, help="Sample every N frames (default 5)")
    parser.add_argument("--deadband", type=float, default=0.03, help="Deadband threshold in normalized width (default 0.03)")
    parser.add_argument("--alpha", type=float, default=0.12, help="Smoothing alpha (default 0.12)")
    parser.add_argument("--max_pan_speed", type=float, default=0.025, help="Max pan velocity limit per step (default 0.025)")
    args = parser.parse_args()

    reframe_video(args.input_video, args.out, step_frames=args.step, deadband=args.deadband, alpha=args.alpha, max_pan_speed=args.max_pan_speed)

if __name__ == "__main__":
    main()
