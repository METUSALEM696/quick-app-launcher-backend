# server_fire_and_forget_FINAL_FIXED.py
# ✅ SINGLE SOURCE OF TRUTH (fără funcții duplicate)
# ✅ Auto-ELEVATE (UAC) dacă nu rulează ca Administrator
# ✅ /kill + /killall BLOCAȚI dacă nu e Admin (nu mai "se preface")
# ✅ Kill REAL: taskkill /T + confirmare că procesul NU mai rulează
# ✅ Status REAL: PID-uri via CIM (merge și la "Arduino IDE.exe" cu spații)
# ✅ Detectează dacă portul 8899 este deja ocupat (alt server)
# ✅ ADDED: Link pagină GitHub Pages personalizată
# ✅ FIX: Fallback pentru EXE din WindowsApps (ChatGPT Desktop) -> os.startfile dacă Popen e refuzat
# ✅ FIX: Eliminat text invalid la finalul fișierului

from __future__ import annotations

import ctypes
import json
import mimetypes
import os
import re
import shlex
import socket
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    from http.server import ThreadingHTTPServer as HTTPServer
except Exception:
    from http.server import HTTPServer

# =========================
# CONFIG
# =========================
PORT = 8899
SERVER_STARTED_AT = time.time()
HTTPD_REF = None
STOP_TOKEN = "1234"

LAUNCHER_HTML = "Launcher_FIRE_AND_FORGET.html"
SOUNDS_DIR_NAME = "sounds"

DEFAULT_FOCUS_TIMEOUT = 3.5
FOCUS_CHECK_INTERVAL = 0.15
FOCUS_INITIAL_DELAY = 0.20

SLOW_APPS = {
    "solidworks": 8.0,
    "cura": 5.0,
    "easyeda": 5.0,
    "nrfconnect": 4.0,
    "word": 3.0,
    "excel": 3.0,
}
SKIP_FOCUS = {"qbittorrent", "throttlestop", "surfshark", "totalav"}

WINDOW_PATTERNS = {
    "taskscheduler": "Task Scheduler",
    "controlpanel": "Control Panel",
    "clock": "Clock",
    "intelgraphics": "Intel",
    "photos": "Photos",
    "code": "Visual Studio Code",
    "claudedesktop": "Claude",
    "claudecode": "Claude",
    "chatgptdesktop": "ChatGPT",
    "wt": "Windows Terminal",
    "arduino": "Arduino",
    "git": "MINGW",
    "python": "Python",
    "easyeda": "EasyEDA",
    "solidworks": "SOLIDWORKS",
    "cura": "Cura",
    "nrfconnect": "nRF Connect",
    "chrome": "Chrome",
    "brave": "Brave",
    "word": "Word",
    "excel": "Excel",
    "vlc": "VLC",
    "qbittorrent": "qBittorrent",
    "surfshark": "Surfshark",
    "keepassxc": "KeePassXC",
    "totalav": "TotalAV",
    "explorer": "File Explorer",
    "calc": "Calculator",
    "notepad": "Notepad",
    "taskmgr": "Task Manager",
    "journal": "Journal",
    "throttlestop": "ThrottleStop",
    "wintools": "Administrative Tools",
}

APPS = {
    "controlpanel": "control",
    "clock": r"shell:AppsFolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App",
    "intelgraphics": r"shell:AppsFolder\AppUp.IntelGraphicsExperience_8j3eq9eme6ctt!App",
    "photos": r"shell:AppsFolder\Microsoft.Windows.Photos_8wekyb3d8bbwe!App",
    "taskscheduler": r"C:\Windows\System32\taskschd.msc",

    # Development Tools
    "code": r"C:\Users\HERCULE SI DANIELA\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "claudedesktop": r"shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude",

    # ChatGPT Desktop (MS Store / WindowsApps)
    # Recomandat: alias stabil (dacă există): ...\WindowsApps\chatgpt.exe
    # Dacă preferi calea lungă din instalare, o poți pune aici.
    "chatgptdesktop": r"C:\Users\HERCULE SI DANIELA\AppData\Local\Microsoft\WindowsApps\chatgpt.exe",

    "claudecode": r"powershell -NoProfile -Command claude",
    "wt": "wt",
    "arduino": r"C:\Program Files\Arduino IDE\Arduino IDE.exe",
    "git": r"C:\Program Files\Git\bin\bash.exe",
    "python": "python",

    # Engineering Software
    "easyeda": r"C:\Program Files\easyeda-pro\easyeda-pro.exe",
    "solidworks": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\SOLIDWORKS 2023\SOLIDWORKS 2023.lnk",
    "cura": r"C:\Program Files\UltiMaker Cura 5.10.1\UltiMaker-Cura.exe",
    "nrfconnect": r"C:\Users\HERCULE SI DANIELA\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Nordic Semiconductor\nRF Connect for Desktop.lnk",

    # Browsers
    "chrome": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",

    # Office
    "word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word 2016.lnk",
    "excel": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel 2016.lnk",

    # Media
    "vlc": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VideoLAN\VLC media player.lnk",
    "qbittorrent": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\qBittorrent\qBittorrent.lnk",

    # Security & Utilities
    "surfshark": r"C:\Program Files\Surfshark\Surfshark.exe",
    "keepassxc": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\KeePassXC\KeePassXC.lnk",
    "totalav": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TotalAV.lnk",

    # System Tools
    "explorer": "explorer",
    "calc": "calc",
    "notepad": "notepad",
    "taskmgr": "taskmgr",
    "journal": r"shell:AppsFolder\Microsoft.MicrosoftJournal_8wekyb3d8bbwe!App",
    "throttlestop": r"E:\script\ThrottleStop.exe",
    "wintools": r"shell:Common Administrative Tools",

    # Web Apps & Links
    "chatgpt": "https://chat.openai.com",

    # Pagină locală — completată după BASE_DIR (nu hardcoda E:)
    "myhomepage": "__LAUNCHER_FINAL_WITH_SOUND__",
}

# IMPORTANT: trebuie să fie imaginea reală (exact cum apare în Task Manager → Details)
PROCESS_NAMES = {
    "code": "Code.exe",
    "claudedesktop": "Claude.exe",
    "chatgptdesktop": "chatgpt.exe",
    "claudecode": "Claude Code.exe",
    "wt": "WindowsTerminal.exe",
    "arduino": "Arduino IDE.exe",
    "git": "bash.exe",
    "python": "python.exe",
    "easyeda": "easyeda-pro.exe",
    "solidworks": "SLDWORKS.exe",
    "cura": "UltiMaker-Cura.exe",
    "nrfconnect": "nrfconnect.exe",
    "chrome": "chrome.exe",
    "brave": "brave.exe",
    "word": "WINWORD.EXE",
    "excel": "EXCEL.EXE",
    "vlc": "vlc.exe",
    "qbittorrent": "qbittorrent.exe",
    "surfshark": "Surfshark.exe",
    "keepassxc": "KeePassXC.exe",
    "totalav": "TotalAV.exe",
    "controlpanel": "control.exe",
    "calc": "CalculatorApp.exe",
    "notepad": "notepad.exe",
    "taskmgr": "Taskmgr.exe",
    "throttlestop": "ThrottleStop.exe",
}

PROTECT_FROM_KILLALL_IMAGES = {
    "chrome.exe", "brave.exe", "msedge.exe", "microsoftedge.exe",
    "firefox.exe", "opera.exe", "vivaldi.exe",
}

BASE_DIR = Path(__file__).resolve().parent
# Fișiere /local/... — mereu lângă script (P:, E:, etc.); nu hardcoda litera discului.
LOCAL_ROOT = BASE_DIR
SOUNDS_DIR = (BASE_DIR / SOUNDS_DIR_NAME).resolve()
LOG_FILE = (BASE_DIR / "server_log.txt").resolve()

# =========================
# PID tracking
# =========================
_last_pid_lock = threading.Lock()
LAST_PIDS: dict[str, dict] = {}  # { key: {"pid": int, "t0": float} }

# =========================
# LOGGING
# =========================
_log_lock = threading.Lock()

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with _log_lock:
            with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
                f.write(line + "\n")
    except Exception:
        pass

# =========================
# ADMIN / ELEVATION
# =========================
def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def ensure_admin_or_relaunch():
    """Dacă nu e admin, relansează cu UAC și oprește instanța curentă."""
    if is_admin():
        return
    script = str(Path(__file__).resolve())
    params = f'"{script}"'
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
    except Exception:
        pass
    sys.exit(0)

# =========================
# NETWORK
# =========================
def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.0.34"

LOCAL_IP = get_local_ip()

# Fereastra din prim-plan — NU tasta Win (evită deschiderea Start / panouri albastre)
_SW_MINIMIZE = 6
_SW_MAXIMIZE = 3
_WM_CLOSE = 0x0010
_KEYEVENTF_KEYUP = 0x0002
_VK_LWIN = 0x5B
_VK_D = 0x44


def _hwnd_foreground() -> int:
    try:
        return int(ctypes.windll.user32.GetForegroundWindow() or 0)
    except Exception:
        return 0


def _win_minimize_foreground() -> None:
    h = _hwnd_foreground()
    if h:
        ctypes.windll.user32.ShowWindow(h, _SW_MINIMIZE)


def _win_maximize_foreground() -> None:
    h = _hwnd_foreground()
    if h:
        ctypes.windll.user32.ShowWindow(h, _SW_MAXIMIZE)


def _win_close_foreground() -> None:
    h = _hwnd_foreground()
    if h:
        ctypes.windll.user32.PostMessageW(h, _WM_CLOSE, 0, 0)


def _toggle_show_desktop() -> None:
    """Arată/ascunde desktopul fără tasta Win (care deschidea meniul Start).

    Folosește COM-ul Shell.Application -> ToggleDesktop(), echivalentul Win+D.
    """
    ps = "(New-Object -ComObject Shell.Application).ToggleDesktop()"
    run_hidden(["powershell", "-NoProfile", "-Command", ps])


# ---- Comutare între ferestrele deschise (ca în taskbar) ----
def _enum_alt_tab_windows() -> list:
    """Întoarce lista de HWND-uri pentru ferestrele vizibile din taskbar."""
    user32 = ctypes.windll.user32
    GWL_EXSTYLE = -20
    WS_EX_TOOLWINDOW = 0x00000080
    DWMWA_CLOAKED = 14
    result = []

    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def _cb(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        if user32.GetWindowTextLengthW(hwnd) == 0:
            return True
        ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        if ex_style & WS_EX_TOOLWINDOW:
            return True
        # Sări peste ferestrele "cloaked" (UWP ascunse, ex. Settings în fundal)
        try:
            cloaked = ctypes.c_int(0)
            ctypes.windll.dwmapi.DwmGetWindowAttribute(
                ctypes.c_void_p(hwnd), DWMWA_CLOAKED,
                ctypes.byref(cloaked), ctypes.sizeof(cloaked)
            )
            if cloaked.value != 0:
                return True
        except Exception:
            pass
        result.append(int(hwnd))
        return True

    user32.EnumWindows(EnumProc(_cb), 0)
    return result


def _activate_window(hwnd: int) -> None:
    user32 = ctypes.windll.user32
    SW_RESTORE = 9
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
    fg = user32.GetForegroundWindow()
    cur_tid = ctypes.windll.kernel32.GetCurrentThreadId()
    fg_tid = user32.GetWindowThreadProcessId(fg, None)
    tgt_tid = user32.GetWindowThreadProcessId(ctypes.c_void_p(hwnd), None)
    try:
        if fg_tid:
            user32.AttachThreadInput(cur_tid, fg_tid, True)
        user32.AttachThreadInput(cur_tid, tgt_tid, True)
        user32.BringWindowToTop(ctypes.c_void_p(hwnd))
        user32.SetForegroundWindow(ctypes.c_void_p(hwnd))
    finally:
        if fg_tid:
            user32.AttachThreadInput(cur_tid, fg_tid, False)
        user32.AttachThreadInput(cur_tid, tgt_tid, False)


def _cycle_window(direction: int = 1) -> None:
    """Activează următoarea / anterioara fereastră deschisă."""
    user32 = ctypes.windll.user32
    user32.GetForegroundWindow.restype = ctypes.c_void_p
    wins = _enum_alt_tab_windows()
    if not wins:
        return
    fg = int(user32.GetForegroundWindow() or 0)
    if fg in wins:
        idx = wins.index(fg)
        nxt = wins[(idx + direction) % len(wins)]
    else:
        nxt = wins[0] if direction > 0 else wins[-1]
    _activate_window(nxt)


def _run_control_thread(fn, label: str) -> None:
    def _wrap():
        try:
            fn()
        except Exception as e:
            log(f"remote_control {label}: {e}")
            log(traceback.format_exc())

    threading.Thread(target=_wrap, daemon=True).start()


def _qs_int(qs: dict, key: str, default: int = 0) -> int:
    for k in (key, key.upper()):
        v = qs.get(k)
        if v and str(v[0]).strip() != "":
            try:
                return int(float(str(v[0]).strip()))
            except ValueError:
                pass
    return default


def _sendkeys_wait(seq: str) -> None:
    """Sintaxă .NET SendKeys (ex. ^{HOME}, %+{TAB}, ^+i)."""
    if not seq:
        return
    safe = seq.replace("'", "''")
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        f"[System.Windows.Forms.SendKeys]::SendWait('{safe}')"
    )
    run_hidden(["powershell", "-NoProfile", "-Command", ps])


def _volume_key(direction: str) -> None:
    u = ctypes.windll.user32
    vk = {"up": 0xAF, "down": 0xAE, "mute": 0xAD}.get(direction, 0xAF)
    u.keybd_event(vk, 0, 0, 0)
    u.keybd_event(vk, 0, _KEYEVENTF_KEYUP, 0)


def _media_key(which: str) -> None:
    """Taste media globale Windows (next/prev/play-pause/stop)."""
    u = ctypes.windll.user32
    vk = {
        "next": 0xB0,   # VK_MEDIA_NEXT_TRACK
        "prev": 0xB1,   # VK_MEDIA_PREV_TRACK
        "stop": 0xB2,   # VK_MEDIA_STOP
        "play": 0xB3,   # VK_MEDIA_PLAY_PAUSE
    }.get(which, 0xB3)
    u.keybd_event(vk, 0, 0, 0)
    u.keybd_event(vk, 0, _KEYEVENTF_KEYUP, 0)


def _type_text(text: str) -> None:
    """Scrie text arbitrar în fereastra activă, prin .NET SendKeys.

    Caracterele speciale SendKeys ( + ^ % ~ ( ) [ ] { } ) sunt escapate,
    iar liniile noi devin {ENTER}.
    """
    if not text:
        return
    special = set("+^%~(){}[]")
    out = []
    for ch in text:
        if ch == "\r":
            continue
        if ch == "\n":
            out.append("{ENTER}")
        elif ch in special:
            out.append("{" + ch + "}")
        else:
            out.append(ch)
    seq = "".join(out)
    safe = seq.replace("'", "''")
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        f"[System.Windows.Forms.SendKeys]::SendWait('{safe}')"
    )
    run_hidden(["powershell", "-NoProfile", "-Command", ps])


# Lock global pentru a serializa comenzile de mouse (down/move/up).
# Esențial pentru drag-select: garantează ordinea down -> move -> up.
_MOUSE_LOCK = threading.Lock()


def _run_mouse_sync(fn, label: str) -> None:
    """Execută o comandă de mouse SINCRON și serializat (cu lock).

    Spre deosebire de _run_control_thread, NU pornește un thread nou, ca
    ordinea comenzilor (mouse_down, mouse_relative..., mouse_up) să fie
    garantată. Apelurile mouse_event sunt instantanee, deci nu blochează HTTP.
    """
    try:
        with _MOUSE_LOCK:
            fn()
    except Exception as e:
        log(f"remote_control {label}: {e}")
        log(traceback.format_exc())


def _mouse_left_click() -> None:
    u = ctypes.windll.user32
    u.mouse_event(0x0002, 0, 0, 0, 0)
    u.mouse_event(0x0004, 0, 0, 0, 0)


def _mouse_left_down() -> None:
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)


def _mouse_left_up() -> None:
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)


def _mouse_right_click() -> None:
    u = ctypes.windll.user32
    u.mouse_event(0x0008, 0, 0, 0, 0)
    u.mouse_event(0x0010, 0, 0, 0, 0)


def _mouse_double_click() -> None:
    _mouse_left_click()
    time.sleep(0.04)
    _mouse_left_click()


def _mouse_wheel(delta: int) -> None:
    ctypes.windll.user32.mouse_event(0x0800, 0, 0, int(delta), 0)


def _mouse_set_pos(x: int, y: int) -> None:
    ctypes.windll.user32.SetCursorPos(int(x), int(y))


def _mouse_move_rel(dx: int, dy: int) -> None:
    ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)


# Comenzi doar tastatură — același set ca index.html (fără ESP).
_REMOTE_SENDKEYS: dict[str, str] = {
    "enter": "{ENTER}",
    "escape": "{ESC}",
    "tab": "{TAB}",
    "shift_tab": "+{TAB}",
    "space": " ",
    "backspace": "{BS}",
    "delete": "{DEL}",
    "arrow_up": "{UP}",
    "arrow_down": "{DOWN}",
    "arrow_left": "{LEFT}",
    "arrow_right": "{RIGHT}",
    "f4": "{F4}",
    "f5": "{F5}",
    "f11": "{F11}",
    "f12": "{F12}",
    "select_all": "^a",
    "select_word": "^+{RIGHT}",
    "select_line": "{HOME}+{END}",
    "copy": "^c",
    "paste": "^v",
    "back": "%{LEFT}",
    "forward": "%{RIGHT}",
    "browser_back": "%{LEFT}",
    "browser_forward": "%{RIGHT}",
    "scroll_page_up": "{PGUP}",
    "scroll_page_down": "{PGDN}",
    "scroll_top": "^{HOME}",
    "scroll_bottom": "^{END}",
    "ctrl_shift_i": "^+i",
    "ctrl_r": "^r",
}


def remote_control_dispatch(cmd: str, qs: dict) -> dict:
    """
    Comenzi GET /?c=... — același protocol ca index.html (ESP / browser).
    sleep, hibernate, turn_off, screenshot, alt_tab, minimize, maximize, etc.
    """
    c = (cmd or "").strip().lower().replace("-", "_")

    def ok(action: str, detail: str = "") -> dict:
        log(f"🎮 remote_control: {action}" + (f" | {detail}" if detail else ""))
        return {"ok": True, "action": action, "detail": detail or action}

    # --- oprire / energie (rulare în thread ca HTTP să răspundă înainte de sleep/shutdown) ---
    if c in ("sleep", "standby", "suspend"):
        def _sleep():
            run_hidden(
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"]
            )

        _run_control_thread(_sleep, "sleep")
        return ok("sleep")

    if c in ("hibernate", "hiber"):
        def _hib():
            run_hidden(["shutdown", "/h"])

        _run_control_thread(_hib, "hibernate")
        return ok("hibernate")

    if c in ("turn_off", "shutdown", "power_off", "off"):
        def _off():
            run_hidden(["shutdown", "/s", "/f", "/t", "0"])

        _run_control_thread(_off, "shutdown")
        return ok("turn_off")

    if c in ("screenshot", "prtsc", "print_screen"):
        def _shot():
            ps = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')"
            )
            run_hidden(["powershell", "-NoProfile", "-Command", ps])

        _run_control_thread(_shot, "screenshot")
        return ok("screenshot")

    if c in ("alt_tab", "alttab", "alt-tab"):
        def _at():
            ps = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.SendKeys]::SendWait('%{TAB}')"
            )
            run_hidden(["powershell", "-NoProfile", "-Command", ps])

        _run_control_thread(_at, "alt_tab")
        return ok("alt_tab")

    if c in ("minimize", "minimise"):
        _run_control_thread(_win_minimize_foreground, "minimize")
        return ok("minimize")

    if c in ("maximize", "maximise"):
        _run_control_thread(_win_maximize_foreground, "maximize")
        return ok("maximize")

    if c in ("close_window", "close"):
        _run_control_thread(_win_close_foreground, "close_window")
        return ok("close_window")

    if c in ("show_desktop", "desktop", "minimize_all"):
        _run_control_thread(_toggle_show_desktop, "show_desktop")
        return ok("show_desktop")

    # --- comutare între ferestrele deschise (taskbar) ---
    if c in ("cycle_window", "next_window", "window_next", "switch_window"):
        _run_control_thread(lambda: _cycle_window(1), "cycle_window")
        return ok("cycle_window")
    if c in ("cycle_window_prev", "prev_window", "window_prev"):
        _run_control_thread(lambda: _cycle_window(-1), "cycle_window_prev")
        return ok("cycle_window_prev")

    # --- volum (taste media Windows) ---
    if c in ("volume_up", "vol_up"):
        _run_control_thread(lambda: _volume_key("up"), "volume_up")
        return ok("volume_up")
    if c in ("volume_down", "vol_down"):
        _run_control_thread(lambda: _volume_key("down"), "volume_down")
        return ok("volume_down")
    if c in ("volume_mute", "mute"):
        _run_control_thread(lambda: _volume_key("mute"), "volume_mute")
        return ok("volume_mute")

    # --- taste media (next / prev / play-pause / stop) ---
    if c in ("next_track", "media_next", "next"):
        _run_control_thread(lambda: _media_key("next"), "next_track")
        return ok("next_track")
    if c in ("prev_track", "media_prev", "previous", "prev"):
        _run_control_thread(lambda: _media_key("prev"), "prev_track")
        return ok("prev_track")
    if c in ("media_play_pause", "media_play"):
        _run_control_thread(lambda: _media_key("play"), "media_play_pause")
        return ok("media_play_pause")
    if c in ("media_stop",):
        _run_control_thread(lambda: _media_key("stop"), "media_stop")
        return ok("media_stop")

    # --- scrie text arbitrar în fereastra activă ---
    if c in ("type", "type_text", "text"):
        txt = ""
        for key in ("text", "t", "TEXT"):
            v = qs.get(key)
            if v:
                txt = str(v[0])
                break
        _run_control_thread(lambda: _type_text(txt), "type")
        return ok("type", (txt[:40] + "…") if len(txt) > 40 else txt)

    # --- mouse poziție / click (înlocuiește ESP pentru același protocol) ---
    if c == "mouse_absolute":
        x = _qs_int(qs, "x", 0)
        y = _qs_int(qs, "y", 0)
        _run_mouse_sync(lambda: _mouse_set_pos(x, y), "mouse_absolute")
        return ok("mouse_absolute", f"x={x} y={y}")

    if c == "mouse_relative":
        dx = _qs_int(qs, "dx", 0)
        dy = _qs_int(qs, "dy", 0)
        _run_mouse_sync(lambda: _mouse_move_rel(dx, dy), "mouse_relative")
        return ok("mouse_relative", f"dx={dx} dy={dy}")

    if c == "click":
        _run_mouse_sync(_mouse_left_click, "click")
        return ok("click")
    if c in ("mouse_down", "left_down", "drag_start"):
        _run_mouse_sync(_mouse_left_down, "mouse_down")
        return ok("mouse_down")
    if c in ("mouse_up", "left_up", "drag_end"):
        _run_mouse_sync(_mouse_left_up, "mouse_up")
        return ok("mouse_up")
    if c in ("double_click", "dblclick"):
        _run_mouse_sync(_mouse_double_click, "double_click")
        return ok("double_click")
    if c in ("right_click", "rightclick"):
        _run_mouse_sync(_mouse_right_click, "right_click")
        return ok("right_click")

    # --- scroll cu valoare variabilă (rotiță) — pentru 2 degete pe trackpad ---
    if c in ("mouse_wheel", "wheel", "scroll"):
        delta = _qs_int(qs, "delta", 0)
        if delta == 0:
            delta = _qs_int(qs, "dy", 0)
        _run_mouse_sync(lambda: _mouse_wheel(delta), "mouse_wheel")
        return ok("mouse_wheel", f"delta={delta}")

    # --- scroll (rotiță) ---
    if c == "scroll_fast_up":
        _run_control_thread(lambda: _mouse_wheel(240), "scroll_fast_up")
        return ok("scroll_fast_up")
    if c == "scroll_fast_down":
        _run_control_thread(lambda: _mouse_wheel(-240), "scroll_fast_down")
        return ok("scroll_fast_down")

    # --- redare media ---
    if c in ("play_pause", "playpause", "play", "pause"):
        _run_control_thread(lambda: _sendkeys_wait(" "), "play_pause")
        return ok("play_pause", "space")

    # --- fullscreen ---
    # Universal pentru video: dublu-click in centrul ecranului
    # (merge pe YouTube, VLC, Netflix, playere HTML5).
    if c in ("fullscreen_video", "fs_video"):
        def _fs_video():
            try:
                sw = ctypes.windll.user32.GetSystemMetrics(0)
                sh = ctypes.windll.user32.GetSystemMetrics(1)
            except Exception:
                sw, sh = 1920, 1080
            _mouse_set_pos(sw // 2, sh // 2)
            time.sleep(0.04)
            _mouse_double_click()
        _run_control_thread(_fs_video, "fullscreen_video")
        return ok("fullscreen_video", "double_click center")

    # Fullscreen pe player web (tasta F, ex. YouTube)
    if c in ("fullscreen", "fs"):
        _run_control_thread(lambda: _sendkeys_wait("f"), "fullscreen")
        return ok("fullscreen", "key f")

    # Fullscreen browser / aplicatie (F11)
    if c in ("fullscreen_f11", "fs_f11"):
        _run_control_thread(lambda: _sendkeys_wait("{F11}"), "fullscreen_f11")
        return ok("fullscreen_f11", "F11")

    # Iesire din fullscreen (Esc)
    if c in ("exit_fullscreen", "fs_exit"):
        _run_control_thread(lambda: _sendkeys_wait("{ESC}"), "exit_fullscreen")
        return ok("exit_fullscreen", "Esc")

    sk = _REMOTE_SENDKEYS.get(c)
    if sk is not None:
        _run_control_thread(lambda s=sk: _sendkeys_wait(s), c)
        return ok(c, "sendkeys")

    return {
        "ok": False,
        "error": "unknown_command",
        "cmd": cmd,
        "hint": "See remote_control_dispatch: power, window, volume, mouse, keys, scroll",
    }


def run_hidden(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
    )

def port_listener_pid(port: int) -> int | None:
    """PID-ul procesului care LISTEN pe port (Windows)."""
    try:
        r = run_hidden(["cmd", "/c", f"netstat -ano | findstr :{port}"])
        out = (r.stdout or "").splitlines()
        for line in out:
            line = line.strip()
            if "LISTENING" in line.upper():
                parts = re.split(r"\s+", line)
                if len(parts) >= 5 and parts[-1].isdigit():
                    return int(parts[-1])
    except Exception:
        pass
    return None

# =========================
# WINDOW CONTROL (optional)
# =========================
WINDOW_CONTROL = False
CONTROL_METHOD = "NONE"

try:
    import win32gui
    import win32con
    import win32process
    WINDOW_CONTROL = True
    CONTROL_METHOD = "WIN32"
    log("✅ WIN32 window control: LOADED")
except ImportError:
    try:
        import pygetwindow as gw
        WINDOW_CONTROL = True
        CONTROL_METHOD = "PYGETWINDOW"
        log("✅ pygetwindow: LOADED")
    except ImportError:
        log("⚠️  No window control. Auto-focus disabled.")

def _force_foreground_win32(hwnd: int) -> bool:
    try:
        if hwnd == 0:
            return False
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.03)
        flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)

        fg = win32gui.GetForegroundWindow()
        try:
            tid_fg, _ = win32process.GetWindowThreadProcessId(fg)
        except Exception:
            tid_fg = None
        tid_hw, _ = win32process.GetWindowThreadProcessId(hwnd)

        if tid_fg and tid_fg != tid_hw:
            try:
                win32process.AttachThreadInput(tid_fg, tid_hw, True)
            except Exception:
                pass

        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

        if tid_fg and tid_fg != tid_hw:
            try:
                win32process.AttachThreadInput(tid_fg, tid_hw, False)
            except Exception:
                pass

        return True
    except Exception:
        return False

def _find_window_win32(app_key: str, pid: int | None, timeout: float) -> int | None:
    pattern = (WINDOW_PATTERNS.get(app_key) or "").strip().lower()
    start = time.time()

    def enum_cb(hwnd, results):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = (win32gui.GetWindowText(hwnd) or "").strip()
            if not title:
                return
            _, this_pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid and this_pid == pid:
                results.append((0, hwnd, title))
                return
            if pattern and pattern in title.lower():
                results.append((1, hwnd, title))
        except Exception:
            return

    while time.time() - start < timeout:
        found = []
        win32gui.EnumWindows(enum_cb, found)
        if found:
            found.sort(key=lambda x: x[0])
            return int(found[0][1])
        time.sleep(FOCUS_CHECK_INTERVAL)
    return None

def focus_app_window(app_key: str, pid: int | None) -> bool:
    if not WINDOW_CONTROL or app_key in SKIP_FOCUS:
        return False
    timeout = float(SLOW_APPS.get(app_key, DEFAULT_FOCUS_TIMEOUT))
    time.sleep(FOCUS_INITIAL_DELAY)
    if CONTROL_METHOD == "WIN32":
        hwnd = _find_window_win32(app_key, pid, timeout)
        if not hwnd:
            return False
        for _ in range(3):
            if _force_foreground_win32(hwnd):
                return True
            time.sleep(0.05)
    return False

# =========================
# PROCESS MANAGEMENT (REAL)
# =========================
def pids_by_image(image_name: str) -> list[int]:
    """PID-uri via CIM (merge și la 'Arduino IDE.exe')."""
    img = (image_name or "").strip()
    if not img:
        return []
    img_ps = img.replace("'", "''")
    ps = (
        f"$p = Get-CimInstance Win32_Process -Filter \"Name='{img_ps}'\"; "
        "if ($p) { $p | Select-Object -ExpandProperty ProcessId }"
    )
    r = run_hidden(["powershell", "-NoProfile", "-Command", ps])
    out = (r.stdout or "").strip()
    if not out:
        return []
    pids = []
    for line in out.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return sorted(set(pids))

def is_running_image(image_name: str) -> bool:
    return len(pids_by_image(image_name)) > 0

def kill_pid(pid: int, force: bool = True) -> tuple[bool, str]:
    if pid <= 0:
        return False, "Invalid PID"

    cmd = ["taskkill", "/PID", str(pid), "/T"]
    if force:
        cmd.insert(1, "/F")

    r = run_hidden(cmd)
    msg = (r.stderr or r.stdout or "").strip()
    low = msg.lower()

    if "not found" in low or "no running instance of the task" in low:
        return True, f"PID {pid} already closed"

    return (r.returncode == 0), (msg or f"rc={r.returncode}")

def kill_image(image_name: str, force: bool = True) -> tuple[bool, str]:
    cmd = ["taskkill", "/IM", image_name, "/T"]
    if force:
        cmd.insert(1, "/F")
    r = run_hidden(cmd)
    msg = (r.stderr or r.stdout or "").strip()
    return (r.returncode == 0), (msg or f"rc={r.returncode}")

def kill_process_smart(image_name: str, force: bool = True) -> tuple[bool, str]:
    if not is_running_image(image_name):
        return False, f"Process '{image_name}' not running"

    ok, msg = kill_image(image_name, force=force)

    if is_running_image(image_name):
        errs = []
        for pid in pids_by_image(image_name):
            okp, msgp = kill_pid(pid, force=force)
            if not okp:
                errs.append(f"PID {pid}: {msgp}")
        if errs:
            msg = (msg + " | " if msg else "") + " | ".join(errs)

    if is_running_image(image_name):
        return False, "Process still running after kill | " + (msg or "")

    return True, msg or f"Process '{image_name}' terminated"

def window_pid_by_pattern(app_key: str) -> int | None:
    """Găsește PID-ul ferestrei după pattern (pentru UWP apps)."""
    if not WINDOW_CONTROL or CONTROL_METHOD != "WIN32":
        return None

    pattern = (WINDOW_PATTERNS.get(app_key) or "").strip().lower()
    if not pattern:
        return None

    hits = []

    def enum_cb(hwnd, results):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = (win32gui.GetWindowText(hwnd) or "").strip()
            if not title:
                return
            if pattern in title.lower():
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid:
                    results.append((hwnd, pid, title))
        except Exception:
            return

    win32gui.EnumWindows(enum_cb, hits)
    if not hits:
        return None

    return int(hits[0][1])

def check_app_status(app_key: str) -> dict:
    process_name = PROCESS_NAMES.get(app_key)

    if process_name:
        running = is_running_image(process_name)
        if running:
            pids = pids_by_image(process_name)
            return {
                "app": app_key,
                "process": process_name,
                "running": True,
                "pids": pids,
                "method": "image"
            }

    pidw = window_pid_by_pattern(app_key)
    if pidw:
        return {
            "app": app_key,
            "process": "WINDOW",
            "running": True,
            "pid": pidw,
            "method": "window"
        }

    return {
        "app": app_key,
        "process": process_name or "",
        "running": False,
        "method": "none"
    }

def kill_app(app_key: str) -> tuple[bool, dict]:
    image = PROCESS_NAMES.get(app_key)

    if not image:
        pidw = window_pid_by_pattern(app_key)
        if pidw:
            okW, msgW = kill_pid(pidw, force=True)
            return okW, {
                "ok": okW,
                "app": app_key,
                "process": "WINDOW",
                "pid": pidw,
                "message": msgW
            }
        return False, {
            "ok": False,
            "app": app_key,
            "error": "No process configured (and no window match)"
        }

    with _last_pid_lock:
        meta = LAST_PIDS.get(app_key) or {}
        pid = int(meta.get("pid") or 0)

    log(f"⚡ KILL: {app_key} ({image})" + (f" [pid={pid}]" if pid else ""))

    messages: list[str] = []

    def still_running() -> bool:
        return is_running_image(image)

    if pid:
        okp, msgp = kill_pid(pid, force=True)
        messages.append(f"pid:{pid} -> {msgp}")
        time.sleep(0.10)

    ok_final = True
    if still_running():
        ok2, msg2 = kill_process_smart(image, force=True)
        messages.append(f"image:{image} -> {msg2}")
        ok_final = ok2
        time.sleep(0.10)

    if still_running():
        pidw = window_pid_by_pattern(app_key)
        if pidw:
            okW, msgW = kill_pid(pidw, force=True)
            messages.append(f"windowpid:{pidw} -> {msgW}")
            ok_final = okW
            time.sleep(0.10)

    if still_running():
        err = "Still running | " + " || ".join(messages)
        if "access is denied" in err.lower():
            err += " | Rulează serverul ca Administrator (UAC)."
        return False, {
            "ok": False,
            "app": app_key,
            "process": image,
            "error": err,
            "pids": pids_by_image(image),
        }

    with _last_pid_lock:
        LAST_PIDS.pop(app_key, None)

    return True, {
        "ok": True,
        "app": app_key,
        "process": image,
        "message": " || ".join(messages)
    }

def kill_all_apps(unsafe: bool = False) -> dict:
    """Kill toate aplicațiile din listă (except browsers dacă unsafe=False)."""
    results = []
    for key in APPS.keys():
        image = PROCESS_NAMES.get(key)
        if not image:
            continue
        if not unsafe and image in PROTECT_FROM_KILLALL_IMAGES:
            continue
        if is_running_image(image):
            ok, res = kill_app(key)
            results.append({"key": key, "ok": ok, "result": res})
    return {"ok": True, "results": results}

# =========================
# APP KEY RESOLUTION
# =========================
def normalize_key(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s

APP_ALIASES: dict[str, str] = {normalize_key(k): k for k in APPS.keys()}

def resolve_app_key(app_raw: str) -> str | None:
    return APP_ALIASES.get(normalize_key(app_raw))

# =========================
# LAUNCH
# =========================
def launch_windows(cmd: str) -> int | None:
    """Lansează comandă/aplicație Windows. Returnează PID sau None."""
    v = (cmd or "").strip()
    if not v:
        raise RuntimeError("Empty command")

    p = Path(v)
    log(f"LAUNCH_CMD_RAW: {v}")

    # Web URLs
    if v.lower().startswith(("http://", "https://")):
        log(f"Opening URL: {v}")
        webbrowser.open(v)
        return None

    # Shell commands (UWP apps, folders, etc)
    if v.lower().startswith("shell:"):
        log(f"Opening shell: {v}")
        subprocess.Popen(["explorer.exe", v], shell=False)
        return None

    # Real file paths
    if p.exists():
        log(f"LAUNCH_EXISTS: {p.exists()} | is_file={p.is_file()}")
        vv = v.lower()
        if vv.endswith(".exe"):
            try:
                proc = subprocess.Popen([v], shell=False)
                return int(proc.pid)
            except (PermissionError, OSError) as e:
                # FIX: WindowsApps/MS Store executables pot refuza Popen.
                log(f"⚠️ EXE Popen failed, fallback to startfile: {e}")
                os.startfile(v)  # type: ignore
                return None

        # .lnk, .html, etc - use os.startfile
        os.startfile(v)  # type: ignore
        return None

    # Dacă arată ca un path absolut (C:\...) dar nu există → eroare clară
    if re.match(r'^[A-Za-z]:[\\\/]', v):
        raise RuntimeError(f"File not found: {v}")

    # Command-line tools (notepad, calc, python, etc)
    parts = shlex.split(v, posix=False)
    log(f"LAUNCH_PARTS: {parts}")

    try:
        proc = subprocess.Popen(parts, shell=False)
        return int(proc.pid)
    except FileNotFoundError as e:
        raise RuntimeError(
            f"WinError2: Command not found: {parts[0]} | cmd='{v}'"
        ) from e

def pid_started_after(image_name: str, t0: float, wait_sec: float = 3.0) -> int | None:
    """Găsește PID-ul procesului lansat după timpul t0."""
    if not image_name:
        return None

    deadline = time.time() + wait_sec
    ft = int(t0 * 10_000_000) + 116444736000000000

    while time.time() < deadline:
        img_ps = image_name.replace("'", "''")
        ps = rf"""
        $name = '{img_ps}';
        $since = [DateTime]::FromFileTimeUtc([Int64]{ft});
        $p = Get-CimInstance Win32_Process -Filter "Name='$name'" |
             Where-Object {{ $_.CreationDate -ge $since }} |
             Sort-Object CreationDate -Descending |
             Select-Object -First 1;
        if ($p) {{ $p.ProcessId }}
        """
        r = run_hidden(["powershell", "-NoProfile", "-Command", ps])
        out = (r.stdout or "").strip()
        if out.isdigit():
            return int(out)
        time.sleep(0.10)

    return None

def launch_app(app_raw: str):
    key = resolve_app_key(app_raw)
    if not key:
        return False, {
            "ok": False,
            "error": "App not recognized",
            "app_raw": app_raw
        }

    cmd = APPS.get(key)
    if not cmd:
        return False, {
            "ok": False,
            "error": "App not configured",
            "key": key
        }

    if cmd == "__LAUNCHER_FINAL_WITH_SOUND__":
        hp = BASE_DIR / "Launcher_FINAL_WITH_SOUND.html"
        cmd = hp.as_uri() if hp.is_file() else ""

    log(f"⚡ LAUNCH: {key}")

    try:
        t0 = time.time()
        pid = launch_windows(cmd)

        img = PROCESS_NAMES.get(key)
        if img and (not isinstance(pid, int) or pid <= 0):
            pid_real = pid_started_after(img, t0, wait_sec=3.0)
            if pid_real:
                pid = pid_real

        with _last_pid_lock:
            LAST_PIDS[key] = {
                "pid": int(pid) if isinstance(pid, int) else 0,
                "t0": t0
            }

        if key in SKIP_FOCUS:
            return True, {
                "ok": True,
                "key": key,
                "pid": pid,
                "focus": "skipped"
            }

        if WINDOW_CONTROL:
            threading.Thread(
                target=lambda: focus_app_window(
                    key, pid if isinstance(pid, int) else None
                ),
                daemon=True
            ).start()
            return True, {
                "ok": True,
                "key": key,
                "pid": pid,
                "focus": "scheduled"
            }

        return True, {"ok": True, "key": key, "pid": pid}

    except Exception as e:
        log(f"   ❌ FAILED: {e}")
        log(traceback.format_exc())
        return False, {"ok": False, "key": key, "error": str(e)}

# =========================
# HTTP HANDLER
# =========================
class H(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, status: int, obj: dict):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def _send_bytes(self, status: int, data: bytes, ctype: str, no_cache: bool = False):
        self.send_response(status)
        self.send_header("Content-type", ctype)
        if no_cache:
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, status: int, text: str):
        self._send_bytes(status, text.encode("utf-8"), "text/plain; charset=utf-8")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            qs = parse_qs(parsed.query)

            if path in ("/ping", "/health"):
                self._send_json(200, {
                    "status": "ok",
                    "kill_support": True,
                    "admin": is_admin(),
                    "pid": os.getpid()
                })
                return

            # ---------- remote control (?c=) — index.html / ESP ----------
            if path == "/":
                c_vals = qs.get("c") or qs.get("C")
                if c_vals and str(c_vals[0]).strip():
                    payload = remote_control_dispatch(str(c_vals[0]).strip(), qs)
                    self._send_json(200, payload)
                    return

            if path == "/online":
                self._send_json(200, {
                    "online": True,
                    "uptime_sec": round(time.time() - SERVER_STARTED_AT, 2),
                    "admin": is_admin(),
                    "pid": os.getpid(),
                    "ip": LOCAL_IP,
                    "port": PORT
                })
                return

            if path == "/favicon.ico":
                ico = BASE_DIR / "favicon.ico"
                if ico.is_file():
                    self._send_bytes(200, ico.read_bytes(), "image/x-icon")
                else:
                    self._send_bytes(204, b"", "image/x-icon")
                return

            # ---------- stop ----------
            if path == "/stop":
                token = (qs.get("token") or [""])[0]
                if token != STOP_TOKEN:
                    self._send_json(200, {"ok": False, "error": "Bad token"})
                    return

                self._send_json(200, {
                    "ok": True,
                    "message": "Server shutting down..."
                })

                def _shutdown():
                    time.sleep(0.3)
                    try:
                        if HTTPD_REF:
                            HTTPD_REF.shutdown()
                    except Exception:
                        pass

                threading.Thread(target=_shutdown, daemon=True).start()
                return

            if path == "/m":
                host = self.headers.get("Host", f"{LOCAL_IP}:{PORT}")
                self.send_response(302)
                self.send_header("Location", f"http://{host}/local/index.html")
                self._cors()
                self.end_headers()
                return

            # ---------- app management ----------
            if path == "/status":
                app = (qs.get("app") or [None])[0]
                if not app:
                    self._send_json(200, {"ok": False, "error": "No app"})
                    return
                key = resolve_app_key(app)
                if not key:
                    self._send_json(200, {
                        "ok": False,
                        "error": "App not recognized",
                        "app_raw": app
                    })
                    return
                data = check_app_status(key)
                data["ok"] = True
                self._send_json(200, data)
                return

            if path == "/kill":
                app = (qs.get("app") or [None])[0]
                if not app:
                    self._send_json(200, {"ok": False, "error": "No app"})
                    return
                key = resolve_app_key(app)
                if not key:
                    self._send_json(200, {
                        "ok": False,
                        "error": "App not recognized",
                        "app_raw": app
                    })
                    return
                if not is_admin():
                    self._send_json(200, {
                        "ok": False,
                        "error": "Server not elevated. Run as Administrator (UAC)."
                    })
                    return

                ok, result = kill_app(key)
                self._send_json(200, result)
                return

            if path == "/killall":
                unsafe = (qs.get("unsafe") or ["0"])[0] in ("1", "true", "yes", "on")
                if not is_admin():
                    self._send_json(200, {
                        "ok": False,
                        "error": "Server not elevated. Run as Administrator (UAC)."
                    })
                    return
                result = kill_all_apps(unsafe=unsafe)
                self._send_json(200, result)
                return

            if path == "/launch":
                app_raw = (qs.get("app") or [None])[0]
                if not app_raw:
                    self._send_json(200, {"ok": False, "error": "No app"})
                    return
                _, payload = launch_app(app_raw)
                self._send_json(200, payload)
                return

            if path == "/api/apps":
                apps_list = [
                    {"key": k, "cmd": APPS[k]}
                    for k in sorted(APPS.keys())
                ]
                self._send_json(200, {"apps": apps_list})
                return

            # ---------- static files ----------
            if path.startswith("/sounds/"):
                fn = path[8:].lstrip("/")
                target = (SOUNDS_DIR / fn).resolve()
                if (not str(target).startswith(str(SOUNDS_DIR))) or (not target.is_file()):
                    self._send_text(404, "Not found")
                    return
                self._send_bytes(
                    200,
                    target.read_bytes(),
                    mimetypes.guess_type(str(target))[0] or "audio/mpeg"
                )
                return

            if path.startswith("/local"):
                rel = path[7:] or "/index.html"
                target = (LOCAL_ROOT / rel.lstrip("/")).resolve()
                if (not str(target).startswith(str(LOCAL_ROOT))) or (not target.is_file()):
                    self._send_text(404, "Not found")
                    return
                mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
                bust_cache = mime.startswith("text/html") or mime in (
                    "application/javascript",
                    "text/css",
                    "application/json",
                )
                self._send_bytes(200, target.read_bytes(), mime, no_cache=bust_cache)
                return

            if path in ("/", "/index.html"):
                html_path = BASE_DIR / LAUNCHER_HTML
                if not html_path.is_file():
                    self._send_text(404, "Launcher HTML not found")
                    return
                self._send_bytes(
                    200,
                    html_path.read_bytes(),
                    "text/html; charset=utf-8",
                    no_cache=True,
                )
                return

            self._send_text(404, "Not Found")

        except Exception as e:
            log("❌ do_GET exception: " + repr(e))
            log(traceback.format_exc())
            try:
                self._send_json(200, {"ok": False, "error": str(e)})
            except Exception:
                pass

# =========================
# MAIN
# =========================
def main():
    global HTTPD_REF

    # 1) auto-elevate (UAC)
    ensure_admin_or_relaunch()

    # 2) verifică dacă portul e ocupat
    listener = port_listener_pid(PORT)
    if listener and listener != os.getpid():
        log(f"❌ PORT {PORT} already in use by PID={listener}.")
        log(f"   Stop that process: taskkill /F /PID {listener} /T")
        input("Press ENTER to exit...")
        return

    log("=" * 70)
    log("🚀 FIRE & FORGET - SERVER CORRECTED")
    log("=" * 70)
    log(f"🏠 Local:  http://127.0.0.1:{PORT}/")
    log(f"📱 Mobile: http://{LOCAL_IP}:{PORT}/")
    log(f"📱 Panou System Control (telefon): http://{LOCAL_IP}:{PORT}/local/index.html")
    log(f"🛑 Kill support: {'ENABLED' if is_admin() else 'DISABLED (not admin)'}")
    log(f"ADMIN CHECK: {is_admin()}")
    log(f"PID SERVER: {os.getpid()}")
    log("=" * 70)

    try:
        httpd = HTTPServer(("0.0.0.0", PORT), H)
        HTTPD_REF = httpd

        # Auto-open browser după 3 secunde
        threading.Thread(
            target=lambda: (
                time.sleep(3),
                webbrowser.open(f"http://127.0.0.1:{PORT}/")
            ),
            daemon=True
        ).start()

        log("✅ Server STARTED!")
        httpd.serve_forever()

    except KeyboardInterrupt:
        log("🛑 Stopped (Ctrl+C)")
    except Exception as e:
        log(f"❌ Error: {e}")
        log(traceback.format_exc())
        input("\nPress ENTER to exit...")
    finally:
        try:
            if HTTPD_REF:
                HTTPD_REF.server_close()
        except Exception:
            pass

if __name__ == "__main__":
    try:
        main()
    except Exception:
        log(traceback.format_exc())
        input("\nPress ENTER to exit...")
