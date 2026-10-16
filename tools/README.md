# 🛠️ Каталог инструментов и служебных скриптов (tools/)

Реестр повторно используемых команд для автоматизации видеомонтажа, транскрибации, саунд-дизайна и проверки качества.

---

## 1. Сводная таблица утилит

| Имя скрипта / команды | Что делает | Пример запуска |
| :--- | :--- | :--- |
| **`ingest.py`** | Аппаратный анализ метаданных видео (HDR/VFR), перевод HDR (HLG/PQ) в SDR Rec.709, CFR 30 fps, генерация 720p прокси и отчёта по экспозиции. | `python tools/ingest.py clients/demo/raw/input.MOV` |
| **`transcribe.bat` / `transcribe.py`** | Транскрибация аудио через faster-whisper с поддержкой словаря спикера (глоссария) и пословными таймкодами. | `tools\transcribe.bat work/ingest/input_sdr_cfr30.mp4 --glossary glossary.txt` |
| **`compact_transcript.py`** | Очистка транскрипта: удаление дублей (оставляет только последний чистый дубль), пауз и слов-паразитов. | `python tools/compact_transcript.py work/input.json` |
| **`beat_table.py`** | Формирование пофразовой таблицы битов (`line`, `visual`, `proof_source`, `camera`, `cut_motivation`, `sfx`, `why`, `approved`) и предупреждение при >2 слайдах текста подряд. | `python tools/beat_table.py work/plan/edit_plan.json` |
| **`plan_contact_sheet.py`** | Рендеринг раскадровки (контактного листа кадров) перед финальным видео на основе битового плана. | `python tools/plan_contact_sheet.py work/plan/edit_plan.json` |
| **`sfx_calibrate.py`** | Измерение пика, RMS и EBU R128 для каждого SFX-файла и расчёт компенсации уровня (`gain_to_reference_db`). | `python tools/sfx_calibrate.py` |
| **`mix.py`** | Сведение звуковой дорожки: позиционирование SFX по относительным уровням к RMS речи, сайдчейн музыки, нормализация до -14 LUFS / -1 dBTP. | `python tools/mix.py work/audio/voice.wav work/plan/edit_plan.json` |
| **`qa.bat` / `qa.py`** | Комплексный аудит видео на 10 fps: проверка пересветов, повторов анимаций, фликкера <0.5с, скорости чтения, закрытия лица, безопасных зон. | `python tools/qa.py out/final.mp4 work/plan/edit_plan.json` |
| **`slice_words_json.py`** | Вырезание фрагмента пословных таймкодов JSON для конкретного диапазона секунд. | `python tools/slice_words_json.py input.json 10.0 25.5` |
| **`auto-editor.bat`** | Удаление участков тишины из видео/аудио через утилиту auto-editor. | `tools\auto-editor.bat input.mp4 --output cut.mp4` |
| **`setup-whisper.bat`** | Идемпотентная установка виртуального окружения `venv-whisper` и PyAV патча. | `tools\setup-whisper.bat` |
| **`verify_fonts.py`** | Проверка поддержки кириллицы (66/66 букв) во всех шрифтах библиотеки `assets/fonts/`. | `python tools/verify_fonts.py` |
| **`verify_subtitles_sync.py`**| Измерение рассинхрона между аудиопотоком и метками субтитров. | `python tools/verify_subtitles_sync.py video.mp4 subs.json` |
| **`generate_pro_sfx_library.py`** | Процедурный синтез библиотеки звуковых эффектов (синус, частотная модуляция, шум). | `python tools/generate_pro_sfx_library.py` |
| **`inventory_and_backup.py`** | Создание архива проекта и аудит окружения. | `python tools/inventory_and_backup.py` |

---

## 2. Папка `tools/_scratch/`
Одноразовые скрипты экспериментов, тестов и старых правок перенесены в `tools/_scratch/` для сохранения истории и освобождения рабочего пространства `tools/`.
