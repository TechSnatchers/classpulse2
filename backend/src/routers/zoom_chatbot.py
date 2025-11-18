from fastapi import APIRouter, Request, HTTPException, Header, status
from typing import Optional
from datetime import datetime
import json
import hmac
import hashlib
import os

router = APIRouter(prefix="/api/zoom/chatbot", tags=["zoom-chatbot"])

# Get Zoom webhook secret token from environment variables
ZOOM_WEBHOOK_SECRET_TOKEN = os.getenv("ZOOM_WEBHOOK_SECRET_TOKEN", "")


def verify_chatbot_signature(request_body: bytes, signature: str, timestamp: str) -> bool:
    """Verify Zoom chatbot webhook signature"""
    if not ZOOM_WEBHOOK_SECRET_TOKEN:
        print("⚠️  ZOOM_WEBHOOK_SECRET_TOKEN not set. Skipping signature verification.")
        return True  # Allow in development if secret is not set

    message = f"v0:{timestamp}:{request_body.decode('utf-8')}"
    hash_signature = hmac.new(
        ZOOM_WEBHOOK_SECRET_TOKEN.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    expected_signature = f"v0={hash_signature}"
    return hmac.compare_digest(signature, expected_signature)


@router.post("/")
async def receive_chatbot_webhook(
    request: Request,
    x_zoom_signature: Optional[str] = Header(None, alias="x-zoom-signature"),
    x_zoom_request_timestamp: Optional[str] = Header(None, alias="x-zoom-request-timestamp")
):
    """
    Receive and process Zoom chatbot webhook events
    
    This endpoint handles:
    - Chatbot message events
    - Bot command events
    - Other chatbot-related events from Zoom
    """
    print("\n" + "=" * 60)
    print("🤖 ZOOM CHATBOT WEBHOOK RECEIVED")
    print(f"   Time: {datetime.now().isoformat()}")
    print("=" * 60)

    try:
        # Get request body
        body_bytes = await request.body()
        print(f"📦 Body received: {len(body_bytes)} bytes")

        # Verify signature if provided
        if x_zoom_signature and x_zoom_request_timestamp:
            print("🔐 Verifying chatbot webhook signature...")
            if not verify_chatbot_signature(body_bytes, x_zoom_signature, x_zoom_request_timestamp):
                print("❌ Invalid chatbot webhook signature!")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook signature"
                )
            print("✅ Signature verified")
        else:
            print("⚠️  No signature provided (skipping verification)")

        # Parse event data
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

        # Extract event type
        event_type = event_data.get("event", "unknown")
        print(f"📋 Event type: {event_type}")

        # Handle different event types
        if event_type == "bot.message":
            print("💬 Processing bot message event...")
            return await handle_bot_message(event_data)
        elif event_type == "bot.command":
            print("⌨️  Processing bot command event...")
            return await handle_bot_command(event_data)
        elif event_type == "endpoint.url_validation":
            print("🔗 Processing URL validation...")
            return handle_url_validation(event_data)
        else:
            print(f"⚠️  Unhandled event type: {event_type}")
            return {
                "status": "received",
                "message": f"Event type {event_type} received but not handled",
                "event_type": event_type
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing chatbot webhook: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chatbot webhook: {str(e)}"
        )


async def handle_bot_message(event_data: dict):
    """Handle bot message events from Zoom"""
    payload = event_data.get("payload", {})
    message = payload.get("message", {})
    sender = payload.get("sender", {})
    
    print(f"   From: {sender.get('user_name', 'Unknown')}")
    print(f"   Message: {message.get('text', '')[:100]}...")
    
    # TODO: Process the message here
    # You can:
    # - Store the message in database
    # - Trigger question sending
    # - Respond to the message
    # - etc.
    
    return {
        "status": "success",
        "message": "Bot message event processed",
        "event_type": "bot.message"
    }


async def handle_bot_command(event_data: dict):
    """Handle bot command events from Zoom"""
    payload = event_data.get("payload", {})
    command = payload.get("command", "")
    sender = payload.get("sender", {})
    
    print(f"   Command: {command}")
    print(f"   From: {sender.get('user_name', 'Unknown')}")
    
    # TODO: Process the command here
    # You can:
    # - Handle slash commands (e.g., /send-question)
    # - Trigger actions based on commands
    # - etc.
    
    return {
        "status": "success",
        "message": "Bot command event processed",
        "event_type": "bot.command",
        "command": command
    }


def handle_url_validation(event_data: dict):
    """Handle URL validation for chatbot webhook"""
    plain_token = event_data.get("payload", {}).get("plainToken", "")
    
    if not plain_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="plainToken not found in validation request"
        )
    
    if not ZOOM_WEBHOOK_SECRET_TOKEN:
        print("⚠️  ZOOM_WEBHOOK_SECRET_TOKEN not set. Cannot generate encrypted token.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret token not configured"
        )
    
    # Generate encrypted token
    encrypted_token = hmac.new(
        ZOOM_WEBHOOK_SECRET_TOKEN.encode('utf-8'),
        plain_token.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print("✅ URL validation successful")
    return {
        "plainToken": plain_token,
        "encryptedToken": encrypted_token
    }


@router.get("/health")
async def chatbot_health():
    """Health check for chatbot endpoint"""
    return {
        "status": "ok",
        "message": "Zoom chatbot endpoint is ready",
        "timestamp": datetime.now().isoformat()
    }

