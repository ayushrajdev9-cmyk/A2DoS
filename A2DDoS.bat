@echo off
if exist "%~dp0A2DDoS.exe" (
    "%~dp0A2DDoS.exe" %*
) else if exist "%~dp0A2DDoS.py" (
    python "%~dp0A2DDoS.py" %*
) else (
    echo Error: A2DDoS.exe or A2DDoS.py not found
    pause
)
if "%*"=="" pause
