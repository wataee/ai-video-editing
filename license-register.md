# ⚖️ Реестр лицензий компонентов рабочей среды (License Register)

> **Дата актуализации:** 17 октября 2026 г.  
> **Статус проверки:** Проверено по фактическим файлам лицензий (`LICENSE`, `OFL.txt`, коду генераторов и метаданным пакетов) непосредственно на локальном диске.  
> Реестр описывает **только те компоненты, которые фактически присутствуют на диске**.

---

## 1. Сводная таблица лицензий

| Компонент / Пакет / Файл | Источник (URL / путь) | Лицензия | Дата проверки | Кто проверил | Примечание и обязательства |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **FFmpeg & FFprobe (9.0.2)** | [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/) | **GNU GPL v3.0** | 2026-10-15 | Агент | Сборка `full_build`. Выходные видеофайлы, созданные через FFmpeg, лицензией GPL не обременяются. |
| **Remotion (Core & CLI 4.0.535)** | [remotion.pro/license](https://www.remotion.pro/license) | **Custom Remotion License** | 2026-10-15 | Агент | Бесплатно для физических лиц, некоммерческих проектов и компаний до 3 сотрудников включительно. |
| **@remotion/\* (captions, media-utils, animation-utils)** | npm / remotion-dev | **Remotion License** | 2026-10-15 | Агент | Входит в единую лицензионную модель Remotion. |
| **Шаблоны React Video Editor (81 шт.)** | [github.com/reactvideoeditor/remotion-templates](https://github.com/reactvideoeditor/remotion-templates) | **MIT License** | 2026-10-15 | Агент | Разрешено коммерческое и личное использование. |
| **Навыки Remotion (.claude/skills)** | [github.com/remotion-dev/skills](https://github.com/remotion-dev/skills) | **MIT License** | 2026-10-15 | Агент | Экспертные инструкции для AI-агентов. Свободное использование. |
| **faster-whisper (1.2.1)** | [github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | **MIT License** | 2026-10-15 | Агент | Разрешено любое коммерческое использование. |
| **CTranslate2 (4.8.3)** | [github.com/OpenNMT/CTranslate2](https://github.com/OpenNMT/CTranslate2) | **MIT License** | 2026-10-15 | Агент | Разрешено любое коммерческое использование. |
| **auto-editor (29.3.1)** | [github.com/WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | **Unlicense (Public Domain)** | 2026-10-15 | Агент | Общественное достояние. Никаких юридических ограничений. |
| **Модели Whisper (tiny, base, small, medium, large-v3-turbo)** | Hugging Face Hub / OpenAI | **Apache 2.0 / MIT** | 2026-10-15 | Агент | Веса моделей открыты для коммерческого использования. |
| **Шрифт Montserrat** (`assets/fonts/Montserrat/`) | [google/fonts/ofl/montserrat](https://github.com/google/fonts/tree/main/ofl/montserrat) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено внедрение в любые коммерческие видео и проекты. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Manrope** (`assets/fonts/Manrope/`) | [google/fonts/ofl/manrope](https://github.com/google/fonts/tree/main/ofl/manrope) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Onest** (`assets/fonts/Onest/`) | [google/fonts/ofl/onest](https://github.com/google/fonts/tree/main/ofl/onest) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Rubik** (`assets/fonts/Rubik/`) | [google/fonts/ofl/rubik](https://github.com/google/fonts/tree/main/ofl/rubik) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Oswald** (`assets/fonts/Oswald/`) | [google/fonts/ofl/oswald](https://github.com/google/fonts/tree/main/ofl/oswald) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Inter** (`assets/fonts/Inter/`) | [google/fonts/ofl/inter](https://github.com/google/fonts/tree/main/ofl/inter) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Unbounded** (`assets/fonts/Unbounded/`) | [google/fonts/ofl/unbounded](https://github.com/google/fonts/tree/main/ofl/unbounded) | **SIL OFL 1.1** | 2026-10-15 | Агент | Разрешено коммерческое использование. Файл `OFL.txt` сохранён в папке. |
| **Шрифт Caveat** (`assets/fonts/Caveat/`) | [google/fonts/ofl/caveat](https://github.com/google/fonts/tree/main/ofl/caveat) | **SIL OFL 1.1** | 2026-10-16 | Агент | Разрешено свободное коммерческое использование. Файл `OFL.txt` сохранён в папке `assets/fonts/Caveat/`. |
| **Библиотека звуковых эффектов (41 WAV)** (`assets/sfx/`) | Процедурная генерация через `tools/generate_pro_sfx_library.py` | **Собственная генерация (Лицензия автора репозитория / CC0)** | 2026-10-16 | Агент | Файлы синтезированы локально математическими методами. Неограниченное коммерческое использование. |
| **Фоновая музыка (5 треков MP3, 48 kHz stereo)** (`assets/music/`) | OpenGameArt.org (авторы: cinameng, bosslevelaudio, Fupi, TAD, isaiah658) | **CC0 1.0 Universal (Public Domain)** | 2026-10-17 | Агент | 100% CC0 Public Domain. Разрешено коммерческое использование без обязательной атрибуции и роялти. |
| **Текстуры бумаги (3 PNG, 1080x1920)** (`assets/overlays/paper_textures/`) | Процедурная генерация (`tools/generate_paper_textures.py`) | **Собственная генерация / CC0** | 2026-10-17 | Агент | Синтез шума, волокон и микроструктуры бумаги. Разрешено любое коммерческое использование. |
| **Световые оверлеи Light Leaks (3 MP4, 1080x1920 30fps)** (`assets/overlays/light_leaks/`) | Процедурный рендеринг FFmpeg (`tools/generate_light_leaks.py`) | **Собственная генерация / CC0** | 2026-10-17 | Агент | Мягкие кинематографичные градиенты боке и бликов под режим наложения Screen/Add. CC0. |
| **Набор векторных UI-иконок (10 SVG)** (`assets/ui/icons/`) | Lucide / Feather icon specification (`tools/generate_icons.py`) | **MIT License / CC0** | 2026-10-17 | Агент | Чистая векторная графика (`check`, `cross`, `warning`, `fire`, `dollar`, `clock`, `chart`, `lock`, `bolt`, `eye`). |

---

## 2. Перечень фактических файлов музыки (`assets/music/`, 5 файлов)

Все 5 треков приведены к стандарту студийного монтажа: 48 000 Гц, стерео, 192 kbps MP3:

1. `tech_minimal.mp3` — трек «Poilo», автор cinameng ([opengameart.org/content/poilo](https://opengameart.org/content/poilo)), лицензия CC0 1.0 Universal.
2. `dark_cinematic.mp3` — трек «Evil Awaits», автор bosslevelaudio ([opengameart.org/content/evil-awaits](https://opengameart.org/content/evil-awaits)), лицензия CC0 1.0 Universal.
3. `energetic_beat.mp3` — трек «OMW to beat the big bad», автор Fupi ([opengameart.org/content/omw-to-beat-the-big-bad](https://opengameart.org/content/omw-to-beat-the-big-bad)), лицензия CC0 1.0 Universal.
4. `lofi_background.mp3` — трек «Bartender (lofi compilation)», автор TAD ([opengameart.org/content/lofi-compilation](https://opengameart.org/content/lofi-compilation)), лицензия CC0 1.0 Universal.
5. `dark_investigation.mp3` — трек «Unsolved Investigation», автор isaiah658 ([opengameart.org/content/unsolved-investigation](https://opengameart.org/content/unsolved-investigation)), лицензия CC0 1.0 Universal.

---

## 3. Перечень фактических файлов SFX (`assets/sfx/`, 41 файл)

Все 41 файл сгенерированы локально скриптом `tools/generate_pro_sfx_library.py` (частота дискретизации 48 000 Гц, 16 бит, стерео/моно PCM WAV):

1. **Whooshes (9 файлов):**
   - `whooshes/deep_voice_whoosh_01.wav`
   - `whooshes/deep_voice_whoosh_02.wav`
   - `whooshes/deep_voice_whoosh_03.wav`
   - `whooshes/hollow_whoosh_01.wav`
   - `whooshes/hollow_whoosh_02.wav`
   - `whooshes/synthetic_transition_whoosh.wav`
   - `whooshes/transition_spacey_whoosh.wav`
   - `whooshes/whoosh_clean_fast.wav`
   - `whooshes/whoosh_subtle_air.wav`
2. **Clicks & UI (6 файлов):**
   - `clicks/click_01.wav`
   - `clicks/click_02.wav`
   - `clicks/mechanical_button.wav`
   - `clicks/mouse_click_soft.wav`
   - `clicks/select_01.wav`
   - `clicks/switch_01.wav`
3. **Pops (5 файлов):**
   - `pops/glass_pop.wav`
   - `pops/pop_01.wav`
   - `pops/pop_02.wav`
   - `pops/pop_bubble_high.wav`
   - `pops/pop_cartoon_clean.wav`
4. **Hits & Impacts (3 файла):**
   - `hits/bass_drop_hit_01.wav`
   - `hits/cinematic_boom_01.wav`
   - `hits/sub_bass_thud.wav`
5. **Risers & Suck-backs (8 файлов):**
   - `risers/metallic_riser_01.wav`
   - `risers/metallic_riser_02.wav`
   - `risers/riser_subtle.wav`
   - `risers/sharp_bass_riser_01.wav`
   - `risers/sharp_bass_riser_02.wav`
   - `risers/sharp_bass_riser_fast.wav`
   - `risers/suck_back_riser_01.wav`
   - `risers/suck_back_riser_fast.wav`
6. **Textures & Mechanisms (5 файлов):**
   - `textures/camera_click_fast.wav`
   - `textures/complex_mechanism_gizmo.wav`
   - `textures/scratch_01.wav`
   - `textures/scratch_02.wav`
   - `textures/tiny_gearwheel_loop.wav`
7. **Glitches & Sci-Fi (4 файла):**
   - `glitches/activate_energy_hit.wav`
   - `glitches/glitch_01.wav`
   - `glitches/glitch_02.wav`
   - `glitches/sci_fi_impact_reveal.wav`
8. **Ambience (1 файл):**
   - `ambience/tech_drone_subtle.wav`
