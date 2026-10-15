# -*- coding: utf-8 -*-
"""
setup_whisper.py — Идемпотентный скрипт создания и починки окружения faster-whisper.
"""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
VENV = TOOLS / "venv-whisper"
REQ_FILE = TOOLS / "requirements-whisper.txt"
PATCH_FILE = TOOLS / "patches" / "faster-whisper-audio.patch"

def run_cmd(args, check=True):
    print(f">> Running: {' '.join(str(a) for a in args)}")
    return subprocess.run(args, check=check)

def ensure_venv():
    py = VENV / "Scripts" / "python.exe"
    if not py.exists():
        print("Creating venv-whisper...")
        run_cmd(["py", "-3.12", "-m", "venv", str(VENV)])
    else:
        print("venv-whisper already exists.")

def install_deps():
    py = VENV / "Scripts" / "python.exe"
    # Check if packages are already importable
    test_import = subprocess.run([str(py), "-c", "import faster_whisper, av"], capture_output=True)
    if test_import.returncode == 0:
        print("Dependencies already satisfied (faster_whisper and av are installed).")
        return

    if REQ_FILE.exists():
        print(f"Installing requirements from {REQ_FILE}...")
        try:
            run_cmd([str(py), "-m", "pip", "install", "-r", str(REQ_FILE)])
        except subprocess.CalledProcessError as e:
            print(f"Warning: pip install encountered an issue: {e}")

def apply_patch():
    audio_py = VENV / "Lib" / "site-packages" / "faster_whisper" / "audio.py"
    if not audio_py.exists():
        print(f"Notice: faster_whisper not yet installed at {audio_py}")
        return

    content = audio_py.read_text(encoding="utf-8")
    target = 'with av.open(input_file, mode="r", metadata_errors="ignore") as container:'
    replacement = '''try:
        container = av.open(input_file, mode="r", metadata_errors="ignore")
    except TypeError:
        container = av.open(input_file, mode="r")
    with container:'''

    if replacement in content:
        print("Patch verified: faster_whisper/audio.py contains PyAV 14+ compatibility.")
    elif target in content:
        new_content = content.replace(target, replacement, 1)
        audio_py.write_text(new_content, encoding="utf-8")
        print("Successfully applied PyAV compatibility patch to faster_whisper/audio.py.")
    else:
        print("Notice: audio.py does not contain the target unpatched pattern.")

def main():
    ensure_venv()
    install_deps()
    apply_patch()
    print("setup_whisper completed successfully.")

if __name__ == "__main__":
    main()
