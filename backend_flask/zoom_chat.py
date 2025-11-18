"""
Zoom Chat API integration for sending messages to participants
Uses Server-to-Server OAuth for authentication
"""
import requests
import base64
import os
from datetime import datetime, timedelta


class ZoomChatAPI:
    """Zoom Chat API client with Server-to-Server OAuth"""
    
    def __init__(self):
        self.account_id = os.getenv('ZOOM_ACCOUNT_ID')
        self.client_id = os.getenv('ZOOM_CLIENT_ID')
        self.client_secret = os.getenv('ZOOM_CLIENT_SECRET')
        
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self):
        """
        Get OAuth access token using Server-to-Server OAuth
        
        Returns:
            str: Access token or None if failed
        """
        # Check if current token is still valid
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Validate credentials
        if not all([self.account_id, self.client_id, self.client_secret]):
            print("❌ Missing Zoom credentials in environment variables")
            return None
        
        try:
            # Prepare Basic Auth credentials
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Request new token
            url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}"
            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            print(f"🔑 Requesting Zoom access token...")
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                expires_in = data.get('expires_in', 3600)
                
                # Set expiration time (with 60 second buffer)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                
                print(f"✅ Access token obtained (expires in {expires_in}s)")
                return self.access_token
            else:
                print(f"❌ Failed to get access token: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting access token: {e}")
            return None
    
    def send_chat_message(self, user_id, message):
        """
        Send a direct chat message to a specific Zoom user
        
        Args:
            user_id (str): Zoom user ID or email
            message (str): Message to send
            
        Returns:
            dict: Response from Zoom API with success status
        """
        token = self.get_access_token()
        
        if not token:
            return {
                'success': False,
                'error': 'Failed to get access token'
            }
        
        try:
            url = f"https://api.zoom.us/v2/chat/users/{user_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "message": message
            }
            
            print(f"📤 Sending direct message to user: {user_id}")
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print(f"✅ Message sent successfully to {user_id}")
                return {
                    'success': True,
                    'user_id': user_id,
                    'status_code': response.status_code,
                    'response': response.json()
                }
            else:
                print(f"❌ Failed to send message to {user_id}: {response.status_code}")
                print(f"   Response: {response.text}")
                return {
                    'success': False,
                    'user_id': user_id,
                    'status_code': response.status_code,
                    'error': response.text
                }
                
        except Exception as e:
            print(f"❌ Error sending message to {user_id}: {e}")
            return {
                'success': False,
                'user_id': user_id,
                'error': str(e)
            }
    
    def send_meeting_chat_message(self, meeting_id, message):
        """
        Send a message to a Zoom meeting chat (requires Chatbot)
        
        Args:
            meeting_id (str): Zoom meeting ID
            message (str): Message to send
            
        Returns:
            dict: Response from Zoom API with success status
        """
        token = self.get_access_token()
        
        if not token:
            return {
                'success': False,
                'error': 'Failed to get access token'
            }
        
        bot_jid = os.getenv('ZOOM_BOT_JID', '')
        
        if not bot_jid:
            print("⚠️  ZOOM_BOT_JID not configured. Cannot send to meeting chat.")
            return {
                'success': False,
                'error': 'ZOOM_BOT_JID not configured'
            }
        
        try:
            # Use Chatbot API to send to meeting channel
            url = "https://api.zoom.us/v2/im/chat/messages"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Meeting channel JID format
            to_jid = f"{meeting_id}@conference.zoomgov.com"
            
            payload = {
                "robot_jid": bot_jid,
                "to_jid": to_jid,
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
            
            print(f"📤 Sending to meeting chat: {meeting_id}")
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                print(f"✅ Message sent to meeting chat successfully")
                return {
                    'success': True,
                    'meeting_id': meeting_id,
                    'status_code': response.status_code
                }
            else:
                print(f"❌ Failed to send to meeting: {response.status_code}")
                print(f"   Response: {response.text}")
                return {
                    'success': False,
                    'meeting_id': meeting_id,
                    'status_code': response.status_code,
                    'error': response.text
                }
                
        except Exception as e:
            print(f"❌ Error sending to meeting chat: {e}")
            return {
                'success': False,
                'meeting_id': meeting_id,
                'error': str(e)
            }
    
    def send_bulk_messages(self, user_ids, message):
        """
        Send the same message to multiple users
        
        Args:
            user_ids (list): List of Zoom user IDs
            message (str): Message to send
            
        Returns:
            dict: Summary of results
        """
        results = {
            'total': len(user_ids),
            'success': 0,
            'failed': 0,
            'responses': []
        }
        
        print(f"📨 Sending bulk messages to {len(user_ids)} users...")
        
        for user_id in user_ids:
            response = self.send_chat_message(user_id, message)
            results['responses'].append(response)
            
            if response.get('success'):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        print(f"✅ Bulk send complete: {results['success']}/{results['total']} successful")
        
        return results
    
    def test_connection(self):
        """
        Test Zoom API connection
        
        Returns:
            dict: Connection test results
        """
        token = self.get_access_token()
        
        if not token:
            return {
                'success': False,
                'message': 'Failed to get access token',
                'configured': bool(self.client_id and self.client_secret and self.account_id)
            }
        
        try:
            # Test by getting user info
            url = "https://api.zoom.us/v2/users/me"
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Zoom API connection successful',
                    'configured': True
                }
            else:
                return {
                    'success': False,
                    'message': f'API test failed: {response.status_code}',
                    'configured': True
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection test error: {str(e)}',
                'configured': True
            }


# Global Zoom Chat API instance
zoom_chat = ZoomChatAPI()


def get_zoom_chat():
    """
    Get the Zoom Chat API instance
    
    Returns:
        ZoomChatAPI: Zoom Chat API instance
    """
    return zoom_chat

