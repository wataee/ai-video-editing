# Creator Archetypes & Visual DNA Specifications

## Overview
This document codifies the visual design tokens, motion physics, color palettes, and editorial pacing for the top viral short-form creator archetypes in vertical 9:16 format.

---

## 1. Minimalist Productivity (Ali Abdaal Aesthetic)

### Visual DNA
- **Theme**: Clean intellectual clarity, calm productivity, organized Notion workspace, soft bookish elegance.
- **Colorway**:
  - Primary Background: Warm Muted Studio Canvas `#F9F9FB` or Clean Cream `#FAF8F5` (Dark mode: `#191919`).
  - Cards: Pure White `#FFFFFF` with ultra-fine border `1px solid rgba(0, 0, 0, 0.05)` and double diffused drop shadow `0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 16px 32px -4px rgba(0, 0, 0, 0.06)`.
  - Pastels & Highlighters:
    - Butter Yellow: `#FEF08A` (fill) / `#CA8A04` (text)
    - Mint Green: `#A7F3D0` (fill) / `#059669` (text)
    - Soft Lavender: `#DDD6FE` (fill) / `#7C3AED` (text)
    - Rose: `#FECDD3` (fill) / `#E11D48` (text)
- **Typography**:
  - Headings: Editorial Serifs (New York, Playfair Display, Fraunces) at 72–84px, line-height 1.15.
  - Body & UI: Inter / SF Pro Text at 36–42px, weight 500, line-height 1.35.
- **Motion Physics**:
  - Subtle floating levitation: Sinusoidal drift `y = 6 * sin(2 * PI * t / 3.6s)`.
  - Slide-up ease: `cubic-bezier(0.19, 1, 0.22, 1)` (Expo Ease Out).
  - Remotion spring: `stiffness: 90, damping: 20, mass: 1.0` (zero bounce, soft organic settle).
- **Sound Design**:
  - Acoustic chisel-tip marker squeak for highlighter sweeps.
  - Warm tactile toggle clicks / wooden block taps for card reveals.
  - Single-page paper flutters for transitions.

---

## 2. High-Retention Noir (Iman Gadzhi Aesthetic)

### Visual DNA
- **Theme**: High-status financial documentary, luxury fashion minimalism, vintage investigative noir.
- **Colorway**:
  - Background: True Obsidian Black `#050505` to `#0B0B0D`.
  - Accents: Metallic Burnished Gold `#E8C872` -> `#BA9444`, Crimson Red `#DC2626`.
  - Surface: High-gloss black with specular edge highlights `1px solid rgba(255, 255, 255, 0.14)`.
- **Textures & Post-FX**:
  - 35mm film grain (12–16% overlay blend mode).
  - Heavy feathered radial vignette (-2.0 EV dark borders).
  - Subtle edge chromatic aberration and lens barreling (0.05).
- **Typography**:
  - Primary Power Serif: Canela / Didot / Bodoni Poster at 92–118px, weight 800+, 3D bevel with drop shadow `0 20px 40px rgba(0,0,0,0.8)`.
  - Signature Cursive Script: Autography / Caveat / Segoe Script at 70–90px, tilted -8deg to -12deg, gold `#E8C872`, overlapping the lower third of the primary headline.
  - Tracking: Expanded uppercase serif tracking `+0.12em` to `+0.20em`.
- **Motion Physics**:
  - Slow Z-axis cinematic push-in: `scale: 1.0 -> 1.08` over 3.5s.
  - Snap zoom punch: 6-frame zoom cut `scale: 1.0 -> 1.25` via `cubic-bezier(0.05, 0.9, 0.1, 1.0)`.
  - Remotion spring: `stiffness: 140, damping: 28, mass: 2.2, overshootClamping: true`.
- **Sound Design**:
  - 40–55 Hz low-end cinematic 808 sub-bass thud (1.2s decay) on thesis statements.
  - Dark atmospheric whoosh with reversed reverb tail on scene switches.
  - Metallic blade ring overtone (6.8 kHz) on gold script accents.

---

## 3. Vox-Style Editorial Data (Johnny Harris & Vox Aesthetic)

### Visual DNA
- **Theme**: Investigative data journalism, topographic maps, archival collages, tactile drafting paper.
- **Colorway**:
  - Caution Yellow: Canary `#FFE600` / `#FFD60A` (Universal focus anchor).
  - Blueprint Navy: Deep slate `#0F172A` / `#1E293B`.
  - Newsprint Cream: Aged archival paper `#F4EFE6`.
  - Conflict Red: `#EF4444`.
- **Textures & Overlays**:
  - Folded paper creases, scotch tape strips, torn edge masks.
  - Cartesian coordinate grids, dotted technical grids spaced 28–36px.
  - Posterize time / "on twos" effect (paper graphics rendered at 12–15 fps over 60 fps camera).
- **Typography**:
  - Heavy Grotesque: Franklin Gothic Heavy / Oswald / Montserrat Black at 80–96px, ALL CAPS, tracking `-0.02em`.
  - Backing: Solid canary yellow rectangle box (`#FFE600`) behind black text (`#000000`).
  - Monospace Data: Space Mono / JetBrains Mono at 28–34px with red locator pins.
- **Motion Physics**:
  - Paper slap down: 10 frames total (scale 1.15 -> 1.0, 3-degree rotation tilt).
  - Camera pan: `cubic-bezier(0.05, 0.85, 0.15, 1)` with 95% deceleration influence.
- **Sound Design**:
  - Dual-layer paper flap + desk thud (120 Hz thump + 3 kHz crisp paper).
  - High-speed projector slide click / mechanical ratchet.
  - Dry drafting pencil scribble during border drawing.

---

## 4. Kinetic Punch (Alex Hormozi Aesthetic)

### Visual DNA
- **Theme**: Relentless energy, rapid attention retention, 100% sound-off mobile readability.
- **Colorway**:
  - Primary Karaoke Text: Pure White `#FFFFFF`.
  - Active Spoken Word: High-Vis Neon Yellow `#FFFD38` or Cyber Lime Green `#00FF66`.
  - Secondary Emphasis: Fire Orange `#FF5500` or Cyan `#00E5FF`.
  - Stroke: 9–10px solid black outer outline (`-webkit-text-stroke: 9px #000000; paint-order: stroke fill;`) + multi-layered shadow `0 10px 24px rgba(0, 0, 0, 0.95)`.
- **Typography**:
  - Font: The Bold Font / Montserrat Black 900 / Rubik 900.
  - Size: 88–108px, ALL CAPS, tracking `+0.02em`.
  - Framing: 1 to 3 words per line, 1 active line on screen at a time.
- **Motion Physics**:
  - Aggressive scale snap: 0.92 -> 1.18 -> 1.0 on active word spoken.
  - Bezier: `cubic-bezier(0.34, 1.56, 0.64, 1)` (High-overshoot elastic spring).
  - Remotion spring: `stiffness: 450, damping: 14, mass: 0.6` (instant snap and settle).
- **Sound Design**:
  - Heavy cork pop / wooden bubble pop on every active word pop.
  - Heavy boxing glove punch thud (80 Hz) on hard punchlines.
  - Mechanical cash register ding / coin drop on financial metrics.

---

## 5. SaaS / Tech Glass & Mockups (Devin Jatho Aesthetic)

### Visual DNA
- **Theme**: High-velocity tech startup, Apple keynote hardware elegance, floating Figma-grade 3D UI mockups.
- **Colorway**:
  - Background: Deep Space Slate `#0B0E14` or Obsidian Grey `#12161F`.
  - Accents: Electric Indigo `#6366F1`, Radiant Violet `#8B5CF6`, Cyber Cyan `#06B6D4`, Emerald `#10B981`.
  - Glass Panels: Frosted glass `rgba(18, 22, 31, 0.65)` with `backdrop-filter: blur(28px)`, 1.5px border `rgba(255, 255, 255, 0.12)`, shadow `0 24px 48px -12px rgba(0, 0, 0, 0.6)`.
- **Mockup Transforms**:
  - Isometric 3D tilt: `perspective: 1200px, rotateX: 12deg, rotateY: -16deg`.
  - Subtle light sweep / sheen across card headers.
- **Typography**:
  - PP Neue Montreal / Inter Display / SF Pro Display at 88–104px (headers) and 32–36px (body).
  - Metric numbers: JetBrains Mono / SF Mono at 72–96px, tabular numbers.
- **Motion Physics**:
  - Ultra Snap Out: `cubic-bezier(0.16, 1, 0.3, 1)` (85% in, 15% out).
  - Remotion spring: `stiffness: 280, damping: 24, mass: 0.85`.
- **Sound Design**:
  - Tactile high-frequency digital click + clean wooden pop (2.8 kHz peak, -12 dB) on modal open.
  - Micro-ratchet UI scroll clicks during number ticker counts.
  - Resonant glass ping (4.2 kHz) on metric completion.
