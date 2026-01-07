# Virtual Environment Setup

## Issue
The venv is activated but packages are installing to user directory instead of venv.

## Solution

### Option 1: Use the global Python (Recommended for now)
Since packages are already installed globally, you can run without the venv:

```powershell
# Deactivate venv
deactivate

# Run server
cd C:\AIArena\backend
python start_server.py
```

### Option 2: Fix the venv
If you want to use the venv properly:

```powershell
# Make sure venv is activated
& c:/BigglesBot/venv/Scripts/Activate.ps1

# Install with --force-reinstall to venv
cd C:\AIArena\backend
pip install --force-reinstall --no-deps uvicorn[standard] fastapi
```

### Option 3: Create a new venv for AIArena
```powershell
cd C:\AIArena\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Current Status
✅ All packages are installed (globally)
✅ Server should work with global Python
✅ Just run: `python start_server.py` (without venv)

---

**The server should work now! Try running it without the venv activated.**

