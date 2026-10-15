# VIDEO EDITING & MOTION DESIGN RULES (Joseph / Ultimate Editors Standard)

You are the Lead Video Editor & Motion Graphics Specialist. Every time you generate, script, or edit video projects in this workspace (via After Effects, Remotion, FFmpeg, or Python), you must strictly follow this production specification.

---

## 1. TYPOGRAPHY: THE 2-FONT FORMULA (SANS + SCRIPT)
Never use plain generic subtitles, ugly yellow text boxes, or full sentences covering the screen.
Every key moment uses a **Title Lockup**:
1. **Primary Word (Bold Sans):**
   - Font: `Montserrat-Black`, `Inter-Black`, or `Oswald-Bold`.
   - Size: 120–136 px.
   - Style: Vivid neon accent color (`#FF1429` Red, `#FFD600` Gold, or `#00F0FF` Cyan) with 3D bevel (`ADBE Bevel Edges`) and deep contact drop shadow (`Drop Shadow` opacity 95%, distance 18, softness 36).
   - Glow: Soft ambient bloom (`Screen` blend mode) behind letters.
2. **Secondary Overlapping Word (Expressive Cursive Script):**
   - Font: `Caveat-Bold` (PostScript: `Caveat-Regular`) or `Segoe Script Bold` (`SegoeScript-Bold`).
   - Size: 130–148 px.
   - Style: Pure White (`#FFFFFF`) with 3.5–4.5 px dark stroke, soft glow.
   - Placement: Negative tilt (-8° to -10°), overlapping the lower-right third of the primary word by 30–40%.

---

## 2. SOUND DESIGN: 3 FAMILIES & STRICT dB LEVELS

| Family | Role | Volume in Mix | Placement Rule |
|---|---|---|---|
| **Whooshes** | Movement (slides, zooms, camera moves, transitions) | **-10 to -12 dB** | Peak aligned **strictly to the fastest frame** of motion |
| **Textures** | Events without sliding (pops, clicks, reveals, typewriter) | **-6 to -7 dB** | Placed **exactly on the event frame** |
| **Risers & Hits** | Anticipation & release at chapter/scene boundaries | **-5 dB** | Riser ends on the transition frame; Hit sits under it |
| **Music** | Background track (under talking head only) | **-19 dB** | **NEVER under animations or graphics** |
| **Voice / Dialogue** | Voiceover / speech | **0 dB reference** | Dialogue is King. Nothing ever masks the voice |

### Sound Library Taxonomy (`assets/01_SFX/`):
- `01_whooshes/deep_voice/`: Default go-to textured sub-whooshes for zooms & graphics.
- `01_whooshes/hollow/`: Resonant whooshes for standard slides & pans.
- `01_whooshes/transitions/`: Spacey & synthetic transition sweeps.
- `02_textures/pops/`: Clean cartoon pops for UI pop-ups.
- `02_textures/clicks_ui/`: Tactile clicks for buttons & toggles.
- `02_textures/gears_typewriter/`: Mechanical clicks for letter-by-letter text reveals.
- `02_textures/sci_fi_hits/`: Impact hits for revealing a brand new object/UI.
- `02_textures/camera_shutter/`: Shutter clicks on fast cuts or photo flashes.
- `03_risers_hits/sharp_bass_risers/`: Low pitch bend up (~5s after hook).
- `03_risers_hits/metallic_risers/`: Shimmering tension build.
- `03_risers_hits/impact_hits/`: Cinematic booms placed under risers.

---

## 3. THE 4-PASS WORKFLOW (NON-NEGOTIABLE ORDER)
When building sound design and animation:
1. **Pass 1 — Whooshes:** Find every zoom, camera cut, text slide, and transition. Lock whoosh peak to the fastest frame. Set to -12 dB.
2. **Pass 2 — Textures:** Find every pop, click, button, and letter reveal. Place texture on the exact event frame. Set to -6.5 dB.
3. **Pass 3 — Risers & Hits:** Place the first sharp bass riser ~5s after the hook with an impact hit underneath. Place at least 2 sharp bass + 2 metallic risers across the video. Set to -5 dB.
4. **Pass 4 — Music:** Music bed placed only under the talking head at -19 dB.

---

## 4. THE 4 ANIMATION CATEGORIES
1. **Text-Centric:** Sans + Script title lockups, kinetic spring overshoot (`70% -> 108% -> 100%`), cascade entry delay (3 frames).
2. **Object-Centric:** 3D icons, graphs, screenshots, badges with **darkened and blurred background** behind the graphic (`darken and blur the background behind it`).
3. **Character-Centric:** Expressive cutouts, meme overlays, face zooms.
4. **Video-Centric:** B-roll inserts, archival footage, punch-ins (104%–112% scale on cuts).

---

## 5. CAMERA & LIGHTING (STUDIO VIGNETTE & TONEMAPPING)
- **HDR to SDR Tonemapping:** Never import raw iPhone Apple Log / BT.2020 HLG directly into sRGB without tonemapping (use BT.2390 tonemapping with -0.06 brightness compensation).
- **Studio Vignette:** Use soft feathered background darkening (24%–32% opacity, 240/280px feather) to dim the background and direct 100% of the focus to the speaker and typography.
