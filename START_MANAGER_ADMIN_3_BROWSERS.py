#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   🔥 FIRE AND FORGET - ULTRA MEGA FANCY EDITION 🔥                   ║
║                                                                       ║
║   Task Scheduler Manager with ALL the BELLS & WHISTLES!             ║
║   - Gradient Colors 🌈                                               ║
║   - Animated Logo ✨                                                 ║
║   - Sound Effects 🔊                                                 ║
║   - Real-time Monitoring 📊                                          ║
║   - Interactive Dashboard 🎮                                         ║
║   - Typing Effects ⌨️                                                ║
║   - System Stats 💻                                                  ║
║   - Auto Refresh 🔄                                                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import subprocess
import ctypes
import random
import threading
from pathlib import Path
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════
# AUTO-INSTALL DEPENDENCIES
# ═════════════════════════════════════════════════════════════════════

REQUIRED_PACKAGES = {
    'colorama': 'colorama',
    'rich': 'rich',
    'psutil': 'psutil',
}

def install_package(package_name, import_name):
    """Install a package if not available"""
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name, "--break-system-packages"],
                capture_output=True,
                check=True
            )
            print(f"✅ {package_name} installed!")
            return True
        except:
            print(f"⚠️  {package_name} installation failed, continuing without it...")
            return False

# Install required packages
for pkg, imp in REQUIRED_PACKAGES.items():
    install_package(pkg, imp)

# ═════════════════════════════════════════════════════════════════════
# IMPORTS
# ═════════════════════════════════════════════════════════════════════

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except:
    HAS_COLORAMA = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
    from rich.tree import Tree
    HAS_RICH = True
    console = Console()
except:
    HAS_RICH = False

try:
    import psutil
    HAS_PSUTIL = True
except:
    HAS_PSUTIL = False

# ═════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════

_SCRIPT_DIR = Path(__file__).resolve().parent
_FINAL_HTML = _SCRIPT_DIR / "Launcher_FINAL_WITH_SOUND.html"
if Path(sys.executable).name.lower() == "python.exe":
    _PROGRAM_EXE = str(Path(sys.executable).with_name("pythonw.exe"))
    if not Path(_PROGRAM_EXE).is_file():
        _PROGRAM_EXE = sys.executable
else:
    _PROGRAM_EXE = sys.executable

CONFIG = {
    'TASK_NAME': 'FIRE_AND_FORGET_AUTOSTART',
    'TASK_DESCRIPTION': '🔥 Fire and Forget Launcher - Server HTTP cu 3 browsers automat',
    'PROGRAM_EXE': _PROGRAM_EXE,
    'PROGRAM_ARGS': str(_SCRIPT_DIR / 'autostart_with_browsers.py'),
    'WORKING_DIR': str(_SCRIPT_DIR),
    'ENABLE_LOGON_TRIGGER': True,
    'ENABLE_BOOT_TRIGGER': True,
    'ENABLE_DAILY_TRIGGER': False,
    'DAILY_TIME': '09:00',
    'DELAY_SECONDS': 15,
    'RUN_LEVEL': 'LeastPrivilege',
    'PRIORITY': 4,
    'SERVER_PORT': 8899,
    'LOCALHOST_URL': 'http://localhost:8899/',
    'LOCAL_FILE_URL': _FINAL_HTML.as_uri(),
    'GITHUB_PAGES_URL': 'https://metusalem696.github.io/quick-app-launcher/',
    'GITHUB_URL': _FINAL_HTML.as_uri(),
    'ENABLE_SOUND': True,
    'ENABLE_ANIMATIONS': True,
    'THEME': 'cyan',  # cyan, green, magenta, yellow, red
}

# ═════════════════════════════════════════════════════════════════════
# GRADIENT & ANIMATION FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

GRADIENTS = {
    'fire': ['red', 'yellow', 'orange'],
    'ocean': ['blue', 'cyan', 'white'],
    'forest': ['green', 'yellow', 'white'],
    'sunset': ['red', 'magenta', 'yellow'],
    'purple': ['magenta', 'blue', 'cyan'],
}

def beep(frequency=1000, duration=100):
    """Play a beep sound (Windows only)"""
    if CONFIG['ENABLE_SOUND'] and os.name == 'nt':
        try:
            import winsound
            winsound.Beep(frequency, duration)
        except:
            pass

def typing_effect(text, delay=0.03, color='cyan'):
    """Print text with typing effect"""
    if not CONFIG['ENABLE_ANIMATIONS'] or not HAS_RICH:
        print(text)
        return
    
    for char in text:
        console.print(char, end='', style=color)
        time.sleep(delay)
    print()

def rainbow_text(text):
    """Create rainbow colored text"""
    if not HAS_RICH:
        return text
    
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    result = Text()
    for i, char in enumerate(text):
        result.append(char, style=colors[i % len(colors)])
    return result

def create_sparkle():
    """Create sparkle effect"""
    sparkles = ['✨', '⭐', '🌟', '💫', '🌠', '✨']
    return random.choice(sparkles)

def animated_banner():
    """Show animated banner with single-line title centered"""
    if not HAS_RICH:
        print("FIRE AND FORGET - ULTRA MEGA FANCY EDITION")
        return
    
    banner_frames = [
        # Frame 1 - Fire Theme (RED + YELLOW)
        {
            'title': [
                ('🔥 ', 'bold red'),
                ('F I R E ', 'bold red'),
                ('• ', 'bold yellow'),
                ('A N D ', 'bold red'),
                ('• ', 'bold yellow'),
                ('F O R G E T ', 'bold yellow'),
                (' 🔥', 'bold red'),
            ],
            'subtitle_color': 'bold red',
            'separator_color': 'red',
        },
        # Frame 2 - Electric Theme (YELLOW + CYAN)
        {
            'title': [
                ('⚡ ', 'bold yellow'),
                ('F I R E ', 'bold yellow'),
                ('• ', 'bold cyan'),
                ('A N D ', 'bold yellow'),
                ('• ', 'bold cyan'),
                ('F O R G E T ', 'bold cyan'),
                (' ⚡', 'bold yellow'),
            ],
            'subtitle_color': 'bold yellow',
            'separator_color': 'yellow',
        },
        # Frame 3 - Matrix Theme (CYAN + GREEN)
        {
            'title': [
                ('✨ ', 'bold cyan'),
                ('F I R E ', 'bold cyan'),
                ('• ', 'bold green'),
                ('A N D ', 'bold cyan'),
                ('• ', 'bold green'),
                ('F O R G E T ', 'bold green'),
                (' ✨', 'bold cyan'),
            ],
            'subtitle_color': 'bold cyan',
            'separator_color': 'cyan',
        },
        # Frame 4 - Vibrant Theme (GREEN + MAGENTA)
        {
            'title': [
                ('💎 ', 'bold green'),
                ('F I R E ', 'bold green'),
                ('• ', 'bold magenta'),
                ('A N D ', 'bold green'),
                ('• ', 'bold magenta'),
                ('F O R G E T ', 'bold magenta'),
                (' 💎', 'bold green'),
            ],
            'subtitle_color': 'bold magenta',
            'separator_color': 'magenta',
        },
    ]
    
    # Animate banner frames
    for i, frame in enumerate(banner_frames):
        console.clear()
        
        # Create centered title on single line
        title = Text()
        for text, style in frame['title']:
            title.append(text, style=style)
        
        # Top separator
        console.print()
        console.print()
        console.print(Align.center(Text("═" * 80, style=frame['separator_color'])))
        console.print()
        
        # Main title - CENTERED on one line
        console.print(Align.center(title))
        
        console.print()
        console.print(Align.center(Text("═" * 80, style=frame['separator_color'])))
        console.print()
        
        # Subtitle centered
        subtitle = Text()
        subtitle.append("✨ ", style="bold yellow")
        subtitle.append("ULTRA MEGA FANCY EDITION", style=frame['subtitle_color'])
        subtitle.append(" ✨", style="bold yellow")
        console.print(Align.center(subtitle))
        
        console.print(Align.center(Text("Task Scheduler Manager v3.0", style="dim white")))
        console.print()
        console.print(Align.center(Text("─" * 60, style=frame['separator_color'])))
        
        # Beep for each frame
        beep(800 + (i * 100), 80)
        time.sleep(0.35)

def loading_animation(message="Loading", duration=2):
    """Fancy loading animation"""
    if not HAS_RICH:
        print(f"{message}...")
        time.sleep(duration)
        return
    
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(message, total=100)
        
        for i in range(100):
            time.sleep(duration / 100)
            progress.update(task, advance=1)
        
        beep(1200, 50)

def success_animation(message):
    """Animated success message"""
    if not HAS_RICH:
        print(f"✅ {message}")
        return
    
    # Create celebratory panel
    success_text = Text()
    success_text.append("🎉 ", style="bold yellow")
    success_text.append(message, style="bold green")
    success_text.append(" 🎉", style="bold yellow")
    
    panel = Panel(
        Align.center(success_text),
        border_style="green",
        box=box.DOUBLE
    )
    
    console.print(panel)
    beep(1000, 100)
    time.sleep(0.1)
    beep(1200, 100)

# ═════════════════════════════════════════════════════════════════════
# SYSTEM MONITORING
# ═════════════════════════════════════════════════════════════════════

def get_system_stats():
    """Get system statistics"""
    if not HAS_PSUTIL:
        return None
    
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': cpu_percent,
            'memory': memory.percent,
            'disk': disk.percent,
            'memory_used': memory.used / (1024**3),  # GB
            'memory_total': memory.total / (1024**3),  # GB
        }
    except:
        return None

def create_stats_panel():
    """Create a panel with system statistics"""
    if not HAS_RICH:
        return None
    
    stats = get_system_stats()
    if not stats:
        return Panel("System stats unavailable", border_style="dim")
    
    # Create progress bars for resources
    cpu_bar = "█" * int(stats['cpu'] / 5) + "░" * (20 - int(stats['cpu'] / 5))
    mem_bar = "█" * int(stats['memory'] / 5) + "░" * (20 - int(stats['memory'] / 5))
    disk_bar = "█" * int(stats['disk'] / 5) + "░" * (20 - int(stats['disk'] / 5))
    
    content = f"""[cyan]💻 SYSTEM RESOURCES[/cyan]

[yellow]CPU:[/yellow]  [{cpu_bar}] {stats['cpu']:.1f}%
[yellow]RAM:[/yellow]  [{mem_bar}] {stats['memory']:.1f}% ({stats['memory_used']:.1f}/{stats['memory_total']:.1f} GB)
[yellow]DISK:[/yellow] [{disk_bar}] {stats['disk']:.1f}%

[green]⏰ {datetime.now().strftime('%H:%M:%S')}[/green]
"""
    
    return Panel(content, border_style="cyan", box=box.ROUNDED)

# ═════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS (from previous version)
# ═════════════════════════════════════════════════════════════════════

def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    """Request administrator privileges and restart"""
    try:
        if os.name == 'nt':
            # Get the python executable path
            python_exe = sys.executable
            script_path = os.path.abspath(__file__)
            
            # Use runas to restart with admin
            import win32api
            import win32con
            import win32process
            
            try:
                win32api.ShellExecute(
                    0,
                    "runas",
                    python_exe,
                    f'"{script_path}"',
                    os.path.dirname(script_path),
                    win32con.SW_SHOWNORMAL
                )
            except:
                # Fallback to PowerShell
                subprocess.run([
                    'powershell', '-Command',
                    f'Start-Process "{python_exe}" -ArgumentList \\"{script_path}\\" -Verb RunAs'
                ])
            
            sys.exit(0)
    except Exception as e:
        print(f"Failed to request admin: {e}")
        return False

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(cmd, capture=True):
    """Run a command and return result"""
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    else:
        return subprocess.run(cmd, shell=True).returncode

def check_server_running():
    """Check if server is listening on port"""
    code, stdout, _ = run_command(f'netstat -an | findstr ":{CONFIG["SERVER_PORT"]}" | findstr "LISTENING"')
    return code == 0

def check_pythonw_running():
    """Check if pythonw.exe is running"""
    code, stdout, _ = run_command('tasklist | findstr "pythonw.exe"')
    return code == 0

def check_task_exists():
    """Check if scheduled task exists"""
    code, _, _ = run_command(f'schtasks /Query /TN "{CONFIG["TASK_NAME"]}"')
    return code == 0

# ═════════════════════════════════════════════════════════════════════
# FANCY UI FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def print_fancy_header():
    """Print ultra fancy header"""
    clear_screen()
    
    if CONFIG['ENABLE_ANIMATIONS']:
        animated_banner()
    else:
        if HAS_RICH:
            console.print(Panel(
                rainbow_text("🔥 FIRE AND FORGET - ULTRA EDITION 🔥"),
                border_style="bold cyan",
                box=box.DOUBLE
            ))

def create_menu_table():
    """Create fancy interactive menu"""
    if not HAS_RICH:
        return None
    
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.HEAVY,
        border_style="cyan",
        title="[bold yellow]⚡ MAIN CONTROL PANEL ⚡[/bold yellow]",
        title_style="bold yellow"
    )
    
    table.add_column("Key", style="bold cyan", width=6, justify="center")
    table.add_column("Action", style="bold green", width=30)
    table.add_column("Icon", style="yellow", width=6, justify="center")
    table.add_column("Description", style="white", width=35)
    
    menu_items = [
        ("1", "CREATE/UPDATE TASK", "🔨", "Setup autostart configuration"),
        ("2", "START SERVER", "▶️", "Launch server immediately"),
        ("3", "STOP SERVER", "⏹️", "Terminate all server processes"),
        ("4", "RESTART SERVER", "🔄", "Full server restart cycle"),
        ("5", "CHECK STATUS", "📊", "Live system monitoring"),
        ("6", "DELETE TASK", "🗑️", "Remove scheduled task"),
        ("7", "TASK SCHEDULER", "📅", "Open Windows Task Scheduler"),
        ("8", "TEST CONNECTION", "🌐", "Test HTTP endpoints"),
        ("9", "SETTINGS", "⚙️", "Configure preferences"),
        ("0", "EXIT", "🚪", "Close manager gracefully"),
    ]
    
    for key, action, icon, desc in menu_items:
        table.add_row(f"[{key}]", action, icon, desc)
    
    return table

def print_status_dashboard():
    """Print live status dashboard"""
    if not HAS_RICH:
        print("\n=== STATUS DASHBOARD ===")
        print(f"Task Exists: {check_task_exists()}")
        print(f"Server Running: {check_server_running()}")
        print(f"Process Active: {check_pythonw_running()}")
        return
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    # Header
    layout["header"].update(Panel(
        Align.center(Text("📊 LIVE STATUS DASHBOARD 📊", style="bold cyan")),
        border_style="cyan"
    ))
    
    # Status table
    status_table = Table(box=box.ROUNDED, border_style="green")
    status_table.add_column("Component", style="cyan")
    status_table.add_column("Status", style="green")
    status_table.add_column("Details", style="yellow")
    
    task_status = "✅ ACTIVE" if check_task_exists() else "❌ NOT FOUND"
    server_status = "✅ ONLINE" if check_server_running() else "❌ OFFLINE"
    process_status = "✅ RUNNING" if check_pythonw_running() else "❌ STOPPED"
    
    status_table.add_row("Scheduled Task", task_status, CONFIG['TASK_NAME'])
    status_table.add_row("HTTP Server", server_status, f"Port {CONFIG['SERVER_PORT']}")
    status_table.add_row("pythonw.exe", process_status, "Background process")
    
    layout["left"].update(Panel(status_table, title="[bold]Service Status[/bold]", border_style="green"))
    
    # System stats
    stats_panel = create_stats_panel()
    if stats_panel:
        layout["right"].update(stats_panel)
    
    # Footer
    layout["footer"].update(Panel(
        Align.center(f"[yellow]Press any key to return to menu...[/yellow]"),
        border_style="yellow"
    ))
    
    console.print(layout)

# ═════════════════════════════════════════════════════════════════════
# TASK OPERATIONS
# ═════════════════════════════════════════════════════════════════════

def create_task():
    """Create Windows scheduled task with fancy UI"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold yellow]🔨 TASK CREATION WIZARD 🔨[/bold yellow]",
            border_style="yellow",
            box=box.DOUBLE
        ))
    
    typing_effect("\n🔍 Running system checks...", delay=0.02, color="cyan")
    time.sleep(0.5)
    
    # Check admin
    if not is_admin():
        if HAS_RICH:
            console.print(Panel(
                "[bold red]❌ ADMINISTRATOR PRIVILEGES REQUIRED[/bold red]\n\n"
                "Please restart with administrator rights:\n"
                "• Right-click the script\n"
                "• Select 'Run as administrator'",
                border_style="red",
                box=box.HEAVY
            ))
        else:
            print("❌ Administrator rights required!")
        
        beep(400, 500)
        input("\nPress ENTER to continue...")
        return
    
    typing_effect("✅ Administrator privileges confirmed", delay=0.02, color="green")
    beep(800, 50)
    
    # Check Python
    if not Path(CONFIG['PROGRAM_EXE']).exists():
        console.print("[bold red]❌ Python executable not found![/bold red]")
        input("\nPress ENTER to continue...")
        return
    
    typing_effect("✅ Python installation verified", delay=0.02, color="green")
    beep(900, 50)
    
    # Check script
    if not Path(CONFIG['PROGRAM_ARGS']).exists():
        console.print(f"[bold red]❌ Script not found: {CONFIG['PROGRAM_ARGS']}[/bold red]")
        input("\nPress ENTER to continue...")
        return
    
    typing_effect("✅ Server script located", delay=0.02, color="green")
    beep(1000, 50)
    
    # Generate XML
    typing_effect("\n🔧 Generating task configuration...", delay=0.02, color="cyan")
    loading_animation("Building XML structure", 1)
    
    xml_content = generate_task_xml()
    xml_path = os.path.join(os.environ['TEMP'], f"{CONFIG['TASK_NAME']}_task.xml")
    
    with open(xml_path, 'w', encoding='utf-16') as f:
        f.write(xml_content)
    
    # Create task
    typing_effect("📝 Registering task with Windows...", delay=0.02, color="cyan")
    run_command(f'schtasks /Delete /TN "{CONFIG["TASK_NAME"]}" /F')
    code, _, error = run_command(f'schtasks /Create /TN "{CONFIG["TASK_NAME"]}" /XML "{xml_path}" /F')
    
    if code == 0:
        success_animation("TASK CREATED SUCCESSFULLY!")
        
        if HAS_RICH:
            info_table = Table(box=box.SIMPLE, show_header=False, border_style="green")
            info_table.add_column("Key", style="cyan")
            info_table.add_column("Value", style="yellow")
            info_table.add_row("📝 Task Name", CONFIG['TASK_NAME'])
            info_table.add_row("🐍 Executor", "pythonw.exe (invisible)")
            info_table.add_row("⏱️  Delay", f"{CONFIG['DELAY_SECONDS']} seconds")
            info_table.add_row("🔄 Triggers", "Logon + Boot")
            console.print(Panel(info_table, title="[bold]Configuration Summary[/bold]", border_style="green"))
        
        time.sleep(2)
        typing_effect("\n🚀 Launching server...", delay=0.02, color="yellow")
        start_server()
    else:
        console.print(f"[bold red]❌ Task creation failed: {error}[/bold red]")
        beep(400, 500)
        input("\nPress ENTER to continue...")
    
    try:
        os.remove(xml_path)
    except:
        pass

def generate_task_xml():
    """Generate XML content for scheduled task"""
    triggers = ""
    
    if CONFIG['ENABLE_LOGON_TRIGGER']:
        triggers += f"""
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}</UserId>
      <Delay>PT{CONFIG['DELAY_SECONDS']}S</Delay>
    </LogonTrigger>"""
    
    if CONFIG['ENABLE_BOOT_TRIGGER']:
        triggers += f"""
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT{CONFIG['DELAY_SECONDS']}S</Delay>
    </BootTrigger>"""
    
    xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>{CONFIG['TASK_DESCRIPTION']}</Description>
  </RegistrationInfo>
  <Triggers>{triggers}
  </Triggers>
  <Principals>
    <Principal>
      <UserId>{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>{CONFIG['RUN_LEVEL']}</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>{CONFIG['PRIORITY']}</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>{CONFIG['PROGRAM_EXE']}</Command>
      <Arguments>"{CONFIG['PROGRAM_ARGS']}"</Arguments>
      <WorkingDirectory>{CONFIG['WORKING_DIR']}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    return xml

def start_server():
    """Start server with fancy animations"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold green]▶️  SERVER STARTUP SEQUENCE ▶️[/bold green]",
            border_style="green",
            box=box.DOUBLE
        ))
    
    if not check_task_exists():
        console.print("[bold yellow]⚠️  Task not found! Create it first (option 1)[/bold yellow]")
        input("\nPress ENTER to continue...")
        return
    
    typing_effect("🚀 Initiating server launch...", delay=0.02, color="cyan")
    code = run_command(f'schtasks /Run /TN "{CONFIG["TASK_NAME"]}"', capture=False)
    
    if code == 0:
        typing_effect("✅ Task started successfully", delay=0.02, color="green")
        loading_animation("Server initialization", 8)
        
        if check_server_running():
            success_animation("SERVER IS ONLINE!")
            
            # Open browsers with animation
            typing_effect("\n🌐 Launching web interfaces...", delay=0.02, color="cyan")
            time.sleep(0.5)
            
            os.startfile(CONFIG['LOCALHOST_URL'])
            typing_effect(f"  ✅ Opened: {CONFIG['LOCALHOST_URL']}", delay=0.01, color="green")
            beep(1000, 80)
            time.sleep(0.3)
            
            os.startfile(CONFIG['LOCAL_FILE_URL'])
            typing_effect(f"  ✅ Opened: Local Launcher", delay=0.01, color="green")
            beep(1100, 80)
            time.sleep(0.3)
            
            os.startfile(CONFIG['GITHUB_PAGES_URL'])
            typing_effect(f"  ✅ Opened: GitHub Pages", delay=0.01, color="green")
            beep(1200, 80)
            
            if HAS_RICH:
                console.print(Panel(
                    f"[bold green]🎉 All systems operational! 🎉[/bold green]\n\n"
                    f"[cyan]Local Server:[/cyan] {CONFIG['LOCALHOST_URL']}\n"
                    f"[cyan]Port:[/cyan] {CONFIG['SERVER_PORT']}\n"
                    f"[cyan]Process:[/cyan] pythonw.exe (invisible)",
                    border_style="green",
                    box=box.HEAVY
                ))
        else:
            console.print("[bold yellow]⚠️  Server started but not responding yet[/bold yellow]")
            beep(600, 300)
    else:
        console.print("[bold red]❌ Failed to start server![/bold red]")
        beep(400, 500)
    
    input("\nPress ENTER to continue...")

def stop_server():
    """Stop server with confirmation - improved version"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold red]⏹️  SERVER SHUTDOWN SEQUENCE ⏹️[/bold red]",
            border_style="red",
            box=box.DOUBLE
        ))
    
    # Check admin rights first
    if not is_admin():
        if HAS_RICH:
            console.print(Panel(
                "[bold yellow]⚠️  ADMINISTRATOR PRIVILEGES REQUIRED ⚠️[/bold yellow]\n\n"
                "To stop server processes, you need admin rights.\n\n"
                "Options:\n"
                "1. Restart this script as administrator\n"
                "2. Close manually from Task Manager (Ctrl+Shift+Esc)\n"
                "3. Use: START_FANCY_3_BROWSERS.bat (automatically requests admin)",
                border_style="yellow",
                box=box.HEAVY
            ))
        else:
            print("\n⚠️  Administrator privileges required!")
            print("Please run as administrator or use the BAT launcher.")
        
        choice = input("\nDo you want to restart as administrator? (Y/N): ")
        if choice.upper() == 'Y':
            print("\nRestarting with admin privileges...")
            request_admin()
            return
        else:
            print("\nCancelled. Server not stopped.")
            input("\nPress ENTER to continue...")
            return
    
    confirm = input("\n⚠️  Are you sure you want to stop the server? (Y/N): ")
    
    if confirm.upper() != 'Y':
        return
    
    typing_effect("\n🛑 Terminating server processes...", delay=0.02, color="yellow")
    
    stopped = False
    
    # Try to kill pythonw.exe (invisible processes)
    code1 = run_command('taskkill /F /IM pythonw.exe', capture=False)
    if code1 == 0:
        typing_effect("  ✅ Stopped pythonw.exe processes", delay=0.02, color="green")
        stopped = True
        time.sleep(0.5)
    
    # Try to kill python.exe (visible processes that might be running the server)
    code2, stdout, _ = run_command('tasklist /FI "IMAGENAME eq python.exe"')
    if 'python.exe' in stdout:
        # Try to find and kill only server-related python processes
        code3, ps_output, _ = run_command('netstat -ano | findstr ":%s"' % CONFIG['SERVER_PORT'])
        if ps_output:
            # Extract PID from netstat output
            import re
            pids = set()
            for line in ps_output.split('\n'):
                match = re.search(r'\s+(\d+)$', line.strip())
                if match:
                    pids.add(match.group(1))
            
            for pid in pids:
                code_kill = run_command(f'taskkill /F /PID {pid}', capture=False)
                if code_kill == 0:
                    typing_effect(f"  ✅ Stopped process PID {pid}", delay=0.02, color="green")
                    stopped = True
        else:
            # No specific server process found, but python.exe exists
            # Ask if user wants to kill all python.exe
            kill_all = input("\n  Python processes found. Kill ALL python.exe? (Y/N): ")
            if kill_all.upper() == 'Y':
                code4 = run_command('taskkill /F /IM python.exe', capture=False)
                if code4 == 0:
                    typing_effect("  ✅ Stopped python.exe processes", delay=0.02, color="green")
                    stopped = True
    
    # Final check
    time.sleep(1)
    if check_server_running():
        typing_effect("\n⚠️  Warning: Server may still be running on port %s" % CONFIG['SERVER_PORT'], delay=0.02, color="yellow")
    elif stopped:
        typing_effect("\n✅ Server stopped successfully", delay=0.02, color="green")
        beep(800, 100)
    else:
        typing_effect("\nℹ️  No active server processes found", delay=0.02, color="cyan")
    
    input("\nPress ENTER to continue...")

def restart_server():
    """Restart server with progress tracking - improved version"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold yellow]🔄 SERVER RESTART PROTOCOL 🔄[/bold yellow]",
            border_style="yellow",
            box=box.DOUBLE
        ))
    
    # Phase 1 - Stop server processes
    typing_effect("\n[1/3] Stopping current server instance...", delay=0.02, color="cyan")
    
    # Kill pythonw.exe
    run_command('taskkill /F /IM pythonw.exe')
    
    # Kill python.exe processes on server port
    code, ps_output, _ = run_command('netstat -ano | findstr ":%s"' % CONFIG['SERVER_PORT'])
    if ps_output:
        import re
        pids = set()
        for line in ps_output.split('\n'):
            match = re.search(r'\s+(\d+)$', line.strip())
            if match:
                pids.add(match.group(1))
        for pid in pids:
            run_command(f'taskkill /F /PID {pid}')
    
    typing_effect("      ✅ Stopped", delay=0.02, color="green")
    beep(800, 50)
    
    # Phase 2
    typing_effect("\n[2/3] Cleaning up resources...", delay=0.02, color="cyan")
    time.sleep(2)
    typing_effect("      ✅ Complete", delay=0.02, color="green")
    beep(900, 50)
    
    # Phase 3
    typing_effect("\n[3/3] Restarting server...", delay=0.02, color="cyan")
    code = run_command(f'schtasks /Run /TN "{CONFIG["TASK_NAME"]}"', capture=False)
    
    if code == 0:
        loading_animation("Initializing server", 8)
        
        if check_server_running():
            success_animation("RESTART SUCCESSFUL!")
            
            typing_effect("\n🌐 Opening interfaces...", delay=0.02, color="cyan")
            os.startfile(CONFIG['LOCALHOST_URL'])
            time.sleep(0.5)
            os.startfile(CONFIG['LOCAL_FILE_URL'])
            time.sleep(0.5)
            os.startfile(CONFIG['GITHUB_PAGES_URL'])
            beep(1200, 100)
        else:
            console.print("[bold yellow]⚠️  Server restarted but not responding[/bold yellow]")
    else:
        console.print("[bold red]❌ Restart failed![/bold red]")
        beep(400, 500)
    
    input("\nPress ENTER to continue...")

def check_status_live():
    """Live status monitoring"""
    print_fancy_header()
    print_status_dashboard()
    input()

def delete_task():
    """Delete task with confirmation - improved version"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold red]🗑️  TASK DELETION PROTOCOL 🗑️[/bold red]",
            border_style="red",
            box=box.HEAVY
        ))
    
    confirm = input("\n⚠️  This will permanently remove the autostart task. Continue? (Y/N): ")
    
    if confirm.upper() != 'Y':
        return
    
    typing_effect("\n🛑 Stopping server...", delay=0.02, color="yellow")
    
    # Kill pythonw.exe
    run_command('taskkill /F /IM pythonw.exe')
    
    # Kill python.exe processes on server port
    code, ps_output, _ = run_command('netstat -ano | findstr ":%s"' % CONFIG['SERVER_PORT'])
    if ps_output:
        import re
        pids = set()
        for line in ps_output.split('\n'):
            match = re.search(r'\s+(\d+)$', line.strip())
            if match:
                pids.add(match.group(1))
        for pid in pids:
            run_command(f'taskkill /F /PID {pid}')
    
    typing_effect("🗑️  Deleting task...", delay=0.02, color="yellow")
    code = run_command(f'schtasks /Delete /TN "{CONFIG["TASK_NAME"]}" /F', capture=False)
    
    if code == 0:
        typing_effect("✅ Task deleted successfully", delay=0.02, color="green")
        beep(800, 100)
    else:
        console.print("[bold red]❌ Deletion failed![/bold red]")
        beep(400, 500)
    
    input("\nPress ENTER to continue...")

def open_task_scheduler():
    """Open Windows Task Scheduler"""
    os.system('start taskschd.msc')
    beep(1000, 50)

def test_connection():
    """Test HTTP connection with status"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold cyan]🌐 CONNECTION TEST SUITE 🌐[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        ))
    
    typing_effect("\n🔍 Testing server availability...", delay=0.02, color="cyan")
    time.sleep(1)
    
    if check_server_running():
        typing_effect(f"✅ Port {CONFIG['SERVER_PORT']}: LISTENING", delay=0.02, color="green")
        beep(1000, 100)
    else:
        typing_effect(f"❌ Port {CONFIG['SERVER_PORT']}: CLOSED", delay=0.02, color="red")
        beep(400, 300)
    
    typing_effect("\n🌐 Opening test interfaces...", delay=0.02, color="cyan")
    os.startfile(CONFIG['LOCALHOST_URL'])
    time.sleep(0.5)
    os.startfile(CONFIG['LOCAL_FILE_URL'])
    time.sleep(0.5)
    os.startfile(CONFIG['GITHUB_PAGES_URL'])
    
    typing_effect("✅ Browsers launched (3 tabs)", delay=0.02, color="green")
    beep(1200, 100)
    
    input("\nPress ENTER to continue...")

def settings_menu():
    """Settings configuration"""
    print_fancy_header()
    
    if HAS_RICH:
        console.print(Panel(
            "[bold magenta]⚙️  PREFERENCES & SETTINGS ⚙️[/bold magenta]",
            border_style="magenta",
            box=box.DOUBLE
        ))
        
        table = Table(box=box.ROUNDED)
        table.add_column("Setting", style="cyan")
        table.add_column("Current Value", style="yellow")
        
        table.add_row("🔊 Sound Effects", "✅ Enabled" if CONFIG['ENABLE_SOUND'] else "❌ Disabled")
        table.add_row("✨ Animations", "✅ Enabled" if CONFIG['ENABLE_ANIMATIONS'] else "❌ Disabled")
        table.add_row("🎨 Theme", CONFIG['THEME'])
        table.add_row("⏱️  Startup Delay", f"{CONFIG['DELAY_SECONDS']} seconds")
        table.add_row("🔒 Run Level", CONFIG['RUN_LEVEL'])
        
        console.print(table)
    
    print("\n[1] Toggle Sound Effects")
    print("[2] Toggle Animations")
    print("[0] Back to Main Menu")
    
    choice = input("\nSelect option: ")
    
    if choice == '1':
        CONFIG['ENABLE_SOUND'] = not CONFIG['ENABLE_SOUND']
        console.print(f"[green]Sound effects {'enabled' if CONFIG['ENABLE_SOUND'] else 'disabled'}[/green]")
        time.sleep(1)
    elif choice == '2':
        CONFIG['ENABLE_ANIMATIONS'] = not CONFIG['ENABLE_ANIMATIONS']
        console.print(f"[green]Animations {'enabled' if CONFIG['ENABLE_ANIMATIONS'] else 'disabled'}[/green]")
        time.sleep(1)

# ═════════════════════════════════════════════════════════════════════
# MAIN PROGRAM
# ═════════════════════════════════════════════════════════════════════

def main():
    """Main program loop with ultra fancy UI"""
    
    # Startup animation
    if CONFIG['ENABLE_ANIMATIONS']:
        animated_banner()
        time.sleep(1)
    
    while True:
        print_fancy_header()
        
        # Show system stats at top
        if HAS_RICH and HAS_PSUTIL:
            stats_panel = create_stats_panel()
            if stats_panel:
                console.print(stats_panel)
        
        # Show menu
        menu_table = create_menu_table()
        if menu_table:
            console.print(menu_table)
        else:
            print("\n=== MAIN MENU ===")
            print("[1] CREATE TASK")
            print("[2] START SERVER")
            print("[3] STOP SERVER")
            print("[4] RESTART SERVER")
            print("[5] CHECK STATUS")
            print("[6] DELETE TASK")
            print("[7] TASK SCHEDULER")
            print("[8] TEST CONNECTION")
            print("[9] SETTINGS")
            print("[0] EXIT")
        
        # Get choice
        if HAS_RICH:
            choice = Prompt.ask(
                "\n[bold cyan]⚡ Select option[/bold cyan]",
                choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            )
        else:
            choice = input("\nSelect option: ")
        
        beep(1000, 30)
        
        # Execute choice
        if choice == '1':
            create_task()
        elif choice == '2':
            start_server()
        elif choice == '3':
            stop_server()
        elif choice == '4':
            restart_server()
        elif choice == '5':
            check_status_live()
        elif choice == '6':
            delete_task()
        elif choice == '7':
            open_task_scheduler()
        elif choice == '8':
            test_connection()
        elif choice == '9':
            settings_menu()
        elif choice == '0':
            print_fancy_header()
            
            if HAS_RICH:
                goodbye = Panel(
                    Align.center(
                        "[bold green]🎉 Thank you for using Fire and Forget Manager! 🎉[/bold green]\n\n"
                        "[cyan]Your Quick App Launcher is ready![/cyan]\n\n"
                        f"{create_sparkle()} {create_sparkle()} {create_sparkle()}"
                    ),
                    border_style="green",
                    box=box.DOUBLE
                )
                console.print(goodbye)
            else:
                print("\n✨ Thank you! ✨")
            
            beep(800, 100)
            time.sleep(0.2)
            beep(1000, 100)
            time.sleep(0.2)
            beep(1200, 150)
            time.sleep(1)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress ENTER to exit...")
        sys.exit(1)