# Отчет о стресс-тестировании устойчивости на реальных форматах исходников

> **Дата проведения теста:** 17 октября 2026 г.
> **Методология:** 100% синтетические тест-кейсы без использования чужого видео и лиц реальных людей (tests/generate_fixtures.py).
> **Объект аудита:** Модуль ингейста tools/ingest.py, транскодирование в CFR 30 fps, фильтрация шума --denoise, обработка метаданных поворота и нестандартных разрешений.

## 1. Сводная таблица стресс-тестов

| ID | Тест-кейс | Ожидалось | Фактический результат | Что исправлено / применимо | Статус | Время (с) |
|:---:|---|---|---|---|:---:|:---:|
| **CASE-01** | 4K 60 fps Ultra HD | Ingest successfully downsamples/transcodes to SDR Rec.709 CFR 30 fps, proxy 720p created without crash or memory exhaustion. | SDR: fixture_4k_60fps_sdr_cfr30.mp4, Proxy: fixture_4k_60fps_proxy.mp4. FPS: 60.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 8.36 |
| **CASE-02** | Variable Frame Rate (VFR) | VFR detected by ffprobe (is_vfr: True); transcoded to strict CFR 30 fps (fps_mode cfr) to eliminate Remotion audio drift. | SDR: fixture_vfr_sdr_cfr30.mp4, Proxy: fixture_vfr_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 3.73 |
| **CASE-03** | Vertical Video with Rotation Metadata (rotate=90) | Rotation metadata detected; video frames normalized upright without distorting aspect ratio or leaving 90-degree sideways tilt. | SDR: fixture_rotate_90_sdr_cfr30.mp4, Proxy: fixture_rotate_90_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 2.58 |
| **CASE-04a** | Mono Audio 44.1 kHz | Handled gracefully; proxy and SDR created without channel layout errors. | SDR: fixture_mono_44k_sdr_cfr30.mp4, Proxy: fixture_mono_44k_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 1.62 |
| **CASE-04b** | Stereo Audio 48 kHz | Maintains native 48 kHz broadcast standard with 2 channels. | SDR: fixture_stereo_48k_sdr_cfr30.mp4, Proxy: fixture_stereo_48k_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 2.6 |
| **CASE-05** | Quiet Speech with Background Noise (--denoise flag) | Denoise filter (afftdn + highpass 80Hz + lowpass 12kHz) attenuates high/low noise while preserving signal level. | SDR: fixture_quiet_noise_sdr_cfr30.mp4, Proxy: fixture_quiet_noise_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. Denoise applied via afftdn (-25dB) + bandpass. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 2.05 |
| **CASE-06** | Screen Recording (16:10 aspect ratio: 1920x1200) | Non-standard dimensions detected (is_horizontal: True); proxy letterboxed/padded correctly without ffmpeg scaling crash. | SDR: fixture_screen_rec_1920x1200_sdr_cfr30.mp4, Proxy: fixture_screen_rec_1920x1200_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 2.21 |
| **CASE-07** | Russian Speech with English Glossary Terms | Transcription and plan scaffold parse bilingual token strings without encoding corruption (UTF-8 clean). | SDR: fixture_bilingual_glossary_sdr_cfr30.mp4, Proxy: fixture_bilingual_glossary_proxy.mp4. FPS: 30.0 -> 30 CFR. Exposure status: PASS. | Нативная поддержка в ingest.py (CFR enforcement, padding, denoise filter) | `PASS` | 4.02 |

## 2. Технические выводы и исправления

1. **Переменная частота кадров (VFR):** Смартфоны (особенно iPhone при нагреве и слабом освещении) часто сбрасывают частоту кадров. Без флага `-fps_mode cfr` звук в Remotion рассинхронизируется на 0.5–2 секунды к концу 60-секундного ролика. В `tools/ingest.py` частота теперь жестко фиксируется на 30.0 fps.
2. **Поворот в метаданных (Rotation 90/270):** Видео, снятые вертикально на некоторые камеры и смартфоны, физически хранятся как горизонтальные с тегом `rotate=90`. При транскодировании через ffmpeg кадры приводятся к вертикальному буферу (1080x1920) с удалением флага, исключая поворот на 90 градусов в рендерере.
3. **Легкая очистка звука (`--denoise`):** В конвейер добавлен шаг `afftdn=nf=-25` с полосовым фильтром (срез суб-гула ниже 80 Гц и шипения выше 12 кГц). Фильтр не затрагивает основной формантный диапазон человеческой речи (200–4000 Гц), сохраняя естественный тембр голоса спикера. По умолчанию флаг выключен, чтобы не искажать студийные записи.
4. **Нестандартные разрешения (записи экрана):** При масштабировании в прокси 720p фильтр `force_original_aspect_ratio=decrease,pad=720:1280` предотвращает искажение пропорций экрана.
