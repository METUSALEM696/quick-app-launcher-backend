#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIRE AND FORGET - AUTOSTART WRAPPER
Porneste serverul + deschide 3 browser-e automat
"""

import os
import sys
import time
import subprocess
import ctypes
from pathlib import Path

# O singură rulare per sesiune — evită 2× tab-uri când Task Scheduler are Boot+Logon sau dublu Run.
_ERROR_ALREADY_EXISTS = 183
_AUTOSTART_MUTEX = "Local\\QuickAppAutostartWithBrowsersOnce"


def _acquire_autostart_mutex() -> bool:
    h = ctypes.windll.kernel32.CreateMutexW(None, False, _AUTOSTART_MUTEX)
    if not h:
        return False
    if ctypes.windll.kernel32.GetLastError() == _ERROR_ALREADY_EXISTS:
        ctypes.windll.kernel32.CloseHandle(h)
        return False
    return True


# ═════════════════════════════════════════════════════════════════════
# CONFIGURATION (același folder ca acest script — P: sau E:)
# ═════════════════════════════════════════════════════════════════════

_THIS_DIR = Path(__file__).resolve().parent
_FINAL_HTML = _THIS_DIR / "Launcher_FINAL_WITH_SOUND.html"
_FILE_URI = _FINAL_HTML.as_uri()  # file:///P:/... sau E:/...

CONFIG = {
    "SERVER_SCRIPT": str(_THIS_DIR / "server_fire_and_forget.py"),
    "WORKING_DIR": str(_THIS_DIR),
    "SERVER_PORT": 8899,
    "BROWSER_DELAY": 5,  # seconds to wait before opening browsers
    "LOCALHOST_URL": "http://localhost:8899/",
    "LOCAL_FILE_URL": _FILE_URI,
    "GITHUB_PAGES_URL": "https://metusalem696.github.io/quick-app-launcher/",
}

# ═════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def start_server():
    """Start the HTTP server in background"""
    try:
        # Start server using pythonw.exe (no console window)
        pythonw = sys.executable.replace('python.exe', 'pythonw.exe')
        
        subprocess.Popen(
            [pythonw, CONFIG['SERVER_SCRIPT']],
            cwd=CONFIG['WORKING_DIR'],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

def check_server_running():
    """Check if server is running"""
    try:
        import psutil
        for conn in psutil.net_connections():
            if conn.laddr.port == CONFIG['SERVER_PORT'] and conn.status == 'LISTEN':
                return True
        return False
    except:
        # Fallback: use netstat
        try:
            result = subprocess.run(
                f'netstat -an | findstr ":{CONFIG["SERVER_PORT"]}" | findstr "LISTENING"',
                shell=True,
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False

def open_browsers():
    """Open all 3 browsers"""
    try:
        # Open localhost
        os.startfile(CONFIG['LOCALHOST_URL'])
        time.sleep(0.5)
        
        # Open local file
        os.startfile(CONFIG['LOCAL_FILE_URL'])
        time.sleep(0.5)
        
        # Open GitHub Pages
        os.startfile(CONFIG['GITHUB_PAGES_URL'])
        
        return True
    except Exception as e:
        print(f"Error opening browsers: {e}")
        return False

# ═════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════

def main():
    """Main autostart function"""
    
    # Check if server is already running
    if check_server_running():
        print("Server already running, just opening browsers...")
        open_browsers()
        return
    
    # Start server
    print("Starting server...")
    if not start_server():
        print("Failed to start server!")
        return
    
    # Wait for server to initialize
    print(f"Waiting {CONFIG['BROWSER_DELAY']} seconds for server to start...")
    time.sleep(CONFIG['BROWSER_DELAY'])
    
    # Verify server is running
    max_attempts = 5
    for i in range(max_attempts):
        if check_server_running():
            print("Server is online!")
            break
        print(f"Waiting for server... attempt {i+1}/{max_attempts}")
        time.sleep(2)
    else:
        print("Warning: Server may not have started correctly")
    
    # Open browsers
    print("Opening 3 browsers...")
    open_browsers()
    
    print("Autostart complete! All 3 pages opened.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
