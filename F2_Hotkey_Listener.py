# F2_Hotkey_Listener.py
# MULTI-HOTKEY LAUNCHER — mod F2-only: fără server_fire_and_forget / fără port 8899
# F2 deschide Launcher_FIRE_AND_FORGET.html din acest folder + pagina Quick App.

import keyboard
import subprocess
import webbrowser
import sys
import os
import time
import json
import traceback
import winsound
import ctypes
import atexit
from datetime import datetime
from pathlib import Path
from threading import Thread
import signal

_ERROR_ALREADY_EXISTS = 183
_MUTEX_NAME = "Local\\F2HotkeyListenerSingleton"
_mutex_handle = None


def _acquire_single_instance() -> bool:
    global _mutex_handle
    h = ctypes.windll.kernel32.CreateMutexW(None, False, _MUTEX_NAME)
    if not h:
        return False
    if ctypes.windll.kernel32.GetLastError() == _ERROR_ALREADY_EXISTS:
        ctypes.windll.kernel32.CloseHandle(h)
        return False
    _mutex_handle = h
    return True


def _release_mutex() -> None:
    global _mutex_handle
    if _mutex_handle:
        try:
            ctypes.windll.kernel32.CloseHandle(_mutex_handle)
        except Exception:
            pass
        _mutex_handle = None


atexit.register(_release_mutex)

# =====================================================================
# REDIRECT STDOUT/STDERR (SAFE)
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent

class SafeLogger:
    def __init__(self, log_file: Path, terminal_stream):
        self.log_file = log_file
        self.terminal = terminal_stream

    def write(self, message):
        # write to original terminal (if any)
        try:
            if self.terminal and hasattr(self.terminal, "write"):
                self.terminal.write(message)
        except:
            pass

        # write to file
        try:
            with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
                f.write(message)
        except:
            pass

    def flush(self):
        try:
            if self.terminal and hasattr(self.terminal, "flush"):
                self.terminal.flush()
        except:
            pass

STDOUT_LOG = BASE_DIR / "F2_STDOUT.log"
STDERR_LOG = BASE_DIR / "F2_STDERR.log"

_orig_stdout = sys.stdout
_orig_stderr = sys.stderr
sys.stdout = SafeLogger(STDOUT_LOG, _orig_stdout)
sys.stderr = SafeLogger(STDERR_LOG, _orig_stderr)

# =====================================================================
# CONFIGURARE - IMPORTANT!
# =====================================================================

LOG_FILE = BASE_DIR / "hotkey_launcher.log"
STATS_FILE = BASE_DIR / "hotkey_stats.json"
ERROR_LOG = BASE_DIR / "F2_ERRORS.log"

DEBOUNCE_TIME = 0.5
last_press = {}
stats = {}
BEEP_ENABLED = True
RUNNING = True

# Nu mai folosim server HTTP local (server_fire_and_forget.py) — F2 = fișier HTML + Quick App
HTTP_SERVER_TASK_NAME = None

# Launcher deschis la F2 (același folder ca acest script)
LAUNCHER_HTML_FILE = "Launcher_FIRE_AND_FORGET.html"

# ✅ URL Quick App (GitHub Pages)
QUICK_APP_URL = "https://metusalem696.github.io/quick-app-launcher/"

# =====================================================================
# LOGGING / UTILS
# =====================================================================

def log_error(msg, exception=None):
    """Logging special pentru erori critice - 100% safe"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ERROR_LOG, "a", encoding="utf-8", errors="replace") as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"[{timestamp}] {msg}\n")
            if exception:
                f.write(f"Exception: {str(exception)}\n")
                f.write(traceback.format_exc())
            f.write(f"{'='*70}\n")
    except:
        pass

def log(msg, level=None):
    """Log - SAFE pentru pythonw.exe"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"

        if "✓" in msg or "PORNIT" in msg or level == "OK":
            print(f"\033[92m{line}\033[0m")
        elif "✗" in msg or "EROARE" in msg or level == "ERR":
            print(f"\033[91m{line}\033[0m")
        elif "⚠" in msg or "ATENTIE" in msg or level == "WARN":
            print(f"\033[93m{line}\033[0m")
        else:
            print(line)

        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write(line + "\n")
    except Exception as e:
        log_error("Logging failed", e)

def beep():
    """Beep ULTRA-SAFE"""
    if not BEEP_ENABLED:
        return

    def safe_beep():
        try:
            sound_files = [
                "mechanical-keyboard-23537.mp3",
                "kmechanical-keyboard-23537.mp3",
                "beep.mp3",
                "beep.wav",
            ]

            for filename in sound_files:
                beep_file = os.path.join(BASE_DIR, filename)

                if os.path.exists(beep_file):
                    if filename.endswith(".mp3"):
                        try:
                            ps_cmd = f"""
Add-Type -AssemblyName presentationCore
$mediaPlayer = New-Object System.Windows.Media.MediaPlayer
$mediaPlayer.Open([uri]"{beep_file}")
$mediaPlayer.Play()
Start-Sleep -Milliseconds 250
$mediaPlayer.Stop()
$mediaPlayer.Close()
"""
                            subprocess.run(
                                ["powershell", "-NoProfile", "-Command", ps_cmd],
                                capture_output=True,
                                creationflags=subprocess.CREATE_NO_WINDOW,
                                timeout=1.0,
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )
                            return
                        except:
                            continue

                    elif filename.endswith(".wav"):
                        try:
                            winsound.PlaySound(beep_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                            return
                        except:
                            continue

            try:
                winsound.MessageBeep(winsound.MB_OK)
            except:
                pass

        except Exception as e:
            log_error("beep() error", e)

    try:
        Thread(target=safe_beep, daemon=True).start()
    except:
        pass

def load_stats():
    global stats
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, "r", encoding="utf-8", errors="replace") as f:
                stats = json.load(f)
    except Exception as e:
        log_error("Failed to load stats", e)
        stats = {}

def save_stats():
    try:
        with open(STATS_FILE, "w", encoding="utf-8", errors="replace") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log_error("Failed to save stats", e)

def increment_stat(hotkey_name):
    try:
        if hotkey_name not in stats:
            stats[hotkey_name] = {"count": 0, "last_used": None}

        stats[hotkey_name]["count"] += 1
        stats[hotkey_name]["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_stats()
    except Exception as e:
        log_error(f"Failed to increment stat for {hotkey_name}", e)

def debounce_check(key_name):
    try:
        now = time.time()
        if key_name in last_press and (now - last_press[key_name] < DEBOUNCE_TIME):
            return False
        last_press[key_name] = now
        return True
    except:
        return True

def show_notification(title, message):
    """Notificare - SAFE pentru pythonw"""
    def safe_notify():
        try:
            ps_cmd = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml(@"
<toast><visual><binding template='ToastText02'>
<text id='1'>{title}</text><text id='2'>{message}</text>
</binding></visual></toast>
"@)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Fire and Forget").Show($toast)
"""
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=1.5,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except:
            pass

    try:
        Thread(target=safe_notify, daemon=True).start()
    except:
        pass

def check_server_running():
    """Verifică server HTTP - SAFE"""
    try:
        result = subprocess.run(
            ["netstat", "-an"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=1.0,
            stdin=subprocess.DEVNULL,
        )
        out = (result.stdout or "")
        return (":8899" in out) and ("LISTENING" in out.upper())
    except:
        return False

def verify_task_exists(task_name):
    """Verifică dacă un task există în Task Scheduler - SAFE"""
    try:
        result = subprocess.run(
            ["schtasks", "/Query", "/TN", task_name],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=2,
            stdin=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except:
        return False


def open_local_launcher_html() -> bool:
    """Deschide Launcher_FIRE_AND_FORGET.html din folderul scriptului (fără localhost:8899)."""
    p = BASE_DIR / LAUNCHER_HTML_FILE
    if not p.is_file():
        log(f"   ✗ Nu găsesc fișierul launcher: {p}", "ERR")
        return False
    try:
        os.startfile(str(p))  # type: ignore[attr-defined]
        return True
    except Exception as e:
        log_error(f"os.startfile launcher failed: {p}", e)
        try:
            return bool(webbrowser.open(p.as_uri()))
        except Exception as e2:
            log_error("webbrowser.open file URI failed", e2)
            return False


def open_url(url: str) -> bool:
    """
    Deschide URL-ul cât mai sigur (pythonw + hotkeys).
    Încearcă: webbrowser tab -> os.startfile -> cmd start
    """
    # 1) webbrowser
    try:
        if webbrowser.open_new_tab(url):
            return True
    except Exception as e:
        log_error(f"webbrowser.open_new_tab failed: {url}", e)

    # 2) Windows shell
    try:
        os.startfile(url)  # type: ignore
        return True
    except Exception as e:
        log_error(f"os.startfile failed: {url}", e)

    # 3) cmd start
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", url],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        log_error(f"cmd start failed: {url}", e)

    return False

# =====================================================================
# DECORATOR
# =====================================================================

def safe_wrapper(func):
    """Decorator pentru protecție completă"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(f"Hotkey function {func.__name__} crashed", e)
            log(f"   ✗ EROARE în {func.__name__}: {str(e)}", "ERR")
    return wrapper

# =====================================================================
# HOTKEY FUNCTIONS
# =====================================================================

@safe_wrapper
def open_launcher():
    """F2 — launcher HTML local + Quick App (fără server_fire_and_forget / 8899)."""
    if not debounce_check("F2"):
        return

    log("🔥 F2 APASAT! Deschid Quick App Launcher (local) + Quick App...")
    increment_stat("F2_Launcher")
    beep()

    if HTTP_SERVER_TASK_NAME and not check_server_running():
        log("   ⚠ Server HTTP (opțional) nu răspunde pe 8899 — continui fără el.", "WARN")

    try:
        ok1 = open_local_launcher_html()
        log(
            f"   ✓ Launcher local ({LAUNCHER_HTML_FILE}) {'deschis' if ok1 else 'NU s-a putut deschide'}!",
            "OK" if ok1 else "WARN",
        )

        time.sleep(0.3)

        ok2 = open_url(QUICK_APP_URL)
        log(f"   ✓ Quick App {'deschis' if ok2 else 'NU s-a putut deschide'}!", "OK" if ok2 else "WARN")

        if ok1 and ok2:
            show_notification("Quick App Launcher", "Launcher local + Quick App deschise!")
        elif ok1:
            show_notification("Quick App Launcher", "Launcher local deschis. Quick App nu s-a putut deschide.")
        else:
            show_notification("Quick App Launcher", "Nu s-au putut deschide paginile.")
    except Exception as e:
        log_error("Failed to open launcher / browsers", e)
        log(f"   ✗ Eroare la deschidere: {e}", "ERR")

@safe_wrapper
def open_task_scheduler():
    if not debounce_check("F10"):
        return

    log("📅 F10 APASAT! Deschid Task Scheduler...")
    increment_stat("F10_TaskScheduler")
    beep()

    subprocess.Popen(
        ["taskschd.msc"],
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log("   ✓ Task Scheduler deschis!", "OK")
    show_notification("Task Scheduler", "Deschis!")

@safe_wrapper
def open_control_panel():
    if not debounce_check("F9"):
        return

    log("⚙️  F9 APASAT! Deschid Control Panel...")
    increment_stat("F9_ControlPanel")
    beep()

    subprocess.Popen(
        ["control"],
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log("   ✓ Control Panel deschis!", "OK")
    show_notification("Control Panel", "Deschis!")

@safe_wrapper
def open_task_manager():
    if not debounce_check("F11"):
        return

    log("📊 F11 APASAT! Deschid Task Manager...")
    increment_stat("F11_TaskManager")
    beep()

    subprocess.Popen(
        ["taskmgr"],
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log("   ✓ Task Manager deschis!", "OK")
    show_notification("Task Manager", "Deschis!")

@safe_wrapper
def open_explorer():
    if not debounce_check("F3"):
        return

    log("📁 F3 APASAT! Deschid File Explorer...")
    increment_stat("F3_Explorer")
    beep()

    subprocess.Popen(
        ["explorer"],
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log("   ✓ Explorer deschis!", "OK")
    show_notification("File Explorer", "Deschis!")

@safe_wrapper
def toggle_beep_and_stats():
    global BEEP_ENABLED

    if not debounce_check("F12"):
        return

    BEEP_ENABLED = not BEEP_ENABLED
    state = "ON 🔊" if BEEP_ENABLED else "OFF 🔇"
    log(f"🔔 BEEP setat pe: {state}")

    if stats:
        log("=" * 70)
        log("📊 STATISTICI UTILIZARE HOTKEYS:")
        log("=" * 70)

        sorted_stats = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)
        for key, data in sorted_stats:
            log(f"   {key}: {data['count']} utilizări | Ultima: {data['last_used']}")

        log("=" * 70)
    else:
        log("   ℹ Nicio statistică disponibilă încă")

@safe_wrapper
def reload_listener():
    log("🔄 Ctrl+F12 APASAT! Restart listener...")
    save_stats()
    python = sys.executable
    os.execl(python, python, *sys.argv)

@safe_wrapper
def test_beep():
    log("🔊 TEST BEEP...")

    mp3_files = [
        "mechanical-keyboard-23537.mp3",
        "kmechanical-keyboard-23537.mp3",
    ]

    found = False
    for mp3 in mp3_files:
        mp3_file = os.path.join(BASE_DIR, mp3)
        if os.path.exists(mp3_file):
            log(f"   ✓ MP3 gasit: {mp3}", "OK")
            found = True
            break

    if not found:
        log("   ⚠ ATENTIE: Niciun MP3 gasit!", "WARN")

    log("   🎵 Redau sunetul...")
    beep()
    time.sleep(0.3)
    beep()
    log("   ✓ Ai auzit 2 beep-uri?", "OK")

def signal_handler(sig, frame):
    global RUNNING
    RUNNING = False
    log("🛑 Primesc semnal de oprire...", "WARN")
    save_stats()
    sys.exit(0)

# =====================================================================
# MAIN
# =====================================================================

def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        if not _acquire_single_instance():
            try:
                with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(
                        f"[{ts}] ⚠ PORNIRE REFUZATĂ: există deja F2_Hotkey_Listener activ (închide dublurile în Task Manager).\n"
                    )
            except Exception:
                pass
            sys.exit(0)

        load_stats()

        log("=" * 70)
        log("🚀 MULTI-HOTKEY LAUNCHER — F2 local (fără server_fire_and_forget)")
        log("=" * 70)
        log("📌 HOTKEYS DISPONIBILE:")
        log(f"   F2  = {LAUNCHER_HTML_FILE} (local) + Quick App")
        log("   F3  = File Explorer")
        log("   F9  = Control Panel")
        log("   F10 = Task Scheduler")
        log("   F11 = Task Manager")
        log("   F12 = Toggle Beep + Statistici")
        log("   Ctrl+F12 = Restart listener")
        log("   Ctrl+Alt+B = Test beep")
        log("")
        log("✨ MODE: DETACHED (fara consola)")
        log(f"   • BEEP: {'ON 🔊' if BEEP_ENABLED else 'OFF 🔇'}")
        log(f"   • Quick App: {QUICK_APP_URL}")

        if HTTP_SERVER_TASK_NAME:
            log(f"   • HTTP Server Task: {HTTP_SERVER_TASK_NAME}")
            if verify_task_exists(HTTP_SERVER_TASK_NAME):
                log("     ✓ Task gasit in Task Scheduler", "OK")
            else:
                log("     ⚠ Task NU gasit! Verifica numele!", "WARN")
        else:
            log("   • F2: fără server HTTP local — nu se folosește server_fire_and_forget.py")

        log("=" * 70)

        if HTTP_SERVER_TASK_NAME:
            if check_server_running():
                log("✓ Server HTTP ACTIV pe portul 8899", "OK")
            else:
                log("⚠ ATENTIE: Server HTTP NU rulează pe 8899!", "WARN")
        else:
            log("   (Port 8899 ignorat — mod doar F2 + fișiere locale)")

        log("=" * 70)

        # Înregistrare hotkeys
        try:
            keyboard.add_hotkey("f2", open_launcher, suppress=True)
            keyboard.add_hotkey("f3", open_explorer, suppress=True)
            keyboard.add_hotkey("f9", open_control_panel, suppress=True)
            keyboard.add_hotkey("f10", open_task_scheduler, suppress=True)
            keyboard.add_hotkey("f11", open_task_manager, suppress=True)
            keyboard.add_hotkey("f12", toggle_beep_and_stats, suppress=True)
            keyboard.add_hotkey("ctrl+f12", reload_listener, suppress=False)
            keyboard.add_hotkey("ctrl+alt+b", test_beep, suppress=True)
            log("✓ Toate hotkey-urile au fost înregistrate!", "OK")
        except Exception as e:
            log_error("Failed to register hotkeys", e)
            log("✗ EROARE la înregistrarea hotkey-urilor!", "ERR")
            return

        # Main loop cu heartbeat
        log("💓 Listener activ - heartbeat la fiecare 60s")
        last_heartbeat = time.time()

        while RUNNING:
            try:
                time.sleep(1)
                if time.time() - last_heartbeat > 60:
                    log("💓 Heartbeat - Listener activ")
                    last_heartbeat = time.time()
            except KeyboardInterrupt:
                break
            except Exception as e:
                log_error("Main loop error", e)
                time.sleep(5)

    except Exception as e:
        log_error("CRITICAL main() error", e)
        log("❌ EROARE CRITICĂ în main()!", "ERR")
    finally:
        log("🛑 Listener oprit", "WARN")
        save_stats()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error("FATAL top-level error", e)
        try:
            with open(BASE_DIR / "F2_CRITICAL_CRASH.log", "a", encoding="utf-8", errors="replace") as f:
                f.write(f"\n{datetime.now()}: {str(e)}\n")
                f.write(traceback.format_exc())
        except:
            pass
        sys.exit(1)
