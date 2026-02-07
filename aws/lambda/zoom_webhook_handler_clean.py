import json
import os
import urllib.request
import urllib.error

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001").strip()
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL.rstrip('/')}/api/zoom/webhook"


def lambda_handler(event, context):
    print("=" * 60)
    print("🔔 LAMBDA FUNCTION INVOKED")
    print(f"   Request ID: {context.aws_request_id if context else 'N/A'}")
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
                "x-zoom-request-timestamp": headers.get("x-zoom-request-timestamp", ""),
                "ngrok-skip-browser-warning": "true",  # Bypass ngrok browser warning
                "User-Agent": "Zoom-Webhook/1.0"  # Set user agent
            }
        )
        
        print(f"   🌐 Making request to: {WEBHOOK_ENDPOINT}")
        
        try:
            # Create opener that follows redirects (including POST redirects)
            class PostRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    # Handle POST redirects (307, 308)
                    if code in (307, 308):
                        # Preserve the original method and data
                        new_req = urllib.request.Request(newurl, data=req.data, headers=req.headers, method=req.get_method())
                        return new_req
                    # For other redirects, use default behavior
                    return super().redirect_request(req, fp, code, msg, headers, newurl)
            
            opener = urllib.request.build_opener(PostRedirectHandler())
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
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(response_json)
                }
        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                if hasattr(e, 'read'):
                    error_body = e.read().decode('utf-8')
                else:
                    error_body = str(e)
            except:
                error_body = str(e)
            
            print(f"   ❌ HTTP Error: {e.code}")
            if error_body:
                print(f"   Error body: {error_body[:200]}")
            
            # If it's a 307 redirect, try to get the location header
            if e.code == 307:
                location = e.headers.get('Location', '')
                if location:
                    print(f"   🔄 Redirect to: {location}")
                    print("   💡 This might be ngrok's browser warning page")
            
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

