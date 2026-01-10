"""
Simple test to verify bounty endpoint works
Tests the endpoint structure without requiring login
"""

import requests
import json

API_BASE = "http://localhost:8000/api"

print("=" * 60)
print("Testing Bounty Endpoint Structure")
print("=" * 60)
print()

# Test 1: Check if server is running
print("[TEST 1] Checking if server is running...")
try:
    response = requests.get(f"{API_BASE.replace('/api', '')}/health", timeout=5)
    if response.status_code == 200:
        print("[PASS] Server is running")
        print(f"   Response: {response.json()}")
    else:
        print(f"[FAIL] Server returned status {response.status_code}")
except Exception as e:
    print(f"[FAIL] Cannot connect to server: {e}")
    print("   Make sure the server is running on http://localhost:8000")
    exit(1)

print()

# Test 2: Try to access bounty endpoint without auth (should fail with 401/403)
print("[TEST 2] Testing bounty endpoint without authentication...")
try:
    test_bounty = {
        "title": "Test Bounty",
        "description": "Test",
        "bounty_type": "social_media",
        "budget": 100.0,
        "success_criteria": {"metric": "posts", "target": 10}
    }
    response = requests.post(f"{API_BASE}/bounties/", json=test_bounty, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("[PASS] Endpoint requires authentication (expected)")
    elif response.status_code == 403:
        print("[PASS] Endpoint requires authentication (expected)")
    else:
        print(f"[INFO] Unexpected status: {response.status_code}")
        try:
            print(f"   Response: {response.json()}")
        except:
            print(f"   Response: {response.text}")
except Exception as e:
    print(f"[ERROR] Request failed: {e}")

print()
print("=" * 60)
print("To test with authentication:")
print("1. Get your auth token from browser (localStorage.getItem('auth_token'))")
print("2. Or run: python test_post_bounty.py <password>")
print("3. Or use the frontend to create a bounty")
print("=" * 60)

