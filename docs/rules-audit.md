# 📑 Аудит правил и системы регламентов AI-Video-Editing

> **Дата аудита:** 16 октября 2026 г.  
> **Цель:** Инвентаризация всех разрозненных файлов правил, выявление противоречий и фиксация единого источника правды.

---

## 1. Таблица всех файлов правил в репозитории

| Файл | Строк | Категория / Описание |
| :--- | :---: | :--- |
| `CLAUDE.md` | 132 | Главный контекст и регламент для Claude Code (Remotion + AE) |
| `GEMINI.md` | 74 | Регламент для Gemini CLI / Antigravity |
| `hooks.md` | 167 | Редакционные правила поиска фрагментов, хуков и холодного старта |
| `style-guide.md` | 125 | Визуальный стиль, безопасные зоны, правила смысловых субтитров |
| `qa-checklist.md` | 154 | Чек-лист контроля качества видео, аудио и субтитров |
| `production-pipeline.md` | 125 | Пошаговый пайплайн производства видео (FFmpeg, Whisper, Remotion) |
| `rules/anti-slop.md` | 56 | 8 смертных грехов дешевого нейрослопа и профессиональные правила |
| `rules/editing-brain.md` | 82 | Когнитивная модель монтажа, темп, удержание внимания |
| `rules/sound-design-guide.md` | 90 | Руководство по саунд-дизайну и 3-слойному сведению звука |
| `rules/modes/ae-montage.md` | 90 | Подключаемый регламент монтажа в After Effects MCP |
| `rules/modes/content-hook.md` | 40 | Регламент генерации хуков для социальных сетей |
| `rules/modes/remotion-render.md` | 67 | Регламент сборки и рендера в Remotion |
| `rules/templates/edit_plan.template.json` | 96 | Устаревший шаблон плана монтажа |
| `rules/templates/project_state.template.md` | 23 | Шаблон фиксации состояния проекта клиента |
| `.claude/design-system/creator-archetypes.md` | 132 | Дизайн-токены и архетипы авторов (Minimalist, Noir, Vox, etc.) |
| `.claude/design-system/sfx-mapping.md` | 43 | Маппинг визуальных триггеров на звуковые файлы |
| `.claude/design-system/typography-scale.md` | 68 | Типографическая шкала, размеры кеглей и караоке-подсветка |
| `.claude/rulebooks/01-hooks-and-script.md` | 34 | Рукбук 01: Архитектура хука и сценария |
| `.claude/rulebooks/02-cut-and-audio-sync.md` | 38 | Рукбук 02: Стандарты склеек и аудиосинхронизации |
| `.claude/rulebooks/03-beat-map-and-planning.md` | 45 | Рукбук 03: Битовая карта и планирование сцен |
| `.claude/rulebooks/04-visual-styles-and-safe-zones.md` | 60 | Рукбук 04: Визуальные стили и безопасные зоны 9:16 |
| `.claude/rulebooks/05-qa-checklist.md` | 50 | Рукбук 05: 6-точечный чек-лист инспекции |
| `.claude/rulebooks/06-self-learning-notes.md` | 29 | Рукбук 06: Протокол самообучения на замечаниях |
| `.claude/rulebooks/07-creator-style-presets.md` | 51 | Рукбук 07: Пресеты стилей авторов |
| `.claude/rulebooks/08-typography-pairings.md` | 33 | Рукбук 08: Шрифтовые пары и правила типографики |
| `.claude/rulebooks/09-sfx-choreography.md` | 30 | Рукбук 09: Хореография звуковых акцентов |
| `.claude/rulebooks/10-hook-patterns.md` | 37 | Рукбук 10: 6 визуальных архетипов хуков |
| `.claude/skills/video-editor/SKILL.md` | 43 | Системный навык видеомонтажера для Claude Code |
| `assets/05_RULES/CLAUDE_EDITING_SYSTEM_RULES.md` | 67 | Устаревшие правила Joseph/Ultimate Editors (агрессивный SFX) |
| `assets/05_RULES/README.md` | 67 | Дубликат устаревших правил Joseph/Ultimate Editors |
| `clients/_template/brief.json` | 36 | Шаблон брифа клиента с устаревшим TheBoldFont и полями 50px |

---

## 2. Таблица выявленных противоречий и их разрешение

| Параметр / Аспект | Значение в старых файлах | Где встречалось | **Единое принятое решение (v2)** | Где зафиксировано |
| :--- | :--- | :--- | :--- | :--- |
| **Главный движок** | After Effects MCP как главный инструмент по умолчанию | `README.md`, `rules/modes/ae-montage.md`, `assets/05_RULES/` | **Remotion 4.x (React 19 + TypeScript)** — главный движок. After Effects MCP — строго вторичный путь для единичной графики / AEP проектов по запросу после утверждения плана. | `CLAUDE.md`, `.claude/rulebooks/03-beat-map-and-planning.md` |
| **Боковые поля безопасной зоны (1080×1920)** | Слева 50 px, справа 130 px (или 100 px с обеих сторон) | `clients/_template/brief.json`, `rules/modes/ae-montage.md`, `style-guide.md` | **Сверху 220 px, снизу 380 px, слева 100 px, справа 130 px.** Область субтитров строго `y: 1120..1380`. | `.claude/rulebooks/04-visual-styles-and-safe-zones.md`, `clients/_template/brief.json` |
| **Шрифт заголовков и титров** | `TheBoldFont` (не имеет кириллицы, латиница only) | `clients/_template/brief.json`, старые скрипты AE | **Заголовок: Montserrat (ExtraBold/Black); Текст/субтитры: Manrope или Inter; Акцент 2-й слой: Caveat.** Шрифт `TheBoldFont` полностью запрещен. | `.claude/rulebooks/08-typography-pairings.md`, `clients/_template/brief.json` |
| **Громкость SFX в миксе** | Абсолютные уровни: вуши -10..-12 dB, текстуры -6..-7 dB, удары -5 dB, в скриптах AE до -3 dB | `assets/05_RULES/*`, `rules/sound-design-guide.md`, `tools/build_perfect_master_reel.mjs` | **Громкость SFX строго относительно RMS речи:** удары и райзеры **−14 dB**, текстуры (клики/поп) **−16 dB**, свисты (whoosh) **−20 dB**, музыка **−22 dB** и ниже с сайдчейном. Лимит: не более 6 SFX на 30 сек. Зумы без звука! | `.claude/rulebooks/09-sfx-choreography.md`, `tools/mix.py` |
| **Цветокоррекция iPhone HDR** | Наложение слоя Exposure -2.2 и Gamma 0.92 поверх кадра в After Effects + черная виньетка 30% | `tools/build_perfect_master_reel.mjs`, `tools/polish_ae_comp.mjs`, `assets/05_RULES/` | **Запрещено лечить HDR слоями Exposure в AE.** Исходник обязан проходить аппаратный `ingest` в SDR Rec.709 (BT.2390/hable tonemapping) на этапе подготовки. Виньетки, затемняющие кадр, запрещены. | `.claude/rulebooks/02-cut-and-audio-sync.md`, `tools/ingest.py` |
| **Схема плана монтажа (Edit Plan)** | Свободная нарезка без доказательств, без полей мотивации, без утверждения человеком | `rules/templates/edit_plan.template.json` | **Построчный план (beat table)** на каждый бит: `line`, `visual`, `proof_source`, `camera`, `cut_motivation`, `sfx`, `why`, `approved: false` (финальный рендер заблокирован до `approved: true`). | `.claude/rulebooks/03-beat-map-and-planning.md`, `edit_plan.template.json` |

---

## 3. План консолидации файлов правил

1. **Единый источник правды:**
   - Короткий индекс: `CLAUDE.md` (до 120 строк).
   - Генератор: `tools/sync_gemini.py` автоматически создает `GEMINI.md` из `CLAUDE.md`.
   - Подробные регламенты: `.claude/rulebooks/` (номера 01–15).
   - Дизайн-токены: `.claude/design-system/`.
2. **Перенос и архивация дубликатов:**
   - Дубликаты из `assets/05_RULES/` переносятся в `_archive/2026-10-16/assets_05_RULES/`.
   - Корневые `hooks.md`, `style-guide.md`, `qa-checklist.md`, `production-pipeline.md`, `rules/*` интегрируются в сквозную нумерацию `.claude/rulebooks/`, а старые дублирующие файлы переносятся в `_archive/2026-10-16/`.
