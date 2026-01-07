# How to Add PostgreSQL Database in Railway

## Why You Need PostgreSQL

Right now your app is using SQLite (local file database), but Railway containers are temporary. When Railway redeploys or restarts your service, **all your data will be lost**!

PostgreSQL is a proper database that persists data even when containers restart.

## Step-by-Step Instructions

### Step 1: Go to Railway Dashboard
1. Open: https://railway.app/dashboard
2. You should see your project with your service

### Step 2: Add PostgreSQL Database
1. Click the **"New"** button (top right, green button)
2. A menu will appear
3. Click **"Database"**
4. Click **"Add PostgreSQL"**

### Step 3: Wait for Database to Create
- Railway will automatically:
  - Create the PostgreSQL database
  - Set the `DATABASE_URL` environment variable
  - Link it to your service
- This takes about 30 seconds

### Step 4: Railway Auto-Redeploys
- Railway will automatically detect the new `DATABASE_URL`
- Your service will automatically redeploy
- Wait 1-2 minutes for redeploy to complete

### Step 5: Test It
1. Go to: https://web-production-fb8c.up.railway.app
2. Register a new user
3. Your data will now persist! 🎉

## What Happens Automatically

✅ Railway sets `DATABASE_URL` automatically  
✅ Your app will use PostgreSQL instead of SQLite  
✅ All your data will persist across deployments  
✅ No code changes needed - it just works!

## Verify It's Working

After adding PostgreSQL and redeploying:
1. Register a new user
2. Log out and log back in
3. Your user should still exist (data persisted!)

## That's It!

Just click "New" → "Database" → "Add PostgreSQL" and Railway does the rest!

---

**Note:** Your existing SQLite data (if any) won't transfer automatically, but that's okay - you can just register new users and they'll be stored in PostgreSQL.

