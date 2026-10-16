# 14. Production Pipeline & Human-in-the-Loop Standard

## 1. The 9-Stage Linear Pipeline
1. **Ingest (tools/ingest.py)**: Detect color transfer (HLG/PQ/BT.709), convert HDR to SDR Rec.709 (BT.2390/hable), enforce CFR 30 fps, generate 720p proxy and exposure report.
2. **Audio Transcription & Analysis (tools/transcribe.bat)**: Extract audio, run faster-whisper with speaker glossary, output word-level JSON.
3. **Script Lock & Clean Takes (tools/compact_transcript.py)**: Discard false starts, eliminate duplicate takes (keep last clean take), select single core thesis.
4. **Beat Sheet JSON Generation (beat_sheet.json / tools/plan_scaffold.py)**: ПЕРВЫМ ШАГОМ выводится JSON-структура таймлайна: тайминги сцен, точные кадры ударов (`hit_frames`), смены ракурсов камеры и точки запуска SFX из `assets/sfx/`.
5. **Plan Contact Sheet (tools/plan_contact_sheet.py)**: Render visual storyboard stills for every beat before committing to motion graphics.
6. **Human Approval Gate**: Review `beat_table.md` and `contact_sheet_plan.png`. Toggle `"approved": true` in `edit_plan.json`. До утверждения писать код компонентов запрещено.
7. **Draft Rendering (npm run draft)**: Build composition section-by-section using Remotion components (`src/components/`) with spring physics (damping/stiffness/mass + 2-5% overshoot), camera micro-drift (1.0 -> 1.03), and procedural noise overlay `<ProceduralNoiseOverlay/>` (3-5% opacity). Render half-resolution preview.
8. **Automated 10 FPS QA Inspection (tools/qa.py)**: Inspect every 3rd frame (10 fps) for replayed animations, flicker < 0.5s, reading speed, face occlusion, duplicate words, black/frozen frames, safe zones.
9. **Final Sound Mix & Master Render (tools/mix.py + npm run render:clip)**: Calibrate SFX relative to speech RMS, loudnorm to -14 LUFS, render master MP4.
