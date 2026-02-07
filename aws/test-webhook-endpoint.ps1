# Test the complete webhook flow

Write-Host "🧪 Testing Zoom Webhook Integration" -ForegroundColor Cyan
Write-Host ""

# Step 1: Test backend
Write-Host "1️⃣ Testing backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/health" -Method GET
    Write-Host "   ✅ Backend is running" -ForegroundColor Green
    Write-Host "   Response: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Backend not running!" -ForegroundColor Red
    Write-Host "   💡 Start it: cd ..\backend; python main.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Step 2: Test webhook endpoint
Write-Host "2️⃣ Testing webhook endpoint..." -ForegroundColor Yellow
try {
    $webhookHealth = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health" -Method GET
    Write-Host "   ✅ Webhook endpoint is ready" -ForegroundColor Green
    Write-Host "   Response: $($webhookHealth.message)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Webhook endpoint not responding" -ForegroundColor Red
}

Write-Host ""

# Step 3: Test with sample event
Write-Host "3️⃣ Testing with sample Zoom event..." -ForegroundColor Yellow

$eventTimestamp = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds

$testEvent = @{
    event = "meeting.started"
    event_ts = $eventTimestamp
    payload = @{
        account_id = "test_account"
        object = @{
            id = "123456789"
            uuid = "test-uuid-12345"
            topic = "Test Learning Session"
            host_id = "test_host_123"
            start_time = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $testEvent -ContentType "application/json"
    Write-Host "   ✅ Event processed successfully!" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "   ⚠️  Event processing: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Local testing complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Start ngrok: ngrok http 3001" -ForegroundColor White
Write-Host "   2. Set Lambda env var: BACKEND_API_URL = ngrok URL" -ForegroundColor White
Write-Host "   3. Get API Gateway URL from Lambda triggers" -ForegroundColor White
Write-Host "   4. Configure Zoom with API Gateway URL" -ForegroundColor White
Write-Host ""

