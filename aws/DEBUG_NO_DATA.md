# Debug: Why Zoom Data Not in MongoDB

## ✅ Good News:
The storage code works! Test confirmed data can be stored.

## 🔍 Possible Issues:

### Issue 1: Events Not Reaching Backend

**Check:**
1. **Backend logs** - Look at terminal running `python main.py`
   - You should see: `📥 Received Zoom event: meeting.started`
   - If you don't see this, events aren't reaching backend

2. **Lambda logs** - AWS Lambda → Monitor → CloudWatch logs
   - Check if Lambda is receiving events
   - Check if Lambda is forwarding to backend
   - Look for errors

3. **ngrok logs** - http://localhost:4040
   - Check if requests are coming through ngrok
   - See request/response details

### Issue 2: Wrong Event Structure

Zoom might be sending events in a different format than expected.

**Check backend logs for:**
```
📥 Received Zoom event: [event_type]
   Event data: [full event structure]
```

Compare with expected structure in `zoom_webhook_service.py`

### Issue 3: Lambda Not Forwarding Correctly

**Check Lambda code:**
- Is it using the correct backend URL?
- Is it forwarding headers correctly?
- Check Lambda environment variable: `BACKEND_API_URL`

### Issue 4: Zoom Not Sending Events

**Check Zoom configuration:**
1. Go to Zoom Marketplace → Your App → Event Subscriptions
2. Verify webhook is **Active** (not paused)
3. Check event types are selected
4. Verify endpoint URL is correct (API Gateway URL)

## 🔧 Diagnostic Steps:

### Step 1: Check Backend is Receiving Events

Look at your backend terminal. You should see:
```
📥 Received Zoom event: meeting.started
   Event data: {...}
```

**If you don't see this:**
- Events aren't reaching backend
- Check Lambda → CloudWatch logs
- Check ngrok is running

### Step 2: Test Directly

Send a test event directly to backend:
```powershell
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

Check backend terminal for logs and MongoDB for data.

### Step 3: Check Lambda Logs

1. Go to AWS Lambda → `zoom_webhook` function
2. Click "Monitor" tab
3. Click "View CloudWatch logs"
4. Look for:
   - Incoming requests
   - Errors
   - Responses

### Step 4: Check ngrok

1. Open: http://localhost:4040
2. See incoming requests
3. Check if requests are reaching ngrok
4. Check response status codes

### Step 5: Verify Zoom Configuration

1. Zoom Marketplace → Your App
2. Event Subscriptions
3. Verify:
   - Status: **Active**
   - Endpoint URL: Your API Gateway URL
   - Events selected: `meeting.started`, etc.

## 🎯 Quick Fixes:

### If events not reaching backend:

1. **Check Lambda environment variable:**
   - `BACKEND_API_URL` = your ngrok URL
   - Make sure ngrok is running

2. **Check Lambda code:**
   - Is it forwarding requests correctly?
   - Check for errors in CloudWatch logs

3. **Test Lambda directly:**
   - Use Lambda test function
   - See if it can reach backend

### If events reaching but not storing:

1. **Check backend logs:**
   - Look for error messages
   - Check database connection

2. **Run diagnostic:**
   ```powershell
   cd backend
   python test_zoom_storage.py
   ```

## 📋 Checklist:

- [ ] Backend running (`python main.py`)
- [ ] ngrok running (`ngrok http 3001`)
- [ ] Lambda environment variable set (BACKEND_API_URL)
- [ ] Lambda function deployed
- [ ] Zoom webhook active in Zoom Marketplace
- [ ] Events selected in Zoom
- [ ] Check backend terminal logs
- [ ] Check Lambda CloudWatch logs
- [ ] Check ngrok web interface (localhost:4040)

## 💡 Most Common Issue:

**Events not reaching backend because:**
- Lambda environment variable wrong (not using ngrok URL)
- ngrok not running
- Lambda not forwarding correctly

**Solution:** Check Lambda logs and verify environment variable!

