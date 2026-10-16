# 02. Cut, Audio Sync & Ingest Standards

## 1. Mandatory Ingest Pass (Color & Frame Rate First)
- **Zero Raw HDR in Editing Engine**:
  - Footage shot on iPhone (HLG / BT.2020 / Apple Log) must NEVER be loaded into Remotion or After Effects without pre-conversion.
  - Using an Exposure adjustment layer (-2.2) or Gamma tweak inside AE to "fix" blown-out HDR is **strictly forbidden**.
  - All footage must pass through `tools/ingest.py`: hardware tone mapping via `libplacebo` (BT.2390) or `zscale` to SDR Rec.709, conversion to CFR 30 fps, and creation of 720p proxy files.
- **Verification**: Automatic check calculates overexposed pixels in the central face region. Less than 2% overexposure allowed.

## 2. Retake Removal & Clean Take Selection
- When duplicate or near-duplicate phrases appear in a transcript, **keep ONLY the last clean take**.
- Discard false starts, throat clears, stammers, and filler breaths.
- Maintain a minimum of 2 frames (66ms at 30fps) of head and tail room around words to preserve consonants.
- Apply a 2-frame micro-fade (crossfade) on every audio edit point to eliminate digital clicks.

## 3. Pacing and Breathing Hygiene
- Natural breaths before key phrases and 0.2–0.4s pauses after major conclusions must be preserved.
- Remove only dead silences > 0.6s and filler sounds ("uh", "um"). Avoid machine-gun pacing.

## 4. Calibrated Loudness Staging (Relative to Speech RMS)
SFX loudness is calculated relative to measured dialogue RMS (not arbitrary fixed master sliders):

| Track / Sound Family | Target Level | Behavior |
|---|---|---|
| **Voiceover (Dialogue)** | Target `-14.0 LUFS` integrated | Reference Anchor (Peak <= -1.0 dBTP) |
| **Hits & Risers** | `−14 dB` relative to speech RMS | On emotional punch or major transition |
| **Textures (Clicks, Pops)** | `−16 dB` relative to speech RMS | On proof appearance or UI toggle |
| **Whooshes (Air Sweeps)** | `−20 dB` relative to speech RMS | Scene transitions and major graphics only |
| **Background Music (BGM)** | `−22 dB` relative to speech RMS | Sidechained with ducking under dialogue |
| **Camera Punch-In (Zooms)** | **NO SOUND** | Zooms never trigger SFX |

- **Density Limit**: Maximum 6 SFX per 30 seconds of video.
