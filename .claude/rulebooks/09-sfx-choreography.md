# 09. Visual-to-SFX Choreography Matrix

## 1. Hard Rule: Local SFX via <Audio/> with Frame Precision
- **Local Folder Only**: Использовать звуки **исключительно** из локальной папки `assets/01_SFX/` (`assets/sfx/`). Внешние URL, сторонние генераторы на лету и системные звуки запрещены.
- **Remotion <Audio/> Component**: Внутри Remotion композиций воспроизведение оформляется через `<SfxAudio />` или нативный `<Audio />` с точным расчетом фреймов:
  - `startFrom`: точный номер кадра сдвига внутри аудиофайла.
  - `durationInFrames`: длительность звучания клипа.
  - `volume={(f) => ...}`: математическая огибающая с мягким `fadeInFrames` (1–3 кадра) и `fadeOutFrames` (4–8 кадров) для исключения щелчков на границах фрагментов.

## 2. Synchronization Physics: The "Lead-In" Rule
- Sound precedes vision in human perception.
- Fast whooshes, air sweeps, and scene transitions start **1 to 2 frames (33–66 ms @ 30fps) BEFORE** the visual asset cuts or reaches peak velocity.
- Physical impact hits (sub drops, thuds) trigger on the **exact frame of visual contact** (scale = 1.0 or card arrival).
- **Zooms Without Sound**: Camera punch-ins and zooms have NO sound effect (eyes do not make sound when focusing).
- **Density Limit**: Maximum 6 SFX per 30 seconds of video.

## 3. Calibrated Loudness Staging (Relative to Speech RMS)
SFX loudness is strictly relative to dialogue RMS, never an arbitrary fixed slider:

| Sound Family | Level Relative to Voice RMS | Placement Principle |
|---|---|---|
| **Hits & Risers** | `−14 dB` | Emotional punch, cold open hook, thesis climax |
| **Textures (Clicks, Pops)** | `−16 dB` | Appearance of real proof, stats, switches |
| **Whooshes (Fast Air)** | `−20 dB` | Fast scene transitions and graphic sweeps only |
| **Background Music** | `−22 dB` and lower | Under voice only, with sidechain ducking (-4 to -6 dB during speech) |
| **Camera Zooms** | **NO SOUND** | Never add sound to camera punch-ins |

## 4. Visual Event to SFX Mapping

| Visual Event | Primary SFX (`assets/01_SFX/`) | Timing Offset | Relative dB |
|---|---|---|---|
| **Card / Modal Entrance** | `pops/pop_bubble_high.wav` | `0 frames` | `−16 dB` |
| **Scene Transition (Cut)** | `whooshes/whoosh_clean_fast.wav` | `-2 frames` | `−20 dB` |
| **Soft Narrative Shift** | `whooshes/deep_voice_whoosh_01.wav` | `-2 frames` | `−20 dB` |
| **Metric / Stat Click** | `clicks/mechanical_button.wav` | `0 frames` | `−16 dB` |
| **Thesis Statement / Major Punch** | `hits/sub_bass_thud.wav` | `0 frames` | `−14 dB` |
| **Anticipation Build** | `risers/metallic_riser_01.wav` | `-30 frames` | `−14 dB` peak |
| **Camera Punch-In (Zoom)** | None | — | **NO SOUND** |
