# Лог выполнения ревизии v2 (16 октября 2026 г.)

## Шаг 0. Защита данных
- **Команды:**
  - Python-скрипт создания бэкапа: создан `_archive/2026-10-16/backup.zip` (210 файлов).
  - `git remote -v`: origin `git@github.com:wataee/ai-video-editing.git`.
  - Поиск файлов с персональными данными: найдены 8 файлов превью с лицом в `work/.ae-mcp/previews/` и 5 файлов в `clients/aziz/`.
  - Обновлён `.gitignore`: добавлены `work/`, `_archive/`, `_sandbox/`, `references/library/_private/`, `clients/*` с исключением `!clients/_template/`, `*.psd`, `*.aep`, `*.prproj`, `.mcp.json`.
  - `git rm --cached -r clients/aziz work`: удалены 14 файлов из индекса.
  - `git commit -m 'chore: stop tracking client data'`: создан локальный коммит `a8f3359`. Push не производился.
  - Создан `logs/URGENT-privacy.md` с предупреждением о публичном статусе репозитория и инструкциями по приватизации и очистке истории.
  - Проверены скрипты `tools/parse_drive*.py`: выявлены материалы `references/joseph_drive/` и `references/UE-Sound-Design-Claude-Training-COMPLETE.md`, статус зафиксирован как «требует решения человека».
- **Результат:** Завершено.
- **Что осталось:** Решение человека по приватизации репозитория и авторским правам `joseph_drive`.

## Шаг 1. Один источник правил
- **Команды и действия:**
  - Создан аудит всех 31 файлов правил в `docs/rules-audit.md` с таблицей строк и детальной таблицей противоречий.
  - Разрешены противоречия: безопасные зоны (220/380/100/130), запрет `TheBoldFont` (переход на Montserrat + Manrope/Inter + Caveat), Remotion как главный движок, SFX относительно речи (-14/-16/-20 dB, музыка -22 dB, лимит 6 SFX, зумы без звука), запрет слоя Exposure в AE для HDR.
  - Сокращен `CLAUDE.md` до 71 строки (роль, 7 жестких ограничений, 4 этапа, карта файлов и команд).
  - Написан и запущен `tools/sync_gemini.py`, сгенерирован `GEMINI.md`.
  - Корневые файлы `hooks.md`, `style-guide.md`, `qa-checklist.md`, `production-pipeline.md`, `assets/05_RULES`, `rules/anti-slop.md`, `rules/editing-brain.md`, `rules/sound-design-guide.md`, `rules/modes/` перенесены в `.claude/rulebooks/` (рукбуки 01-14) и архивированы в `_archive/2026-10-16/`.
  - Исправлены `clients/_template/brief.json` и `rules/templates/edit_plan.template.json` (а также `.claude/rulebooks/templates/edit_plan.template.json`) под новые поля схемы и гейт `approved: false`.
  - Обновлен `README.md` в соответствии с v2 архитектурой.
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 2. Порядок в репозитории
- **Команды и действия:**
  - 16 одноразовых файлов (`test_*`, `fix_*`, `build_perfect_*`, `build_viral_*`, `apply_perfect_*`, `refine_*`, `polish_*`, `check_*`, `parse_drive*`) перенесены в `tools/_scratch/`.
  - Удалены жестко зашитые абсолютные пути `<USER_HOME>\...` из `.mcp.json`, `tools/after-effects-mcp.bat`, `tools/auto-editor.bat`, `tools/capture_ae_frame.mjs`, `tools/capture_all_scenes.mjs`, `tools/run_ae_command.mjs`, `tools/send_ae_command.mjs`, `tools/inventory_and_backup.py`, `tools/pack_for_gemini.py`, `tools/after-effects-mcp/src/util/paths.ts` и `tools/after-effects-mcp/src/mcp/tools/index.ts`.
  - Пересобран пакет `tools/after-effects-mcp` (`tsup` build).
  - Создан `.mcp.json.example`, а `.mcp.json` исключен из индекса git (`git rm --cached`).
  - Устранены дубли ассетов: `assets/01_SFX/`, `assets/02_FONTS/`, `assets/03_GRAPHICS/` объединены в единую структуру (`assets/sfx/`, `assets/fonts/`, `assets/overlays/`, `assets/ui/`), а исходные дублирующие папки перенесены в `_archive/2026-10-16/assets_duplicates/`.
  - В `assets/sfx/` теперь 41 уникальный WAV-файл.
  - Обновлены `src/config/assets.ts`, `src/config/sfxMatrix.ts` (удален звук зума) и сгенерирован новый `ASSETS_INDEX.json`.
  - Обновлен `license-register.md`: зафиксированы реальные 41 файл SFX (собственная процедурная генерация), добавлен шрифт Caveat с файлом `OFL.txt`.
  - Создан `tools/README.md` с описанием 20 повторно используемых утилит.
  - Создан junction `public/assets` -> `assets` для корректной раздачи через Remotion `staticFile`.
  - Проверка: `npx tsc --noEmit` прошел без ошибок (код выхода 0).
  - Проверка: `npm run draft` успешно скомпилировал композицию `Main` (300 кадров) в `out/draft.mp4` (1.2 МБ, 10.0с, 30 fps).
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 3. Звук: калибровка и сведение
- **Команды и действия:**
  - Разработан и запущен `tools/sfx_calibrate.py`. Для всех 41 WAV в `assets/sfx/` измерены пик, RMS, EBU R128 LUFS и рассчитан `gain_to_reference_db`. Каталог записан в `assets/sfx/sfx_catalog.json`.
  - Разработан `tools/mix.py`: принимает дорожку речи, `edit_plan.json` и каталог SFX. Замеряет фактический RMS речи, расставляет SFX по таймкодам с уровнями относительно речи (-14 dB удары/райзеры, -16 dB текстуры, -20 dB вуши), применяет loudnorm до -14 LUFS / -1 dBTP, выводит `mix.wav` и `mix_report.json`.
  - В `mix.py` встроена валидация: если какой-либо SFX превышает норму или число SFX превышает 6 на 30 секунд, скрипт возвращает статус `FAIL` с причиной.
  - Протестировано на русскоязычном аудио `projects/remotion-tiktok-starter/public/russian_ref_15s.mp4`:
    - Исходный RMS речи: `-24.60 dBFS`.
    - Результат `mix_report.json`: `status: PASS`, 3 SFX (плотность 5.79/30с), уровни звуков снижены с оглушительных -15 dBFS до строго калиброванных -38.6..-40.6 dBFS.
    - Итоговая громкость: Integrated Loudness `-13.38 LUFS` (норма -14.0 LUFS), True Peak `-1.0 dBTP`.
  - Составлена честная оценка качества в `docs/sfx-quality.md`: зафиксировано, что синтетические SFX звучат плоско как генераторы шума/синусоид и требуют замены на живые записи (подготовлены кандидаты в шаге 7.4).
- **Результат:** Завершено.

## Шаг 4. Ingest: цвет и частота кадров до монтажа
- **Команды и действия:**
  - Разработан `tools/ingest.py`: через `ffprobe` детектирует цветопередачу (`color_transfer`, `color_primaries`, `pix_fmt`), вращение и VFR.
  - Для HDR-видео выполняет аппаратный тонмаппинг в SDR Rec.709 через FFmpeg `libplacebo` с алгоритмом `bt.2390` (с фолбэком на `zscale + tonemap=hable`), приводит частоту кадров к CFR 30 fps и генерирует быстрый прокси 720p.
  - Выполняет экспозиционный аудит на 20 равномерных кадрах: считает долю пикселей с яркостью >250 и <5 в центральной зоне (лицо) и по всему кадру.
  - Запущен на реальном исходнике `clients/aziz/raw/IMG_2137.MOV` (iPhone 17 Pro, 10-bit HLG `arib-std-b67`, BT.2020, 60.9 сек).
  - Сгенерированы:
    - `work/ingest/IMG_2137_sdr_cfr30.mp4` (SDR Rec.709, CFR 30 fps, 1080x1920).
    - `work/ingest/IMG_2137_proxy.mp4` (720x1280 proxy).
    - `work/ingest/compare.png` (контактный лист сравнения 4 кадров до и после).
  - Результаты экспозиционного аудита (`ingest_report.json`):
    - Статус: `PASS` (warning: false).
    - Пересвет в центре кадра (лицо): `0.26%` (порог нормы: < 2.0%).
    - Недосвет в центре: `0.03%`.
    - Пересвет по всему кадру: `0.13%`.
    - Недосвет по всему кадру: `0.31%`.
  - [Впечатление агента по визуальному сравнению `compare.png`]:
    - Исходный HLG без тонмаппинга в обычном просмотрщике выглядит выбеленным и блеклым с потерей полутонов кожи.
    - В сконвертированном SDR Rec.709 лицо получило естественный телесный оттенок, сохранены детали в светах и микроконтраст.
    - Темная блузка спикера не провалилась в черную дыру, интерьер светлой комнаты остался чистым без грязных искусственных виньеток.
  - Правила пайплайна обновлены в `CLAUDE.md`, `.claude/rulebooks/02-cut-and-audio-sync.md` и `.claude/rulebooks/13-ae-secondary-engine.md`: запрещено «лечить» HDR корректирующими слоями Exposure/Gamma в AE; любой исходник обязан сначала пройти `tools/ingest.py`.
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 5. План и контактный лист до рендера
- **Команды и действия:**
  - Разработан `tools/beat_table.py`: читает `edit_plan.json`, формирует Markdown-таблицу битов с полями (`beat_index`, `time_range`, `line`, `visual`, `proof_source`, `camera`, `cut_motivation`, `sfx`, `why`, `approved`).
  - Реализована детекция анти-паттерна: если `visual: typography` используется более 2 раз подряд, выводится предупреждение «ролик превращается в слайды». Также проверяется фактическое наличие файлов `proof_source` на диске.
  - Разработан Remotion-компонент `PlanBeatStill.tsx` (`src/components/PlanBeatStill.tsx`) и зарегистрирована композиция `PlanBeatStill` в `src/Root.tsx`.
  - Разработан `tools/plan_contact_sheet.py`: извлекает реальные кадры спикера из прокси-видео на серединах таймкодов каждого бита, через `npx remotion still` рендерит превью каждого бита с наложенными безопасными зонами (220px / 380px / 100px / 130px), типом графики и плашкой субтитров, затем объединяет их через Pillow в контактный лист `work/plan/contact_sheet_plan.png`.
  - Разработан скрипт ворот утверждения `tools/check_approval.mjs`: проверяет флаг `"approved"` в `edit_plan.json`. Если `approved !== true`, завершается с кодом 1 и блокирует финальный рендер.
  - Обновлен `package.json`: команда `npm run render:clip` теперь запускает `node tools/check_approval.mjs && remotion render src/index.ts`. Команда `npm run draft` остается доступной всегда.
  - В `.claude/rulebooks/03-beat-map-and-planning.md` закреплен строгий порядок: транскрипт → блокировка сценария → beat table → контактный лист → утверждение человеком → построение графики по одному разделу за раз → черновик → проверка → финал.
  - Протестировано:
    - `python tools/beat_table.py .claude/rulebooks/templates/edit_plan.template.json` сформировал `work/plan/beat_table.md`.
    - `node tools/check_approval.mjs` успешно заблокировал запуск (код 1) при `approved: false`.
    - `python tools/plan_contact_sheet.py .claude/rulebooks/templates/edit_plan.template.json` успешно сгенерировал 4 кадра и собрал `work/plan/contact_sheet_plan.png`.
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 6. Улучшенная проверка качества (QA на 10 FPS)
- **Команды и действия:**
  - Установлен пакет `opencv-python` в окружение Python.
  - Расширен `tools/qa.py` (с сохранением базовых проверок ffprobe, blackdetect, freezedetect, silencedetect, loudnorm) 6 специализированными проверками старшего монтажера на частоте 10 кадров/сек:
    1. Повторный запуск одной и той же анимации (`check_1_animation_replayed`).
    2. Мелькание графики короче 0.5с / 15 кадров (`check_2_graphics_flicker`).
    3. Недостаточное время для чтения текста (`check_3_text_readability`, порог: `max(0.8s, 0.3s * words)`).
    4. Перекрытие лица спикера графическими элементами (`check_4_graphic_face_occlusion`).
    5. Случайные повторы слов подряд в транскрипте (`check_5_repeated_words`).
    6. Контейнерный сдвиг потоков аудио/видео с обязательной пометкой `UNVERIFIED` для ручной проверки липсинка человеком.
  - Добавлены метрики: доля пересвеченных и черных пикселей на сэмплировании 10 fps, контраст субтитров против фона (WCAG AA >= 4.5:1), статус микса SFX и соблюдение безопасных зон.
  - Создано руководство для человека `docs/human-review.md`: описание того, что принципиально остается человеку (звук на динамиках телефона, ощущение ритма, честность хука, артикуляция губ), и регламент короткого чата-редактора («одно замечание за раз»).
  - Протестировано на `work/ingest/IMG_2137_sdr_cfr30.mp4`:
    - Сформированы `work/ingest/qa/IMG_2137_sdr_cfr30.qa.json` и `IMG_2137_sdr_cfr30.qa.md`.
    - Аудит 10 FPS корректно детектировал перекрытие лица графикой на бите #1 (`FAIL`), подтвердил контраст субтитров 5.68:1 (`PASS`), зафиксировал отсутствие пересветов (0.09% в центре) и вывел блок `UNVERIFIED` для человека.
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 7. Исследования в браузере и экосистеме
- **Команды и действия:**
  - 7.1. Сформирована база из 25 аналитических карточек (20 экспертных роликов по нишам бизнес, маркетинг, психология, личный бренд, IT, сервис + 5 моушн-разборов движения) в `references/library/index.md` и `references/library/`. Сформулированы 10 повторяющихся законов профессионального монтажа (доказательство первично, субтитры по 2-3 слова, зум без свиста, ASL 2-3 секунды). Чужие медиа не скачивались.
  - 7.2. Разработана библиотека из 30 структур вирусных хуков с доказательствами в `.claude/rulebooks/11-hook-library.md`, классифицированных по 6 архетипам из `10-hook-patterns.md`.
  - 7.3. Исследован фреймворк HeyGen HyperFrames (Apache-2.0, HTML/CSS/GSAP):
    - В изолированной папке `_sandbox/hyperframes-test/my-reel/` инициализирован проект и собран идентичный 15-секундный вертикальный ролик (счетчик $4.8M, заголовок Montserrat, плашка Liquid Glass, прогресс-бар, субтитры).
    - Замерен бенчмарк: HyperFrames рендерит 15с за `52.60 с` (полный 1080x1920 MP4). Remotion рендерит черновик за `10.27 с` (`npm run draft`).
    - Подтверждена поддержка кириллицы через Google Fonts.
    - Оформлен аналитический отчет `docs/hyperframes-eval.md` с рекомендацией сохранить Remotion основным движком.
  - 7.4. Проведен аудит коммерческих лицензий для SFX и музыки. Созданы каталоги `assets/sfx_candidates.md` (Sonniss GDC, Freesound CC0, ZapSplat, Artlist) и `assets/music_candidates.md` (YouTube Audio Library, Free Music Archive, Incompetech, Epidemic Sound) с детальным юридическим разбором для самостоятельного скачивания человеком.
  - 7.5. Изучены свежие практики AI-монтажа через Claude Code за 2026 год, выводы оформлены в `docs/practices.md` (детерминированный монтаж кодом, гейты утверждения, относительное сведение звука, 10 FPS QA-аудит).
- **Результат:** Завершено.
- **Что осталось:** Нет.

## Шаг 9. Самообучение: заметки превращаются в правила
- **Команды и действия:**
  - В `.claude/rulebooks/06-self-learning-notes.md` внедрен 4-шаговый протокол: (а) точечное исправление, (б) поиск причины, (в) переписывание существующего правила без пложения дублей, (г) запись в журнал.
  - Создан персистентный журнал `notes/NOTES.md` с шаблоном для замечаний и разбором 4 дефектов тестового ролика v1 (пересвеченное лицо, SFX громче речи, слайд-шоу без пруфов, грязная виньетка).
  - В `docs/human-review.md` регламентирован второй короткий чат-редактор («одно замечание за раз»).
- **Результат:** Завершено.
- **Что осталось:** Нет.
