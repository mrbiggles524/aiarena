# ✅ Railway Database Setup Checklist

## 🔍 STEP 1: Check Current Status

1. Go to: https://web-production-fb8c.up.railway.app/health
2. Look for these fields:
   - `database_type`: Should be "PostgreSQL" (NOT "SQLite")
   - `database_connected`: Should be `true`
   - `warning`: Should NOT exist

## 🔧 STEP 2: Fix Database Connection

### If `database_type` is "SQLite":

1. **Go to Railway Dashboard**: https://railway.app
2. **Open your project**
3. **Click on "web" service** (your app, not Postgres)
4. **Go to "Variables" tab**
5. **Look for `DATABASE_URL`**:
   - ✅ If it exists and starts with `postgresql://` → You're good!
   - ❌ If it's missing or starts with `sqlite://` → Continue below

### Fix Missing DATABASE_URL:

**Option A: Copy from Postgres Service**
1. Click on **"Postgres"** service
2. Go to **"Variables"** tab
3. Find `DATABASE_URL` or `POSTGRES_URL`
4. **Copy the entire value** (starts with `postgresql://`)
5. Go back to **"web"** service → **Variables**
6. Click **"+ New Variable"**
7. Name: `DATABASE_URL`
8. Value: Paste the PostgreSQL URL
9. Click **"Add"**

**Option B: Railway Auto-Link**
1. Make sure both services are in the same project
2. Railway should auto-link them
3. If not linked, check service settings

## ✅ STEP 3: Verify the Fix

1. **Wait 2-3 minutes** for Railway to redeploy
2. **Check health endpoint again**: https://web-production-fb8c.up.railway.app/health
3. **Verify**:
   - `database_type`: "PostgreSQL" ✅
   - `database_connected`: true ✅
   - No warnings ✅

## 🧪 STEP 4: Test Data Persistence

1. **Register/Login** to your app
2. **Create a test bounty**
3. **Wait 5 minutes**
4. **Hard refresh** (Ctrl+F5)
5. **Check if bounty is still there**
   - ✅ Still there = PostgreSQL working!
   - ❌ Gone = Still using SQLite, check DATABASE_URL again

## 🚨 Troubleshooting

**"DATABASE_URL not found in Variables"**
- PostgreSQL service might not be linked
- Manually add DATABASE_URL (see Option A above)

**"Still shows SQLite after fix"**
- Wait longer for deployment (5 minutes)
- Check Railway logs for errors
- Verify DATABASE_URL value is correct

**"Connection refused"**
- PostgreSQL service might be stopped
- Restart PostgreSQL service in Railway

**"Data still lost"**
- You're still using SQLite
- Double-check DATABASE_URL in Railway Variables
- Make sure it starts with `postgresql://`

---

## ✅ Success Indicators

When everything is working:
- ✅ Health check shows `"database_type": "PostgreSQL"`
- ✅ Health check shows `"database_connected": true`
- ✅ Login works consistently
- ✅ Bounties persist after deployments
- ✅ No data loss on redeploy

**Once PostgreSQL is connected, your data will persist forever!** 🎉

