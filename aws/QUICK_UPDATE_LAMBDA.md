# Quick Guide: Update Your Lambda Function

## Your Current Setup
- ✅ Lambda function: `zoom_webhook` (already created)
- ✅ Region: `eu-north-1`
- ✅ Connected to API Gateway

## What You Need to Do

### 1. Update Lambda Code

**In AWS Console:**
1. Go to Lambda → `zoom_webhook` function
2. Click "Code" tab
3. Replace the code with this:

```python
import json
import os
import requests

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
        
        response = requests.post(
            WEBHOOK_ENDPOINT,
            json=body_data,
            headers={
                "Content-Type": "application/json",
                "x-zoom-signature": headers.get("x-zoom-signature", ""),
                "x-zoom-request-origin": headers.get("x-zoom-request-origin", ""),
                "x-zoom-request-timestamp": headers.get("x-zoom-request-timestamp", "")
            },
            timeout=10
        )
        
        return {
            "statusCode": response.status_code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response.json() if response.text else {"status": "received"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
```

4. Click "Deploy"

### 2. Add Layer for Requests Library

Since Lambda needs the `requests` library:

**Option A: Add Layer (Easiest)**
1. In Lambda → Layers
2. Click "Add a layer"
3. Choose "AWS provided" or create custom layer with `requests`

**Option B: Bundle with Code**
- Create a deployment package with `requests` included

### 3. Set Environment Variable

1. Go to Configuration → Environment variables
2. Add:
   - Key: `BACKEND_API_URL`
   - Value: `http://localhost:3001` (or your backend URL)

### 4. Get Webhook URL

1. Go to Configuration → Triggers
2. Click on API Gateway
3. Copy the "API endpoint" URL
4. Use this URL in Zoom webhook configuration

### 5. Make Sure Backend is Running

```powershell
cd ..\backend
python main.py
```

## Test It

1. Configure Zoom with the API Gateway URL
2. Create a test meeting
3. Check Lambda logs in CloudWatch
4. Check backend logs

