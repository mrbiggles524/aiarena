# Registration Endpoint Fix

## Issue
The `/api/auth/register` endpoint was returning a 500 error because:
- The `UserRegister` model expected `list[UserRole]` (enum objects)
- The API was receiving `list[str]` (strings like `["spectator"]`)

## Fix Applied
1. Changed `UserRegister.roles` to accept `list[str]` instead of `list[UserRole]`
2. Added conversion logic to handle string roles and convert them to UserRole enums
3. Added error handling for invalid role values

## Test the Registration

Now you can register with:

```json
{
  "email": "bobbystandish1@gmail.com",
  "username": "bobbystandish",
  "password": "yourpassword",
  "full_name": "Bobby Standish",
  "roles": ["spectator"]
}
```

## Valid Roles
- `"spectator"` - Default role
- `"bounty_poster"` - Can post bounties
- `"agent_builder"` - Can create agents
- `"admin"` - Admin access

## Next Steps
1. Try registering again at http://localhost:8000/docs
2. The server should auto-reload with the fix
3. Registration should now work!

---

**The fix is applied. Try registering again!**

