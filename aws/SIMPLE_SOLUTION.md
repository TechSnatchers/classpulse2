# Simple Solution: Add Requests to Lambda

## Easiest Method: Bundle Requests with Code

Since you're already in the Lambda editor, here's the simplest approach:

### Option 1: Use "Specify an ARN" (Quick)

1. In the "Add layer" page, select **"Specify an ARN"**
2. Use this public layer ARN (for Python 3.11):
   ```
   arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p311-requests:1
   ```
3. Click "Add"

**Note:** If that ARN doesn't work, try searching for "Klayers" or "requests" layers online.

### Option 2: Install Requests in Lambda (If you have shell access)

If you see a terminal/shell option in Lambda:
```bash
pip install requests -t .
```

### Option 3: Skip Layer - Use urllib Instead

You can modify the code to use Python's built-in `urllib` instead of `requests`:

```python
import json
import os
import urllib.request
import urllib.parse

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001")
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL}/api/zoom/webhook"

def lambda_handler(event, context):
    try:
        headers = event.get("headers", {})
        body = event.get("body", "{}")
        
        if isinstance(body, str):
            body_data = json.loads(body)
        else:
            body_data = body
        
        # Use urllib instead of requests
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
            return {
                "statusCode": response.getcode(),
                "headers": {"Content-Type": "application/json"},
                "body": response_data if response_data else json.dumps({"status": "received"})
            }
            
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
```

This uses Python's built-in `urllib` - no layer needed!

## Recommendation

**Use Option 3** (urllib) - it's the simplest and requires no additional setup. Just replace the code in your Lambda function.

