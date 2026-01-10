# 🔗 How to Connect PostgreSQL to Your Web Service

## Current Situation
Your PostgreSQL service has `DATABASE_URL`, but your **web service** can't see it yet.

## ✅ Solution: Add Variable Reference

You have **2 options**:

### Option 1: Variable Reference (Recommended - Stays in Sync)

1. Go to Railway Dashboard
2. Click on your **"web"** service (not PostgreSQL)
3. Click **"Variables"** tab
4. Click **"+ New Variable"** button
5. In the **Variable Name** field, type: `DATABASE_URL`
6. Click the **"Reference"** button (or look for "Reference from another service")
7. Select **PostgreSQL** service
8. Select **`DATABASE_URL`** from the dropdown
9. Click **"Add"**

This creates a reference that automatically stays in sync!

### Option 2: Copy the Value Directly

1. Go to Railway Dashboard
2. Click on **PostgreSQL** service
3. Click **"Variables"** tab
4. Find **`DATABASE_URL`** and click the **eye icon** to reveal it
5. **Copy the entire value** (starts with `postgresql://...`)
6. Go to **"web"** service
7. Click **"Variables"** tab
8. Click **"+ New Variable"**
9. **Name:** `DATABASE_URL`
10. **Value:** Paste the PostgreSQL URL
11. Click **"Add"**

## ✅ Verify It Worked

After adding the variable:

1. Wait 2-3 minutes for Railway to redeploy
2. Check the health endpoint: https://web-production-fb8c.up.railway.app/health
3. Or look at the **database status indicator** in the app header
4. Should show: `✅ PostgreSQL` (green)

## 🎯 Quick Test

Run this command to check:
```bash
python backend/test_database_status.py
```

Should show:
```
✅ SUCCESS: Using PostgreSQL - Data will persist!
```

---

**Note:** The Variable Reference method (Option 1) is better because if the PostgreSQL URL changes, your web service automatically gets the update!

