# -*- coding: utf-8 -*-
import os
import sys
import shutil
import zipfile
import subprocess
import datetime
from pathlib import Path

ROOT = Path(os.environ.get("ROOT", Path(__file__).resolve().parent.parent))
ARCHIVE = ROOT / "_archive" / datetime.date.today().isoformat()
LOGS = ROOT / "logs"

ARCHIVE.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

# 1. Check claude
claude_path = shutil.which("claude")
claude_status = f"Найдена: {claude_path}" if claude_path else "НЕ найдена в PATH"
print(f"Claude CLI status: {claude_status}")

# 2. Backup zip
backup_zip_path = ARCHIVE / "backup.zip"
if backup_zip_path.exists():
    backup_zip_path.unlink()

include_exts = {".md", ".bat", ".py", ".ps1", ".json"}
exclude_dirs = {"node_modules", "references", ".git", "_archive"}

files_backed_up = []
with zipfile.ZipFile(backup_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        parts = rel.parts
        # check exclusions
        if any(ex in parts for ex in exclude_dirs):
            continue
        if any(part.startswith("venv") for part in parts):
            continue
        if p.suffix.lower() in include_exts:
            zf.write(p, arcname=str(rel))
            files_backed_up.append(str(rel))

zip_size = backup_zip_path.stat().st_size
print(f"Backup created: {backup_zip_path} ({zip_size} bytes, {len(files_backed_up)} files)")

# 3. Folder sizes
top_folders = [d for d in ROOT.iterdir() if d.is_dir()]
folder_stats = []
for d in sorted(top_folders):
    total_size = 0
    total_files = 0
    for f in d.rglob("*"):
        if f.is_file():
            try:
                total_size += f.stat().st_size
                total_files += 1
            except OSError:
                pass
    folder_stats.append((d.name, round(total_size / (1024 * 1024), 2), total_files))

# 4. Assets inventory
assets_dir = ROOT / "assets"
assets_files = []
if assets_dir.exists():
    for f in sorted(assets_dir.rglob("*")):
        if f.is_file():
            assets_files.append((str(f.relative_to(ROOT)), f.stat().st_size))

# 5. Tree up to depth 3 (excluding node_modules, venv, .git)
def build_tree(current_dir, depth=0, max_depth=3):
    lines = []
    if depth >= max_depth:
        return lines
    try:
        entries = sorted(list(current_dir.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
    except OSError:
        return lines

    for entry in entries:
        if entry.name in {"node_modules", ".git"} or entry.name.startswith("venv"):
            continue
        indent = "  " * depth
        if entry.is_dir():
            lines.append(f"{indent}├── {entry.name}/")
            lines.extend(build_tree(entry, depth + 1, max_depth))
        else:
            try:
                size = entry.stat().st_size
            except OSError:
                size = 0
            lines.append(f"{indent}├── {entry.name} ({size} B)")
    return lines

tree_lines = build_tree(ROOT, depth=0, max_depth=3)

# 6. Save inventory-before.md
inventory_path = LOGS / "inventory-before.md"
with open(inventory_path, "w", encoding="utf-8") as out:
    out.write("# Инвентаризация рабочей среды до начала очистки\n")
    out.write(f"**Дата:** 2026-10-15  \n**Корневая папка:** `{ROOT}`\n\n")
    out.write(f"## 1. Наличие команды Claude CLI\n- Статус команды `claude`: **{claude_status}**\n\n")
    out.write("## 2. Размеры верхних папок\n")
    out.write("| Папка | Размер (МБ) | Кол-во файлов |\n| :--- | :--- | :--- |\n")
    for name, size_mb, count in folder_stats:
        out.write(f"| `{name}` | {size_mb} MB | {count} |\n")
    out.write("\n## 3. Содержимое папки assets\\\n")
    out.write(f"Всего файлов: {len(assets_files)}\n\n")
    if not assets_files:
        out.write("*Файлы в assets\\ отсутствуют (подпапки пустые).*\n\n")
    else:
        out.write("| Файл | Размер (байт) |\n| :--- | :--- |\n")
        for rel_p, sz in assets_files:
            out.write(f"| `{rel_p}` | {sz} B |\n")
        out.write("\n")
    out.write("## 4. Дерево директорий (до глубины 3, без node_modules, venv, .git)\n```text\n")
    out.write("\n".join(tree_lines))
    out.write("\n```\n")

print(f"Inventory saved: {inventory_path}")
