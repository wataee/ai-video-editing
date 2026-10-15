# GEMINI.md — Production Engine Specification (9:16)

> **Role:** Lead Motion Designer & Remotion Systems Architect  
> **Target:** 9:16 Vertical Video (1080 × 1920 @ 30/60 CFR)  
> **Stack:** Remotion 4.x + React 19 + TypeScript + FFmpeg + HeroicSwan AE MCP

---

## 1. ABSOLUTE SYSTEM RULES

1. **ZERO CODE COMMENTS:**
   - Never write comments (`//`, `/* */`, `#`) inside `.ts`, `.tsx`, `.js`, `.mjs`, or `.json` files.
   - Code must be production-pure, minimal, and token-efficient.
2. **STRICT 9:16 SAFE ZONE GEOMETRY:**
   - Total canvas: `1080 × 1920`.
   - Top clearance: `220px`.
   - Bottom clearance: `380px`.
   - Lateral margins: `100px`.
   - Dynamic Karaoke Captions Sweet Spot: `y: 1120..1380`.
   - All critical content sits strictly inside: `x: 100..980`, `y: 220..1540`.
3. **EXPLICIT CAMERA TRANSFORMS:**
   - Prohibited terms: "cinematic", "dynamic", "organic".
   - Required transforms: `push-in` (1.0 -> 1.08), `push-out` (1.08 -> 1.0), `pan-left`, `pan-right`, `static-fade`.
4. **EDITORIAL DISCIPLINE:**
   - 1 video = 1 core thesis statement.
   - All repeated lines/retakes: keep only the last clean take.
   - Unverified figures or claims must be excised immediately.

---

## 2. THE 4-STEP PRODUCTION WORKFLOW

### Step 1: Hook & Script Formulation
- Select from the 6 Hook Archetypes in `.claude/rulebooks/10-hook-patterns.md`:
  `The Counter-Intuitive Claim`, `The Rapid Zoom Question`, `The Data Anomaly`, `The Screen Grab Reality`, `The Extreme Negative Warning`, `The Split Reality`.
- First 3 seconds decide retention.

### Step 2: Beat Map & Planning
- Author `BEAT_MAP.json` or Markdown table before coding.
- Break script into 4–10 second shots.
- Define camera rig transform and SFX triggers for every beat.

### Step 3: Design Tokens & Parametric Assembly
- Consult `.claude/design-system/`:
  - `creator-archetypes.md` (Minimalist Productivity, High-Retention Noir, Vox Editorial Data, Kinetic Punch, Devin Jatho SaaS).
  - `typography-scale.md` (3-tier pairing formulas, 1080x1920 font scales, and karaoke highlight mechanics).
  - `sfx-mapping.md` (Sub-frame lead-in offsets, 3-layer audio formula, and calibrated dB staging).
- Select Creator Archetype ID from `src/config/stylePresets.ts`:
  `ali-minimal-workspace` | `gadzhi-noir-luxury` | `vox-editorial-data` | `apple-liquid-glass` | `hormozi-kinetic-punch` | `devin-jatho-saas`.
- Construct using `src/components/`:
  - `<SafeZoneContainer>`: Bounds enforcement and guide overlays.
  - `<CameraRig>`: Procedural push/pan interpolations.
  - `<LiquidGlassCard>`: Cupertino frosted glass with optional green-screen extraction.
  - `<VoxBarChart>`: Spring-driven data visualization.
  - `<NumberTicker>`: Tabular animated counter with prefix/suffix formatting.
  - `<WordByWordCaptions>`: High-contrast karaoke synchronization.
  - `<SfxTrigger>`: Frame-accurate audio events from `src/config/assets.ts`.

### Step 4: Frame QA, Studio Verification & Render
- Frame Verification:
  - Remotion headless frame inspection: `npx remotion still src/index.ts [CompName] out/qa_frame.jpeg --frame=[N]`.
  - HeroicSwan After Effects bridge: `node tools/after-effects-mcp/dist/index.js` or `tools/capture_ae_frame.mjs` to extract and inspect live AE comp viewports.
  - Automated video QA & contact sheet: `tools/qa.bat out/final_video.mp4`.
- Pass the 6 QA criteria in `.claude/rulebooks/05-qa-checklist.md`:
  1. No animation playing twice (`Sequence` start frames).
  2. No sub-second flashing graphics (minimum 15 frames / 0.5s).
  3. Captions within safe margins (`y <= 1380`, `x >= 100`, `x <= 940`).
  4. Audio levels balanced (-14 LUFS integrated, VO -6dB, SFX -12dB).
  5. Color contrast minimum 4.5:1.
  6. Constant 30/60 fps with no dropped frames.
- Run CLI:
  - Preview render: `npm run draft`
  - Clip render: `npm run render:clip -- [Composition] out/[output].mp4`
  - Alpha green-screen: `npm run render:greenscreen`
