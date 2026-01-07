# 🚂 Deploy to Railway.app - Step by Step

## Prerequisites

1. GitHub account
2. Railway.app account (free $5 credit/month)

## Steps

1. **Push code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Go to Railway:**
   - Visit https://railway.app
   - Sign up with GitHub

3. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `ai-arena` repository

4. **Railway Auto-Detection:**
   - Railway will detect it's a Python app
   - It will look for `requirements.txt` in `backend/`
   - It will try to run the app

5. **Configure Settings:**
   - Go to "Settings" → "Deploy"
   - **Root Directory:** Leave empty (or set to `/`)
   - **Start Command:** `cd backend && python start_server.py`
   - **Watch Paths:** `backend/**`

6. **Add Environment Variables:**
   - Go to "Variables" tab
   - Add:
     - `SECRET_KEY` = (generate new: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
     - `GOOGLE_API_KEY` = (your key)
     - `FRONTEND_URL` = (will be shown after deploy)
     - `DATABASE_URL` = (Railway will auto-create PostgreSQL)

7. **Add PostgreSQL Database:**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will auto-set `DATABASE_URL`

8. **Deploy:**
   - Railway will automatically deploy
   - Wait 2-5 minutes
   - Get your URL from the "Settings" → "Domains" tab

9. **Generate Domain:**
   - Click "Generate Domain" to get a public URL
   - Your app is live! 🎉

## Update Your App

Just push to GitHub and Railway auto-deploys!

```bash
git add .
git commit -m "Update"
git push
```

---

**Your app will be live at:** `https://your-app-name.up.railway.app` 🎉

