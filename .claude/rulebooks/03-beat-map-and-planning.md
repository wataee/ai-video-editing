# 03. Beat Map & Production Planning

## 1. Production Pipeline Order (Mandatory Sequence)
To prevent robotic AI slop and ensure the video meets live-editor quality, follow this exact sequence:

```
[1. Transcript & Audio Slicing]
        ↓
[2. Beat Sheet JSON Generation (beat_sheet.json)]
        ↓
[3. Beat Table (Sentence-by-sentence plan)]
        ↓
[4. Plan Contact Sheet (Stills before render)]
        ↓
[5. Human Approval Gate (approved: true)]
        ↓
[6. Remotion Component Construction (Only after step 5!)]
        ↓
[7. Draft Preview (npm run draft)]
        ↓
[8. 10 FPS Automated QA Check]
        ↓
[9. Final Render (npm run render:clip)]
```

## 2. Hard Rule: Beat Sheet Before Code
**Агент обязан первым шагом всегда выводить JSON-структуру таймлайна (`beat_sheet.json`):**
- Точные тайминги сцен (`start_frame`, `end_frame`, `duration_frames`).
- Кадры ударов (`hit_frames`), где смысловой акцент фразы совпадает с визуальным или звуковым триггером.
- Смены ракурсов камеры (`camera_angle`: `push-in`, `static`, `push-out`).
- Точки запуска SFX (`sfx_triggers`) с привязкой к локальным файлам `assets/sfx/`.
- **Запрещено** приступать к написанию или редактированию React/Remotion компонентов до того, как структура утверждена человеком (`approved: true`).

## 3. Mandatory Approval Gate
- В `edit_plan.json` и `beat_sheet.json` поле `"approved"` по умолчанию равно `false`.
- `npm run render:clip` блокирует рендер финального ролика с кодом ошибки 1, если `approved !== true`.
- Черновые рендеры (`npm run draft`) разрешены в любой момент для промежуточной визуальной оценки.

## 4. Beat Table Schema
Каждое предложение или фраза спикера транскрипта формирует отдельный бит:

| Field | Type | Valid Values / Description |
|---|---|---|
| `beat_index` | integer | Sequential index (0, 1, 2...) |
| `line` | string | Exact spoken sentence or phrase |
| `time_range` | string | `[start_sec, end_sec]` |
| `visual` | enum | `speaker` \| `proof` \| `typography` \| `chart` \| `broll` |
| `proof_source` | string / null | Path to real verified artifact (screenshot, code, product, doc) |
| `camera` | enum | `static` \| `push-in` \| `push-out` \| `pan-left` \| `pan-right` |
| `cut_motivation` | enum | `THESIS_SHIFT` \| `EMOTIONAL_PUNCH` \| `PROOF_INJECTION` \| `RHYTHMIC_CONTRAST` \| `FATIGUE_RESET` |
| `sfx` | string / null | ID from `assets/sfx/` (`assets/sfx/sfx_catalog.json`) or `none` |
| `why` | string | Exactly one sentence justifying the visual choice and cut |
| `approved` | boolean | `false` by default, toggled to `true` by human review |

## 5. Visual Balance & Anti-Slide Rule
- **Proof-First**: Если спикер называет цифру, факт или результат, `visual` обязан быть `proof` или `chart` со ссылкой на реальный файл (`proof_source`).
- **Анти-слайдшоу**: Если `visual: typography` встречается подряд более 2 раз, `tools/beat_table.py` выдает предупреждение: *"Ролик превращается в слайд-шоу из текста — добавьте лицо спикера или реальный материал (proof)"*.
