---
name: video-editor
description: Production-ready 9:16 vertical video editing engine based on Remotion and viral storytelling rules.
---

# Video Editor Engine (9:16)

This skill governs the end-to-end production of high-retention, broadcast-quality vertical short-form video (TikTok, Reels, Shorts) inside the Remotion environment.

## 1. Modular Rulebooks
Always reference and strictly adhere to the modular rulebooks located in `.claude/rulebooks/`:
- `01-hooks-and-script.md`: 1 video = 1 idea, outlier hooks, fact checking.
- `02-cut-and-audio-sync.md`: Silence removal, clean retake filtering, lip-sync offset, dB loudness.
- `03-beat-map-and-planning.md`: Beat mapping, 4-10s shot segmentation, camera rig motion, parallel sub-prompts.
- `04-visual-styles-and-safe-zones.md`: 9:16 geometry (1080x1920, x: 100..980, y: 220..1540), visual languages.
- `05-qa-checklist.md`: The mandatory 6-point pre-render inspection.
- `06-self-learning-notes.md`: Continuous user corrections and preference bank.
- `07-creator-style-presets.md`: 5 Creator archetypes (`ali-minimal-workspace`, `gadzhi-noir-luxury`, `vox-editorial-data`, `apple-liquid-glass`, `hormozi-kinetic-punch`).
- `08-typography-pairings.md`: Typography scales and pairing matrix.
- `09-sfx-choreography.md`: Visual-to-SFX mapping, timing offsets, 3-layer sound design.
- `10-hook-patterns.md`: The 6 visual hook archetypes.

## 2. Component Toolset (`src/components/`)
Use the parametric, reusable Remotion components:
- `SafeZoneContainer`: Enforces strict 9:16 layout bounds and optional debug overlay.
- `CameraRig`: Continuous procedural motion (`push-in`, `push-out`, `pan-left`, `pan-right`, `static-fade`).
- `LiquidGlassCard`: Frosted glass modal with optional chroma green-screen mode.
- `VoxBarChart`: High-impact spring-driven data visualization.
- `NumberTicker`: Fluid numeric counter with locale formatting and unit suffixes.
- `WordByWordCaptions`: Frame-accurate karaoke captions styled per archetype.
- `SfxTrigger`: Synchronized audio trigger linking directly to cataloged assets.

## 3. Strict Development Rule
- **ZERO COMMENTS IN CODE FILES**: Never emit code comments (`//`, `/* */`, `#`) in `.ts`, `.tsx`, `.js`, `.mjs`, or `.json` files.
