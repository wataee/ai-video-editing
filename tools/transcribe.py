#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transcribe.py — Профессиональный инструмент локальной транскрибации медиафайлов
на базе faster-whisper (CTranslate2).

Поддерживает экспорт:
- TXT: полный сплошной текст
- SRT: стандартные субтитры с таймкодами
- JSON: пословные метки (word-level timestamps), полностью совместимые с Remotion @remotion/captions
- Поддержка глоссариев (--glossary) через initial_prompt и hotwords
"""

import argparse
import inspect
import json
import os
import sys
import time
from pathlib import Path

# Поиск CUDA DLLs в site-packages/nvidia/*/bin
site_packages = Path(sys.prefix) / "Lib" / "site-packages"
if site_packages.exists():
    for nv_bin in site_packages.glob("nvidia/*/bin"):
        if nv_bin.is_dir():
            try:
                os.add_dll_directory(str(nv_bin))
                os.environ["PATH"] = str(nv_bin) + os.pathsep + os.environ["PATH"]
            except Exception:
                pass


def format_timestamp_srt(seconds: float) -> str:
    """Форматирование секунд в формат SRT (ЧЧ:ММ:СС,мс)"""
    millisec = int(round((seconds - int(seconds)) * 1000))
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisec:03d}"


def detect_device() -> tuple[str, str]:
    """Автоматическое определение доступности GPU (NVIDIA CUDA) с безопасным откатом на CPU"""
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda", "float16"
    except Exception:
        pass
    return "cpu", "int8"


def main():
    parser = argparse.ArgumentParser(description="Локальная транскрибация видео/аудио через faster-whisper")
    parser.add_argument("input_file", help="Путь к видео или аудио файлу (MP4, MKV, MOV, WAV, MP3 и т.д.)")
    parser.add_argument("--model", default="base", help="Размер модели: tiny, base, small, medium, large-v3 (по умолчанию: base)")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"], help="Устройство вычислений (auto, cpu, cuda)")
    parser.add_argument("--language", default=None, help="Код языка (ru, en и т.д.). По умолчанию автоопределение")
    parser.add_argument("--output_dir", "--output-dir", default=None, help="Директория сохранения результатов (по умолчанию: work клиента)")
    parser.add_argument("--glossary", default=None, help="Файл глоссария с терминами и именами (txt)")
    parser.add_argument("--word_timestamps", "--word-timestamps", action="store_true", default=True, help="Извлекать пословные таймкоды (для Remotion)")

    args = parser.parse_args()

    input_path = Path(args.input_file).resolve()
    if not input_path.exists():
        print(f"Ошибка: Файл не найден: {input_path}", file=sys.stderr)
        sys.exit(1)

    root_dir = Path(__file__).resolve().parent.parent
    if args.output_dir:
        out_dir = Path(args.output_dir).resolve()
    else:
        # Ищем родительскую директорию клиента, содержащую work/
        curr = input_path.parent
        found_work = None
        while curr != curr.parent and curr != root_dir:
            if (curr / "work").is_dir():
                found_work = (curr / "work").resolve()
                break
            if curr.name == "raw" and (curr.parent / "work").is_dir():
                found_work = (curr.parent / "work").resolve()
                break
            curr = curr.parent
        out_dir = found_work if found_work else (root_dir / "clients" / "_demo" / "work").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = input_path.stem

    # Чтение глоссария
    glossary_terms = []
    initial_prompt = None
    hotwords_str = None
    if args.glossary:
        gl_path = Path(args.glossary).resolve()
        if gl_path.exists():
            for line in gl_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    glossary_terms.append(line)
            if glossary_terms:
                initial_prompt = "Термины и имена: " + ", ".join(glossary_terms)
                hotwords_str = " ".join(glossary_terms)
        else:
            print(f"Предупреждение: файл глоссария не найден: {gl_path}", file=sys.stderr)

    # Определение устройства
    if args.device == "auto":
        device, compute_type = detect_device()
    elif args.device == "cuda":
        device, compute_type = "cuda", "float16"
    else:
        device, compute_type = "cpu", "int8"

    print(f"Запуск транскрибации:")
    print(f" - Входной файл: {input_path.name}")
    print(f" - Модель: {args.model}")
    print(f" - Устройство: {device} ({compute_type})")
    if args.language:
        print(f" - Заданный язык: {args.language}")
    else:
        print(f" - Язык: Автоопределение")
    if glossary_terms:
        print(f" - Загружен глоссарий ({len(glossary_terms)} терминов)")

    from faster_whisper import WhisperModel

    def run_transcription(dev, comp):
        m = WhisperModel(args.model, device=dev, compute_type=comp)
        kwargs = {
            "language": args.language,
            "word_timestamps": args.word_timestamps,
            "beam_size": 5
        }
        if initial_prompt:
            kwargs["initial_prompt"] = initial_prompt

        sig = inspect.signature(m.transcribe)
        if "hotwords" in sig.parameters and hotwords_str:
            kwargs["hotwords"] = hotwords_str

        segs, inf = m.transcribe(str(input_path), **kwargs)
        return list(segs), inf

    start_time = time.time()
    try:
        segments, info = run_transcription(device, compute_type)
    except Exception as e:
        if device == "cuda":
            print(f"Внимание: Не удалось выполнить на CUDA ({e}). Переключение на CPU (int8)...", file=sys.stderr)
            device, compute_type = "cpu", "int8"
            segments, info = run_transcription(device, compute_type)
        else:
            raise

    detected_lang = info.language
    lang_prob = info.language_probability
    print(f"Определён язык: {detected_lang} (вероятность {lang_prob:.2%}), длительность: {info.duration:.1f} с")

    txt_lines = []
    srt_entries = []
    remotion_words = []
    full_segments_data = []

    srt_index = 1
    for segment in segments:
        text = segment.text.strip()
        txt_lines.append(text)

        # Формирование SRT
        start_srt = format_timestamp_srt(segment.start)
        end_srt = format_timestamp_srt(segment.end)
        srt_entries.append(f"{srt_index}\n{start_srt} --> {end_srt}\n{text}\n")
        srt_index += 1

        # Формирование JSON для Remotion @remotion/captions
        seg_words = []
        if segment.words:
            for word in segment.words:
                w_start_ms = int(round(word.start * 1000))
                w_end_ms = int(round(word.end * 1000))
                w_text = word.word
                remotion_words.append({
                    "text": w_text,
                    "startMs": w_start_ms,
                    "endMs": w_end_ms,
                    "timestampMs": w_start_ms,
                    "confidence": round(word.probability, 3)
                })
                seg_words.append({
                    "word": w_text,
                    "start": round(word.start, 3),
                    "end": round(word.end, 3),
                    "probability": round(word.probability, 3)
                })

        full_segments_data.append({
            "id": segment.id,
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": text,
            "avg_logprob": round(segment.avg_logprob, 3),
            "no_speech_prob": round(segment.no_speech_prob, 3),
            "words": seg_words
        })

    # Сохранение файлов
    txt_path = out_dir / f"{base_name}.txt"
    srt_path = out_dir / f"{base_name}.srt"
    json_path = out_dir / f"{base_name}.json"
    detailed_json_path = out_dir / f"{base_name}_detailed.json"
    compact_txt_path = out_dir / f"{base_name}_compact.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines) + "\n")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(remotion_words, f, ensure_ascii=False, indent=2)

    with open(detailed_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "source_file": input_path.name,
            "language": detected_lang,
            "language_probability": round(lang_prob, 4),
            "duration": round(info.duration, 2),
            "model": args.model,
            "device": device,
            "compute_type": compute_type,
            "segments_count": len(segments),
            "segments": full_segments_data
        }, f, ensure_ascii=False, indent=2)

    # Генерация компактного транскрипта для LLM (экономия токенов Claude Pro)
    compact_lines = [
        f"# Компактный транскрипт для LLM (Claude Pro): {base_name}",
        f"# Длительность: {info.duration:.1f} с | Язык: {detected_lang}",
        "-" * 50,
        ""
    ]
    for seg in segments:
        s_m = int(seg.start // 60)
        s_s = int(seg.start % 60)
        e_m = int(seg.end // 60)
        e_s = int(seg.end % 60)
        compact_lines.append(f"[{s_m:02d}:{s_s:02d} - {e_m:02d}:{e_s:02d}] {seg.text.strip()}")

    with open(compact_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(compact_lines) + "\n")

    elapsed = time.time() - start_time
    print(f"\nТранскрибация успешно завершена за {elapsed:.2f} с!")
    print(f"Результаты сохранены:")
    print(f"  [Компактный для LLM] : {compact_txt_path}")
    print(f"  [TXT]               : {txt_path}")
    print(f"  [SRT]               : {srt_path}")
    print(f"  [Remotion Words]    : {json_path}")
    print(f"  [Detailed JSON]     : {detailed_json_path}")


if __name__ == "__main__":
    main()
