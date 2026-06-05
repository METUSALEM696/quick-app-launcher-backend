# Quick App Launcher — Backend

Server Python pentru **ESP32 Pro Control** / Quick App Launcher.  
Frontend (panou web): https://METUSALEM969.github.io/quick-app-launcher/

## Instalare rapidă

```powershell
git clone https://github.com/metusalem969-ro/esp32-pro-control-backend.git
cd esp32-pro-control-backend
pip install -r requirements.txt
```

## Pornire server (PC Windows)

**Variantă simplă:** dublu-click pe `START_SERVER.bat` sau `QUICK_START.bat`

**Variantă manuală:**
```powershell
python server_fire_and_forget.py
```

Serverul ascultă pe **portul 8899**:
- Local: http://localhost:8899/
- Panou telefon (local): http://localhost:8899/local/index.html
- Ping: http://localhost:8899/ping

## Utilizare remote (telefon → PC)

1. Pornește serverul pe PC (`server_fire_and_forget.py`).
2. Deschide pe telefon: https://METUSALEM969.github.io/quick-app-launcher/
3. În setările paginii, pune **IP-ul PC-ului** (ex. `192.168.1.10`) și portul **8899**.
4. Telefonul și PC-ul trebuie pe **aceeași rețea Wi‑Fi**.
5. Permite portul **8899** în **Firewall Windows** (regulă inbound TCP).

### Din rețea externă (internet)

GitHub Pages nu poate rula Python — serverul rămâne pe PC-ul tău. Pentru acces de oriunde:
- **Port forwarding** pe router (8899 → IP PC), sau
- **Tailscale / ZeroTier / VPN** (recomandat, mai sigur)

## Personalizare aplicații

Editează dicționarul `APPS` din `server_fire_and_forget.py` cu căile tale (VS Code, Chrome, etc.).

## Scripturi utile

| Fișier | Rol |
|--------|-----|
| `server_fire_and_forget.py` | Server HTTP principal |
| `QUICK_START.bat` | Pornește server + deschide browsere |
| `F2_Hotkey_Listener.py` | Hotkey F2 pentru launcher |
| `fire_and_forget_manager.py` | Task Scheduler (autostart) |
| `STOP_ALL_SERVERS_ULTRA.py` | Oprește serverul |

## Repo frontend

https://github.com/METUSALEM969/quick-app-launcher
