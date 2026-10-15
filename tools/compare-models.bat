@echo off
chcp 65001 >nul
"%~dp0venv-whisper\Scripts\python.exe" "%~dp0compare_models.py" %*
