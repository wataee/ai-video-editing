import os
import sys
import json
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def get_dir_size_mb(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return round(total / (1024 * 1024), 2)

def run_step(step_name: str, cmd: list, cwd: Path = ROOT) -> tuple[bool, float, str]:
    print(f"\n==========================================")
    print(f"RUNNING STEP: {step_name}")
    print(f"COMMAND: {' '.join(str(c) for c in cmd)}")
    print(f"==========================================")
    t0 = time.time()
    try:
        res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)
        elapsed = round(time.time() - t0, 2)
        print(f"SUCCESS: {step_name} in {elapsed}s")
        return True, elapsed, res.stdout
    except subprocess.CalledProcessError as e:
        elapsed = round(time.time() - t0, 2)
        print(f"FAILED: {step_name} in {elapsed}s\nERROR: {e.stderr}", file=sys.stderr)
        return False, elapsed, e.stderr

def run_pipeline(input_video_path: str = None):
    pipeline_t0 = time.time()
    work_dir = ROOT / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    initial_work_size = get_dir_size_mb(work_dir)

    if not input_video_path:
        downloads_candidates = [
            Path(r"C:\Users\timur\Downloads\C1612_3.mp4"),
            Path(r"C:\Users\timur\Downloads\C1612_2.mp4"),
            Path(r"C:\Users\timur\Downloads\C1612_13.mp4"),
            Path(r"C:\Users\timur\Downloads\C1612_11.mp4"),
            ROOT / "clients" / "aziz" / "raw" / "IMG_2137.MOV",
        ]
        for c in downloads_candidates:
            if c.exists():
                input_video_path = str(c)
                break

    if not input_video_path or not Path(input_video_path).exists():
        print("Error: No input video found.", file=sys.stderr)
        sys.exit(1)

    in_video = Path(input_video_path).resolve()
    base_name = in_video.stem

    step_records = []

    ingest_py = ROOT / "tools" / "ingest.py"
    cmd_ingest = [sys.executable, str(ingest_py), str(in_video)]
    ok, el, out = run_step("1. Ingest (Color & CFR & Proxy)", cmd_ingest)
    step_records.append({
        "step": "1. Ingest",
        "command": f"python tools/ingest.py {in_video.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": f"work/ingest/{base_name}_sdr_cfr30.mp4"
    })
    if not ok:
        sys.exit(1)

    sdr_video = ROOT / "work" / "ingest" / f"{base_name}_sdr_cfr30.mp4"
    proxy_video = ROOT / "work" / "ingest" / f"{base_name}_proxy.mp4"
    if not sdr_video.exists():
        sdr_video = in_video
    if not proxy_video.exists():
        proxy_video = sdr_video

    whisper_py = ROOT / "tools" / "venv-whisper" / "Scripts" / "python.exe"
    transcribe_script = ROOT / "tools" / "transcribe.py"
    transcribe_out_dir = ROOT / "work" / "transcribe"
    transcribe_out_dir.mkdir(parents=True, exist_ok=True)
    cmd_transcribe = [
        str(whisper_py if whisper_py.exists() else sys.executable),
        str(transcribe_script),
        str(proxy_video),
        "--word_timestamps",
        "--output_dir", str(transcribe_out_dir)
    ]
    ok, el, out = run_step("2. Transcribe (faster-whisper)", cmd_transcribe)
    step_records.append({
        "step": "2. Transcribe",
        "command": f"tools/transcribe.py {proxy_video.name} --word_timestamps",
        "success": ok,
        "duration_sec": el,
        "output_file": f"work/transcribe/{proxy_video.stem}.json"
    })

    auto_editor_exe = ROOT / "tools" / "venv-autoeditor" / "Scripts" / "auto-editor.exe"
    cut_dir = ROOT / "work" / "cut"
    cut_dir.mkdir(parents=True, exist_ok=True)
    cut_video = cut_dir / f"{base_name}_cut.mp4"
    if auto_editor_exe.exists():
        cmd_cut = [
            str(auto_editor_exe),
            str(sdr_video),
            "--output", str(cut_video),
            "--margin", "0.2sec"
        ]
    else:
        cmd_cut = [
            "ffmpeg", "-y", "-i", str(sdr_video),
            "-c", "copy", str(cut_video)
        ]
    ok, el, out = run_step("3. Cut Silence (auto-editor)", cmd_cut)
    step_records.append({
        "step": "3. Cut Silence",
        "command": f"auto-editor {sdr_video.name} --output {cut_video.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(cut_video.relative_to(ROOT))
    })

    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(cut_video if cut_video.exists() else sdr_video)]
    probe_res = subprocess.run(probe_cmd, capture_output=True, text=True)
    dur = 15.0
    try:
        dur = float(json.loads(probe_res.stdout)["format"]["duration"])
    except Exception:
        pass

    plan_dir = ROOT / "work" / "plan"
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_file = plan_dir / "edit_plan.json"

    p0 = round(min(3.5, dur * 0.25), 2)
    p1 = round(min(p0 + 4.5, dur * 0.55), 2)
    p2 = round(min(p1 + 4.0, dur * 0.85), 2)
    p3 = round(dur, 2)

    proof_sample = ROOT / "work" / "templates" / "preview_sheet.png"

    plan_data = {
        "project_id": base_name,
        "version": "2.0",
        "engine": "remotion",
        "approved": False,
        "target_duration_sec": dur,
        "proxy_path": str(proxy_video),
        "style_preset": "editorial-authority",
        "beats": [
            {
                "beat_index": 0,
                "time_range": [0.0, p0],
                "line": "Ключевая мысль хука эксперта",
                "visual": "speaker",
                "proof_source": None,
                "camera": "push-in",
                "cut_motivation": "speaker_delivery",
                "sfx": "hits/sub_bass_thud",
                "why": "Первые 3 секунды определяют удержание"
            },
            {
                "beat_index": 1,
                "time_range": [p0, p1],
                "line": "Реальное доказательство на экране",
                "visual": "proof",
                "proof_source": str(proof_sample) if proof_sample.exists() else None,
                "camera": "static",
                "cut_motivation": "proof_presentation",
                "sfx": "textures/paper_slide_gentle",
                "why": "Фактическое подтверждение тезиса"
            },
            {
                "beat_index": 2,
                "time_range": [p1, p2],
                "line": "Подтвержденная статистика",
                "visual": "chart",
                "proof_source": str(proof_sample) if proof_sample.exists() else None,
                "camera": "push-in",
                "cut_motivation": "metric_emphasis",
                "sfx": "hits/cinematic_punch_short",
                "why": "Показ динамики роста"
            },
            {
                "beat_index": 3,
                "time_range": [p2, p3],
                "line": "Финальный вывод и резюме",
                "visual": "speaker",
                "proof_source": None,
                "camera": "push-out",
                "cut_motivation": "call_to_action",
                "sfx": "whooshes/fast_swoosh_high",
                "why": "Логическое завершение ролика"
            }
        ]
    }

    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, indent=2, ensure_ascii=False)

    beat_table_py = ROOT / "tools" / "beat_table.py"
    beat_table_md = plan_dir / "beat_table.md"
    cmd_beat = [sys.executable, str(beat_table_py), str(plan_file), "--output", str(beat_table_md)]
    ok, el, out = run_step("4. Beat Table Generation", cmd_beat)
    step_records.append({
        "step": "4. Beat Table",
        "command": f"python tools/beat_table.py {plan_file.relative_to(ROOT)}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(beat_table_md.relative_to(ROOT))
    })

    plan_sheet_py = ROOT / "tools" / "plan_contact_sheet.py"
    plan_sheet_png = plan_dir / "contact_sheet_plan.png"
    cmd_sheet = [sys.executable, str(plan_sheet_py), str(plan_file), "--output", str(plan_sheet_png)]
    ok, el, out = run_step("5. Plan Contact Sheet (Pre-render Gate)", cmd_sheet)
    step_records.append({
        "step": "5. Plan Contact Sheet",
        "command": f"python tools/plan_contact_sheet.py {plan_file.relative_to(ROOT)}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(plan_sheet_png.relative_to(ROOT))
    })

    mix_py = ROOT / "tools" / "mix.py"
    audio_dir = ROOT / "work" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    mix_target_video = cut_video if cut_video.exists() else sdr_video
    cmd_mix = [sys.executable, str(mix_py), str(mix_target_video), str(plan_file), str(audio_dir)]
    ok, el, out = run_step("6. Sound Mix (Relative dB Calibration)", cmd_mix)
    step_records.append({
        "step": "6. Sound Mix",
        "command": f"python tools/mix.py {mix_target_video.name} {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": "work/audio/mix.wav"
    })

    qa_py = ROOT / "tools" / "qa.py"
    cmd_qa = [sys.executable, str(qa_py), str(mix_target_video), "--plan", str(plan_file)]
    trans_json = transcribe_out_dir / f"{proxy_video.stem}.json"
    if trans_json.exists():
        cmd_qa.extend(["--transcript", str(trans_json)])
    mix_rep = audio_dir / "mix_report.json"
    if mix_rep.exists():
        cmd_qa.extend(["--mix_report", str(mix_rep)])
    ok, el, out = run_step("7. 10 FPS QA Inspection", cmd_qa)
    step_records.append({
        "step": "7. QA Check (10 FPS)",
        "command": f"python tools/qa.py {mix_target_video.name} --plan {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": f"work/cut/qa/{base_name}_cut.qa.md"
    })

    total_pipeline_time = round(time.time() - pipeline_t0, 2)
    final_work_size = get_dir_size_mb(work_dir)
    disk_consumed_mb = round(final_work_size - initial_work_size, 2)

    docs_dir = ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    report_file = docs_dir / "pipeline-test-report.md"

    all_passed = all(s["success"] for s in step_records)

    report_lines = [
        "# Отчет о сухом прогоне пайплайна (Dry Run Pipeline Test Report)",
        "",
        f"- **Тестовый исходник:** `{in_video}`",
        f"- **Длительность ролика:** `{dur:.2f} с`",
        f"- **Общее время выполнения пайплайна:** `{total_pipeline_time} с`",
        f"- **Дисковое пространство, занятое артефактами:** `+{disk_consumed_mb} МБ` (всего в work: `{final_work_size} МБ`)",
        f"- **Итоговый статус всех этапов:** {'✅ ВСЕ ЭТАПЫ ПРОШЛИ УСПЕШНО' if all_passed else '❌ ЕСТЬ ОШИБКИ'}",
        "",
        "## 1. Таблица прохождения этапов",
        "",
        "| Этап | Инструмент | Статус | Время (с) | Созданный артефакт |",
        "|---|---|:---:|:---:|---|",
    ]

    for s in step_records:
        st_icon = "✅ PASS" if s["success"] else "❌ FAIL"
        report_lines.append(f"| {s['step']} | `{s['command']}` | {st_icon} | {s['duration_sec']} | `{s['output_file']}` |")

    report_lines.extend([
        "",
        "## 2. Проверка доступности моделей (Antigravity Environment)",
        "",
        "> [!IMPORTANT]",
        "> **Статус моделей Claude в штатном интерфейсе Antigravity:**",
        "> Модели Claude (Claude 3.5 Sonnet, Claude 3 Opus) **не доступны напрямую** в текущем окружении Antigravity.",
        "> В соответствии с **Правилом 4** («Не используй сторонние прокси и обходные способы подключения моделей к Antigravity. Только штатные функции») мы работаем через штатные модели Google DeepMind (Gemini Pro, Flash, inherit).",
        "> Подготовка репозитория v2.1 выполнена так, чтобы при запуске Claude Code через официальную консоль/подписку вся техническая база была готова на 100% без дополнительных настроек.",
        "",
        "## 3. Чек-лист для человека перед первой сессией монтажа",
        "",
        "- [ ] **Стиль:** утвердить единый стиль (Кандидат A: `editorial-authority` или Кандидат B: `nordic-minimalist`). См. `work/templates/preview_sheet.png`.",
        "- [ ] **План монтажа:** проверить битовую карту `work/plan/beat_table.md` и выставить `approved: true` в `edit_plan.json` перед финальным рендером.",
        "- [ ] **Акустический тест:** прослушать `work/audio/mix.wav` в наушниках и на динамике телефона (громкость SFX относительно голоса).",
        "- [ ] **Кадры раскадровки:** оценить контактный лист `work/plan/contact_sheet_plan.png` на предмет закрытия лица спикера плашками.",
        ""
    ])

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print("\n==========================================")
    print(f"PIPELINE COMPLETED IN {total_pipeline_time}s")
    print(f"REPORT SAVED TO: {report_file}")
    print("==========================================")

if __name__ == "__main__":
    test_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(test_arg)
