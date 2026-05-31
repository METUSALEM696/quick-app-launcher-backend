@echo off
echo.
echo ========================================
echo   PORNESC SISTEM F2 RESTART
echo ========================================
echo.

echo [1/2] Pornesc F2 Listener...
schtasks /Run /TN "F2_PYTHON_LISTENER"

if %errorLevel% equ 0 (
    echo [OK] F2 Listener pornit
) else (
    echo [X] EROARE la pornire F2 Listener
    pause
    exit /b 1
)

echo Astept 3 secunde...
timeout /t 3 >nul

echo.
echo [2/2] Pornesc Server HTTP...
schtasks /Run /TN "FIRE_AND_FORGET_AUTOSTART"

if %errorLevel% equ 0 (
    echo [OK] Server pornit
) else (
    echo [X] EROARE la pornire Server
    pause
    exit /b 1
)

echo Astept 8 secunde ca serverul sa porneasca complet...
timeout /t 8 >nul

echo.
echo ========================================
echo   VERIFICARE
echo ========================================
echo.

echo Verific pythonw.exe...
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I "pythonw.exe" >NUL
if %errorLevel% equ 0 (
    echo [OK] pythonw.exe ruleaza:
    tasklist /FI "IMAGENAME eq pythonw.exe"
) else (
    echo [X] pythonw.exe NU ruleaza!
)

echo.
echo Verific server HTTP pe 8899...
netstat -an | findstr ":8899" | findstr "LISTENING" >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Server HTTP activ pe portul 8899
    echo.
    echo Deschid browser-ul...
    start http://localhost:8899/
) else (
    echo [X] Server HTTP NU raspunde pe 8899!
)

echo.
echo ========================================
echo   GATA!
echo ========================================
echo.
echo TESTEAZA ACUM:
echo   - Apasa F2 de oriunde
echo   - Browser-ul se deschide in 8-10 secunde
echo.
pause