@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

:: --- Elevate to Admin if needed ---
net session >nul 2>&1
if %errorlevel% neq 0 (
  powershell -NoProfile -Command "Start-Process -FilePath 'cmd.exe' -ArgumentList '/c','\"%~f0\"' -Verb RunAs"
  exit /b
)

echo [OK] Running as Administrator
echo.

:: --- Pick server .py (priority order) ---
set "PY="
if exist "%~dp0server_fire_and_forget_FINAL_FIXED.py" set "PY=%~dp0server_fire_and_forget_FINAL_FIXED.py"
if not defined PY if exist "%~dp0server_fire_and_forget.py" set "PY=%~dp0server_fire_and_forget.py"
if not defined PY for %%F in ("%~dp0server*.py") do (set "PY=%%~fF" & goto :found)

:found
if not defined PY (
  echo [ERROR] Nu găsesc niciun server*.py în acest folder:
  echo %~dp0
  echo.
  dir /b "%~dp0*.py"
  pause
  exit /b 1
)

echo [INFO] Using: "%PY%"
echo.

python "%PY%"
echo.
echo [INFO] Server stopped.
pause
