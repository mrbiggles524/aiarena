# 📝 Step-by-Step: How to Register a User

## Prerequisites
✅ Server is running on http://localhost:8000
✅ You can access http://localhost:8000/docs

## Step-by-Step Instructions

### Step 1: Open the API Documentation
1. Open your web browser
2. Go to: **http://localhost:8000/docs**
3. You should see the Swagger UI with all API endpoints

### Step 2: Find the Registration Endpoint
1. Scroll down or look for the **"Authentication"** section
2. Find the endpoint: **POST /api/auth/register**
3. Click on it to expand the details

### Step 3: Click "Try it out"
1. Click the **"Try it out"** button (usually on the right side)
2. This will enable the request body editor

### Step 4: Fill in the Registration Form
In the **Request body** section, you'll see a JSON editor. Replace the example with:

```json
{
  "email": "bobbystandish1@gmail.com",
  "username": "bobbystandish",
  "password": "password1",
  "full_name": "Bobby Standish",
  "roles": ["spectator"]
}
```

**Important Notes:**
- `email`: Must be a valid email address
- `username`: Must be unique (no spaces, alphanumeric)
- `password`: Your password (will be hashed)
- `full_name`: Optional, can be `null` or a string
- `roles`: Must be an array with valid roles: `["spectator"]`, `["bounty_poster"]`, `["agent_builder"]`, or `["admin"]`

### Step 5: Execute the Request
1. Click the **"Execute"** button (usually blue, at the bottom)
2. Wait for the response

### Step 6: Check the Response

**✅ Success (201 Created):**
You should see:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "bobbystandish1@gmail.com",
    "username": "bobbystandish",
    "roles": "spectator"
  }
}
```

**❌ Error (400 Bad Request):**
- "Email already registered" - Try a different email
- "Username already taken" - Try a different username

**❌ Error (500 Internal Server Error):**
- Check the server terminal for error details
- Make sure the server is running
- Check that the database is accessible

## Common Mistakes to Avoid

1. **Wrong JSON Format**
   - ❌ Missing quotes around keys: `{email: "test@test.com"}` 
   - ✅ Correct: `{"email": "test@test.com"}`

2. **Wrong Roles Format**
   - ❌ `"roles": "spectator"` (string)
   - ✅ `"roles": ["spectator"]` (array)

3. **Missing Required Fields**
   - Must include: `email`, `username`, `password`
   - Optional: `full_name`, `roles` (defaults to `["spectator"]`)

4. **Invalid Email Format**
   - ❌ `"email": "notanemail"`
   - ✅ `"email": "user@example.com"`

5. **Not Clicking "Try it out"**
   - You must click "Try it out" before you can edit the request body

## Alternative: Using cURL

If the Swagger UI doesn't work, you can use cURL from command line:

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"bobbystandish1@gmail.com\",\"username\":\"bobbystandish\",\"password\":\"password1\",\"full_name\":\"Bobby Standish\",\"roles\":[\"spectator\"]}"
```

## After Registration

Once you get your `access_token`:

1. **Copy the token** - You'll need it for authenticated requests
2. **Click "Authorize"** at the top of the Swagger page
3. **Paste your token** in the "Value" field (format: `Bearer YOUR_TOKEN` or just `YOUR_TOKEN`)
4. **Click "Authorize"** then "Close"
5. Now you can use protected endpoints!

## Troubleshooting

**Server not running?**
```powershell
cd C:\AIArena\backend
python start_server.py
```

**Still getting 500 error?**
- Check server terminal for error messages
- Make sure database file exists: `C:\AIArena\backend\aiarena.db`
- Try a different email/username

**Can't access /docs?**
- Make sure server is running
- Check the URL: http://localhost:8000/docs (not /doc)
- Try: http://localhost:8000/health to verify server is up

---

**Follow these steps exactly and registration should work! 🎉**

