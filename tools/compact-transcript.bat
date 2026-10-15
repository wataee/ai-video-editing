@echo off
set ROOT=%~dp0..
"%ROOT%\tools\venv-whisper\Scripts\python.exe" "%ROOT%\tools\compact_transcript.py" %*
