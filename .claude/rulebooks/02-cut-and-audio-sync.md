# 02. Cut & Audio Sync Standards

## 1. Retake Removal & Clean Take Selection
- Speakers frequently repeat lines when stumbling or searching for cadence.
- **Rule**: When duplicate or near-duplicate phrases appear in a transcript, **keep ONLY the last clean take**.
- Discard false starts, throat clears, stammers, and filler breaths preceding the successful delivery.
- Never splice two partial takes together if the vocal pitch or room tone noticeably shifts.

## 2. Silence Detection & Pacing
- Remove dead silences longer than 300ms in fast-paced TikTok/Reels edits, but preserve natural 150-250ms cadence pauses at major paragraph transitions.
- Maintain a minimum of 2 frames (66ms at 30fps) of head and tail room around words to prevent cutting off plosives (p, b, t) or sibilants (s, sh).
- Apply a 2-frame micro-fade (crossfade) on every audio edit point to eliminate digital clicks and DC-offset pops.

## 3. Lip-Sync & Hardware Offset Compensation
- Consumer cameras (iPhone, Sony HDMI capture, webcams) often introduce audio/video sync lag when using external USB or XLR microphones.
- **audioOffsetFrames parameter**:
  - Always support an explicit `audioOffsetFrames` configuration on video compositions.
  - Positive offset shifts audio forward; negative offset delays audio.
  - Verify sync using plosive consonant visual checks (e.g. lips contacting on "B" or "P").

## 4. Calibrated Loudness & Gain Staging
All audio in the Remotion engine must adhere to strict broadcast gain staging:

| Track / Bus | Target Peak Range | Average / Integrated Target | Remotion Audio Volume Multiplier |
|---|---|---|---|
| **Voiceover (A-Roll / Mic)** | `-6.0 dB` to `-3.0 dB` | `-14 LUFS` to `-16 LUFS` | `1.0` (Master level reference) |
| **Sound Effects (SFX / 01_SFX)** | `-12.0 dB` to `-8.0 dB` | Transient peaks only | `0.25` to `0.45` |
| **Background Music (BGM)** | `-24.0 dB` to `-20.0 dB` | Underneath vocal ducking | `0.06` to `0.12` |
| **Master Bus (Final Export)** | True Peak `<= -1.0 dBTP` | `-14.0 LUFS (±1.0 LUFS)` | Broadcast Compliant |

### Remotion Volume Formula:
Remotion `volume` prop accepts a linear float `0.0` to `1.0`. Convert dB using:
`volume = Math.pow(10, dB / 20)`
- `-6 dB` ~= `0.50`
- `-10 dB` ~= `0.316`
- `-12 dB` ~= `0.251`
- `-20 dB` ~= `0.100`
- `-24 dB` ~= `0.063`
