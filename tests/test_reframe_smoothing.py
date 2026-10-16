#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_reframe_smoothing.py — Unit Tests for Speaker Reframing Trajectory Smoothing.
Tests:
1. High-frequency micro-jitter (Deadband filter verification)
2. Sudden position jump / step function (Max pan speed capping verification)
3. Face detection loss / occlusion (Position hold verification)
"""

import math
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from reframe import smooth_trajectory

class TestReframeSmoothing(unittest.TestCase):

    def test_deadband_suppresses_micro_jitter(self):
        """Micro-jitter within deadband threshold (e.g. 2% amplitude) must not move the camera."""
        deadband = 0.03
        raw_detections = []
        for f in range(20):
            # Alternating jitter +/- 0.01 around 0.5 (smaller than 0.03 deadband)
            jitter = 0.01 if f % 2 == 0 else -0.01
            raw_detections.append({
                "frame": f * 5,
                "time_sec": (f * 5) / 30.0,
                "detected": True,
                "raw_x": 0.5 + jitter,
                "raw_y": 0.42,
                "face_area": 10000
            })

        smoothed = smooth_trajectory(raw_detections, deadband=deadband, alpha=0.15, max_pan_speed=0.03)

        # The camera x position should stay strictly at 0.500 because all jitter was within deadband
        for s in smoothed:
            self.assertAlmostEqual(s["x_center"], 0.5, delta=0.001,
                                   msg=f"Deadband failed to absorb micro-jitter at frame {s['frame']}")

    def test_max_pan_speed_limits_sudden_jump(self):
        """A sudden jump (e.g. from 0.5 to 0.8) must be smoothed with velocity <= max_pan_speed per step."""
        max_pan_speed = 0.025
        raw_detections = []
        # First 5 frames at 0.5
        for f in range(5):
            raw_detections.append({
                "frame": f * 5,
                "time_sec": (f * 5) / 30.0,
                "detected": True,
                "raw_x": 0.5,
                "raw_y": 0.42,
                "face_area": 10000
            })
        # Instant jump to 0.8
        for f in range(5, 15):
            raw_detections.append({
                "frame": f * 5,
                "time_sec": (f * 5) / 30.0,
                "detected": True,
                "raw_x": 0.8,
                "raw_y": 0.42,
                "face_area": 10000
            })

        smoothed = smooth_trajectory(raw_detections, deadband=0.02, alpha=0.3, max_pan_speed=max_pan_speed)

        # Verify that for every step, delta <= max_pan_speed
        for i in range(1, len(smoothed)):
            delta = abs(smoothed[i]["x_center"] - smoothed[i-1]["x_center"])
            self.assertLessEqual(delta, max_pan_speed + 1e-4,
                                 msg=f"Step at frame {smoothed[i]['frame']} exceeded max pan speed: {delta} > {max_pan_speed}")

    def test_face_disappearance_holds_last_position(self):
        """When face detection is lost, camera must hold last valid position and not jump to default 0.5."""
        raw_detections = []
        # Move speaker to x=0.7
        for f in range(10):
            raw_detections.append({
                "frame": f * 5,
                "time_sec": (f * 5) / 30.0,
                "detected": True,
                "raw_x": 0.7,
                "raw_y": 0.42,
                "face_area": 10000
            })
        # Face lost for 10 frames
        for f in range(10, 20):
            raw_detections.append({
                "frame": f * 5,
                "time_sec": (f * 5) / 30.0,
                "detected": False,
                "raw_x": 0.5,
                "raw_y": 0.42,
                "face_area": 0
            })

        smoothed = smooth_trajectory(raw_detections, deadband=0.02, alpha=0.2, max_pan_speed=0.03)

        # Position during lost detection should stay held near the position reached at frame 9
        pos_at_loss = smoothed[9]["x_center"]
        for i in range(10, 20):
            self.assertAlmostEqual(smoothed[i]["x_center"], pos_at_loss, delta=0.001,
                                   msg=f"Frame {smoothed[i]['frame']} did not hold position during face occlusion")

if __name__ == "__main__":
    unittest.main()
