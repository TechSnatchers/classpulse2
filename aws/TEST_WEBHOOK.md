# How to Test Zoom Webhook Integration

## Testing Methods

### Method 1: Test Backend Endpoint Directly (Easiest)

Test if your backend webhook endpoint is working:

```powershell
# Test health endpoint
Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health"

# Test with sample event
$testEvent = @{
    event = "meeting.started"
    event_ts = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
    payload = @{
        account_id = "test_account"
        object = @{
            id = "123456789"
            uuid = "test-uuid-12345"
            topic = "Test Learning Session"
            host_id = "test_host_123"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $testEvent -ContentType "application/json"
```

### Method 2: Test Lambda Function

1. **In Lambda Console:**
   - Go to your `zoom_webhook` function
   - Click **"Test"** tab
   - Click **"Create new test event"**
   - Use this test event:

```json
{
  "headers": {
    "x-zoom-signature": "test-signature",
    "x-zoom-request-timestamp": "1234567890"
  },
  "body": "{\"event\":\"meeting.started\",\"event_ts\":1697461200000,\"payload\":{\"account_id\":\"test\",\"object\":{\"id\":\"123456789\",\"topic\":\"Test Meeting\"}}}"
}
```

2. Click **"Test"** button
3. Check the response and logs

### Method 3: Test Full Flow (Zoom → API Gateway → Lambda → Backend)

1. **Get API Gateway URL:**
   - Lambda → Configuration → Triggers → Copy API endpoint

2. **Test with curl or PowerShell:**
```powershell
$apiGatewayUrl = "https://your-api-gateway-url.execute-api.eu-north-1.amazonaws.com/prod/webhook"

$testEvent = @{
    event = "meeting.started"
    event_ts = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
    payload = @{
        account_id = "test_account"
        object = @{
            id = "123456789"
            uuid = "test-uuid"
            topic = "Test Meeting"
            host_id = "test_host"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri $apiGatewayUrl -Method POST -Body $testEvent -ContentType "application/json"
```

### Method 4: Test with Real Zoom Meeting

1. **Create a Zoom meeting:**
   - Start a meeting in Zoom
   - Join as participant
   - End the meeting

2. **Check logs:**
   - **Lambda logs:** Lambda → Monitor → View CloudWatch logs
   - **Backend logs:** Check terminal running `python main.py`
   - **MongoDB:** Check for stored events

### Method 5: Check MongoDB Data

Verify events are stored in MongoDB:

```powershell
# Connect to MongoDB and check collections
# zoom_meetings - meeting events
# zoom_participants - participant join/leave events
# zoom_recordings - recording events
```

## Quick Test Script

Save this as `test-webhook.ps1`:

```powershell
Write-Host "🧪 Testing Zoom Webhook" -ForegroundColor Cyan

# Test 1: Backend health
Write-Host "`n1️⃣ Testing backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health"
    Write-Host "   ✅ Backend OK: $($health.message)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend not running!" -ForegroundColor Red
    exit 1
}

# Test 2: Backend webhook endpoint
Write-Host "`n2️⃣ Testing webhook endpoint..." -ForegroundColor Yellow
$event = @{
    event = "meeting.started"
    event_ts = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
    payload = @{
        object = @{
            id = "test123"
            topic = "Test Meeting"
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $event -ContentType "application/json"
    Write-Host "   ✅ Webhook OK: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Webhook failed: $_" -ForegroundColor Red
}

Write-Host "`n✅ Testing complete!" -ForegroundColor Green
```

## What to Check

### ✅ Success Indicators:

1. **Backend responds:**
   - Health endpoint returns `{"status":"ok"}`
   - Webhook endpoint processes events

2. **Lambda works:**
   - Test event succeeds
   - No errors in CloudWatch logs

3. **Data stored:**
   - Events appear in MongoDB
   - Check `zoom_meetings` collection

4. **Zoom integration:**
   - Zoom sends validation request
   - Real meeting events are received

### ❌ Common Issues:

1. **"Connection refused"**
   - Backend not running
   - ngrok not running
   - Wrong URL in Lambda

2. **"Invalid signature"**
   - Zoom secret token not set
   - Headers not forwarded correctly

3. **"Timeout"**
   - Backend too slow
   - Network issues
   - Increase Lambda timeout

## Debugging Tips

1. **Check all logs:**
   - Lambda CloudWatch logs
   - Backend terminal output
   - ngrok web interface (http://localhost:4040)

2. **Verify URLs:**
   - ngrok URL is correct
   - API Gateway URL is correct
   - Backend is accessible

3. **Test incrementally:**
   - Test backend first
   - Then Lambda
   - Then full flow
   - Finally with Zoom

