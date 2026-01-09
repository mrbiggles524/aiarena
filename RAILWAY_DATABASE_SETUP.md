# 🔒 Railway Database Setup - Prevent Data Loss

## ⚠️ CRITICAL: Your database is being reset on each deployment!

This happens because Railway isn't using a persistent PostgreSQL database. Follow these steps to fix it:

## Step 1: Add PostgreSQL Database to Railway

1. **Go to Railway Dashboard**: https://railway.app
2. **Open your project** (AI Arena)
3. **Click "New"** button (top right)
4. **Select "Database"**
5. **Choose "Add PostgreSQL"**
6. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Link it to your app service

## Step 2: Verify DATABASE_URL is Set

1. In Railway, go to your **app service** (not the database)
2. Click **"Variables"** tab
3. Look for `DATABASE_URL` - it should be there automatically
4. It should look like: `postgresql://user:password@host:port/dbname`

## Step 3: Verify Database Connection

After adding PostgreSQL, Railway will:
- ✅ Automatically set `DATABASE_URL`
- ✅ Your app will connect to PostgreSQL instead of SQLite
- ✅ Data will persist across deployments

## Step 4: Test the Connection

After deployment, check the logs:
- Look for: `✅ Database tables verified/created (existing data preserved)`
- If you see errors, check that `DATABASE_URL` is set correctly

## Why This Happens

**SQLite (default)**:
- ❌ Creates a file (`aiarena.db`) in the container
- ❌ File is deleted when container restarts/redeploys
- ❌ All data is lost

**PostgreSQL (Railway)**:
- ✅ Persistent database service
- ✅ Data survives deployments
- ✅ Automatic backups
- ✅ Production-ready

## Current Status Check

Run this to check your current database:
```bash
# Check if DATABASE_URL is set
echo $DATABASE_URL

# Should show: postgresql://... (not sqlite://)
```

## After Setup

1. **Redeploy your app** (or wait for auto-deploy)
2. **Register your account again** (one-time)
3. **Create your bounties** - they will now persist! 🎉

## Troubleshooting

**"DATABASE_URL not found"**:
- Make sure PostgreSQL service is added
- Check that services are linked in Railway

**"Connection refused"**:
- Wait 1-2 minutes after adding database
- Check Railway database service is running

**"Still losing data"**:
- Verify `DATABASE_URL` starts with `postgresql://`
- Check Railway logs for database connection errors

---

**Once PostgreSQL is set up, your data will persist forever!** 🚀

