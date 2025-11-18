from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from ..database.connection import get_database


class QuestionResponse(BaseModel):
    """Model for student responses to live questions"""
    id: Optional[str] = None
    sessionId: str  # Reference to LiveQuestionSession
    sessionToken: str
    questionId: str
    studentId: Optional[str] = None
    studentName: Optional[str] = None
    studentEmail: Optional[str] = None
    zoomUserId: Optional[str] = None
    selectedAnswer: int  # Index of selected option
    isCorrect: bool
    responseTime: float  # Time taken to answer in seconds
    submittedAt: datetime
    ipAddress: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "sessionId": "507f1f77bcf86cd799439011",
                "sessionToken": "abc123def456",
                "questionId": "507f1f77bcf86cd799439012",
                "studentName": "John Doe",
                "selectedAnswer": 1,
                "isCorrect": True,
                "responseTime": 12.5
            }
        }


class QuestionResponseModel:
    @staticmethod
    async def create(response_data: dict) -> dict:
        """Create a new question response"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")
        
        response_data["createdAt"] = datetime.now()
        response_data["submittedAt"] = response_data.get("submittedAt", datetime.now())
        
        result = await database.question_responses.insert_one(response_data)
        response_data["id"] = str(result.inserted_id)
        
        if "_id" in response_data:
            del response_data["_id"]
        return response_data

    @staticmethod
    async def find_by_id(response_id: str) -> Optional[dict]:
        """Find response by ID"""
        database = get_database()
        if database is None:
            return None
        try:
            response = await database.question_responses.find_one({"_id": ObjectId(response_id)})
            if response:
                response["id"] = str(response["_id"])
                del response["_id"]
            return response
        except Exception as e:
            print(f"Error finding response: {e}")
            return None

    @staticmethod
    async def find_by_session(session_id: str) -> list:
        """Find all responses for a session"""
        database = get_database()
        if database is None:
            return []
        
        responses = []
        async for response in database.question_responses.find({"sessionId": session_id}).sort("submittedAt", 1):
            response["id"] = str(response["_id"])
            del response["_id"]
            responses.append(response)
        return responses

    @staticmethod
    async def find_by_student_and_session(student_identifier: str, session_id: str) -> Optional[dict]:
        """Check if student has already responded to this session"""
        database = get_database()
        if database is None:
            return None
        
        # Try to find by multiple student identifiers
        query = {
            "sessionId": session_id,
            "$or": [
                {"studentId": student_identifier},
                {"studentEmail": student_identifier},
                {"zoomUserId": student_identifier},
                {"studentName": student_identifier}
            ]
        }
        
        response = await database.question_responses.find_one(query)
        if response:
            response["id"] = str(response["_id"])
            del response["_id"]
        return response

    @staticmethod
    async def get_session_statistics(session_id: str) -> Dict[str, Any]:
        """Get statistics for a session"""
        database = get_database()
        if database is None:
            return {}
        
        responses = await QuestionResponseModel.find_by_session(session_id)
        
        if not responses:
            return {
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "averageResponseTime": 0,
                "fastestResponse": 0,
                "slowestResponse": 0
            }
        
        correct = sum(1 for r in responses if r.get("isCorrect"))
        incorrect = len(responses) - correct
        response_times = [r.get("responseTime", 0) for r in responses]
        
        return {
            "total": len(responses),
            "correct": correct,
            "incorrect": incorrect,
            "accuracy": (correct / len(responses) * 100) if responses else 0,
            "averageResponseTime": sum(response_times) / len(response_times) if response_times else 0,
            "fastestResponse": min(response_times) if response_times else 0,
            "slowestResponse": max(response_times) if response_times else 0
        }

    @staticmethod
    async def get_live_responses(session_id: str, limit: int = 50) -> list:
        """Get recent responses for live dashboard"""
        database = get_database()
        if database is None:
            return []
        
        responses = []
        async for response in database.question_responses.find(
            {"sessionId": session_id}
        ).sort("submittedAt", -1).limit(limit):
            response["id"] = str(response["_id"])
            del response["_id"]
            responses.append(response)
        return responses

