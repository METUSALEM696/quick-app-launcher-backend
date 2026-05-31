@echo off
setlocal enabledelayedexpansion
:: =====================================================================
:: TEMPLATE UNIVERSAL TASK SCHEDULER - FIRE AND FORGET LAUNCHER
:: =====================================================================
:: Versiune cu MULTI-TRIGGER si RESTART SERVER
:: =====================================================================

:: =====================================================================
:: CONFIGURATIE PERSONALIZABILA - PATH-URI FIRE AND FORGET
:: =====================================================================

:: =====================================================================
:: CONFIGURATIE PERSONALIZABILA - PATH-URI FIRE AND FORGET
:: =====================================================================

:: DETALII TASK:
set TASK_NAME=FIRE_AND_FORGET_AUTOSTART
set TASK_DESCRIPTION=Fire and Forget Launcher - Server HTTP pentru quick app launcher

:: PROGRAMUL DE RULAT (Python DIRECT - fara wrapper):
:: PYTHON DIRECT (FARA WRAPPER VBS!):
set PROGRAM_EXE=C:\Users\HERCULE SI DANIELA\AppData\Local\Programs\Python\Python313\pythonw.exe
:: Trebuie sa coincida cu discul/folderul real al proiectului (verifica cu explorer sau Test-Path).
set PROGRAM_ARGS="E:\script\Quick App Launcher\New folder\server_fire_and_forget.py"
set WORKING_DIR=E:\script\Quick App Launcher\New folder

:: =====================================================================
:: TRIGGER-E MULTIPLE - ACTIVEAZA CE VREI (true/false)
:: =====================================================================
set ENABLE_LOGON_TRIGGER=true
:: Boot + Logon pot rula amândouă la login → același script de 2 ori → tab-uri duplicate. Lasă doar Logon.
set ENABLE_BOOT_TRIGGER=false
set ENABLE_DAILY_TRIGGER=false
set DAILY_TIME=09:00

:: SETARI AVANSATE:
set DELAY_SECONDS=15
set RUN_LEVEL=LeastPrivilege
set ALLOW_ON_BATTERY=true
set STOP_ON_BATTERY=false
set WAKE_TO_RUN=false
set PRIORITY=4

:: =====================================================================
:: NU MODIFICA SUB ACEASTA LINIE - MOTOR UNIVERSAL TASK SCHEDULER
:: =====================================================================

:MAIN_MENU
cls
title Fire and Forget - Task Scheduler Manager
echo.
echo =====================================================================
echo   FIRE AND FORGET - TASK SCHEDULER MANAGER
echo =====================================================================
echo.
echo [1] CREAZA/ACTUALIZEAZA TASK-UL
echo [2] PORNESTE SERVERUL ACUM
echo [3] OPRESTE SERVERUL
echo [4] RESTART COMPLET SERVER (Stop + Start)
echo [5] VERIFICA STATUS SERVER
echo [6] STERGE TASK-UL
echo [7] DESCHIDE TASK SCHEDULER
echo [8] TEST CONEXIUNE HTTP
echo [0] IESIRE
echo.
echo =====================================================================
set /p choice="Alege optiunea (0-8): "

if "%choice%"=="1" goto CREATE_TASK
if "%choice%"=="2" goto START_SERVER
if "%choice%"=="3" goto STOP_SERVER
if "%choice%"=="4" goto RESTART_SERVER
if "%choice%"=="5" goto CHECK_STATUS
if "%choice%"=="6" goto DELETE_TASK
if "%choice%"=="7" goto OPEN_SCHEDULER
if "%choice%"=="8" goto TEST_HTTP
if "%choice%"=="0" exit /b 0
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: CREAZA/ACTUALIZEAZA TASK-UL
:: =====================================================================
:CREATE_TASK
cls
echo.
echo =====================================================================
echo   CREATOR UNIVERSAL TASK SCHEDULER - FIRE AND FORGET
echo =====================================================================
echo.
echo [INFO] Creez taskul: %TASK_NAME%
echo [INFO] Program: %PROGRAM_EXE%
echo [INFO] Argumente: %PROGRAM_ARGS%
echo [INFO] Working Directory: %WORKING_DIR%
echo [INFO] Descriere: %TASK_DESCRIPTION%
echo.

set XML_PATH=%TEMP%\%TASK_NAME%_task.xml

:: Verifica privilegi administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [X] EROARE: Script-ul necesita privilegi de administrator!
    echo [!] Solutie: Click dreapta pe script si selecteaza "Run as administrator"
    echo.
    pause
    goto MAIN_MENU
)
echo [OK] Privilegi administrator: OK

:: Verifica daca Python pentru background exista
pythonw --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [X] EROARE: Python nu a fost gasit in sistem!
        echo [!] Solutie: Instaleaza Python sau verifica instalarea
        pause
        goto MAIN_MENU
    ) else (
        echo [OK] Python gasit! (pythonw va rula invizibil)
    )
) else (
    echo [OK] Python pentru background gasit!
)

:: Verifica scriptul Python
set SCRIPT_PATH=%PROGRAM_ARGS:"=%
if not exist "%SCRIPT_PATH%" (
    echo [X] EROARE: Scriptul Python nu a fost gasit la:
    echo    %SCRIPT_PATH%
    echo.
    echo [!] Solutie: Verifica ca scriptul server_fire_and_forget.py exista
    echo.
    pause
    goto MAIN_MENU
) else (
    echo [OK] Script Python gasit!
)

:: Verifica working directory
if not exist "%WORKING_DIR%" (
    echo [X] EROARE: Working directory nu exista:
    echo    %WORKING_DIR%
    echo.
    echo [!] Solutie: Verifica si corecteaza calea in sectiunea CONFIGURATIE
    echo.
    pause
    goto MAIN_MENU
) else (
    echo [OK] Working directory gasit!
)

echo.
echo Generez configuratia XML pentru task...

:: Creaza fisierul XML pentru task
(
echo ^<?xml version="1.0" encoding="UTF-16"?^>
echo ^<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^>
echo   ^<RegistrationInfo^>
echo     ^<Date^>2024-01-01T12:00:00^</Date^>
echo     ^<Author^>%USERNAME%^</Author^>
echo     ^<Description^>%TASK_DESCRIPTION%^</Description^>
echo   ^</RegistrationInfo^>
echo   ^<Triggers^>
) > "%XML_PATH%"

:: Contorizeaza trigger-ele active
set ACTIVE_TRIGGERS=0

:: Adauga trigger-ul de logon daca este activat
if /i "%ENABLE_LOGON_TRIGGER%"=="true" (
    echo [OK] Trigger ACTIV: La logarea utilizatorului (+%DELAY_SECONDS%s)
    set /a ACTIVE_TRIGGERS+=1
    (
    echo     ^<LogonTrigger^>
    echo       ^<Enabled^>true^</Enabled^>
    echo       ^<UserId^>%USERDOMAIN%\%USERNAME%^</UserId^>
    echo       ^<Delay^>PT%DELAY_SECONDS%S^</Delay^>
    echo     ^</LogonTrigger^>
    ) >> "%XML_PATH%"
)

:: Adauga trigger-ul de boot daca este activat
if /i "%ENABLE_BOOT_TRIGGER%"=="true" (
    echo [OK] Trigger ACTIV: La pornirea Windows (+%DELAY_SECONDS%s)
    set /a ACTIVE_TRIGGERS+=1
    (
    echo     ^<BootTrigger^>
    echo       ^<Enabled^>true^</Enabled^>
    echo       ^<Delay^>PT%DELAY_SECONDS%S^</Delay^>
    echo     ^</BootTrigger^>
    ) >> "%XML_PATH%"
)

:: Adauga trigger zilnic daca este activat
if /i "%ENABLE_DAILY_TRIGGER%"=="true" (
    echo [OK] Trigger ACTIV: Zilnic la %DAILY_TIME%
    set /a ACTIVE_TRIGGERS+=1
    (
    echo     ^<CalendarTrigger^>
    echo       ^<StartBoundary^>2024-01-01T%DAILY_TIME%:00^</StartBoundary^>
    echo       ^<Enabled^>true^</Enabled^>
    echo       ^<ScheduleByDay^>
    echo         ^<DaysInterval^>1^</DaysInterval^>
    echo       ^</ScheduleByDay^>
    echo     ^</CalendarTrigger^>
    ) >> "%XML_PATH%"
)

:: Verifica daca exista cel putin un trigger activ
if %ACTIVE_TRIGGERS% equ 0 (
    color 0E
    echo.
    echo [!] ATENTIE: Nici un trigger nu este activat!
    echo [!] Activeaza cel putin un trigger in sectiunea CONFIGURATIE
    echo.
    pause
    goto MAIN_MENU
)

echo [INFO] Total trigger-e active: %ACTIVE_TRIGGERS%

:: Continua cu restul configuratiei XML
(
echo   ^</Triggers^>
echo   ^<Principals^>
echo     ^<Principal id="Author"^>
echo       ^<UserId^>%USERDOMAIN%\%USERNAME%^</UserId^>
echo       ^<LogonType^>InteractiveToken^</LogonType^>
echo       ^<RunLevel^>%RUN_LEVEL%^</RunLevel^>
echo     ^</Principal^>
echo   ^</Principals^>
echo   ^<Settings^>
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^>
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^>
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^>
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^>
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^>
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^>
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^>
echo     ^<Enabled^>true^</Enabled^>
echo     ^<Hidden^>true^</Hidden^>
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^>
echo     ^<DisallowStartOnRemoteAppSession^>false^</DisallowStartOnRemoteAppSession^>
echo     ^<UseUnifiedSchedulingEngine^>true^</UseUnifiedSchedulingEngine^>
echo     ^<WakeToRun^>false^</WakeToRun^>
echo     ^<ExecutionTimeLimit^>PT0S^</ExecutionTimeLimit^>
echo     ^<Priority^>%PRIORITY%^</Priority^>
echo     ^<RestartOnFailure^>
echo       ^<Interval^>PT1M^</Interval^>
echo       ^<Count^>3^</Count^>
echo     ^</RestartOnFailure^>
echo   ^</Settings^>

echo   ^<Actions Context="Author"^>
echo     ^<Exec^>
echo       ^<Command^>%PROGRAM_EXE%^</Command^>
echo       ^<Arguments^>%PROGRAM_ARGS%^</Arguments^>
echo       ^<WorkingDirectory^>%WORKING_DIR%^</WorkingDirectory^>
echo     ^</Exec^>
echo   ^</Actions^>
echo ^</Task^>
) >> "%XML_PATH%"

echo.
echo Sterg taskul existent (daca exista)...
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

echo Creez noul task in Windows Task Scheduler...
schtasks /Create /TN "%TASK_NAME%" /XML "%XML_PATH%" /F

:: Verifica daca task-ul a fost creat cu succes
if !errorlevel! equ 0 (
    color 0A
    echo.
    echo =====================================================================
    echo   [SUCCES] TASK CREAT CU SUCCES!
    echo =====================================================================
    echo.
    echo [INFO] Nume task:        %TASK_NAME%
    echo [INFO] Program:          %PROGRAM_EXE%
    echo [INFO] Working Dir:      %WORKING_DIR%
    echo [INFO] Trigger-e active: %ACTIVE_TRIGGERS%
    echo [INFO] Intarziere:       %DELAY_SECONDS% secunde
    echo.
    echo [TRIGGER-E CONFIGURATE]
    if /i "%ENABLE_LOGON_TRIGGER%"=="true" echo   [X] La logarea utilizatorului (+%DELAY_SECONDS%s)
    if /i "%ENABLE_BOOT_TRIGGER%"=="true" echo   [X] La pornirea Windows (+%DELAY_SECONDS%s)
    if /i "%ENABLE_DAILY_TRIGGER%"=="true" echo   [X] Zilnic la %DAILY_TIME%
    echo.
    
    :: Curata fisierul XML temporar
    del "%XML_PATH%" >nul 2>&1
    
    echo Pornesc task-ul automat...
    timeout /t 2 >nul
    goto START_SERVER
) else (
    color 0C
    echo.
    echo [X] EROARE la crearea taskului!
    echo Cod eroare: !errorlevel!
    echo [!] Incearca sa rulezi ca Administrator
    echo.
    del "%XML_PATH%" >nul 2>&1
    pause
    goto MAIN_MENU
)

:: =====================================================================
:: FUNCTIE: PORNESTE SERVERUL
:: =====================================================================
:START_SERVER
cls
echo.
echo =====================================================================
echo   PORNIRE SERVER
echo =====================================================================
echo.

:: Verifica daca task-ul exista
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if !errorlevel! neq 0 (
    color 0E
    echo [!] Task-ul nu exista! Trebuie sa-l creezi mai intai.
    echo.
    pause
    goto MAIN_MENU
)

echo [INFO] Pornesc task-ul: %TASK_NAME%
schtasks /Run /TN "%TASK_NAME%"

if !errorlevel! equ 0 (
    echo [OK] Task-ul a fost pornit!
    echo [INFO] Astept 8 secunde pentru incarcare server...
    
    :: Progres bar
    for /L %%i in (1,1,8) do (
        echo|set /p="."
        timeout /t 1 >nul
    )
    echo.
    echo.
    
    :: Verifica daca serverul ruleaza
    netstat -an | findstr ":8899" | findstr "LISTENING" >nul 2>&1
    if !errorlevel! equ 0 (
        color 0A
        echo =====================================================================
        echo   [PERFECT] SERVERUL ESTE ACTIV!
        echo =====================================================================
        echo.
        echo [OK] Server HTTP: ACTIV pe portul 8899
        echo [OK] Process: pythonw.exe ruleaza invizibil
        echo.
        echo [ACCES RAPID]
        echo   Browser: http://localhost:8899/
        echo   Ping: http://localhost:8899/ping
        echo.
        echo [INFO] Deschid browser automat...
        start http://localhost:8899/
        echo.
    ) else (
        color 0E
        echo [!] Task pornit, dar serverul nu raspunde
        echo [!] Posibile probleme: module Python, sintaxa, port ocupat
        echo.
    )
) else (
    color 0C
    echo [X] Eroare la pornirea task-ului!
)

pause
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: OPRESTE SERVERUL
:: =====================================================================
:STOP_SERVER
cls
echo.
echo =====================================================================
echo   OPRIRE SERVER
echo =====================================================================
echo.

echo [INFO] Opresc procesele pythonw.exe...
taskkill /F /IM pythonw.exe >nul 2>&1

if !errorlevel! equ 0 (
    color 0A
    echo [OK] Serverul a fost oprit cu succes!
) else (
    color 0E
    echo [!] Nu exista procese pythonw.exe active
)

echo.
pause
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: RESTART COMPLET SERVER
:: =====================================================================
:RESTART_SERVER
cls
echo.
echo =====================================================================
echo   RESTART COMPLET SERVER
echo =====================================================================
echo.

echo [STEP 1/3] Opresc serverul actual...
taskkill /F /IM pythonw.exe >nul 2>&1
echo [OK] Procese pythonw.exe terminate

echo.
echo [STEP 2/3] Astept 3 secunde pentru cleanup...
timeout /t 3 >nul

echo.
echo [STEP 3/3] Pornesc serverul din nou...
schtasks /Run /TN "%TASK_NAME%" >nul 2>&1

if !errorlevel! equ 0 (
    echo [OK] Task-ul a fost repornit
    echo [INFO] Astept 8 secunde pentru incarcare...
    
    for /L %%i in (1,1,8) do (
        echo|set /p="."
        timeout /t 1 >nul
    )
    echo.
    echo.
    
    netstat -an | findstr ":8899" | findstr "LISTENING" >nul 2>&1
    if !errorlevel! equ 0 (
        color 0A
        echo =====================================================================
        echo   [SUCCES] RESTART COMPLET!
        echo =====================================================================
        echo.
        echo [OK] Server repornit si functional pe portul 8899
        echo.
        echo [INFO] Deschid browser automat...
        start http://localhost:8899/
        echo.
    ) else (
        color 0E
        echo [!] Server repornit, dar nu raspunde inca
    )
) else (
    color 0C
    echo [X] Eroare la repornirea serverului!
)

pause
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: VERIFICA STATUS
:: =====================================================================
:CHECK_STATUS
cls
echo.
echo =====================================================================
echo   STATUS SERVER
echo =====================================================================
echo.

:: Verifica task-ul
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Task exists: %TASK_NAME%
    schtasks /Query /TN "%TASK_NAME%" /FO LIST /V | findstr "Status:"
) else (
    echo [X] Task-ul nu exista in Task Scheduler
)

echo.

:: Verifica procesul pythonw.exe
tasklist | findstr "pythonw.exe" >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Proces pythonw.exe: RUNNING
    tasklist | findstr "pythonw.exe"
) else (
    echo [X] Proces pythonw.exe: NU RULEAZA
)

echo.

:: Verifica portul HTTP
netstat -an | findstr ":8899" | findstr "LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Server HTTP: LISTENING pe portul 8899
    netstat -an | findstr ":8899"
) else (
    echo [X] Server HTTP: NU ESTE ACTIV pe portul 8899
)

echo.
echo =====================================================================
pause
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: STERGE TASK-UL
:: =====================================================================
:DELETE_TASK
cls
echo.
echo =====================================================================
echo   STERGERE TASK
echo =====================================================================
echo.

set /p confirm="Esti sigur ca vrei sa stergi task-ul? (Y/N): "
if /i not "%confirm%"=="Y" goto MAIN_MENU

echo.
echo [INFO] Opresc procesele pythonw.exe...
taskkill /F /IM pythonw.exe >nul 2>&1

echo [INFO] Sterg task-ul: %TASK_NAME%
schtasks /Delete /TN "%TASK_NAME%" /F

if !errorlevel! equ 0 (
    color 0A
    echo [OK] Task-ul a fost sters cu succes!
) else (
    color 0C
    echo [X] Eroare la stergerea task-ului!
)

pause
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: DESCHIDE TASK SCHEDULER
:: =====================================================================
:OPEN_SCHEDULER
start taskschd.msc
goto MAIN_MENU

:: =====================================================================
:: FUNCTIE: TEST CONEXIUNE HTTP
:: =====================================================================
:TEST_HTTP
cls
echo.
echo =====================================================================
echo   TEST CONEXIUNE HTTP
echo =====================================================================
echo.

echo [INFO] Deschid browser cu launcher-ul...
start http://localhost:8899/

echo.
echo [INFO] Test ping endpoint...
curl -s http://localhost:8899/ping >nul 2>&1
if !errorlevel! equ 0 (
    color 0A
    echo [OK] Server raspunde la ping!
) else (
    color 0E
    echo [X] Server nu raspunde!
)

pause
goto MAIN_MENU