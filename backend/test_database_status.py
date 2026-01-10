"""
Test script to check database status and verify PostgreSQL connection
"""
import sys
import requests
import json

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://web-production-fb8c.up.railway.app"

def test_database_status():
    """Test the database status endpoint"""
    print("=" * 60)
    print("🔍 Testing Database Status")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        response.raise_for_status()
        health = response.json()
        
        print(f"\n✅ Health Check: {health.get('status', 'unknown')}")
        print(f"📊 Database Type: {health.get('database_type', 'unknown')}")
        print(f"🔌 Database Connected: {health.get('database_connected', False)}")
        print(f"📋 Bounty Count: {health.get('bounty_count', 0)}")
        print(f"👥 User Count: {health.get('user_count', 0)}")
        
        if health.get('warning'):
            print(f"\n⚠️  WARNING: {health.get('warning')}")
        
        # Check if PostgreSQL
        if health.get('database_type') == 'PostgreSQL':
            print("\n" + "=" * 60)
            print("✅ SUCCESS: Using PostgreSQL - Data will persist!")
            print("=" * 60)
            return True
        elif health.get('database_type') == 'SQLite':
            print("\n" + "=" * 60)
            print("❌ PROBLEM: Using SQLite - Data will be lost on deployment!")
            print("=" * 60)
            print("\n🔧 SOLUTION:")
            print("1. Go to Railway Dashboard → Postgres service")
            print("2. Copy DATABASE_URL from Variables tab")
            print("3. Go to 'web' service → Variables tab")
            print("4. Add DATABASE_URL variable with PostgreSQL URL")
            print("5. Wait for redeploy (2-3 minutes)")
            print("=" * 60)
            return False
        else:
            print("\n⚠️  Unknown database type")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error connecting to server: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_status()
    sys.exit(0 if success else 1)

