#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compact_transcript.py — Генерация ультра-компактного транскрипта для LLM (Claude Pro).

Экономит до 85-95% токенов контекста по сравнению с передачей полного *_detailed.json.
Принимает на вход:
- Файл *_detailed.json или *.json от faster-whisper
- Или файл *.srt
- Или напрямую медиафайл (автоматически находит транскрипт в work/ или запускает transcribe.py)

Выход: файл *_compact.txt с таймкодами вида:
[02:14 - 02:19] Большинство людей монтируют видео неправильно, потому что начинают с эффектов.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def format_seconds(sec: float) -> str:
    total_sec = int(round(sec))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_srt(srt_path: Path) -> list[dict]:
    content = srt_path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(
        r"(\d+)\s*\n"
        r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n"
        r"([\s\S]*?)(?=\n\s*\n|\Z)",
        re.MULTILINE
    )
    entries = []
    for match in pattern.finditer(content):
        text = " ".join(match.group(4).strip().splitlines())
        if not text:
            continue
        entries.append({
            "start_str": match.group(2)[:8],
            "end_str": match.group(3)[:8],
            "text": text
        })
    return entries


def parse_detailed_json(json_path: Path) -> list[dict]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    segments = data.get("segments", [])
    entries = []
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue
        start = seg.get("start", 0.0)
        end = seg.get("end", 0.0)
        entries.append({
            "start": start,
            "end": end,
            "start_str": format_seconds(start),
            "end_str": format_seconds(end),
            "text": text
        })
    return entries


def main():
    parser = argparse.ArgumentParser(description="Создание компактного транскрипта для LLM")
    parser.add_argument("input_path", help="Путь к *_detailed.json, *.srt или видеофайлу")
    parser.add_argument("--output", "-o", default=None, help="Путь к выходному файлу (по умолчанию: <name>_compact.txt)")
    args = parser.parse_args()

    in_path = Path(args.input_path).resolve()
    if not in_path.exists():
        print(f"Ошибка: входной файл не найден: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Определение типа файла
    entries = []
    base_name = in_path.stem
    if base_name.endswith("_detailed"):
        base_name = base_name[:-9]

    if in_path.suffix.lower() == ".json":
        entries = parse_detailed_json(in_path)
    elif in_path.suffix.lower() == ".srt":
        entries = parse_srt(in_path)
    else:
        # Попытка найти существующий json в папке work
        possible_json = in_path.parent.parent / "work" / f"{in_path.stem}_detailed.json"
        if not possible_json.exists():
            possible_json = in_path.parent / f"{in_path.stem}_detailed.json"
        if possible_json.exists():
            entries = parse_detailed_json(possible_json)
        else:
            print(f"Файл {in_path} является медиафайлом. Сначала запустите: tools/transcribe.bat \"{in_path}\"", file=sys.stderr)
            sys.exit(1)

    if not entries:
        print(f"Ошибка: не удалось извлечь сегменты речи из {in_path}", file=sys.stderr)
        sys.exit(1)

    out_file = Path(args.output).resolve() if args.output else in_path.parent / f"{base_name}_compact.txt"

    lines = [
        f"# Компактный транскрипт для анализа хуков и монтажа",
        f"# Исходник: {base_name}",
        f"# Сегментов: {len(entries)}",
        f"# Формат: [ММ:СС - ММ:СС] Текст речи",
        "-" * 50,
        ""
    ]

    for item in entries:
        start_s = item.get("start_str", "")
        end_s = item.get("end_str", "")
        text = item.get("text", "")
        lines.append(f"[{start_s} - {end_s}] {text}")

    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Компактный транскрипт успешно создан:")
    print(f"  Файл: {out_file}")
    print(f"  Строк: {len(entries)}")
    print(f"  Размер: {out_file.stat().st_size} байт (готов к отправке в Claude Pro)")


if __name__ == "__main__":
    main()
