from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizAnswer(BaseModel):
    questionId: str
    answerIndex: int
    timeTaken: float  # in seconds
    studentId: str
    sessionId: str
    timestamp: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "questionId": "1",
                "answerIndex": 1,
                "timeTaken": 5.5,
                "studentId": "student123",
                "sessionId": "session456",
            }
        }

