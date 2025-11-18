"""
Zoom Webhook handler for receiving meeting events
Handles participant_joined and participant_left events
"""
from flask import Blueprint, request, jsonify
import hmac
import hashlib
import os
from datetime import datetime
from database import get_db


# Create Blueprint
webhook_bp = Blueprint('zoom_webhook', __name__, url_prefix='/api/zoom')


def verify_webhook_signature(payload, signature, timestamp):
    """
    Verify Zoom webhook signature
    
    Args:
        payload (bytes): Request payload
        signature (str): Zoom signature from header
        timestamp (str): Timestamp from header
        
    Returns:
        bool: True if valid, False otherwise
    """
    secret = os.getenv('ZOOM_WEBHOOK_SECRET', '')
    
    if not secret:
        # In development, allow without verification
        print("⚠️  Warning: ZOOM_WEBHOOK_SECRET not set, skipping verification")
        return True
    
    try:
        message = f"v0:{timestamp}:{payload.decode('utf-8')}"
        hash_signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        expected_signature = f"v0={hash_signature}"
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        print(f"❌ Signature verification error: {e}")
        return False


@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming Zoom webhooks
    
    Supported events:
    - endpoint.url_validation: Zoom webhook validation
    - meeting.participant_joined: Participant joins meeting
    - meeting.participant_left: Participant leaves meeting
    """
    print("\n" + "="*60)
    print(f"🔔 ZOOM WEBHOOK RECEIVED")
    print(f"   Time: {datetime.now().isoformat()}")
    print("="*60)
    
    try:
        # Get headers
        signature = request.headers.get('x-zoom-signature')
        timestamp = request.headers.get('x-zoom-request-timestamp')
        
        # Get payload
        payload = request.get_data()
        
        # Verify signature (if configured)
        if signature and timestamp:
            if not verify_webhook_signature(payload, signature, timestamp):
                print("❌ Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse event data
        event_data = request.get_json()
        event_type = event_data.get('event')
        
        print(f"📥 Event Type: {event_type}")
        
        # Handle different event types
        if event_type == 'endpoint.url_validation':
            return handle_url_validation(event_data)
        
        elif event_type in ['meeting.participant_joined', 'participant.joined']:
            return handle_participant_joined(event_data)
        
        elif event_type in ['meeting.participant_left', 'participant.left']:
            return handle_participant_left(event_data)
        
        else:
            print(f"⚠️  Unknown event type: {event_type}")
            return jsonify({
                'status': 'received',
                'message': 'Event logged but not processed',
                'event': event_type
            }), 200
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def handle_url_validation(event_data):
    """
    Handle Zoom webhook URL validation
    
    Args:
        event_data (dict): Event payload
        
    Returns:
        Response: JSON response with encrypted token
    """
    print("🔐 Handling URL validation")
    
    payload = event_data.get('payload', {})
    plain_token = payload.get('plainToken', '')
    
    # Encrypt token
    secret = os.getenv('ZOOM_WEBHOOK_SECRET', '')
    
    if not secret:
        print("❌ ZOOM_WEBHOOK_SECRET not configured")
        return jsonify({'error': 'Webhook secret not configured'}), 500
    
    hash_signature = hmac.new(
        secret.encode('utf-8'),
        plain_token.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    import base64
    encrypted_token = base64.b64encode(hash_signature).decode('utf-8')
    
    print(f"✅ URL validation successful")
    
    return jsonify({
        'plainToken': plain_token,
        'encryptedToken': encrypted_token
    }), 200


def handle_participant_joined(event_data):
    """
    Handle participant joined event
    
    Args:
        event_data (dict): Event payload
        
    Returns:
        Response: JSON response
    """
    print("👤 Handling participant_joined event")
    
    try:
        payload = event_data.get('payload', {})
        meeting = payload.get('object', {})
        participant = meeting.get('participant', {})
        
        if not participant:
            print("⚠️  No participant data in event")
            return jsonify({'error': 'No participant data'}), 400
        
        # Extract participant information
        participant_data = {
            'meeting_id': str(meeting.get('id', '')),
            'user_id': str(participant.get('user_id') or participant.get('id', '')),
            'name': participant.get('user_name') or participant.get('name', 'Unknown'),
            'email': participant.get('email', ''),
            'join_time': datetime.utcnow(),
            'status': 'joined',
            'raw_data': participant  # Store raw data for debugging
        }
        
        print(f"   Meeting ID: {participant_data['meeting_id']}")
        print(f"   User ID: {participant_data['user_id']}")
        print(f"   Name: {participant_data['name']}")
        print(f"   Email: {participant_data['email']}")
        
        # Save to database
        db = get_db()
        db.add_participant(participant_data)
        
        print(f"✅ Participant stored in database")
        
        return jsonify({
            'status': 'success',
            'message': 'Participant joined event processed',
            'participant': {
                'user_id': participant_data['user_id'],
                'name': participant_data['name']
            }
        }), 200
    
    except Exception as e:
        print(f"❌ Error handling participant_joined: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def handle_participant_left(event_data):
    """
    Handle participant left event
    
    Args:
        event_data (dict): Event payload
        
    Returns:
        Response: JSON response
    """
    print("👋 Handling participant_left event")
    
    try:
        payload = event_data.get('payload', {})
        meeting = payload.get('object', {})
        participant = meeting.get('participant', {})
        
        if not participant:
            print("⚠️  No participant data in event")
            return jsonify({'error': 'No participant data'}), 400
        
        meeting_id = str(meeting.get('id', ''))
        user_id = str(participant.get('user_id') or participant.get('id', ''))
        
        print(f"   Meeting ID: {meeting_id}")
        print(f"   User ID: {user_id}")
        
        # Remove from database
        db = get_db()
        db.remove_participant(meeting_id, user_id)
        
        print(f"✅ Participant removed from database")
        
        return jsonify({
            'status': 'success',
            'message': 'Participant left event processed',
            'user_id': user_id
        }), 200
    
    except Exception as e:
        print(f"❌ Error handling participant_left: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@webhook_bp.route('/webhook/test', methods=['GET'])
def test_webhook():
    """Test endpoint to verify webhook is accessible"""
    return jsonify({
        'status': 'ok',
        'message': 'Zoom webhook endpoint is ready',
        'endpoint': '/api/zoom/webhook'
    }), 200

