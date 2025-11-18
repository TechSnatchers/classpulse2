from fastapi import APIRouter, Request, HTTPException, Header, status
from typing import Optional
from ..services.zoom_webhook_service import ZoomWebhookService
from datetime import datetime
from starlette.requests import ClientDisconnect
import json

router = APIRouter(prefix="/api/zoom/webhook", tags=["zoom"])

zoom_webhook_service = ZoomWebhookService()


@router.post("/")
async def receive_webhook(
    request: Request,
    x_zoom_signature: Optional[str] = Header(None, alias="x-zoom-signature"),
    x_zoom_request_origin: Optional[str] = Header(None, alias="x-zoom-request-origin"),
    x_zoom_request_timestamp: Optional[str] = Header(None, alias="x-zoom-request-timestamp")
):
    """Receive and process Zoom webhook events"""
    print("=" * 60)
    print("🔔 WEBHOOK REQUEST RECEIVED")
    print(f"   Time: {datetime.now().isoformat()}")
    print(f"   Headers: x-zoom-signature={bool(x_zoom_signature)}, x-zoom-request-timestamp={bool(x_zoom_request_timestamp)}")
    print("=" * 60)
    
    try:
        # Get request body as bytes for signature verification
        # Handle ClientDisconnect gracefully
        body_bytes = None
        event_data = None
        
        try:
            body_bytes = await request.body()
            print(f"📦 Body received: {len(body_bytes)} bytes")
        except ClientDisconnect:
            print("⚠️  Client disconnected before body could be read")
            # If client disconnected, we can't read the body
            # Return success to prevent Zoom from retrying
            return {
                "status": "received",
                "message": "Request received but client disconnected before body could be read"
            }
        except Exception as e:
            print(f"⚠️  Error reading body: {e}")
            # Try to get JSON directly as fallback
            try:
                event_data = await request.json()
                body_bytes = json.dumps(event_data).encode('utf-8')
                print(f"📦 Body retrieved from JSON fallback: {len(body_bytes)} bytes")
            except Exception as json_error:
                print(f"❌ Could not retrieve request body: {json_error}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Request body could not be read"
                )
        
        # If body_bytes is empty, try to get JSON directly
        if not body_bytes or len(body_bytes) == 0:
            print("⚠️  Body is empty, trying to get JSON directly...")
            try:
                event_data = await request.json()
                body_bytes = json.dumps(event_data).encode('utf-8')
                print(f"📦 Body retrieved from JSON: {len(body_bytes)} bytes")
            except Exception as e:
                print(f"❌ Could not retrieve request body: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Request body is empty"
                )
        
        # Verify webhook signature if provided
        if x_zoom_signature and x_zoom_request_timestamp and body_bytes:
            print("🔐 Verifying webhook signature...")
            if not zoom_webhook_service.verify_webhook(
                body_bytes,
                x_zoom_signature,
                x_zoom_request_timestamp
            ):
                print("❌ Invalid webhook signature!")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook signature"
                )
            print("✅ Signature verified")
        else:
            print("⚠️  No signature provided (skipping verification)")
        
        # Parse event data from body if not already parsed
        if event_data is None:
            try:
                body_str = body_bytes.decode('utf-8')
                print(f"📄 Body content: {body_str[:200]}...")  # First 200 chars
                event_data = json.loads(body_str)
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid JSON payload"
                )
        
        print(f"✅ Event parsed: {event_data.get('event', 'unknown')}")
        
        # Handle the event
        print("🔄 Processing event...")
        result = await zoom_webhook_service.handle_event(event_data)
        print(f"✅ Event processed: {result.get('status', 'unknown')}")
        print("=" * 60)
        
        return result
        
    except ClientDisconnect:
        print("❌ Client disconnected during request processing")
        # Return 200 OK to prevent retries from Zoom
        return {
            "status": "received",
            "message": "Request received but client disconnected"
        }
    except HTTPException:
        print("❌ HTTP Exception raised")
        raise
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )


@router.get("/health")
async def webhook_health():
    """Health check for webhook endpoint"""
    return {
        "status": "ok",
        "message": "Zoom webhook endpoint is ready"
    }

