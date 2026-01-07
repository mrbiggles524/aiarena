# 🔐 How to Use Authentication

## ✅ You're Registered!

Your token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc2NzcyNTI0OH0.puWZ0FDbkabDoJn4Hd5VozV-Fot1EdeFMoC3PrEaA54
```

## Method 1: Using Swagger UI "Authorize" Button (Easiest)

### Step 1: Click "Authorize"
1. At the **top right** of the Swagger page
2. Look for the **🔒 "Authorize"** button
3. Click it

### Step 2: Enter Your Token
1. In the popup, you'll see a field labeled **"Value"**
2. Paste your token **EXACTLY** (no extra spaces):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc2NzcyNTI0OH0.puWZ0FDbkabDoJn4Hd5VozV-Fot1EdeFMoC3PrEaA54
   ```
3. **IMPORTANT**: Do NOT add "Bearer" - Swagger adds it automatically
4. Click **"Authorize"**
5. Click **"Close"**

### Step 3: Test It
1. Find **GET /api/auth/me**
2. Click **"Try it out"** → **"Execute"**
3. You should see your user info!

## Method 2: Manual Authorization Header

If the "Authorize" button doesn't work:

1. For any endpoint, click **"Try it out"**
2. Look for **"Authorization"** section
3. Enter: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTc2NzcyNTI0OH0.puWZ0FDbkabDoJn4Hd5VozV-Fot1EdeFMoC3PrEaA54`
4. **Important**: Only ONE space between "Bearer" and the token!

## Common Mistakes

❌ **Wrong**: `Bearer    eyJhbGci...` (multiple spaces)
✅ **Correct**: `Bearer eyJhbGci...` (one space)

❌ **Wrong**: `eyJhbGci...` (missing "Bearer")
✅ **Correct**: `Bearer eyJhbGci...` (with "Bearer")

❌ **Wrong**: Copying with extra spaces or line breaks
✅ **Correct**: Copy token exactly as shown

## Token Expiration

- Your token expires in **30 minutes**
- After expiration, use **POST /api/auth/login** to get a new one
- Or register again to get a fresh token

## Quick Test

1. **Authorize** with your token (Method 1 above)
2. Try **GET /api/auth/me**
3. Should return your user info!

---

**Use the "Authorize" button - it's the easiest way! 🔒**

