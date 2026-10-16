@echo off
chcp 65001 >nul
set "PATH=%~dp0venv-whisper\Lib\site-packages\nvidia\cublas\bin;%~dp0venv-whisper\Lib\site-packages\nvidia\cudnn\bin;%~dp0venv-whisper\Lib\site-packages\nvidia\cuda_nvrtc\bin;%PATH%"
"%~dp0venv-whisper\Scripts\python.exe" "%~dp0transcribe.py" %*
