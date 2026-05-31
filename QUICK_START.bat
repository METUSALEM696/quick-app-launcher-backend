@echo off
:: =====================================================================
:: ONE-CLICK LAUNCHER - CLEAN EDITION
:: Large font, full screen, 3 browsers
:: =====================================================================

:: Request admin if needed
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Change to script directory
cd /d "%~dp0"

:: Set console to large size
mode con: cols=120 lines=40

:: Quick visual feedback
cls
echo.
echo ===============================================================================
echo.
echo                ONE-CLICK LAUNCHER - STARTING NOW!
echo.
echo ===============================================================================
echo.

:: Start server silently using Task Scheduler
echo [1/3] Starting server...
schtasks /Run /TN "FIRE_AND_FORGET_AUTOSTART" >nul 2>&1

:: Wait for server to initialize
echo [2/3] Initializing (5 seconds)...
timeout /t 5 /nobreak >nul

:: Open browsers (all 3!)
echo [3/3] Opening browsers...
start "" "http://localhost:8899/"
timeout /t 1 /nobreak >nul
start "" "file:///E:/script/Quick%%20App%%20Launcher/New%%20folder/Launcher_FINAL_WITH_SOUND.html"
timeout /t 1 /nobreak >nul
start "" "https://metusalem696.github.io/quick-app-launcher/"

:: Success message
echo.
echo ===============================================================================
echo   ALL DONE!
echo ===============================================================================
echo.
echo   Server: http://localhost:8899/
echo   Local Launcher: Opened in browser
echo   GitHub Pages Launcher: Opened in browser
echo.
echo   Closing this window in 3 seconds...
echo.

timeout /t 3 /nobreak >nul
exit /b