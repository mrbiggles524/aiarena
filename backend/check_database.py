"""
Quick script to check database configuration
Run this to verify your database setup
"""

import os
from app.config import settings

print("=" * 60)
print("Database Configuration Check")
print("=" * 60)
print()

print(f"Environment: {settings.ENVIRONMENT}")
print(f"Railway Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'Not set')}")
print()

database_url = settings.DATABASE_URL

if database_url.startswith("sqlite"):
    print("[WARNING] Using SQLite database!")
    print("   - SQLite files are NOT persistent on Railway")
    print("   - Data will be lost on each deployment")
    print("   - You need to add PostgreSQL database in Railway")
    print()
    print("   Solution:")
    print("   1. Go to Railway Dashboard")
    print("   2. Click 'New' → 'Database' → 'Add PostgreSQL'")
    print("   3. Railway will auto-set DATABASE_URL")
    print()
elif database_url.startswith("postgresql"):
    print("[SUCCESS] GOOD: Using PostgreSQL database!")
    print("   - PostgreSQL is persistent on Railway")
    print("   - Data will survive deployments")
    print(f"   - Connection: {database_url[:50]}...")
    print()
else:
    print(f"❓ Unknown database type: {database_url[:30]}...")
    print()

print("=" * 60)

