@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "ROOT=C:\Users\timur\Videos\AI-Video-Editing"
set "HAS_OUT="

for %%A in (%*) do (
    if "%%~A"=="--output" set HAS_OUT=1
    if "%%~A"=="-o" set HAS_OUT=1
)

if defined HAS_OUT (
    "%ROOT%\tools\venv-autoeditor\Scripts\auto-editor.exe" %*
) else (
    set "INFILE=%~1"
    set "NAME=%~n1"
    set "EXT=%~x1"
    if not exist "%ROOT%\clients\_demo\out" mkdir "%ROOT%\clients\_demo\out"
    "%ROOT%\tools\venv-autoeditor\Scripts\auto-editor.exe" %* --output "%ROOT%\clients\_demo\out\!NAME!_cut!EXT!"
)
