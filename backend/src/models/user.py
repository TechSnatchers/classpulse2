from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from bson import ObjectId
from ..database.connection import get_database


class User(BaseModel):
    id: Optional[str] = None
    firstName: str
    lastName: str
    email: EmailStr
    password: str  # Should be hashed in production
    role: str  # 'student', 'instructor', 'admin'
    status: int = 0  # 0 = pending, 1 = active
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "password": "hashed_password",
                "role": "student",
                "status": 1
            }
        }


class UserModel:
    @staticmethod
    async def find_by_email(email: str) -> Optional[dict]:
        """Find user by email"""
        database = get_database()
        if database is None:
            return None
        user = await database.users.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user

    @staticmethod
    async def find_by_id(user_id: str) -> Optional[dict]:
        """Find user by ID"""
        database = get_database()
        if database is None:
            return None
        try:
            user = await database.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                del user["_id"]
            return user
        except:
            return None

    @staticmethod
    async def create(user_data: dict) -> dict:
        """Create a new user"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")
        
        user_data["createdAt"] = datetime.now()
        user_data["updatedAt"] = datetime.now()
        
        result = await database.users.insert_one(user_data)
        user_data["id"] = str(result.inserted_id)
        # Remove _id to avoid serialization issues
        if "_id" in user_data:
            del user_data["_id"]
        return user_data

    @staticmethod
    async def update(user_id: str, update_data: dict) -> Optional[dict]:
        """Update user"""
        database = get_database()
        if database is None:
            return None
        
        update_data["updatedAt"] = datetime.now()
        result = await database.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await UserModel.find_by_id(user_id)
        return None

    @staticmethod
    async def delete(user_id: str) -> bool:
        """Delete user"""
        database = get_database()
        if database is None:
            return False
        
        result = await database.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

