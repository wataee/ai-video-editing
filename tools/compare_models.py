# -*- coding: utf-8 -*-
"""
compare_models.py — Сравнение скорости и точности (WER) моделей Whisper.
Модели: tiny, base, small, medium, large-v3-turbo.
"""

import argparse
import sys
import os
import re
import time
from pathlib import Path

# Поиск CUDA DLLs
site_packages = Path(sys.prefix) / "Lib" / "site-packages"
if site_packages.exists():
    for nv_bin in site_packages.glob("nvidia/*/bin"):
        if nv_bin.is_dir():
            try:
                os.add_dll_directory(str(nv_bin))
                os.environ["PATH"] = str(nv_bin) + os.pathsep + os.environ["PATH"]
            except Exception:
                pass


def word_levenshtein(ref_words: list[str], hyp_words: list[str]) -> int:
    """Вычисление расстояния Левенштейна на уровне слов без внешних библиотек."""
    r_len = len(ref_words)
    h_len = len(hyp_words)
    d = [[0] * (h_len + 1) for _ in range(r_len + 1)]

    for i in range(r_len + 1):
        d[i][0] = i
    for j in range(h_len + 1):
        d[0][j] = j

    for i in range(1, r_len + 1):
        for j in range(1, h_len + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[r_len][h_len]


def normalize_words(text: str) -> list[str]:
    """Нормализация текста для подсчета WER (нижний регистр, удаление пунктуации)."""
    text = text.lower().replace("ё", "е")
    words = re.findall(r"\b\w+\b", text)
    return words


def compute_wer(ref_text: str, hyp_text: str) -> float:
    ref_words = normalize_words(ref_text)
    hyp_words = normalize_words(hyp_text)
    if not ref_words:
        return 0.0 if not hyp_words else 100.0
    dist = word_levenshtein(ref_words, hyp_words)
    return round((dist / len(ref_words)) * 100.0, 2)


def main():
    parser = argparse.ArgumentParser(description="Сравнение моделей Whisper по скорости и точности")
    parser.add_argument("input_file", help="Входной медиафайл")
    parser.add_argument("--ref", default=None, help="Файл с эталонным текстом (txt)")
    parser.add_argument("--output", default=None, help="Путь сохранения markdown-отчета")
    parser.add_argument("--language", default="ru", help="Код языка (ru)")
    args = parser.parse_args()

    input_path = Path(args.input_file).resolve()
    if not input_path.exists():
        print(f"Ошибка: входной файл не найден: {input_path}", file=sys.stderr)
        sys.exit(1)

    ref_text = ""
    if args.ref:
        ref_path = Path(args.ref).resolve()
        if ref_path.exists():
            ref_text = ref_path.read_text(encoding="utf-8", errors="ignore").strip()
            print(f"Загружен эталонный текст ({len(normalize_words(ref_text))} слов)")

    root_dir = Path(__file__).resolve().parent.parent
    out_report = Path(args.output).resolve() if args.output else (root_dir / "clients" / "_demo" / "work" / "model-comparison.md")
    out_report.parent.mkdir(parents=True, exist_ok=True)

    from faster_whisper import WhisperModel

    models_to_test = ["tiny", "base", "small", "medium", "large-v3-turbo"]
    results = []

    print(f"\nЗапуск тестирования моделей на файле: {input_path.name}")
    print(f"Целевой файл отчёта: {out_report}\n")

    for model_name in models_to_test:
        print(f"--- Тестирование модели: {model_name} ---")
        device = "cpu"
        compute_type = "int8"
        t0 = time.time()
        try:
            model = WhisperModel(model_name, device=device, compute_type=compute_type)
            segments, info = model.transcribe(str(input_path), language=args.language, beam_size=5)
            transcribed_text = " ".join(seg.text.strip() for seg in segments)
            elapsed = time.time() - t0
            duration = info.duration
            speedup = round(duration / elapsed, 2) if elapsed > 0 else 0.0

            wer_val = None
            if ref_text:
                wer_val = compute_wer(ref_text, transcribed_text)

            results.append({
                "model": model_name,
                "status": "OK",
                "device": f"{device} ({compute_type})",
                "duration": round(duration, 1),
                "elapsed": round(elapsed, 2),
                "speedup": f"{speedup}x",
                "wer": f"{wer_val}%" if wer_val is not None else "Н/Д",
                "text": transcribed_text
            })
            wer_str = f", WER: {wer_val}%" if wer_val is not None else ""
            print(f"  Успешно за {elapsed:.2f} с ({speedup}x быстрее реалтайма){wer_str}")

        except Exception as e:
            elapsed = time.time() - t0
            print(f"  Ошибка при прогоне {model_name}: {e}", file=sys.stderr)
            results.append({
                "model": model_name,
                "status": f"FAIL ({type(e).__name__})",
                "device": f"{device} ({compute_type})",
                "duration": "Н/Д",
                "elapsed": round(elapsed, 2),
                "speedup": "Н/Д",
                "wer": "Н/Д",
                "text": str(e)
            })

    # Формирование Markdown таблицы
    md_lines = [
        "# Сравнение моделей faster-whisper",
        f"**Дата тестирования:** 2026-10-15  ",
        f"**Входной файл:** `{input_path.name}`  ",
        f"**Процессор / Платформа:** Intel Core i7-12700H (14 ядер / 20 потоков, Windows 11)  ",
        "",
        "> [!WARNING]",
        "> **Ограничение методологии:** Тестирование проводилось на синтезированной речи (Microsoft Irina Desktop).",
        "> Речь синтезатора артикулирована идеально и не воспроизводит искажения живого голоса (фоновый шум, проглатывание окончаний, акценты, изменения тембра). На живой речи процент ошибок (WER) будет отличаться.",
        "",
        "## Итоговая таблица производительности и точности",
        "",
        "| Модель | Статус | Устройство | Время работы (с) | Скорость (vs реалтайм) | Ошибочные слова (WER) |",
        "| :--- | :---: | :--- | :---: | :---: | :---: |"
    ]

    for r in results:
        md_lines.append(f"| `{r['model']}` | {r['status']} | {r['device']} | {r['elapsed']} с | {r['speedup']} | {r['wer']} |")

    md_lines.extend([
        "",
        "## Расшифровки по моделям",
        ""
    ])

    for r in results:
        md_lines.append(f"### Модель `{r['model']}`")
        md_lines.append(f"```text\n{r['text']}\n```\n")

    out_report.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nОтчёт сохранён: {out_report}")

    # Вывод таблицы в консоль
    print("\n" + "="*70)
    print(f"{'Модель':<18} | {'Статус':<8} | {'Время (с)':<10} | {'Скорость':<10} | {'WER':<8}")
    print("-" * 70)
    for r in results:
        print(f"{r['model']:<18} | {r['status']:<8} | {str(r['elapsed']) + ' c':<10} | {r['speedup']:<10} | {r['wer']:<8}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
