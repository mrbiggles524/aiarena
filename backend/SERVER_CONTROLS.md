# 🎮 Server Control Guide

## Easy Server Management

### 🚀 Start the Server

**Option 1: Double-click (Easiest)**
- Double-click `start_server.bat` in the `backend` folder

**Option 2: Command Line**
```powershell
cd C:\AIArena\backend
python start_server.py
```

### 🛑 Stop the Server

**Option 1: Double-click (Easiest)**
- Double-click `stop_server.bat` in the `backend` folder
- This will kill ALL running servers on port 8000

**Option 2: Command Line**
```powershell
cd C:\AIArena\backend
python stop_server.py
```

**Option 3: Manual (if scripts don't work)**
```powershell
# Find processes on port 8000
netstat -ano | findstr :8000

# Kill specific process (replace PID with actual number)
taskkill /F /PID <PID>
```

### 🔄 Restart the Server

1. Run `stop_server.bat` (or `python stop_server.py`)
2. Wait a few seconds
3. Run `start_server.bat` (or `python start_server.py`)

### ⚠️ Troubleshooting

**If Ctrl+C doesn't work:**
- Use `stop_server.bat` instead
- Or close the terminal window
- Or use Task Manager to kill Python processes

**If multiple servers are running:**
- Run `stop_server.bat` - it will kill ALL servers on port 8000
- Then start fresh with `start_server.bat`

**If port 8000 is still in use:**
```powershell
# Check what's using the port
netstat -ano | findstr :8000

# Kill all Python processes (WARNING: kills ALL Python)
taskkill /F /IM python.exe
```

### 📝 Quick Reference

| Action | Command |
|--------|---------|
| Start | `start_server.bat` or `python start_server.py` |
| Stop | `stop_server.bat` or `python stop_server.py` |
| Check Port | `netstat -ano \| findstr :8000` |
| Kill Process | `taskkill /F /PID <PID>` |

---

**Tip:** Keep `stop_server.bat` handy - it's the easiest way to stop the server!

