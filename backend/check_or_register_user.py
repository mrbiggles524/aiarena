"""
Check if user exists or register them
"""

import requests
import json
import sys

RAILWAY_URL = "https://web-production-fb8c.up.railway.app"
API_BASE = f"{RAILWAY_URL}/api"

EMAIL = "manhattanbreaks@gmail.com"
PASSWORD = "PASSWORD1"
USERNAME = "manhattanbreaks"

def try_login(email, password):
    """Try to login"""
    print(f"[LOGIN] Attempting to login as {email}...")
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] Login successful!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Username: {data['user']['username']}")
            print(f"   Roles: {data['user']['roles']}")
            print(f"   Token: {data['access_token'][:30]}...")
            return data['access_token']
        else:
            error_data = response.json()
            print(f"[FAIL] Login failed: {response.status_code}")
            print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"[ERROR] Login request failed: {e}")
        return None

def try_register(email, username, password):
    """Try to register a new user"""
    print(f"[REGISTER] Attempting to register {email}...")
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
                "full_name": None,
                "roles": ["spectator", "bounty_poster"]  # Give them both roles
            },
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print("[SUCCESS] Registration successful!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Username: {data['user']['username']}")
            print(f"   Roles: {data['user']['roles']}")
            print(f"   Token: {data['access_token'][:30]}...")
            return data['access_token']
        else:
            error_data = response.json()
            print(f"[FAIL] Registration failed: {response.status_code}")
            print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            if "already registered" in error_data.get('detail', '').lower():
                print("   User already exists - password might be wrong")
            return None
    except Exception as e:
        print(f"[ERROR] Registration request failed: {e}")
        return None

def main():
    print("=" * 60)
    print("User Check/Registration Tool")
    print("=" * 60)
    print()
    
    # Try login first
    token = try_login(EMAIL, PASSWORD)
    
    if token:
        print()
        print("[SUCCESS] You can now use this account!")
        print(f"   Save this token for testing: {token[:50]}...")
        return True
    
    print()
    print("[INFO] Login failed, trying to register...")
    print()
    
    # Try to register
    token = try_register(EMAIL, USERNAME, PASSWORD)
    
    if token:
        print()
        print("[SUCCESS] New account created! You can now login.")
        return True
    
    print()
    print("=" * 60)
    print("[FAIL] Could not login or register")
    print("=" * 60)
    print()
    print("Possible issues:")
    print("1. User exists but password is different")
    print("2. Server is not responding")
    print("3. Email format issue")
    print()
    print("Try:")
    print("- Check if you remember a different password")
    print("- Try registering with a different email")
    print("- Check Railway server logs")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

