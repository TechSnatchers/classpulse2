# Why You're Not Seeing Zoom Event Logs

## The Problem:
You're not seeing these logs in your backend terminal:
```
📥 Received Zoom event: meeting.started
✅ Meeting stored: [meeting_id]
```

## Possible Reasons:

### 1. Events Not Reaching Backend ⚠️ (Most Likely)

**Check:**
- Is backend running? (`python main.py`)
- Is ngrok running? (`ngrok http 3001`)
- Is Lambda environment variable correct? (BACKEND_API_URL = ngrok URL)
- Are events actually being sent from Zoom?

**How to verify:**
1. Check backend terminal - you should see: `🔔 WEBHOOK REQUEST RECEIVED`
2. Check ngrok web interface: http://localhost:4040
3. Check Lambda CloudWatch logs

### 2. Lambda Not Forwarding to Backend

**Check Lambda:**
- Lambda → Monitor → CloudWatch logs
- Look for errors forwarding to backend
- Verify environment variable: `BACKEND_API_URL`

### 3. Zoom Not Sending Events

**Check Zoom:**
- Zoom Marketplace → Your App → Event Subscriptions
- Is webhook **Active**?
- Are events selected?
- Is endpoint URL correct? (API Gateway URL)

### 4. Wrong Event Structure

Zoom might be sending events in different format.

**Check backend logs for:**
```
📄 Body content: {...}
```

Compare with expected structure.

## 🔍 Diagnostic Steps:

### Step 1: Test Backend Directly

```powershell
$event = @{
    event = "meeting.started"
    event_ts = 1697461200000
    payload = @{
        object = @{
            id = "999"
            topic = "Test"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $event -ContentType "application/json"
```

**Check backend terminal** - you should see:
```
🔔 WEBHOOK REQUEST RECEIVED
📥 Received Zoom event: meeting.started
✅ Meeting stored: 999
```

### Step 2: Check Lambda Logs

1. AWS Lambda → `zoom_webhook` function
2. Monitor → View CloudWatch logs
3. Look for:
   - Incoming requests
   - Errors
   - Forwarding attempts

### Step 3: Check ngrok

1. Open: http://localhost:4040
2. See if requests are coming through
3. Check request/response details

### Step 4: Verify Full Chain

1. **Zoom** → Sends event to API Gateway
2. **API Gateway** → Forwards to Lambda
3. **Lambda** → Forwards to ngrok URL
4. **ngrok** → Forwards to localhost:3001
5. **Backend** → Processes and stores

**Check each step!**

## ✅ What You Should See:

When an event arrives, backend terminal shows:
```
============================================================
🔔 WEBHOOK REQUEST RECEIVED
   Time: 2024-11-12T18:30:00
   Headers: x-zoom-signature=True, x-zoom-request-timestamp=True
============================================================
📦 Body received: 245 bytes
🔐 Verifying webhook signature...
✅ Signature verified
📄 Body content: {"event":"meeting.started",...
✅ Event parsed: meeting.started
🔄 Processing event...
📥 Received Zoom event: meeting.started
   Event data: {...}
   → Handling meeting.started
✅ Meeting stored: 123456789 (inserted_id: ...)
✅ Event processed: success
============================================================
```

## 🎯 Most Common Issue:

**Events not reaching backend because:**
- Lambda environment variable wrong (not using ngrok URL)
- ngrok not running
- Backend not running

**Solution:** Check all three are running and configured correctly!

