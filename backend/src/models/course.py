from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from ..database.connection import get_database


class Course(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    instructorId: str
    instructorName: str
    instructorEmail: str
    category: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = "Beginner"  # Beginner, Intermediate, Advanced
    thumbnail: Optional[str] = None
    syllabus: Optional[List[dict]] = []
    enrolledStudents: Optional[List[str]] = []
    maxStudents: Optional[int] = None
    status: str = "draft"  # draft, published, archived
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction to Python Programming",
                "description": "Learn Python from scratch",
                "instructorId": "507f1f77bcf86cd799439011",
                "instructorName": "John Doe",
                "instructorEmail": "john@example.com",
                "category": "Programming",
                "duration": "8 weeks",
                "level": "Beginner",
                "status": "published"
            }
        }


class CourseModel:
    @staticmethod
    async def create(course_data: dict) -> dict:
        """Create a new course"""
        database = get_database()
        if database is None:
            raise Exception("Database not connected")
        
        course_data["createdAt"] = datetime.now()
        course_data["updatedAt"] = datetime.now()
        course_data["enrolledStudents"] = course_data.get("enrolledStudents", [])
        course_data["syllabus"] = course_data.get("syllabus", [])
        
        result = await database.courses.insert_one(course_data)
        course_data["id"] = str(result.inserted_id)
        
        # Remove _id to avoid serialization issues
        if "_id" in course_data:
            del course_data["_id"]
        return course_data

    @staticmethod
    async def find_by_id(course_id: str) -> Optional[dict]:
        """Find course by ID"""
        database = get_database()
        if database is None:
            return None
        try:
            course = await database.courses.find_one({"_id": ObjectId(course_id)})
            if course:
                course["id"] = str(course["_id"])
                del course["_id"]
            return course
        except Exception as e:
            print(f"Error finding course: {e}")
            return None

    @staticmethod
    async def find_by_instructor(instructor_id: str) -> List[dict]:
        """Find all courses by instructor"""
        database = get_database()
        if database is None:
            return []
        
        courses = []
        async for course in database.courses.find({"instructorId": instructor_id}):
            course["id"] = str(course["_id"])
            del course["_id"]
            courses.append(course)
        return courses

    @staticmethod
    async def find_all(filters: dict = None) -> List[dict]:
        """Find all courses with optional filters"""
        database = get_database()
        if database is None:
            return []
        
        query = filters if filters else {}
        courses = []
        async for course in database.courses.find(query):
            course["id"] = str(course["_id"])
            del course["_id"]
            courses.append(course)
        return courses

    @staticmethod
    async def update(course_id: str, update_data: dict) -> Optional[dict]:
        """Update course"""
        database = get_database()
        if database is None:
            return None
        
        update_data["updatedAt"] = datetime.now()
        
        try:
            result = await database.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": update_data}
            )
            
            if result.modified_count or result.matched_count:
                return await CourseModel.find_by_id(course_id)
            return None
        except Exception as e:
            print(f"Error updating course: {e}")
            return None

    @staticmethod
    async def delete(course_id: str) -> bool:
        """Delete course"""
        database = get_database()
        if database is None:
            return False
        
        try:
            result = await database.courses.delete_one({"_id": ObjectId(course_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting course: {e}")
            return False

    @staticmethod
    async def enroll_student(course_id: str, student_id: str) -> Optional[dict]:
        """Enroll a student in a course"""
        database = get_database()
        if database is None:
            return None
        
        try:
            # Check if student is already enrolled
            course = await CourseModel.find_by_id(course_id)
            if not course:
                return None
            
            enrolled = course.get("enrolledStudents", [])
            if student_id in enrolled:
                return course  # Already enrolled
            
            # Add student to enrolled list
            result = await database.courses.update_one(
                {"_id": ObjectId(course_id)},
                {
                    "$push": {"enrolledStudents": student_id},
                    "$set": {"updatedAt": datetime.now()}
                }
            )
            
            if result.modified_count:
                return await CourseModel.find_by_id(course_id)
            return None
        except Exception as e:
            print(f"Error enrolling student: {e}")
            return None

    @staticmethod
    async def unenroll_student(course_id: str, student_id: str) -> Optional[dict]:
        """Unenroll a student from a course"""
        database = get_database()
        if database is None:
            return None
        
        try:
            result = await database.courses.update_one(
                {"_id": ObjectId(course_id)},
                {
                    "$pull": {"enrolledStudents": student_id},
                    "$set": {"updatedAt": datetime.now()}
                }
            )
            
            if result.modified_count:
                return await CourseModel.find_by_id(course_id)
            return None
        except Exception as e:
            print(f"Error unenrolling student: {e}")
            return None

