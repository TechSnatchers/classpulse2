from typing import Dict, Optional
from datetime import datetime
from ..models.zoom_event import ZoomMeetingEvent, ZoomParticipant
from ..database.connection import get_database, get_database_by_name
import hmac
import hashlib
import base64
import os
import json


class ZoomWebhookService:
    """Service to handle Zoom webhook events"""
    
    def __init__(self):
        self.secret_token = os.getenv("ZOOM_WEBHOOK_SECRET_TOKEN", "")
    
    def verify_webhook(self, payload: bytes, signature: str, timestamp: str) -> bool:
        """Verify Zoom webhook signature"""
        if not self.secret_token:
            # In development, allow without verification
            return True
        
        message = f"v0:{timestamp}:{payload.decode('utf-8')}"
        hash_signature = hmac.new(
            self.secret_token.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        expected_signature = f"v0={hash_signature}"
        return hmac.compare_digest(signature, expected_signature)
    
    async def handle_event(self, event_data: Dict) -> Dict:
        """Handle incoming Zoom webhook event"""
        event_type = event_data.get("event")
        print(f"📥 Received Zoom event: {event_type}")
        print(f"   Event data: {event_data}")
        
        try:
            if event_type == "endpoint.url_validation":
                print("   → Handling URL validation")
                return await self.handle_validation(event_data)
            elif event_type == "meeting.started":
                print("   → Handling meeting.started")
                return await self.handle_meeting_started(event_data)
            elif event_type == "meeting.ended":
                print("   → Handling meeting.ended")
                return await self.handle_meeting_ended(event_data)
            elif event_type == "participant.joined" or event_type == "meeting.participant_joined":
                print(f"   → Handling {event_type}")
                return await self.handle_participant_joined(event_data)
            elif event_type == "participant.left" or event_type == "meeting.participant_left":
                print(f"   → Handling {event_type}")
                return await self.handle_participant_left(event_data)
            elif event_type == "recording.completed":
                print("   → Handling recording.completed")
                return await self.handle_recording_completed(event_data)
            else:
                print(f"   ⚠️  Unknown event type: {event_type}")
                return {
                    "status": "received",
                    "event": event_type,
                    "message": "Event logged but not processed"
                }
        except Exception as e:
            print(f"❌ Error handling Zoom event: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def handle_validation(self, event_data: Dict) -> Dict:
        """Handle Zoom webhook URL validation"""
        plain_token = event_data.get("payload", {}).get("plainToken", "")
        encrypted_token = self.encrypt_token(plain_token)
        
        return {
            "plainToken": plain_token,
            "encryptedToken": encrypted_token
        }
    
    def encrypt_token(self, plain_token: str) -> str:
        """Encrypt token using Zoom secret"""
        if not self.secret_token:
            return ""
        
        hash_signature = hmac.new(
            self.secret_token.encode('utf-8'),
            plain_token.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(hash_signature).decode('utf-8')
    
    async def handle_meeting_started(self, event_data: Dict) -> Dict:
        """Handle meeting started event"""
        # Get zoom_attendance database
        zoom_db = get_database_by_name("zoom_attendance")
        if zoom_db is None:
            print("❌ Database not connected in handle_meeting_started")
            return {"status": "error", "message": "Database not connected"}
        
        payload = event_data.get("payload", {})
        meeting = payload.get("object", {})
        
        if not meeting:
            print(f"⚠️  No meeting object in payload: {payload}")
            return {"status": "error", "message": "No meeting object in payload"}
        
        # Parse start_time if it's a string
        start_time_str = meeting.get("start_time")
        if isinstance(start_time_str, str):
            try:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            except:
                start_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        else:
            start_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        
        meeting_data = {
            "zoom_meeting_id": meeting.get("id"),
            "zoom_uuid": meeting.get("uuid"),
            "topic": meeting.get("topic"),
            "start_time": start_time,
            "host_id": meeting.get("host_id"),
            "meeting_type": meeting.get("type"),
            "duration": meeting.get("duration", 0),
            "timezone": meeting.get("timezone", ""),
            "status": "started",
            "created_at": datetime.now(),
            "raw_meeting_data": meeting  # Store raw data for reference
        }
        
        print(f"   💾 Saving to database: zoom_attendance, collection: meetings")
        
        try:
            # Save to zoom_attendance database, meetings collection
            result = await zoom_db.meetings.insert_one(meeting_data)
            print(f"✅ Meeting stored successfully!")
            print(f"      Database: zoom_attendance")
            print(f"      Collection: meetings")
            print(f"      Meeting ID: {meeting.get('id')}")
            print(f"      Topic: {meeting.get('topic')}")
            print(f"      MongoDB ID: {result.inserted_id}")
        except Exception as e:
            print(f"❌ Error storing meeting: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"Error storing meeting: {str(e)}"}
        
        return {
            "status": "success",
            "message": "Meeting started event processed",
            "meeting_id": meeting.get("id")
        }
    
    async def handle_meeting_ended(self, event_data: Dict) -> Dict:
        """Handle meeting ended event"""
        # Get zoom_attendance database
        zoom_db = get_database_by_name("zoom_attendance")
        if zoom_db is None:
            print("❌ Database not connected in handle_meeting_ended")
            return {"status": "error", "message": "Database not connected"}
        
        payload = event_data.get("payload", {})
        meeting = payload.get("object", {})
        meeting_id = meeting.get("id")
        
        # Parse end_time if it's a string
        end_time_str = meeting.get("end_time")
        if isinstance(end_time_str, str):
            try:
                end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
            except:
                end_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        else:
            end_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        
        print(f"   💾 Updating in database: zoom_attendance, collection: meetings")
        
        try:
            result = await zoom_db.meetings.update_one(
                {"zoom_meeting_id": meeting_id},
                {
                    "$set": {
                        "status": "ended",
                        "end_time": end_time,
                        "duration": meeting.get("duration", 0),
                        "updated_at": datetime.now()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"   ✅ Meeting ended updated: {meeting_id}")
            else:
                print(f"   ⚠️  Meeting not found to update: {meeting_id}")
        except Exception as e:
            print(f"   ❌ Error updating meeting: {e}")
            return {"status": "error", "message": f"Error updating meeting: {str(e)}"}
        
        return {
            "status": "success",
            "message": "Meeting ended event processed",
            "meeting_id": meeting_id
        }
    
    async def handle_participant_joined(self, event_data: Dict) -> Dict:
        """Handle participant joined event"""
        print(f"   👤 Processing participant.joined event")
        print(f"   Full event data: {json.dumps(event_data, indent=2, default=str)}")
        
        # Get zoom_attendance database
        zoom_db = get_database_by_name("zoom_attendance")
        if zoom_db is None:
            print("   ❌ Database not connected")
            return {"status": "error", "message": "Database not connected"}
        
        payload = event_data.get("payload", {})
        print(f"   Payload keys: {list(payload.keys())}")
        
        # Zoom can send participant data in different structures
        # Try multiple possible locations
        meeting = payload.get("object", {})
        participant = None
        
        # Try different participant locations
        if "participant" in meeting:
            participant = meeting.get("participant", {})
        elif "participant" in payload:
            participant = payload.get("participant", {})
        elif "object" in payload and isinstance(payload.get("object"), dict):
            # Sometimes participant is directly in object
            obj = payload.get("object", {})
            if "participant" in obj:
                participant = obj.get("participant", {})
            elif "user_id" in obj or "user_name" in obj:
                # Participant data might be directly in object
                participant = obj
        
        print(f"   Meeting ID: {meeting.get('id')}")
        print(f"   Meeting object keys: {list(meeting.keys())}")
        print(f"   Participant found: {bool(participant)}")
        if participant:
            print(f"   Participant keys: {list(participant.keys())}")
            print(f"   Participant data: {participant}")
        
        if not participant:
            print("   ⚠️  No participant data found in event!")
            print(f"   Full payload structure:")
            print(f"   {json.dumps(payload, indent=2, default=str)}")
            # Try to extract any user-like data
            if "object" in payload:
                obj = payload.get("object", {})
                print(f"   Object contains: {list(obj.keys())}")
            return {"status": "error", "message": "No participant data in event"}
        
        # Parse join_time if it's a string
        join_time_str = participant.get("join_time")
        if isinstance(join_time_str, str):
            try:
                join_time = datetime.fromisoformat(join_time_str.replace('Z', '+00:00'))
            except:
                join_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        else:
            join_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        
        # Extract participant data with multiple fallbacks
        participant_data = {
            "zoom_meeting_id": meeting.get("id") or payload.get("meeting_id"),
            "meeting_topic": meeting.get("topic", ""),
            "meeting_uuid": meeting.get("uuid", ""),
            "user_id": (
                participant.get("user_id") or 
                participant.get("id") or 
                participant.get("participant_user_id") or
                "unknown"
            ),
            "user_name": (
                participant.get("user_name") or 
                participant.get("name") or 
                participant.get("display_name") or
                "Unknown User"
            ),
            "email": participant.get("email") or participant.get("user_email"),
            "participant_user_id": participant.get("participant_user_id"),
            "participant_uuid": participant.get("participant_uuid"),
            "public_ip": participant.get("public_ip"),
            "private_ip": participant.get("private_ip"),
            "join_time": join_time,
            "status": "joined",
            "created_at": datetime.now(),
            "raw_participant_data": participant  # Store raw data for debugging
        }
        
        print(f"   📝 Participant data to store: {participant_data}")
        print(f"   💾 Saving to database: zoom_attendance, collection: participants")
        
        try:
            # Save to zoom_attendance database, participants collection
            result = await zoom_db.participants.insert_one(participant_data)
            print(f"   ✅ Participant stored successfully!")
            print(f"      Database: zoom_attendance")
            print(f"      Collection: participants")
            print(f"      Name: {participant_data.get('user_name')}")
            print(f"      User ID: {participant_data.get('user_id')}")
            print(f"      Meeting ID: {participant_data.get('zoom_meeting_id')}")
            print(f"      MongoDB ID: {result.inserted_id}")
        except Exception as e:
            print(f"   ❌ Error storing participant: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"Error storing participant: {str(e)}"}
        
        return {
            "status": "success",
            "message": "Participant joined event processed",
            "participant": participant_data.get("user_name"),
            "user_id": participant_data.get("user_id")
        }
    
    async def handle_participant_left(self, event_data: Dict) -> Dict:
        """Handle participant left event"""
        print(f"   👋 Processing participant.left event")
        print(f"   Full event data: {json.dumps(event_data, indent=2, default=str)}")
        
        # Get zoom_attendance database
        zoom_db = get_database_by_name("zoom_attendance")
        if zoom_db is None:
            print("   ❌ Database not connected")
            return {"status": "error", "message": "Database not connected"}
        
        payload = event_data.get("payload", {})
        meeting = payload.get("object", {})
        participant = meeting.get("participant", {})
        
        print(f"   Meeting ID: {meeting.get('id')}")
        print(f"   Meeting object keys: {list(meeting.keys())}")
        print(f"   Participant found: {bool(participant)}")
        if participant:
            print(f"   Participant keys: {list(participant.keys())}")
            print(f"   Participant data: {participant}")
        
        if not participant:
            print("   ⚠️  No participant data in event!")
            return {"status": "error", "message": "No participant data in event"}
        
        # Extract user_id using same logic as join handler
        user_id = (
            participant.get("user_id") or 
            participant.get("id") or 
            participant.get("participant_user_id") or
            "unknown"
        )
        participant_user_id = participant.get("participant_user_id")
        meeting_id = meeting.get("id")
        
        print(f"   🔍 Searching for participant:")
        print(f"      Meeting ID: {meeting_id}")
        print(f"      User ID: {user_id}")
        print(f"      Participant User ID: {participant_user_id}")
        
        # Parse leave_time if it's a string
        leave_time_str = participant.get("leave_time")
        if isinstance(leave_time_str, str):
            try:
                leave_time = datetime.fromisoformat(leave_time_str.replace('Z', '+00:00'))
            except:
                leave_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        else:
            leave_time = datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000)
        
        print(f"   💾 Updating in database: zoom_attendance, collection: participants")
        
        try:
            # Try multiple query combinations to find the participant
            update_data = {
                "$set": {
                    "leave_time": leave_time,
                    "leave_reason": participant.get("leave_reason", ""),
                    "status": "left",
                    "updated_at": datetime.now()
                }
            }
            
            # First try: match by meeting_id and user_id (most common case)
            query1 = {
                "zoom_meeting_id": meeting_id,
                "user_id": user_id
            }
            print(f"   🔍 Trying query 1: {query1}")
            result = await zoom_db.participants.update_one(query1, update_data)
            
            if result.modified_count > 0:
                print(f"   ✅ Participant left updated (query 1): {user_id}")
            else:
                # Second try: match by meeting_id and participant_user_id
                if participant_user_id:
                    query2 = {
                        "zoom_meeting_id": meeting_id,
                        "participant_user_id": participant_user_id
                    }
                    print(f"   🔍 Trying query 2: {query2}")
                    result = await zoom_db.participants.update_one(query2, update_data)
                    
                    if result.modified_count > 0:
                        print(f"   ✅ Participant left updated (query 2): {participant_user_id}")
                    else:
                        # Third try: match by meeting_id and email
                        email = participant.get("email")
                        if email:
                            query3 = {
                                "zoom_meeting_id": meeting_id,
                                "email": email
                            }
                            print(f"   🔍 Trying query 3: {query3}")
                            result = await zoom_db.participants.update_one(query3, update_data)
                            
                            if result.modified_count > 0:
                                print(f"   ✅ Participant left updated (query 3): {email}")
                            else:
                                print(f"   ⚠️  Participant not found with any query")
                                # Create new record if not found
                                await self._create_participant_left_record(zoom_db, meeting, participant, leave_time)
                        else:
                            print(f"   ⚠️  Participant not found, creating new record")
                            await self._create_participant_left_record(zoom_db, meeting, participant, leave_time)
                else:
                    print(f"   ⚠️  Participant not found, creating new record")
                    await self._create_participant_left_record(zoom_db, meeting, participant, leave_time)
            
            # Log final result
            print(f"   ✅ Participant left event processed successfully")
            
        except Exception as e:
            print(f"   ❌ Error updating participant: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"Error updating participant: {str(e)}"}
        
        return {
            "status": "success",
            "message": "Participant left event processed"
        }
    
    async def _create_participant_left_record(self, zoom_db, meeting: Dict, participant: Dict, leave_time: datetime):
        """Helper method to create a new participant record for left event"""
        user_id = (
            participant.get("user_id") or 
            participant.get("id") or 
            participant.get("participant_user_id") or
            "unknown"
        )
        
        participant_data = {
            "zoom_meeting_id": meeting.get("id"),
            "meeting_topic": meeting.get("topic", ""),
            "meeting_uuid": meeting.get("uuid", ""),
            "user_id": user_id,
            "user_name": participant.get("user_name") or participant.get("name", "Unknown"),
            "email": participant.get("email"),
            "participant_user_id": participant.get("participant_user_id"),
            "participant_uuid": participant.get("participant_uuid"),
            "public_ip": participant.get("public_ip"),
            "private_ip": participant.get("private_ip"),
            "join_time": None,  # We don't have join time for left events
            "leave_time": leave_time,
            "leave_reason": participant.get("leave_reason", ""),
            "status": "left",
            "created_at": datetime.now()
        }
        
        result = await zoom_db.participants.insert_one(participant_data)
        print(f"   ✅ Created new participant record for left event")
        print(f"      MongoDB ID: {result.inserted_id}")
        print(f"      User: {participant_data.get('user_name')}")
        print(f"      Meeting ID: {participant_data.get('zoom_meeting_id')}")
    
    async def handle_recording_completed(self, event_data: Dict) -> Dict:
        """Handle recording completed event"""
        database = get_database()
        if database is None:
            return {"status": "error", "message": "Database not connected"}
        
        payload = event_data.get("payload", {})
        meeting = payload.get("object", {})
        recording_files = payload.get("object", {}).get("recording_files", [])
        
        recording_data = {
            "zoom_meeting_id": meeting.get("id"),
            "recording_files": recording_files,
            "completed_at": datetime.fromtimestamp(event_data.get("event_ts", 0) / 1000),
            "created_at": datetime.now()
        }
        
        await database.zoom_recordings.insert_one(recording_data)
        
        return {
            "status": "success",
            "message": "Recording completed event processed"
        }

