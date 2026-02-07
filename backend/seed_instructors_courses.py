"""
Seed script to populate the database with sample instructors and courses
Run this script to create test data: python seed_instructors_courses.py
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.database.connection import connect_to_mongo, close_mongo_connection, get_database
from src.models.user import UserModel
from src.models.course import CourseModel
import hashlib
from datetime import datetime, timedelta


def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


async def seed_data():
    """Seed the database with sample instructors and courses"""
    print("🌱 Starting database seeding...")
    
    # Connect to MongoDB
    await connect_to_mongo()
    database = get_database()
    
    if database is None:
        print("❌ Failed to connect to database")
        return
    
    # Sample Instructors
    instructors_data = [
        {
            "firstName": "Sarah",
            "lastName": "Johnson",
            "email": "sarah.johnson@example.com",
            "password": hash_password("password123"),
            "role": "instructor",
            "status": 1
        },
        {
            "firstName": "Michael",
            "lastName": "Chen",
            "email": "michael.chen@example.com",
            "password": hash_password("password123"),
            "role": "instructor",
            "status": 1
        },
        {
            "firstName": "Emily",
            "lastName": "Rodriguez",
            "email": "emily.rodriguez@example.com",
            "password": hash_password("password123"),
            "role": "instructor",
            "status": 1
        }
    ]
    
    print("\n📚 Creating instructors...")
    instructors = []
    
    for instructor_data in instructors_data:
        # Check if instructor already exists
        existing = await UserModel.find_by_email(instructor_data["email"])
        if existing:
            print(f"  ⚠️  Instructor {instructor_data['email']} already exists")
            instructors.append(existing)
        else:
            instructor = await UserModel.create(instructor_data)
            instructors.append(instructor)
            print(f"  ✅ Created instructor: {instructor['firstName']} {instructor['lastName']} ({instructor['email']})")
    
    # Sample Courses
    courses_data = [
        # Sarah's courses
        {
            "title": "Introduction to Python Programming",
            "description": "Learn Python from scratch with hands-on projects. This comprehensive course covers Python basics, data structures, OOP, and more. Perfect for beginners!",
            "instructorId": instructors[0]["id"],
            "instructorName": f"{instructors[0]['firstName']} {instructors[0]['lastName']}",
            "instructorEmail": instructors[0]["email"],
            "category": "Programming",
            "duration": "8 weeks",
            "level": "Beginner",
            "syllabus": [
                {
                    "week": 1,
                    "title": "Python Basics",
                    "topics": ["Variables and Data Types", "Operators", "Input/Output"]
                },
                {
                    "week": 2,
                    "title": "Control Flow",
                    "topics": ["If-Else Statements", "Loops", "Break and Continue"]
                },
                {
                    "week": 3,
                    "title": "Functions",
                    "topics": ["Defining Functions", "Parameters", "Return Values", "Lambda Functions"]
                },
                {
                    "week": 4,
                    "title": "Data Structures",
                    "topics": ["Lists", "Tuples", "Dictionaries", "Sets"]
                }
            ],
            "maxStudents": 50,
            "status": "published",
            "startDate": datetime.now(),
            "endDate": datetime.now() + timedelta(weeks=8)
        },
        {
            "title": "Advanced Python: Data Science & Machine Learning",
            "description": "Master data science with Python. Learn NumPy, Pandas, Matplotlib, and Scikit-learn for data analysis and machine learning.",
            "instructorId": instructors[0]["id"],
            "instructorName": f"{instructors[0]['firstName']} {instructors[0]['lastName']}",
            "instructorEmail": instructors[0]["email"],
            "category": "Data Science",
            "duration": "10 weeks",
            "level": "Advanced",
            "syllabus": [
                {
                    "week": 1,
                    "title": "NumPy Fundamentals",
                    "topics": ["Arrays", "Operations", "Broadcasting"]
                },
                {
                    "week": 2,
                    "title": "Pandas for Data Analysis",
                    "topics": ["DataFrames", "Data Cleaning", "Aggregation"]
                }
            ],
            "maxStudents": 30,
            "status": "published",
            "startDate": datetime.now() + timedelta(days=7),
            "endDate": datetime.now() + timedelta(weeks=10, days=7)
        },
        # Michael's courses
        {
            "title": "Web Development Bootcamp: HTML, CSS & JavaScript",
            "description": "Complete web development course covering front-end fundamentals. Build real-world projects and become job-ready!",
            "instructorId": instructors[1]["id"],
            "instructorName": f"{instructors[1]['firstName']} {instructors[1]['lastName']}",
            "instructorEmail": instructors[1]["email"],
            "category": "Web Development",
            "duration": "12 weeks",
            "level": "Beginner",
            "syllabus": [
                {
                    "week": 1,
                    "title": "HTML Basics",
                    "topics": ["Tags", "Attributes", "Forms", "Semantic HTML"]
                },
                {
                    "week": 2,
                    "title": "CSS Fundamentals",
                    "topics": ["Selectors", "Box Model", "Flexbox", "Grid"]
                },
                {
                    "week": 3,
                    "title": "JavaScript Essentials",
                    "topics": ["Variables", "Functions", "DOM Manipulation", "Events"]
                }
            ],
            "maxStudents": 100,
            "status": "published",
            "startDate": datetime.now(),
            "endDate": datetime.now() + timedelta(weeks=12)
        },
        {
            "title": "React.js Masterclass",
            "description": "Master React.js from beginner to advanced. Learn hooks, context, Redux, and build production-ready applications.",
            "instructorId": instructors[1]["id"],
            "instructorName": f"{instructors[1]['firstName']} {instructors[1]['lastName']}",
            "instructorEmail": instructors[1]["email"],
            "category": "Web Development",
            "duration": "8 weeks",
            "level": "Intermediate",
            "syllabus": [
                {
                    "week": 1,
                    "title": "React Fundamentals",
                    "topics": ["Components", "Props", "State", "JSX"]
                },
                {
                    "week": 2,
                    "title": "React Hooks",
                    "topics": ["useState", "useEffect", "useContext", "Custom Hooks"]
                }
            ],
            "maxStudents": 40,
            "status": "published",
            "startDate": datetime.now() + timedelta(days=14),
            "endDate": datetime.now() + timedelta(weeks=8, days=14)
        },
        # Emily's courses
        {
            "title": "Digital Marketing Fundamentals",
            "description": "Learn digital marketing from scratch. Master SEO, social media marketing, email marketing, and analytics.",
            "instructorId": instructors[2]["id"],
            "instructorName": f"{instructors[2]['firstName']} {instructors[2]['lastName']}",
            "instructorEmail": instructors[2]["email"],
            "category": "Marketing",
            "duration": "6 weeks",
            "level": "Beginner",
            "syllabus": [
                {
                    "week": 1,
                    "title": "Introduction to Digital Marketing",
                    "topics": ["Marketing Basics", "Digital Channels", "Consumer Behavior"]
                },
                {
                    "week": 2,
                    "title": "SEO Fundamentals",
                    "topics": ["Keywords", "On-Page SEO", "Link Building"]
                }
            ],
            "maxStudents": 60,
            "status": "published",
            "startDate": datetime.now(),
            "endDate": datetime.now() + timedelta(weeks=6)
        },
        {
            "title": "UI/UX Design Principles",
            "description": "Master the art of user interface and user experience design. Learn design thinking, wireframing, prototyping, and user testing.",
            "instructorId": instructors[2]["id"],
            "instructorName": f"{instructors[2]['firstName']} {instructors[2]['lastName']}",
            "instructorEmail": instructors[2]["email"],
            "category": "Design",
            "duration": "8 weeks",
            "level": "Intermediate",
            "syllabus": [
                {
                    "week": 1,
                    "title": "Design Thinking",
                    "topics": ["User Research", "Personas", "Journey Maps"]
                },
                {
                    "week": 2,
                    "title": "Wireframing",
                    "topics": ["Low-Fidelity Wireframes", "Tools", "Best Practices"]
                }
            ],
            "maxStudents": 35,
            "status": "published",
            "startDate": datetime.now() + timedelta(days=7),
            "endDate": datetime.now() + timedelta(weeks=8, days=7)
        },
        {
            "title": "Mobile App Development with Flutter",
            "description": "Build beautiful cross-platform mobile apps with Flutter and Dart. From basics to publishing on app stores.",
            "instructorId": instructors[1]["id"],
            "instructorName": f"{instructors[1]['firstName']} {instructors[1]['lastName']}",
            "instructorEmail": instructors[1]["email"],
            "category": "Mobile Development",
            "duration": "10 weeks",
            "level": "Intermediate",
            "syllabus": [
                {
                    "week": 1,
                    "title": "Flutter Basics",
                    "topics": ["Widgets", "Layouts", "Navigation"]
                },
                {
                    "week": 2,
                    "title": "State Management",
                    "topics": ["setState", "Provider", "Riverpod"]
                }
            ],
            "maxStudents": 25,
            "status": "draft",
            "startDate": datetime.now() + timedelta(days=30),
            "endDate": datetime.now() + timedelta(weeks=10, days=30)
        }
    ]
    
    print("\n📖 Creating courses...")
    created_courses = 0
    
    for course_data in courses_data:
        try:
            course = await CourseModel.create(course_data)
            created_courses += 1
            status_icon = "🟢" if course["status"] == "published" else "🟡"
            print(f"  {status_icon} Created course: {course['title']} ({course['level']}) - {course['status']}")
        except Exception as e:
            print(f"  ❌ Failed to create course: {course_data['title']} - {str(e)}")
    
    print(f"\n✅ Seeding complete!")
    print(f"   - Created {len(instructors)} instructors")
    print(f"   - Created {created_courses} courses")
    print(f"\n📝 Test Credentials:")
    print("   Email: sarah.johnson@example.com | Password: password123")
    print("   Email: michael.chen@example.com | Password: password123")
    print("   Email: emily.rodriguez@example.com | Password: password123")
    
    # Close connection
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_data())

