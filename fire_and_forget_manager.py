#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIRE AND FORGET - TASK SCHEDULER MANAGER
Versiune Python cu CULORI si EFECTE FANCY!
"""

import os
import sys
import time
import subprocess
import ctypes
from pathlib import Path

# ═════════════════════════════════════════════════════════════════════
# IMPORT LIBRARIES FOR FANCY UI
# ═════════════════════════════════════════════════════════════════════

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    print("Installing colorama for colors...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "--break-system-packages"], 
                   capture_output=True)
    try:
        from colorama import init, Fore, Back, Style
        init(autoreset=True)
        HAS_COLORAMA = True
    except:
        HAS_COLORAMA = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt
    from rich.table import Table
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    print("Installing rich for fancy effects...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "--break-system-packages"],
                   capture_output=True)
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
        from rich.prompt import Prompt
        from rich.table import Table
        from rich import box
        HAS_RICH = True
        console = Console()
    except:
        HAS_RICH = False

# ═════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════

_SCRIPT_DIR = Path(__file__).resolve().parent
if Path(sys.executable).name.lower() == "python.exe":
    _PROGRAM_EXE = str(Path(sys.executable).with_name("pythonw.exe"))
    if not Path(_PROGRAM_EXE).is_file():
        _PROGRAM_EXE = sys.executable
else:
    _PROGRAM_EXE = sys.executable

GITHUB_PAGES_URL = "https://METUSALEM969.github.io/quick-app-launcher/"

CONFIG = {
    'TASK_NAME': 'FIRE_AND_FORGET_AUTOSTART',
    'TASK_DESCRIPTION': 'Fire and Forget Launcher - Server HTTP pentru quick app launcher',
    'PROGRAM_EXE': _PROGRAM_EXE,
    'PROGRAM_ARGS': str(_SCRIPT_DIR / 'server_fire_and_forget.py'),
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
    'GITHUB_URL': GITHUB_PAGES_URL
}

# ═════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
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

def print_banner():
    """Print fancy ASCII art banner"""
    if HAS_RICH:
        banner = """
[bold cyan]
   ███████╗██╗██████╗ ███████╗     █████╗ ███╗   ██╗██████╗ 
   ██╔════╝██║██╔══██╗██╔════╝    ██╔══██╗████╗  ██║██╔══██╗
   █████╗  ██║██████╔╝█████╗      ███████║██╔██╗ ██║██║  ██║
   ██╔══╝  ██║██╔══██╗██╔══╝      ██╔══██║██║╚██╗██║██║  ██║
   ██║     ██║██║  ██║███████╗    ██║  ██║██║ ╚████║██████╔╝
   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ 
                                                              
   ███████╗ ██████╗ ██████╗  ██████╗ ███████╗████████╗
   ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝
   █████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ██║   
   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ██║   
   ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ██║   
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
[/bold cyan]
[bold yellow]         🚀 TASK SCHEDULER MANAGER v3.0 - Python Edition 🚀[/bold yellow]
        """
        console.print(Panel(banner, border_style="cyan", box=box.DOUBLE))
    else:
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  FIRE AND FORGET - TASK SCHEDULER MANAGER")
        print(f"{Fore.YELLOW}  Python Edition with COLORS & EFFECTS!")
        print(f"{Fore.CYAN}{'='*70}")

def print_menu():
    """Print fancy main menu"""
    if HAS_RICH:
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Action", style="green", width=35)
        table.add_column("Description", style="yellow")
        
        table.add_row("[1]", "🔨 CREATE/UPDATE TASK", "Setup autostart task")
        table.add_row("[2]", "▶️  START SERVER", "Launch server now")
        table.add_row("[3]", "⏹️  STOP SERVER", "Terminate server")
        table.add_row("[4]", "🔄 RESTART SERVER", "Full restart cycle")
        table.add_row("[5]", "📊 CHECK STATUS", "View server status")
        table.add_row("[6]", "🗑️  DELETE TASK", "Remove from scheduler")
        table.add_row("[7]", "📅 TASK SCHEDULER", "Open Windows scheduler")
        table.add_row("[8]", "🌐 TEST CONNECTION", "Test HTTP endpoint")
        table.add_row("[0]", "🚪 EXIT", "Close manager")
        
        console.print(table)
    else:
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}  MAIN MENU")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.YELLOW}  [1] CREATE/UPDATE TASK     - Setup autostart")
        print(f"{Fore.YELLOW}  [2] START SERVER           - Launch now")
        print(f"{Fore.YELLOW}  [3] STOP SERVER            - Terminate")
        print(f"{Fore.YELLOW}  [4] RESTART SERVER         - Full restart")
        print(f"{Fore.YELLOW}  [5] CHECK STATUS           - View status")
        print(f"{Fore.YELLOW}  [6] DELETE TASK            - Remove task")
        print(f"{Fore.YELLOW}  [7] TASK SCHEDULER         - Open GUI")
        print(f"{Fore.YELLOW}  [8] TEST CONNECTION        - Test HTTP")
        print(f"{Fore.YELLOW}  [0] EXIT                   - Quit")
        print(f"{Fore.CYAN}{'='*70}")

def print_success(message):
    """Print success message with fancy formatting"""
    if HAS_RICH:
        console.print(f"[bold green]✅ {message}[/bold green]")
    else:
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message with fancy formatting"""
    if HAS_RICH:
        console.print(f"[bold red]❌ {message}[/bold red]")
    else:
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message with fancy formatting"""
    if HAS_RICH:
        console.print(f"[bold cyan]ℹ️  {message}[/bold cyan]")
    else:
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message with fancy formatting"""
    if HAS_RICH:
        console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    else:
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def fancy_progress_bar(duration, message="Processing"):
    """Show fancy progress bar"""
    if HAS_RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task(message, total=duration)
            for i in range(duration):
                time.sleep(1)
                progress.update(task, advance=1)
    else:
        for i in range(duration):
            percent = int((i + 1) / duration * 100)
            bar = '█' * (percent // 2) + '░' * (50 - percent // 2)
            print(f"\r{Fore.CYAN}{message}: [{bar}] {percent}%{Style.RESET_ALL}", end='', flush=True)
            time.sleep(1)
        print()

# ═════════════════════════════════════════════════════════════════════
# TASK CREATION
# ═════════════════════════════════════════════════════════════════════

def create_task():
    """Create Windows scheduled task"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold cyan]TASK CREATOR[/bold cyan]", border_style="cyan"))
    else:
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  TASK CREATOR")
        print(f"{Fore.CYAN}{'='*70}\n")
    
    # Check admin
    print_info("Checking administrator privileges...")
    if not is_admin():
        print_error("Administrator rights required!")
        print_warning("Right-click script and select 'Run as administrator'")
        input("\nPress ENTER to continue...")
        return
    print_success("Administrator privileges: OK")
    
    # Check Python
    print_info("Verifying Python installation...")
    if not Path(CONFIG['PROGRAM_EXE']).exists():
        print_error(f"Python not found at: {CONFIG['PROGRAM_EXE']}")
        input("\nPress ENTER to continue...")
        return
    print_success("Python executable: OK")
    
    # Check script
    print_info("Checking Python script...")
    if not Path(CONFIG['PROGRAM_ARGS']).exists():
        print_error(f"Script not found: {CONFIG['PROGRAM_ARGS']}")
        input("\nPress ENTER to continue...")
        return
    print_success("Python script: OK")
    
    # Check working directory
    print_info("Verifying working directory...")
    if not Path(CONFIG['WORKING_DIR']).exists():
        print_error(f"Directory not found: {CONFIG['WORKING_DIR']}")
        input("\nPress ENTER to continue...")
        return
    print_success("Working directory: OK")
    
    # Generate XML
    print_info("Generating XML configuration...")
    xml_content = generate_task_xml()
    xml_path = os.path.join(os.environ['TEMP'], f"{CONFIG['TASK_NAME']}_task.xml")
    
    with open(xml_path, 'w', encoding='utf-16') as f:
        f.write(xml_content)
    
    # Delete old task
    print_info("Removing old task (if exists)...")
    run_command(f'schtasks /Delete /TN "{CONFIG["TASK_NAME"]}" /F')
    
    # Create new task
    print_info("Creating new task...")
    code, _, error = run_command(f'schtasks /Create /TN "{CONFIG["TASK_NAME"]}" /XML "{xml_path}" /F')
    
    if code == 0:
        print_success("TASK CREATED SUCCESSFULLY!")
        print_info(f"Task Name: {CONFIG['TASK_NAME']}")
        print_info(f"Executor: pythonw.exe (invisible)")
        print_info(f"Delay: {CONFIG['DELAY_SECONDS']} seconds")
        
        time.sleep(2)
        print_info("Starting server automatically...")
        start_server()
    else:
        print_error("Failed to create task!")
        print_error(error)
        input("\nPress ENTER to continue...")
    
    # Cleanup
    try:
        os.remove(xml_path)
    except:
        pass

def generate_task_xml():
    """Generate XML content for scheduled task"""
    triggers = ""
    active_count = 0
    
    if CONFIG['ENABLE_LOGON_TRIGGER']:
        active_count += 1
        triggers += f"""
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}</UserId>
      <Delay>PT{CONFIG['DELAY_SECONDS']}S</Delay>
    </LogonTrigger>"""
    
    if CONFIG['ENABLE_BOOT_TRIGGER']:
        active_count += 1
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

# ═════════════════════════════════════════════════════════════════════
# SERVER CONTROL
# ═════════════════════════════════════════════════════════════════════

def start_server():
    """Start the server"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold green]SERVER STARTUP[/bold green]", border_style="green"))
    else:
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}  SERVER STARTUP")
        print(f"{Fore.GREEN}{'='*70}\n")
    
    # Check if task exists
    if not check_task_exists():
        print_warning("Task not found! Please create it first (option 1)")
        input("\nPress ENTER to continue...")
        return
    
    print_info(f"Starting task: {CONFIG['TASK_NAME']}")
    code = run_command(f'schtasks /Run /TN "{CONFIG["TASK_NAME"]}"', capture=False)
    
    if code == 0:
        print_success("Task started!")
        fancy_progress_bar(8, "Waiting for server initialization")
        
        if check_server_running():
            print_success("SERVER IS ONLINE!")
            print_success(f"HTTP Server: LISTENING on port {CONFIG['SERVER_PORT']}")
            print_success("Process: pythonw.exe (invisible)")
            print_info(f"Local URL: {CONFIG['LOCALHOST_URL']}")
            
            print_info("Opening browsers automatically...")
            os.startfile(CONFIG['LOCALHOST_URL'])
            os.startfile(CONFIG['GITHUB_URL'])
            time.sleep(1)
            print_success("Browsers opened!")
        else:
            print_warning("Task started but server not responding")
            print_info("Check: Python modules, syntax, port conflicts")
    else:
        print_error("Failed to start task!")
    
    input("\nPress ENTER to continue...")

def stop_server():
    """Stop the server"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold red]SERVER SHUTDOWN[/bold red]", border_style="red"))
    else:
        print(f"\n{Fore.RED}{'='*70}")
        print(f"{Fore.RED}  SERVER SHUTDOWN")
        print(f"{Fore.RED}{'='*70}\n")
    
    print_info("Terminating pythonw.exe processes...")
    code = run_command('taskkill /F /IM pythonw.exe', capture=False)
    
    if code == 0:
        print_success("Server stopped successfully!")
    else:
        print_warning("No pythonw.exe processes found")
    
    input("\nPress ENTER to continue...")

def restart_server():
    """Restart the server"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold yellow]SERVER RESTART[/bold yellow]", border_style="yellow"))
    else:
        print(f"\n{Fore.YELLOW}{'='*70}")
        print(f"{Fore.YELLOW}  SERVER RESTART")
        print(f"{Fore.YELLOW}{'='*70}\n")
    
    print_info("[1/3] Stopping server...")
    run_command('taskkill /F /IM pythonw.exe')
    print_success("Stopped")
    
    print_info("[2/3] Cleanup (3 seconds)...")
    time.sleep(3)
    print_success("Done")
    
    print_info("[3/3] Starting server...")
    code = run_command(f'schtasks /Run /TN "{CONFIG["TASK_NAME"]}"', capture=False)
    
    if code == 0:
        print_success("Started")
        fancy_progress_bar(8, "Waiting for initialization")
        
        if check_server_running():
            print_success("RESTART SUCCESSFUL!")
            print_info("Opening browsers...")
            os.startfile(CONFIG['LOCALHOST_URL'])
            os.startfile(CONFIG['GITHUB_URL'])
            print_success("Done!")
        else:
            print_warning("Server restarted but not responding yet")
    else:
        print_error("Failed to restart!")
    
    input("\nPress ENTER to continue...")

def check_status():
    """Check server status"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold cyan]STATUS REPORT[/bold cyan]", border_style="cyan"))
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Component", style="cyan", width=20)
        table.add_column("Status", style="green", width=15)
        table.add_column("Details", style="yellow")
        
        # Task status
        task_exists = check_task_exists()
        table.add_row(
            "Scheduled Task",
            "✅ EXISTS" if task_exists else "❌ NOT FOUND",
            CONFIG['TASK_NAME'] if task_exists else "Create task first"
        )
        
        # Process status
        pythonw_running = check_pythonw_running()
        table.add_row(
            "pythonw.exe Process",
            "✅ RUNNING" if pythonw_running else "❌ STOPPED",
            "Server active" if pythonw_running else "Server not running"
        )
        
        # Port status
        server_running = check_server_running()
        table.add_row(
            "HTTP Server",
            "✅ LISTENING" if server_running else "❌ OFFLINE",
            f"Port {CONFIG['SERVER_PORT']}" if server_running else "Not accessible"
        )
        
        console.print(table)
    else:
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  STATUS REPORT")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        task_exists = check_task_exists()
        if task_exists:
            print_success(f"Task: {CONFIG['TASK_NAME']}")
        else:
            print_error("Task: NOT FOUND")
        
        if check_pythonw_running():
            print_success("Process: pythonw.exe RUNNING")
        else:
            print_error("Process: pythonw.exe STOPPED")
        
        if check_server_running():
            print_success(f"HTTP: LISTENING on port {CONFIG['SERVER_PORT']}")
        else:
            print_error(f"HTTP: NOT LISTENING on port {CONFIG['SERVER_PORT']}")
    
    input("\nPress ENTER to continue...")

def delete_task():
    """Delete scheduled task"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold red]DELETE TASK[/bold red]", border_style="red"))
    else:
        print(f"\n{Fore.RED}{'='*70}")
        print(f"{Fore.RED}  DELETE TASK")
        print(f"{Fore.RED}{'='*70}\n")
    
    confirm = input(f"{Fore.YELLOW}Are you sure you want to delete the task? (Y/N): {Style.RESET_ALL}")
    
    if confirm.upper() != 'Y':
        return
    
    print_info("Stopping pythonw.exe...")
    run_command('taskkill /F /IM pythonw.exe')
    
    print_info(f"Deleting task: {CONFIG['TASK_NAME']}")
    code = run_command(f'schtasks /Delete /TN "{CONFIG["TASK_NAME"]}" /F', capture=False)
    
    if code == 0:
        print_success("Task deleted successfully!")
    else:
        print_error("Failed to delete task!")
    
    input("\nPress ENTER to continue...")

def open_task_scheduler():
    """Open Windows Task Scheduler"""
    os.system('start taskschd.msc')

def test_connection():
    """Test HTTP connection"""
    clear_screen()
    print_banner()
    
    if HAS_RICH:
        console.print(Panel("[bold cyan]CONNECTION TEST[/bold cyan]", border_style="cyan"))
    else:
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  CONNECTION TEST")
        print(f"{Fore.CYAN}{'='*70}\n")
    
    print_info("Opening browsers...")
    os.startfile(CONFIG['LOCALHOST_URL'])
    os.startfile(CONFIG['GITHUB_URL'])
    
    print_info("Testing endpoint availability...")
    time.sleep(1)
    
    if check_server_running():
        print_success(f"Connection successful! Port {CONFIG['SERVER_PORT']} LISTENING")
    else:
        print_error(f"Connection failed! Port {CONFIG['SERVER_PORT']} CLOSED")
    
    input("\nPress ENTER to continue...")

# ═════════════════════════════════════════════════════════════════════
# MAIN PROGRAM
# ═════════════════════════════════════════════════════════════════════

def main():
    """Main program loop"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        if HAS_RICH:
            choice = Prompt.ask("\n[bold cyan]Select option[/bold cyan]", 
                              choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"])
        else:
            choice = input(f"\n{Fore.CYAN}Select option (0-8): {Style.RESET_ALL}")
        
        if choice == '1':
            create_task()
        elif choice == '2':
            start_server()
        elif choice == '3':
            stop_server()
        elif choice == '4':
            restart_server()
        elif choice == '5':
            check_status()
        elif choice == '6':
            delete_task()
        elif choice == '7':
            open_task_scheduler()
        elif choice == '8':
            test_connection()
        elif choice == '0':
            clear_screen()
            if HAS_RICH:
                console.print(Panel(
                    "[bold green]Thank you for using Fire and Forget Manager!\n\n"
                    "🚀 Your Quick App Launcher is ready![/bold green]",
                    border_style="green"
                ))
            else:
                print(f"\n{Fore.GREEN}{'='*70}")
                print(f"{Fore.GREEN}  Thank you for using Fire and Forget Manager!")
                print(f"{Fore.GREEN}  Your Quick App Launcher is ready!")
                print(f"{Fore.GREEN}{'='*70}\n")
            time.sleep(2)
            break
        else:
            print_error("Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        input("\nPress ENTER to exit...")
        sys.exit(1)
