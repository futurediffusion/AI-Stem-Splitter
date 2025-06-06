@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0venv\Scripts\python.exe" (
    python -m venv "%~dp0venv"
    call "%~dp0venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

call "%~dp0venv\Scripts\activate"
python -m src.gui_app
pause
