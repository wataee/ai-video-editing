# CLAUDE.md — Vertical Video Editing Engine (9:16)

> **Workstation Root:** `C:\Users\timur\Videos\AI-Video-Editing`  
> **Primary Engine:** Remotion 4.x + React 19 + TypeScript + FFmpeg (After Effects via monolithic ExtendScript is secondary)  
> **Target Format:** Strict 9:16 Vertical Video (1080 × 1920, CFR 30 fps)  
> **Core Role:** Senior Video Editor & Technical Motion Director

---

## 1. 9 HARD CONSTRAINTS (ЖЕСТКИЕ ОГРАНИЧЕНИЯ)

1. **PRIMARY ENGINE REMOTION & EXTENDSCRIPT MONOLITH:** Remotion (`src/components`, `src/config`) — главный движок. After Effects вторичен: взаимодействие с After Effects происходит ИСКЛЮЧИТЕЛЬНО путем генерации готового монолитного файла сценария ExtendScript (`scripts/build_ae_project.jsx` или `scripts/import_to_ae.jsx`), который пользователь запускает в AE вручную через `File -> Scripts -> Run Script File...`. Внутри каждого такого скрипта код обязан быть обернут в `app.beginUndoGroup("AI Video Build")` и `app.endUndoGroup()`. Использование любых MCP-серверов AE запрещено.
2. **ZERO COMMENTS IN CODE:** Никаких комментариев (`//`, `/* */`, `#`) в коде (`.ts`, `.tsx`, `.js`, `.mjs`, `.json`, `.css`, `.jsx`).
3. **STRICT SAFE ZONES (1080×1920):** Сверху 220 px, снизу 380 px, слева 100 px, справа 130 px (`x: 100..950`, `y: 220..1540`). Субтитры strictly `y: 1120..1380`. Все элементы оборачивать в `<SafeZoneContainer>`.
4. **LOCAL FONTS ONLY (NO ARIAL/ROBOTO):** Загружать шрифты строго локально из `assets/02_FONTS/` (`Montserrat`, `Inter`, `Unbounded`, `Manrope`, `Caveat`) через нативные `@font-face` (`src/styles/fonts.css`). Системные дефолты (`Arial`, `Roboto`, `TheBoldFont`) КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНЫ.
5. **LOCAL SFX VIA <AUDIO/> WITH FRAME CALCULATION:** Использовать звуковые эффекты ТОЛЬКО из локальной папки `assets/01_SFX/` через компонент Remotion `<Audio/>` (`SfxAudio`) с точным расчетом фреймов (`startFrom`, кривая громкости, затухание fade-in/fade-out). Уровни strictly относительные: удары `−14 dB`, текстуры `−16 dB`, вуши `−20 dB`, музыка `−22 dB` с ducking. Не более 6 SFX на 30с. Зумы без звука!
6. **REMOTION SPRING PHYSICS (NO CSS TRANSITIONS):** Категорически запрещены CSS-анимации (`@keyframes`) и обычные `transition: all`. Всё движение реализуется только математикой Remotion: `spring({ fps, frame, config: { damping, mass, stiffness } })` и `interpolate()` с овершутом/отскоком (2–5%).
7. **ANTI-SLOP TEXTURING & CAMERA DRIFT:** Обязательный глобальный оверлей `<ProceduralNoiseOverlay/>` (SVG `<feTurbulence>`, непрозрачность 3–5%) поверх всех сцен против «стерильного векторного рендера». Легкий параллакс и плавный микро-дрифт камеры (`scale` от 1.0 до 1.03) за длительность сцены.
8. **BEAT SHEET BEFORE CODE:** Агент обязан ПЕРВЫМ ШАГОМ всегда выводить JSON-структуру таймлайна (`beat_sheet.json`): тайминги сцен, кадры ударов (`hits`), смены ракурсов и точки запуска SFX, и ТОЛЬКО после утверждения структуры человеком писать рендер-компоненты.
9. **MANDATORY INGEST & APPROVAL GATE:** iPhone HDR обязан проходить `tools/ingest.py` (SDR Rec.709, CFR 30 fps). В плане поле `"approved"` по умолчанию `false`. Финальный рендер заблокирован до утверждения человеком. Автоматический QA проверяет ролик с частотой 10 кадров/сек.

---

## 2. 4-STAGE PRODUCTION WORKFLOW

```
[1. Ingest & Transcript] ➔ [2. Beat Sheet & Contact Sheet] ➔ [3. Draft Assembly] ➔ [4. 10 FPS QA & Final Mix]
```

- **Этап 1: Ингейст и текст.** `tools/ingest.py <raw>` (SDR Rec.709, CFR 30), `tools/transcribe.bat` (faster-whisper), чистка дублей (оставляем только последний чистый дубль).
- **Этап 2: Битовый план и раскадровка.** Агент выводит `beat_sheet.json` (кадры ударов, смена ракурсов, точки SFX). `tools/beat_table.py` проверяет структуру на слайд-шоу. `tools/plan_contact_sheet.py` рендерит раскадровку ключевых кадров. Человек утверждает структуру (`approved: true`).
- **Этап 3: Сборка компонентов.** Сборка сцен в Remotion с Remotion spring-физикой, микро-дрифтом (1.0 -> 1.03) и процедурным шумом `<ProceduralNoiseOverlay/>`. Предпросмотр: `npm run draft`.
- **Этап 4: QA и финальный микс.** `tools/qa.py` (проверка 10 fps: повтор анимаций, фликкер <0.5с, скорость чтения, закрытие лица, дубли слов, черные кадры, фриз). Сведение звука через `tools/mix.py`. Финальный рендер: `npm run render:clip`.

---

## 3. FILE & RULEBOOK MAP

```
.claude/
├── rulebooks/
│   ├── 01-hooks-and-script.md               # Архитектура хука (0-3s)
│   ├── 02-cut-and-audio-sync.md             # Склейки, Ingest SDR, относительные уровни звука
│   ├── 03-beat-map-and-planning.md          # Beat Sheet JSON, пруфы и гейт утверждения
│   ├── 04-visual-styles-and-safe-zones.md   # Безопасные зоны (220/380/100/130) и шрифты
│   ├── 05-qa-checklist.md                   # Чек-лист контроля на 10 fps
│   ├── 06-self-learning-notes.md            # Протокол самообучения на замечаниях
│   ├── 07-creator-style-presets.md          # Стили авторов
│   ├── 08-typography-pairings.md            # Шрифты: локальные assets/02_FONTS (запрет Arial/Roboto)
│   ├── 09-sfx-choreography.md               # Звук: assets/01_SFX через <Audio/> с расчетом фреймов
│   ├── 10-hook-patterns.md                  # 6 архетипов хуков
│   ├── 11-hook-library.md                   # Каталог хуков
│   ├── 12-anti-slop.md                      # 8 правил anti-slop, процедурный шум и микро-дрифт
│   ├── 13-ae-secondary-engine.md            # Регламент After Effects ExtendScript (монолитные скрипты)
│   └── 14-production-pipeline.md            # Сквозной пайплайн производства
└── design-system/
    ├── creator-archetypes.md
    ├── typography-scale.md
    └── sfx-mapping.md
```

---

## 4. ESSENTIAL COMMANDS

- `npm run preview` — запуск Remotion Studio для визуальной проверки компонентов.
- `npm run render:stems` — пакетный рендер прозрачных UI-стемов (ProRes 4444 с альфа-каналом в `out/stems/`).
- `npm run render:full` — полный рендер мастер-композиции.
- `npm run draft` — быстрый черновой предпросмотр Remotion (половинное разрешение).
- `npm run render:clip -- [Composition] [out.mp4]` — финальный рендер (требует `approved: true`).
- `python tools/ingest.py <raw_video>` — аппаратный перевод HDR в SDR Rec.709 + CFR 30.
- `python tools/plan_scaffold.py <whisper.json>` — автоматический каркас плана из транскрипта.
- `python tools/beat_table.py <plan.json>` — построение таблицы битов с проверкой на слайд-шоу.
- `python tools/plan_contact_sheet.py <plan.json>` — генерация контактного листа кадров до рендера.
- `python tools/mix.py <voice.wav> <plan.json>` — сведение звука по относительным dB и сайдчейн.
- `python tools/qa.py <video.mp4> [plan.json]` — автоматический аудит видео на 10 fps.
- **After Effects Build:** запуск `scripts/build_ae_project.jsx` или `scripts/import_to_ae.jsx` через `File -> Scripts -> Run Script File...`.
