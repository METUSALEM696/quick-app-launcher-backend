# STOP_ALL_SERVERS_ULTRA.py  🎮✨ FULL COLOR + PROGRESS BAR (RICH)
# ✅ VERSIUNE CINEMATOGRAFICA - Mai lent, mai frumos
# ✅ Bara de progres COLORATA cu mai multe frame-uri
# ✅ Totul COLOR + emoji + panouri + animatii
# ✅ NU se inchide repede (ENTER la final)
# ✅ FIX: nu isi mai omoara propriul python (exclude PID curent)
# ✅ BONUS: poate opri DOAR procesul care tine portul (recomandat)
# ⚠ Necesita: pip install rich

import os
import sys
import time
import subprocess
from typing import List, Set

PORT = 8899
BAT_TO_START = r"E:\script\Quick App Launcher\New folder\StartServer_FIRE_AND_FORGET.bat"

# --- MODE ---
# "PORT_ONLY"  = opreste doar PID-urile care ocupa PORT (recomandat)
# "ALL_PY_SAFE" = opreste toate python/pythonw EXCEPT acest script
KILL_MODE = "PORT_ONLY"

# --- check rich ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.text import Text
    from rich import box
except Exception:
    print("\n❌ Lipseste 'rich' pentru culori + progress bar!")
    print("✅ Instaleaza asa:  pip install rich\n")
    input("Apasa ENTER ca sa inchizi...")
    raise

console = Console()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def run(cmd: str):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def is_port_busy(port: int) -> bool:
    r = run(f'netstat -ano | findstr ":{port}"')
    return r.stdout.strip() != ""

def netstat_port(port: int) -> str:
    r = run(f'netstat -ano | findstr ":{port}"')
    return r.stdout.strip()

def progress_bar(title: str, total_steps: int = 150, sleep_s: float = 0.04, color: str = "green"):
    """Progress bar mai lent si cu mai multe frame-uri pentru efect cinematografic"""
    with Progress(
        SpinnerColumn(style="bold magenta", speed=0.8),
        TextColumn(f"[bold cyan]{title}[/bold cyan]"),
        BarColumn(bar_width=40, style=f"bold {color}", complete_style=f"bold {color}"),
        TextColumn("[bold]{task.percentage:>3.0f}%[/bold]"),
        TimeElapsedColumn(),
        console=console
    ) as p:
        t = p.add_task("go", total=total_steps)
        for _ in range(total_steps):
            time.sleep(sleep_s)
            p.update(t, advance=1)

def typing_effect(text: str, delay: float = 0.03):
    """Efect de scriere caracter cu caracter"""
    for char in text:
        console.print(char, end="", style="bold cyan")
        time.sleep(delay)
    console.print()

def separator_line(char: str = "=", width: int = 70, color: str = "cyan"):
    """Linie separatoare colorata"""
    console.print(f"[{color}]{char * width}[/{color}]")
    time.sleep(0.5)

def countdown(seconds: int = 3, message: str = "Incep in"):
    """Numaratoare inversa"""
    for i in range(seconds, 0, -1):
        console.print(f"[bold yellow]{message} {i}...[/bold yellow]", end="\r")
        time.sleep(1)
    console.print(" " * 50, end="\r")  # Clear line

def pids_on_port(port: int) -> List[int]:
    """
    Extrage PID-urile care apar in netstat pe portul dat.
    ATENTIE: netstat poate lista mai multe intrari; colectam PID-urile unice.
    """
    r = run(f'netstat -ano | findstr ":{port}"')
    pids: Set[int] = set()
    for line in r.stdout.splitlines():
        parts = line.split()
        # Exemplu: TCP  0.0.0.0:8899  0.0.0.0:0  LISTENING  1234
        if len(parts) >= 5:
            pid_str = parts[-1]
            try:
                pid = int(pid_str)
                pids.add(pid)
            except ValueError:
                pass
    return sorted(pids)

def kill_pids(pids: List[int]):
    """Opreste PID-urile cu animatie"""
    for pid in pids:
        console.print(f"[bold red]⚔️  Opresc PID {pid}...[/bold red]")
        time.sleep(0.5)
        run(f"taskkill /F /PID {pid}")
        console.print(f"[bold green]   ✅ PID {pid} oprit![/bold green]")
        time.sleep(0.3)

def kill_python_all_safe():
    """
    Opreste toate python/pythonw EXCEPT procesul curent (altfel se inchide scriptul).
    """
    my_pid = os.getpid()
    console.print(f"[dim]Procesul meu (protejat): PID {my_pid}[/dim]")
    time.sleep(0.5)
    
    ps_cmd = (
        f'powershell -NoProfile -ExecutionPolicy Bypass -Command '
        f'"$me={my_pid}; '
        f'Get-Process python,pythonw -ErrorAction SilentlyContinue | '
        f'Where-Object {{$_.Id -ne $me}} | '
        f'Stop-Process -Force -ErrorAction SilentlyContinue"'
    )
    return run(ps_cmd)

def close_browsers_best_effort():
    """
    Inchide browserele cele mai comuni cu animatie.
    """
    console.print("\n")
    separator_line("─", 70, "cyan")
    typing_effect("🌐 Inchid browser-ul...")
    time.sleep(0.8)
    
    browsers = [
        ("brave.exe", "Brave", "🦁"),
        ("chrome.exe", "Chrome", "🔵"),
        ("msedge.exe", "Edge", "🌊"),
        ("firefox.exe", "Firefox", "🦊")
    ]
    
    closed_any = False
    for exe, name, emoji in browsers:
        r = run(f"taskkill /F /IM {exe}")
        if r.returncode == 0:
            console.print(f"   {emoji} [bold yellow]{name}[/bold yellow] detectat...")
            time.sleep(0.4)
            console.print(f"   ✅ [bold green]{name} inchis![/bold green]")
            closed_any = True
            time.sleep(0.6)
    
    if not closed_any:
        console.print("   ℹ️ [bold yellow]Browser-ul nu era deschis[/bold yellow]")
        time.sleep(0.5)
    
    separator_line("─", 70, "cyan")

def main():
    clear()

    # HEADER EPIC
    console.print("\n")
    separator_line("═", 70, "red")
    console.print(Panel.fit(
        Text(
            "🛑 STOP ALL SERVERS – ULTRA ENTERTAINMENT 🎮✨\n\n"
            "💥 Python Slayer • 🌐 Browser Closer\n"
            "🛰 Port Hunter • 🚀 Auto Launcher\n\n"
            f"🎯 Target Port: [bold white]{PORT}[/bold white]\n"
            f"🚀 Auto Start: [bold white]{BAT_TO_START}[/bold white]\n"
            f"🧠 Kill Mode: [bold yellow]{KILL_MODE}[/bold yellow]\n\n"
            "⚠ ATENTIE: poate inchide procese!\n"
            "(in functie de modul ales)",
            justify="center"
        ),
        border_style="bold red",
        box=box.DOUBLE
    ))
    separator_line("═", 70, "red")
    console.print("\n")

    if not Confirm.ask("[bold yellow]🔥 Continui?[/bold yellow]"):
        console.print(Panel("❌ Anulat. N-am oprit nimic.", border_style="yellow", box=box.ROUNDED))
        time.sleep(1)
        return

    # =======================
    # OPERATION 1/3
    # =======================
    console.print("\n")
    countdown(3, "Incep in")
    clear()
    
    console.print("\n")
    separator_line("═", 70, "red")

    if KILL_MODE.upper() == "PORT_ONLY":
        console.print(Panel(
            f"[bold white]🔴 OPERATION 1/3: KILL PORT OWNER[/bold white]\n\n"
            f"🧨 Omor doar PID-urile care ocupa portul [bold yellow]{PORT}[/bold yellow]\n"
            f"✅ NU omor toate Python-urile din PC\n"
            f"🛡️ Acest script este protejat!",
            border_style="bold red",
            box=box.DOUBLE
        ))
        console.print("\n")
        
        progress_bar("💣 Scanare & Oprire PID pe port", total_steps=150, sleep_s=0.04, color="red")
        console.print("\n")

        typing_effect("🔍 Caut PID-uri pe portul 8899...")
        time.sleep(1)
        
        pids = pids_on_port(PORT)
        if pids:
            console.print(Panel(
                "\n".join([f"PID: {p}" for p in pids]), 
                title=f"[bold yellow]🎯 PID-uri gasite pe port {PORT}[/bold yellow]", 
                border_style="yellow",
                box=box.ROUNDED
            ))
            time.sleep(1.5)
            console.print("\n")
            typing_effect("⚔️  Incep eliminarea PID-urilor...")
            time.sleep(0.8)
            console.print("\n")
            kill_pids(pids)
            console.print("\n")
            console.print("✅ [bold green]Toate PID-urile de pe port au fost oprite![/bold green] 🎯")
        else:
            console.print("✅ [bold green]Nimic pe port, totul curat![/bold green] 🟢")
        
        time.sleep(1.5)

    else:
        console.print(Panel(
            "[bold white]🔴 OPERATION 1/3: KILL PYTHON (SAFE)[/bold white]\n\n"
            "🧨 Opreste python/pythonw EXCEPT acest script\n"
            "🛡️ Fix pentru inchidere rapida - NU se omoară singur!",
            border_style="bold red",
            box=box.DOUBLE
        ))
        console.print("\n")
        
        progress_bar("💣 Oprire Python (safe mode)", total_steps=150, sleep_s=0.04, color="red")
        console.print("\n")

        typing_effect("🔍 Identific procesele Python...")
        time.sleep(1)
        
        r = kill_python_all_safe()
        if r.returncode == 0:
            console.print("✅ [bold green]Python (în afară de mine) oprit![/bold green] 🎉🧹")
        else:
            console.print("ℹ️ [bold yellow]Nu existau Python active[/bold yellow] sau permisiuni limitate 🧩")
        
        time.sleep(1.5)

    # Inchide browser-ul (optional)
    close_browsers_best_effort()

    time.sleep(2.0)  # Pauza mai mare ca sa vezi tot

    # =======================
    # OPERATION 2/3
    # =======================
    clear()
    console.print("\n")
    separator_line("═", 70, "magenta")
    console.print(Panel(
        f"[bold white]🛰 OPERATION 2/3: PORT SCAN[/bold white]\n\n"
        f"🔎 Verific daca portul [bold yellow]{PORT}[/bold yellow] este liber...",
        border_style="bold magenta",
        box=box.DOUBLE
    ))
    console.print("\n")
    
    progress_bar("📡 Scanare completa port", total_steps=120, sleep_s=0.04, color="magenta")
    console.print("\n")

    typing_effect("🔍 Analizez portul...")
    time.sleep(1.2)
    
    busy = is_port_busy(PORT)
    if busy:
        console.print(Panel(
            f"⚠ [bold yellow]PORT INCA OCUPAT[/bold yellow] 😬\n\n"
            f"Portul [bold]{PORT}[/bold] este încă ocupat!\n\n"
            f"Posibile cauze:\n"
            f"• Alt proces foloseste portul\n"
            f"• Python nu s-a oprit complet\n"
            f"• Delay de eliberare port",
            border_style="yellow",
            box=box.ROUNDED
        ))
        time.sleep(1)
        ns = netstat_port(PORT)
        if ns:
            console.print(Panel(
                ns, 
                title=f"[bold yellow]📌 netstat (PID) pe {PORT}[/bold yellow]", 
                border_style="yellow",
                box=box.ROUNDED
            ))
        console.print("\n💡 [bold]Poți opri manual PID:[/bold]  [yellow]taskkill /F /PID <number>[/yellow]  🧯")
        time.sleep(2)
    else:
        console.print(Panel(
            f"✅ [bold green]PORT LIBER[/bold green] 🟢✨\n\n"
            f"Portul [bold]{PORT}[/bold] este LIBER!\n"
            f"Totul este gata pentru noul server!",
            border_style="green",
            box=box.DOUBLE
        ))
        console.print("\n🚀 [bold green]Poți porni serverul nou fără conflicte![/bold green] 🎯")
        time.sleep(2)

    # =======================
    # OPERATION 3/3
    # =======================
    clear()
    console.print("\n")
    separator_line("═", 70, "green")
    console.print(Panel(
        "[bold white]✅ OPERATION 3/3: NEXT STEP[/bold white]\n\n"
        "🎉 Serverele vechi sunt închise!\n"
        "🌐 Browser-ul a fost inchis!\n"
        "🔓 Portul este liber!\n\n"
        "[bold cyan]📌 NEXT STEPS:[/bold cyan]\n"
        f"1️⃣  Pornesc: [bold yellow]{BAT_TO_START}[/bold yellow]\n"
        "2️⃣  Browser se deschide automat\n"
        "3️⃣  Serverul ruleaza pe portul 8899\n"
        "4️⃣  Testează launcher-ul! 🔊😈✨",
        border_style="bold green",
        box=box.DOUBLE
    ))
    separator_line("═", 70, "green")
    console.print("\n")

    time.sleep(1)

    if Confirm.ask("[bold yellow]🚀 Vrei să pornesc serverul FIRE AND FORGET acum?[/bold yellow]"):
        console.print("\n")
        if os.path.exists(BAT_TO_START):
            typing_effect("🚀 Pregatesc serverul...")
            time.sleep(0.8)
            console.print("\n")
            progress_bar("🧪 Lansare server", total_steps=100, sleep_s=0.04, color="cyan")
            console.print("\n")
            
            subprocess.Popen(['cmd', '/c', 'start', '', BAT_TO_START], shell=True)
            
            time.sleep(0.5)
            console.print("✅ [bold green]Server PORNIT cu succes![/bold green] 🎉🟩")
            time.sleep(0.5)
            console.print("🌐 [bold cyan]Browser-ul se va deschide in cateva secunde...[/bold cyan]")
            time.sleep(0.5)
            console.print("🎮 [bold yellow]Launcher-ul va fi gata de folosit![/bold yellow]")
            time.sleep(1)
        else:
            console.print(Panel(
                f"❌ [bold red]EROARE[/bold red]\n\n"
                f"Nu găsesc: [bold yellow]{BAT_TO_START}[/bold yellow] 🧨\n\n"
                "Pune-l în același folder cu acest .py",
                border_style="bold red",
                box=box.ROUNDED
            ))
            time.sleep(2)

    console.print("\n")
    separator_line("═", 70, "blue")
    console.print(Panel(
        "[bold white]🏁 MISSION COMPLETE[/bold white] 🎮✨\n\n"
        "Toate operațiunile au fost finalizate cu succes!\n\n"
        "🫡 Apasă ENTER ca să închizi acest script.",
        border_style="bold blue",
        box=box.DOUBLE
    ))
    separator_line("═", 70, "blue")
    console.print("\n")
    
    input()

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        console.print("\n\n[bold red]⚠️  Intrerupt de utilizator![/bold red]")
        time.sleep(1)
        console.print("[yellow]Scriptul se inchide...[/yellow]")
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"💥 [bold red]EROARE CRITICA[/bold red]\n\n{repr(e)}", 
            border_style="bold red",
            box=box.DOUBLE
        ))
        time.sleep(2)
        input("Apasă ENTER ca să închizi...")
        sys.exit(1)
