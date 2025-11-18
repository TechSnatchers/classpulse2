from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from ..database.connection import get_database
import secrets


class LiveQuestionSession(BaseModel):
    """Model for live question sessions triggered in Zoom meetings"""
    id: Optional[str] = None
    sessionToken: str  # Unique token for accessing the question
    questionId: str
    question: str
    options: List[str]
    correctAnswer: int
    instructorId: str
    instructorName: str
    zoomMeetingId: Optional[str] = None
    courseId: Optional[str] = None
    status: str = "active"  # active, completed, expired
    timeLimit: int = 30  # seconds
    triggeredAt: datetime
    expiresAt: datetime
    responses: List[str] = []  # List of response IDs
    totalResponses: int = 0
    correctResponses: int = 0
    incorrectResponses: int = 0
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "sessionToken": "abc123def456",
                "questionId": "507f1f77bcf86cd799439011",
                "question": "What is Python?",
                "options": ["A language", "A snake", "Both"],
                "correctAnswer": 2,
                "instructorId": "instructor_id",
                "zoomMeetingId": "123456789",
                "status": "active",
                "timeLimit": 30
            }
        }


class LiveQuestionSessionModel:
    @staticmethod
    def generate_session_token() -> str:
        """Generate a unique session token"""
        return secrets.token_urlsafe(16)

    @staticmethod
    async def create(session_data: dict) -> dict:
        """Create a new live question session"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")
        
        # Generate unique token if not provided
        if "sessionToken" not in session_data:
            session_data["sessionToken"] = LiveQuestionSessionModel.generate_session_token()
        
        session_data["createdAt"] = datetime.now()
        session_data["updatedAt"] = datetime.now()
        session_data["responses"] = []
        session_data["totalResponses"] = 0
        session_data["correctResponses"] = 0
        session_data["incorrectResponses"] = 0
        
        result = await database.live_question_sessions.insert_one(session_data)
        session_data["id"] = str(result.inserted_id)
        
        if "_id" in session_data:
            del session_data["_id"]
        return session_data

    @staticmethod
    async def find_by_id(session_id: str) -> Optional[dict]:
        """Find session by ID"""
        database = get_database()
        if database is None:
            return None
        try:
            session = await database.live_question_sessions.find_one({"_id": ObjectId(session_id)})
            if session:
                session["id"] = str(session["_id"])
                del session["_id"]
            return session
        except Exception as e:
            print(f"Error finding session: {e}")
            return None

    @staticmethod
    async def find_by_token(token: str) -> Optional[dict]:
        """Find session by token"""
        database = get_database()
        if database is None:
            return None
        
        session = await database.live_question_sessions.find_one({"sessionToken": token})
        if session:
            session["id"] = str(session["_id"])
            del session["_id"]
        return session

    @staticmethod
    async def find_active_sessions(instructor_id: str = None) -> List[dict]:
        """Find all active sessions (optionally filtered by instructor)"""
        database = get_database()
        if database is None:
            return []
        
        query = {"status": "active"}
        if instructor_id:
            query["instructorId"] = instructor_id
        
        sessions = []
        async for session in database.live_question_sessions.find(query).sort("triggeredAt", -1):
            session["id"] = str(session["_id"])
            del session["_id"]
            sessions.append(session)
        return sessions

    @staticmethod
    async def find_by_meeting_id(meeting_id: str) -> List[dict]:
        """Find all sessions for a specific Zoom meeting"""
        database = get_database()
        if database is None:
            return []
        
        sessions = []
        async for session in database.live_question_sessions.find({"zoomMeetingId": meeting_id}).sort("triggeredAt", -1):
            session["id"] = str(session["_id"])
            del session["_id"]
            sessions.append(session)
        return sessions

    @staticmethod
    async def update(session_id: str, update_data: dict) -> Optional[dict]:
        """Update session"""
        database = get_database()
        if database is None:
            return None
        
        update_data["updatedAt"] = datetime.now()
        
        try:
            result = await database.live_question_sessions.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": update_data}
            )
            
            if result.modified_count or result.matched_count:
                return await LiveQuestionSessionModel.find_by_id(session_id)
            return None
        except Exception as e:
            print(f"Error updating session: {e}")
            return None

    @staticmethod
    async def add_response(session_id: str, response_id: str, is_correct: bool) -> Optional[dict]:
        """Add a response to the session and update stats"""
        database = get_database()
        if database is None:
            return None
        
        try:
            # Increment counters
            increment_data = {"totalResponses": 1}
            if is_correct:
                increment_data["correctResponses"] = 1
            else:
                increment_data["incorrectResponses"] = 1
            
            result = await database.live_question_sessions.update_one(
                {"_id": ObjectId(session_id)},
                {
                    "$push": {"responses": response_id},
                    "$inc": increment_data,
                    "$set": {"updatedAt": datetime.now()}
                }
            )
            
            if result.modified_count:
                return await LiveQuestionSessionModel.find_by_id(session_id)
            return None
        except Exception as e:
            print(f"Error adding response: {e}")
            return None

    @staticmethod
    async def complete_session(session_id: str) -> bool:
        """Mark session as completed"""
        database = get_database()
        if database is None:
            return False
        
        try:
            result = await database.live_question_sessions.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"status": "completed", "updatedAt": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error completing session: {e}")
            return False

    @staticmethod
    async def expire_old_sessions() -> int:
        """Expire sessions that have passed their expiry time"""
        database = get_database()
        if database is None:
            return 0
        
        try:
            result = await database.live_question_sessions.update_many(
                {
                    "status": "active",
                    "expiresAt": {"$lt": datetime.now()}
                },
                {"$set": {"status": "expired", "updatedAt": datetime.now()}}
            )
            return result.modified_count
        except Exception as e:
            print(f"Error expiring sessions: {e}")
            return 0

