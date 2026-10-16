# 🎬 AI Video Editing — Vertical Video Engine (v2)

Production-ready vertical short-form video editing engine (9:16) powered by **Remotion 4.x (React 19 + TypeScript)**, **FFmpeg**, and **After Effects ExtendScript** (secondary engine).

---

## 🚀 Key Features

* **Primary Engine: Remotion (React 19):** Frame-accurate parametric motion design, kinetic karaoke captions, procedural camera rigs, and automated headless rendering.
* **Secondary Engine: After Effects ExtendScript:** Driven via generated monolithic ExtendScript scripts (`scripts/build_ae_project.jsx`) executed manually via `File -> Scripts -> Run Script File...` with undo group protection and safe plugin fallbacks (`safeApplyEffect`). No MCP bridge or external daemons needed.
* **Calibrated Sound Design (Relative to Speech RMS):**
  * Hits & Risers: `−14 dB` relative to measured speech RMS.
  * Textures (Clicks, Pops): `−16 dB` relative to speech RMS.
  * Whooshes (Air sweeps): `−20 dB` relative to speech RMS.
  * Music Bed: `−22 dB` and lower with sidechain ducking.
  * Maximum 6 SFX per 30s. Zooms without sound.
* **Approved Cyrillic Typography Formula:**
  * Headline: `Montserrat` (ExtraBold / Black).
  * Body / Captions: `Manrope` or `Inter` (Regular / Medium / SemiBold).
  * Accent signature (2nd layer only): `Caveat` (Bold).
  * `TheBoldFont` is strictly prohibited.
* **Color Science & Hardware Ingest:**
  * Mandatory pre-ingest via `tools/ingest.py` (libplacebo BT.2390 or zscale to SDR Rec.709, CFR 30 fps, 720p proxy).
  * Exposure adjustment layers to "fix" HDR in AE are strictly forbidden.
* **Human-in-the-Loop Quality Assurance:**
  * Sentence-by-sentence Beat Table (`edit_plan.json`) with `line`, `visual`, `proof_source`, `camera`, `cut_motivation`, `sfx`, `why`.
  * Pre-render Contact Sheet (`contact_sheet_plan.png`).
  * Approval Gate (`approved: false` by default; final render refused until approved).
  * 10 FPS Automated Inspection (`tools/qa.py`).

---

## 📂 Asset Taxonomy (`assets/`)

```text
assets/
├── sfx/                             # Calibrated 48kHz WAV audio library
│   ├── hits/                        # Sub bass drops, semantic punches (-14 dB)
│   ├── risers/                      # Pre-hook and climax risers (-14 dB)
│   ├── textures/                    # Friction, scratches (-16 dB)
│   ├── clicks/                      # UI toggles, switches (-16 dB)
│   ├── pops/                        # Modal popups, clean bubbles (-16 dB)
│   ├── glitches/                    # Digital accents (-16 dB)
│   ├── whooshes/                    # Fast air & scene transitions (-20 dB)
│   └── ambience/                    # Low drones
├── fonts/                           # OFL fonts with 100% Cyrillic support
│   ├── Montserrat/
│   ├── Manrope/
│   ├── Inter/
│   ├── Oswald/
│   ├── Rubik/
│   └── Caveat/
└── overlays/
    └── film_grain/                  # 35mm film grain loop (1080x1920)
```

---

## 🛠️ Essential Commands

```bash
# Ingest HDR video to SDR Rec.709 + CFR 30 fps + proxy
python tools/ingest.py path/to/raw_video.MOV

# Transcribe audio with glossary
tools\transcribe.bat work/ingest/video_sdr_cfr30.mp4 --glossary clients/client/glossary.txt

# Generate Beat Table and Contact Sheet
python tools/beat_table.py work/plan/edit_plan.json
python tools/plan_contact_sheet.py work/plan/edit_plan.json

# Draft Remotion preview (half-res)
npm run draft

# Calibrate and mix audio
python tools/mix.py work/audio/voice.wav work/plan/edit_plan.json

# 10 FPS QA Inspection
python tools/qa.py out/final_video.mp4 work/plan/edit_plan.json

# Final render (requires approved: true in edit_plan.json)
npm run render:clip -- [CompositionName] out/final_video.mp4
```
