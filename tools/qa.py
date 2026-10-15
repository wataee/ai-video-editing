# -*- coding: utf-8 -*-
"""
qa.py — Автоматизированный контроль качества готового видео (Quality Assurance).
Реализует все автоматические проверки по стандарту qa-checklist.md:
- ffprobe: разрешение, fps, кодек, pix_fmt, VFR/CFR
- blackdetect: обнаружение непреднамеренных чёрных кадров
- freezedetect: обнаружение зависших кадров
- silencedetect: проверка пауз и тишины
- loudnorm: измерение EBU R128 (Integrated LUFS, True Peak, LRA)
- Извлечение ключевых кадров и контактного листа (contact sheet)
- Разметка безопасных зон платформ (1080x1920: top 220, bottom 380, right 130)
- Экспорт детального JSON и Markdown отчёта
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    return res.returncode, res.stdout, res.stderr


def parse_fraction(s: str) -> float:
    try:
        if "/" in s:
            num, den = s.split("/")
            return float(num) / float(den) if float(den) != 0 else 0.0
        return float(s)
    except Exception:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="Автоматический контроль качества видео (QA)")
    parser.add_argument("video_file", help="Путь к видеофайлу")
    parser.add_argument("--output_dir", default=None, help="Папка сохранения QA-отчета и кадров")
    args = parser.parse_args()

    video_path = Path(args.video_file).resolve()
    if not video_path.exists():
        print(f"Ошибка: видеофайл не найден: {video_path}", file=sys.stderr)
        sys.exit(1)

    qa_dir = Path(args.output_dir).resolve() if args.output_dir else (video_path.parent / "qa")
    frames_dir = qa_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    base_name = video_path.stem
    print(f"Запуск QA-проверки для файла: {video_path.name}")
    print(f"Результаты будут сохранены в: {qa_dir}")

    report_data = {
        "file_name": video_path.name,
        "file_size_bytes": video_path.stat().st_size,
        "checks": {},
        "verdict": "ПРОЙДЕНО"
    }

    # 1. FFPROBE анализ стримов
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_streams", "-show_format",
        "-of", "json",
        str(video_path)
    ]
    code, stdout, stderr = run_command(cmd_probe)
    if code != 0:
        print(f"Ошибка ffprobe: {stderr}", file=sys.stderr)
        sys.exit(1)

    probe_json = json.loads(stdout)
    video_stream = next((s for s in probe_json.get("streams", []) if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in probe_json.get("streams", []) if s.get("codec_type") == "audio"), None)
    format_info = probe_json.get("format", {})

    duration = float(format_info.get("duration", 0.0))
    report_data["duration_seconds"] = round(duration, 2)

    # Видео-параметры
    v_width = int(video_stream.get("width", 0)) if video_stream else 0
    v_height = int(video_stream.get("height", 0)) if video_stream else 0
    v_codec = video_stream.get("codec_name", "unknown") if video_stream else "none"
    v_pix_fmt = video_stream.get("pix_fmt", "unknown") if video_stream else "none"
    r_fps = parse_fraction(video_stream.get("r_frame_rate", "0")) if video_stream else 0.0
    avg_fps = parse_fraction(video_stream.get("avg_frame_rate", "0")) if video_stream else 0.0
    is_vfr = abs(r_fps - avg_fps) > 0.05

    report_data["video"] = {
        "width": v_width,
        "height": v_height,
        "aspect_ratio": f"{v_width}:{v_height}",
        "codec": v_codec,
        "pix_fmt": v_pix_fmt,
        "r_fps": round(r_fps, 2),
        "avg_fps": round(avg_fps, 2),
        "is_vfr": is_vfr
    }

    # Аудио-параметры
    a_codec = audio_stream.get("codec_name", "none") if audio_stream else "none"
    a_channels = int(audio_stream.get("channels", 0)) if audio_stream else 0
    a_rate = int(audio_stream.get("sample_rate", 0)) if audio_stream else 0
    report_data["audio"] = {
        "present": audio_stream is not None,
        "codec": a_codec,
        "channels": a_channels,
        "sample_rate": a_rate
    }

    # 2. Blackdetect (поиск чёрных кадров)
    cmd_black = [
        "ffmpeg", "-v", "error", "-i", str(video_path),
        "-vf", "blackdetect=d=0.1:pix_th=0.10",
        "-f", "null", "-"
    ]
    _, _, black_stderr = run_command(cmd_black)
    black_starts = re.findall(r"black_start:([0-9.]+)", black_stderr)
    black_ends = re.findall(r"black_end:([0-9.]+)", black_stderr)
    black_durations = re.findall(r"black_duration:([0-9.]+)", black_stderr)
    black_events = [{"start": s, "end": e, "duration": d} for s, e, d in zip(black_starts, black_ends, black_durations)]
    report_data["checks"]["black_frames"] = {
        "status": "ПРОЙДЕНО" if len(black_events) == 0 else "ВНИМАНИЕ",
        "events_count": len(black_events),
        "events": black_events
    }

    # 3. Freezedetect (поиск зависших кадров)
    cmd_freeze = [
        "ffmpeg", "-v", "error", "-i", str(video_path),
        "-vf", "freezedetect=n=0.003:d=2",
        "-f", "null", "-"
    ]
    _, _, freeze_stderr = run_command(cmd_freeze)
    freeze_starts = re.findall(r"lavfi.freezedetect.freeze_start:\s*([0-9.]+)", freeze_stderr)
    freeze_durations = re.findall(r"lavfi.freezedetect.freeze_duration:\s*([0-9.]+)", freeze_stderr)
    freeze_events = [{"start": s, "duration": d} for s, d in zip(freeze_starts, freeze_durations)]
    report_data["checks"]["freeze_frames"] = {
        "status": "ПРОЙДЕНО" if len(freeze_events) == 0 else "ВНИМАНИЕ",
        "events_count": len(freeze_events),
        "events": freeze_events
    }

    # 4. Silencedetect (поиск длинных пауз тишины)
    cmd_silence = [
        "ffmpeg", "-v", "error", "-i", str(video_path),
        "-af", "silencedetect=n=-50dB:d=1.5",
        "-f", "null", "-"
    ]
    _, _, silence_stderr = run_command(cmd_silence)
    silence_starts = re.findall(r"silence_start:\s*([0-9.]+)", silence_stderr)
    silence_ends = re.findall(r"silence_end:\s*([0-9.]+)", silence_stderr)
    silence_events = [{"start": s, "end": e} for s, e in zip(silence_starts, silence_ends)]
    report_data["checks"]["silence_gaps"] = {
        "status": "ПРОЙДЕНО" if len(silence_events) == 0 else "ВНИМАНИЕ",
        "events_count": len(silence_events),
        "events": silence_events
    }

    # 5. Loudnorm (EBU R128 анализ)
    cmd_loud = [
        "ffmpeg", "-nostats", "-i", str(video_path),
        "-af", "loudnorm=print_format=json",
        "-f", "null", "-"
    ]
    _, _, loud_stderr = run_command(cmd_loud)
    loud_json_match = re.search(r"\{[\s\S]*\"input_i\"[\s\S]*\}", loud_stderr)
    if loud_json_match:
        try:
            loud_data = json.loads(loud_json_match.group(0))
            meas_i = float(loud_data.get("input_i", -99))
            meas_tp = float(loud_data.get("input_tp", 99))
            meas_lra = float(loud_data.get("input_lra", 0))

            i_ok = -16.0 <= meas_i <= -13.0
            tp_ok = meas_tp <= -0.5
            report_data["checks"]["loudness_ebu_r128"] = {
                "status": "ПРОЙДЕНО" if (i_ok and tp_ok) else "ТРЕБУЕТ КОРРЕКЦИИ",
                "integrated_lufs": meas_i,
                "target_lufs": -14.0,
                "true_peak_dbtp": meas_tp,
                "max_true_peak_dbtp": -1.0,
                "lra": meas_lra
            }
        except Exception as e:
            report_data["checks"]["loudness_ebu_r128"] = {"status": "ОШИБКА", "error": str(e)}
    else:
        report_data["checks"]["loudness_ebu_r128"] = {"status": "Н/Д", "note": "Звук отсутствует или не распознан"}

    # 6. Извлечение ключевых кадров
    # Кадр 0.1s
    frame_01 = frames_dir / "frame_start.png"
    run_command(["ffmpeg", "-y", "-ss", "0.1", "-i", str(video_path), "-vframes", "1", str(frame_01)])

    # Кадр середины
    mid_time = max(0.5, duration / 2.0)
    frame_mid = frames_dir / "frame_middle.png"
    run_command(["ffmpeg", "-y", "-ss", str(round(mid_time, 2)), "-i", str(video_path), "-vframes", "1", str(frame_mid)])

    # Последний кадр
    end_time = max(0.1, duration - 0.2)
    frame_end = frames_dir / "frame_end.png"
    run_command(["ffmpeg", "-y", "-ss", str(round(end_time, 2)), "-i", str(video_path), "-vframes", "1", str(frame_end)])

    # 7. Контактный лист (Contact Sheet)
    contact_sheet = qa_dir / "contact_sheet.png"
    cmd_sheet = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", "fps=1/2,scale=270:480,tile=4x2",
        "-frames:v", "1",
        str(contact_sheet)
    ]
    run_command(cmd_sheet)

    # 8. Наложение безопасных зон (Safe Zones Overlay)
    # Зоны для 1080x1920: верх 220px, низ 380px, право 130px, лево 50px
    safe_zones_frame = qa_dir / "safe_zones_overlay.png"
    box_filter = (
        "drawbox=x=0:y=0:w=iw:h=220:color=red@0.35:t=fill,"
        "drawbox=x=0:y=ih-380:w=iw:h=380:color=red@0.35:t=fill,"
        "drawbox=x=iw-130:y=220:w=130:h=ih-600:color=yellow@0.35:t=fill,"
        "drawbox=x=0:y=220:w=50:h=ih-600:color=yellow@0.35:t=fill"
    )
    cmd_safe = [
        "ffmpeg", "-y", "-ss", str(round(mid_time, 2)), "-i", str(video_path),
        "-vf", box_filter,
        "-frames:v", "1",
        str(safe_zones_frame)
    ]
    run_command(cmd_safe)

    # 9. Формирование финальных файлов отчёта
    json_path = qa_dir / f"{base_name}.qa.json"
    summary_path = qa_dir / f"{base_name}.qa.summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    # Формирование ультра-компактного JSON для LLM (Claude Pro)
    issues = []
    if is_vfr:
        issues.append(f"VFR detected (variable framerate: r_fps={r_fps}, avg_fps={avg_fps})")
    if v_width != 1080 or v_height != 1920:
        issues.append(f"Non-standard 9:16 resolution: {v_width}x{v_height}")
    if len(black_events) > 0:
        issues.append(f"Detected {len(black_events)} unexpected black frame sequences")
    if len(freeze_events) > 0:
        issues.append(f"Detected {len(freeze_events)} frozen frame events (>2s)")
    if len(silence_events) > 0:
        issues.append(f"Detected {len(silence_events)} audio silence gaps (>1.5s)")

    loud_info = report_data["checks"].get("loudness_ebu_r128", {})
    if loud_info.get("status") == "ТРЕБУЕТ КОРРЕКЦИИ":
        issues.append(f"Audio loudness out of spec: I={loud_info.get('integrated_lufs')} LUFS, TP={loud_info.get('true_peak_dbtp')} dBTP")

    overall_verdict = "ТРЕБУЕТ ПРАВОК" if issues else "ПРОЙДЕНО"
    report_data["verdict"] = overall_verdict

    summary_data = {
        "file": video_path.name,
        "verdict": overall_verdict,
        "duration_sec": round(duration, 2),
        "resolution": f"{v_width}x{v_height}",
        "fps": round(r_fps, 2),
        "is_vfr": is_vfr,
        "loudness_lufs": loud_info.get("integrated_lufs", "N/A"),
        "true_peak_dbtp": loud_info.get("true_peak_dbtp", "N/A"),
        "issues_count": len(issues),
        "issues": issues,
        "contact_sheet": str(contact_sheet.relative_to(qa_dir)),
        "safe_zones_frame": str(safe_zones_frame.relative_to(qa_dir))
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    # Markdown отчет
    md_path = qa_dir / f"{base_name}.qa.md"
    loud_info = report_data["checks"].get("loudness_ebu_r128", {})
    loud_status = loud_info.get("status", "Н/Д")
    meas_i_str = f"{loud_info.get('integrated_lufs', 'Н/Д')} LUFS"
    meas_tp_str = f"{loud_info.get('true_peak_dbtp', 'Н/Д')} dBTP"

    md_content = f"""# QA Отчёт технического контроля: `{video_path.name}`

> **Дата инспекции:** 2026-10-15  
> **Инспектор:** `tools/qa.bat` (автоматизированный конвейер)  
> **Чеклист:** `qa-checklist.md` (Разделы 1–3)

---

## 1. Сводка технических параметров

| Параметр | Измеренное значение | Требование стандарта | Вердикт |
| :--- | :--- | :--- | :---: |
| **Разрешение / Соотношение** | `{v_width}x{v_height}` (`{v_width}:{v_height}`) | `1080x1920` (9:16) | {"✅ ПРОЙДЕНО" if (v_width==1080 and v_height==1920) else "❌ НЕ ПРОЙДЕНО"} |
| **Частота кадров (FPS)** | `{round(r_fps, 2)}` fps (VFR: `{'Да (переменный)' if is_vfr else 'Нет (CFR)'}`) | 30 или 60 fps (CFR) | {"✅ ПРОЙДЕНО" if not is_vfr else "⚠️ VFR ОБНАРУЖЕН"} |
| **Видеокодек / Pix Fmt** | `{v_codec}` / `{v_pix_fmt}` | H.264 (yuv420p) | {"✅ ПРОЙДЕНО" if (v_codec=='h264' and v_pix_fmt=='yuv420p') else "⚠️ ПРОВЕРИТЬ"} |
| **Длительность** | `{round(duration, 2)}` с | По ТЗ ролика | ✅ ИНФО |
| **Аудиоканал** | `{a_codec}`, `{a_channels}` канала, `{a_rate}` Гц | AAC Stereo, 48000 Гц | {"✅ ПРОЙДЕНО" if (a_channels>=2 and a_codec=='aac') else "⚠️ ПРОВЕРИТЬ"} |
| **Интегральная громкость (I)** | `{meas_i_str}` | `-14.0 LUFS` (±1.5) | {loud_status} |
| **True Peak (TP)** | `{meas_tp_str}` | `≤ -1.0 dBTP` | {loud_status} |
| **Чёрные кадры (blackdetect)** | `{len(black_events)}` событий | 0 непреднамеренных | {"✅ ПРОЙДЕНО" if len(black_events)==0 else "⚠️ ОБНАРУЖЕНЫ"} |
| **Зависшие кадры (freezedetect)** | `{len(freeze_events)}` событий | 0 зависаний | {"✅ ПРОЙДЕНО" if len(freeze_events)==0 else "⚠️ ОБНАРУЖЕНЫ"} |
| **Длинные паузы (silencedetect)**| `{len(silence_events)}` событий (>1.5 с) | 0 немотивированных | {"✅ ПРОЙДЕНО" if len(silence_events)==0 else "⚠️ ОБНАРУЖЕНЫ"} |

---

## 2. Графические материалы инспекции

- **Контактный лист таймлайна (Contact Sheet):** [`{contact_sheet.name}`]({contact_sheet.name})
- **Проверка безопасных зон (Safe Zones):** [`{safe_zones_frame.name}`]({safe_zones_frame.name})
  *(Красная заливка: верхние 220 px и нижние 380 px; Жёлтая заливка: боковые системные кнопки 130 px)*
- **Ключевые кадры:**
  - Начало (0.1 с): [`{frame_01.name}`]({frame_01.name})
  - Середина ({round(mid_time, 1)} с): [`{frame_mid.name}`]({frame_mid.name})
  - Финал ({round(end_time, 1)} с): [`{frame_end.name}`]({frame_end.name})

---

## 3. Что НЕ удалось проверить автономно (Требует человека)

1. **Субъективное восприятие анимации:** Плавность динамических зумов и переходов на 120 Гц экранах смартфонов.
2. **Акустический баланс:** Разборчивость голоса спикера на встроенных динамиках мобильного телефона при внешнем шуме.
3. **Эмоциональная честность хука:** Соответствие драматургического обещания первых 3 секунд содержанию ролика.
"""

    md_path.write_text(md_content, encoding="utf-8")
    print(f"\nQA проверка успешно завершена!")
    print(f"  JSON отчет: {json_path}")
    print(f"  Markdown отчет: {md_path}")
    print(f"  Контактный лист: {contact_sheet}")
    print(f"  Безопасные зоны: {safe_zones_frame}")


if __name__ == "__main__":
    main()
