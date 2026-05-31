# task_manager_fire_and_forget.py
# ✅ Task Scheduler Manager (Python) pentru Fire & Forget Launcher
# ✅ UI frumos: culori + emoji (Rich optional)
# ✅ AUTO-UAC: se relansează singur ca Administrator când e nevoie (Create/Delete)
# ✅ Fallback NO-ADMIN: dacă refuzi UAC, încearcă să creeze un task simplu (Logon only) în unele sisteme
# ✅ Start / Stop / Restart / Status / Test HTTP / Open Task Scheduler
#
# Rulare:
#   python task_manager_fire_and_forget.py
#
# Notă:
#   - Rich este OPTIONAL. Dacă nu e instalat, scriptul merge și fără el.
#   - Pentru BOOT trigger (la pornirea Windows) și pentru setări avansate, Admin este normal să fie necesar.

from __future__ import annotations

import ctypes
import datetime as _dt
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from xml.sax.saxutils import escape as _xml_escape

# =========================
# CONFIG (editează aici)
# =========================

@dataclass(frozen=True)
class Config:
    # Task details
    task_name: str = "FIRE_AND_FORGET_AUTOSTART"
    task_description: str = "Fire and Forget Launcher - Server HTTP pentru quick app launcher"

    # Program to run (pythonw recommended for invisible)
    program_exe: str = r"C:\Users\HERCULE SI DANIELA\AppData\Local\Programs\Python\Python313\pythonw.exe"
    script_path: str = r"E:\script\Quick App Launcher\New folder\server_fire_and_forget.py"
    working_dir: str = r"E:\script\Quick App Launcher\New folder"

    # Triggers
    enable_logon_trigger: bool = True
    enable_boot_trigger: bool = True
    enable_daily_trigger: bool = False
    daily_time: str = "09:00"  # HH:MM (24h)

    # Advanced
    delay_seconds: int = 15
    run_level: str = "LeastPrivilege"  # "LeastPrivilege" or "HighestAvailable"
    allow_on_battery: bool = True
    stop_on_battery: bool = False
    wake_to_run: bool = False
    priority: int = 4  # 0..10 (Task Scheduler)

    # Server checks
    server_port: int = 8899
    ping_url: str = "http://localhost:8899/ping"
    home_url: str = "http://localhost:8899/"

CFG = Config()

# =========================
# UI (Rich optional)
# =========================

RICH = False
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.text import Text
    from rich import box

    console = Console()
    RICH = True
except Exception:
    console = None  # type: ignore


def cprint(msg: str, style: str = "") -> None:
    if RICH:
        console.print(msg, style=style)  # type: ignore
    else:
        print(msg)


def header(title: str) -> None:
    if RICH:
        console.clear()  # type: ignore
        console.print(Panel.fit(f"🚀 {title}", border_style="cyan"))  # type: ignore
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 70)
        print(f"  {title}")
        print("=" * 70)


def pause(msg: str = "Apasă ENTER pentru a continua...") -> None:
    try:
        input(msg)
    except KeyboardInterrupt:
        pass


def prompt_choice(prompt_text: str) -> str:
    if RICH:
        return Prompt.ask(prompt_text)  # type: ignore
    return input(prompt_text)


# =========================
# Privileges (AUTO-UAC)
# =========================

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def relaunch_as_admin(reason: str = "") -> bool:
    if is_admin():
        return True

    # folosim python.exe (cu consolă), nu pythonw.exe
    py = sys.executable
    try:
        p = Path(py)
        if p.name.lower() == "pythonw.exe":
            cand = p.with_name("python.exe")
            if cand.exists():
                py = str(cand)
    except Exception:
        pass

    args = " ".join([f'"{a}"' for a in sys.argv])

    cmd = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "System32", "cmd.exe")
    cmd_params = f'/k ""{py}" {args}"'

    # mesaj scurt ca să știi unde să te uiți
    try:
        ctypes.windll.user32.MessageBoxW(
            None,
            "Se va deschide o fereastră nouă CMD ca Administrator.\nInstanța curentă se va închide.",
            "Elevare Admin",
            0x40
        )
    except Exception:
        pass

    rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", cmd, cmd_params, None, 1)
    if rc <= 32:
        cprint("UAC refuzat / eroare la elevare.", style="bold yellow" if RICH else "")
        pause()
        return False

    sys.exit(0)




# =========================
# Helpers
# =========================

def run_cmd(cmd: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        shell=False,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def run_cmd_shell(cmd: str, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def normalize_time_hhmm(s: str) -> str:
    s = s.strip()
    parts = s.split(":")
    if len(parts) != 2:
        raise ValueError("Format invalid. Folosește HH:MM")
    hh = int(parts[0])
    mm = int(parts[1])
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        raise ValueError("Oră invalidă.")
    return f"{hh:02d}:{mm:02d}"


def exists_path(path: str) -> bool:
    try:
        return Path(path).expanduser().exists()
    except Exception:
        return False


def ensure_paths_ok() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not exists_path(CFG.program_exe):
        errors.append(f"❌ PROGRAM_EXE nu există: {CFG.program_exe}")
    if not exists_path(CFG.script_path):
        errors.append(f"❌ Script Python nu există: {CFG.script_path}")
    if not Path(CFG.working_dir).exists():
        errors.append(f"❌ Working directory nu există: {CFG.working_dir}")
    return (len(errors) == 0, errors)


def schtasks_exists(task_name: str) -> bool:
    cp = run_cmd(["schtasks", "/Query", "/TN", task_name], capture=True)
    return cp.returncode == 0


def netstat_listening(port: int) -> bool:
    cmd = f'cmd /c netstat -an | findstr ":{port}" | findstr "LISTENING"'
    cp = run_cmd_shell(cmd, capture=True)
    return cp.returncode == 0 and bool((cp.stdout or "").strip())


def open_url(url: str) -> None:
    try:
        webbrowser.open(url)
    except Exception:
        run_cmd_shell(f'start "" "{url}"')


def http_ping(url: str, timeout_sec: float = 1.5) -> bool:
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=timeout_sec) as r:  # nosec
            return 200 <= getattr(r, "status", 200) < 400
    except Exception:
        return False


def powershell_kill_pythonw_by_script(script_path: str) -> bool:
    sp = script_path.replace('"', "")
    ps = textwrap.dedent(f"""
    $sp = "{sp}"
    $killed = 0
    Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | ForEach-Object {{
        if ($_.CommandLine -and $_.CommandLine.ToLower().Contains($sp.ToLower())) {{
            try {{
                Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop
                $killed++
            }} catch {{}}
        }}
    }}
    if ($killed -gt 0) {{ exit 0 }} else {{ exit 2 }}
    """).strip()

    cp = run_cmd(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], capture=True)
    return cp.returncode in (0, 2)


# =========================
# XML Builder (multi-trigger)
# =========================

def build_task_xml() -> tuple[str, int]:
    now = _dt.datetime.now().replace(microsecond=0)
    date_iso = now.isoformat()

    daily_time = CFG.daily_time
    if CFG.enable_daily_trigger:
        daily_time = normalize_time_hhmm(CFG.daily_time)

    user = os.environ.get("USERNAME", "User")
    domain = os.environ.get("USERDOMAIN", "")
    user_id = f"{domain}\\{user}" if domain else user

    desc = _xml_escape(CFG.task_description)

    stop_on_batt = "true" if CFG.stop_on_battery else "false"
    wake_to_run = "true" if CFG.wake_to_run else "false"

    triggers: list[str] = []
    active = 0

    if CFG.enable_logon_trigger:
        active += 1
        triggers.append(
            f"""<LogonTrigger>
  <Enabled>true</Enabled>
  <UserId>{_xml_escape(user_id)}</UserId>
  <Delay>PT{CFG.delay_seconds}S</Delay>
</LogonTrigger>"""
        )

    if CFG.enable_boot_trigger:
        active += 1
        triggers.append(
            f"""<BootTrigger>
  <Enabled>true</Enabled>
  <Delay>PT{CFG.delay_seconds}S</Delay>
</BootTrigger>"""
        )

    if CFG.enable_daily_trigger:
        active += 1
        triggers.append(
            f"""<CalendarTrigger>
  <StartBoundary>2024-01-01T{daily_time}:00</StartBoundary>
  <Enabled>true</Enabled>
  <ScheduleByDay>
    <DaysInterval>1</DaysInterval>
  </ScheduleByDay>
</CalendarTrigger>"""
        )

    # IMPORTANT: XML începe FIX cu <?xml ...?> (fără spații/newline înainte)
    xml = (
        '<?xml version="1.0" encoding="UTF-16"?>\n'
        '<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">\n'
        "  <RegistrationInfo>\n"
        f"    <Date>{_xml_escape(date_iso)}</Date>\n"
        f"    <Author>{_xml_escape(user)}</Author>\n"
        f"    <Description>{desc}</Description>\n"
        "  </RegistrationInfo>\n\n"
        "  <Triggers>\n"
        + ("\n".join("    " + t.replace("\n", "\n    ") for t in triggers) + "\n")
        + "  </Triggers>\n\n"
        "  <Principals>\n"
        '    <Principal id="Author">\n'
        f"      <UserId>{_xml_escape(user_id)}</UserId>\n"
        "      <LogonType>InteractiveToken</LogonType>\n"
        f"      <RunLevel>{_xml_escape(CFG.run_level)}</RunLevel>\n"
        "    </Principal>\n"
        "  </Principals>\n\n"
        "  <Settings>\n"
        "    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>\n"
        f"    <DisallowStartIfOnBatteries>{str(not CFG.allow_on_battery).lower()}</DisallowStartIfOnBatteries>\n"
        f"    <StopIfGoingOnBatteries>{stop_on_batt}</StopIfGoingOnBatteries>\n"
        "    <AllowHardTerminate>true</AllowHardTerminate>\n"
        "    <StartWhenAvailable>true</StartWhenAvailable>\n"
        "    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>\n"
        "    <AllowStartOnDemand>true</AllowStartOnDemand>\n"
        "    <Enabled>true</Enabled>\n"
        "    <Hidden>true</Hidden>\n"
        "    <RunOnlyIfIdle>false</RunOnlyIfIdle>\n"
        "    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>\n"
        "    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>\n"
        f"    <WakeToRun>{wake_to_run}</WakeToRun>\n"
        "    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>\n"
        f"    <Priority>{CFG.priority}</Priority>\n"
        "    <RestartOnFailure>\n"
        "      <Interval>PT1M</Interval>\n"
        "      <Count>3</Count>\n"
        "    </RestartOnFailure>\n"
        "  </Settings>\n\n"
        '  <Actions Context="Author">\n'
        "    <Exec>\n"
        f"      <Command>{_xml_escape(CFG.program_exe)}</Command>\n"
        f"      <Arguments>{_xml_escape(f'\"{CFG.script_path}\"')}</Arguments>\n"
        f"      <WorkingDirectory>{_xml_escape(CFG.working_dir)}</WorkingDirectory>\n"
        "    </Exec>\n"
        "  </Actions>\n"
        "</Task>\n"
    )

    return xml, active


# === 2) ÎNLOCUIEȘTE COMPLET funcția write_temp_xml() cu asta ===
def write_temp_xml(xml: str, task_name: str) -> str:
    """
    Scrie UTF-16LE + BOM explicit, ca schtasks să nu se plângă.
    Și taie orice whitespace accidental înainte de <?xml.
    """
    xml = xml.lstrip("\ufeff\r\n\t ")  # protecție extra
    temp_dir = Path(tempfile.gettempdir())
    xml_path = temp_dir / f"{task_name}_task.xml"

    bom = b"\xff\xfe"  # UTF-16 LE BOM
    data = xml.encode("utf-16-le")

    xml_path.write_bytes(bom + data)
    return str(xml_path)

# =========================
# NO-ADMIN fallback (simple task)
# =========================

def try_create_simple_logon_task_no_admin() -> bool:
    """
    Fallback: încearcă un task simplu cu schtasks /Create (Logon only).
    Poate reuși fără admin în unele sisteme; în altele tot cere admin.
    """
    header("Create/Update — Fallback fără Admin (Logon only)")
    cprint("🧪 Încerc un task simplu (Logon trigger doar) fără XML avansat.", style="cyan" if RICH else "")
    cprint("⚠️ Dacă ai BootTrigger activ, acesta NU va fi inclus în fallback.", style="yellow" if RICH else "")

    task_name = CFG.task_name
    tr = "ONLOGON"

    # /RL LIMITED ca să evităm cereri de privilegii în plus
    cmd = [
        "schtasks",
        "/Create",
        "/TN", task_name,
        "/TR", f'"{CFG.program_exe}" "{CFG.script_path}"',
        "/SC", tr,
        "/RL", "LIMITED",
        "/F",
    ]

    cp = run_cmd(cmd, capture=True)
    if cp.returncode == 0:
        cprint("✅ SUCCES: Task simplu creat fără admin (dacă sistemul a permis).", style="bold green" if RICH else "")
        pause()
        return True

    cprint("❌ Nu a mers nici fallback fără admin.", style="bold red" if RICH else "")
    if (cp.stdout or "").strip():
        cprint(cp.stdout.strip())
    if (cp.stderr or "").strip():
        cprint(cp.stderr.strip(), style="red" if RICH else "")
    cprint("\n🔐 Concluzie: sistemul tău cere Administrator pentru crearea task-ului.", style="yellow" if RICH else "")
    pause()
    return False


# =========================
# Actions
# =========================

def action_create_task() -> None:
    header("Task Scheduler — Create/Update")

    ok, errs = ensure_paths_ok()
    if not ok:
        cprint("❌ Config invalidă. Repară următoarele:", style="bold red" if RICH else "")
        for e in errs:
            cprint(f"   {e}", style="red" if RICH else "")
        pause()
        return

    xml, active_triggers = build_task_xml()
    if active_triggers == 0:
        cprint("⚠️ ATENȚIE: Niciun trigger activ!", style="bold yellow" if RICH else "")
        cprint("   Activează cel puțin unul: logon / boot / daily.")
        pause()
        return

    # Decide if admin needed (practically yes when boot trigger used)
    needs_admin = CFG.enable_boot_trigger or True  # keep strict: schtasks /Create /XML often needs admin
    if not is_admin():
        cprint("❌ Nu ai drepturi de Administrator.", style="bold red" if RICH else "")
        cprint("   Pot cere UAC automat (recomandat).", style="yellow" if RICH else "")
        ans = prompt_choice("Vrei să cer UAC acum? (Y/N): ").strip().upper()
        if ans == "Y":
            relaunch_as_admin("Create/Update task")
            return
        # user refused UAC -> try fallback simple logon task
        return try_create_simple_logon_task_no_admin()

    # Admin path
    xml_path = write_temp_xml(xml, CFG.task_name)

    cprint("🧩 Rezumat:", style="bold cyan" if RICH else "")
    cprint(f"   • Task: {CFG.task_name}")
    cprint(f"   • Program: {CFG.program_exe}")
    cprint(f"   • Script: {CFG.script_path}")
    cprint(f"   • Working Dir: {CFG.working_dir}")
    cprint(f"   • Trigger-e active: {active_triggers}")
    if CFG.enable_boot_trigger:
        cprint("   • BootTrigger: DA (necesită Admin)", style="yellow" if RICH else "")

    cprint("\n🧹 Șterg task-ul existent (dacă există)...", style="cyan" if RICH else "")
    run_cmd(["schtasks", "/Delete", "/TN", CFG.task_name, "/F"], capture=True)

    cprint("🛠️ Creez task-ul în Task Scheduler...", style="cyan" if RICH else "")
    cp = run_cmd(["schtasks", "/Create", "/TN", CFG.task_name, "/XML", xml_path, "/F"], capture=True)

    try:
        Path(xml_path).unlink(missing_ok=True)  # type: ignore[arg-type]
    except Exception:
        pass

    if cp.returncode == 0:
        cprint("\n✅ SUCCES: Task creat/actualizat!", style="bold green" if RICH else "")
        cprint("▶️ Pornesc serverul acum...", style="green" if RICH else "")
        action_start_server(open_browser=True)
    else:
        cprint("\n❌ EROARE la crearea task-ului.", style="bold red" if RICH else "")
        if (cp.stdout or "").strip():
            cprint(cp.stdout.strip())
        if (cp.stderr or "").strip():
            cprint(cp.stderr.strip(), style="red" if RICH else "")
        pause()


def action_start_server(open_browser: bool = False) -> None:
    header("Server — Start")

    if not schtasks_exists(CFG.task_name):
        cprint("⚠️ Task-ul nu există. Creează-l întâi (opțiunea 1).", style="bold yellow" if RICH else "")
        pause()
        return

    cprint(f"▶️ Start task: {CFG.task_name}", style="cyan" if RICH else "")
    cp = run_cmd(["schtasks", "/Run", "/TN", CFG.task_name], capture=True)

    if cp.returncode != 0:
        cprint("❌ Nu am putut porni task-ul.", style="bold red" if RICH else "")
        if (cp.stderr or "").strip():
            cprint(cp.stderr.strip(), style="red" if RICH else "")
        pause()
        return

    cprint("⏳ Aștept 8 secunde pentru pornirea serverului...", style="cyan" if RICH else "")
    for i in range(1, 9):
        if RICH:
            console.print(f"   • {i}/8", style="dim")  # type: ignore
        else:
            print(".", end="", flush=True)
        time.sleep(1)
    if not RICH:
        print()

    listening = netstat_listening(CFG.server_port)
    ping_ok = http_ping(CFG.ping_url, timeout_sec=1.5)

    if listening or ping_ok:
        cprint("\n✅ PERFECT: Serverul este activ!", style="bold green" if RICH else "")
        cprint(f"   • Port: {CFG.server_port} (LISTENING={listening})")
        cprint(f"   • Ping: {CFG.ping_url} (OK={ping_ok})")
        cprint(f"   • Home: {CFG.home_url}")
        if open_browser:
            cprint("🌐 Deschid browser...", style="green" if RICH else "")
            open_url(CFG.home_url)
    else:
        cprint("\n⚠️ Task pornit, dar serverul nu pare activ încă.", style="bold yellow" if RICH else "")
        cprint("   Posibile cauze: port ocupat, eroare în script, module lipsă, path greșit.")
    pause()


def action_stop_server() -> None:
    header("Server — Stop")

    cprint("🛑 Oprire: încerc să omor DOAR pythonw.exe care rulează scriptul tău...", style="cyan" if RICH else "")
    ok = powershell_kill_pythonw_by_script(CFG.script_path)

    if not ok:
        cprint("⚠️ Nu am putut rula comanda PowerShell de oprire.", style="bold yellow" if RICH else "")
        cprint("   Fallback: omor toate pythonw.exe (mai agresiv).", style="yellow" if RICH else "")
        run_cmd(["taskkill", "/F", "/IM", "pythonw.exe"], capture=True)

    listening = netstat_listening(CFG.server_port)
    if not listening:
        cprint("✅ Server oprit (portul nu mai ascultă).", style="bold green" if RICH else "")
    else:
        cprint("⚠️ Portul încă ascultă. Posibil alt proces folosește portul.", style="bold yellow" if RICH else "")

    pause()


def action_restart_server() -> None:
    header("Server — Restart")
    cprint("1/3 🛑 Stop...", style="cyan" if RICH else "")
    powershell_kill_pythonw_by_script(CFG.script_path)

    cprint("2/3 ⏳ Wait 3s...", style="cyan" if RICH else "")
    time.sleep(3)

    cprint("3/3 ▶️ Start...", style="cyan" if RICH else "")
    action_start_server(open_browser=True)


def action_check_status() -> None:
    header("Status — Task + Process + Port + HTTP")

    if schtasks_exists(CFG.task_name):
        cprint("✅ Task există.", style="bold green" if RICH else "")
        cp = run_cmd(["schtasks", "/Query", "/TN", CFG.task_name, "/FO", "LIST", "/V"], capture=True)
        lines = (cp.stdout or "").splitlines()
        status_lines = [ln for ln in lines if "Status:" in ln]
        for ln in status_lines[:2]:
            cprint(f"   {ln.strip()}", style="dim" if RICH else "")
    else:
        cprint("❌ Task NU există.", style="bold red" if RICH else "")

    cprint("\n🧠 Process check (pythonw.exe):", style="cyan" if RICH else "")
    cp2 = run_cmd_shell('cmd /c tasklist | findstr /I "pythonw.exe"', capture=True)
    if cp2.returncode == 0 and (cp2.stdout or "").strip():
        cprint("✅ pythonw.exe rulează:", style="green" if RICH else "")
        cprint(cp2.stdout.strip(), style="dim" if RICH else "")
    else:
        cprint("⚠️ pythonw.exe nu apare în tasklist.", style="yellow" if RICH else "")

    cprint("\n🌐 Port check:", style="cyan" if RICH else "")
    listening = netstat_listening(CFG.server_port)
    if listening:
        cprint(f"✅ Port {CFG.server_port}: LISTENING", style="bold green" if RICH else "")
        cp3 = run_cmd_shell(f'cmd /c netstat -an | findstr ":{CFG.server_port}"', capture=True)
        if (cp3.stdout or "").strip():
            cprint(cp3.stdout.strip(), style="dim" if RICH else "")
    else:
        cprint(f"❌ Port {CFG.server_port}: NU este LISTENING", style="bold red" if RICH else "")

    cprint("\n📡 HTTP ping:", style="cyan" if RICH else "")
    ok = http_ping(CFG.ping_url, timeout_sec=1.5)
    if ok:
        cprint("✅ /ping răspunde.", style="bold green" if RICH else "")
    else:
        cprint("⚠️ /ping nu răspunde.", style="bold yellow" if RICH else "")

    pause()


def action_delete_task() -> None:
    header("Task — Delete")

    ans = prompt_choice("Ești sigur că vrei să ștergi task-ul? (Y/N): ").strip().upper()
    if ans != "Y":
        return

    if not is_admin():
        cprint("❌ Ștergerea task-ului cere Administrator.", style="bold red" if RICH else "")
        ans2 = prompt_choice("Vrei să cer UAC acum? (Y/N): ").strip().upper()
        if ans2 == "Y":
            relaunch_as_admin("Delete task")
            return
        cprint("⚠️ Ai refuzat UAC. Nu pot șterge task-ul fără drepturi.", style="yellow" if RICH else "")
        pause()
        return

    cprint("🛑 Oprire server (doar scriptul tău)...", style="cyan" if RICH else "")
    powershell_kill_pythonw_by_script(CFG.script_path)

    cprint(f"🗑️ Șterg task: {CFG.task_name}", style="cyan" if RICH else "")
    cp = run_cmd(["schtasks", "/Delete", "/TN", CFG.task_name, "/F"], capture=True)

    if cp.returncode == 0:
        cprint("✅ Task șters.", style="bold green" if RICH else "")
    else:
        cprint("❌ Eroare la ștergere.", style="bold red" if RICH else "")
        if (cp.stderr or "").strip():
            cprint(cp.stderr.strip(), style="red" if RICH else "")
    pause()


def action_open_scheduler() -> None:
    header("Open — Task Scheduler")
    cprint("🧭 Deschid Task Scheduler...", style="cyan" if RICH else "")
    run_cmd_shell("start taskschd.msc")
    pause()


def action_test_http() -> None:
    header("Test — HTTP")

    cprint("🌐 Deschid launcher în browser...", style="cyan" if RICH else "")
    open_url(CFG.home_url)

    cprint("📡 Test /ping...", style="cyan" if RICH else "")
    ok = http_ping(CFG.ping_url, timeout_sec=1.5)

    if ok:
        cprint("✅ Server răspunde la ping.", style="bold green" if RICH else "")
    else:
        cprint("❌ Server nu răspunde la ping.", style="bold red" if RICH else "")
        cprint("   Verifică: status (opțiunea 5) / port ocupat / erori în script.")
    pause()


# =========================
# Main Menu
# =========================

def show_menu() -> None:
    header("Fire & Forget — Task Scheduler Manager")

    admin_txt = "DA" if is_admin() else "NU"
    admin_style = "bold green" if (RICH and is_admin()) else ("bold red" if RICH else "")

    if RICH:
        tbl = Table(box=box.SIMPLE_HEAVY)
        tbl.add_column("Opțiune", style="bold cyan", no_wrap=True)
        tbl.add_column("Acțiune", style="white")

        tbl.add_row("1", "🧰 Creează / Actualizează task-ul (AUTO-UAC)")
        tbl.add_row("2", "▶️ Pornește serverul acum")
        tbl.add_row("3", "🛑 Oprește serverul (safe kill by script path)")
        tbl.add_row("4", "🔁 Restart complet (Stop + Start)")
        tbl.add_row("5", "📊 Verifică status (task + process + port + ping)")
        tbl.add_row("6", "🗑️ Șterge task-ul (AUTO-UAC)")
        tbl.add_row("7", "🧭 Deschide Task Scheduler")
        tbl.add_row("8", "🌐 Test conexiune HTTP")
        tbl.add_row("0", "🚪 Ieșire")

        console.print(tbl)  # type: ignore
        console.print(Text(f"\nAdmin: {admin_txt}", style=admin_style))
        console.print(Text(f"Task: {CFG.task_name} | Port: {CFG.server_port}", style="dim"))
        if CFG.enable_boot_trigger:
            console.print(Text("BootTrigger: ON (Admin necesar)", style="yellow"))
    else:
        print("[1] Creează/Actualizează task-ul (AUTO-UAC)")
        print("[2] Pornește serverul acum")
        print("[3] Oprește serverul")
        print("[4] Restart complet (Stop + Start)")
        print("[5] Verifică status")
        print("[6] Șterge task-ul (AUTO-UAC)")
        print("[7] Deschide Task Scheduler")
        print("[8] Test conexiune HTTP")
        print("[0] Ieșire")
        print(f"\nAdmin: {admin_txt} | Task: {CFG.task_name} | Port: {CFG.server_port}")
        if CFG.enable_boot_trigger:
            print("BootTrigger: ON (Admin necesar)")

    choice = prompt_choice("\nAlege opțiunea (0-8): ").strip()

    if choice == "1":
        action_create_task()
    elif choice == "2":
        action_start_server(open_browser=True)
    elif choice == "3":
        action_stop_server()
    elif choice == "4":
        action_restart_server()
    elif choice == "5":
        action_check_status()
    elif choice == "6":
        action_delete_task()
    elif choice == "7":
        action_open_scheduler()
    elif choice == "8":
        action_test_http()
    elif choice == "0":
        sys.exit(0)
    else:
        cprint("⚠️ Opțiune invalidă.", style="yellow" if RICH else "")
        pause()


def main() -> None:
    # Nu cerem admin la pornire (ca să poți folosi Start/Status fără UAC).
    # Cerem automat admin doar când alegi Create/Delete.
    while True:
        show_menu()


if __name__ == "__main__":
    main()
