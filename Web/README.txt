╔══════════════════════════════════════════════════════════╗
║           SR — PRIVATE MENU WEBSITE                 ║
║                    PROJECT NOTES                        ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WHERE ARE MY FILES?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Folder:   Desktop > Web

  Files:
    menu.html    — Customer-facing menu (gate + menu screen)
    admin.html   — Admin panel (password protected)
    server.py    — Backend server (runs everything)
    data.json    — Your menu items, clients & settings
    logo.png     — Your SR logo
    uploads/     — All photos/videos you upload

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW TO START THE WEBSITE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Open Terminal
  2. Type:  cd "/Users/ogsr/Desktop/Web"
  3. Type:  python3 server.py
  4. Keep Terminal open while using the site

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WEBSITE URLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  On your computer:
    Customer menu  →  http://localhost:5050
    Admin panel    →  http://localhost:5050/admin

  On your phone (same WiFi):
    Customer menu  →  http://192.168.1.113:5050
    Admin panel    →  http://192.168.1.113:5050/admin
    (IP may change if you reconnect to WiFi)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LOGIN INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Admin Password:   admin123
  (Change it in Admin > Settings tab)

  Your client entry:
    Handle:
    Code:     VIP2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WHAT THE ADMIN PANEL CAN DO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Menu Items tab:
    - Add / edit / delete listings
    - Upload photos & videos (drag & drop or camera roll)
    - Set status: Available / Pre-Order / Sold Out
    - Categories: Flower, Concentrates, Edibles, Disposables

  Approved Clients tab:
    - Add clients with name, IG handle, phone, access code
    - Generate random codes with one click
    - Copy codes to send to clients
    - Download full client list as CSV (Excel/Sheets)

  Settings tab:
    - Change brand name, tagline, IG handle, phone number
    - Change admin password

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW CLIENTS ACCESS THE MENU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 1 — Client enters their IG handle or phone number
  Step 2 — Client enters their personal access code
  Then they can view the full menu and tap listings for detail

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BACKUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  A backup ZIP is saved on your Desktop:
    SR-Menu-BACKUP-[date].zip
  Re-open this project with Claude anytime to make changes.
