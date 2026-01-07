# 🚀 Quick Register Guide

## The Fastest Way to Register

### 1. Make sure server is running
```powershell
cd C:\AIArena\backend
python start_server.py
```

### 2. Open browser
Go to: **http://localhost:8000/docs**

### 3. Find Registration
- Look for: **POST /api/auth/register**
- Click **"Try it out"**

### 4. Paste this JSON
```json
{
  "email": "bobbystandish1@gmail.com",
  "username": "bobbystandish",
  "password": "password1",
  "full_name": "Bobby Standish",
  "roles": ["spectator"]
}
```

### 5. Click "Execute"

### 6. You should get:
- Status: **201 Created**
- Response with your `access_token`

## If You Get an Error

**400 Bad Request:**
- Email or username already exists
- Try changing the email/username

**500 Internal Server Error:**
- Check the server terminal window
- Look for error messages
- Share the error with me

## Visual Guide

```
Swagger UI Page
├── Authentication section
│   └── POST /api/auth/register
│       ├── [Click "Try it out"]
│       ├── Request body (paste JSON)
│       └── [Click "Execute"]
└── Response section (shows result)
```

---

**That's it! Simple 6-step process! 🎯**

