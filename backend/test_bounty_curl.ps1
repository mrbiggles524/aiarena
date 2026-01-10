# PowerShell script to test bounty creation
# Usage: .\test_bounty_curl.ps1 -Email "manhattanbreaks@gmail.com" -Password "yourpassword"

param(
    [string]$Email = "manhattanbreaks@gmail.com",
    [string]$Password
)

if (-not $Password) {
    Write-Host "Usage: .\test_bounty_curl.ps1 -Email 'your@email.com' -Password 'yourpassword'" -ForegroundColor Red
    exit 1
}

$API_BASE = "http://localhost:8000/api"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🧪 Bounty Creation Test (PowerShell)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Login
Write-Host "🔐 Logging in..." -ForegroundColor Yellow
$loginBody = @{
    email = $Email
    password = $Password
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$API_BASE/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody
    
    $token = $loginResponse.access_token
    $user = $loginResponse.user
    
    Write-Host "✅ Login successful!" -ForegroundColor Green
    Write-Host "   User: $($user.username) (ID: $($user.id))" -ForegroundColor Gray
    Write-Host "   Roles: $($user.roles)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ Login failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    exit 1
}

# Step 2: Create bounty
Write-Host "📋 Creating test bounty..." -ForegroundColor Yellow

$bountyData = @{
    title = "Test: Advertising bot for social media automation"
    description = "Socials like Youtube, Instagram, TikTok etc post comments, create posts, create videos etc automatically for my business. Bot must be able to take a input for my business and do these things automatically. Posting once per day."
    bounty_type = "social_media"
    budget = 100.0
    success_criteria = @{
        metric = "posts_created"
        target = 30
        unit = "posts"
        timeframe = "month"
    }
    requirements = @{
        target_industry = "Technology"
        company_size = "50-500"
        required_platforms = @("youtube", "instagram", "tiktok")
        min_agent_reputation = 50
    }
    tags = "social media, automation, advertising"
} | ConvertTo-Json -Depth 10

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

try {
    Write-Host "📤 Sending POST request to $API_BASE/bounties/" -ForegroundColor Gray
    Write-Host ""
    
    $response = Invoke-RestMethod -Uri "$API_BASE/bounties/" `
        -Method POST `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $bountyData
    
    Write-Host "✅ Bounty created successfully!" -ForegroundColor Green
    Write-Host "   Bounty ID: $($response.id)" -ForegroundColor Gray
    Write-Host "   Title: $($response.title)" -ForegroundColor Gray
    Write-Host "   Budget: `$$($response.budget)" -ForegroundColor Gray
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
    Write-Host "   Platform Fee: `$$($response.platform_fee)" -ForegroundColor Gray
    Write-Host "   Agent Reward: `$$($response.agent_reward)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "✅ Test PASSED - Bounty creation works!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    exit 0
} catch {
    Write-Host "❌ Bounty creation failed!" -ForegroundColor Red
    Write-Host "   Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        $errorObj = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "   Error: $($errorObj.detail)" -ForegroundColor Red
    } else {
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "❌ Test FAILED - Check error above" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Cyan
    exit 1
}

