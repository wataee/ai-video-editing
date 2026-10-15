# Audio-Visual SFX Choreography & Sound Mapping

## 1. The Physics of Audio-Visual Sync
In human perception, the auditory cortex processes transient spikes faster than visual motion settles.
- **The Lead-In Rule**: Whooshes, slides, and heavy thuds must start **1 to 2 frames (16–33 ms @ 60fps) BEFORE** the visual asset reaches maximum velocity or contacts the screen.
- **The Contact Rule**: Pops, clicks, and chimes must align on the **exact frame (0 ms)** of visual arrival.

---

## 2. Comprehensive Animation Trigger to Local SFX Mapping

All paths reference the broadcast WAV library located in `assets/01_SFX/`:

| Animation / Visual Trigger | Local SFX File (`assets/01_SFX/`) | Secondary Texture Layer | Lead-In Offset | Target dB | Remotion Volume |
|---|---|---|---|---|---|
| **Text Pop-up / Kinetic Word** | `02_textures/pops/pop_01.wav` or `pop_bubble_high.wav` | — | `0 frames` | `-14 dB` | `0.20` |
| **Glass Card / Modal Entrance** | `01_whooshes/futuristic/whoosh_clean_fast.wav` | `02_textures/pops/glass_pop.wav` | `-2 frames` | `-12 dB` | `0.25` |
| **Number Ticker Increment** | `02_textures/clicks_ui/click_01.wav` or `mouse_click_soft.wav` | — | Per tick | `-20 dB` | `0.10` |
| **Chart Bar Growth** | `02_textures/gears_typewriter/scratch_01.wav` | `02_textures/clicks_ui/select_01.wav` | `0 frames` | `-16 dB` | `0.16` |
| **Camera Punch-In (1.0 -> 1.08)** | `03_risers_hits/impact_hits/sub_bass_thud.wav` | `01_whooshes/deep_voice/deep_voice_whoosh_01.wav` | `-1 frame` | `-10 dB` | `0.32` |
| **Key Metric / Thesis Impact** | `03_risers_hits/impact_hits/bass_drop_hit_01.wav` | `03_risers_hits/impact_hits/cinematic_boom_01.wav` | `-1 frame` | `-8 dB` | `0.40` |
| **Document / Paper Slide** | `02_textures/camera_shutter/camera_click_fast.wav` | `02_textures/gears_typewriter/scratch_02.wav` | `-1 frame` | `-15 dB` | `0.18` |
| **Scene Whip Cut / Transition** | `01_whooshes/transitions/synthetic_transition_whoosh.wav` | `01_whooshes/transitions/transition_spacey_whoosh.wav` | `-2 frames` | `-11 dB` | `0.28` |
| **Button / Toggle Switch** | `02_textures/clicks_ui/switch_01.wav` or `mechanical_button.wav` | — | `0 frames` | `-14 dB` | `0.20` |
| **Anticipation Build (Pre-Hook)** | `03_risers_hits/sharp_bass_risers/sharp_bass_riser_fast.wav` | `03_risers_hits/metallic_risers/metallic_riser_01.wav` | `-30 frames` | `-12 dB` | `0.25` |
| **Suck-Back Tension Release** | `03_risers_hits/suck_back_risers/suck_back_riser_fast.wav` | `03_risers_hits/impact_hits/sub_bass_thud.wav` | `-15 frames` | `-10 dB` | `0.32` |

---

## 3. The 3-Layer Sound Design Formula (Joseph / Ultimate Editors)

Never play solitary, naked SFX. Every major visual beat should utilize up to 3 complementary layers:
1. **Transient / Air (Attack)**: High-pass whoosh (`01_whooshes/`) initiating 2 frames early to lead the eye.
2. **Body / Weight (Impact)**: Low-end thud or boom (`03_risers_hits/impact_hits/`) providing kinetic weight on contact.
3. **Texture / Friction (Character)**: Tactile mechanical pop, paper rustle, or click (`02_textures/`) cementing physical reality.

---

## 4. Master Mix Loudness Hierarchy
- **Voiceover (Dialogue)**: `-6.0 dB` to `-3.0 dB` (Center channel anchor).
- **SFX Bus**: `-14.0 dB` to `-8.0 dB` (Underneath speech peaks).
- **Background Music**: `-24.0 dB` to `-20.0 dB` (Ducked under dialogue).
- **Master Export Target**: `-14.0 LUFS (±1.0 LUFS)`, True Peak `<= -1.0 dBTP`.
