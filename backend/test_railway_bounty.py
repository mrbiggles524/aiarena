"""
Test Railway production endpoint to verify bounty creation works
"""

import requests
import json

RAILWAY_URL = "https://web-production-fb8c.up.railway.app"
API_BASE = f"{RAILWAY_URL}/api"

print("=" * 60)
print("Testing Railway Production Bounty Endpoint")
print("=" * 60)
print()

# Test 1: Health check
print("[TEST 1] Checking Railway server health...")
try:
    response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
    if response.status_code == 200:
        print(f"[PASS] Server is running")
        print(f"   Response: {response.json()}")
    else:
        print(f"[FAIL] Server returned status {response.status_code}")
except Exception as e:
    print(f"[FAIL] Cannot connect to Railway: {e}")
    exit(1)

print()

# Test 2: Check if endpoint exists (without auth - should get 401/403)
print("[TEST 2] Testing bounty endpoint structure...")
try:
    test_bounty = {
        "title": "Test Bounty",
        "description": "Test",
        "bounty_type": "social_media",
        "budget": 100.0,
        "success_criteria": {"metric": "posts", "target": 10}
    }
    response = requests.post(f"{API_BASE}/bounties/", json=test_bounty, timeout=10)
    print(f"   Status: {response.status_code}")
    
    if response.status_code in [401, 403]:
        print("[PASS] Endpoint requires authentication (expected)")
        try:
            error_data = response.json()
            error_msg = error_data.get('detail', '')
            print(f"   Error message: {error_msg}")
            
            # Check if it's the old role error
            if "bounty poster role" in error_msg.lower():
                print("[WARNING] Still getting role check error!")
                print("   This means Railway hasn't deployed the new code yet.")
                print("   Check Railway dashboard for deployment status.")
            else:
                print("[INFO] Different error (expected - need auth)")
        except:
            print(f"   Response: {response.text[:200]}")
    else:
        print(f"[INFO] Unexpected status: {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"[ERROR] Request failed: {e}")

print()
print("=" * 60)
print("Next Steps:")
print("1. Check Railway dashboard for deployment status")
print("2. If deployment is complete, wait 1-2 minutes for restart")
print("3. Try creating bounty in frontend with hard refresh (Ctrl+F5)")
print("=" * 60)

