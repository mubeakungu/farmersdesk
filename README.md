# FarmersDesk Ltd – Packaging & Deployment Guide
=====================================================

## Architecture Overview

```
┌────────────────────────────────────┐
│         SERVER MACHINE             │
│  • SQL Server Express running      │
│  • Database: FarmersDeskLtd        │
│  • Python + build tools here only  │
│  • Also runs FarmersDesk.exe       │
└──────────────┬─────────────────────┘
               │  LAN / Network
    ┌──────────┴──────────────┐
    │                         │
┌───┴────────┐         ┌──────┴─────┐
│  CLIENT 1  │         │  CLIENT 2  │
│ FarmersDesk│         │ FarmersDesk│
│  .exe only │   ...   │  .exe only │
│ No Python  │         │ No Python  │
└────────────┘         └────────────┘
```

---

## PART 1 – Build the EXE  (done ONCE on your server/build machine)

### Prerequisites on the build machine only:
- Windows 10 or 11
- Python 3.10, 3.11, or 3.12  →  https://python.org/downloads
  ⚠️  During install tick **"Add Python to PATH"**
- Internet connection (to download packages)

### Steps:

1. Put these files in ONE folder together:
   ```
   farmersdesk.py          ← your application
   FarmersDesk.spec        ← from this package
   build.bat               ← from this package
   FarmersDesk_Installer.iss ← from this package
   farmersdesk.ico         ← (optional) your app icon
   ```

2. **Double-click `build.bat`**
   - It installs all Python packages automatically
   - It runs PyInstaller
   - When done, a folder appears:  `dist\FarmersDesk\`
   - That folder IS the application (self-contained, no Python needed)

3. **Test it right away:**
   Double-click `dist\FarmersDesk\FarmersDesk.exe`
   It should open, connect to your local DB, and log in.

---

## PART 2 – Create the Installer EXE  (makes deployment easier)

Instead of copying a whole folder to each PC, create ONE installer .exe.

1. Download and install **Inno Setup** (free):
   https://jrsoftware.org/isinfo.php

2. Open `FarmersDesk_Installer.iss` in Inno Setup Compiler

3. Click **Build → Compile** (or press F9)

4. A file appears:  `installer_output\FarmersDesk_Setup.exe`

That single file is your installer. Copy it to a USB stick or shared network folder.

---

## PART 3 – Install on Client PCs  (repeat for each machine)

Each client PC needs TWO things installed (both free):

### Step A – ODBC Driver (one-time, ~2 min)
Download from Microsoft:
https://aka.ms/downloadmsodbcsql

Install **"ODBC Driver 17 for SQL Server"** (the installer already warns if it's missing).

### Step B – Run FarmersDesk_Setup.exe
- Double-click the installer
- Accept defaults
- A desktop shortcut is created automatically
- Done ✓

---

## PART 4 – Network / Firewall Configuration

### On the SERVER machine:

1. **SQL Server must accept remote connections:**
   - Open **SQL Server Configuration Manager**
   - SQL Server Network Configuration → Protocols for SQLEXPRESS01
   - Enable **TCP/IP**
   - Restart the SQL Server service

2. **Find your server's IP address:**
   Open CMD and type:  `ipconfig`
   Note the IPv4 address, e.g. `192.168.1.10`

3. **Open firewall port 1433:**
   - Windows Defender Firewall → Advanced Settings
   - Inbound Rules → New Rule → Port → TCP → 1433
   - Allow the connection

### Update the app's connection string:

In `farmersdesk.py`, find this block near the top and update the server line
before you build the EXE:

```python
DB_CONFIG = {
    "driver":   "ODBC Driver 17 for SQL Server",
    "server":   "192.168.1.10\\SQLEXPRESS01",   # ← put your server's IP here
    "database": "FarmersDeskLtd",
    "trusted":  False,
    "uid":      "pos",
    "pwd":      "pos2026",
}
```

Replace `192.168.1.10` with your server's actual LAN IP address.
Then rebuild using `build.bat`.

> **Tip:** Use a **static IP** on your server machine so this never changes.
> (Router settings → DHCP → Reserve IP for server's MAC address)

---

## PART 5 – SQL Server User Setup (if not done yet)

Run this on your SQL Server (in SSMS) to create the `pos` login:

```sql
-- Create login
CREATE LOGIN pos WITH PASSWORD = 'pos2026';

-- Give access to the database
USE FarmersDeskLtd;
CREATE USER pos FOR LOGIN pos;

-- Grant permissions
ALTER ROLE db_datareader ADD MEMBER pos;
ALTER ROLE db_datawriter ADD MEMBER pos;
GRANT EXECUTE TO pos;
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot reach database" on login | Check server IP in DB_CONFIG, check firewall port 1433, check SQL Server TCP/IP is enabled |
| "ODBC Driver not found" | Install ODBC Driver 17 from https://aka.ms/downloadmsodbcsql |
| App opens then crashes | Right-click EXE → Run as Administrator (first time only) |
| Printer not working | Open app → 🖨 Printer button → configure USB/Network/Serial settings |
| Build fails on `win32api` | Run: `pip install pywin32` then `python Scripts/pywin32_postinstall.py -install` |

---

## Quick Reference – File Locations

| File | Purpose |
|---|---|
| `build.bat` | Run once on build machine to produce the EXE |
| `FarmersDesk.spec` | PyInstaller config (no edits needed) |
| `FarmersDesk_Installer.iss` | Inno Setup script → makes installer .exe |
| `dist\FarmersDesk\` | The built app folder |
| `installer_output\FarmersDesk_Setup.exe` | Final installer to copy to client PCs |
| `printer_cfg.json` | Auto-created in app folder; stores printer settings |
