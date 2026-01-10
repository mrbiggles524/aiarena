# 🚨 URGENT: Fix Database to Stop Losing Data

## ⚠️ CURRENT PROBLEM
Your app is using **SQLite** which **deletes all data** on every deployment!

**Evidence:**
- Health check shows: `"database_type": "SQLite"`
- Bounties keep disappearing
- Login works but data is lost

## ✅ THE FIX (5 Minutes)

### Step 1: Get PostgreSQL URL
1. Go to Railway: https://railway.app
2. Click on **"Postgres"** service (the database, not "web")
3. Click **"Variables"** tab
4. Find **`DATABASE_URL`** or **`POSTGRES_URL`**
5. **Copy the entire value** (looks like: `postgresql://user:pass@host:port/dbname`)

### Step 2: Add to Web Service
1. Click on **"web"** service (your app)
2. Click **"Variables"** tab
3. Click **"+ New Variable"** button
4. **Name:** `DATABASE_URL`
5. **Value:** Paste the PostgreSQL URL you copied
6. Click **"Add"**

### Step 3: Wait for Redeploy
1. Railway will automatically redeploy (2-3 minutes)
2. Check: https://web-production-fb8c.up.railway.app/health
3. Should now show: `"database_type": "PostgreSQL"` ✅

### Step 4: Test
1. Register/login
2. Create a bounty
3. Wait 5 minutes
4. Refresh - bounty should still be there! 🎉

## 🔍 How to Verify It's Fixed

After adding DATABASE_URL, check the health endpoint:
```
https://web-production-fb8c.up.railway.app/health
```

**Before (WRONG):**
```json
{
  "database_type": "SQLite",
  "warning": "Using SQLite on Railway..."
}
```

**After (CORRECT):**
```json
{
  "database_type": "PostgreSQL",
  "database_connected": true,
  "bounty_count": 1
}
```

## ⏱️ Do This NOW

**This is why your bounties keep disappearing!** 

Once you add `DATABASE_URL` to the web service, your data will persist forever.

---

**Time needed: 5 minutes** ⏱️
**Result: Data will never be lost again** ✅

