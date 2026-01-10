"""
Test the /auth/me endpoint to see what's happening
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

def test_profile():
    """Test login and then /auth/me endpoint"""
    print("=" * 60)
    print("🔍 Testing Profile Endpoint")
    print("=" * 60)
    
    # Step 1: Login
    print("\n[STEP 1] Logging in...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": EMAIL, "password": PASSWORD},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Error: {login_response.json()}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token')
        print(f"✅ Login successful!")
        print(f"   Token: {token[:50]}...")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Test /auth/me
    print("\n[STEP 2] Testing /auth/me endpoint...")
    try:
        me_response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"Status Code: {me_response.status_code}")
        print(f"Response Headers: {dict(me_response.headers)}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print("✅ /auth/me successful!")
            print(f"\nUser Data:")
            print(json.dumps(user_data, indent=2, default=str))
            return True
        else:
            print(f"❌ /auth/me failed!")
            try:
                error_data = me_response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Raw response: {me_response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ /auth/me error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_profile()
    sys.exit(0 if success else 1)

