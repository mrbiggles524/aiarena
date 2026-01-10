"""
Test script to create a bounty via API
Run this to test if bounty creation works without role restrictions
"""

import requests
import json
import sys

# Configuration
API_BASE_URL = "http://localhost:8000/api"
TEST_EMAIL = "manhattanbreaks@gmail.com"
TEST_PASSWORD = ""  # Add your password here or pass as argument

def login(email, password):
    """Login and get auth token"""
    print(f"[LOGIN] Logging in as {email}...")
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    
    if response.status_code != 200:
        print(f"[ERROR] Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    data = response.json()
    token = data.get("access_token")
    user = data.get("user", {})
    
    print(f"[SUCCESS] Login successful!")
    print(f"   User: {user.get('username')} (ID: {user.get('id')})")
    print(f"   Roles: {user.get('roles')}")
    print(f"   Token: {token[:20]}...")
    print()
    
    return token

def create_bounty(token):
    """Create a test bounty"""
    print("[CREATE] Creating test bounty...")
    
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
    
    print(f"[SEND] Sending POST request to {API_BASE_URL}/bounties/")
    print(f"   Data: {json.dumps(bounty_data, indent=2)}")
    print()
    
    response = requests.post(
        f"{API_BASE_URL}/bounties/",
        json=bounty_data,
        headers=headers
    )
    
    print(f"[RESPONSE] Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("[SUCCESS] Bounty created successfully!")
        print(f"   Bounty ID: {data.get('id')}")
        print(f"   Title: {data.get('title')}")
        print(f"   Budget: ${data.get('budget')}")
        print(f"   Status: {data.get('status')}")
        print(f"   Platform Fee: ${data.get('platform_fee')}")
        print(f"   Agent Reward: ${data.get('agent_reward')}")
        return True
    else:
        print(f"[ERROR] Bounty creation failed!")
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('detail', 'Unknown error')}")
        except:
            print(f"   Response: {response.text}")
        return False

def main():
    """Main test function"""
    import sys
    import io
    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("Bounty Creation Test")
    print("=" * 60)
    print()
    
    # Get password from command line or use default
    password = sys.argv[1] if len(sys.argv) > 1 else TEST_PASSWORD
    
    if not password:
        print("[ERROR] Password required!")
        print("   Usage: python test_post_bounty.py <password>")
        print("   Or set TEST_PASSWORD in the script")
        return False
    
    # Step 1: Login
    token = login(TEST_EMAIL, password)
    if not token:
        return False
    
    # Step 2: Create bounty
    success = create_bounty(token)
    
    print()
    print("=" * 60)
    if success:
        print("[PASS] Test PASSED - Bounty creation works!")
    else:
        print("[FAIL] Test FAILED - Check the error above")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

