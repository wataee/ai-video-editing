import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    "node_modules",
    "references",
    "projects",
    "public",
    ".git",
    "dist",
    "build",
    ".next",
    ".remotion",
    "work",
    "out",
    "_archive",
    "_scratch",
    "_sandbox",
    "_tmp_download",
    "coverage",
    ".pytest_cache",
}

def is_excluded_dir(name: str) -> bool:
    if name in EXCLUDED_DIRS:
        return True
    if name.startswith("venv") or (name.startswith(".") and name != ".claude"):
        return True
    return False

TARGET_EXTENSIONS = {
    ".ts",
    ".tsx",
    ".js",
    ".mjs",
    ".json",
    ".css",
    ".jsx",
}

def is_comment_line(line: str, ext: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    if ext == ".json":
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*/"):
            return True
        if re.search(r'^\s*"//[^"]*"\s*:', stripped):
            return True
        return False

    if "/*" in stripped or "*/" in stripped:
        return True

    if "{/*" in stripped or "*/}" in stripped:
        return True

    sanitized = re.sub(r'https?://[^\s"\')]*', '', stripped)
    sanitized = re.sub(r'data:[^;\s]+;base64,', '', sanitized)
    sanitized = sanitized.replace(r'\/', '')
    if "//" in sanitized:
        return True

    return False

def check_file(file_path: Path) -> list[tuple[int, str]]:
    errors = []
    ext = file_path.suffix.lower()
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [(0, f"Cannot read file: {e}")]

    for line_idx, line in enumerate(content.splitlines(), start=1):
        if is_comment_line(line, ext):
            errors.append((line_idx, line.strip()))

    return errors

def main():
    all_errors = []
    scanned_count = 0

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not is_excluded_dir(d)]
        for f in files:
            path = Path(root) / f
            if path.suffix.lower() in TARGET_EXTENSIONS:
                scanned_count += 1
                errs = check_file(path)
                if errs:
                    for line_num, line_text in errs:
                        all_errors.append((path.relative_to(ROOT), line_num, line_text))

    print(f"Scanned {scanned_count} code files for forbidden comments...")

    if all_errors:
        print(f"\nFAILED: Found {len(all_errors)} lines with forbidden comments:\n", file=sys.stderr)
        for rel_path, line_num, line_text in all_errors:
            print(f"  {rel_path}:{line_num} -> {line_text}", file=sys.stderr)
        sys.exit(1)

    print("PASS: Zero comments found in .ts/.tsx/.js/.mjs/.json/.css/.jsx files.")
    sys.exit(0)

if __name__ == "__main__":
    main()
