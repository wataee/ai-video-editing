# 🎬 AI Video Editing — Viral Automation Engine

Automated short-form video editing pipeline powered by **Claude / Antigravity**, **Adobe After Effects (MCP)**, **Remotion**, and the production standards of **Joseph (Ultimate Editors)** and **Mahabur Rahman (@mahdibgfx)**.

---

## 🚀 Key Features

* **Live After Effects MCP Bridge:** Real-time bi-directional IPC control of Adobe After Effects 2026. Zero GUI manual clicking — automated cuts, keyframing, typography, effects, and frame capture.
* **Joseph / Ultimate Editors Production Standards:**
  * Strict 3-family sound design (`Whooshes`, `Textures`, `Risers & Hits`) with standardized target decibels (`-12 dB`, `-6.5 dB`, `-5 dB`, `-19 dB`).
  * 4-pass sequential editing workflow.
  * 4 core animation categories: `Text-Centric`, `Object-Centric`, `Character-Centric`, `Video-Centric`.
* **The 2-Font Viral Formula (Sans + Script):**
  * Primary hook word in bold 3D geometric sans (`Montserrat Black`) with bevel, drop shadow, and neon bloom.
  * Overlapping secondary word in expressive brush script (`Caveat Bold`) with a -9° negative tilt.
* **Color Science & HDR Ingest:**
  * Native iPhone Apple Log / Dolby Vision BT.2020 HLG to SDR Rec.709 tonemapping via `libplacebo` and `BT.2390`.
  * Studio background vignette falloff for subject separation.

---

## 📂 Asset Library Taxonomy (`assets/`)

```text
assets/
├── 01_SFX/                          # Broadcast 48,000 Hz WAV audio library
│   ├── 01_whooshes/                 # Movement (zooms, pans, slides) -> -12 dB
│   │   ├── deep_voice/              # Textured sci-fi low sweeps (default)
│   │   ├── hollow/                  # Resonant whooshes for standard slides
│   │   ├── futuristic/              # Rapid high-tech swooshes
│   │   ├── organic_wind/            # Gentle air for camera drifts
│   │   └── transitions/             # Spacey scene-to-scene transitions
│   ├── 02_textures/                 # Non-sliding events -> -6.5 dB
│   │   ├── pops/                    # UI & graphics pop-ups
│   │   ├── clicks_ui/               # Tactile buttons & toggles
│   │   ├── gears_typewriter/        # Letter-by-letter mechanical reveals
│   │   ├── sci_fi_hits/             # Impact reveals for new elements
│   │   └── camera_shutter/          # Shutter clicks on fast cuts
│   └── 03_risers_hits/              # Anticipation & release -> -5 dB
│       ├── sharp_bass_risers/       # Punchy low pitch bends (5s post-hook)
│       ├── metallic_risers/         # Shimmering tension builds
│       ├── suck_back_risers/        # Reverse crescendo into drops
│       └── impact_hits/             # Cinematic booms under risers
├── 02_FONTS/
│   ├── 01_sans/                     # Montserrat Black, Inter, Oswald, Rubik
│   └── 02_script/                   # Caveat Bold (Cyrillic + Latin), Segoe Script
├── 03_GRAPHICS/
│   ├── 01_overlays/                 # 35mm film grain loop, tech grids, safe zones
│   ├── 02_objects_3d/               # Verified badges, callout arrows, icons
│   └── 03_studio_lighting/          # Studio vignette masks & ambient bloom
├── 04_PRESETS/
│   ├── ae_expressions/             # Spring bounce overshoot, cascade delay
│   └── color_luts/                  # Rec.709 BT.2390 tonemapping curves
└── 05_RULES/
    ├── CLAUDE_EDITING_SYSTEM_RULES.md # Complete guidelines for AI editors
    └── catalog.json                 # Machine-readable asset manifest
```

---

## 🧠 System Rules for AI Agents (`GEMINI.md`)

The repository root includes `GEMINI.md`, which enforces:
1. **Rule of Fonts:** Always pair heavy Sans + expressive Script. Never use plain multi-line subtitles.
2. **Rule of Levels:** Dialogue (0 dB) > Risers (-5 dB) > Textures (-6.5 dB) > Whooshes (-12 dB) > Music (-19 dB).
3. **Rule of Placement:** Whoosh peak aligns to the fastest frame. Textures align to event frames. Risers end on transition cuts.
4. **Order of Operations:** Pass 1 (Whooshes) → Pass 2 (Textures) → Pass 3 (Risers/Hits) → Pass 4 (Music).

---

## 🛠 Tech Stack

* **Automation & Scripting:** Node.js (ESM), Python 3.12+, ExtendScript (JSX).
* **Video Engines:** Adobe After Effects 2026, Remotion, FFmpeg 9.0 (`libplacebo`).
* **AI & Transcription:** Faster-Whisper, Claude, Gemini.

---

## 📜 License

MIT License. Designed for automated high-retention video production.
