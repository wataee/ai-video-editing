# 🎬 AI Video Editing — Vertical Video Engine (9:16)

Движок вертикального монтажа коротких видео (9:16, 1080×1920, 30 fps) на базе **Remotion 4.x (React 19 + TypeScript)**, **FFmpeg** и **After Effects ExtendScript** (монолитные скрипты автоматизации).

---

## 📊 Статус (Status & Verification)

### ✅ Проверено автотестами и реальными запусками
- **Remotion Headless Render:** Сборка и рендеринг мастер-композиции `ReelFromPlan` на реальном видеоряде (1080×1920, 30 fps, процедурный шум, микро-дрифт, караоке-субтитры).
- **Сквозной E2E пайплайн (`tests/test_e2e.py`):** Автоматическая генерация тестового видео -> аппаратный `ingest` -> построение плана `plan_scaffold` -> установка `approved: true` -> финальный рендер `render_clip.py` -> проверка структуры контейнера через `ffprobe` (видео, аудио, длительность ±0.2 с).
- **Кросс-платформенный рендер (`tools/render_clip.py`):** Запуск через нативный `npx`/`npx.cmd` без вызова `cmd.exe`; передача видео через изолированный `--public-dir`; вывод ошибок ffmpeg в stderr; флаг `--allow-voice-fallback`; валидация аудиодорожки и хронометража по `ffprobe`.
- **Approval Gate (`tools/check_approval.mjs`):** Защита всех финальных npm-скриптов (`render:full`, `render:stems`, `render:greenscreen`). Остановка с exit code 1 при отсутствии файла плана или при `approved: false`. Черновой драфт `npm run draft` работает без блокировки.
- **Динамические метаданные (`calculateMetadata`):** Автоматический расчет длительности `durationInFrames = round(plan.target_duration_sec * fps)` и габаритов 1080×1920 @ 30 fps.
- **Сглаживание траектории спикера (`tests/test_reframe_smoothing.py`):** Фильтр deadband против микро-джиттера, ограничение скорости панорамирования, удержание позиции при потере лица.
- **Сборка и типизация:** `npm ci` и `npm run typecheck` (0 ошибок на Node.js 22 и 24).
- **CI пайплайн:** GitHub Actions workflow на Ubuntu Linux (Node 22/24, Python compile check, unit tests).

### ⚠️ UNVERIFIED (требует ручной проверки человеком / окружения)
- **Adobe After Effects ExtendScript:** Выполнение монолитного `scripts/build_ae_project.jsx` внутри GUI After Effects 2025/2026 пользователем вручную.
- **Локальный Whisper:** Транскрибация длинных видео через `tools/transcribe.bat` / faster-whisper с GPU CUDA.
- **Hardware Ingest на macOS:** Аппаратное кодирование VideoToolbox (`-c:v h264_videotoolbox`) требует реального macOS хоста.

---

## 💻 Системные требования

- **Node.js:** `>= 22.0.0` (протестировано на Node 22 и 24)
- **Python:** `>= 3.10` (протестировано на Python 3.12 и 3.14)
- **FFmpeg & FFprobe:** `>= 6.0` в системном `PATH` (поддержка h264, aac, libplacebo/zscale)
- **ОС:** Windows 10/11, Linux (Ubuntu 22.04+), macOS

---

## ⚡ Быстрый старт на тестовом видео

```bash
# 1. Установка зависимостей
npm ci

# 2. Проверка типов и целостности путей
npm run typecheck
npm run check

# 3. Запуск сквозного E2E-теста (полный цикл: генерация -> ingest -> scaffold -> render -> ffprobe)
pytest tests/test_e2e.py -s -v

# 4. Ручной запуск пайплайна на тестовом ролике:
# Сгенерировать тестовое видео (10 сек)
ffmpeg -y -f lavfi -i testsrc=duration=10:size=1080x1920:rate=30 -f lavfi -i sine=frequency=440:duration=10 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k work/ingest/raw_test.mp4

# Выполнить Ingest (SDR Rec.709 CFR 30 + proxy)
python tools/ingest.py work/ingest/raw_test.mp4 --output_dir work/ingest

# Собрать финальный клип (требует approved: true в плане)
python tools/render_clip.py work/plan/edit_plan.json --output out/test_final.mp4
```

---

## 🛠️ Основные команды

| Команда | Описание |
| :--- | :--- |
| `npm run preview` | Запуск интерактивной Remotion Studio для визуальной инспекции компонентов |
| `npm run draft` | Быстрый черновой предпросмотр композиции Remotion (без Approval Gate) |
| `npm run typecheck` | Строгая проверка TypeScript (`tsc --noEmit`, 0 ошибок) |
| `npm run check` | Валидация всех локальных путей к ассетам и правилам (`tools/check_paths.py`) |
| `npm run render:full` | Финальный мастер-рендер (блокируется Approval Gate при `approved: false`) |
| `npm run render:stems` | Пакетный рендер UI-стемов ProRes 4444 с альфа-каналом |
| `npm run render:clip` | Сквозной продакшен-рендер с калибровкой аудио и проверкой ffprobe |
| `pytest tests/ -m "not slow"` | Запуск быстрых модульных тестов пайплайна |
| `pytest tests/test_e2e.py` | Полный сквозной интеграционный E2E-тест |

---

## 🔧 Устранение неполадок (Troubleshooting)

### 1. Chromium не скачивается или ошибки рендера Remotion
Remotion использует headless Chromium для рендера кадров. Если при первом запуске браузер не скачался автоматически или возникли проблемы с сетью/правами:
```bash
npx remotion browser ensure
```
В средах с ограниченным доступом к сети или за прокси можно указать путь к установленному браузеру через переменную окружения `PUPPETEER_EXECUTABLE_PATH` или параметры Remotion.

### 2. Ошибка "ffmpeg / ffprobe not found in PATH"
Движок требует утилиты FFmpeg и FFprobe для транскодирования, микширования и верификации контейнеров.
- **Windows:** Установите через `winget install Gyan.FFmpeg` или скачайте с [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/) и добавьте папку `bin` в системную переменную `PATH`.
- **Linux (Ubuntu/Debian):** `sudo apt-get update && sudo apt-get install -y ffmpeg`
- **macOS:** `brew install ffmpeg`
Проверьте доступность:
```bash
ffmpeg -version
ffprobe -version
```

### 3. 'npx' не найден или npx.cmd
Убедитесь, что Node.js (>= 22.0.0) установлен и добавлен в системный `PATH`. На Windows скрипт `tools/render_clip.py` автоматически разрешает `npx.cmd`. Проверьте вызов в консоли:
```bash
node -v
npx -v
```
