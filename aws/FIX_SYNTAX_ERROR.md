# Fix Syntax Error in Lambda

## The Problem:
```
[ERROR] Runtime.UserCodeSyntaxError: Syntax error in module 'lambda_function': invalid syntax (lambda_function.py, line 104)
```

You copied markdown code blocks (with ```) into Lambda, which is invalid Python syntax.

## ✅ Solution: Copy Clean Python Code

### Step 1: Delete All Code in Lambda

1. **Lambda Console → `zoom_webhook` function**
2. **Code tab**
3. **Select ALL code (Ctrl+A)**
4. **Delete it**

### Step 2: Copy Clean Code

**Copy ONLY the Python code from:** `aws/lambda/zoom_webhook_handler_clean.py`

**OR copy this clean code (NO markdown, NO triple backticks):**

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

### Step 3: Paste and Deploy

1. **Paste the clean code** (NO markdown, NO ```)
2. **Click "Deploy"**
3. **Wait for "Successfully updated"**

### Step 4: Test

1. **Test tab → Create test event**
2. **Click "Test"**
3. **Check CloudWatch logs** - should work now!

## ⚠️ Important:

- **NO markdown code blocks** (```)
- **NO triple backticks**
- **ONLY Python code**
- **Copy from the file, not from markdown documentation**

