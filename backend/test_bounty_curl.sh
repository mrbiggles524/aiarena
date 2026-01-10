#!/bin/bash
# Test script to create a bounty using curl
# Usage: ./test_bounty_curl.sh <email> <password>

EMAIL=${1:-"manhattanbreaks@gmail.com"}
PASSWORD=${2}

if [ -z "$PASSWORD" ]; then
    echo "Usage: ./test_bounty_curl.sh <email> <password>"
    exit 1
fi

API_BASE="http://localhost:8000/api"

echo "=========================================="
echo "🧪 Bounty Creation Test (curl)"
echo "=========================================="
echo ""

# Step 1: Login
echo "🔐 Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed!"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi

echo "✅ Login successful!"
echo ""

# Step 2: Create bounty
echo "📋 Creating test bounty..."
BOUNTY_DATA='{
    "title": "Test: Advertising bot for social media automation",
    "description": "Socials like Youtube, Instagram, TikTok etc post comments, create posts, create videos etc automatically for my business.",
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
        "required_platforms": ["youtube", "instagram", "tiktok"]
    },
    "tags": "social media, automation"
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/bounties/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$BOUNTY_DATA")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "Response Status: $HTTP_CODE"
echo "Response Body: $BODY"
echo ""

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Test PASSED - Bounty created successfully!"
    exit 0
else
    echo "❌ Test FAILED - Check error above"
    exit 1
fi

