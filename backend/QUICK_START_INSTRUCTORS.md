# 🚀 Quick Start Guide: Instructor & Course Management

## What's Been Created

I've implemented a complete instructor and course management system with the following features:

### ✅ Features Implemented

1. **Instructor Registration & Login**
   - Instructors can register with `role: "instructor"`
   - Secure login system
   - User data stored in `users` collection

2. **Course Management (Instructor Only)**
   - Create courses with detailed information
   - Update their own courses
   - Delete their own courses
   - View all their courses
   - Draft/Published/Archived status

3. **Course Browsing (Everyone)**
   - View all published courses
   - View courses by specific instructor
   - View course details

4. **Enrollment System**
   - Students can enroll in courses
   - Students can unenroll from courses
   - Track enrolled students per course

---

## 📁 Files Created/Modified

### New Files:
- `src/models/course.py` - Course database model
- `src/routers/course.py` - Course API endpoints
- `INSTRUCTOR_COURSE_API.md` - Complete API documentation
- `seed_instructors_courses.py` - Sample data seeder
- `test_api_example.py` - Example API test script

### Modified Files:
- `main.py` - Added course router
- `src/middleware/auth.py` - Enhanced authentication

---

## 🎯 How to Use

### Step 1: Start the Server

```bash
cd backend
python main.py
```

The server will start on `http://localhost:3001`

---

### Step 2: Seed Sample Data (Optional)

To populate the database with sample instructors and courses:

```bash
python seed_instructors_courses.py
```

This creates:
- 3 sample instructors
- 7 sample courses
- Test credentials (password: `password123` for all):
  - sarah.johnson@example.com
  - michael.chen@example.com
  - emily.rodriguez@example.com

---

### Step 3: Test the API

#### Option A: Using the Test Script

```bash
pip install requests  # if not already installed
python test_api_example.py
```

This will:
- Register an instructor
- Create a course
- Register a student
- Enroll student in course
- Show all API interactions

#### Option B: Using Postman/cURL

See `INSTRUCTOR_COURSE_API.md` for detailed endpoint documentation.

#### Option C: Using FastAPI Interactive Docs

Visit: `http://localhost:3001/docs`

---

## 📝 API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Register user (student/instructor)
- `POST /api/auth/login` - Login

### Courses
- `POST /api/courses/create` - Create course (instructor only)
- `GET /api/courses/` - Get all published courses
- `GET /api/courses/my-courses` - Get my courses (instructor only)
- `GET /api/courses/{id}` - Get course by ID
- `PUT /api/courses/{id}` - Update course (instructor only)
- `DELETE /api/courses/{id}` - Delete course (instructor only)
- `POST /api/courses/{id}/enroll` - Enroll in course
- `POST /api/courses/{id}/unenroll` - Unenroll from course
- `GET /api/courses/instructor/{id}` - Get courses by instructor

---

## 🔐 Authentication

For development, we use headers to simulate authentication:

```javascript
headers: {
  'x-user-id': 'user_id_from_login',
  'x-user-email': 'user@example.com'
}
```

**Important:** Include these headers in requests that require authentication.

---

## 💾 Database Collections

### users
```javascript
{
  firstName: string,
  lastName: string,
  email: string (unique),
  password: string (hashed),
  role: "student" | "instructor" | "admin",
  status: 0 | 1,  // 0=inactive, 1=active
  createdAt: datetime,
  updatedAt: datetime
}
```

### courses
```javascript
{
  title: string,
  description: string,
  instructorId: string,
  instructorName: string,
  instructorEmail: string,
  category: string,
  duration: string,
  level: "Beginner" | "Intermediate" | "Advanced",
  thumbnail: string,
  syllabus: [
    {
      week: number,
      title: string,
      topics: [string]
    }
  ],
  enrolledStudents: [string],  // array of user IDs
  maxStudents: number,
  status: "draft" | "published" | "archived",
  startDate: datetime,
  endDate: datetime,
  createdAt: datetime,
  updatedAt: datetime
}
```

---

## 🎓 Example: Complete Workflow

### 1. Register as Instructor

```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "instructor"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Save the returned `id` for next steps!**

### 3. Create a Course

```bash
curl -X POST http://localhost:3001/api/courses/create \
  -H "Content-Type: application/json" \
  -H "x-user-id: YOUR_USER_ID" \
  -H "x-user-email: john@example.com" \
  -d '{
    "title": "My First Course",
    "description": "Learn amazing things!",
    "category": "Programming",
    "level": "Beginner",
    "status": "published"
  }'
```

### 4. View Your Courses

```bash
curl http://localhost:3001/api/courses/my-courses \
  -H "x-user-id: YOUR_USER_ID"
```

---

## 🎨 Frontend Integration Tips

When building a React/Vue/Angular frontend:

### 1. Store User Data After Login

```javascript
// After successful login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

const data = await response.json();
if (data.success) {
  // Store user data
  localStorage.setItem('user', JSON.stringify(data.user));
}
```

### 2. Include Headers in Authenticated Requests

```javascript
const user = JSON.parse(localStorage.getItem('user'));

const response = await fetch('/api/courses/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-user-id': user.id,
    'x-user-email': user.email
  },
  body: JSON.stringify(courseData)
});
```

### 3. Conditional Rendering Based on Role

```javascript
{user.role === 'instructor' && (
  <button onClick={createCourse}>Create Course</button>
)}
```

---

## 🔧 Troubleshooting

### Server won't start
- Check MongoDB connection in `.env` file
- Ensure MongoDB is running

### Authentication errors
- Make sure you include `x-user-id` header
- Verify the user ID from login response

### Can't create course
- Ensure you're logged in as instructor
- Check that `role: "instructor"` was set during registration

### Course not appearing
- Check if status is `"published"` (only published courses show in public list)
- Draft courses only appear in `/api/courses/my-courses`

---

## 📚 Next Steps

1. ✅ Start the server
2. ✅ Run the seed script
3. ✅ Test with the example script
4. ✅ Read the full API documentation in `INSTRUCTOR_COURSE_API.md`
5. ✅ Build your frontend

---

## 🆘 Need Help?

- **Full API Docs:** See `INSTRUCTOR_COURSE_API.md`
- **Interactive API:** `http://localhost:3001/docs`
- **Test Script:** Run `python test_api_example.py`

---

## ✨ Features Available

- ✅ Instructor registration
- ✅ Instructor login
- ✅ Create courses
- ✅ Update courses
- ✅ Delete courses
- ✅ View courses
- ✅ Course enrollment
- ✅ Student management per course
- ✅ Draft/Published status
- ✅ Course categories & levels
- ✅ Syllabus management
- ✅ Student capacity limits

**Happy Teaching! 🎓**

