"""
Test database connection and configuration
"""

import os
import sys
from app.config import settings
from app.database import engine, Base
from sqlalchemy import inspect, text

print("=" * 60)
print("Database Connection Test")
print("=" * 60)
print()

# Check environment
print("[ENV] Environment Check:")
print(f"   ENVIRONMENT: {settings.ENVIRONMENT}")
print(f"   RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'Not set')}")
print(f"   DATABASE_URL set: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
print()

# Check database URL
database_url = settings.DATABASE_URL
print("[CONFIG] Database Configuration:")
print(f"   DATABASE_URL: {database_url[:50]}..." if len(database_url) > 50 else f"   DATABASE_URL: {database_url}")
print()

if database_url.startswith("sqlite"):
    print("[WARNING] Using SQLite database!")
    print("   - SQLite is NOT persistent on Railway")
    print("   - Data will be lost on each deployment")
    print("   - You MUST use PostgreSQL on Railway")
    print()
    print("   SOLUTION:")
    print("   1. Go to Railway Dashboard")
    print("   2. Add PostgreSQL database service")
    print("   3. Railway will auto-set DATABASE_URL")
    print("   4. Redeploy your app")
    print()
elif database_url.startswith("postgresql"):
    print("[SUCCESS] Using PostgreSQL database!")
    print("   - PostgreSQL is persistent on Railway")
    print("   - Data will survive deployments")
    print()
else:
    print(f"[UNKNOWN] Unknown database type: {database_url[:30]}...")
    print()

# Test connection
print("[TEST] Testing Database Connection...")
try:
    with engine.connect() as conn:
        # Test basic connection
        result = conn.execute(text("SELECT 1"))
        result.fetchone()
        print("[SUCCESS] Database connection works!")
        print()
        
        # Check if tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"[TABLES] Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        print()
        
        # Check if users table has data
        if 'users' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"[USERS] Users in database: {user_count}")
        
        # Check if bounties table has data
        if 'bounties' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM bounties"))
            bounty_count = result.fetchone()[0]
            print(f"[BOUNTIES] Bounties in database: {bounty_count}")
        
        print()
        print("[SUCCESS] Database is working correctly!")
        
except Exception as e:
    print(f"[ERROR] Database connection failed!")
    print(f"   Error: {str(e)}")
    print()
    print("   Possible issues:")
    print("   1. DATABASE_URL not set correctly")
    print("   2. Database service not running")
    print("   3. Connection credentials wrong")
    print("   4. Network/firewall issue")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

