import os
import requests
import base64
from typing import Optional
from datetime import datetime, timedelta
import json


class ZoomChatService:
    """Service to send messages to Zoom meeting chat using Zoom API"""
    
    def __init__(self):
        self.client_id = os.getenv("ZOOM_CLIENT_ID", "")
        self.client_secret = os.getenv("ZOOM_CLIENT_SECRET", "")
        self.account_id = os.getenv("ZOOM_ACCOUNT_ID", "")
        self.chatbot_jid = os.getenv("ZOOM_CHATBOT_JID", "")
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> Optional[str]:
        """Get or refresh OAuth access token for Zoom API"""
        # Check if token is still valid
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Get new token using Server-to-Server OAuth
        if not self.account_id or not self.client_id or not self.client_secret:
            print("⚠️  Zoom credentials not configured")
            return None
        
        try:
            # Encode credentials
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Request token
            url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}"
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                expires_in = data.get("expires_in", 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                print(f"✅ Zoom access token obtained (expires in {expires_in}s)")
                return self.access_token
            else:
                print(f"❌ Failed to get Zoom token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error getting Zoom access token: {e}")
            return None
    
    def send_message_to_meeting(
        self,
        meeting_id: str,
        message: str,
        bot_jid: Optional[str] = None
    ) -> bool:
        """
        Send a message to Zoom meeting chat
        
        Args:
            meeting_id: The Zoom meeting ID
            message: The message to send
            bot_jid: The chatbot JID (optional, uses env var if not provided)
        
        Returns:
            True if message sent successfully, False otherwise
        """
        token = self.get_access_token()
        if not token:
            print("❌ Cannot send message: No access token")
            return False
        
        jid = bot_jid or self.chatbot_jid
        if not jid:
            print("❌ Cannot send message: No chatbot JID configured")
            return False
        
        try:
            url = "https://api.zoom.us/v2/im/chat/messages"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "robot_jid": jid,
                "to_jid": f"{meeting_id}@conference.zoomgov.com",  # Meeting channel
                "account_id": self.account_id,
                "content": {
                    "head": {
                        "text": "📝 New Question!"
                    },
                    "body": [
                        {
                            "type": "message",
                            "text": message
                        }
                    ]
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print(f"✅ Message sent to Zoom meeting {meeting_id}")
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code} - {response.text}")
                # Try alternative format
                return self._send_message_alternative(meeting_id, message, token, jid)
        except Exception as e:
            print(f"❌ Error sending message to Zoom: {e}")
            return False
    
    def _send_message_alternative(
        self,
        meeting_id: str,
        message: str,
        token: str,
        jid: str
    ) -> bool:
        """Try alternative API format for sending messages"""
        try:
            # Alternative: Use in-meeting chat API
            url = f"https://api.zoom.us/v2/meetings/{meeting_id}/chat"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "message": message
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print(f"✅ Message sent using alternative API")
                return True
            else:
                print(f"❌ Alternative API also failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Alternative send also failed: {e}")
            return False
    
    def send_question_link(
        self,
        meeting_id: str,
        question_text: str,
        question_url: str,
        time_limit: int = 30
    ) -> bool:
        """
        Send a question link to Zoom meeting chat
        
        Args:
            meeting_id: The Zoom meeting ID
            question_text: The question text
            question_url: The URL where students can answer
            time_limit: Time limit in seconds
        
        Returns:
            True if sent successfully
        """
        message = (
            f"📝 **NEW QUESTION** (Time limit: {time_limit}s)\n\n"
            f"❓ {question_text}\n\n"
            f"👉 Click here to answer: {question_url}\n\n"
            f"⏱️ Answer quickly to get full points!"
        )
        
        return self.send_message_to_meeting(meeting_id, message)
    
    def test_connection(self) -> dict:
        """Test Zoom API connection"""
        token = self.get_access_token()
        
        if not token:
            return {
                "success": False,
                "message": "Failed to get access token",
                "configured": bool(self.client_id and self.client_secret and self.account_id)
            }
        
        try:
            # Test by getting user info
            url = "https://api.zoom.us/v2/users/me"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Zoom API connection successful",
                    "configured": True
                }
            else:
                return {
                    "success": False,
                    "message": f"API test failed: {response.status_code}",
                    "configured": True
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection test error: {str(e)}",
                "configured": True
            }

