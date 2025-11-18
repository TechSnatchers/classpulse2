# Copy This Lambda Code

## The Problem:
You're seeing START/END/REPORT in CloudWatch but NO function logs. This means the code isn't logging or needs to be updated.

## Solution: Update Lambda Code

### Step 1: Copy This Code

Go to Lambda → Code tab and replace ALL code with this:

```python
import json
import os
import urllib.request
import urllib.error

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001")
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL}/api/zoom/webhook"


def lambda_handler(event, context):
    print("=" * 60)
    print("🔔 LAMBDA FUNCTION INVOKED")
    print(f"   Request ID: {context.request_id if context else 'N/A'}")
    print(f"   Backend URL: {BACKEND_API_URL}")
    print(f"   Webhook Endpoint: {WEBHOOK_ENDPOINT}")
    print("=" * 60)
    
    try:
        print("📦 Processing event...")
        headers = event.get("headers", {}) or {}
        body = event.get("body", "{}")
        
        print(f"   Headers present: {bool(headers)}")
        print(f"   Body type: {type(body)}")
        print(f"   Body length: {len(str(body))} bytes")
        
        if isinstance(body, str):
            try:
                body_data = json.loads(body)
                print(f"   ✅ Body parsed as JSON")
            except json.JSONDecodeError as e:
                print(f"   ⚠️  Body is not JSON: {e}")
                body_data = {}
        else:
            body_data = body
            print(f"   ✅ Body is already dict/object")
        
        print(f"   Event type: {body_data.get('event', 'unknown') if isinstance(body_data, dict) else 'N/A'}")
        
        data = json.dumps(body_data).encode('utf-8')
        print(f"   📤 Sending {len(data)} bytes to backend...")
        
        req = urllib.request.Request(
            WEBHOOK_ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-zoom-signature": headers.get("x-zoom-signature", ""),
                "x-zoom-request-timestamp": headers.get("x-zoom-request-timestamp", "")
            }
        )
        
        print(f"   🌐 Making request to: {WEBHOOK_ENDPOINT}")
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = response.read().decode('utf-8')
                print(f"   ✅ Backend responded: {response.getcode()}")
                print(f"   📥 Response: {response_data[:200]}...")
                
                try:
                    response_json = json.loads(response_data) if response_data else {"status": "received"}
                except json.JSONDecodeError:
                    response_json = {"status": "received", "raw": response_data}
                
                print("=" * 60)
                print("✅ SUCCESS - Event forwarded to backend")
                print("=" * 60)
                
                return {
                    "statusCode": response.getcode(),
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(response_json)
                }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            print(f"   ❌ HTTP Error: {e.code} - {error_body}")
            print("=" * 60)
            return {
                "statusCode": e.code,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Failed to forward webhook", "message": error_body, "code": e.code})
            }
        except urllib.error.URLError as e:
            print(f"   ❌ Connection Error: {e}")
            print(f"   💡 Check if backend is accessible at: {BACKEND_API_URL}")
            print("=" * 60)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Connection error", "message": str(e), "backend_url": BACKEND_API_URL})
            }
            
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "message": str(e)})
        }
```

### Step 2: Deploy

1. **Click "Deploy" button**
2. **Wait for "Successfully updated" message**

### Step 3: Test

1. **Click "Test" tab**
2. **Use test event** (see below)
3. **Click "Test"**
4. **Check CloudWatch logs** - you should see detailed output!

## Test Event:

```json
{
  "headers": {
    "x-zoom-signature": "test",
    "x-zoom-request-timestamp": "1234567890"
  },
  "body": "{\"event\":\"meeting.started\",\"event_ts\":1697461200000,\"payload\":{\"object\":{\"id\":\"123\",\"topic\":\"Test Meeting\"}}}"
}
```

## After Update, You Should See:

In CloudWatch logs:
```
============================================================
🔔 LAMBDA FUNCTION INVOKED
   Request ID: xxx
   Backend URL: https://divertive-ricki-goadingly.ngrok-free.dev
============================================================
📦 Processing event...
   ✅ Body parsed as JSON
   Event type: meeting.started
   📤 Sending to backend...
   ✅ Backend responded: 200
============================================================
```

If you still don't see logs, the code might not be deployed or there's an issue with the function execution.

