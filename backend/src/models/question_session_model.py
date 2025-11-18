from datetime import datetime
from typing import Optional
from ..database.connection import get_database


class QuestionSessionModel:
    @staticmethod
    async def activate(session_id: str, mode: str = "individual") -> dict:
        """Mark a session as having active personalized questions and increment version"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")

        session_doc = await database.question_sessions.find_one({"sessionId": session_id})
        current_version = session_doc.get("version", 0) + 1 if session_doc else 1

        result = await database.question_sessions.update_one(
            {"sessionId": session_id},
            {
                "$set": {
                    "sessionId": session_id,
                    "mode": mode,
                    "active": True,
                    "version": current_version,
                    "updatedAt": datetime.utcnow()
                },
                "$setOnInsert": {
                    "createdAt": datetime.utcnow()
                }
            },
            upsert=True
        )
        return {
            "matched": result.matched_count,
            "upserted": result.upserted_id is not None,
            "version": current_version
        }

    @staticmethod
    async def deactivate(session_id: str) -> bool:
        """Deactivate personalized questions for a session"""
        database = get_database()
        if database is None:
            return False

        result = await database.question_sessions.update_one(
            {"sessionId": session_id},
            {"$set": {"active": False, "updatedAt": datetime.utcnow()}}
        )
        return result.modified_count > 0

    @staticmethod
    async def is_active(session_id: str) -> bool:
        """Check if a session currently has personalized questions active"""
        database = get_database()
        if database is None:
            return False

        session_doc = await database.question_sessions.find_one({"sessionId": session_id})
        if not session_doc:
            return False
        return bool(session_doc.get("active"))

    @staticmethod
    async def get_state(session_id: str) -> Optional[dict]:
        """Return session trigger state"""
        database = get_database()
        if database is None:
            return None

        session_doc = await database.question_sessions.find_one({"sessionId": session_id})
        return session_doc

