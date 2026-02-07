from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class ZoomParticipant(BaseModel):
    user_id: str
    user_name: str
    email: Optional[str] = None
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None
    duration: Optional[int] = None  # in seconds


class ZoomMeetingEvent(BaseModel):
    event: str  # meeting.started, meeting.ended, participant.joined, etc.
    event_ts: int  # timestamp
    payload: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "event": "meeting.started",
                "event_ts": 1697461200000,
                "payload": {
                    "account_id": "xxx",
                    "object": {
                        "id": "123456789",
                        "uuid": "xxx",
                        "host_id": "xxx",
                        "topic": "Learning Session",
                        "start_time": "2023-10-15T14:00:00Z"
                    }
                }
            }
        }


class ZoomWebhookVerification(BaseModel):
    plainToken: str
    encryptedToken: Optional[str] = None

