@echo off
set ROOT=%~dp0..
"%ROOT%\tools\venv-whisper\Scripts\python.exe" "%ROOT%\tools\slice_words_json.py" %*
