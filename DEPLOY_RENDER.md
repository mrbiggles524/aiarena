# 🚀 Deploy to Render.com - Step by Step

## Prerequisites

1. GitHub account
2. Render.com account (free)

## Step 1: Prepare Your Code

1. **Make sure your code is on GitHub:**
   ```bash
   cd C:\AIArena
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ai-arena.git
   git push -u origin main
   ```

2. **Update your `.env` file:**
   - Generate a new `SECRET_KEY` for production:
     ```python
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - Keep your `GOOGLE_API_KEY`
   - Remove `DATABASE_URL` (Render will provide PostgreSQL)

## Step 2: Deploy on Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Sign up/Login

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `ai-arena` repository

3. **Configure Service:**
   - **Name:** `ai-arena-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && python start_server.py`
   - **Plan:** Free

4. **Add Environment Variables:**
   Click "Environment" and add:
   - `SECRET_KEY` = (generate a new one)
   - `GOOGLE_API_KEY` = (your existing key)
   - `FRONTEND_URL` = `https://ai-arena-backend.onrender.com`
   - `DATABASE_URL` = (Render will auto-create this)
   - `STRIPE_SECRET_KEY` = (optional, leave empty if not using)

5. **Create Database:**
   - Click "New +" → "PostgreSQL"
   - Name: `aiarena-db`
   - Plan: Free
   - Copy the `Internal Database URL` to your service's `DATABASE_URL` env var

6. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://ai-arena-backend.onrender.com`

## Step 3: Update Database Models

Since you're switching from SQLite to PostgreSQL, you may need to:
1. Update your database connection string
2. Run migrations (if using Alembic)

## Step 4: Test Your Deployment

1. Visit: `https://your-app-name.onrender.com`
2. Test the API: `https://your-app-name.onrender.com/docs`
3. Test the frontend: `https://your-app-name.onrender.com/`

## Troubleshooting

### If deployment fails:
- Check build logs in Render dashboard
- Make sure all dependencies are in `requirements.txt`
- Verify environment variables are set correctly

### If app is slow:
- Free tier spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading to paid plan for always-on

### Database issues:
- Make sure PostgreSQL is created and connected
- Check `DATABASE_URL` is set correctly
- May need to update SQLAlchemy connection string

---

**Your app will be live at:** `https://your-app-name.onrender.com` 🎉

