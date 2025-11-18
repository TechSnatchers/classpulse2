"""
Send question endpoint
Broadcasts question links to all participants in a meeting
"""
from flask import Blueprint, request, jsonify
from database import get_db
from zoom_chat import get_zoom_chat


# Create Blueprint
send_question_bp = Blueprint('send_question', __name__, url_prefix='/api')


@send_question_bp.route('/send-question', methods=['POST'])
def send_question():
    """
    Send question link to meeting chat or individual participants
    
    Request JSON:
    {
        "question_link": "https://example.com/question/abc123",
        "meeting_id": "123456789",
        "send_to_meeting_chat": true  // Optional: if true, sends to meeting chat instead of DMs
    }
    
    Returns:
        JSON response with results
    """
    print("\n" + "="*60)
    print("📤 SEND QUESTION REQUEST")
    print("="*60)
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        question_link = data.get('question_link')
        meeting_id = data.get('meeting_id')
        send_to_meeting_chat = data.get('send_to_meeting_chat', True)  # Default to meeting chat
        
        # Validate input
        if not question_link:
            return jsonify({'error': 'question_link is required'}), 400
        
        if not meeting_id:
            return jsonify({'error': 'meeting_id is required'}), 400
        
        print(f"   Question Link: {question_link}")
        print(f"   Meeting ID: {meeting_id}")
        print(f"   Send to meeting chat: {send_to_meeting_chat}")
        
        # Prepare message
        message = f"📝 New Question! Answer here: {question_link}"
        
        # Get Zoom Chat API
        zoom_chat = get_zoom_chat()
        
        if send_to_meeting_chat:
            # Send to meeting chat (all participants see it)
            print("\n📢 Sending to meeting chat...")
            response = zoom_chat.send_meeting_chat_message(meeting_id, message)
            
            if response.get('success'):
                print(f"✅ Message sent to meeting chat!")
                return jsonify({
                    'success': True,
                    'message': 'Question sent to meeting chat',
                    'meeting_id': meeting_id,
                    'method': 'meeting_chat',
                    'response': response
                }), 200
            else:
                print(f"❌ Failed to send to meeting chat: {response.get('error')}")
                # Fall back to direct messages
                print("\n⚠️  Falling back to direct messages...")
                send_to_meeting_chat = False
        
        if not send_to_meeting_chat:
            # Send direct messages to each participant
            db = get_db()
            participants = db.get_participants_by_meeting(meeting_id)
            
            if not participants:
                print(f"⚠️  No participants found for meeting {meeting_id}")
                return jsonify({
                    'success': False,
                    'error': 'No participants found for this meeting',
                    'meeting_id': meeting_id,
                    'participants_found': 0
                }), 404
            
            print(f"✅ Found {len(participants)} participants")
            
            # Send messages to all participants
            results = []
            success_count = 0
            failed_count = 0
            
            for participant in participants:
                user_id = participant.get('user_id')
                name = participant.get('name', 'Unknown')
                email = participant.get('email', '')
                
                print(f"\n📨 Sending to: {name} ({user_id})")
                
                # Send message
                response = zoom_chat.send_chat_message(user_id, message)
                
                # Add participant info to response
                response['name'] = name
                response['email'] = email
                
                results.append(response)
                
                if response.get('success'):
                    success_count += 1
                else:
                    failed_count += 1
            
            print(f"\n{'='*60}")
            print(f"✅ SENDING COMPLETE")
            print(f"   Total: {len(participants)}")
            print(f"   Success: {success_count}")
            print(f"   Failed: {failed_count}")
            print(f"{'='*60}\n")
            
            return jsonify({
                'success': True,
                'message': f'Question sent to {len(participants)} participants',
                'meeting_id': meeting_id,
                'method': 'direct_messages',
                'total_participants': len(participants),
                'success_count': success_count,
                'failed_count': failed_count,
                'results': results
            }), 200
    
    except Exception as e:
        print(f"❌ Error sending question: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@send_question_bp.route('/meetings/<meeting_id>/participants', methods=['GET'])
def get_meeting_participants(meeting_id):
    """
    Get all participants for a specific meeting
    
    Args:
        meeting_id (str): Zoom meeting ID
        
    Returns:
        JSON response with list of participants
    """
    try:
        db = get_db()
        participants = db.get_participants_by_meeting(meeting_id)
        
        # Convert MongoDB documents to JSON-serializable format
        participants_list = []
        for p in participants:
            participant = {
                'user_id': p.get('user_id'),
                'name': p.get('name'),
                'email': p.get('email'),
                'meeting_id': p.get('meeting_id'),
                'join_time': p.get('join_time').isoformat() if p.get('join_time') else None,
                'status': p.get('status', 'joined')
            }
            participants_list.append(participant)
        
        return jsonify({
            'success': True,
            'meeting_id': meeting_id,
            'count': len(participants_list),
            'participants': participants_list
        }), 200
    
    except Exception as e:
        print(f"❌ Error getting participants: {e}")
        return jsonify({'error': str(e)}), 500


@send_question_bp.route('/test-zoom', methods=['GET'])
def test_zoom_connection():
    """
    Test Zoom API connection
    
    Returns:
        JSON response with connection status
    """
    try:
        zoom_chat = get_zoom_chat()
        result = zoom_chat.test_connection()
        
        return jsonify(result), 200 if result.get('success') else 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error testing connection: {str(e)}'
        }), 500

