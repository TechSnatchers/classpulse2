"""
AWS Lambda function to handle Zoom webhooks (No external dependencies)
Uses Python's built-in urllib instead of requests
"""
import json
import os
import urllib.request
import urllib.error

# Backend API endpoint
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3001")
WEBHOOK_ENDPOINT = f"{BACKEND_API_URL}/api/zoom/webhook"


def lambda_handler(event, context):
    """
    AWS Lambda handler for Zoom webhooks
    Uses urllib (built-in) - no external dependencies needed!
    """
    try:
        # Extract headers and body from API Gateway event
        headers = event.get("headers", {}) or {}
        body = event.get("body", "{}")
        
        # Parse body if it's a string
        if isinstance(body, str):
            try:
                body_data = json.loads(body)
            except json.JSONDecodeError:
                body_data = {}
        else:
            body_data = body
        
        # Prepare request data
        data = json.dumps(body_data).encode('utf-8')
        
        # Create request with headers
        req = urllib.request.Request(
            WEBHOOK_ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-zoom-signature": headers.get("x-zoom-signature") or headers.get("x-zoom-signature", ""),
                "x-zoom-request-origin": headers.get("x-zoom-request-origin") or headers.get("x-zoom-request-origin", ""),
                "x-zoom-request-timestamp": headers.get("x-zoom-request-timestamp") or headers.get("x-zoom-request-timestamp", "")
            }
        )
        
        # Make request
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode('utf-8')
            try:
                response_json = json.loads(response_data) if response_data else {"status": "received"}
            except json.JSONDecodeError:
                response_json = {"status": "received", "raw": response_data}
            
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
        return {
            "statusCode": e.code,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Failed to forward webhook",
                "message": error_body
            })
        }
    except urllib.error.URLError as e:
        # Handle URL errors (connection issues)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Connection error",
                "message": str(e)
            })
        }
    except Exception as e:
        # Handle any other errors
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

