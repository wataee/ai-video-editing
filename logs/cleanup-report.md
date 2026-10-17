# 📋 Итоговый отчёт о приведении рабочей станции AI-Video-Editing в порядок

> **Дата составления:** 15 октября 2026 г.  
> **Рабочая станция:** Windows 11 Pro 64-bit (Build 26100), Intel Core i7-12700H, NVIDIA GeForce RTX 3060 Laptop (4 ГБ VRAM), 16 ГБ RAM.  
> **Корневая папка (ROOT):** `<ROOT>`  
> **Цель:** Полное исправление 7 проблем рабочей среды, выявленных внешним ревью, с обеспечением строгой технической достоверности, воспроизводимости и открытости ограничений.

---

## 1. Сводная таблица по 7 выявленным проблемам

| № | Проблема | Что было не так | Что сделано | Доказательство | Статус |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Недостоверный QA и нереалистичные заявления об «идеальности»** | Отсутствовали реальные измерения звука, битрейта, артефактов и рассинхрона; в документации заявлялось об «идеальном монтаже» без фактов. | Создан комплексный автоматический QA-инструмент `tools\qa.py` (`tools\qa.bat`), выполняющий все проверки `qa-checklist.md` (FFprobe, `blackdetect`, `freezedetect`, `silencedetect`, EBU R128 `loudnorm`). Разработан скрипт `tools\verify_subtitles_sync.py` для измерения рассинхрона. В `install-report.md` и `README.md` добавлен честный раздел ограничений. | Отчёт [`clients\_demo\out\qa\test_tiktok_render.qa.md`](clients/_demo/out/qa/test_tiktok_render.qa.md), изображения `safe_zones_overlay.png` и `contact_sheet.png`. Рассинхрон субтитров: медиана 0.0 мс, среднее 2.5 мс. | **ИСПРАВЛЕНО** *(техчасть)* + **ТРЕБУЕТ ЧЕЛОВЕКА** *(субъективная оценка)* |
| **2** | **Несоответствие ассетов и проблемы с лицензиями** | Папки `assets/` были пустыми; шрифт `theboldfont.ttf` в Remotion не поддерживал кириллицу (0/66 букв); `license-register.md` содержал фиктивные записи. | Загружено 7 OFL шрифтов из Google Fonts. Алгоритмически проверено 100% покрытие кириллицы (66/66 глифов). Создан спесимен `specimen.png`. В `remotion-tiktok-starter` шрифт заменён на Montserrat (проверен рендер `test_ru_still.png`). Папки музыки и SFX снабжены регламентами и таблицами прав. `license-register.md` полностью переписан под файлы на диске. | [`docs\fonts-check.md`](docs/fonts-check.md), [`assets\fonts\specimen.png`](assets/fonts/specimen.png), [`license-register.md`](license-register.md), `projects\remotion-tiktok-starter\public\test_ru_still.png`. | **ИСПРАВЛЕНО** |
| **3** | **Дублирование чек-листов (`qa-checklist` vs `quality-checklist`)** | Два файла с дублирующимся содержимым (155 строк) создавали путаницу в источнике правды. | Проведено сравнение через `difflib`. Дубликат `quality-checklist.md` перенесён в `_archive\2026-10-15\`. Заголовок `qa-checklist.md` стандартизирован. Все ссылки в проекте заменены. `Select-String` подтвердил 0 упоминаний дубликата. | [`qa-checklist.md`](qa-checklist.md), архивный дубликат в [`_archive\2026-10-15\quality-checklist.md`](_archive/2026-10-15/quality-checklist.md). | **ИСПРАВЛЕНО** |
| **4** | **Недоступность Remotion skills для Claude Code** | 12 экспертных навыков лежали в `.agents\skills\` и не распознавались Claude Code. Команда `claude` отсутствует в PATH. | Все 12 навыков с проверенным YAML frontmatter скопированы в целевую директорию `.claude\skills\`. Составлен каталог `docs\skills-inventory.md`. В `README.md` добавлено требование запуска Claude строго из корня ROOT. | Директория [`.claude\skills\`](.claude/skills), каталог [`docs\skills-inventory.md`](docs/skills-inventory.md). | **ИСПРАВЛЕНО** *(файлы)* + **ТРЕБУЕТ ЧЕЛОВЕКА** *(установка CLI и авторизация)* |
| **5** | **Хрупкое окружение Whisper и недокументированный патч PyAV** | Заплатка в `faster_whisper/audio.py` была сделана «по месту» без исходного `.patch` файла и lock-файлов; бинарник `auto-editor.exe` не имел верификации хеша. | Сформированы `requirements-whisper.lock.txt`, `requirements-autoeditor.lock.txt`, `requirements-whisper.txt`. Зафиксирован SHA256 хеш `auto-editor.exe`. Создан diff-патч `tools\patches\faster-whisper-audio.patch`. Написан идемпотентный скрипт развёртывания `tools\setup-whisper.bat`. Экспериментально подтверждена необходимость патча для PyAV 14+. | [`tools\patches\faster-whisper-audio.patch`](tools/patches/faster-whisper-audio.patch), [`tools\requirements-whisper.lock.txt`](tools/requirements-whisper.lock.txt), [`docs\auto-editor-binary.md`](docs/auto-editor-binary.md). | **ИСПРАВЛЕНО** |
| **6** | **Неоптимальная работа Whisper (CUDA, модели, глоссарий)** | Отсутствовал бенчмарк моделей; не было поддержки глоссария спикеров/терминов; отсутствовали CUDA DLLs для RTX 3060. | Добавлен поиск CUDA DLLs и мягкий фоллбэк на CPU int8. Реализован флаг `--glossary` в `transcribe.bat` / `transcribe.py`. Кэшированы 5 моделей (`tiny`, `base`, `small`, `medium`, `large-v3-turbo`). Проведён бенчмарк WER и скорости на русской речи. Обоснован выбор моделей: `base` (быстрый дефолт, 10x реалтайма), `small` (для шумной живой речи). | Отчёт бенчмарка [`clients\_demo\work\model-comparison.md`](clients/_demo/work/model-comparison.md), таблица в `README.md`. | **ИСПРАВЛЕНО** |
| **7** | **Хаос в структуре папок и относительных путях** | Разрозненные папки `samples/`, `exports/`; отсутствие стандартизированной клиентской папки; скрипты путались при нестандартных путях. | Создан эталонный шаблон клиента `clients\_template\` (`brand\`, `raw\`, `proxy\`, `work\`, `out\`, `brief.json`, `glossary.txt`, `credits.md`, `revisions.md`). Создан тестовый клиент `clients\_demo\`. Папки `samples/` и `exports/` перенесены и удалены. Скрипты обновлены. В `CLAUDE.md` и `README.md` зафиксирован регламент клиентского пайплайна из 7 шагов. | Папки [`clients\_template\`](clients/_template) и [`clients\_demo\`](clients/_demo). Успешный сквозной прогон пайплайна. | **ИСПРАВЛЕНО** |

---

## 2. Задачи, которые ТРЕБУЮТ УЧАСТИЯ ЧЕЛОВЕКА

Следующие шаги невозможно выполнить программно или они требуют прав администратора / персональных аккаунтов / субъективного восприятия:

### 1. Установка DaVinci Resolve (для цветокоррекции и NLE-монтажа)
- **Причина:** Официальный сайт Blackmagic Design защищён обязательной персональной формой регистрации, а установщик запрашивает права администратора (UAC).
- **Пошаговая инструкция:**
  1. Перейдите по ссылке: [blackmagicdesign.com/products/davinciresolve](https://www.blackmagicdesign.com/products/davinciresolve).
  2. Нажмите **Free Download Now** и выберите бесплатную версию **DaVinci Resolve 19** (левая колонка, Windows).
  3. Заполните поля формы (имя, email, город) и нажмите **Register & Download**.
  4. Распакуйте скачанный архив и запустите `DaVinci_Resolve_19.x_Windows.exe`. Подтвердите запрос контроля учётных записей (UAC).
  5. Руководство по импорту XML-таймлайнов из `auto-editor`: [`docs\davinci-resolve-guide.md`](docs/davinci-resolve-guide.md).

### 2. Установка и авторизация Claude Code CLI
- **Причина:** Утилита `claude` отсутствует в системе. Требуется глобальная установка и OAuth-авторизация в браузере с аккаунтом Anthropic.
- **Пошаговая инструкция:**
  1. Откройте терминал PowerShell и выполните:
     ```powershell
     npm install -g @anthropic-ai/claude-code
     ```
  2. Перейдите строго в корневую папку проекта:
     ```powershell
     cd <ROOT>
     ```
  3. Запустите Claude CLI:
     ```powershell
     claude
     ```
  4. Завершите авторизацию в открывшемся окне браузера. Claude Code автоматически подхватит 12 навыков Remotion из папки `.claude\skills\` и регламент из `CLAUDE.md`.

### 3. Личная проверка готового видео (субъективный QA)
- **Причина:** Алгоритмический QA замеряет громкость и кадры, но не способен оценить восприятие зрителем.
- **Пошаговая инструкция:**
  1. Откройте файл [`clients\_demo\out\test_tiktok_render.mp4`](clients/_demo/out/test_tiktok_render.mp4) на смартфоне.
  2. Оцените читаемость шрифта Montserrat при быстром скролле ленты.
  3. Послушайте звук через динамик телефона на средней и высокой громкости — нет ли хрипов или неразборчивых согласных.
  4. Сверьте расположение субтитров с наложенным оверлеем [`clients\_demo\out\qa\safe_zones_overlay.png`](clients/_demo/out/qa/safe_zones_overlay.png).

### 4. Юридическая проверка сторонних музыкальных треков и SFX
- **Причина:** Коммерческая безопасность требует личной проверки лицензий на музыку.
- **Пошаговая инструкция:**
  1. При добавлении треков в `assets\music` или `assets\sfx` сверяйте условия лицензии (CC-BY, CC0, Royalty-Free).
  2. Вносите данные об авторе и лицензии в `clients\<клиент>\credits.md` в соответствии с памятками [`assets\music\README.md`](assets/music/README.md) и [`assets\sfx\README.md`](assets/sfx/README.md).

---

## 3. Реестр созданных и изменённых файлов

### Созданные файлы и директории:
- `_archive\2026-10-15\backup.zip` — полный исходный бэкап настроек и скриптов (819 КБ).
- `_archive\2026-10-15\quality-checklist.md` — заархивированный дубликат чек-листа.
- `_archive\2026-10-15\load-font.ts.old` — архивный вариант загрузки шрифта `theboldfont.ttf`.
- `clients\_template\` — эталонный шаблон клиента (`brand\`, `raw\`, `proxy\`, `work\`, `out\`, `brief.json`, `glossary.txt`, `credits.md`, `revisions.md`).
- `clients\_demo\` — рабочая директория тестового клиента (`raw\`, `work\`, `out\`, `qa\`).
- `.claude\skills\` — 12 специализированных навыков Remotion с валидным YAML frontmatter.
- `docs\skills-inventory.md` — реестр и описание всех 12 навыков Remotion.
- `docs\auto-editor-binary.md` — документ фиксации бинарника auto-editor с URL и SHA256 хешем.
- `docs\fonts-check.md` — отчёт аудита 100% покрытия кириллицы (66/66 глифов) для 7 семейств шрифтов.
- `assets\fonts\` — 7 гарнитур (Montserrat, Manrope, Onest, Rubik, Oswald, Inter, Unbounded) с лицензиями OFL.
- `assets\fonts\specimen.png` — визуальный образец шрифтов.
- `assets\music\README.md` — регламент лицензионной чистоты и учёта музыки.
- `assets\sfx\README.md` — регламент лицензионной чистоты и учёта звуковых эффектов.
- `tools\requirements-whisper.lock.txt` — полный lock-файл окружения Whisper.
- `tools\requirements-autoeditor.lock.txt` — полный lock-файл окружения auto-editor.
- `tools\requirements-whisper.txt` — явные зависимости faster-whisper.
- `tools\patches\faster-whisper-audio.patch` — унифицированный patch для PyAV 14+.
- `tools\setup-whisper.bat` & `tools\setup_whisper.py` — идемпотентное восстановление окружения.
- `tools\qa.py` & `tools\qa.bat` — инструмент автоматического контроля качества видео и аудио.
- `tools\verify_subtitles_sync.py` — скрипт анализа рассинхрона субтитров.
- `tools\compare-models.bat` & `tools\compare_models.py` — бенчмарк моделей Whisper (WER и скорость).
- `clients\_demo\work\model-comparison.md` — отчёт бенчмарка моделей faster-whisper.
- `clients\_demo\out\qa\` — отчёты QA (`test_tiktok_render.qa.md`, `test_tiktok_render.qa.json`, `safe_zones_overlay.png`, `contact_sheet.png`, `subtitles_sync_report.md`).
- `logs\inventory-before.md` — инвентаризация до начала очистки.
- `logs\cleanup-2026-10-15.md` — пошаговый подробный лог выполнения каждого шага очистки.
- `logs\cleanup-report.md` — этот итоговый сводный отчёт.

### Изменённые файлы:
- `CLAUDE.md` — добавлен регламент клиентских директорий и обновлены ссылки на `qa-checklist.md`.
- `README.md` — добавлены инструкции по клиентскому пайплайну, QA-инструменту, бенчмарку моделей Whisper, патчам и лицензиям.
- `qa-checklist.md` — стандартизирован заголовок, удалены следы дублирования.
- `license-register.md` — актуализирован под реальные файлы, очищен от фиктивных деклараций.
- `install-report.md` — исправлены устаревшие пути, добавлены результаты бенчмарка и QA, сформирован раздел ограничений тестов.
- `tools\transcribe.py` & `tools\transcribe.bat` — поддержка `--glossary`, вывод в `work\`, динамический поиск CUDA DLLs и фоллбэк на CPU int8.
- `tools\auto-editor.bat` — интеллектуальный вывод в `out\`.
- `projects\remotion-tiktok-starter\src\load-font.ts` — замена шрифта `theboldfont.ttf` на кириллический Montserrat.

---

## 4. Состояние папки `_archive`

Все перемещённые файлы сохранены в директории `ROOT\_archive\2026-10-15\`. Безвозвратное удаление файлов не производилось.

1. `_archive\2026-10-15\backup.zip` (819 017 байт):
   - **Зачем создано:** Полная страховочная копия всех конфигураций, скриптов, markdown-документов и исходников Remotion до внесения правок.
2. `_archive\2026-10-15\quality-checklist.md` (13 253 байта):
   - **Зачем перемещено:** Файл являлся точной копией `qa-checklist.md` (за исключением первой строки заголовка) и создавал неоднозначность источников правил.
3. `_archive\2026-10-15\load-font.ts.old` (495 байт):
   - **Зачем перемещено:** Исходный файл конфигурации шрифтов стартера TikTok, подключавший `theboldfont.ttf` без кириллицы. Сохранён для истории на случай отката.

---

## 5. Заключение

Рабочая станция полностью упорядочена, независима от облачных подписок, снабжена строгими алгоритмическими средствами контроля качества и готова к производству контента.
