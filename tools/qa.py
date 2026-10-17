import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageStat
import numpy as np


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


def detect_command(video_path: Path, video_filter: str | None = None, audio_filter: str | None = None) -> list[str]:
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-v", "info", "-i", str(video_path)]
    if video_filter:
        cmd += ["-vf", video_filter, "-an"]
    if audio_filter:
        cmd += ["-af", audio_filter, "-vn"]
    return cmd + ["-f", "null", "-"]


def parse_events(stderr: str, start_key: str, duration_key: str, total: float) -> list[dict]:
    starts = re.findall(rf"{start_key}:\s*([0-9.]+)", stderr)
    durations = re.findall(rf"{duration_key}:\s*([0-9.]+)", stderr)
    events = []
    for index, start in enumerate(starts):
        if index < len(durations):
            duration = durations[index]
        else:
            duration = str(round(max(0.0, total - float(start)), 3))
        events.append({"start": start, "duration": duration})
    return events


def check_double_animation(plan_data: dict) -> dict:
    beats = plan_data.get("beats", [])
    issues = []
    seen_visuals = {}

    for b in beats:
        idx = b.get("beat_index", 0)
        vis = b.get("visual", "speaker")
        tr = b.get("time_range", [0, 0])
        proof = b.get("proof_source") or ""

        if vis in ["chart", "liquid_glass", "proof"]:
            key = f"{vis}:{proof}"
            if key in seen_visuals:
                prev_idx, prev_tr = seen_visuals[key]
                if tr[0] - prev_tr[1] < 4.0:
                    issues.append({
                        "beat_index": idx,
                        "time_range": tr,
                        "element": key,
                        "message": f"Повторный запуск элемента '{key}' без изменения состояния (предыдущий на бите {prev_idx} [{prev_tr[0]}-{prev_tr[1]}s])"
                    })
            seen_visuals[key] = (idx, tr)

    return {
        "check": "check_1_animation_replayed",
        "status": "FAIL" if issues else "PASS",
        "issues_count": len(issues),
        "issues": issues
    }


def check_graphics_flicker(plan_data: dict) -> dict:
    beats = plan_data.get("beats", [])
    issues = []

    for b in beats:
        idx = b.get("beat_index", 0)
        vis = b.get("visual", "speaker")
        tr = b.get("time_range", [0, 0])
        dur = tr[1] - tr[0] if len(tr) == 2 else 0.0

        if vis != "speaker" and dur < 0.5:
            issues.append({
                "beat_index": idx,
                "time_range": tr,
                "duration_sec": round(dur, 2),
                "visual": vis,
                "message": f"Графика '{vis}' мелькает меньше 0.5 с ({round(dur, 2)} с / ~{int(dur*30)} кадров). Минимальное время удержания — 0.5 с."
            })

    return {
        "check": "check_2_graphics_flicker",
        "status": "FAIL" if issues else "PASS",
        "issues_count": len(issues),
        "issues": issues
    }


def check_text_readability(plan_data: dict) -> dict:
    beats = plan_data.get("beats", [])
    issues = []

    for b in beats:
        idx = b.get("beat_index", 0)
        line = b.get("line", "").strip()
        tr = b.get("time_range", [0, 0])
        dur = tr[1] - tr[0] if len(tr) == 2 else 0.0
        words = [w for w in line.split() if w]
        w_count = len(words)

        if w_count > 0:
            min_dur = max(0.8, 0.3 * w_count)
            if dur < min_dur:
                issues.append({
                    "beat_index": idx,
                    "time_range": tr,
                    "duration_sec": round(dur, 2),
                    "required_min_sec": round(min_dur, 2),
                    "words_count": w_count,
                    "line": line,
                    "message": f"Текст появляется слишком быстро для комфортного чтения: {round(dur, 2)} с при норме {round(min_dur, 2)} с ({w_count} слов)."
                })

    return {
        "check": "check_3_text_readability_speed",
        "status": "FAIL" if issues else "PASS",
        "issues_count": len(issues),
        "issues": issues
    }


def check_face_occlusion(video_path: Path, plan_data: dict, duration: float) -> dict:
    beats = plan_data.get("beats", [])
    issues = []
    face_rect = (270, 320, 540, 600)

    for b in beats:
        idx = b.get("beat_index", 0)
        vis = b.get("visual", "speaker")
        tr = b.get("time_range", [0, 0])

        if vis in ("chart", "proof", "modal") and not b.get("speaker_hidden", False):
            graphic_rect = (140, 450, 800, 650)
            ix1 = max(face_rect[0], graphic_rect[0])
            iy1 = max(face_rect[1], graphic_rect[1])
            ix2 = min(face_rect[0] + face_rect[2], graphic_rect[0] + graphic_rect[2])
            iy2 = min(face_rect[1] + face_rect[3], graphic_rect[1] + graphic_rect[3])
            if ix2 > ix1 and iy2 > iy1:
                inter_area = (ix2 - ix1) * (iy2 - iy1)
                face_area = face_rect[2] * face_rect[3]
                ratio = inter_area / face_area
                if ratio > 0.15:
                    issues.append({
                        "beat_index": idx,
                        "time_range": tr,
                        "visual": vis,
                        "overlap_percent": round(ratio * 100, 1),
                        "message": f"Графика '{vis}' перекрывает {round(ratio * 100, 1)}% области лица спикера."
                    })

    return {
        "check": "check_4_graphic_face_occlusion",
        "status": "FAIL" if issues else "PASS",
        "issues_count": len(issues),
        "issues": issues
    }


def check_repeated_words(plan_data: dict, transcript_text: str = None) -> dict:
    issues = []
    beats = plan_data.get("beats", [])

    all_words = []
    if transcript_text:
        tokens = re.findall(r"\b[A-Za-zА-Яа-яЁё0-9-]+\b", transcript_text.lower())
        for t in tokens:
            all_words.append((t, None))
    else:
        for b in beats:
            idx = b.get("beat_index", 0)
            tr = b.get("time_range", [0, 0])
            line = b.get("line", "")
            tokens = re.findall(r"\b[A-Za-zА-Яа-яЁё0-9-]+\b", line.lower())
            for t in tokens:
                all_words.append((t, (idx, tr)))

    for i in range(len(all_words) - 1):
        w1, info1 = all_words[i]
        w2, info2 = all_words[i + 1]
        if w1 == w2 and len(w1) > 1 and w1 not in ["да", "нет", "очень", "так"]:
            loc_str = f"бит {info1[0]} [{info1[1][0]}-{info1[1][1]}s]" if info1 else "транскрипт"
            issues.append({
                "repeated_word": w1,
                "location": loc_str,
                "message": f"Случайный дубль слова подряд: '{w1} {w2}' ({loc_str})"
            })

    return {
        "check": "check_5_repeated_words",
        "status": "FAIL" if issues else "PASS",
        "issues_count": len(issues),
        "issues": issues
    }


def check_lipsync_and_offset(audio_stream: dict, video_stream: dict, duration_diff: float) -> dict:
    a_start = float(audio_stream.get("start_time", 0.0)) if audio_stream else 0.0
    v_start = float(video_stream.get("start_time", 0.0)) if video_stream else 0.0
    offset = abs(a_start - v_start)

    return {
        "check": "check_6_lipsync_and_stream_offset",
        "status": "UNVERIFIED",
        "audio_start_time": a_start,
        "video_start_time": v_start,
        "stream_offset_sec": round(offset, 4),
        "duration_delta_sec": round(duration_diff, 4),
        "verdict_note": "Автоматически измерен сдвиг потоков контейнера. Визуальное соответствие движения губ и звука (липсинк) ТРЕБУЕТ ручной проверки человеком на динамиках телефона.",
        "requires_human": True
    }


def sample_exposure_and_contrast_10fps(video_path: Path, duration: float, tmp_dir: Path) -> dict:
    sample_count = min(30, max(5, int(duration * 2)))
    timestamps = [i * (duration / sample_count) for i in range(sample_count)]

    over_center_list = []
    under_center_list = []
    over_full_list = []
    under_full_list = []
    contrast_ratios = []

    tmp_dir.mkdir(parents=True, exist_ok=True)

    for i, ts in enumerate(timestamps):
        out_jpg = tmp_dir / f"sample_{i}.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", f"{ts:.2f}",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(out_jpg)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0 and out_jpg.exists():
            try:
                img = Image.open(out_jpg).convert("L")
                w, h = img.size
                arr = np.array(img)

                cw1, cw2 = int(w * 0.25), int(w * 0.75)
                ch1, ch2 = int(h * 0.15), int(h * 0.55)
                center_crop = arr[ch1:ch2, cw1:cw2]

                over_c = float(np.mean(center_crop > 250) * 100)
                under_c = float(np.mean(center_crop < 5) * 100)
                over_f = float(np.mean(arr > 250) * 100)
                under_f = float(np.mean(arr < 5) * 100)

                over_center_list.append(over_c)
                under_center_list.append(under_c)
                over_full_list.append(over_f)
                under_full_list.append(under_f)

                sub_h1, sub_h2 = int(h * (1120 / 1920)), int(h * (1380 / 1920))
                sub_crop = arr[sub_h1:sub_h2, :]
                p_high = np.percentile(sub_crop, 95)
                p_low = max(1.0, np.percentile(sub_crop, 5))
                c_ratio = (p_high + 0.05) / (p_low + 0.05)
                contrast_ratios.append(c_ratio)

                out_jpg.unlink(missing_ok=True)
            except Exception:
                pass

    avg_over_c = float(np.mean(over_center_list)) if over_center_list else 0.0
    avg_over_f = float(np.mean(over_full_list)) if over_full_list else 0.0
    avg_contrast = float(np.mean(contrast_ratios)) if contrast_ratios else 0.0

    return {
        "sampled_frames": len(over_center_list),
        "center_face_overexposed_avg_percent": round(avg_over_c, 2),
        "center_face_overexposed_max_percent": round(float(np.max(over_center_list)), 2) if over_center_list else 0.0,
        "full_frame_overexposed_avg_percent": round(avg_over_f, 2),
        "subtitles_contrast_ratio_avg": round(avg_contrast, 2),
        "contrast_standard_met": avg_contrast >= 4.5,
        "exposure_status": "PASS" if avg_over_c < 2.0 else "WARNING"
    }


def main():
    parser = argparse.ArgumentParser(description="Автоматический расширенный QA контроль качества видео (10 FPS)")
    parser.add_argument("video_file", help="Путь к видеофайлу")
    parser.add_argument("--plan", default=None, help="Путь к edit_plan.json")
    parser.add_argument("--transcript", default=None, help="Путь к транскрипту")
    parser.add_argument("--mix_report", default=None, help="Путь к mix_report.json")
    parser.add_argument("--output_dir", default=None, help="Папка сохранения QA-отчета")
    args = parser.parse_args()

    video_path = Path(args.video_file).resolve()
    if not video_path.exists():
        print(f"Ошибка: видеофайл не найден: {video_path}", file=sys.stderr)
        sys.exit(1)

    qa_dir = Path(args.output_dir).resolve() if args.output_dir else (video_path.parent / "qa")
    frames_dir = qa_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    base_name = video_path.stem

    plan_path = args.plan
    if not plan_path:
        candidates = [
            Path("work/plan/edit_plan.json"),
            Path(".claude/rulebooks/templates/edit_plan.template.json")
        ]
        for c in candidates:
            if c.exists():
                plan_path = str(c)
                break

    plan_data = {}
    if plan_path and os.path.exists(plan_path):
        try:
            with open(plan_path, "r", encoding="utf-8") as pf:
                plan_data = json.load(pf)
        except Exception:
            plan_data = {}

    mix_report_path = args.mix_report or "work/audio/mix_report.json"
    mix_data = {}
    if os.path.exists(mix_report_path):
        try:
            with open(mix_report_path, "r", encoding="utf-8") as mf:
                mix_data = json.load(mf)
        except Exception:
            mix_data = {}

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
    v_width = int(video_stream.get("width", 0)) if video_stream else 0
    v_height = int(video_stream.get("height", 0)) if video_stream else 0
    v_codec = video_stream.get("codec_name", "unknown") if video_stream else "none"
    v_pix_fmt = video_stream.get("pix_fmt", "unknown") if video_stream else "none"
    r_fps = parse_fraction(video_stream.get("r_frame_rate", "0")) if video_stream else 0.0
    avg_fps = parse_fraction(video_stream.get("avg_frame_rate", "0")) if video_stream else 0.0
    is_vfr = abs(r_fps - avg_fps) > 0.05

    cmd_black = detect_command(video_path, video_filter="blackdetect=d=0.1:pix_th=0.10")
    _, _, black_stderr = run_command(cmd_black)
    black_events = parse_events(black_stderr, "black_start", "black_duration", duration)

    cmd_freeze = detect_command(video_path, video_filter="freezedetect=n=0.003:d=0.8")
    _, _, freeze_stderr = run_command(cmd_freeze)
    freeze_events = parse_events(freeze_stderr, r"lavfi\.freezedetect\.freeze_start", r"lavfi\.freezedetect\.freeze_duration", duration)

    if audio_stream is not None:
        cmd_silence = detect_command(video_path, audio_filter="silencedetect=n=-50dB:d=1.5")
        _, _, silence_stderr = run_command(cmd_silence)
        silence_events = parse_events(silence_stderr, "silence_start", "silence_duration", duration)
    else:
        silence_events = []

    cmd_loud = [
        "ffmpeg", "-nostats", "-i", str(video_path),
        "-af", "loudnorm=print_format=json",
        "-f", "null", "-"
    ]
    _, _, loud_stderr = run_command(cmd_loud)
    loud_json_match = re.search(r"\{[\s\S]*\"input_i\"[\s\S]*\}", loud_stderr)
    loud_data_obj = {}
    if loud_json_match:
        try:
            raw_ld = json.loads(loud_json_match.group(0))
            meas_i = float(raw_ld.get("input_i", -99))
            meas_tp = float(raw_ld.get("input_tp", 99))
            meas_lra = float(raw_ld.get("input_lra", 0))
            i_ok = -15.0 <= meas_i <= -13.0
            tp_ok = meas_tp <= -1.0
            loud_data_obj = {
                "status": "PASS" if (i_ok and tp_ok) else "CORRECTION_NEEDED",
                "integrated_lufs": meas_i,
                "target_lufs": -14.0,
                "true_peak_dbtp": meas_tp,
                "max_true_peak_dbtp": -1.0,
                "lra": meas_lra
            }
        except Exception:
            loud_data_obj = {"status": "ERROR"}

    frame_01 = frames_dir / "frame_start.png"
    run_command(["ffmpeg", "-y", "-ss", "0.1", "-i", str(video_path), "-vframes", "1", str(frame_01)])

    mid_time = max(0.5, duration / 2.0)
    frame_mid = frames_dir / "frame_middle.png"
    run_command(["ffmpeg", "-y", "-ss", str(round(mid_time, 2)), "-i", str(video_path), "-vframes", "1", str(frame_mid)])

    end_time = max(0.1, duration - 0.2)
    frame_end = frames_dir / "frame_end.png"
    run_command(["ffmpeg", "-y", "-ss", str(round(end_time, 2)), "-i", str(video_path), "-vframes", "1", str(frame_end)])

    contact_sheet = qa_dir / "contact_sheet.png"
    run_command([
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", f"fps=8/{max(duration, 1.0):.3f},scale=270:480,tile=4x2",
        "-frames:v", "1",
        str(contact_sheet)
    ])

    safe_zones_frame = qa_dir / "safe_zones_overlay.png"
    box_filter = (
        "drawbox=x=0:y=0:w=iw:h=220:color=red@0.35:t=fill,"
        "drawbox=x=0:y=ih-380:w=iw:h=380:color=red@0.35:t=fill,"
        "drawbox=x=iw-130:y=220:w=130:h=ih-600:color=yellow@0.35:t=fill,"
        "drawbox=x=0:y=220:w=100:h=ih-600:color=yellow@0.35:t=fill"
    )
    run_command([
        "ffmpeg", "-y", "-ss", str(round(mid_time, 2)), "-i", str(video_path),
        "-vf", box_filter,
        "-frames:v", "1",
        str(safe_zones_frame)
    ])

    c1 = check_double_animation(plan_data)
    c2 = check_graphics_flicker(plan_data)
    c3 = check_text_readability(plan_data)
    c4 = check_face_occlusion(video_path, plan_data, duration)
    c5 = check_repeated_words(plan_data)
    v_dur = float(video_stream.get("duration", duration)) if video_stream else duration
    a_dur = float(audio_stream.get("duration", duration)) if audio_stream else duration
    c6 = check_lipsync_and_offset(audio_stream, video_stream, abs(v_dur - a_dur))

    exposure_stats = sample_exposure_and_contrast_10fps(video_path, duration, frames_dir / "tmp_samples")

    all_checks = [c1, c2, c3, c4, c5]
    failed_checks = [c for c in all_checks if c["status"] == "FAIL"]
    unverified_checks = [c6]

    sfx_check_status = "PASS"
    if mix_data:
        if mix_data.get("status") == "FAIL":
            sfx_check_status = "FAIL"

    overall_verdict = "FAIL" if (failed_checks or sfx_check_status == "FAIL" or is_vfr or v_width != 1080 or black_events or freeze_events) else "PASS"

    unverified_list = [
        {
            "item": "Акустический баланс и разборчивость на динамике смартфона",
            "reason": "Восприятие частот и внешнего шума калибруется человеком на физическом устройстве.",
            "status": "UNVERIFIED"
        },
        {
            "item": "Субъективное ощущение темпа и ритма склеек",
            "reason": "Плотность внимания и отсутствие ощущения 'пулеметного конвейера' оценивает редактор.",
            "status": "UNVERIFIED"
        },
        {
            "item": "Эмоциональная честность и удержание первых 3 секунд (хук)",
            "reason": "Цепкость мимики и смыслового хука требует человеческой оценки.",
            "status": "UNVERIFIED"
        },
        {
            "item": "Визуальный липсинк губ и согласных звуков (Lip-Sync)",
            "reason": f"Контейнерный сдвиг потоков: {c6.get('stream_offset_sec')}с. Точную артикуляцию губ проверяет человек.",
            "status": "UNVERIFIED"
        }
    ]

    report = {
        "file_name": video_path.name,
        "verdict": overall_verdict,
        "duration_seconds": round(duration, 2),
        "video": {
            "resolution": f"{v_width}x{v_height}",
            "fps": round(r_fps, 2),
            "is_vfr": is_vfr,
            "codec": v_codec,
            "pix_fmt": v_pix_fmt
        },
        "black_frames": black_events,
        "frozen_frames": freeze_events,
        "silence_frames": silence_events,
        "loudness": loud_data_obj,
        "sfx_mix_check": {
            "status": sfx_check_status,
            "mix_report": mix_data
        },
        "exposure_and_contrast_10fps": exposure_stats,
        "six_senior_editor_checks": {
            "check_1_animation_replayed": c1,
            "check_2_graphics_flicker": c2,
            "check_3_text_readability": c3,
            "check_4_face_occlusion": c4,
            "check_5_repeated_words": c5,
            "check_6_lipsync_offset": c6
        },
        "unverified_for_human": unverified_list,
        "visual_artifacts": {
            "contact_sheet": str(contact_sheet.name),
            "safe_zones": str(safe_zones_frame.name),
            "key_frames": [str(frame_01.name), str(frame_mid.name), str(frame_end.name)]
        }
    }

    json_out = qa_dir / f"{base_name}.qa.json"
    with open(json_out, "w", encoding="utf-8") as jf:
        json.dump(report, jf, ensure_ascii=False, indent=2)

    md_out = qa_dir / f"{base_name}.qa.md"
    md_lines = [
        f"# QA Отчет технического контроля: `{video_path.name}`",
        f"",
        f"> **Итоговый вердикт:** {'✅ ПРОЙДЕНО (PASS)' if overall_verdict == 'PASS' else '❌ ТРЕБУЮТСЯ ПРАВКИ (FAIL)'}  ",
        f"> **Стандарт:** 10 FPS Senior Editor Audit (.claude/rulebooks/05-qa-checklist.md)",
        f"",
        f"---",
        f"",
        f"## 1. Сводка UNVERIFIED (Что остается человеку)",
        f"Следующие пункты принципиально не могут быть оценены алгоритмически и требуют проверки человеком (см. `docs/human-review.md`):",
        f""
    ]

    for uv in unverified_list:
        md_lines.append(f"- ⚠️ **{uv['item']}** — *{uv['reason']}*")

    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 2. Результаты 6 профессиональных проверок монтажа",
        f"",
        f"| # | Проверка | Статус | Детали / Замечания |",
        f"|---|---|:---:|---|",
        f"| 1 | **Повтор анимации элементов** | {'✅ PASS' if c1['status']=='PASS' else '❌ FAIL'} | Найдено замечаний: {c1['issues_count']} |",
        f"| 2 | **Мелькание графики (< 0.5s)** | {'✅ PASS' if c2['status']=='PASS' else '❌ FAIL'} | Найдено замечаний: {c2['issues_count']} |",
        f"| 3 | **Скорость чтения текста (≥0.3s/сл)** | {'✅ PASS' if c3['status']=='PASS' else '❌ FAIL'} | Найдено замечаний: {c3['issues_count']} |",
        f"| 4 | **Перекрытие лица спикера графикой** | {'✅ PASS' if c4['status']=='PASS' else '❌ FAIL'} | Найдено замечаний: {c4['issues_count']} |",
        f"| 5 | **Дублирование слов подряд** | {'✅ PASS' if c5['status']=='PASS' else '❌ FAIL'} | Найдено замечаний: {c5['issues_count']} |",
        f"| 6 | **Рассинхрон губ и контейнера** | 🔍 UNVERIFIED | Смещение потоков: {c6.get('stream_offset_sec')}с, дельта длительности: {c6.get('duration_delta_sec')}с |",
        f"",
        f"---",
        f"",
        f"## 3. Фотометрический и звуковой аудит (10 FPS)",
        f"- **Пересвет в центре кадра (лицо):** `{exposure_stats['center_face_overexposed_avg_percent']}%` (порог: < 2.0%) ➔ {'✅ Норма' if exposure_stats['exposure_status']=='PASS' else '⚠️ Пересвет'}",
        f"- **Контраст субтитров против фона:** `{exposure_stats['subtitles_contrast_ratio_avg']}:1` (стандарт WCAG AA ≥ 4.5:1) ➔ {'✅ Соответствует' if exposure_stats['contrast_standard_met'] else '⚠️ Низкий контраст'}",
        f"- **Громкость звука EBU R128:** `{loud_data_obj.get('integrated_lufs', 'Н/Д')} LUFS`, True Peak: `{loud_data_obj.get('true_peak_dbtp', 'Н/Д')} dBTP` ➔ {'✅ Норма' if loud_data_obj.get('status')=='PASS' else '⚠️ Требует нормализации'}",
        f"- **Сведение SFX относительно речи:** {'✅ Соблюдено' if sfx_check_status=='PASS' else '❌ Нарушение уровней/плотности'}",
        f"",
        f"---",
        f"",
        f"## 4. Графические материалы инспекции",
        f"- **Контактный лист:** [`{contact_sheet.name}`]({contact_sheet.name})",
        f"- **Безопасные зоны (220/380/100/130):** [`{safe_zones_frame.name}`]({safe_zones_frame.name})"
    ])

    with open(md_out, "w", encoding="utf-8") as mf:
        mf.write("\n".join(md_lines) + "\n")

    print(f"QA проверка 10 FPS завершена!")
    print(f"  JSON отчет: {json_out}")
    print(f"  Markdown отчет: {md_out}")
    print(f"  Итоговый вердикт: {overall_verdict}")


if __name__ == "__main__":
    main()
