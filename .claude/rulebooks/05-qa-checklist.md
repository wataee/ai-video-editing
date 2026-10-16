# 05. Quality Assurance & Inspection Checklist (10 FPS)

## 1. 10 FPS Multi-Point Verification Engine
Every render undergoes automated inspection on frames sampled at 10 frames per second (every 3 frames @ 30fps) through `tools/qa.py`:

1. **Animation Replayed Twice**:
   - Compares component entrance triggers in `edit_plan.json` and timeline state.
   - Status: `PASS` / `FAIL` (flags any element unexpectedly re-animating or bouncing back).
2. **Sub-Half-Second Flickering (< 0.5s / 15 frames)**:
   - Any graphic or text staying visible for less than 15 frames is flagged.
   - Status: `PASS` / `FAIL`.
3. **Reading Speed & On-Screen Duration**:
   - Text display duration must satisfy: `duration >= max(0.8s, 0.3s * word_count)`.
   - Status: `PASS` / `FAIL`.
4. **Graphic Covering Speaker Face**:
   - Face detection (Haar cascade / MediaPipe) against graphic bounding boxes.
   - Status: `PASS` / `FAIL`.
5. **Consecutive Repeated Words**:
   - Word-level transcript analysis for accidental stammering or duplicated takes.
   - Status: `PASS` / `FAIL`.
6. **Lip-Sync & Audio-Video Alignment**:
   - Measures stream start timestamp differences and audio/video durations.
   - Status: Marked `UNVERIFIED` for human check if automated phoneme match cannot be definitively certified.

## 2. Technical Signal Inspection
- **Exposure Integrity**: Pixel brightness > 250 in central face zone must be < 2%. Total black frames (< 5) must be 0%.
- **Subtitle Contrast**: WCAG minimum 4.5:1 contrast against video background.
- **SFX Relative Loudness**: Must match mix standards (-14 dB hits/risers, -16 dB textures, -20 dB whooshes relative to speech RMS). Max 6 SFX per 30s.
- **Safe Zone Geometry**: All visual graphics must stay inside `x: 100..950`, `y: 220..1540`. Subtitles strictly `y: 1120..1380`.
