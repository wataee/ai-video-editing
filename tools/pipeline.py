#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline.py — Universal End-to-End Vertical Video Production Pipeline.
Usage:
  python tools/pipeline.py <input_video> --client <client_name> [--long] [--denoise]
Or via npm:
  npm run pipeline -- <input_video> --client <client_name>
"""

import os
import sys
import json
import time
import argparse
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

def generate_chapters(transcript_json_path: Path, out_chapters_md: Path, total_duration: float):
    if not transcript_json_path.exists():
        return
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        words = json.load(f)
    if not words:
        return

    chapters = []
    current_chapter_words = []
    chapter_start_sec = 0.0
    interval_target = 60.0  # ~60 seconds per chapter
    
    for w in words:
        current_chapter_words.append(w.get("text", ""))
        end_sec = w.get("endMs", 0) / 1000.0
        if (end_sec - chapter_start_sec) >= interval_target and any(w.get("text", "").endswith(p) for p in [".", "!", "?"]):
            snippet = " ".join(current_chapter_words[:12]).strip() + "..."
            chapters.append({
                "chapter": len(chapters) + 1,
                "start": round(chapter_start_sec, 2),
                "end": round(end_sec, 2),
                "duration": round(end_sec - chapter_start_sec, 2),
                "preview": snippet
            })
            chapter_start_sec = end_sec
            current_chapter_words = []
            
    if current_chapter_words:
        end_sec = words[-1].get("endMs", 0) / 1000.0
        snippet = " ".join(current_chapter_words[:12]).strip() + "..."
        chapters.append({
            "chapter": len(chapters) + 1,
            "start": round(chapter_start_sec, 2),
            "end": round(end_sec, 2),
            "duration": round(end_sec - chapter_start_sec, 2),
            "preview": snippet
        })

    lines = [
        "# Таблица глав длинного видео (Chapter Table)",
        f"> Общая длительность: {total_duration:.1f} с ({total_duration/60.0:.1f} мин)",
        "",
        "| Глава # | Начало (с) | Конец (с) | Длительность (с) | Превью тезиса |",
        "|:---:|:---:|:---:|:---:|---|",
    ]
    for ch in chapters:
        lines.append(f"| {ch['chapter']} | {ch['start']} | {ch['end']} | {ch['duration']} | {ch['preview']} |")
    lines.append("")
    
    out_chapters_md.parent.mkdir(parents=True, exist_ok=True)
    with open(out_chapters_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Chapters generated at: {out_chapters_md}")

def main():
    parser = argparse.ArgumentParser(description="AI Video Editing Production Pipeline")
    parser.add_argument("input_video", help="Path to input raw video file (mandatory)")
    parser.add_argument("--client", "-c", required=True, help="Client slug / name (mandatory)")
    parser.add_argument("--long", action="store_true", help="Long-form video mode (>5min): ingest, transcribe, scaffold, chapter table without rendering")
    parser.add_argument("--denoise", action="store_true", help="Apply gentle audio denoise (afftdn + filter)")
    parser.add_argument("--style", default="editorial-authority", help="Style preset name")
    args = parser.parse_args()

    in_video = Path(args.input_video).resolve()
    if not in_video.exists():
        print(f"Error: Input video does not exist: {in_video}", file=sys.stderr)
        sys.exit(1)

    client_slug = args.client.strip().lower().replace(" ", "_")
    client_dir = ROOT / "clients" / client_slug
    work_dir = client_dir / "work"
    out_dir = client_dir / "out"

    ingest_dir = work_dir / "ingest"
    transcribe_dir = work_dir / "transcribe"
    cut_dir = work_dir / "cut"
    plan_dir = work_dir / "plan"
    audio_dir = work_dir / "audio"
    qa_dir = work_dir / "qa"

    for d in [ingest_dir, transcribe_dir, cut_dir, plan_dir, audio_dir, qa_dir, out_dir]:
        d.mkdir(parents=True, exist_ok=True)

    base_name = in_video.stem
    pipeline_t0 = time.time()
    initial_work_size = get_dir_size_mb(work_dir)
    step_records = []

    print(f"Starting pipeline for Client='{client_slug}', Input='{in_video.name}'")

    # Step 1: Ingest
    ingest_py = ROOT / "tools" / "ingest.py"
    cmd_ingest = [sys.executable, str(ingest_py), str(in_video), "--output_dir", str(ingest_dir)]
    if args.denoise:
        cmd_ingest.append("--denoise")
    ok, el, out = run_step("1. Ingest (Color SDR Rec.709, CFR 30, Proxy)", cmd_ingest)
    sdr_video = ingest_dir / f"{base_name}_sdr_cfr30.mp4"
    proxy_video = ingest_dir / f"{base_name}_proxy.mp4"
    step_records.append({
        "step": "1. Ingest",
        "command": f"python tools/ingest.py {in_video.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(sdr_video.relative_to(ROOT)) if sdr_video.exists() else "FAIL"
    })
    if not ok or not sdr_video.exists():
        print("Ingest failed, stopping pipeline.", file=sys.stderr)
        sys.exit(1)

    # Probe duration
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(sdr_video)]
    probe_res = subprocess.run(probe_cmd, capture_output=True, text=True)
    dur = 15.0
    try:
        dur = float(json.loads(probe_res.stdout)["format"]["duration"])
    except Exception:
        pass

    is_long_mode = args.long or (dur > 300.0)

    # Step 2: Transcribe
    whisper_py = ROOT / "tools" / "venv-whisper" / "Scripts" / "python.exe"
    transcribe_script = ROOT / "tools" / "transcribe.py"
    cmd_transcribe = [
        str(whisper_py if whisper_py.exists() else sys.executable),
        str(transcribe_script),
        str(proxy_video if proxy_video.exists() else sdr_video),
        "--word_timestamps",
        "--output_dir", str(transcribe_dir)
    ]
    ok, el, out = run_step("2. Transcribe (faster-whisper word-level)", cmd_transcribe)
    transcript_json = transcribe_dir / f"{proxy_video.stem}.json"
    step_records.append({
        "step": "2. Transcribe",
        "command": f"tools/transcribe.py {proxy_video.name} --word_timestamps",
        "success": ok,
        "duration_sec": el,
        "output_file": str(transcript_json.relative_to(ROOT)) if transcript_json.exists() else "FAIL"
    })
    if not ok or not transcript_json.exists():
        print("Transcription failed, stopping pipeline.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Scaffold Plan via plan_scaffold.py
    scaffold_py = ROOT / "tools" / "plan_scaffold.py"
    plan_file = plan_dir / "edit_plan.json"
    cmd_scaffold = [
        sys.executable, str(scaffold_py),
        str(transcript_json),
        "--project_id", base_name,
        "--proxy", str(proxy_video),
        "--sdr", str(sdr_video),
        "--output", str(plan_file)
    ]
    ok, el, out = run_step("3. Plan Scaffold Generation (from transcript)", cmd_scaffold)
    step_records.append({
        "step": "3. Plan Scaffold",
        "command": f"python tools/plan_scaffold.py {transcript_json.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(plan_file.relative_to(ROOT))
    })

    if is_long_mode:
        chapters_md = plan_dir / "chapters.md"
        generate_chapters(transcript_json, chapters_md, dur)
        step_records.append({
            "step": "4. Chapter Table (Long-form Mode)",
            "command": "generate_chapters",
            "success": True,
            "duration_sec": 0.05,
            "output_file": str(chapters_md.relative_to(ROOT))
        })
        print("\n" + "="*80)
        print("LONG-FORM VIDEO DETECTED (>5 min or --long flag).")
        print("Completed: Ingest, Word-level Transcription, Scaffold Plan, Chapter Table.")
        print("Long-form video assembly is NOT rendered as per design.")
        print(f"Chapters saved to: {chapters_md}")
        print("="*80 + "\n")
        return

    # Step 4: Beat Table
    beat_table_py = ROOT / "tools" / "beat_table.py"
    beat_table_md = plan_dir / "beat_table.md"
    cmd_beat = [sys.executable, str(beat_table_py), str(plan_file), "--output", str(beat_table_md)]
    ok, el, out = run_step("4. Beat Table Verification", cmd_beat)
    step_records.append({
        "step": "4. Beat Table",
        "command": f"python tools/beat_table.py {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(beat_table_md.relative_to(ROOT))
    })

    # Step 5: Contact Sheet
    plan_sheet_py = ROOT / "tools" / "plan_contact_sheet.py"
    plan_sheet_png = plan_dir / "contact_sheet_plan.png"
    cmd_sheet = [sys.executable, str(plan_sheet_py), str(plan_file), "--output", str(plan_sheet_png)]
    ok, el, out = run_step("5. Plan Contact Sheet (Pre-render Storyboard)", cmd_sheet)
    step_records.append({
        "step": "5. Plan Contact Sheet",
        "command": f"python tools/plan_contact_sheet.py {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(plan_sheet_png.relative_to(ROOT))
    })

    # Check approval status
    with open(plan_file, "r", encoding="utf-8") as f:
        loaded_plan = json.load(f)
    is_approved = loaded_plan.get("approved", False)

    total_pipeline_time = round(time.time() - pipeline_t0, 2)
    final_work_size = get_dir_size_mb(work_dir)
    disk_consumed_mb = round(final_work_size - initial_work_size, 2)

    if not is_approved:
        print("\n" + "#"*80)
        print(" " * 20 + "APPROVAL GATE: ACTION REQUIRED BY HUMAN EDITOR")
        print("#"*80)
        print(f"The plan '{plan_file.name}' was constructed from Whisper transcript timestamps.")
        print("Creative visual decisions remain TODO and approved is false.")
        print("Pipeline is safely paused after the contact sheet.\n")
        print("WHAT YOU NEED TO DO:")
        print(f"  1. Review the keyframe storyboard: {plan_sheet_png}")
        print(f"  2. Review the beat sheet table:    {beat_table_md}")
        print(f"  3. Fill in creative fields (visual, proof_source, camera, sfx) in:")
        print(f"     -> {plan_file}")
        print("  4. Set 'approved': true in edit_plan.json.")
        print(f"  5. To finish assembly and sound mixing:")
        print(f"     python tools/mix.py {sdr_video} {plan_file} {audio_dir}")
        print(f"     python tools/qa.py {sdr_video} --plan {plan_file}")
        print(f"     npm run render:clip -- ReelFromPlan {out_dir / (base_name + '_v1.mp4')}")
        print("#"*80 + "\n")
        return

    # If already approved, proceed to mix and QA
    mix_py = ROOT / "tools" / "mix.py"
    cmd_mix = [sys.executable, str(mix_py), str(sdr_video), str(plan_file), str(audio_dir)]
    ok, el, out = run_step("6. Sound Mix (Relative dB Calibration)", cmd_mix)
    step_records.append({
        "step": "6. Sound Mix",
        "command": f"python tools/mix.py {sdr_video.name} {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str((audio_dir / "mix.wav").relative_to(ROOT))
    })

    qa_py = ROOT / "tools" / "qa.py"
    cmd_qa = [sys.executable, str(qa_py), str(sdr_video), "--plan", str(plan_file)]
    if transcript_json.exists():
        cmd_qa.extend(["--transcript", str(transcript_json)])
    mix_rep = audio_dir / "mix_report.json"
    if mix_rep.exists():
        cmd_qa.extend(["--mix_report", str(mix_rep)])
    ok, el, out = run_step("7. 10 FPS QA Inspection", cmd_qa)
    qa_report_file = qa_dir / f"{base_name}.qa.md"
    step_records.append({
        "step": "7. QA Check (10 FPS)",
        "command": f"python tools/qa.py {sdr_video.name} --plan {plan_file.name}",
        "success": ok,
        "duration_sec": el,
        "output_file": str(qa_report_file.relative_to(ROOT))
    })

    print(f"\nPipeline finished for Client='{client_slug}' in {total_pipeline_time}s.")

if __name__ == "__main__":
    main()
