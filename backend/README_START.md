# 🚀 How to Start the Server

## Quick Start

1. **Navigate to backend directory:**
   ```powershell
   cd C:\AIArena\backend
   ```

2. **Start the server:**
   ```powershell
   python start_server.py
   ```
   
   Or directly:
   ```powershell
   python main.py
   ```

3. **Access the API:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health
   - **API Root**: http://localhost:8000/

## Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### "email-validator not found"
```powershell
pip install email-validator
```

### Port already in use
Change the port in `main.py` or `start_server.py`:
```python
uvicorn.run("main:app", port=8001, ...)
```

### Server won't start
Check for import errors:
```powershell
python -c "from app.api import auth; print('OK')"
```

## What to Expect

When the server starts successfully, you should see:
```
🚀 Starting AI Agent Bounty Arena Server...
📍 Server will be available at: http://localhost:8000
📚 API Docs: http://localhost:8000/docs

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Next Steps

1. Open http://localhost:8000/docs in your browser
2. Test the `/health` endpoint
3. Register a user via `/api/auth/register`
4. Create your first bounty!

---

**Happy coding! 🎉**

