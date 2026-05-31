# 🎹 GHID PERSONALIZARE HOTKEYS - Fire and Forget Launcher

## ✅ MODIFICARE APLICATĂ: F8 → F3

Script-ul tău a fost deja modificat cu **F3** în loc de **F8** pentru File Explorer!

### Hotkeys Actuale:

```
F2         = Fire and Forget Launcher
F3         = File Explorer          ← NOU! (era F8)
F9         = Control Panel
F10        = Task Scheduler
F11        = Task Manager
F12        = Statistici + Toggle Beep
Ctrl+F12   = Restart Listener
Ctrl+Alt+B = Test Beep
```

---

## 🎨 ALTE COMBINAȚII POSIBILE

Dacă vrei să schimbi și alte hotkeys, iată opțiunile:

### 📋 **1. Taste Simple (F1-F12)**

```python
# Exemple:
keyboard.add_hotkey('f1', functie, suppress=True)
keyboard.add_hotkey('f3', functie, suppress=True)
keyboard.add_hotkey('f4', functie, suppress=True)
keyboard.add_hotkey('f5', functie, suppress=True)
keyboard.add_hotkey('f6', functie, suppress=True)
keyboard.add_hotkey('f7', functie, suppress=True)
```

**Avantaje:** Rapid de apăsat  
**Dezavantaje:** Pot intra în conflict cu alte aplicații

---

### 🎯 **2. Combinații Ctrl+ (Recomandate!)**

```python
keyboard.add_hotkey('ctrl+e', open_explorer, suppress=True)        # Explorer
keyboard.add_hotkey('ctrl+l', open_launcher, suppress=True)        # Launcher
keyboard.add_hotkey('ctrl+t', open_task_manager, suppress=True)    # Task Manager
keyboard.add_hotkey('ctrl+shift+t', open_task_scheduler, suppress=True)
keyboard.add_hotkey('ctrl+p', open_control_panel, suppress=True)   # Control Panel
```

**Avantaje:** Mai puține conflicte, mai profesional  
**Dezavantaje:** Trebuie două taste

---

### 🚀 **3. Combinații Alt+**

```python
keyboard.add_hotkey('alt+e', open_explorer, suppress=True)
keyboard.add_hotkey('alt+l', open_launcher, suppress=True)
keyboard.add_hotkey('alt+t', open_task_manager, suppress=True)
keyboard.add_hotkey('alt+c', open_control_panel, suppress=True)
```

**Avantaje:** Rapid și puține conflicte  
**Dezavantaje:** Unele aplicații folosesc Alt+

---

### 💪 **4. Combinații Win+ (Windows Key)**

```python
keyboard.add_hotkey('win+e', open_explorer, suppress=True)      # Explorer
keyboard.add_hotkey('win+l', open_launcher, suppress=True)      # Launcher
keyboard.add_hotkey('win+t', open_task_manager, suppress=True)  # Task Manager
```

**Avantaje:** Foarte puține conflicte  
**Dezavantaje:** Windows deja folosește unele (Win+E = Explorer nativ)

---

### 🎨 **5. Combinații Triple (Ctrl+Shift+)**

```python
keyboard.add_hotkey('ctrl+shift+e', open_explorer, suppress=True)
keyboard.add_hotkey('ctrl+shift+l', open_launcher, suppress=True)
keyboard.add_hotkey('ctrl+shift+t', open_task_scheduler, suppress=True)
keyboard.add_hotkey('ctrl+alt+e', open_explorer, suppress=True)
```

**Avantaje:** ZERO conflicte  
**Dezavantaje:** Mai greu de apăsat

---

## 🛠️ CUM SĂ MODIFICI HOTKEYS-URILE

### Metoda 1: Editare Manuală (Simplu)

**1. Deschide fișierul:**
```
E:\script\Quick App Launcher\New folder\F2_Hotkey_Listener.py
```

**2. Caută secțiunea (linia ~492):**
```python
keyboard.add_hotkey('f2', open_launcher, suppress=True)
keyboard.add_hotkey('f3', open_explorer, suppress=True)
keyboard.add_hotkey('f9', open_control_panel, suppress=True)
```

**3. Schimbă ce vrei:**
```python
# Exemplu: F9 → Ctrl+P pentru Control Panel
keyboard.add_hotkey('ctrl+p', open_control_panel, suppress=True)
```

**4. NU UITA să schimbi și în funcție:**
```python
@safe_wrapper
def open_control_panel():
    if not debounce_check("Ctrl+P"):  # ← Schimbă și aici!
        return
    
    log("⚙️  Ctrl+P APASAT! Deschid Control Panel...")  # ← Și aici!
    increment_stat("CtrlP_ControlPanel")  # ← Și aici!
```

**5. Actualizează mesajele informative (linia ~470):**
```python
log("   Ctrl+P = Control Panel")  # ← Schimbă mesajul
```

**6. Salvează și repornește:**
```batch
# Oprește listener-ul
schtasks /End /TN "F2_PYTHON_LISTENER"

# Pornește din nou
schtasks /Run /TN "F2_PYTHON_LISTENER"

# SAU apasă Ctrl+F12 (dacă listener-ul rulează)
```

---

## 📝 EXEMPLE COMPLETE DE CONFIGURAȚII

### 🎯 **Configurație 1: Taste F (Rapid)**

```python
keyboard.add_hotkey('f2', open_launcher, suppress=True)
keyboard.add_hotkey('f3', open_explorer, suppress=True)
keyboard.add_hotkey('f4', open_control_panel, suppress=True)
keyboard.add_hotkey('f5', open_task_scheduler, suppress=True)
keyboard.add_hotkey('f6', open_task_manager, suppress=True)
keyboard.add_hotkey('f12', toggle_beep_and_stats, suppress=True)
```

### 🎯 **Configurație 2: Ctrl+ (Profesional)**

```python
keyboard.add_hotkey('ctrl+l', open_launcher, suppress=True)         # L = Launcher
keyboard.add_hotkey('ctrl+e', open_explorer, suppress=True)         # E = Explorer
keyboard.add_hotkey('ctrl+p', open_control_panel, suppress=True)    # P = Panel
keyboard.add_hotkey('ctrl+shift+t', open_task_scheduler, suppress=True)  # T = Task Scheduler
keyboard.add_hotkey('ctrl+shift+m', open_task_manager, suppress=True)    # M = Manager
keyboard.add_hotkey('f12', toggle_beep_and_stats, suppress=True)
```

### 🎯 **Configurație 3: Alt+ (Balansat)**

```python
keyboard.add_hotkey('f2', open_launcher, suppress=True)       # F2 = Launcher (main)
keyboard.add_hotkey('alt+e', open_explorer, suppress=True)
keyboard.add_hotkey('alt+c', open_control_panel, suppress=True)
keyboard.add_hotkey('alt+s', open_task_scheduler, suppress=True)  # S = Scheduler
keyboard.add_hotkey('alt+m', open_task_manager, suppress=True)    # M = Manager
keyboard.add_hotkey('f12', toggle_beep_and_stats, suppress=True)
```

### 🎯 **Configurație 4: Numpad (Pentru Keyboards cu Numpad)**

```python
keyboard.add_hotkey('num1', open_launcher, suppress=True)
keyboard.add_hotkey('num2', open_explorer, suppress=True)
keyboard.add_hotkey('num3', open_control_panel, suppress=True)
keyboard.add_hotkey('num4', open_task_scheduler, suppress=True)
keyboard.add_hotkey('num5', open_task_manager, suppress=True)
```

---

## ⚠️ ATENȚIE LA CONFLICTE!

### Combinații Deja Folosite de Windows:

```
Win+E     = File Explorer (nativ Windows)
Win+R     = Run dialog
Win+D     = Show Desktop
Win+L     = Lock Screen
Win+Tab   = Task View
Ctrl+C    = Copy
Ctrl+V    = Paste
Ctrl+Z    = Undo
Alt+Tab   = Switch Windows
Alt+F4    = Close Window
```

**Sfat:** Evită aceste combinații! Poți să le override cu `suppress=True`, dar nu e recomandat.

---

## 🔥 RECOMANDĂRI PERSONALE

### Pentru Viteză (Gaming Style):
```python
F2, F3, F4, F5, F6  # Rapid, o singură tastă
```

### Pentru Profesionalism (Office Style):
```python
Ctrl+L, Ctrl+E, Ctrl+P, Ctrl+Shift+T
```

### Pentru Siguranță (Zero Conflicte):
```python
Ctrl+Shift+L, Ctrl+Alt+E, Ctrl+Shift+P
```

---

## 🎮 TASTE SPECIALE DISPONIBILE

```python
# Mouse buttons
keyboard.add_hotkey('mouse4', functie, suppress=True)  # Mouse side button
keyboard.add_hotkey('mouse5', functie, suppress=True)

# Numpad
keyboard.add_hotkey('num0', functie, suppress=True)
keyboard.add_hotkey('num1', functie, suppress=True)
# ... până la num9

# Litere
keyboard.add_hotkey('a', functie, suppress=True)
keyboard.add_hotkey('b', functie, suppress=True)
# ... toate literele

# Simboluri
keyboard.add_hotkey('-', functie, suppress=True)
keyboard.add_hotkey('=', functie, suppress=True)
keyboard.add_hotkey('[', functie, suppress=True)

# Combinații complexe
keyboard.add_hotkey('ctrl+shift+alt+f12', functie, suppress=True)  # 4 taste!
```

---

## 📊 TEMPLATE COMPLET PENTRU MODIFICARE

Folosește acest template pentru a schimba orice hotkey:

```python
# ============================================================
# PAS 1: Modifică funcția
# ============================================================

@safe_wrapper
def open_NUME_FUNCTIE():
    if not debounce_check("HOTKEY_NOU"):  # ex: "Ctrl+E"
        return
    
    log("🔥 HOTKEY_NOU APASAT! Descriere...")
    increment_stat("HotkeyNou_Descriere")
    beep()
    
    subprocess.Popen(["comanda"], shell=True, ...)
    log("   ✓ Success!", "OK")
    show_notification("Titlu", "Mesaj")

# ============================================================
# PAS 2: Înregistrează hotkey-ul (în main(), linia ~492)
# ============================================================

keyboard.add_hotkey('hotkey_nou', open_NUME_FUNCTIE, suppress=True)

# ============================================================
# PAS 3: Actualizează mesajele informative (linia ~470)
# ============================================================

log("   HOTKEY_NOU = Descriere")
```

---

## 🚀 APLICARE RAPIDĂ

După modificare:

### Metodă 1: Restart Manual
```batch
schtasks /End /TN "F2_PYTHON_LISTENER"
timeout /t 2
schtasks /Run /TN "F2_PYTHON_LISTENER"
```

### Metodă 2: Hotkey de Restart
```
Apasă: Ctrl+F12 (dacă listener-ul rulează)
```

### Metodă 3: Re-instalare Completă
```batch
F2_INSTALLER_v2.3_DETACHED.bat
```

---

## 🎯 EXEMPLU PRACTIC: Schimbare F9 → Ctrl+P

### Înainte:
```python
keyboard.add_hotkey('f9', open_control_panel, suppress=True)
```

### După:

**1. Modifică înregistrarea:**
```python
keyboard.add_hotkey('ctrl+p', open_control_panel, suppress=True)
```

**2. Modifică funcția:**
```python
@safe_wrapper
def open_control_panel():
    if not debounce_check("Ctrl+P"):  # Era "F9"
        return
    
    log("⚙️  Ctrl+P APASAT! Deschid Control Panel...")  # Era "F9 APASAT"
    increment_stat("CtrlP_ControlPanel")  # Era "F9_ControlPanel"
```

**3. Modifică mesajul:**
```python
log("   Ctrl+P = Control Panel")  # Era "F9 = Control Panel"
```

**4. Salvează și repornește!**

---

## 📚 DOCUMENTAȚIE COMPLETĂ KEYBOARD MODULE

Pentru combinații mai complexe, vezi:
- [keyboard module docs](https://github.com/boppreh/keyboard)
- Toate tastele suportate: `keyboard.all_modifiers`, `keyboard.all_keys`

---

**Creat:** 2024-12-25  
**Versiune Script:** v2.3 DETACHED  
**Modificare Aplicată:** F8 → F3 ✅
