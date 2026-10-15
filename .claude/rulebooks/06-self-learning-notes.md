# 06. Self-Learning Memory & User Corrections

## Purpose
This file acts as a persistent memory bank for user feedback, style corrections, and aesthetic preferences.
Whenever the user specifies a correction (e.g. "don't make captions yellow", "increase chart padding", "use lower whoosh volume"), record it here immediately to prevent making the same mistake in subsequent sessions.

---

## Active User Directives & Preferences

### 1. Zero Code Comments
- **Rule**: Never write comments (`//`, `/* */`, `#`) inside code files (`.ts`, `.tsx`, `.js`, `.mjs`, `.json`).
- **Rationale**: Strict instruction from user to keep files clean, token-efficient, and production-ready.

### 2. High Production Aesthetic vs. "AI Slop"
- **Disallowed**: Bouncing emojis over every word, arbitrary zoom cuts every 0.8 seconds, generic stock videos of smiling people in offices, aggressive repetitive whoosh sounds on every slide.
- **Enforced**: Clean, high-end motion design inspired by Vox, Apple keynote UI, Mahabur Rahman, and Joseph editing styles.

### 3. Safe Zones
- Respect platform UI boundaries: 220px top margin, 380px bottom margin, 100px lateral margins.

---

## Log of Corrections & Iterations
| Date | User Feedback / Observation | Action Taken / Rule Established |
|---|---|---|
| 2026-10-15 | "получилось полное говно даже хуже нейрослопа... ожидал увидеть что то типо Behance / Pinterest" | Removed cheap template animations; shifted engine to custom Remotion components (LiquidGlass, VoxBarChart, CameraRig). |
| 2026-10-15 | Analyzed Joseph / Ultimate Editors sound design manual | Cataloged all 61 broadcast SFX files with strict dB gain staging (-12dB for SFX, -6dB for VO). |
| 2026-10-16 | Refactoring raw docs into high-speed Remotion engine | Deleted duplicate skills, established 10 modular rulebooks, strictly 0 comments in code files. |
