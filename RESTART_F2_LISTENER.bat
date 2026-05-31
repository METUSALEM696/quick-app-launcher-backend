@echo off
chcp 65001 >nul
title Restart F2 Hotkey Listener
set "PYW=C:\Users\HERCULE SI DANIELA\AppData\Local\Programs\Python\Python313\pythonw.exe"
set "SCRIPT=P:\script\Quick App Launcher\New folder\F2_Hotkey_Listener.py"
set "WORKDIR=P:\script\Quick App Launcher\New folder"

echo Opreste instantele vechi (pythonw + F2_Hotkey_Listener)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process -Filter \"Name='pythonw.exe'\" | Where-Object { $_.CommandLine -like '*F2_Hotkey_Listener*' } | ForEach-Object { Write-Host ('Stop PID ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

timeout /t 2 /nobreak >nul

if not exist "%PYW%" (
  echo [EROARE] Nu gasesc pythonw. Editeaza PYW in acest fisier.
  pause
  exit /b 1
)

echo Pornesc listener nou...
start "" /D "%WORKDIR%" "%PYW%" "%SCRIPT%"
echo Gata. Incearca F2 dupa 2-3 secunde.
timeout /t 4
exit /b 0
