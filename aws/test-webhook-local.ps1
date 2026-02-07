# Test Zoom webhook endpoint locally

Write-Host "🧪 Testing Zoom Webhook Endpoint Locally" -ForegroundColor Cyan
Write-Host ""

$backendUrl = "http://localhost:3001"

# Test 1: Health check
Write-Host "1️⃣ Testing health endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$backendUrl/api/zoom/webhook/health" -Method GET
    Write-Host "   ✅ Health check passed: $($health.message)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Health check failed. Is the backend running?" -ForegroundColor Red
    Write-Host "   💡 Start backend: cd ..\backend; python main.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Test 2: Sample meeting.started event
Write-Host "2️⃣ Testing meeting.started event..." -ForegroundColor Yellow

$eventTimestamp = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds

$eventBody = @{
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
    $response = Invoke-RestMethod -Uri "$backendUrl/api/zoom/webhook" -Method POST -Body $eventBody -ContentType "application/json"
    Write-Host "   ✅ Event processed successfully!" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Event processing failed: $_" -ForegroundColor Red
    Write-Host "   Response: $($_.Exception.Response)" -ForegroundColor Gray
}

Write-Host ""

# Test 3: URL validation event (Zoom sends this first)
Write-Host "3️⃣ Testing URL validation event..." -ForegroundColor Yellow

$validationBody = @{
    event = "endpoint.url_validation"
    event_ts = $eventTimestamp
    payload = @{
        plainToken = "test_token_12345"
    }
} | ConvertTo-Json -Depth 10

try {
    $validationResponse = Invoke-RestMethod -Uri "$backendUrl/api/zoom/webhook" -Method POST -Body $validationBody -ContentType "application/json"
    Write-Host "   ✅ Validation response received!" -ForegroundColor Green
    Write-Host "   Plain Token: $($validationResponse.plainToken)" -ForegroundColor Gray
    if ($validationResponse.encryptedToken) {
        Write-Host "   Encrypted Token: $($validationResponse.encryptedToken)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Validation test failed (this is OK if secret token not set)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Local testing complete!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Install ngrok: https://ngrok.com/download" -ForegroundColor White
Write-Host "   2. Run: ngrok http 3001" -ForegroundColor White
Write-Host "   3. Use the ngrok URL in Zoom webhook configuration" -ForegroundColor White
Write-Host ""

