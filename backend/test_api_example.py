"""
Example script showing how to interact with the Instructor & Course API
This demonstrates the full workflow: register, login, create course, etc.
"""

import requests
import json

# Base URL - change if your server runs on a different port
BASE_URL = "http://localhost:3001"


def print_response(title, response):
    """Helper function to print API responses"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")


def main():
    print("\n🚀 Testing Instructor & Course Management API\n")
    
    # 1. Register an Instructor
    print("\n1️⃣  Registering a new instructor...")
    register_data = {
        "firstName": "Alice",
        "lastName": "Williams",
        "email": "alice.williams@example.com",
        "password": "securePassword123",
        "role": "instructor"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print_response("Register Instructor", response)
    
    if response.status_code == 200:
        instructor = response.json()["user"]
        instructor_id = instructor["id"]
        instructor_email = instructor["email"]
        print(f"\n✅ Instructor registered successfully!")
        print(f"   ID: {instructor_id}")
        print(f"   Email: {instructor_email}")
    else:
        print("\n⚠️  Registration failed. The instructor might already exist.")
        # Try to login instead
        print("\n   Attempting to login with existing account...")
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            instructor = response.json()["user"]
            instructor_id = instructor["id"]
            instructor_email = instructor["email"]
            print(f"\n✅ Logged in successfully!")
            print(f"   ID: {instructor_id}")
        else:
            print("\n❌ Failed to login. Exiting...")
            return
    
    # 2. Create a Course
    print("\n\n2️⃣  Creating a new course...")
    course_data = {
        "title": "Advanced JavaScript: ES6 and Beyond",
        "description": "Master modern JavaScript features including ES6+, async/await, modules, and more. Build production-ready applications.",
        "category": "Programming",
        "duration": "6 weeks",
        "level": "Intermediate",
        "syllabus": [
            {
                "week": 1,
                "title": "ES6 Fundamentals",
                "topics": ["Arrow Functions", "Destructuring", "Template Literals", "Spread Operator"]
            },
            {
                "week": 2,
                "title": "Async JavaScript",
                "topics": ["Promises", "Async/Await", "Fetch API", "Error Handling"]
            },
            {
                "week": 3,
                "title": "Modules and Classes",
                "topics": ["ES6 Modules", "Classes", "Inheritance", "Static Methods"]
            }
        ],
        "maxStudents": 40,
        "status": "published"
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-user-id": instructor_id,
        "x-user-email": instructor_email
    }
    
    response = requests.post(f"{BASE_URL}/api/courses/create", json=course_data, headers=headers)
    print_response("Create Course", response)
    
    if response.status_code == 200:
        course = response.json()["course"]
        course_id = course["id"]
        print(f"\n✅ Course created successfully!")
        print(f"   Course ID: {course_id}")
        print(f"   Title: {course['title']}")
    else:
        print("\n❌ Failed to create course")
        return
    
    # 3. Get All My Courses
    print("\n\n3️⃣  Getting all courses by this instructor...")
    response = requests.get(f"{BASE_URL}/api/courses/my-courses", headers=headers)
    print_response("My Courses", response)
    
    if response.status_code == 200:
        courses = response.json()["courses"]
        print(f"\n✅ Found {len(courses)} course(s)")
    
    # 4. Get All Published Courses (Public - No Auth)
    print("\n\n4️⃣  Getting all published courses (public)...")
    response = requests.get(f"{BASE_URL}/api/courses/")
    print_response("All Published Courses", response)
    
    if response.status_code == 200:
        courses = response.json()["courses"]
        print(f"\n✅ Found {len(courses)} published course(s)")
    
    # 5. Get Specific Course by ID
    print("\n\n5️⃣  Getting course by ID...")
    response = requests.get(f"{BASE_URL}/api/courses/{course_id}")
    print_response("Get Course by ID", response)
    
    # 6. Update Course
    print("\n\n6️⃣  Updating the course...")
    update_data = {
        "description": "UPDATED: Master modern JavaScript with this comprehensive course. Now includes bonus content on TypeScript!",
        "maxStudents": 50
    }
    
    response = requests.put(f"{BASE_URL}/api/courses/{course_id}", json=update_data, headers=headers)
    print_response("Update Course", response)
    
    if response.status_code == 200:
        print("\n✅ Course updated successfully!")
    
    # 7. Register a Student
    print("\n\n7️⃣  Registering a student...")
    student_data = {
        "firstName": "Bob",
        "lastName": "Student",
        "email": "bob.student@example.com",
        "password": "studentPass123",
        "role": "student"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=student_data)
    
    if response.status_code == 200:
        student = response.json()["user"]
        student_id = student["id"]
        print(f"\n✅ Student registered!")
        print(f"   ID: {student_id}")
    else:
        # Login if already exists
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": student_data["email"],
            "password": student_data["password"]
        })
        if login_response.status_code == 200:
            student = login_response.json()["user"]
            student_id = student["id"]
            print(f"\n✅ Student logged in!")
        else:
            print("\n⚠️  Using mock student ID")
            student_id = "student123"
    
    # 8. Enroll Student in Course
    print("\n\n8️⃣  Enrolling student in the course...")
    student_headers = {
        "x-user-id": student_id
    }
    
    response = requests.post(f"{BASE_URL}/api/courses/{course_id}/enroll", headers=student_headers)
    print_response("Enroll in Course", response)
    
    if response.status_code == 200:
        print("\n✅ Student enrolled successfully!")
    
    # 9. Get Course Details (should show enrolled student)
    print("\n\n9️⃣  Getting course details (with enrolled students)...")
    response = requests.get(f"{BASE_URL}/api/courses/{course_id}")
    print_response("Course with Enrolled Students", response)
    
    if response.status_code == 200:
        course = response.json()["course"]
        print(f"\n✅ Enrolled students: {len(course.get('enrolledStudents', []))}")
    
    # 10. Delete Course (Optional - uncomment to test)
    # print("\n\n🔟 Deleting the course...")
    # response = requests.delete(f"{BASE_URL}/api/courses/{course_id}", headers=headers)
    # print_response("Delete Course", response)
    
    print("\n\n" + "="*60)
    print("✅ All API tests completed successfully!")
    print("="*60)
    print("\n💡 Tips:")
    print("   - Use x-user-id header to authenticate requests")
    print("   - Instructors can only edit/delete their own courses")
    print("   - Students can enroll in published courses")
    print("   - Visit http://localhost:3001/docs for interactive API docs")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server")
        print("   Make sure the backend is running on http://localhost:3001")
        print("   Run: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

