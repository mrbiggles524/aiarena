# 🔐 Login Troubleshooting Guide

## ✅ Your Account Info
- **Email:** `manhattanbreaks@gmail.com`
- **Password:** `PASSWORD1`
- **Status:** Account exists and is active ✅

## 🐛 Common Login Issues

### Issue 1: "Incorrect email or password"
**Solution:**
- Make sure you're using the exact password: `PASSWORD1` (all caps)
- Check for extra spaces before/after the email or password
- Try copying and pasting the email to avoid typos

### Issue 2: "Network error"
**Solution:**
- Check if the server is running
- Open browser console (F12) and look for errors
- Try refreshing the page
- Check if you can access: https://web-production-fb8c.up.railway.app/health

### Issue 3: Account was reset
**If your account was lost due to database reset:**
1. The account has been automatically recreated
2. Use the credentials above to login
3. If it still doesn't work, try registering again

## 🔍 Debug Steps

1. **Open Browser Console (F12)**
   - Look for any red error messages
   - Check the "Network" tab to see if the login request is being sent

2. **Check API URL**
   - The app should use: `https://web-production-fb8c.up.railway.app/api`
   - Check console for: `API URL: ...`

3. **Test Login Directly**
   Run this command to test:
   ```bash
   python backend/test_login_direct.py
   ```

## ✅ Quick Fix

If login still doesn't work:

1. **Clear browser cache and localStorage:**
   - Open browser console (F12)
   - Go to "Application" tab
   - Clear "Local Storage"
   - Refresh the page

2. **Try registering again:**
   - Click "Sign Up"
   - Use the same email: `manhattanbreaks@gmail.com`
   - Use password: `PASSWORD1`
   - This will either create a new account or tell you the email is already registered

3. **Check Railway logs:**
   - Go to Railway Dashboard
   - Click on "web" service
   - Check "Logs" tab for any errors

## 📞 Still Having Issues?

If login still fails after trying the above:
1. Check the browser console for specific error messages
2. Share the exact error message you see
3. Check if the server is responding at: https://web-production-fb8c.up.railway.app/health

