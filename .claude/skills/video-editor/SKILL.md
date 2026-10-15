---
name: video-editor
description: Production-ready 9:16 vertical video editing engine based on Remotion, design system tokens, and viral storytelling rules.
---

# Video Editor Engine (9:16)

This skill governs the end-to-end production of high-retention, broadcast-quality vertical short-form video (TikTok, Reels, Shorts) inside the Remotion environment.

## 1. Local Design System (`.claude/design-system/`)
Always reference the codified creator visual DNA and design tokens:
- `creator-archetypes.md`: Visual DNA for Minimalist Productivity (Ali Abdaal), High-Retention Noir (Iman Gadzhi), Vox Editorial Data (Johnny Harris), Kinetic Punch (Alex Hormozi), and SaaS Tech Glass (Devin Jatho).
- `typography-scale.md`: 1080x1920 font scale, 3-tier pairing formulas, dynamic karaoke rules, safe zone bounds (captions sweet spot `y: 1120..1380`).
- `sfx-mapping.md`: Mappings from animation triggers to local `assets/01_SFX/` files with sub-frame lead-in offsets and calibrated dB levels.

## 2. Modular Rulebooks (`.claude/rulebooks/`)
- `01-hooks-and-script.md`: 1 video = 1 idea, outlier hooks, fact checking.
- `02-cut-and-audio-sync.md`: Silence removal, clean retake filtering, lip-sync offset, dB loudness.
- `03-beat-map-and-planning.md`: Beat mapping, 4-10s shot segmentation, camera rig motion, parallel sub-prompts.
- `04-visual-styles-and-safe-zones.md`: 9:16 geometry (1080x1920, x: 100..980, y: 220..1540), visual languages.
- `05-qa-checklist.md`: The mandatory 6-point pre-render inspection.
- `06-self-learning-notes.md`: Continuous user corrections and preference bank.
- `07-creator-style-presets.md`: 6 Creator archetypes (`ali-minimal-workspace`, `gadzhi-noir-luxury`, `vox-editorial-data`, `apple-liquid-glass`, `hormozi-kinetic-punch`, `devin-jatho-saas`).
- `08-typography-pairings.md`: Typography scales and pairing matrix.
- `09-sfx-choreography.md`: Visual-to-SFX mapping, timing offsets, 3-layer sound design.
- `10-hook-patterns.md`: The 6 visual hook archetypes.

## 3. Parametric Components (`src/components/`)
- `SafeZoneContainer`: Enforces strict 9:16 layout bounds and optional debug overlay.
- `CameraRig`: Continuous procedural motion (`push-in`, `push-out`, `pan-left`, `pan-right`, `static-fade`).
- `LiquidGlassCard`: Frosted glass modal with optional chroma green-screen mode.
- `VoxBarChart`: High-impact spring-driven data visualization.
- `NumberTicker`: Fluid numeric counter with locale formatting and unit suffixes.
- `WordByWordCaptions`: Frame-accurate karaoke captions styled per archetype.
- `SfxTrigger`: Synchronized audio trigger linking directly to cataloged assets.

## 4. Verification & Studio Inspection
- Verify frame layout using headless Remotion (`npx remotion still src/index.ts [CompName] out/qa.jpeg --frame=[N]`).
- Verify live After Effects comps using the HeroicSwan AE MCP bridge (`tools/after-effects-mcp`) and inspection scripts (`tools/capture_ae_frame.mjs`).
- Run automated QA audit via `tools/qa.bat out/final_video.mp4`.

## 5. Strict Development Rule
- **ZERO COMMENTS IN CODE FILES**: Never emit code comments (`//`, `/* */`, `#`) in `.ts`, `.tsx`, `.js`, `.mjs`, or `.json` files.
