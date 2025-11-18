# Quick Test Guide

## Test 1: Backend Endpoint (Easiest)

```powershell
# Test health
Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health"

# Test with sample event
$event = @{
    event = "meeting.started"
    event_ts = 1697461200000
    payload = @{
        object = @{
            id = "123456789"
            topic = "Test Meeting"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $event -ContentType "application/json"
```

## Test 2: Lambda Function

1. **In AWS Lambda Console:**
   - Go to `zoom_webhook` function
   - Click **"Test"** tab
   - Create test event:
   ```json
   {
     "headers": {
       "x-zoom-signature": "test",
       "x-zoom-request-timestamp": "1234567890"
     },
     "body": "{\"event\":\"meeting.started\",\"event_ts\":1697461200000,\"payload\":{\"object\":{\"id\":\"123\",\"topic\":\"Test\"}}}"
   }
   ```
   - Click **"Test"**
   - Check response and logs

## Test 3: API Gateway

Get your API Gateway URL from Lambda → Configuration → Triggers, then:

```powershell
$url = "YOUR_API_GATEWAY_URL"
$event = @{
    event = "meeting.started"
    event_ts = 1697461200000
    payload = @{
        object = @{
            id = "123"
            topic = "Test"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri $url -Method POST -Body $event -ContentType "application/json"
```

## Test 4: Real Zoom Meeting

1. Create a Zoom meeting
2. Start it
3. Check:
   - Lambda CloudWatch logs
   - Backend terminal logs
   - MongoDB for stored events

## Check Logs

- **Lambda:** Lambda → Monitor → View CloudWatch logs
- **Backend:** Terminal running `python main.py`
- **ngrok:** http://localhost:4040 (web interface)

