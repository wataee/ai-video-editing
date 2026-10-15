#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slice_words_json.py — Нарезка пословных таймкодов Whisper под конкретный фрагмент ролика.

Позволяет вырезать только те слова, которые попадают в хронометраж выбранного хука
(например, с 02:14.5 по 02:49.0), и при необходимости сместить таймкоды к 0.0 с.
Это избавляет от необходимости передавать мегабайтные файлы пословных меток в LLM.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_time_str(val: str) -> float:
    """Парсинг строки времени (секунды или ММ:СС / ММ:СС.мс) в секунды (float)."""
    val = str(val).strip()
    if ":" in val:
        parts = val.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return float(minutes) * 60.0 + float(seconds)
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return float(hours) * 3600.0 + float(minutes) * 60.0 + float(seconds)
    return float(val)


def main():
    parser = argparse.ArgumentParser(description="Нарезка пословных меток Whisper под выбранный диапазон")
    parser.add_argument("input_json", help="Путь к *_detailed.json или *.json с пословными метками")
    parser.add_argument("--start", default=None, help="Время начала (секунды или ММ:СС.мс, например 134.5 или 02:14.5)")
    parser.add_argument("--end", default=None, help="Время конца (секунды или ММ:СС.мс, например 169.0 или 02:49.0)")
    parser.add_argument("--plan", default=None, help="Путь к edit_plan.json (автоматически берет start и end)")
    parser.add_argument("--output", "-o", default=None, help="Путь сохранения результата (по умолчанию: <name>_sliced_words.json)")
    parser.add_argument("--keep_absolute", action="store_true", default=False, help="Не смещать таймкоды к 0.0 с (оставить абсолютное время исходника)")
    args = parser.parse_args()

    in_path = Path(args.input_json).resolve()
    if not in_path.exists():
        print(f"Ошибка: входной файл не найден: {in_path}", file=sys.stderr)
        sys.exit(1)

    start_sec = None
    end_sec = None

    if args.plan:
        plan_path = Path(args.plan).resolve()
        if not plan_path.exists():
            print(f"Ошибка: файл плана не найден: {plan_path}", file=sys.stderr)
            sys.exit(1)
        plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
        # Попытка извлечь start/end из hook или timeline.cuts
        hook = plan_data.get("hook", {})
        cuts = plan_data.get("timeline", {}).get("cuts", [])
        if "source_in" in hook:
            start_sec = parse_time_str(hook["source_in"])
        elif cuts:
            start_sec = parse_time_str(cuts[0]["source_in"])
        
        if cuts:
            end_sec = parse_time_str(cuts[-1]["source_out"])
        elif "source_out" in hook:
            end_sec = parse_time_str(hook["source_out"])

    if args.start is not None:
        start_sec = parse_time_str(args.start)
    if args.end is not None:
        end_sec = parse_time_str(args.end)

    if start_sec is None or end_sec is None:
        print("Ошибка: необходимо указать --start и --end, либо передать --plan", file=sys.stderr)
        sys.exit(1)

    if start_sec >= end_sec:
        print(f"Ошибка: start ({start_sec}с) должен быть меньше end ({end_sec}с)", file=sys.stderr)
        sys.exit(1)

    raw_data = json.loads(in_path.read_text(encoding="utf-8"))

    all_words = []
    # Вариант 1: файл *_detailed.json
    if isinstance(raw_data, dict) and "segments" in raw_data:
        for seg in raw_data["segments"]:
            for w in seg.get("words", []):
                all_words.append({
                    "text": w.get("word", ""),
                    "start": w.get("start", 0.0),
                    "end": w.get("end", 0.0),
                    "confidence": w.get("probability", 1.0)
                })
    # Вариант 2: Remotion words list
    elif isinstance(raw_data, list):
        for item in raw_data:
            start_s = item.get("startMs", 0) / 1000.0
            end_s = item.get("endMs", 0) / 1000.0
            all_words.append({
                "text": item.get("text", ""),
                "start": start_s,
                "end": end_s,
                "confidence": item.get("confidence", 1.0)
            })
    else:
        print(f"Ошибка: неизвестный формат JSON в {in_path}", file=sys.stderr)
        sys.exit(1)

    sliced = []
    offset = 0.0 if args.keep_absolute else start_sec

    for w in all_words:
        w_start = w["start"]
        w_end = w["end"]
        # Слово попадает в диапазон, если его середина внутри [start_sec, end_sec]
        mid = (w_start + w_end) / 2.0
        if start_sec <= mid <= end_sec:
            adj_start = max(0.0, w_start - offset)
            adj_end = max(adj_start + 0.05, w_end - offset)
            sliced.append({
                "text": w["text"].strip(),
                "startMs": int(round(adj_start * 1000)),
                "endMs": int(round(adj_end * 1000)),
                "timestampMs": int(round(adj_start * 1000)),
                "confidence": round(w["confidence"], 3)
            })

    base_name = in_path.stem.replace("_detailed", "")
    out_file = Path(args.output).resolve() if args.output else in_path.parent / f"{base_name}_sliced_words.json"

    out_file.write_text(json.dumps(sliced, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Пословные метки успешно нарезаны:")
    print(f"  Диапазон: {start_sec:.2f} с -> {end_sec:.2f} с (длительность: {end_sec - start_sec:.2f} с)")
    print(f"  Слов отобрано: {len(sliced)}")
    print(f"  Смещение таймкодов к 0.0: {'Нет (абсолютные)' if args.keep_absolute else 'Да (относительные для сборки)'}")
    print(f"  Результат сохранён в: {out_file}")


if __name__ == "__main__":
    main()
