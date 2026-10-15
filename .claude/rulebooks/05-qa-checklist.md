# 05. Quality Assurance & Inspection Checklist

## 1. The Mandatory 6-Point Inspection
Before any render is submitted or marked complete, it must strictly pass all 6 inspection gates:

1. **No Duplicate or Re-triggering Animations**:
   - Check all `<Sequence>` and `spring()` hooks.
   - Animations must never reset, glitch, or fire twice accidentally on loop or re-render.
2. **No Sub-Second Flashing Graphics**:
   - Every on-screen graphic, card, or stat badge must stay visible for a **minimum of 15 frames (0.5s)**.
   - Never flash cards for 3-5 frames unless deliberately simulating a strobe effect.
3. **Strict Safe Zone Compliance**:
   - All text, icons, cards, and caption tokens must strictly lie within:
     `x: 100..980px`, `y: 220..1540px`.
   - Never allow words to overflow below `y: 1540` where native platform captions overlap.
4. **Calibrated Audio Levels**:
   - Master integrated loudness: `-14.0 LUFS (±1.0 LUFS)`.
   - Voiceover peak: `-6.0 dB` to `-3.0 dB`.
   - SFX: `-12.0 dB` to `-8.0 dB`.
   - Background Music: `-24.0 dB` to `-20.0 dB`.
   - Master True Peak: `<= -1.0 dBTP` (zero clipping).
5. **Color Contrast & Readability**:
   - Minimum WCAG AA 4.5:1 contrast ratio between text and its immediate background.
   - For light text over variable footage, enforce drop shadows or backdrop blur cards.
6. **Constant Frame Rate (CFR 30/60 FPS)**:
   - Zero dropped frames, zero stuttering, zero VFR drift.

---

## 2. Technical Inspection Commands (FFmpeg & FFprobe)

### Stream Validation:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -of json out/final_video.mp4
```

### Black Frame Detection:
```bash
ffmpeg -i out/final_video.mp4 -vf "blackdetect=d=0.08:pix_th=0.10" -an -f null - 2>&1 | grep -E "black_start|black_duration"
```

### Frozen Frame Detection:
```bash
ffmpeg -i out/final_video.mp4 -vf "freezedetect=n=-60dB:d=0.8" -an -f null - 2>&1 | grep -E "freeze_start|freeze_duration"
```

### Audio Loudness Normalization Check:
```bash
ffmpeg -i out/final_video.mp4 -af "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json" -f null - 2>&1 | tail -n 25
```
