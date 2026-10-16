#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_paths.py — Валидатор путей в документации и коде.
Сканирует CLAUDE.md, README.md, .claude/rulebooks/*.md, .claude/skills/**/*.md
и проверяет реальное существование упомянутых локальных путей на диске.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Целевые файлы для проверки
TARGET_PATTERNS = [
    "CLAUDE.md",
    "README.md",
    ".claude/rulebooks/**/*.md",
    ".claude/skills/**/*.md",
    ".claude/design-system/**/*.md",
]

# Регулярное выражение для поиска путей в репозитории
# Ищет пути вида: assets/..., tools/..., scripts/..., docs/..., clients/..., src/..., references/..., templates/..., .claude/...
PATH_REGEX = re.compile(
    r'(?:[`"\'\(\[\s]|^)'
    r'('
    r'(?:assets|tools|scripts|docs|clients|src|references|templates|\.claude|work|out)'
    r'[\\/][A-Za-z0-9_\-\.\/\\*]+'
    r')'
    r'(?:[`"\'\)\]\s:,\.]|$)'
)

# Исключения (плейсхолдеры, расширения масок, внешние или генерируемые шаблоны)
IGNORE_EXACT = {
    "assets/02_FONTS",
    "assets/01_SFX",
}

def should_ignore(path_str: str) -> bool:
    clean = path_str.replace("\\", "/").rstrip("/.")
    if clean in IGNORE_EXACT:
        return False  # Do not ignore these, we want to catch legacy bad paths!
    
    # Плейсхолдеры в документации (e.g. <client>, <style>, <slug>, *.mp4, [Composition], {CLIENT})
    if any(token in clean for token in ["<", ">", "[", "]", "*", "...", "{", "}"]):
        return True
    
    # Шаблоны в примерах команд (например path/to/raw_video.MOV, C1612_*.mp4)
    if "path/to" in clean or clean.endswith(".MOV") and "raw_video" in clean:
        return True
    
    # Виртуальные или динамически генерируемые артефакты при рендере
    if any(clean.startswith(prefix) for prefix in [
        "work/ingest", "work/transcribe", "work/cut", "work/plan", "work/audio", "work/templates",
        "clients/", "out/"
    ]):
        return True
        
    return False

def check_file(file_path: Path) -> list[dict]:
    errors = []
    if not file_path.exists():
        return [{"file": str(file_path), "line": 0, "path": str(file_path), "reason": "Target file does not exist"}]

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [{"file": str(file_path), "line": 0, "path": "", "reason": f"Cannot read: {e}"}]

    for line_idx, line in enumerate(content.splitlines(), start=1):
        for match in PATH_REGEX.finditer(line):
            raw_path = match.group(1).strip()
            # Очистим хвостовые знаки пунктуации
            cleaned = re.sub(r'[\.,:;]+$', '', raw_path).strip()
            if not cleaned or should_ignore(cleaned):
                continue
            
            # Проверяем существование файла или директории
            normalized = cleaned.replace("\\", "/")
            target = (ROOT / normalized).resolve()
            
            if not target.exists():
                errors.append({
                    "file": str(file_path.relative_to(ROOT)),
                    "line": line_idx,
                    "path": cleaned,
                    "reason": f"Path not found: {cleaned}"
                })

    return errors

def main():
    target_files = []
    for pat in TARGET_PATTERNS:
        if "*" in pat:
            target_files.extend(ROOT.glob(pat))
        else:
            p = ROOT / pat
            if p.exists():
                target_files.append(p)

    target_files = sorted(set(f for f in target_files if f.is_file()))
    all_errors = []

    print(f"Scanning {len(target_files)} files for path integrity against ROOT={ROOT}...\n")

    for f in target_files:
        errs = check_file(f)
        if errs:
            all_errors.extend(errs)

    if all_errors:
        print(f"FAILED: Found {len(all_errors)} broken or outdated path references:\n")
        for err in all_errors:
            print(f"  {err['file']}:{err['line']} -> {err['path']}")
        print(f"\nPlease fix the paths above.")
        sys.exit(1)
    else:
        print("PASS: All referenced paths exist.")
        sys.exit(0)

if __name__ == "__main__":
    main()
