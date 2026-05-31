@echo off
REM ====================================================================
REM APLICARE RAPIDA - F3 pentru File Explorer
REM ====================================================================

color 0B
echo.
echo ====================================================================
echo   APLICARE MODIFICARE: F8 -^> F3
echo ====================================================================
echo.

set WORKDIR=E:\script\Quick App Launcher\New folder
set SCRIPT=%WORKDIR%\F2_Hotkey_Listener.py

REM ====================================================================
REM 1. VERIFICARE
REM ====================================================================

echo [1] Verificare script existent...
if not exist "%SCRIPT%" (
    color 0C
    echo [EROARE] Script nu gasit: %SCRIPT%
    pause
    exit /b 1
)
echo [OK] Script gasit
echo.

REM ====================================================================
REM 2. BACKUP
REM ====================================================================

echo [2] Creare backup...
copy "%SCRIPT%" "%SCRIPT%.BACKUP_F8" >nul
if %errorLevel% equ 0 (
    echo [OK] Backup creat: %SCRIPT%.BACKUP_F8
) else (
    color 0C
    echo [EROARE] Nu am putut crea backup!
    pause
    exit /b 1
)
echo.

REM ====================================================================
REM 3. VERIFICARE VERSIUNE
REM ====================================================================

echo [3] Verificare versiune...
findstr /C:"v2.3 DETACHED" "%SCRIPT%" >nul
if %errorLevel% neq 0 (
    color 0E
    echo [ATENTIE] Script-ul nu este v2.3 DETACHED!
    echo.
    echo Pentru rezultate optime, instaleaza v2.3 DETACHED mai intai!
    echo.
    set /p CONTINUE="Continui oricum? (Y/N): "
    if /i not "!CONTINUE!"=="Y" (
        echo Operatie anulata.
        pause
        exit /b 0
    )
)
echo.

REM ====================================================================
REM 4. OPRIRE LISTENER
REM ====================================================================

echo [4] Oprire listener...
schtasks /End /TN "F2_PYTHON_LISTENER" >nul 2>&1
timeout /t 2 >nul
taskkill /F /IM pythonw.exe >nul 2>&1
echo [OK] Listener oprit
echo.

REM ====================================================================
REM 5. MODIFICARE SCRIPT
REM ====================================================================

echo [5] Aplicare modificari...
echo.
echo Modificari aplicate:
echo   - Functie open_explorer: F8 -^> F3
echo   - Inregistrare hotkey: F8 -^> F3
echo   - Mesaje informative: F8 -^> F3
echo.

powershell -NoProfile -Command ^
    "$content = Get-Content '%SCRIPT%' -Raw; " ^
    "$content = $content -replace 'debounce_check\(\"F8\"\)', 'debounce_check(\"F3\")'; " ^
    "$content = $content -replace 'F8 APASAT', 'F3 APASAT'; " ^
    "$content = $content -replace 'F8_Explorer', 'F3_Explorer'; " ^
    "$content = $content -replace \"'f8', open_explorer\", \"'f3', open_explorer\"; " ^
    "$content = $content -replace 'F8  = File Explorer', 'F3  = File Explorer'; " ^
    "Set-Content '%SCRIPT%' -Value $content -Encoding UTF8"

if %errorLevel% equ 0 (
    echo [OK] Script modificat cu succes!
) else (
    color 0C
    echo [EROARE] Modificare esuata!
    echo.
    echo Restaurare backup...
    copy "%SCRIPT%.BACKUP_F8" "%SCRIPT%" >nul
    echo [INFO] Backup restaurat
    pause
    exit /b 1
)
echo.

REM ====================================================================
REM 6. PORNIRE LISTENER
REM ====================================================================

echo [6] Repornire listener...
schtasks /Run /TN "F2_PYTHON_LISTENER"
if %errorLevel% neq 0 (
    echo [ATENTIE] Task nu a pornit! Incearca manual:
    echo          schtasks /Run /TN "F2_PYTHON_LISTENER"
)

timeout /t 3 >nul
echo.

REM ====================================================================
REM 7. VERIFICARE
REM ====================================================================

echo [7] Verificare finala...
tasklist | find "pythonw.exe" >nul
if %errorLevel% equ 0 (
    color 0A
    echo [OK] Listener RULEAZA!
    echo.
    echo Verificare modificari:
    findstr /C:"F3 APASAT" "%SCRIPT%" >nul
    if %errorLevel% equ 0 (
        echo [OK] Modificare F3 aplicata corect!
    )
) else (
    color 0E
    echo [ATENTIE] Listener NU ruleaza!
    echo.
    echo Porneste manual:
    echo   schtasks /Run /TN "F2_PYTHON_LISTENER"
)
echo.

REM ====================================================================
REM SUCCESS
REM ====================================================================

color 0A
echo ====================================================================
echo   MODIFICARE APLICATA CU SUCCES!
echo ====================================================================
echo.
echo Hotkeys NOI:
echo   F2  = Fire and Forget Launcher
echo   F3  = File Explorer           ^<-- SCHIMBAT din F8!
echo   F9  = Control Panel
echo   F10 = Task Scheduler
echo   F11 = Task Manager
echo   F12 = Statistici
echo.
echo TEST: Apasa F3 pentru a deschide File Explorer!
echo.
echo Backup vechi: %SCRIPT%.BACKUP_F8
echo (Poti sterge backup-ul daca totul functioneaza OK)
echo.
echo ====================================================================
pause
