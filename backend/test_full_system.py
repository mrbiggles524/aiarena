"""
Test the full system after deployment
"""

import requests
import json

RAILWAY_URL = "https://web-production-fb8c.up.railway.app"
API_BASE = f"{RAILWAY_URL}/api"

print("=" * 60)
print("Full System Test After Deployment")
print("=" * 60)
print()

# Test 1: Health check
print("[TEST 1] Server Health...")
try:
    response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
    if response.status_code == 200:
        health = response.json()
        print(f"[PASS] Server is healthy")
        print(f"   Status: {health.get('status')}")
        print(f"   Database: {health.get('database')}")
        print(f"   Sandbox: {health.get('sandbox')}")
    else:
        print(f"[FAIL] Health check failed: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Cannot connect: {e}")
    exit(1)

print()

# Test 2: Try to login
print("[TEST 2] Login Test...")
EMAIL = "manhattanbreaks@gmail.com"
PASSWORD = "PASSWORD1"

try:
    login_response = requests.post(
        f"{API_BASE}/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=10
    )
    
    if login_response.status_code == 200:
        data = login_response.json()
        token = data['access_token']
        user = data['user']
        print(f"[PASS] Login successful")
        print(f"   User: {user['username']} (ID: {user['id']})")
        print(f"   Roles: {user['roles']}")
    else:
        error = login_response.json().get('detail', 'Unknown')
        print(f"[FAIL] Login failed: {error}")
        print(f"   Status: {login_response.status_code}")
        
        # Try to register
        print()
        print("[INFO] Attempting to register...")
        register_response = requests.post(
            f"{API_BASE}/auth/register",
            json={
                "email": EMAIL,
                "username": "manhattanbreaks",
                "password": PASSWORD,
                "roles": ["spectator", "bounty_poster"]
            },
            timeout=10
        )
        
        if register_response.status_code == 201:
            data = register_response.json()
            token = data['access_token']
            user = data['user']
            print(f"[PASS] Registration successful")
            print(f"   User: {user['username']} (ID: {user['id']})")
        else:
            error = register_response.json().get('detail', 'Unknown')
            print(f"[FAIL] Registration failed: {error}")
            token = None
except Exception as e:
    print(f"[ERROR] Login/Register failed: {e}")
    token = None

print()

# Test 3: List bounties
print("[TEST 3] List Bounties...")
try:
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = {}
    
    response = requests.get(f"{API_BASE}/bounties/", headers=headers, timeout=10)
    
    if response.status_code == 200:
        bounties = response.json()
        print(f"[PASS] Found {len(bounties)} bounties")
        if len(bounties) > 0:
            print("   Bounties:")
            for bounty in bounties[:3]:  # Show first 3
                print(f"   - {bounty.get('title', 'N/A')} (ID: {bounty.get('id')}, Status: {bounty.get('status')})")
        else:
            print("   [INFO] No bounties found - database might be empty")
    else:
        error = response.json().get('detail', 'Unknown')
        print(f"[FAIL] Failed to list bounties: {error}")
        print(f"   Status: {response.status_code}")
except Exception as e:
    print(f"[ERROR] List bounties failed: {e}")

print()

# Test 4: Create a test bounty (if logged in)
if token:
    print("[TEST 4] Create Test Bounty...")
    try:
        bounty_data = {
            "title": "Test Bounty After Deployment",
            "description": "Testing if bounty creation still works after deployment",
            "bounty_type": "social_media",
            "budget": 50.0,
            "success_criteria": {
                "metric": "test",
                "target": 1
            }
        }
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE}/bounties/", json=bounty_data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            bounty = response.json()
            print(f"[PASS] Bounty created successfully")
            print(f"   ID: {bounty.get('id')}")
            print(f"   Title: {bounty.get('title')}")
        else:
            error = response.json().get('detail', 'Unknown')
            print(f"[FAIL] Bounty creation failed: {error}")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Create bounty failed: {e}")

print()
print("=" * 60)
print("Test Complete")
print("=" * 60)

