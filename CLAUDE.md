# CLAUDE.md — Vertical Video Editing Engine (9:16)

> **Primary Engine:** Remotion 4.x (React 19 + TypeScript) | **Secondary:** After Effects ExtendScript monolith
> **Target Format:** Strict 9:16 Vertical Video (1080 × 1920, CFR 30 fps) | **Safe Zones:** 220/380/100/130 px

---

## 10 HARD CONSTRAINTS (ЖЕСТКИЕ ПРАВИЛА)

1. **PRIMARY ENGINE REMOTION & EXTENDSCRIPT MONOLITH:** Remotion (`src/`) — главный движок. After Effects вторичен: только генерация монолитного `scripts/build_ae_project.jsx` для ручного запуска в AE (`File -> Scripts -> Run Script File...`) с `app.beginUndoGroup`/`app.endUndoGroup`. Использование любых MCP-серверов AE запрещено.
2. **ZERO COMMENTS IN CODE:** Никаких комментариев (`//`, `/* */`, `#`) в `.ts`, `.tsx`, `.js`, `.mjs`, `.json`, `.css`, `.jsx`.
3. **STRICT SAFE ZONES (1080×1920):** Сверху 220 px, снизу 380 px, слева 100 px, справа 130 px (`x: 100..950`, `y: 220..1540`). Субтитры строго `y: 1120..1380`. Все элементы оборачивать в `<SafeZoneContainer>`.
4. **LOCAL FONTS ONLY:** Шрифты строго локально из `assets/fonts/` (`Montserrat`, `Inter`, `Unbounded`, `Manrope`, `Caveat`) через `@font-face` (`src/styles/fonts.css`). Системные дефолты (`Arial`, `Roboto`, `TheBoldFont`) категорически запрещены.
5. **LOCAL SFX VIA <AUDIO/> WITH FRAME CALCULATION:** Звуковые эффекты только из `assets/sfx/` через `<Audio/>` (`SfxAudio`) с точным расчетом фреймов. Уровни относительно речи: удары −14 dB, текстуры −16 dB, вуши −20 dB, музыка −22 dB с ducking. Не более 6 SFX на 30с. Зумы без звука!
6. **REMOTION SPRING PHYSICS (NO CSS TRANSITIONS):** Запрещены CSS keyframes и transitions. Всё движение реализуется только математикой Remotion: `spring({ fps, frame, config })` и `interpolate()` с овершутом 2–5%.
7. **ANTI-SLOP TEXTURING & CAMERA DRIFT:** Обязательный глобальный оверлей `<ProceduralNoiseOverlay/>` (3–5%) поверх всех сцен и плавный микро-дрифт камеры (`scale` 1.0 -> 1.03) за длительность сцены.
8. **BEAT SHEET BEFORE CODE:** Первый шаг — формирование `edit_plan.json` (`beat_sheet.json`): тайминги, удары, смены ракурсов, точки SFX. Рендер компонентов только после утверждения структуры человеком.
9. **MANDATORY INGEST & APPROVAL GATE:** iPhone HDR обязан проходить `tools/ingest.py` (SDR Rec.709, CFR 30 fps). В плане `"approved": false` по умолчанию, финальный рендер заблокирован approval gate до подтверждения человеком.
10. **ANTI-MISHMASH PROTOCOL & STYLE ISOLATION:** Ровно 1 пресет стиля на проект. Смешивание элементов из разных стилей запрещено. Всегда следовать `references/pinterest/<style>/assembly_blueprint.md`.

---

## RULEBOOK MAP (.claude/rulebooks/)

- [01-hooks-and-script.md](.claude/rulebooks/01-hooks-and-script.md) — Архитектура хука (0-3s)
- [02-cut-and-audio-sync.md](.claude/rulebooks/02-cut-and-audio-sync.md) — Склейки, Ingest SDR Rec.709, относительные уровни звука
- [03-beat-map-and-planning.md](.claude/rulebooks/03-beat-map-and-planning.md) — Beat Sheet JSON, пруфы и approval gate
- [04-visual-styles-and-safe-zones.md](.claude/rulebooks/04-visual-styles-and-safe-zones.md) — Безопасные зоны (220/380/100/130) и шрифты
- [05-qa-checklist.md](.claude/rulebooks/05-qa-checklist.md) — Чек-лист контроля качества на 10 fps
- [06-self-learning-notes.md](.claude/rulebooks/06-self-learning-notes.md) — Протокол самообучения на замечаниях
- [07-creator-style-presets.md](.claude/rulebooks/07-creator-style-presets.md) — Стили авторов и креативные ДНК
- [08-typography-pairings.md](.claude/rulebooks/08-typography-pairings.md) — Локальные шрифты (запрет Arial/Roboto/TheBoldFont)
- [09-sfx-choreography.md](.claude/rulebooks/09-sfx-choreography.md) — Звук: assets/sfx через <Audio/> и относительные dB
- [10-hook-patterns.md](.claude/rulebooks/10-hook-patterns.md) — 6 архетипов хуков
- [11-hook-library.md](.claude/rulebooks/11-hook-library.md) — Каталог проверенных хуков
- [12-anti-slop.md](.claude/rulebooks/12-anti-slop.md) — 8 правил anti-slop, процедурный шум и микро-дрифт
- [13-ae-secondary-engine.md](.claude/rulebooks/13-ae-secondary-engine.md) — Регламент After Effects ExtendScript (монолитные скрипты)
- [14-production-pipeline.md](.claude/rulebooks/14-production-pipeline.md) — 4-этапный сквозной пайплайн производства
- [15-upwork-ops.md](.claude/rulebooks/15-upwork-ops.md) — Upwork: intake brief, proposal, delivery & rates
- [16-anti-mishmash-cohesion.md](.claude/rulebooks/16-anti-mishmash-cohesion.md) — Защита от «солянки», стилевая изоляция
- **Шаблоны планов:** [.claude/rulebooks/templates/](.claude/rulebooks/templates/)
- **Дизайн-система:** [.claude/design-system/](.claude/design-system/)
