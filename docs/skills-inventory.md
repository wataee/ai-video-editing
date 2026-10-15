# Инвентарь навыков Remotion (Remotion Skills Inventory)

**Дата составления:** 2026-10-15  
**Источник:** `.agents/skills`  
**Целевая папка для Claude Code:** `.claude/skills`  

| Имя навыка | Папка | Frontmatter (name/description) | Краткое назначение | Вложенных файлов |
| :--- | :--- | :---: | :--- | :---: |
| `remotion-best-practices` | `.agents\skills\remotion-best-practices` | Да | Router for all Remotion skills | 140 |
| `remotion-captions` | `.agents\skills\remotion-captions` | Да | Transcribing, displaying and animating captions | 5 |
| `remotion-create` | `.agents\skills\remotion-create` | Да | Create a new Remotion video | 4 |
| `remotion-docs` | `.agents\skills\remotion-docs` | Да | Search Remotion documentation | 2 |
| `remotion-interactivity` | `.agents\skills\remotion-interactivity` | Да | Structure Remotion markup for interactivity | 3 |
| `remotion-maps` | `.agents\skills\remotion-maps` | Да | Remotion Map animation knowledge | 31 |
| `remotion-markup` | `.agents\skills\remotion-markup` | Да | Content, animation and effects best practices | 65 |
| `remotion-multimedia` | `.agents\skills\remotion-multimedia` | Да | Interacting with Mediabunny | 5 |
| `remotion-render` | `.agents\skills\remotion-render` | Да | Export a Remotion video | 3 |
| `remotion-saas` | `.agents\skills\remotion-saas` | Да | Build an app with Remotion | 5 |
| `remotion-studio` | `.agents\skills\remotion-studio` | Да | Preview a Remotion video | 2 |
| `remotion-upgrade` | `.agents\skills\remotion-upgrade` | Да | Upgrade Remotion, and related packages | 2 |


## Детализация структуры каждого навыка

### `remotion-best-practices`
- **Название:** remotion-best-practices
- **Описание:** Router for all Remotion skills
- **SKILL.md:** Присутствует
- **Вложенные файлы (140):**
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`
  - `remotion-captions\display-captions.md`
  - `remotion-captions\import-srt-captions.md`
  - `remotion-captions\REFERENCE.md`
  - `remotion-captions\transcribe-captions.md`
  - `remotion-create\REFERENCE.md`
  - `remotion-create\tailwind.md`
  - `remotion-create\video-layout.md`
  - `remotion-docs\REFERENCE.md`
  - *...и ещё 130 файлов*

### `remotion-captions`
- **Название:** remotion-captions
- **Описание:** Transcribing, displaying and animating captions
- **SKILL.md:** Присутствует
- **Вложенные файлы (5):**
  - `display-captions.md`
  - `import-srt-captions.md`
  - `transcribe-captions.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-create`
- **Название:** remotion-create
- **Описание:** Create a new Remotion video
- **SKILL.md:** Присутствует
- **Вложенные файлы (4):**
  - `tailwind.md`
  - `video-layout.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-docs`
- **Название:** remotion-docs
- **Описание:** Search Remotion documentation
- **SKILL.md:** Присутствует
- **Вложенные файлы (2):**
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-interactivity`
- **Название:** remotion-interactivity
- **Описание:** Structure Remotion markup for interactivity
- **SKILL.md:** Присутствует
- **Вложенные файлы (3):**
  - `inline-effects.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-maps`
- **Название:** remotion-maps
- **Описание:** Remotion Map animation knowledge
- **SKILL.md:** Присутствует
- **Вложенные файлы (31):**
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`
  - `techniques\cesium\TECHNIQUE.md`
  - `techniques\mapbox\TECHNIQUE.md`
  - `techniques\maplibre\TECHNIQUE.md`
  - `techniques\maptiler\TECHNIQUE.md`
  - `techniques\static-map\TECHNIQUE.md`
  - `techniques\cesium\assets\cesium-path.json`
  - `techniques\cesium\assets\CesiumFlythrough.tsx`
  - `techniques\cesium\assets\city-path.json`
  - *...и ещё 21 файлов*

### `remotion-markup`
- **Название:** remotion-markup
- **Описание:** Content, animation and effects best practices
- **SKILL.md:** Присутствует
- **Вложенные файлы (65):**
  - `3d.md`
  - `audio-visualization.md`
  - `audio.md`
  - `calculate-metadata.md`
  - `compositions.md`
  - `connected-compositions.md`
  - `cropping.md`
  - `effects.md`
  - `embedding-videos.md`
  - `ffmpeg.md`
  - *...и ещё 55 файлов*

### `remotion-multimedia`
- **Название:** remotion-multimedia
- **Описание:** Interacting with Mediabunny
- **SKILL.md:** Присутствует
- **Вложенные файлы (5):**
  - `get-audio-duration.md`
  - `get-video-dimensions.md`
  - `get-video-duration.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-render`
- **Название:** remotion-render
- **Описание:** Export a Remotion video
- **SKILL.md:** Присутствует
- **Вложенные файлы (3):**
  - `transparent-videos.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-saas`
- **Название:** remotion-saas
- **Описание:** Build an app with Remotion
- **SKILL.md:** Присутствует
- **Вложенные файлы (5):**
  - `framework.md`
  - `player.md`
  - `rendering.md`
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-studio`
- **Название:** remotion-studio
- **Описание:** Preview a Remotion video
- **SKILL.md:** Присутствует
- **Вложенные файлы (2):**
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

### `remotion-upgrade`
- **Название:** remotion-upgrade
- **Описание:** Upgrade Remotion, and related packages
- **SKILL.md:** Присутствует
- **Вложенные файлы (2):**
  - `agents\openai.yaml`
  - `assets\remotion-icon.svg`

