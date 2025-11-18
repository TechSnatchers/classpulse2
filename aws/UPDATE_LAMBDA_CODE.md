# Update Lambda Code - Step by Step

## Quick Steps:

### 1. Copy the New Code

The updated Lambda code is in: `aws/lambda/zoom_webhook_handler.py`

### 2. Update in Lambda Console

1. **Go to AWS Lambda Console**
2. **Your `zoom_webhook` function**
3. **Click "Code" tab**
4. **Replace all code** with the new code from the file
5. **Click "Deploy"**

### 3. Verify Environment Variable

1. **Configuration → Environment variables**
2. **Check:**
   - Key: `BACKEND_API_URL`
   - Value: Your ngrok URL (e.g., `https://abc123.ngrok-free.app`)

### 4. Test

1. **Click "Test" tab**
2. **Create test event** (see below)
3. **Click "Test"**
4. **Check CloudWatch logs** - you should see detailed output!

## Test Event for Lambda:

```json
{
  "headers": {
    "x-zoom-signature": "test-signature",
    "x-zoom-request-timestamp": "1234567890"
  },
  "body": "{\"event\":\"meeting.started\",\"event_ts\":1697461200000,\"payload\":{\"object\":{\"id\":\"123\",\"topic\":\"Test Meeting\"}}}"
}
```

## What Changed:

The new code adds:
- ✅ Detailed logging at every step
- ✅ Error handling with logs
- ✅ Connection status logging
- ✅ Request/response logging

Now you'll see exactly what's happening in CloudWatch!

