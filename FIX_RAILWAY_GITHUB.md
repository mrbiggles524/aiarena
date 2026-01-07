# Fix: Railway Can't See Your Repository

## Problem
Railway shows "No repositories found" when trying to deploy from GitHub.

## Solution: Configure GitHub App Permissions

### Step 1: Authorize Railway on GitHub
1. **Go to GitHub Settings:**
   - Open https://github.com/settings/applications
   - Or: GitHub → Your Profile (top right) → Settings → Applications → Installed GitHub Apps

2. **Find Railway:**
   - Look for "Railway" in the list
   - If you see it, click on it
   - If you DON'T see it, continue to Step 2

### Step 2: Install Railway GitHub App
1. **Go back to Railway:**
   - In Railway, when you see "Configure GitHub App", click it
   - OR go to: https://railway.app/account

2. **Authorize Repository Access:**
   - Railway will ask for permissions
   - Make sure to:
     - ✅ Select "All repositories" OR
     - ✅ Select "Only select repositories" and choose `aiarena`
   - Click "Install" or "Authorize"

3. **Grant Permissions:**
   - Railway needs these permissions:
     - ✅ Repository access
     - ✅ Read repository contents
     - ✅ Read and write repository hooks (for auto-deploy)

### Step 3: Refresh Railway
1. **Go back to Railway Dashboard:**
   - Click "New Project" again
   - Click "Deploy from GitHub repo"
   - Your `aiarena` repository should now appear!

### Alternative: Manual Repository Connection

If the above doesn't work, try this:

1. **In Railway:**
   - Click "New Project"
   - Instead of "Deploy from GitHub repo", look for:
     - "Deploy from GitHub" (different option)
     - OR "Connect Repository" button

2. **Enter Repository URL:**
   - Repository: `mrbiggles524/aiarena`
   - OR full URL: `https://github.com/mrbiggles524/aiarena`

3. **Authorize when prompted**

### Step 4: Verify Repository is Public/Private

**Check if repository is visible:**
- Go to: https://github.com/mrbiggles524/aiarena
- If you see it, it's accessible
- If it's private, make sure Railway has access (Step 2)

**To make it public (optional):**
1. Go to: https://github.com/mrbiggles524/aiarena/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → "Make public"
4. Confirm

### Step 5: Try Again
1. Go back to Railway
2. Click "New Project"
3. Click "Deploy from GitHub repo"
4. Search for "aiarena" or scroll to find it
5. Select it and deploy!

---

## Still Not Working?

### Check These:
1. ✅ Are you logged into Railway with the same GitHub account?
2. ✅ Did you authorize Railway in GitHub settings?
3. ✅ Is the repository name exactly `aiarena`?
4. ✅ Try logging out and back into Railway

### Manual Deploy Alternative:
If Railway still can't see it, you can:
1. Download Railway CLI
2. Deploy manually from command line
3. See `DEPLOY_RAILWAY.md` for CLI instructions

---

**Quick Links:**
- GitHub Apps: https://github.com/settings/applications
- Railway Dashboard: https://railway.app/dashboard
- Your Repo: https://github.com/mrbiggles524/aiarena

