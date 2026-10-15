# 09. Visual-to-SFX Choreography Matrix

## 1. Synchronization Physics: The "Lead-In" Rule
- Sound precedes vision in human perception.
- Fast whooshes, air cuts, and camera snaps must start **1 to 2 frames BEFORE** the visual asset hits peak velocity or contacts the screen.
- Hard impact hits (sub drops, thuds) must trigger on the **exact frame of visual contact** (scale = 1.0 or card arrival).

## 2. The 3-Layer Sound Design Rule (Joseph / Ultimate Editors)
Never play isolated, naked SFX. A professional audio event consists of up to 3 complementary layers:
1. **The Transient / Attack**: Fast whoosh, snap, or click that leads the motion.
2. **The Body / Impact**: Low thud, resonant bell, or glass ping that gives weight.
3. **The Texture / Tail**: Paper slide, vinyl crackle, or subtle reverb tail that creates atmosphere.

## 3. Visual Event to SFX Mapping Matrix

| Visual Event | Primary SFX (`assets/01_SFX/`) | Layer 2 (Optional) | Timing Offset | Remotion Volume |
|---|---|---|---|---|
| **Card / Modal Entrance** | `whooshes/fast-swish-air.wav` | `pops/soft-pop-wood.wav` | `-2 frames` | `0.35` |
| **Data Bar Growth / Start** | `textures/paper-slide-light.wav` | `sci-fi/digital-click-accent.wav` | `0 frames` | `0.25` |
| **Number Ticker Step** | `sci-fi/digital-tick-single.wav` | — | Per change | `0.18` |
| **Camera Punch-In (1.0->1.08)** | `impacts/low-thud-cinematic.wav` | `whooshes/deep-air-whoosh.wav` | `0 frames` | `0.40` |
| **Thesis Statement / Major Claim** | `impacts/heavy-cinematic-hit.wav` | `risers/sub-drop-short.wav` | `0 frames` | `0.45` |
| **Word Highlight / Karaoke** | `sci-fi/clean-blip-high.wav` | — | Exact word start | `0.15` |
| **Paper Document Slide-In** | `textures/paper-rustle-crisp.wav` | — | `-1 frame` | `0.30` |
| **Scene Transition (Cut)** | `whooshes/transitional-air-pass.wav` | — | `-2 frames` | `0.30` |

## 4. Audio Gain Control
- SFX must sit comfortably below dialogue.
- Dialogue Voiceover: `-6 dB`
- SFX: `-12 dB` to `-10 dB` (Volume `0.25` to `0.35` in Remotion props).
