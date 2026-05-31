# STOP_ALL_SERVERS_ULTRA.py  🎮✨ CINEMATIC + CONFIRM START + HOLD + CLOSE SERVER WINDOW

import os
import sys
import time
import subprocess
from typing import List, Set

PORT = 8899
BAT_TO_START = r"E:\script\Quick App Launcher\New folder\StartServer_FIRE_AND_FORGET.bat"

# --- MODE ---
KILL_MODE = "PORT_ONLY"

# --- USER ---
CONFIRM_BEFORE_START = True
HOLD_AT_END = True

# --- CLOSE THAT CMD WINDOW (din screenshot) ---
CLOSE_SERVER_CMD_WINDOW = True
SERVER_WINDOW_TITLE = "FÜÇ Fire"   # trebuie sa fie EXACT ca titlul ferestrei BAT

# --- CINEMATIC ---
CINEMATIC = True
PROGRESS_STEPS = 160 if CINEMATIC else 80
PROGRESS_SLEEP = 0.035 if CINEMATIC else 0.015
TYPE_DELAY = 0.025 if CINEMATIC else 0.006
PAUSE_SHORT = 0.55 if CINEMATIC else 0.15

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.text import Text
    from rich import box
except Exception:
    print("\n❌ Lipseste 'rich'!  Instaleaza: pip install rich\n")
    input("ENTER...")
    raise

console = Console()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def run(cmd: str):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def typing_effect(text: str, style: str = "bold cyan", delay: float = None):
    d = TYPE_DELAY if delay is None else delay
    for ch in text:
        console.print(ch, end="", style=style)
        time.sleep(d)
    console.print()

def separator_line(char: str = "=", width: int = 70, color: str = "cyan"):
    console.print(f"[{color}]{char * width}[/{color}]")
    time.sleep(PAUSE_SHORT)

def progress_bar(title: str, color: str = "green"):
    with Progress(
        SpinnerColumn(style="bold magenta", speed=0.85 if CINEMATIC else 1.25),
        TextColumn(f"[bold cyan]{title}[/bold cyan]"),
        BarColumn(bar_width=42 if CINEMATIC else 36, style=f"bold {color}", complete_style=f"bold {color}"),
        TextColumn("[bold]{task.percentage:>3.0f}%[/bold]"),
        TimeElapsedColumn(),
        console=console
    ) as p:
        t = p.add_task("go", total=PROGRESS_STEPS)
        for _ in range(PROGRESS_STEPS):
            time.sleep(PROGRESS_SLEEP)
            p.update(t, advance=1)

def countdown(seconds: int = 3, message: str = "Incep in"):
    for i in range(seconds, 0, -1):
        console.print(f"[bold yellow]{message} {i}...[/bold yellow]", end="\r")
        time.sleep(1 if CINEMATIC else 0.6)
    console.print(" " * 60, end="\r")

def is_port_busy(port: int) -> bool:
    return run(f'netstat -ano | findstr ":{port}"').stdout.strip() != ""

def netstat_port(port: int) -> str:
    return run(f'netstat -ano | findstr ":{port}"').stdout.strip()

def pids_on_port(port: int) -> List[int]:
    r = run(f'netstat -ano | findstr ":{port}"')
    pids: Set[int] = set()
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 5:
            try:
                pids.add(int(parts[-1]))
            except ValueError:
                pass
    return sorted(pids)

def kill_pids(pids: List[int]):
    for pid in pids:
        console.print(f"[bold red]⚔️  Opresc PID {pid}...[/bold red]")
        time.sleep(0.35 if CINEMATIC else 0.10)
        run(f"taskkill /F /PID {pid}")
        console.print(f"[bold green]✅ PID {pid} oprit![/bold green]")
        time.sleep(0.22 if CINEMATIC else 0.06)

def close_browsers_best_effort():
    console.print("\n")
    separator_line("─", 70, "cyan")
    typing_effect("🌐 Inchid browser-ul...", "bold cyan")
    time.sleep(0.6 if CINEMATIC else 0.2)

    for exe, name, emoji in [
        ("brave.exe", "Brave", "🦁"),
        ("chrome.exe", "Chrome", "🔵"),
        ("msedge.exe", "Edge", "🌊"),
        ("firefox.exe", "Firefox", "🦊"),
    ]:
        run(f"taskkill /F /IM {exe}")

    separator_line("─", 70, "cyan")

def close_cmd_window_by_title(title_contains: str):
    # Inchide fereastra CMD dupa titlu (ex: "FÜÇ Fire")
    ps = (
        'powershell -NoProfile -ExecutionPolicy Bypass -Command '
        f'"$t=\\"{title_contains}\\"; '
        'Get-Process cmd -ErrorAction SilentlyContinue | '
        'Where-Object { $_.MainWindowTitle -and $_.MainWindowTitle -like (\'*\' + $t + \'*\') } | '
        'ForEach-Object { try { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue } catch {} }"'
    )
    run(ps)

def start_server_with_confirm():
    console.print(Panel(
        f"🚀 URMEAZA SA PORNESC SERVERUL!\n\n"
        f"⚠️ Va porni BAT si poate deschide browser-ul.\n\n"
        f"📌 BAT:\n{BAT_TO_START}\n",
        border_style="bold yellow",
        box=box.DOUBLE
    ))

    if CONFIRM_BEFORE_START and (not Confirm.ask("[bold yellow]Pornesc serverul acum?[/bold yellow]")):
        console.print(Panel("❌ OK. Nu pornesc serverul.", border_style="yellow", box=box.ROUNDED))
        return

    if not os.path.exists(BAT_TO_START):
        console.print(Panel(
            f"❌ Nu găsesc BAT:\n[bold]{BAT_TO_START}[/bold]",
            border_style="bold red",
            box=box.DOUBLE
        ))
        return

    typing_effect("🧪 Pregatesc lansarea...", "bold cyan")
    progress_bar("🚀 Lansare server", color="cyan")

    batch_dir = os.path.dirname(BAT_TO_START)
    subprocess.Popen([BAT_TO_START], shell=True, cwd=batch_dir)

    console.print("✅ [bold green]Server PORNIT![/bold green] 🎉")

    # ✅ inchide fereastra aia ramasa (daca BAT-ul mai sta deschis)
    if CLOSE_SERVER_CMD_WINDOW and SERVER_WINDOW_TITLE:
        time.sleep(0.8)
        typing_effect(f"🧼 Inchid fereastra: {SERVER_WINDOW_TITLE} ...", "bold cyan")
        close_cmd_window_by_title(SERVER_WINDOW_TITLE)

def main():
    clear()
    console.print("\n")
    separator_line("═", 70, "red")

    console.print(Panel.fit(
        Text(
            "🛑 STOP ALL SERVERS – ULTRA CINEMATIC 🎮✨\n\n"
            f"🎯 Target Port: {PORT}\n"
            f"🚀 BAT: {BAT_TO_START}\n"
            f"🧠 Kill Mode: {KILL_MODE}\n",
            justify="center"
        ),
        border_style="bold red",
        box=box.DOUBLE
    ))

    separator_line("═", 70, "red")
    console.print("\n")

    countdown(3, "Incep in")
    clear()

    # OP 1: kill port owners
    console.print("\n")
    separator_line("═", 70, "red")
    console.print(Panel(
        f"[bold]🔴 OPERATION 1/3: KILL PORT OWNER[/bold]\n\n"
        f"🧨 Omoara doar PID-urile care ocupa portul {PORT}",
        border_style="bold red",
        box=box.DOUBLE
    ))
    console.print("\n")
    progress_bar("💣 Scanare & Oprire PID pe port", color="red")
    console.print("\n")

    typing_effect(f"🔍 Caut PID-uri pe portul {PORT}...")
    time.sleep(1.0 if CINEMATIC else 0.25)

    pids = pids_on_port(PORT)
    if pids:
        console.print(Panel(
            "\n".join([f"PID: {p}" for p in pids]),
            title=f"🎯 PID-uri gasite pe port {PORT}",
            border_style="yellow",
            box=box.ROUNDED
        ))
        time.sleep(1.2 if CINEMATIC else 0.35)
        kill_pids(pids)
        console.print("\n✅ [bold green]PID-urile de pe port au fost oprite![/bold green] 🎯")
    else:
        console.print("✅ [bold green]Nimic pe port, totul curat![/bold green] 🟢")

    time.sleep(1.0 if CINEMATIC else 0.25)

    close_browsers_best_effort()
    time.sleep(1.2 if CINEMATIC else 0.25)

    # OP 2: scan port
    clear()
    console.print("\n")
    separator_line("═", 70, "magenta")
    console.print(Panel(
        f"[bold]🛰 OPERATION 2/3: PORT SCAN[/bold]\n\nVerific portul {PORT}...",
        border_style="bold magenta",
        box=box.DOUBLE
    ))
    console.print("\n")
    progress_bar("📡 Scanare port", color="magenta")
    console.print("\n")

    if is_port_busy(PORT):
        console.print(Panel(
            f"⚠ PORTUL {PORT} INCA OCUPAT!\n\n{netstat_port(PORT)}",
            border_style="yellow",
            box=box.ROUNDED
        ))
        time.sleep(1.6 if CINEMATIC else 0.4)
    else:
        console.print(Panel(
            f"✅ PORTUL {PORT} ESTE LIBER! 🟢✨",
            border_style="green",
            box=box.DOUBLE
        ))
        time.sleep(1.4 if CINEMATIC else 0.35)

    # OP 3: start server (cu confirmare)
    clear()
    console.print("\n")
    separator_line("═", 70, "green")
    console.print(Panel(
        "[bold]✅ OPERATION 3/3: START SERVER[/bold]\n\nPornesc serverul cu confirmare.",
        border_style="bold green",
        box=box.DOUBLE
    ))
    console.print("\n")
    start_server_with_confirm()

    console.print("\n")
    separator_line("═", 70, "blue")
    console.print(Panel(
        "🏁 MISSION COMPLETE 🎮✨\n\nApasă ENTER ca să închizi.",
        border_style="bold blue",
        box=box.DOUBLE
    ))
    separator_line("═", 70, "blue")

    if HOLD_AT_END:
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠ Oprit de utilizator.[/bold yellow]")
        input("ENTER...")
    except Exception as e:
        console.print(Panel(f"💥 EROARE:\n{repr(e)}", border_style="red", box=box.DOUBLE))
        input("ENTER...")
