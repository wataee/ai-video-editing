# CLAUDE.md — Vertical Video Editing Engine (9:16)

> **Workstation Root:** `C:\Users\timur\Videos\AI-Video-Editing`  
> **Engine:** Remotion 4.x + React 19 + TypeScript + FFmpeg + HeroicSwan AE MCP  
> **Target Format:** Strict 9:16 Vertical Video (1080 × 1920, 30/60 CFR)  
> **Core Role:** Senior Video Editor & Technical Motion Director

---

## 1. ABSOLUTE SYSTEM CONSTRAINTS

1. **ZERO COMMENTS IN CODE FILES:**
   - **NEVER** write comments (`//`, `/* */`, `#`) inside `.ts`, `.tsx`, `.js`, `.mjs`, or `.json` files.
   - Code must be self-explanatory, clean, and token-efficient.
2. **STRICT 9:16 SAFE ZONES:**
   - Dimensions: `1080 × 1920`.
   - Top Exclusion Zone: `220px` (profile, search, audio bar).
   - Bottom Exclusion Zone: `380px` (native UI captions, username, sound badge).
   - Lateral Margins: `100px` (engagement buttons on right, clearance on left).
   - Content Container: strictly `x: 100..980`, `y: 220..1540`.
   - Dynamic Karaoke Captions Sweet Spot: `y: 1120..1380`.
   - All components must be wrapped in `<SafeZoneContainer>`.
3. **EXPLICIT MOTION ONLY:**
   - Never use vague words like "cinematic" or "dynamic".
   - Only use explicit camera transforms: `push-in` (1.0 -> 1.08), `push-out` (1.08 -> 1.0), `pan-left`, `pan-right`, `static-fade`.
4. **VERIFIED DATA & 1 VIDEO = 1 IDEA:**
   - Every video must have exactly 1 core thesis.
   - Every number, statistic, or date must be verified against source data or cut.

---

## 2. THE 4-STEP PRODUCTION WORKFLOW

```
[ Step 1: Hook & Script ] ➔ [ Step 2: Beat Map ] ➔ [ Step 3: Design Tokens & Assembly ] ➔ [ Step 4: Frame QA & Render ]
```

### Step 1: Transcript & Hook Formulation
- Reference: `.claude/rulebooks/01-hooks-and-script.md` & `10-hook-patterns.md`.
- Select one of the 6 proven hook archetypes for the first 3 seconds:
  `The Counter-Intuitive Claim`, `The Rapid Zoom Question`, `The Data Anomaly`, `The Screen Grab Reality`, `The Extreme Negative Warning`, `The Split Reality`.
- Eliminate retakes: keep **only the last clean take** of any repeated line.

### Step 2: Beat Map & Planning
- Reference: `.claude/rulebooks/03-beat-map-and-planning.md`.
- Generate a `BEAT_MAP.json` or Markdown table before writing code.
- Segment video into 4–10 second beats.
- Map every sentence to: visual component, explicit camera motion, and cataloged SFX trigger.
- When working on large compositions, generate isolated parallel sub-prompts for specific clips.

### Step 3: Parametric Assembly & Design Tokens
- Automatically consult `.claude/design-system/`:
  - `creator-archetypes.md` (Minimalist Productivity, High-Retention Noir, Vox Editorial Data, Kinetic Punch, Devin Jatho SaaS).
  - `typography-scale.md` (3-tier pairing formulas, 1080x1920 font scales, and karaoke highlight mechanics).
  - `sfx-mapping.md` (Sub-frame lead-in offsets, 3-layer audio formula, and calibrated dB staging).
- Select a Creator Style Preset ID from `src/config/stylePresets.ts`:
  - `ali-minimal-workspace`
  - `gadzhi-noir-luxury`
  - `vox-editorial-data`
  - `apple-liquid-glass`
  - `hormozi-kinetic-punch`
  - `devin-jatho-saas`
- Build compositions using pre-built components in `src/components/`:
  - `<SafeZoneContainer>`
  - `<CameraRig>`
  - `<LiquidGlassCard>`
  - `<VoxBarChart>`
  - `<NumberTicker>`
  - `<WordByWordCaptions>`
  - `<SfxTrigger>`
- Use typed asset paths from `src/config/assets.ts` and pairings from `src/config/sfxMatrix.ts`.

### Step 4: Frame QA, Studio Verification & Render
- Reference: `.claude/rulebooks/05-qa-checklist.md`.
- Frame Layout Verification:
  - Remotion headless frame inspection: `npx remotion still src/index.ts [CompName] out/qa_frame.jpeg --frame=[N]`.
  - HeroicSwan After Effects bridge: `node tools/after-effects-mcp/dist/index.js` or `tools/capture_ae_frame.mjs` / `tools/capture_all_scenes.mjs` to extract and inspect live AE comp viewports.
  - Automated video QA & contact sheet: `tools/qa.bat out/final_video.mp4` generates `qa.summary.json` and `contact_sheet.png`.
- Enforce the 6-Point Inspection:
  1. No duplicate or re-triggering animations (`Sequence` / `spring` start frames).
  2. No sub-second flashing graphics (minimum duration >= 15 frames / 0.5s).
  3. Captions within safe margins (`y <= 1380`, `x >= 100`, `x <= 940`).
  4. Audio levels balanced (-14 LUFS integrated, VO -6dB, SFX -12dB).
  5. Color contrast minimum 4.5:1.
  6. Constant 30/60 fps with no dropped frames.
- Run render scripts via `package.json`:
  - Fast preview: `npm run draft`
  - Isolated clip: `npm run render:clip -- [CompositionName] out/[output].mp4`
  - Alpha green-screen extraction: `npm run render:greenscreen`

---

## 3. ENGINE REPOSITORY MAP

```
C:\Users\timur\Videos\AI-Video-Editing\
├── .claude/
│   ├── design-system/
│   │   ├── creator-archetypes.md
│   │   ├── typography-scale.md
│   │   └── sfx-mapping.md
│   ├── rulebooks/
│   │   ├── 01-hooks-and-script.md
│   │   ├── 02-cut-and-audio-sync.md
│   │   ├── 03-beat-map-and-planning.md
│   │   ├── 04-visual-styles-and-safe-zones.md
│   │   ├── 05-qa-checklist.md
│   │   ├── 06-self-learning-notes.md
│   │   ├── 07-creator-style-presets.md
│   │   ├── 08-typography-pairings.md
│   │   ├── 09-sfx-choreography.md
│   │   └── 10-hook-patterns.md
│   └── skills/
│       └── video-editor/SKILL.md
├── assets/
│   ├── 01_SFX/ (48kHz broadcast WAV library)
│   ├── 02_FONTS/ (Montserrat, Inter, Oswald, Rubik, Caveat, Segoe Script)
│   └── 03_GRAPHICS/ (Grids, film grain, 3D badges)
├── src/
│   ├── components/ (SafeZoneContainer, CameraRig, LiquidGlassCard, VoxBarChart, NumberTicker, WordByWordCaptions, SfxTrigger)
│   ├── config/ (assets.ts, stylePresets.ts, sfxMatrix.ts)
│   ├── Root.tsx
│   └── index.ts
├── tools/
│   ├── after-effects-mcp/ (HeroicSwan AE Model Context Protocol bridge)
│   ├── capture_ae_frame.mjs
│   ├── capture_all_scenes.mjs
│   └── qa.bat / qa.py
├── ASSETS_INDEX.json
├── package.json
└── remotion.config.ts
```
