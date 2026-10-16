---
name: video-editor
description: Production-ready vertical video editing engine based on Remotion, design system tokens, local assets, spring physics, and anti-slop rules.
---

# Video Editor Engine

This skill governs the end-to-end production of high-retention, broadcast-quality short-form video inside the Remotion environment.

## 1. Mandatory Workflow Rule: Beat Sheet First
- **ПЕРВЫЙ ШАГ (ОБЯЗАТЕЛЬНО):** Модель обязана первым шагом сгенерировать и согласовать покадровую структуру `beat_sheet.json` (точные тайминги сцен, кадры ударов `hit_frames`, физика переходов, смены ракурсов камеры и используемые SFX из локальной папки `assets/sfx/`).
- **БЛОКИРОВКА ГЕНЕРАЦИИ КОДА:** Категорически запрещено переходить к генерации или модификации React/Remotion компонентов до того, как структура `beat_sheet.json` выведена, проверена и утверждена пользователем (`approved: true`).

## 2. Local Design System (`.claude/design-system/`)
Always reference the codified creator visual DNA and design tokens:
- `creator-archetypes.md`: Visual DNA for Minimalist Productivity, High-Retention Noir, Vox Editorial Data, and SaaS Tech Glass.
- `typography-scale.md`: Font scale, approved local pairings (`Montserrat`, `Inter`, `Unbounded`, `Manrope`, `Caveat` from `assets/fonts/`), safe zones (`x: 100..950, y: 220..1540`, captions sweet spot `y: 1120..1380`). System fonts (`Arial`, `Roboto`) are strictly prohibited.
- `sfx-mapping.md`: Mappings from animation triggers to local `assets/sfx/` files with calibrated relative dB levels.

## 3. Modular Rulebooks (`.claude/rulebooks/`)
- `01-hooks-and-script.md`: 1 video = 1 idea, outlier hooks, fact checking.
- `02-cut-and-audio-sync.md`: Silence removal, clean retake filtering, mandatory HDR ingest, relative SFX levels.
- `03-beat-map-and-planning.md`: Beat Sheet first requirement, beat mapping, proof_source, approval gate, pre-render contact sheet.
- `04-visual-styles-and-safe-zones.md`: Safe zones and geometry (220/380/100/130).
- `05-qa-checklist.md`: The mandatory 10 fps multi-point pre-render inspection.
- `06-self-learning-notes.md`: Continuous user corrections and preference bank.
- `07-creator-style-presets.md`: Creator style archetypes.
- `08-typography-pairings.md`: Local fonts only from `assets/fonts/`. Strict ban on `Arial` and `Roboto`.
- `09-sfx-choreography.md`: SFX from `assets/sfx/` via `<Audio/>` (`AudioTrigger`) with frame-accurate timing, volume curve, and fade-out.
- `10-hook-patterns.md`: The 6 visual hook archetypes.
- `11-hook-library.md`: Outlier hook structures.
- `12-anti-slop.md`: 8 rules against cheap AI slop, procedural noise overlay (`AntiSlopOverlay`), and camera micro-drift.
- `13-ae-secondary-engine.md`: Secondary After Effects ExtendScript rules (monolithic scripts, safeApplyEffect, no exposure HDR fix).
- `14-production-pipeline.md`: The linear production pipeline with Beat Sheet gate.
- `15-upwork-ops.md`: Upwork freelance operations.
- `16-anti-mishmash-cohesion.md`: Anti-mishmash protocol and style isolation.

## 4. Parametric Components (`src/components/`)
- `AntiSlopOverlay`: Post-processing wrapper with SVG `<feTurbulence>` noise (3–5%), camera micro-drift (1.0 to 1.03), and subtle vignette.
- `AudioTrigger`: Synchronized local audio trigger linking to `assets/sfx/` with frame offset, volume envelope, and fade-out.
- `ProceduralNoiseOverlay`: Standalone SVG grain overlay against sterile vector rendering.
- `SafeZoneContainer`: Enforces strict 9:16 layout bounds and optional debug overlay.
- `CameraRig`: Continuous procedural motion with micro-drift.
- `ProofCard`: Frosted glass verification modal with spring physics and bounce-back overshoot.
- `HookHeadline`: Dynamic opening hook headline with spring physics.
- `SpeakerBadge`: Clean pill badge with animated spring entrance.
- `LiquidGlassCard`: Frosted glass modal with optional chroma green-screen mode.
- `VoxBarChart`: High-impact spring-driven data visualization.
- `NumberTicker`: Fluid numeric counter with locale formatting and unit suffixes.
- `WordByWordCaptions`: Frame-accurate karaoke captions with spring pop on active words.

## 5. Verification & Studio Inspection
- Verify frame layout using headless Remotion (`npx remotion still src/index.ts [CompName] out/qa.jpeg --frame=[N]`).
- Run generated monolithic ExtendScript scripts (`scripts/build_ae_project.jsx`) in After Effects via `File -> Scripts -> Run Script File...` wrapped in `app.beginUndoGroup("AI Video Build")`.
- Run automated QA audit via `python tools/qa.py out/final_video.mp4`.

## 6. Strict Development Rule
- **ZERO COMMENTS IN CODE FILES**: Never emit code comments (`//`, `/* */`, `#`) in `.ts`, `.tsx`, `.js`, `.mjs`, `.css`, `.json`, or `.jsx` files.
