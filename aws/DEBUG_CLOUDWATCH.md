# Debug: No Logs in CloudWatch

## What You're Seeing:
- ✅ Lambda is being invoked (START/END/REPORT in CloudWatch)
- ❌ No logs from Lambda function code
- ❌ No events reaching backend

## The Problem:
Lambda is running but not logging anything, which means:
1. Function code might not be executing
2. Events might not be reaching Lambda
3. Function might be failing silently

## Solutions:

### Step 1: Update Lambda Code with Logging

I've updated the Lambda function code with detailed logging. You need to:

1. **Copy the new code** from `aws/lambda/zoom_webhook_handler.py`
2. **Paste into Lambda** code editor
3. **Deploy** the function
4. **Test again** - you should now see detailed logs

### Step 2: Test Lambda Directly

1. **In Lambda Console:**
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
   - Check CloudWatch logs - you should see detailed output

### Step 3: Check API Gateway

1. **Verify API Gateway is connected:**
   - Lambda → Configuration → Triggers
   - Check API Gateway is listed
   - Check endpoint URL

2. **Test API Gateway directly:**
   - Get API Gateway URL
   - Send test request:
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

### Step 4: Check Environment Variable

1. **Lambda → Configuration → Environment variables**
2. **Verify:**
   - `BACKEND_API_URL` = your ngrok URL (not localhost!)
   - Example: `https://abc123.ngrok-free.app`

### Step 5: Verify Zoom Configuration

1. **Zoom Marketplace → Your App → Event Subscriptions**
2. **Check:**
   - Status: **Active**
   - Endpoint URL: Your API Gateway URL (not ngrok URL!)
   - Events selected

## What You Should See After Update:

In CloudWatch logs, you should see:
```
============================================================
🔔 LAMBDA FUNCTION INVOKED
   Request ID: xxx
   Backend URL: https://abc123.ngrok-free.app
   Webhook Endpoint: https://abc123.ngrok-free.app/api/zoom/webhook
============================================================
📦 Processing event...
   ✅ Body parsed as JSON
   Event type: meeting.started
   📤 Sending 245 bytes to backend...
   🌐 Making request to: https://abc123.ngrok-free.app/api/zoom/webhook
   ✅ Backend responded: 200
   📥 Response: {"status":"success",...
============================================================
✅ SUCCESS - Event forwarded to backend
============================================================
```

## Common Issues:

1. **No logs at all:**
   - Lambda code not deployed
   - Wrong function version
   - Check function code is saved and deployed

2. **Connection errors:**
   - Backend URL wrong (using localhost instead of ngrok)
   - ngrok not running
   - Backend not running

3. **Events not reaching Lambda:**
   - API Gateway not connected
   - Wrong API Gateway URL in Zoom
   - API Gateway not deployed

## Next Steps:

1. ✅ Update Lambda code with new logging
2. ✅ Deploy Lambda function
3. ✅ Test Lambda directly
4. ✅ Check CloudWatch logs
5. ✅ Test API Gateway endpoint
6. ✅ Verify Zoom webhook URL

