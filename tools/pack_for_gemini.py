# -*- coding: utf-8 -*-
"""
pack_for_gemini.py
Генератор единого файла базы знаний и исходных кодов для Gemini.
Создаёт на Рабочем столе файл AI_VIDEO_EDITING_FOR_GEMINI.txt
"""

import os
import sys
import datetime
from pathlib import Path

ROOT = Path(os.environ.get("ROOT", Path(__file__).resolve().parent.parent))

# Пути к Рабочему столу
desktop_paths = [
    Path(os.environ.get("USERPROFILE", "")) / "OneDrive" / "Рабочий стол",
    Path(os.environ.get("USERPROFILE", "")) / "Desktop"
]

target_dirs = [d for d in desktop_paths if d.exists()]
if not target_dirs:
    target_dirs = [Path(os.environ.get("USERPROFILE", "")) / "Desktop"]

# Расширения текстовых файлов
TEXT_EXTENSIONS = {
    ".md", ".py", ".bat", ".ps1", ".json", ".txt", ".patch",
    ".ts", ".tsx", ".mjs", ".js", ".css", ".html"
}

# Папки для пропуска
SKIP_PARTS = {
    "node_modules", ".git", "venv-whisper", "venv-autoeditor",
    "_archive", ".agents", "official-remotion-templates"
}


def is_text_file(p: Path) -> bool:
    if p.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    parts = p.relative_to(ROOT).parts
    for skip in SKIP_PARTS:
        if skip in parts:
            return False
    # Пропускаем большие бинарники если случайно попали
    if p.stat().st_size > 1024 * 1024 * 2: # > 2 MB
        return False
    return True


def collect_files():
    files = []
    for p in ROOT.rglob("*"):
        if p.is_file() and is_text_file(p):
            rel_path = p.relative_to(ROOT)
            files.append((str(rel_path).replace("\\", "/"), p))
    # Сортировка: сначала корень, потом по алфавиту
    files.sort(key=lambda x: (0 if "/" not in x[0] else 1, x[0]))
    return files


def generate_gemini_header(files):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    total_bytes = sum(p.stat().st_size for _, p in files)

    header = f"""# ================================================================================
# 🎬 AI-VIDEO-EDITING WORKSPACE: FULL KNOWLEDGE BASE & CODEBASE FOR GEMINI
# ================================================================================
# Дата генерации: {now}
# Корневая директория (ROOT): <ROOT>
# Операционная система: Windows 11 Pro 64-bit (AMD64)
# Аппаратная спецификация: Intel Core i7-12700H (14 ядер / 20 потоков), NVIDIA GeForce RTX 3060 Laptop (4 ГБ VRAM), 16 ГБ RAM
# Всего файлов в пакете: {len(files)}
# Общий размер исходного кода: {total_bytes / 1024:.1f} КБ (~{total_bytes / (1024*1024):.2f} МБ)
# ================================================================================

## ИНСТРУКЦИЯ ДЛЯ МОДЕЛИ GEMINI (РОЛЬ И КОНТЕКСТ)

Ты — главный AI-режиссёр монтажа, моушен-дизайнер на Remotion (React/TypeScript) и ведущий инженер автоматизации видеопайплайна (FFmpeg, Python, faster-whisper, auto-editor).
Перед тобой полная база знаний, правила, регламенты, скрипты автоматизации и исходные коды рабочей станции AI-Video-Editing.

### Ключевая концепция рабочей станции:
1. **Полная автономность и бесплатность:** Вся работа выполняется локально на ПК без платных подписок и облачных API.
2. **Стек технологий:**
   - **Remotion 4.0.535 (React 19, TypeScript):** Программный рендеринг вертикальных (9:16) и горизонтальных видео.
   - **faster-whisper 1.2.1 (CTranslate2):** Локальная транскрибация речи с генерацией пословных таймкодов (миллисекунды) для динамических караоке-субтитров. Поддерживает `--glossary` для имён и терминов.
   - **auto-editor 29.3.1:** Автоматическая нарезка тишины, вздохов и пауз из черновых видео.
   - **FFmpeg 9.0.2 & FFprobe:** Аудиофильтры, перекодирование, нарезка и технический контроль качества (QA).
   - **7 семейств шрифтов Google Fonts (OFL):** Montserrat, Manrope, Onest, Rubik, Oswald, Inter, Unbounded с 100% поддержкой кириллицы.

### Структура работы с клиентами (клиентский пайплайн):
Все клиентские проекты изолированы в директории `clients/<имя_клиента>/`:
- `brand/` — логотипы, цвета, фирменные шрифты.
- `raw/` — исходные видео со съёмки.
- `proxy/` — легковесные копии для быстрого предпросмотра.
- `work/` — транскрипты Whisper (`.txt`, `.srt`, `.json`), черновые файлы.
- `out/` — финальные отрендеренные ролики и отчёты QA.
- `brief.json` — параметры ролика (стиль, платформа, цвета, безопасные зоны).
- `glossary.txt` — спикеры, бренды и спецтермины для модели Whisper.
- `credits.md` — учёт лицензий ассетов.
- `revisions.md` — журнал правок.

### Типовой производственный процесс из 7 шагов:
1. Создать клиента: скопировать `clients/_template` в `clients/<имя_клиента>`.
2. Поместить исходник в `clients/<имя_клиента>/raw/video.mp4` и заполнить `brief.json`, `glossary.txt`.
3. Черновая нарезка тишины: `tools\\auto-editor.bat clients\\<клиент>\\raw\\video.mp4 --output clients\\<клиент>\\out\\cut.mp4`
4. Транскрибация: `tools\\transcribe.bat clients\\<клиент>\\out\\cut.mp4 --model base --output-dir clients\\<клиент>\\work --glossary clients\\<клиент>\\glossary.txt`
5. Монтаж в Remotion: перенести `cut.mp4` и `cut.json` в `projects/remotion-tiktok-starter/public/`, настроить анимацию и стили, предпросмотр `npm run dev`.
6. Рендеринг: `npx remotion render CaptionedVideo ..\\..\\clients\\<клиент>\\out\\final.mp4 --crf=18`
7. Контроль качества (QA): `tools\\qa.bat clients\\<клиент>\\out\\final.mp4 --platform tiktok`

### Главные регламенты в файлах:
- `CLAUDE.md` — стандарты кода, правила путей и команд.
- `hooks.md` — редакционные правила создания цепляющих и честных хуков (опора на реальные факты из материала, анализ всего транскрипта, запрет кликбейта с вырыванием из контекста).
- `style-guide.md` — визуальный стиль: типографика, безопасные зоны (Safe Zones) TikTok/Shorts/Reels, правила субтитров (максимум 2-3 слова на строку, без переноса предлогов).
- `qa-checklist.md` — чек-лист контроля: EBU R128 (-14 LUFS для TikTok/Shorts, True Peak <= -1.0 dBFS), 0 чёрных/зависших кадров, рассинхрон субтитров <= 80 мс.

# ================================================================================
## СОДЕРЖАНИЕ (РЕЕСТР ВСЕХ ВКЛЮЧЕННЫХ ФАЙЛОВ)
# ================================================================================
"""
    for i, (rel, p) in enumerate(files, 1):
        header += f"{i:3d}. [{p.stat().st_size:7d} B] {rel}\n"
    header += "# ================================================================================\n\n"
    return header


def pack_all():
    files = collect_files()
    print(f"Найдено {len(files)} текстовых файлов для упаковки.")

    content_parts = [generate_gemini_header(files)]

    for i, (rel, p) in enumerate(files, 1):
        size = p.stat().st_size
        print(f"[{i}/{len(files)}] Упаковка: {rel} ({size} B)")
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            text = f"<< Ошибка чтения файла: {e} >>"

        section = f"""
# ================================================================================
# FILE: {rel}
# SIZE: {size} bytes
# ================================================================================
{text}
"""
        content_parts.append(section)

    full_text = "".join(content_parts)

    saved_paths = []
    filename = "AI_VIDEO_EDITING_FOR_GEMINI.txt"

    for target_dir in set(target_dirs):
        target_dir.mkdir(parents=True, exist_ok=True)
        out_file = target_dir / filename
        out_file.write_text(full_text, encoding="utf-8")
        saved_paths.append(str(out_file))
        print(f"Успешно сохранён: {out_file} ({len(full_text.encode('utf-8')) / 1024:.1f} KB)")

    return saved_paths


if __name__ == "__main__":
    paths = pack_all()
    print("\nГотово! Файлы созданы:")
    for p in paths:
        print(f"  -> {p}")
