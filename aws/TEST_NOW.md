# ✅ Environment Variable Set! Now Test It

## What's Set:
- ✅ `BACKEND_API_URL` = `https://divertive-ricki-goadingly.ngrok-free.dev`
- ✅ `ZOOM_VERIFICATION_TOKEN` = `FUILACWxTn2aG5HKwAeRaA`

## Next Steps:

### Step 1: Update Lambda Code (If Not Done)

Make sure Lambda code has the detailed logging. If not:
1. Copy code from `aws/lambda/zoom_webhook_handler.py`
2. Paste into Lambda code editor
3. Click "Deploy"

### Step 2: Test Lambda Directly

1. **Lambda Console → `zoom_webhook` function**
2. **Click "Test" tab**
3. **Create test event:**
   ```json
   {
     "headers": {
       "x-zoom-signature": "test",
       "x-zoom-request-timestamp": "1234567890"
     },
     "body": "{\"event\":\"meeting.started\",\"event_ts\":1697461200000,\"payload\":{\"object\":{\"id\":\"123\",\"topic\":\"Test Meeting\"}}}"
   }
   ```
4. **Click "Test"**
5. **Check CloudWatch logs** - you should see detailed output!

### Step 3: Check CloudWatch Logs

1. **Lambda → Monitor → View CloudWatch logs**
2. **Look for:**
   ```
   🔔 LAMBDA FUNCTION INVOKED
   Backend URL: https://divertive-ricki-goadingly.ngrok-free.dev
   ✅ Backend responded: 200
   ```

### Step 4: Verify Backend is Running

Make sure:
- ✅ Backend running: `python main.py`
- ✅ ngrok running: `ngrok http 3001`
- ✅ ngrok URL matches: `https://divertive-ricki-goadingly.ngrok-free.dev`

### Step 5: Test with Real Zoom Event

1. **Create a Zoom meeting**
2. **Start the meeting**
3. **Check:**
   - Lambda CloudWatch logs
   - Backend terminal logs
   - MongoDB for stored data

## What You Should See:

### In CloudWatch:
```
============================================================
🔔 LAMBDA FUNCTION INVOKED
   Backend URL: https://divertive-ricki-goadingly.ngrok-free.dev
============================================================
📦 Processing event...
   ✅ Body parsed as JSON
   Event type: meeting.started
   📤 Sending to backend...
   ✅ Backend responded: 200
============================================================
```

### In Backend Terminal:
```
============================================================
🔔 WEBHOOK REQUEST RECEIVED
============================================================
📥 Received Zoom event: meeting.started
✅ Meeting stored: [meeting_id]
============================================================
```

## Troubleshooting:

**If you see connection errors:**
- Check ngrok is running
- Verify ngrok URL matches environment variable
- Check backend is running

**If no logs in CloudWatch:**
- Make sure Lambda code is deployed
- Check you're looking at the right log group

**If events not reaching:**
- Verify Zoom webhook is Active
- Check API Gateway URL in Zoom
- Test API Gateway directly

