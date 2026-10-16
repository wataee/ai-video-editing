# Audio-Visual SFX Choreography & Sound Mapping

## 1. Physics & Psychology of Sound Synchronization
- **Speech is King**: Dialogue is the absolute center of the mix. Nothing ever masks speech.
- **Relative Staging**: SFX loudness is NEVER set to fixed master slider values. It is calculated strictly relative to measured speech RMS loudness.
- **Lead-In Offset**: Whooshes and air transitions start **1 to 2 frames (33–66 ms @ 30fps) BEFORE** the visual cut or element arrival.
- **Impact Alignment**: Sub drops and physical hits align with the exact contact frame.
- **Zooms Without Sound**: Camera punch-ins and zooms have NO sound effect (eyes do not make sound when focusing).
- **Density Limit**: Maximum 6 SFX per 30 seconds of video.

---

## 2. Calibrated Loudness Staging (Relative to Speech RMS)

All levels are offsets relative to the measured dialogue RMS level:

| Sound Category | Offset Relative to Voice RMS | Role & Behavior |
|---|---|---|
| **Hits & Sub Thuds** | `−14 dB` | Semantic impact on hook or key revelation |
| **Risers** | `−14 dB` (peak) | Tension build ending abruptly on transition frame |
| **Textures (Clicks, Pops, UI)** | `−16 dB` | Tactile confirmation of proof/data appearance |
| **Whooshes (Fast Air / Transitions)** | `−20 dB` | Fast scene transitions and large graphic slides only |
| **Background Music (BGM)** | `−22 dB` and lower | Under dialogue only, ducked with sidechain |

---

## 3. Visual Event to Local SFX Mapping

All paths reference the cataloged WAV library in `assets/sfx/`:

| Visual Event | Family | Catalog File (`assets/sfx/`) | Offset | Level (Rel. to Voice) |
|---|---|---|---|---|
| **Hook / Core Punchline** | Hit | `hits/sub_bass_thud.wav` | `0 frames` | `−14 dB` |
| **Scene Transition Cut** | Whoosh | `whooshes/whoosh_clean_fast.wav` | `-2 frames` | `−20 dB` |
| **Soft Narrative Transition** | Whoosh | `whooshes/whoosh_subtle_air.wav` | `-2 frames` | `−20 dB` |
| **Proof / Stat Modal Appearance** | Texture (Pop) | `pops/glass_pop.wav` | `0 frames` | `−16 dB` |
| **Interface Toggle / Step** | Texture (Click) | `clicks/switch_01.wav` or `click_01.wav` | `0 frames` | `−16 dB` |
| **Anticipation Build (Pre-Hook)** | Riser | `risers/riser_subtle.wav` | `-30 frames` | `−14 dB` peak |
| **Camera Punch-In (Zoom)** | None | **NO SOUND** | — | — |

---

## 4. Master Loudness Limits
- Master Bus Integrated Loudness: `-14.0 LUFS (±1.0 LUFS)`
- True Peak: `<= -1.0 dBTP`
- Ducking: Music dips by `-4 dB` to `-6 dB` during vocal utterances.
