# 03. Beat Map & Production Planning

## 1. Mandatory Pre-Flight: The Beat Map
Before authoring any React component or Remotion composition, create a formal `BEAT_MAP.json` or structured Markdown table.
Every vertical video must be broken down into individual 4 to 10 second beats. Every single sentence of the transcript must have an exact 1:1 mapping to an on-screen asset, camera motion, and sound effect trigger.

## 2. Standard Beat Schema
Each beat must specify:
1. `beatIndex`: Integer (0-indexed).
2. `timeRange`: Start and end timestamps (`MM:SS.ms` or frames).
3. `spokenWords`: The exact transcript phrase.
4. `visualFocus`: Concrete UI component or asset (e.g. `LiquidGlassCard`, `VoxBarChart`, `A-Roll Speaker`, `DeviceMockup`).
5. `cameraMotion`: Explicit camera transform name. **NEVER** use subjective words like "cinematic", "dynamic", or "cool".
6. `sfx`: Exact SFX filename from `assets/01_SFX/` or asset ID.

## 3. Approved Camera Movements
Only the following explicit camera movements are permitted:
- `push-in`: Scale smoothly from `1.0` to `1.08` over beat duration.
- `push-out`: Scale smoothly from `1.08` to `1.0` over beat duration.
- `pan-left`: Horizontal translation `x: 0 -> -40px` with slight scale `1.04`.
- `pan-right`: Horizontal translation `x: 0 -> +40px` with slight scale `1.04`.
- `static-fade`: Constant scale `1.0`, opacity fade or hard cut.

## 4. Markdown Beat Map Template
| Beat # | Time / Frames | Spoken Line | Visual Component & Preset | Camera Rig | SFX Trigger |
|---|---|---|---|---|---|
| **01** | `00:00 - 00:03` (0-90) | "Almost everyone fails at..." | `SafeZoneContainer` + `LiquidGlassCard` hook | `push-in` | `whoosh-deep-reverb.wav` |
| **02** | `00:03 - 00:07` (90-210) | "Look at these numbers from Q3" | `VoxBarChart` (Growth 0% -> 87%) | `static-fade` | `digital-click-accent.wav` |
| **03** | `00:07 - 00:12` (210-360) | "They burnt 4 million dollars..." | `NumberTicker` ($4,200,000) | `push-out` | `heavy-impact-sub.wav` |

## 5. Standalone Sub-Prompt Generator
When developing multi-scene projects or delegating individual clip renders across parallel chats or subagents, generate isolated clip prompts:

### Sub-Prompt Format:
```markdown
### PARALLEL CLIP PROMPT: CLIP [X]
- **Target Composition**: `Clip_[X]`
- **Duration**: [N] frames ([S] seconds @ 30fps)
- **Visual Preset**: [e.g. `vox-editorial-data` / `apple-liquid-glass`]
- **Spoken Audio / Transcript**: "[Exact line for this clip]"
- **Camera Movement**: [e.g. `push-in` (1.0 -> 1.08)]
- **Primary Component**: `[ComponentName]` from `src/components/`
- **Assets Required**: [List filenames from `src/config/assets.ts`]
- **Constraints**: 1080x1920, strictly inside safe zones, ZERO comments in code.
```
