"""
Direct login test to verify credentials
"""
import sys
import requests
import json

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://web-production-fb8c.up.railway.app"
EMAIL = "manhattanbreaks@gmail.com"
PASSWORD = "PASSWORD1"

def test_login():
    """Test login with credentials"""
    print("=" * 60)
    print("🔐 Testing Login")
    print("=" * 60)
    print(f"Email: {EMAIL}")
    print(f"Password: {'*' * len(PASSWORD)}")
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": EMAIL,
                "password": PASSWORD
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"   Token: {data.get('access_token', '')[:50]}...")
            print(f"   User: {data.get('user', {}).get('username', 'unknown')}")
            print(f"   Email: {data.get('user', {}).get('email', 'unknown')}")
            print(f"   Roles: {data.get('user', {}).get('roles', 'unknown')}")
            return True
        else:
            error_data = response.json()
            print(f"❌ LOGIN FAILED")
            print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            print()
            print("💡 Possible solutions:")
            print("   1. Check if email and password are correct")
            print("   2. Account may have been reset - try registering again")
            print("   3. Make sure you're using the exact password (case-sensitive)")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)

