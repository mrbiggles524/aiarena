"""
Test bounty creation with the newly registered account
"""

import requests
import json

RAILWAY_URL = "https://web-production-fb8c.up.railway.app"
API_BASE = f"{RAILWAY_URL}/api"

EMAIL = "manhattanbreaks@gmail.com"
PASSWORD = "PASSWORD1"

print("=" * 60)
print("Testing Bounty Creation with New Account")
print("=" * 60)
print()

# Step 1: Login
print("[STEP 1] Logging in...")
try:
    login_response = requests.post(
        f"{API_BASE}/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=10
    )
    
    if login_response.status_code != 200:
        print(f"[FAIL] Login failed: {login_response.status_code}")
        print(f"   Error: {login_response.json().get('detail', 'Unknown')}")
        exit(1)
    
    login_data = login_response.json()
    token = login_data['access_token']
    user = login_data['user']
    
    print("[SUCCESS] Login successful!")
    print(f"   User: {user['username']} (ID: {user['id']})")
    print(f"   Roles: {user['roles']}")
    print()
except Exception as e:
    print(f"[ERROR] Login failed: {e}")
    exit(1)

# Step 2: Create bounty
print("[STEP 2] Creating test bounty...")
bounty_data = {
    "title": "Test: Advertising bot for social media automation",
    "description": "Socials like Youtube, Instagram, TikTok etc post comments, create posts, create videos etc automatically for my business. Bot must be able to take a input for my business and do these things automatically. Posting once per day.",
    "bounty_type": "social_media",
    "budget": 100.0,
    "success_criteria": {
        "metric": "posts_created",
        "target": 30,
        "unit": "posts",
        "timeframe": "month"
    },
    "requirements": {
        "target_industry": "Technology",
        "company_size": "50-500",
        "required_platforms": ["youtube", "instagram", "tiktok"],
        "min_agent_reputation": 50
    },
    "tags": "social media, automation, advertising"
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        f"{API_BASE}/bounties/",
        json=bounty_data,
        headers=headers,
        timeout=10
    )
    
    print(f"[RESPONSE] Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("[SUCCESS] Bounty created successfully!")
        print(f"   Bounty ID: {data['id']}")
        print(f"   Title: {data['title']}")
        print(f"   Budget: ${data['budget']}")
        print(f"   Status: {data['status']}")
        print(f"   Platform Fee: ${data['platform_fee']}")
        print(f"   Agent Reward: ${data['agent_reward']}")
        print()
        print("=" * 60)
        print("[PASS] Test PASSED - Bounty creation works!")
        print("=" * 60)
    else:
        error_data = response.json()
        error_msg = error_data.get('detail', 'Unknown error')
        print(f"[FAIL] Bounty creation failed!")
        print(f"   Error: {error_msg}")
        print()
        
        if "bounty poster role" in error_msg.lower():
            print("[WARNING] Still getting role check error!")
            print("   Railway may not have deployed the new code yet.")
            print("   Check Railway dashboard for deployment status.")
        else:
            print(f"[INFO] Different error: {error_msg}")
        
        print("=" * 60)
        print("[FAIL] Test FAILED")
        print("=" * 60)
        
except Exception as e:
    print(f"[ERROR] Request failed: {e}")
    import traceback
    traceback.print_exc()

