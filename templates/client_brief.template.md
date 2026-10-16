# Client Brief — Intake Form

> **Usage:** Paste the raw Upwork job description below "RAW JOB POST", then ask Claude to fill the parsed fields automatically.

---

## RAW JOB POST
```
[PASTE UPWORK JOB DESCRIPTION HERE]
```

---

## PARSED OUTPUT (Claude fills this)

### Project Identity
- **client_slug:** `[e.g. john_doe_oct26]`
- **platform:** `[ ] TikTok  [ ] Reels  [ ] Shorts  [ ] All`
- **content_type:** `[ ] talking_head  [ ] product_demo  [ ] tutorial  [ ] storytime  [ ] montage`
- **duration_target:** `[ ] 15s  [ ] 30s  [ ] 60s  [ ] 90s`
- **language:** `[ ] EN  [ ] RU  [ ] Other: ___`

### Style Mapping
- **creator_archetype:** `[from 07-creator-style-presets.md]`
- **tone:** `[ ] educational  [ ] hype  [ ] calm_authority  [ ] storytime  [ ] comedic`
- **palette:** `[palette name from assets/design-system/palettes.json]`
- **hook_pattern:** `[hook archetype # from 10-hook-patterns.md]`

### Logistics
- **deadline:** `YYYY-MM-DD`
- **budget:** `$___`
- **revision_rounds:** `2 (standard)`
- **raw_footage_provided:** `[ ] Yes  [ ] No — client shoots on direction`
- **voice_over:** `[ ] client records  [ ] synth (synth_speech.ps1)  [ ] existing`

### Source Material
- **reference_links:** 
  - 
- **raw_files_location:** `clients/<slug>/raw/`
- **brand_kit:** `[ ] Logo  [ ] Colors  [ ] Fonts` → `clients/<slug>/brand/`

### Deliverables
- [ ] 1080×1920 MP4 (H.264, 30fps)
- [ ] Captions burned in
- [ ] SFX mixed
- [ ] Optional: ProRes stems for client's editor

### Notes / Special Requests
```
[paste any specific client notes]
```

---

## AUTO-GENERATED brief.json

> After filling above, Claude will write this to `clients/<slug>/brief.json`:

```json
{
  "client_slug": "",
  "platform": "",
  "content_type": "",
  "duration_target_s": 30,
  "language": "en",
  "creator_archetype": "",
  "tone": "",
  "palette": "",
  "hook_pattern": 1,
  "deadline": "",
  "budget_usd": 0,
  "revision_rounds": 2,
  "raw_footage_provided": true,
  "voice_path": null,
  "reference_links": [],
  "approved": false
}
```
