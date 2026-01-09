# 🔧 FIX RAILWAY DATABASE - Step by Step

## ⚠️ CRITICAL ISSUE
Your app is using SQLite instead of PostgreSQL on Railway, causing data loss on every deployment.

## ✅ SOLUTION - Follow These Steps EXACTLY:

### Step 1: Verify PostgreSQL is Added
1. Go to Railway Dashboard: https://railway.app
2. Open your project
3. You should see TWO services:
   - ✅ **Postgres** (database service)
   - ✅ **web** (your app service)

### Step 2: Check if Services are Linked
1. Click on your **web** service (not Postgres)
2. Go to **"Variables"** tab
3. Look for `DATABASE_URL` variable
4. It should show: `postgresql://...` (NOT `sqlite://`)

### Step 3: If DATABASE_URL is Missing or Wrong

**Option A: Railway Auto-Link (Preferred)**
1. In Railway, click on **Postgres** service
2. Go to **"Variables"** tab
3. Copy the `DATABASE_URL` value
4. Go to **web** service → **Variables** tab
5. Click **"+ New Variable"**
6. Name: `DATABASE_URL`
7. Value: Paste the PostgreSQL URL you copied
8. Click **"Add"**

**Option B: Manual Link**
1. In Railway, make sure both services are in the same project
2. Railway should auto-link them
3. If not, check service settings

### Step 4: Verify the Fix
1. After setting DATABASE_URL, Railway will auto-redeploy
2. Wait 2-3 minutes
3. Check health endpoint: https://web-production-fb8c.up.railway.app/health
4. Look for: `"database_type": "PostgreSQL"` (NOT "SQLite")

### Step 5: Test Data Persistence
1. Register/login
2. Create a bounty
3. Wait 5 minutes
4. Refresh page - bounty should still be there
5. If it's gone, DATABASE_URL is still wrong

## 🚨 Common Issues:

**"DATABASE_URL not found"**
- PostgreSQL service might not be linked
- Add DATABASE_URL manually (Step 3)

**"Still using SQLite"**
- DATABASE_URL is set but wrong value
- Make sure it starts with `postgresql://`
- Check for typos

**"Connection refused"**
- Database service might be stopped
- Restart PostgreSQL service in Railway

**"Data still lost"**
- You're still using SQLite
- Double-check DATABASE_URL value

## ✅ Success Indicators:

When it's working, you'll see:
- Health check shows: `"database_type": "PostgreSQL"`
- Health check shows: `"database_connected": true`
- Data persists after deployments
- Login works consistently
- Bounties don't disappear

---

**After fixing, your data will persist forever!** 🎉

