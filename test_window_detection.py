"""
🔍 Window Detection Test Script
Use this to find the correct window titles for your apps!
"""

import time

print("=" * 70)
print("🔍 WINDOW DETECTION TEST")
print("=" * 70)
print()

# Try win32gui first (preferred on Windows)
try:
    import win32gui
    
    print("✅ Using WIN32GUI (Best for Windows)")
    print()
    print("Current windows:")
    print("-" * 70)
    
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Only show windows with titles
                results.append(title)
    
    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    
    for i, title in enumerate(sorted(windows), 1):
        print(f"{i:3}. {title}")
    
    print()
    print(f"Total: {len(windows)} windows")
    print()
    print("=" * 70)
    print("📝 INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("1. Launch your app (e.g., VS Code, Chrome, etc.)")
    print("2. Run this script again")
    print("3. Find the window title in the list")
    print("4. Copy PART of the title that's unique")
    print("5. Update WINDOW_PATTERNS in server_fire_and_forget.py")
    print()
    print("Example:")
    print('  Window title: "main.py - Visual Studio Code"')
    print('  Pattern to use: "Visual Studio Code"')
    print()
    print("=" * 70)
    print()
    
    # Test specific patterns
    test_patterns = {
        "VS Code": "Visual Studio Code",
        "Chrome": "Google Chrome",
        "Notepad": "Notepad",
        "Calculator": "Calculator",
    }
    
    print("🧪 Testing common patterns:")
    print("-" * 70)
    
    for name, pattern in test_patterns.items():
        found = [w for w in windows if pattern.lower() in w.lower()]
        if found:
            print(f"✅ {name:15} → Found {len(found)} window(s)")
            for w in found[:3]:  # Show first 3
                print(f"   - {w}")
        else:
            print(f"❌ {name:15} → Not found")
    
    print()
    print("=" * 70)
    
except ImportError:
    print("⚠️  WIN32GUI not available")
    print()
    
    # Fallback to pygetwindow
    try:
        import pygetwindow as gw
        
        print("✅ Using PYGETWINDOW (Fallback)")
        print()
        print("Current windows:")
        print("-" * 70)
        
        windows = gw.getAllTitles()
        windows = [w for w in windows if w]  # Filter empty titles
        
        for i, title in enumerate(sorted(windows), 1):
            print(f"{i:3}. {title}")
        
        print()
        print(f"Total: {len(windows)} windows")
        
    except ImportError:
        print("❌ No window control library installed!")
        print()
        print("Install one of:")
        print("  pip install pywin32 --break-system-packages")
        print("  pip install pygetwindow --break-system-packages")

input("\nPress Enter to exit...")
