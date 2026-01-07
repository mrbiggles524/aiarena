# Railway Deployment - Next Steps

## ✅ Your App Domain
**Your public URL:** `https://web-production-fb8c.up.railway.app`

## Step 1: Check Deployment Status

1. Go to Railway Dashboard
2. Click on your service
3. Check the "Deployments" tab
4. Look for the latest deployment - it should show:
   - ✅ **Active** (green) = Working!
   - ⏳ **Building** = Still deploying
   - ❌ **Failed** = Check logs

## Step 2: Add Environment Variables

Go to your service → **Variables** tab → Add these:

### Required Variables:

1. **SECRET_KEY**
   - Generate one: Run this in PowerShell:
     ```powershell
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - Copy the output and paste as the value

2. **GOOGLE_API_KEY**
   - Your existing Gemini API key
   - (The one from your `.env` file)

3. **FRONTEND_URL**
   - Set to: `https://web-production-fb8c.up.railway.app`
   - (Your Railway domain)

### Optional Variables:
- `DATABASE_URL` - Auto-set when you add PostgreSQL
- `STRIPE_SECRET_KEY` - If you want payments

## Step 3: Add PostgreSQL Database

1. In Railway Dashboard, click **"New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway automatically:
   - Creates the database
   - Sets `DATABASE_URL` environment variable
   - Links it to your service

## Step 4: Test Your App

1. Open: `https://web-production-fb8c.up.railway.app`
2. You should see your beautiful UI!
3. Try registering a new user
4. Check API docs: `https://web-production-fb8c.up.railway.app/docs`

## Step 5: Update Domain Settings (Optional)

### Custom Domain
If you want a custom domain (like `aiarena.com`):
1. Click **"Custom Domain"** in Networking
2. Add your domain
3. Follow Railway's DNS instructions

### Port Settings
- **Don't change the port** - Railway sets it automatically
- The default (8000) is correct

## Troubleshooting

### If the app doesn't load:

1. **Check Deployment Logs:**
   - Service → Deployments → Latest → "Deploy Logs"
   - Look for errors

2. **Check Environment Variables:**
   - Make sure `SECRET_KEY` is set
   - Make sure `DATABASE_URL` is set (if using PostgreSQL)

3. **Check Build Logs:**
   - Service → Deployments → Latest → "Build Logs"
   - Make sure build succeeded

### Common Issues:

**"Application Error" or 502:**
- Service might be starting up (wait 30 seconds)
- Check Deploy Logs for startup errors
- Make sure all environment variables are set

**"Database connection error":**
- Add PostgreSQL database
- Check that `DATABASE_URL` is set

**"SECRET_KEY not set":**
- Add `SECRET_KEY` in Variables tab

## Quick Test Commands

Test if your API is working:
```bash
# Health check
curl https://web-production-fb8c.up.railway.app/health

# API docs
# Open in browser: https://web-production-fb8c.up.railway.app/docs
```

## Your App URLs

- **Main App:** https://web-production-fb8c.up.railway.app
- **API Docs:** https://web-production-fb8c.up.railway.app/docs
- **Health Check:** https://web-production-fb8c.up.railway.app/health

---

**Next:** Add environment variables and test your app! 🚀

