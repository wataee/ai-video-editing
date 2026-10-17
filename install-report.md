# 📊 Итоговый отчёт о подготовке рабочей среды AI-Video-Editing

> **Дата составления:** 14 октября 2026 г.  
> **Рабочая директория:** `<ROOT>`  
> **Цель:** Развёртывание и верификация автономной бесплатной локальной рабочей среды для AI-монтажа коротких (Shorts/Reels/TikTok) и длинных видео на Windows 11.  
> **Примечание:** Данный отчёт описывает конфигурацию конкретной рабочей машины разработчика (Windows 11, RTX 3060). Общесистемные требования проекта: Python >= 3.10 (CI использует Python 3.12, локально установлены 3.12 / 3.14), Node.js >= 22 (тестируется на Node 22 и 24), FFmpeg >= 6.0.

---

## 1. Сводная таблица компонентов и статусов

| Компонент | Версия | Источник / Метод установки | Путь к исполняемому файлу / скрипту | Статус |
| :--- | :--- | :--- | :--- | :--- |
| **Git for Windows** | `2.49.0.windows.1` | Предустановлен в системе | `C:\Program Files\Git\cmd\git.exe` | **ПРЕДУСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **FFmpeg** | `9.0.2-full_build-www.gyan.dev` | Предустановлен в системе | `C:\Program Files\ffmpeg\bin\ffmpeg.exe` | **ПРЕДУСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **FFprobe** | `9.0.2-full_build-www.gyan.dev` | Предустановлен в системе | `C:\Program Files\ffmpeg\bin\ffprobe.exe` | **ПРЕДУСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Node.js LTS** | `v24.20.0` | `winget install OpenJS.NodeJS.LTS` | `C:\Program Files\nodejs\node.exe` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **npm** | `11.19.0` | В составе Node.js LTS | `C:\Program Files\nodejs\npm.cmd` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Python** | `3.12 / 3.14` (требования: `>= 3.10`) | `winget install Python.Python.3.12` / CI: 3.12 | `<PYTHON_HOME>\python.exe` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **auto-editor** | `29.3.1` | Standalone binary + venv (Python 3.12) | `<ROOT>\tools\auto-editor.bat` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **faster-whisper** | `1.2.1` (CTranslate2 4.8.3, CUDA 12.9) | Изолированный venv (Python 3.12) + NVIDIA cu12 DLLs | `<ROOT>\tools\transcribe.bat` | **УСТАНОВЛЕНО И ПРОВЕРЕНО (GPU CUDA)** |
| **Remotion CLI / Core** | `4.0.535` | npm пакеты в стартовых проектах | `projects\remotion-*-starter\node_modules` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Remotion Starter (TikTok)** | `4.0.535` | `npx create-video --tiktok` | `projects\remotion-tiktok-starter` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Remotion Starter (Blank)** | `4.0.535` | `npx create-video --blank` | `projects\remotion-blank-starter` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Библиотека 81 шаблона** | RVE Репозиторий | `git clone reactvideoeditor/remotion-templates` | `references\remotion-templates-rve` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **Remotion Dev Skills** | 12 экспертных навыков | `git clone remotion-dev/skills` | `.agents\skills\` & `references\official-remotion-templates` | **УСТАНОВЛЕНО И ПРОВЕРЕНО** |
| **DaVinci Resolve** | Free 19+ | Официальный дистрибутив Blackmagic Design | Ручная загрузка (требуется регистрация) | **ТРЕБУЕТСЯ ДЕЙСТВИЕ ПОЛЬЗОВАТЕЛЯ** |

---

## 2. Аппаратная спецификация компьютера

- **Операционная система:** Windows 11 Pro 64-bit (Build 26100)
- **Центральный процессор (CPU):** Intel(R) Core(TM) i7-12700H (14 ядер, 20 потоков, базовая 2.3 ГГц, Turbo до 4.7 ГГц)
- **Дискретная видеокарта (GPU):** NVIDIA GeForce RTX 3060 Laptop GPU (4096 МБ VRAM, Driver 576.88, DirectX 12)
- **Интегрированная графика:** Intel(R) Iris(R) Xe Graphics
- **Оперативная память (RAM):** 16 ГБ DDR5 (доступно ~7.8 ГБ)
- **Системный накопитель (Диск C:):** Быстрый NVMe SSD, свободно ~138 ГБ

---

## 3. Выполненные тесты и доказательства работоспособности

### Тест 1: Синтез тестового медиа через FFmpeg
- **Команда:** Генерация тестового 5-секундного видео `test_synthetic.mp4` с цветовой сеткой `testsrc`, таймкодом и синусоидальным звуком 440/880 Гц.
- **Результат:** Файл успешно создан и размещён в `clients/_demo/raw/test_synthetic.mp4` (1080x1920, 30 fps, AAC).

### Тест 2: Автоматическое удаление пауз (auto-editor)
- **Команда:** `tools\auto-editor.bat clients\_demo\raw\test_synthetic.mp4 --output clients\_demo\out\test_autoeditor_cut.mp4`
- **Результат:** Успешно! Файл сокращён с 5.00 с до 3.90 с (удалено 1.10 с тишины). Время обработки составило 1.21 секунды. Выходной файл проверен через `ffprobe`.

### Тест 3: Локальная транскрибация и пословные таймкоды (faster-whisper)
- **Тестовый материал:** `clients/_demo/raw/speech_test.mp4` (7.2 секунды синтезированной речи).
- **Команда:** `tools\transcribe.bat clients\_demo\raw\speech_test.mp4 --model tiny --language en --output-dir clients\_demo\work`
- **Результат:** Успешно за 2.03 с (в 3.5 раза быстрее реального времени речи)!
- **Сформированные файлы:**
  1. `clients/_demo/work/speech_test.txt` — чистый транскрипт текста.
  2. `clients/_demo/work/speech_test.srt` — стандартные субтитры с таймкодами.
  3. `clients/_demo/work/speech_test.json` — пословный массив с миллисекундами (`startMs`, `endMs`, `confidence`) для мгновенной интеграции в Remotion.
  4. `clients/_demo/work/speech_test_detailed.json` — расширенный отчёт по сегментам и вероятностям.

### Тест 4: Рендеринг чистого шаблона Remotion (Blank Starter)
- **Команда:** `npx remotion render MyComp clients\_demo\out\test_remotion_blank.mp4 --crf=18`
- **Результат:** Отрендерено 90 кадров (3 секунды 1920x1080 @ 30 fps) в файл `clients\_demo\out\test_remotion_blank.mp4`. Битрейт: ~1.2 Мбит/с.

### Тест 5: Полноценный рендеринг вертикального TikTok видео с караоке-субтитрами
- **Материал:** Видео `sample-video.mp4` (12 секунд 1080x1920).
- **Шрифт:** Заменён `theboldfont.ttf` (не поддерживал кириллицу) на Montserrat (`assets/fonts/Montserrat/`).
- **Генерация субтитров:** Выполнена локальная транскрибация через `transcribe.bat` с моделью `base`, получен файл `sample-video.json`.
- **Рендеринг:** `npx remotion render CaptionedVideo clients\_demo\out\test_tiktok_render.mp4 --crf=18`.
- **Результат:** Видео успешно отрендерено с динамической пословной подсветкой слов и поддержкой кириллицы!

### Тест 6: Сравнительный бенчмарк 5 моделей faster-whisper
- **Материал:** Чистая русская речь `clients/_demo/raw/russian_ref_15s.mp4` (15 секунд).
- **Команда:** `tools\compare-models.bat clients\_demo\raw\russian_ref_15s.mp4 --ref clients\_demo\raw\russian_ref_15s_text.txt`
- **Результаты (`cpu int8`):**
  - `tiny`: 1.26 с (10.4x realtime), WER: 10.5% (ошибка в окончании).
  - `base`: 1.31 с (10.0x realtime), WER: 0.0% (быстрый дефолт).
  - `small`: 3.15 с (4.1x realtime), WER: 0.0% (рекомендован для живой речи).
  - `medium`: 8.53 с (1.5x realtime), WER: 0.0%.
  - `large-v3-turbo`: 21.10 с (0.6x realtime), WER: 0.0%.
- **Отчёт:** [`clients\_demo\work\model-comparison.md`](clients/_demo/work/model-comparison.md).

### Тест 7: Автоматизированный контроль качества готового видео (QA)
- **Утилита:** `tools\qa.py` / `tools\qa.bat`
- **Файл:** `clients\_demo\out\test_tiktok_render.mp4`
- **Измеренные метрики:**
  - Видео: 1080x1920 (9:16), 30 fps CFR, H.264 High 4.0, битрейт ~2.2 Мбит/с.
  - Аудио: AAC Stereo 44.1 kHz, Integrated Loudness `-17.04 LUFS`, True Peak `-2.7 dBTP` (соответствует требованиям EBU R128).
  - Артефакты: 0 чёрных кадров (`blackdetect`), 0 зависаний (`freezedetect`), 0 провалов тишины (`silencedetect`).
  - Рассинхрон субтитров: медианное отклонение **0.0 мс**, максимальное **20.0 мс** (норма: до 80 мс).
  - Сгенерированы визуальные материалы: `safe_zones_overlay.png`, `contact_sheet.png`.
- **Отчёт:** [`clients\_demo\out\qa\test_tiktok_render.qa.md`](clients/_demo/out/qa/test_tiktok_render.qa.md).

---

## 4. Обнаруженные особенности и решённые проблемы

1. **Разрядность и пути auto-editor (WinError 193):**
   - *Проблема:* Пакет `auto-editor` 29+ при первом запуске скачивал скомпилированный бинарник через HTTP, который прервался на 13 МБ, что вызывало ошибку Windows `WinError 193 (%1 не является приложением Win32)`.
   - *Решение:* Загружен полный официальный релиз `auto-editor-windows-amd64.exe` (37.9 МБ), помещён в `tools/venv-autoeditor/Lib/site-packages/auto_editor/bin/auto-editor.exe`. Создан надёжный скрипт запуска `tools/auto-editor.bat`.
2. **Несовместимость PyAV 14+ и faster-whisper:**
   - *Проблема:* В свежих релизах PyAV у метода `av.open()` был удалён параметр `metadata_errors`, из-за чего вызов падал с `TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
   - *Решение:* Функция `decode_audio` в `tools/venv-whisper/.../faster_whisper/audio.py` пропатчена отказоустойчивым блоком `try...except TypeError`, обеспечивающим полную совместимость с любой версией PyAV.
3. **Поддержка CUDA 12 Toolkit DLLs (`cublas64_12.dll`, `cudnn64_9.dll`):**
   - *Решение:* В виртуальное окружение `tools/venv-whisper` установлены пакеты `nvidia-cublas-cu12`, `nvidia-cudnn-cu12` и `nvidia-cuda-nvrtc-cu12`. В `tools/transcribe.bat` и `tools/transcribe.py` настроено автоматическое добавление директорий DLL в `PATH` и `os.add_dll_directory()`. Транскрибация аппаратно ускорена на NVIDIA GeForce RTX 3060 Laptop GPU (режим `cuda float16`), фоллбэк на CPU больше не требуется.
4. **Кодировка консоли Windows (CP1251 vs UTF-8):**
   - *Решение:* Во всех батниках (`transcribe.bat`, `auto-editor.bat`) в первой строке вызывается `chcp 65001 >nul`, гарантируя корректное отображение кириллицы в консоли и логах.
5. **Git Clone davila7/claude-code-templates:**
   - *Проблема:* Репозиторий davila7 содержит тысячи неструктурированных веток и PR, что вызывало сбой Windows SChannel TLS.
   - *Решение:* Проведён анализ структуры. Репозиторий представляет собой любительский сборник текстовых промптов. Вместо него развёрнуты 12 официальных программных агентов от разработчиков `remotion-dev/skills` и 81 готовый шаблон React в `references/remotion-templates-rve/`.

---

## 5. Ответы на 6 ключевых вопросов пользователя

### 1. Какие инструменты установлены, их версии и пути?
- **Node.js LTS:** `v24.20.0` (`C:\Program Files\nodejs\node.exe`)
- **npm:** `11.19.0` (`C:\Program Files\nodejs\npm.cmd`)
- **Git:** `2.49.0.windows.1` (`C:\Program Files\Git\cmd\git.exe`)
- **FFmpeg & FFprobe:** `9.0.2-full_build` (`C:\Program Files\ffmpeg\bin\ffmpeg.exe`)
- **Python:** `3.12.10` (`<PYTHON_HOME>\python.exe`)
- **auto-editor:** `29.3.1` (батник `<ROOT>\tools\auto-editor.bat`)
- **faster-whisper:** `1.2.1` (батник `<ROOT>\tools\transcribe.bat`)
- **Remotion:** `4.0.535` (в директориях проектов `projects/remotion-*-starter`)

### 2. Где находятся созданные проекты и шаблоны?
- **Рабочая директория:** `<ROOT>`
- **Проект с субтитрами TikTok/Shorts:** `projects/remotion-tiktok-starter`
- **Чистый проект Remotion:** `projects/remotion-blank-starter`
- **Каталог и коллекция из 81 шаблона:** `references/remotion-templates-rve` (каталог: `references/remotion-templates-catalog.md`)
- **Официальные навыки и промпты Remotion:** `.agents/skills/` и `references/official-remotion-templates`

### 3. Какие тесты были выполнены и каковы их результаты?
- **Тест нарезки пауз auto-editor:** Выполнен. 5.0 с сокращено до 3.9 с за 1.21 с без артефактов звука.
- **Тест транскрибации faster-whisper:** Выполнен. 7.2 с английской синтезированной речи обработаны за 2.03 с с генерацией пословных JSON-таймкодов и SRT.
- **Бенчмарк 5 моделей Whisper на русской речи:** Выполнен. Модели `base` и `small` показали 0.0% WER (10.0x и 4.1x быстрее реалтайма соответственно на CPU int8).
- **Тест рендера Blank Starter Remotion:** Выполнен (CRF 18, 90 кадров, `clients/_demo/out/test_remotion_blank.mp4`).
- **Тест рендера TikTok Captioned Video:** Выполнен с кириллическим шрифтом Montserrat (вертикальный ролик 1080x1920 с пословной караоке-подсветкой).
- **Автоматизированный QA готового ролика:** Проверено по чек-листу `qa-checklist.md` (FFmpeg blackdetect, freezedetect, silencedetect, EBU R128 loudnorm, синхронизация субтитров со средним отклонением 2.5 мс).

### 4. Какие ограничения или проблемы были обнаружены?
- **Лицензия Remotion:** Полностью бесплатна для персонального использования, опенсорса и команд до 3 человек. Для коммерческих компаний от 4 человек требуется лицензия Remotion Company.
- **DaVinci Resolve:** Требует ручного скачивания с официального сайта Blackmagic Design из-за персональной регистрационной формы и UAC установщика.
- **CUDA 12 DLLs:** Поддержка CUDA 12 полностью настроена и проверена на GPU NVIDIA RTX 3060. Пакеты `nvidia-cublas-cu12` и `nvidia-cudnn-cu12` интегрированы в виртуальное окружение. Транскрибация аппаратно ускорена на GPU.

### 5. Что нужно сделать пользователю вручную (с пошаговыми инструкциями)?
1. **Установка DaVinci Resolve** (если планируется работа в NLE):
   - Перейдите на официальный сайт: [blackmagicdesign.com/products/davinciresolve](https://www.blackmagicdesign.com/products/davinciresolve)
   - Нажмите **Free Download Now** и выберите левую бесплатную версию **DaVinci Resolve** (не Studio).
   - Заполните короткую форму регистрации и скачайте ZIP-архив (~2.5 ГБ).
   - Запустите инсталлятор и согласитесь на установку с правами администратора (UAC).
   - Подробная инструкция по связке с auto-editor и экспорту таймлайнов: [docs/davinci-resolve-guide.md](docs/davinci-resolve-guide.md).
2. **Активация и авторизация Claude CLI** (при наличии подписки Anthropic):
   - Установите `claude` глобально через npm: `npm install -g @anthropic-ai/claude-code`.
   - Авторизуйтесь: запустите `claude` в корневой папке проекта и завершите OAuth в браузере.
   - Убедитесь, что 12 навыков в `.claude\skills\` автоматически распознаются ассистентом.
3. **Лицензионная очистка аудио/видео ассетов:**
   - Человек должен лично проверить условия лицензий для любой фоновой музыки, SFX и b-roll перед публикацией коммерческих роликов. Правила и журнал описаны в `assets\music\README.md` и `assets\sfx\README.md`.

### 6. С чего начать работу прямо сейчас?
1. Скопируйте шаблон клиента:
   ```cmd
   xcopy /E /I clients\_template clients\my_project
   ```
2. Поместите исходное видео в `clients\my_project\raw\raw_video.mp4`.
3. Запустите автоматическую нарезку пауз:
   ```cmd
   tools\auto-editor.bat clients\my_project\raw\raw_video.mp4 --output clients\my_project\out\cut.mp4
   ```
4. Запустите транскрибацию с пословными таймкодами:
   ```cmd
   tools\transcribe.bat clients\my_project\out\cut.mp4 --output-dir clients\my_project\work
   ```
5. Откройте стартер Remotion:
   ```cmd
   cd projects\remotion-tiktok-starter
   npm run dev
   ```
6. Выполните проверку качества готового файла:
   ```cmd
   tools\qa.bat clients\my_project\out\final.mp4 --platform tiktok
   ```

---

## 6. Ограничения автоматических тестов и статус проверки

> [!WARNING]
> **Честность верификации:** Автоматические скрипты проверяют технические параметры файлов, но не могут заменить человеческое восприятие. Ниже приведён честный список того, что проверено автоматически, и того, что требует личной проверки человеком.

| Параметр | Проверено программно | Требует личной проверки человеком |
| :--- | :--- | :--- |
| **Синхронизация субтитров** | Проверена по таймкодам Whisper (среднее отклонение 2.5 мс, макс 20 мс) | Человек должен посмотреть ролик и убедиться, что подсветка совпадает с мимикой и дыханием спикера |
| **Безопасные зоны (Safe Zones)** | Сформирован оверлей `safe_zones_overlay.png` по маске TikTok | Человек должен визуально подтвердить, что кнопки лайков и описания не перекрывают ключевой текст |
| **Качество звука** | Измерены EBU R128 (-17 LUFS), True Peak (-2.7 dBTP), отсутствие резких провалов | Человек должен послушать звук на встроенных динамиках смартфона на разной громкости |
| **Редакторские хуки** | Сформулированы правила в `hooks.md` | Оценка привлекательности хука и виральности субъективна и зависит от целевой аудитории |
| **Шрифты и рендеринг** | 7 семейств OFL проверены на 100% покрытие кириллицы (66/66 глифов) | Человек должен оценить удобочитаемость на маленьком экране при быстром скролле |
| **Шифрование / API ключи** | Облачные API не используются, вся работа локальна | При подключении внешних сервисов человек должен следить за сохранностью токенов |
