# Instructor and Course Management API Documentation

## Overview
This system allows instructors to register, login, and create/manage courses. Students can browse and enroll in courses.

## Database Collections
- **users**: Stores all users (students, instructors, admins)
- **courses**: Stores all courses created by instructors

---

## 1. Instructor Registration

### Register as Instructor
**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.instructor@example.com",
  "password": "securePassword123",
  "role": "instructor"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.instructor@example.com",
    "role": "instructor",
    "status": 1,
    "createdAt": "2023-11-15T10:30:00.000Z",
    "updatedAt": "2023-11-15T10:30:00.000Z"
  }
}
```

---

## 2. Instructor Login

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "john.instructor@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.instructor@example.com",
    "role": "instructor",
    "status": 1,
    "createdAt": "2023-11-15T10:30:00.000Z",
    "updatedAt": "2023-11-15T10:30:00.000Z"
  }
}
```

**Note:** After login, use the returned user `id` and `email` in request headers for authenticated endpoints.

---

## 3. Course Management

### 3.1 Create Course (Instructor Only)

**Endpoint:** `POST /api/courses/create`

**Headers:**
```
x-user-id: 507f1f77bcf86cd799439011
x-user-email: john.instructor@example.com
```

**Request Body:**
```json
{
  "title": "Introduction to Python Programming",
  "description": "Learn Python from scratch with hands-on projects and real-world examples.",
  "category": "Programming",
  "duration": "8 weeks",
  "level": "Beginner",
  "thumbnail": "https://example.com/python-course.jpg",
  "syllabus": [
    {
      "week": 1,
      "title": "Python Basics",
      "topics": ["Variables", "Data Types", "Operators"]
    },
    {
      "week": 2,
      "title": "Control Flow",
      "topics": ["If Statements", "Loops", "Functions"]
    }
  ],
  "maxStudents": 50,
  "status": "published",
  "startDate": "2024-01-15T00:00:00.000Z",
  "endDate": "2024-03-15T00:00:00.000Z"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Course created successfully",
  "course": {
    "id": "507f1f77bcf86cd799439012",
    "title": "Introduction to Python Programming",
    "description": "Learn Python from scratch...",
    "instructorId": "507f1f77bcf86cd799439011",
    "instructorName": "John Doe",
    "instructorEmail": "john.instructor@example.com",
    "category": "Programming",
    "duration": "8 weeks",
    "level": "Beginner",
    "status": "published",
    "enrolledStudents": [],
    "createdAt": "2023-11-15T10:35:00.000Z",
    "updatedAt": "2023-11-15T10:35:00.000Z"
  }
}
```

---

### 3.2 Get All Published Courses

**Endpoint:** `GET /api/courses/`

**No authentication required**

**Response:**
```json
{
  "success": true,
  "count": 5,
  "courses": [
    {
      "id": "507f1f77bcf86cd799439012",
      "title": "Introduction to Python Programming",
      "description": "Learn Python from scratch...",
      "instructorName": "John Doe",
      "category": "Programming",
      "level": "Beginner",
      "status": "published"
    }
  ]
}
```

---

### 3.3 Get My Courses (Instructor Only)

**Endpoint:** `GET /api/courses/my-courses`

**Headers:**
```
x-user-id: 507f1f77bcf86cd799439011
```

**Response:** Returns all courses created by the authenticated instructor (including drafts).

---

### 3.4 Get Course by ID

**Endpoint:** `GET /api/courses/{course_id}`

**Example:** `GET /api/courses/507f1f77bcf86cd799439012`

**Response:**
```json
{
  "success": true,
  "course": {
    "id": "507f1f77bcf86cd799439012",
    "title": "Introduction to Python Programming",
    "description": "Learn Python from scratch...",
    "instructorId": "507f1f77bcf86cd799439011",
    "instructorName": "John Doe",
    "enrolledStudents": ["student_id_1", "student_id_2"]
  }
}
```

---

### 3.5 Update Course (Instructor Only)

**Endpoint:** `PUT /api/courses/{course_id}`

**Headers:**
```
x-user-id: 507f1f77bcf86cd799439011
```

**Request Body:** (Only include fields you want to update)
```json
{
  "title": "Advanced Python Programming",
  "description": "Updated description",
  "status": "published"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Course updated successfully",
  "course": { ... }
}
```

**Note:** Instructors can only update their own courses.

---

### 3.6 Delete Course (Instructor Only)

**Endpoint:** `DELETE /api/courses/{course_id}`

**Headers:**
```
x-user-id: 507f1f77bcf86cd799439011
```

**Response:**
```json
{
  "success": true,
  "message": "Course deleted successfully"
}
```

**Note:** Instructors can only delete their own courses.

---

### 3.7 Enroll in Course (Student/Instructor)

**Endpoint:** `POST /api/courses/{course_id}/enroll`

**Headers:**
```
x-user-id: student_id_here
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully enrolled in course",
  "course": { ... }
}
```

---

### 3.8 Unenroll from Course

**Endpoint:** `POST /api/courses/{course_id}/unenroll`

**Headers:**
```
x-user-id: student_id_here
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully unenrolled from course",
  "course": { ... }
}
```

---

### 3.9 Get Courses by Instructor

**Endpoint:** `GET /api/courses/instructor/{instructor_id}`

**Example:** `GET /api/courses/instructor/507f1f77bcf86cd799439011`

**Response:** Returns all published courses by a specific instructor.

---

## Course Status Types

- **draft**: Course is being created but not visible to students
- **published**: Course is live and students can enroll
- **archived**: Course is no longer available for new enrollments

---

## Course Levels

- **Beginner**: For beginners with no prior knowledge
- **Intermediate**: Requires some basic knowledge
- **Advanced**: For experienced learners

---

## User Roles

- **student**: Can browse and enroll in courses
- **instructor**: Can create, manage courses, and view all users
- **admin**: Full access to all features

---

## Testing with cURL or Postman

### Example 1: Register an Instructor
```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jane@example.com",
    "password": "password123",
    "role": "instructor"
  }'
```

### Example 2: Create a Course
```bash
curl -X POST http://localhost:3001/api/courses/create \
  -H "Content-Type: application/json" \
  -H "x-user-id: YOUR_USER_ID_HERE" \
  -H "x-user-email: jane@example.com" \
  -d '{
    "title": "Web Development Bootcamp",
    "description": "Complete web development course",
    "category": "Web Development",
    "level": "Intermediate",
    "status": "published"
  }'
```

### Example 3: Get All Courses
```bash
curl http://localhost:3001/api/courses/
```

---

## Frontend Integration

When building a frontend, you should:

1. **Store user data after login** (in localStorage or state management)
2. **Include user headers** in authenticated requests:
   ```javascript
   const headers = {
     'Content-Type': 'application/json',
     'x-user-id': user.id,
     'x-user-email': user.email
   };
   ```

3. **Check user role** to show/hide instructor features:
   ```javascript
   if (user.role === 'instructor') {
     // Show "Create Course" button
     // Show "My Courses" link
   }
   ```

---

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "firstName": "string",
  "lastName": "string",
  "email": "string (unique)",
  "password": "string (hashed)",
  "role": "student | instructor | admin",
  "status": 0 | 1,
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Courses Collection
```json
{
  "_id": ObjectId,
  "title": "string",
  "description": "string",
  "instructorId": "string",
  "instructorName": "string",
  "instructorEmail": "string",
  "category": "string",
  "duration": "string",
  "level": "Beginner | Intermediate | Advanced",
  "thumbnail": "string",
  "syllabus": [
    {
      "week": "number",
      "title": "string",
      "topics": ["string"]
    }
  ],
  "enrolledStudents": ["string"],
  "maxStudents": "number",
  "status": "draft | published | archived",
  "startDate": "datetime",
  "endDate": "datetime",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message here"
}
```

Common HTTP Status Codes:
- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

---

## Next Steps

1. Start the backend server: `python main.py`
2. Register an instructor account
3. Login with the instructor account
4. Create a course using the instructor's ID from login response
5. View the course in the database or via GET endpoints

For production, you should:
- Implement proper JWT authentication
- Add password validation rules
- Add email verification
- Implement file upload for course thumbnails
- Add pagination for course listings
- Add search and filter functionality

