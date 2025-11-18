# Copy This Code to Lambda (No Layer Needed!)

This version uses Python's built-in `urllib` - **no external dependencies required!**

## Copy and Paste This Code:

```python
import json
import os
import urllib.request
import urllib.error

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001")
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL}/api/zoom/webhook"

def lambda_handler(event, context):
    try:
        headers = event.get("headers", {}) or {}
        body = event.get("body", "{}")
        
        if isinstance(body, str):
            try:
                body_data = json.loads(body)
            except json.JSONDecodeError:
                body_data = {}
        else:
            body_data = body
        
        data = json.dumps(body_data).encode('utf-8')
        
        req = urllib.request.Request(
            WEBHOOK_ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-zoom-signature": headers.get("x-zoom-signature", ""),
                "x-zoom-request-timestamp": headers.get("x-zoom-request-timestamp", "")
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode('utf-8')
            try:
                response_json = json.loads(response_data) if response_data else {"status": "received"}
            except json.JSONDecodeError:
                response_json = {"status": "received"}
            
            return {
                "statusCode": response.getcode(),
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response_json)
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        return {
            "statusCode": e.code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Failed to forward webhook", "message": error_body})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "message": str(e)})
        }
```

## Steps:

1. **Cancel the "Add layer" dialog** (you don't need it!)
2. **Go back to your Lambda function code**
3. **Replace the code** with the code above
4. **Click "Deploy"**
5. **Done!** No layer needed - uses Python's built-in libraries only

This will work immediately without any additional setup!

