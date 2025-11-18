"""
AWS Lambda function to handle Zoom webhooks (No external dependencies)
Uses Python's built-in urllib instead of requests
"""
import json
import os
import urllib.request
import urllib.error

# Backend API endpoint
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001").strip()
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL.rstrip('/')}/api/zoom/webhook"


def lambda_handler(event, context):
    """
    AWS Lambda handler for Zoom webhooks
    Uses urllib (built-in) - no external dependencies needed!
    """
    print("=" * 60)
    print("🔔 LAMBDA FUNCTION INVOKED")
    print(f"   Request ID: {context.aws_request_id if context else 'N/A'}")
    print(f"   Backend URL: {BACKEND_API_URL}")
    print(f"   Webhook Endpoint: {WEBHOOK_ENDPOINT}")
    print("=" * 60)
    
    try:
        # Extract headers and body from API Gateway event
        print("📦 Processing event...")
        headers = event.get("headers", {}) or {}
        body = event.get("body", "{}")
        
        print(f"   Headers present: {bool(headers)}")
        print(f"   Body type: {type(body)}")
        print(f"   Body length: {len(str(body))} bytes")
        
        # Parse body if it's a string
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
        
        # Prepare request data
        data = json.dumps(body_data).encode('utf-8')
        print(f"   📤 Sending {len(data)} bytes to backend...")
        
        # Create request with headers
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
        
        # Make request with redirect handler
        try:
            # Create opener that follows redirects (for ngrok HTTP 307)
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
            with opener.open(req, timeout=10) as response:
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
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps(response_json)
                }
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            print(f"   ❌ HTTP Error: {e.code} - {error_body}")
            print("=" * 60)
            return {
                "statusCode": e.code,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Failed to forward webhook",
                    "message": error_body,
                    "code": e.code
                })
            }
        except urllib.error.URLError as e:
            # Handle URL errors (connection issues)
            print(f"   ❌ Connection Error: {e}")
            print(f"   💡 Check if backend is accessible at: {BACKEND_API_URL}")
            print("=" * 60)
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Connection error",
                    "message": str(e),
                    "backend_url": BACKEND_API_URL
                })
            }
            
    except Exception as e:
        # Handle any other errors
        print(f"   ❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        }
