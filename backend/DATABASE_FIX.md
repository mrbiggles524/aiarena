# Database Relationship Fix

## Issue
The 500 error was caused by an ambiguous foreign key relationship between `Bounty` and `Arena` models.

## Problem
- `Bounty.arena_id` -> `Arena.id` (many-to-one)
- `Arena.bounty_id` -> `Bounty.id` (one-to-one, unique)
- SQLAlchemy couldn't determine which foreign key to use for the relationship

## Fix Applied
1. Added `foreign_keys` parameter to explicitly specify which foreign key to use
2. Added `uselist=False` to make it a one-to-one relationship
3. Recreated database tables with correct relationships

## Status
✅ Database relationships fixed
✅ Tables recreated
✅ Registration should work now

## Next Steps
1. The server should auto-reload
2. Try registering again at http://localhost:8000/docs
3. Registration should now succeed!

---

**The database is fixed. Try registering again!**

