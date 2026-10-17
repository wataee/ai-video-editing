# CHANGELOG

Все изменения в проекте документируются в этом файле.

## [Unreleased] - 2026-10-17

### Блок B. Сборка и зависимости
- **B1 (`package.json`, `package-lock.json`):** Добавлено поле `"engines": { "node": ">=22.0.0" }`. Выполнена пересборка `package-lock.json` через `npm install`, устранен конфликт `@types/node` и `undici-types`. Обеспечена чистая воспроизводимая установка `npm ci` на Node.js 22 и 24.
- **B2 (`package.json`):** Добавлен npm-скрипт `"typecheck": "tsc --noEmit"`. Проверено: `npm run typecheck` завершается с 0 ошибок.
- **B3 (`.github/workflows/ci.yml`, `pytest.ini`):** Создан GitHub Actions CI workflow на базе Ubuntu Linux с матрицей Node 22/24 и Python 3.12. Включены шаги: `npm ci`, `npm run typecheck`, компиляция Python (`python -m py_compile tools/*.py`), прогон тестов (`pytest tests/ -m "not slow"`). В `pytest.ini` зарегистрирован маркер `slow`.

### Блок C. Рендер на реальном видео
- **C1 (`src/compositions/ReelFromPlan.tsx`, `tools/render_clip.py`):** Удалена хрупкая Windows-специфичная регулярка путей `C:\...AI-Video-Editing`. Видео передается надежно: `render_clip.py` создает изолированную структуру временной public-папки со ссылками на `assets/` и исходный видеоролик, передавая `--public-dir` в Remotion. Относительные пути клиентов (`clients/<имя>/work/...`) корректно разрешаются.
- **C2 (`src/compositions/ReelFromPlan.tsx`, `src/Root.tsx`):** В композицию `ReelFromPlan` добавлена функция `calculateMetadata`: динамический расчет длительности `durationInFrames = Math.round(plan.target_duration_sec * fps)`, а также габаритов (по умолчанию 1080×1920) и fps (30) из плана.
- **C3 (`tools/render_clip.py`, `src/components/SfxAudio.tsx`):**
  - Убран вызов `cmd.exe /c`; запуск `npx` реализован кросс-платформенно (`shutil.which("npx.cmd")` / `shutil.which("npx")`).
  - Ошибки FFmpeg не глушатся: вывод перенаправлен в `stderr`.
  - Ошибки сведения звука (`tools/mix.py`) приводят к остановке с ошибкой (exit code 1). Для явного разрешения использования исходного голоса добавлен флаг `--allow-voice-fallback`.
  - Добавлена валидация готового MP4 через `ffprobe` (наличие видеопотока, аудиопотока и совпадение длительности с планом в пределах допуска).
  - В `SfxAudio.tsx` поддержаны расширения `.wav` при их отсутствии в идентификаторе бита и предотвращена загрузка пустых/'TODO' звуков.
- **C4 (`tests/test_e2e.py`):** Разработан сквозной E2E-тест: синтез 10-секундного тестового ролика (testsrc + sine) через `ffmpeg` -> `tools/ingest.py` -> `tools/plan_scaffold.py` -> установка `approved: true` -> `tools/render_clip.py` -> валидация контейнера через `ffprobe` (1080×1920, 30 fps, аудиопоток, длительность ±0.2 с). Тест помечен `@pytest.mark.slow`.

### Блок D. Approval Gate
- **D1 (`package.json`):** Гейт `node tools/check_approval.mjs` подключен во все финальные npm-скрипты рендера: `render:full`, `render:stems`, `render:greenscreen`. Скрипт `draft` оставлен без гейта для свободного чернового предпросмотра.
- **D2 (`tools/check_approval.mjs`):** Исправлено поведение гейта: при отсутствии файла плана монтажа процесс немедленно завершается с ошибкой (`process.exit(1)`). Добавлена поддержка аргумента `--plan <путь>`.

### Блок E. Документация и порядок
- **E1 (`CLAUDE.md`):** Сокращен до 42 строк: содержит 10 жестких правил проекта и карту всех 16 рулбуков со ссылками. Избыточные дублирующие описания удалены.
- **E2 (`docs/`, `rules/`, `tools/qa.py`):**
  - Устранены ссылки на несуществующие `GEMINI.md` и `sync_gemini.py`.
  - Зафиксировано актуальное число рулбуков (16 рулбуков, включая `07-creator-style-presets.md`).
  - Документ `docs/after-effects-mcp-integration.md` помечен как архивный и запрещенный к использованию в продакшене.
  - Устаревшая директория `rules/templates` удалена, единым источником шаблонов объявлена `.claude/rulebooks/templates/`.
- **E3 (`README.md`):** Убрано заявление "production-ready". Добавлен подробный раздел «Статус» с четким разделением на проверенное и UNVERIFIED, требования к окружению и пошаговый быстрый старт на синтетическом видео.
- **E4 (`.gitignore`, `.claude/settings.json`):** Добавлен `.claude/settings.json` с директивой `permissions.deny` на `references/**` и `tools/_scratch/**`. В `.gitignore` внесены `tools/_scratch/` и сторонние каталоги `references/`.
