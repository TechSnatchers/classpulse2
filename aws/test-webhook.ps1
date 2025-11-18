# Quick test script for Zoom webhook

Write-Host "🧪 Testing Zoom Webhook Integration" -ForegroundColor Cyan
Write-Host ""

# Test 1: Backend health
Write-Host "1️⃣ Testing backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/health" -Method GET
    Write-Host "   ✅ Backend is running" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Backend not running!" -ForegroundColor Red
    Write-Host "   💡 Start it: cd ..\backend; python main.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Test 2: Webhook health
Write-Host "2️⃣ Testing webhook endpoint..." -ForegroundColor Yellow
try {
    $webhookHealth = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health" -Method GET
    Write-Host "   ✅ Webhook endpoint is ready" -ForegroundColor Green
    Write-Host "   Message: $($webhookHealth.message)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Webhook endpoint not responding" -ForegroundColor Red
}

Write-Host ""

# Test 3: Sample meeting.started event
Write-Host "3️⃣ Testing with sample event..." -ForegroundColor Yellow

$eventTimestamp = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds

$testEvent = @{
    event = "meeting.started"
    event_ts = $eventTimestamp
    payload = @{
        account_id = "test_account_123"
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
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
    if ($response.message) {
        Write-Host "   Message: $($response.message)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Event processing: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Test 4: URL validation event (Zoom sends this first)
Write-Host "4️⃣ Testing URL validation event..." -ForegroundColor Yellow

$validationEvent = @{
    event = "endpoint.url_validation"
    event_ts = $eventTimestamp
    payload = @{
        plainToken = "test_token_12345"
    }
} | ConvertTo-Json -Depth 10

try {
    $validationResponse = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $validationEvent -ContentType "application/json"
    Write-Host "   ✅ Validation response received!" -ForegroundColor Green
    Write-Host "   Plain Token: $($validationResponse.plainToken)" -ForegroundColor Gray
    if ($validationResponse.encryptedToken) {
        Write-Host "   Encrypted Token: $($validationResponse.encryptedToken)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Validation test (OK if secret token not set)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Local testing complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next: Test Lambda and API Gateway" -ForegroundColor Cyan
Write-Host "   1. Test Lambda function in AWS Console" -ForegroundColor White
Write-Host "   2. Test API Gateway URL with curl/PowerShell" -ForegroundColor White
Write-Host "   3. Configure Zoom and test with real meeting" -ForegroundColor White
Write-Host ""

