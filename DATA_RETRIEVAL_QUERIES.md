# Data Retrieval & Mutation Queries — ClassPulse Backend

This document lists all MongoDB data retrieval and write/update/delete queries used across the ClassPulse backend, grouped by collection.

---

## 1. Users Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.users.find_one({"email": email})` | Find user by email address | `models/user.py` → `UserModel.find_by_email()` |
| 2 | `db.users.find_one({"_id": ObjectId(user_id)})` | Find user by MongoDB ObjectId | `models/user.py` → `UserModel.find_by_id()` |
| 3 | `db.users.find_one({"verificationToken": token})` | Find user by email verification token | `routers/auth.py` → `verify_email()` |
| 4 | `db.users.find_one({"resetPasswordToken": token})` | Find user by password reset token | `routers/auth.py` → `reset_password()` |
| 5 | `db.users.find()` | Get all registered users (admin only) | `routers/auth.py` → `get_all_users()` |
| 6 | `db.users.find({"_id": {"$in": obj_ids}}, {"firstName": 1, "lastName": 1, "email": 1})` | Fetch user names and emails by list of IDs | `services/feedback_service.py` → `_fetch_raw_data()` |

---

## 2. Sessions Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.sessions.find_one({"_id": ObjectId(session_id)})` | Get session by ID | `routers/session.py` — used in multiple endpoints |
| 2 | `db.sessions.find({"instructorId": instructor_id}).sort("date", -1)` | All sessions by instructor, newest first | `routers/session.py` → `get_sessions()` |
| 3 | `db.sessions.find().sort("date", -1)` | All sessions (admin view), newest first | `routers/session.py` → `get_sessions()` |
| 4 | `db.sessions.find({"courseId": {"$in": enrolled_course_ids}}).sort("date", -1)` | Sessions for courses a student is enrolled in | `routers/session.py` → `get_sessions()` |
| 5 | `db.sessions.find({"isStandalone": True, "enrolledStudents": user_id})` | Standalone sessions where student is enrolled | `routers/session.py` → `get_sessions()` |
| 6 | `db.sessions.find({"courseId": course_id}).sort("date", -1)` | Sessions for a specific course | `routers/session.py` → `get_sessions_by_course()` |
| 7 | `db.sessions.find({"instructorId": instructor_id}).sort("date", -1)` | Instructor sessions with cluster question counts | `routers/session.py` → `get_previous_sessions_with_cluster_questions()` |
| 8 | `db.sessions.find({"instructorId": instructor_id}, {"_id": 1})` | Session IDs for an instructor (cluster source normalization) | `routers/session.py` → `_normalize_cluster_sources()` |
| 9 | `db.sessions.find_one({"enrollmentKey": key, "isStandalone": True})` | Find standalone session by enrollment key | `routers/session.py` → `enroll_standalone()` |
| 10 | `db.sessions.find_one({"_id": ObjectId(session_id), "isStandalone": True})` | Find standalone session by ID | `routers/session.py` → `leave_standalone()` |
| 11 | `db.sessions.find_one({"zoomMeetingId": int(zoom_id)})` | Find session by Zoom meeting ID (integer) | `routers/live.py`, `routers/zoom_webhook.py`, `services/quiz_scheduler.py` |
| 12 | `db.sessions.find_one({"zoomMeetingId": str(zoom_id)})` | Find session by Zoom meeting ID (string fallback) | `routers/live.py`, `routers/zoom_webhook.py`, `services/quiz_scheduler.py` |
| 13 | `db.sessions.find_one({"zoomMeetingId": zoom_meeting_id, "instructorId": user["id"]})` | Session by Zoom ID and instructor | `routers/session.py` → Zoom session creation |
| 14 | `db.sessions.find_one({"_id": result.inserted_id})` | Newly created session after insert | `routers/session.py` → `create_session()` |

---

## 3. Questions Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.questions.find_one({"_id": ObjectId(id)})` | Find question by ObjectId | `models/question.py` → `Question.find_by_id()` |
| 2 | `db.questions.find_one({"id": id})` | Find question by string ID (fallback) | `models/question.py` → `Question.find_by_id()` |
| 3 | `db.questions.find()` | Get all questions | `models/question.py` → `Question.find_all()` |
| 4 | `db.questions.find({"sessionId": session_id})` | Questions for a specific session | `models/question.py` → `find_by_session()` |
| 5 | `db.questions.find({"instructorId": instructor_id})` | Questions by instructor (with optional course/session filter) | `models/question.py` → `find_by_instructor()` |
| 6 | `db.questions.find({"$or": [{"instructorId": id}, {"createdBy": id}], "questionType": {"$nin": ["cluster"]}})` | All generic questions by instructor across all sessions | `models/question.py` → `find_for_session_with_fallback()` |
| 7 | `db.questions.find({"sessionId": session_id, "questionType": "cluster"})` | Cluster questions for a session | `routers/session.py` → readiness check, start validation |
| 8 | `db.questions.find({"sessionId": {"$in": query_sids}, "questionType": "cluster"})` | Cluster questions across multiple source sessions | `routers/session.py` → `_fetch_cluster_questions_from_sources()` |
| 9 | `db.questions.count_documents({generic_filter})` | Count generic questions for instructor (across all sessions) | `routers/session.py` → readiness & start validation |
| 10 | `db.questions.count_documents({"sessionId": sid, "questionType": "cluster"})` | Count cluster questions per session | `routers/session.py` → `get_previous_sessions_with_cluster_questions()` |
| 11 | `db.questions.find({}).to_list(length=None)` | All questions (fallback when no session match) | `routers/live.py` → trigger endpoints |

---

## 4. Quiz Answers Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.quiz_answers.count_documents({"sessionId": {"$in": ids}, "timestamp": {"$gte": started_at}})` | Count answers after session start (first-question detection) | `routers/live.py` → trigger endpoints |
| 2 | `db.quiz_answers.find({"sessionId": sid, "studentId": student_id})` | Student's quiz answers in a session | `routers/student_reports.py` → session items |
| 3 | `db.quiz_answers.find({"studentId": student_id})` | All quiz answers for a student | `routers/student_reports.py` → student report |
| 4 | `db.quiz_answers.find({"sessionId": session_id})` | All quiz answers for a session | `routers/instructor_reports.py` → quiz performance |
| 5 | `db.quiz_answers.find({"sessionId": str(zoom_meeting_id)})` | Quiz answers by Zoom session ID | `routers/instructor_reports.py` |
| 6 | `db.quiz_answers.count_documents({"sessionId": sid, "studentId": student_id})` | Count answers per student per session | `routers/student_reports.py` |
| 7 | `db.quiz_answers.count_documents({"studentId": student_id, "isCorrect": True})` | Count correct answers for student | `routers/student_reports.py` |
| 8 | `db.quiz_answers.find_one({"studentId": sid, "sessionId": {"$in": all_ids}}, sort=[("timestamp", -1)])` | Latest answer for student in session (duplicate check) | `services/quiz_service.py` → `submit_answer()` |
| 9 | `db.quiz_answers.find({"sessionId": {"$in": all_ids}, "studentId": student_id}).sort("timestamp", 1)` | Student answers in session sorted by time | `services/feedback_service.py` |
| 10 | `db.quiz_answers.find({}).limit(50)` | Sample answers for debugging | `routers/instructor_reports.py` → debug endpoint |

---

## 5. Question Assignments Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.question_assignments.find({"sessionId": sid, "studentId": student_id})` | Assignments for student in session | `routers/student_reports.py` |
| 2 | `db.question_assignments.find({"studentId": student_id})` | All assignments for a student | `routers/student_reports.py` |
| 3 | `db.question_assignments.find({"sessionId": session_id})` | All assignments for a session | `routers/instructor_reports.py` |
| 4 | `db.question_assignments.find({"sessionId": session_id, "answerIndex": {"$ne": None}})` | Answered assignments for a session | `routers/instructor_reports.py` |
| 5 | `db.question_assignments.count_documents({"sessionId": sid, "studentId": student_id})` | Count assignments per student per session | `routers/student_reports.py` |
| 6 | `db.question_assignments.count_documents({"studentId": student_id, "isCorrect": True})` | Count correct assignments for student | `routers/student_reports.py` |
| 7 | `db.question_assignments.count_documents({"sessionId": {"$in": session_ids}})` | Total assignments for instructor sessions | `routers/instructor_reports.py` |
| 8 | `db.question_assignments.aggregate([{"$match": {...}}, {"$group": {"_id": None, "correct": {"$sum": ...}, "total": {"$sum": 1}}}])` | Aggregate correct/total score for instructor | `routers/instructor_reports.py` → `get_instructor_dashboard_stats()` |

---

## 6. Session Participants Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.session_participants.find({"sessionId": session_id})` | All participants in a session | `routers/session.py`, `routers/instructor_reports.py`, `models/session_report_model.py` |
| 2 | `db.session_participants.find({"sessionId": str(zoom_meeting_id)})` | Participants by Zoom meeting ID | `routers/session.py`, `models/session_report_model.py` |
| 3 | `db.session_participants.find({"studentId": student_id})` | Sessions attended by student | `routers/student_reports.py` |
| 4 | `db.session_participants.find({"studentEmail": student_email})` | Sessions attended by student email | `routers/student_reports.py` |
| 5 | `db.session_participants.find_one({"sessionId": session_id, "studentId": student_id})` | Single participant in session | `routers/student_reports.py` |
| 6 | `db.session_participants.count_documents({"sessionId": session_id})` | Participant count for session | `routers/session.py`, `routers/instructor_reports.py`, `routers/zoom_webhook.py` |
| 7 | `db.session_participants.count_documents({"studentId": student_id})` | Total sessions attended by student | `routers/student_reports.py` |

---

## 7. Session Reports Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.session_reports.find_one({"_id": ObjectId(report_id)})` | Report by ID | `models/session_report_model.py` → `get_saved_report()` |
| 2 | `db.session_reports.find({"sessionId": session_id})` | Reports for a session | `models/session_report_model.py` → `get_reports_for_session()` |
| 3 | `db.session_reports.find_one({"sessionId": session_id, "reportType": "master"})` | Master report for session | `models/session_report_model.py`, `routers/instructor_reports.py` |
| 4 | `db.session_reports.find({"instructorId": instructor_id, "reportType": "master"}).sort("generatedAt", -1)` | All master reports by instructor | `routers/instructor_reports.py` |
| 5 | `db.session_reports.find({"students.studentId": student_id})` | Reports containing a student | `routers/student_reports.py` |
| 6 | `db.session_reports.find({"students.studentEmail": student_email})` | Reports by student email | `routers/student_reports.py` |
| 7 | `db.session_reports.find({"reportType": "master"})` | All master reports (fallback) | `routers/student_reports.py` |
| 8 | `db.session_reports.find_one({"sessionId": session_id, "reportType": report_type, ...})` | Find existing report (duplicate check) | `models/session_report_model.py` → `find_existing_report()` |

---

## 8. Courses Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.courses.find_one({"_id": ObjectId(course_id)})` | Course by ID | `models/course.py` → `CourseModel.find_by_id()` |
| 2 | `db.courses.find({"instructorId": instructor_id})` | Courses by instructor | `models/course.py` → `CourseModel.find_by_instructor()` |
| 3 | `db.courses.find(query)` | Courses with filters (status, etc.) | `models/course.py` → `CourseModel.find_all()` |
| 4 | `db.courses.find_one({"enrollmentKey": enrollment_key.upper()})` | Course by enrollment key | `models/course.py` → `CourseModel.find_by_enrollment_key()` |
| 5 | `db.courses.find({"enrolledStudents": student_id})` | Courses student is enrolled in | `models/course.py` → `CourseModel.find_enrolled_courses()` |
| 6 | `db.courses.find_one({"_id": ObjectId(course_id), "enrolledStudents": student_id})` | Check if student is enrolled | `models/course.py` → `CourseModel.is_student_enrolled()` |
| 7 | `db.courses.find_one({"enrollmentKey": new_key})` | Check if enrollment key exists (regeneration) | `models/course.py` → `CourseModel.regenerate_enrollment_key()` |

---

## 9. Course Enrollments Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.course_enrollments.count_documents({"studentId": student_id})` | Count courses enrolled by student | `routers/student_reports.py` |

---

## 10. Clusters Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.clusters.find({"sessionId": session_id})` | Cluster data for a session | `models/session_report_model.py`, `services/feedback_service.py`, `routers/instructor_reports.py` |
| 2 | `db.clusters.find({"sessionId": str(zoom_meeting_id)})` | Cluster data by Zoom meeting ID | `models/session_report_model.py` |

---

## 11. Latency Metrics Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.latency_metrics.find({"session_id": session_id})` | Latency metrics for a session | `models/session_report_model.py`, `services/feedback_service.py`, `routers/instructor_reports.py` |
| 2 | `db.latency_metrics.find({"session_id": str(zoom_meeting_id)})` | Latency metrics by Zoom meeting ID | `models/session_report_model.py` |

---

## 12. Push Subscriptions Collection

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.push_subscriptions.find({"studentId": student_id})` | Push subscriptions for a student | `services/push_service.py` |
| 2 | `db.push_subscriptions.find({})` | All push subscriptions (broadcast) | `services/push_service.py` |

---

## 13. Participation Collection (Zoom Events Log)

| # | Query | Description | Location |
|---|-------|-------------|----------|
| — | No retrieval queries | Write-only collection for Zoom webhook event logging | `routers/zoom_webhook.py` |

---

---
---

# Part 2 — Write / Update / Delete Queries

---

## 14. Insert a New User (Registration)

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.users.insert_one(user_data)` | Insert a newly registered user with all profile, auth, and verification fields | `routers/auth.py` → `register()` calls `models/user.py` → `UserModel.create()` |

**Endpoint:** `POST /api/auth/register`

**Request Body (Pydantic Model — `RegisterRequest`):**

```python
class RegisterRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    role: str = "student"   # "student" | "instructor" | "admin"
```

**Full document inserted into `users` collection:**

```python
db.users.insert_one({
    "firstName":                "John",                              # from request body
    "lastName":                 "Doe",                               # from request body
    "email":                    "john@example.com",                  # from request body
    "password":                 "a665a45920422f9d417e4867efdc...",   # SHA-256 hash of plain password
    "role":                     "student",                           # from request body (default "student")
    "status":                   0,                                   # 0 = pending email verification
    "verificationToken":        "a1b2c3d4e5f6...",                   # generated token for email verification
    "verificationTokenExpiry":  datetime(2026, 2, 26, 12, 0, 0),    # token valid for 24 hours
    "createdAt":                datetime(2026, 2, 25, 12, 0, 0),    # auto-set in UserModel.create()
    "updatedAt":                datetime(2026, 2, 25, 12, 0, 0)     # auto-set in UserModel.create()
})
```

**Step-by-step flow:**



user_data = {
    "firstName": request_data.firstName,
    "lastName": request_data.lastName,
    "email": request_data.email,
    "password": hashlib.sha256(request_data.password.encode()).hexdigest(),
    "role": request_data.role,
    "status": 0,
    "verificationToken": email_service.generate_verification_token(),
    "verificationTokenExpiry": email_service.get_token_expiry(hours=24),
}

# 2. Model adds timestamps and inserts  (models/user.py → UserModel.create())
user_data["createdAt"] = datetime.now()
user_data["updatedAt"] = datetime.now()
result = await database.users.insert_one(user_data)
user_data["id"] = str(result.inserted_id)


**Collection:** `users`  
**Fields count:** 10

---

## 15. Update User Activation Status

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.users.update_one(...)` | Activate user account after email verification — sets `status` to `1`, `emailVerified` to `True`, and removes the verification token fields | `routers/auth.py` → `verify_email()` |

**Endpoint:** `POST /api/auth/verify-email/{token}`

**How it works:**
1. User clicks the verification link sent to their email
2. Backend finds the user by `verificationToken`
3. Checks token expiry
4. Updates the user document

**Full query with all fields:**

```python
db.users.update_one(
    # Filter — find user by their ObjectId
    {"_id": ObjectId("507f1f77bcf86cd799439011")},

    # Update operations
    {
        "$set": {
            "status":            1,                                  # 0 → 1 (pending → active)
            "emailVerified":     True,                               # account is now verified
            "emailVerifiedAt":   datetime(2026, 2, 25, 14, 30, 0),  # timestamp of verification
            "updatedAt":         datetime(2026, 2, 25, 14, 30, 0)   # record last modified
        },
        "$unset": {
            "verificationToken":       "",                           # remove — no longer needed
            "verificationTokenExpiry": ""                            # remove — no longer needed
        }
    }
)
```

**Step-by-step flow:**

```python
# 1. Find user by verification token
user = await database.users.find_one({"verificationToken": token})

# 2. Check if token is expired
token_expiry = user.get("verificationTokenExpiry")
if token_expiry and datetime.utcnow() > token_expiry:
    raise HTTPException(detail="Verification link has expired.")

# 3. Activate user account
await database.users.update_one(
    {"_id": user["_id"]},
    {
        "$set": {
            "status": 1,
            "emailVerified": True,
            "emailVerifiedAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        "$unset": {
            "verificationToken": "",
            "verificationTokenExpiry": ""
        }
    }
)
```

**Collection:** `users`  
**Fields modified:** 4 (`$set`) + 2 (`$unset`)

---

## 16. Insert a Quiz Answer

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.quiz_answers.insert_one(answer_data)` | Save a student's quiz answer with correctness, timing, and network data | `models/quiz_answer_model.py` → `QuizAnswerModel.create()` (called from `services/quiz_service.py` → `submit_answer()`) |

**Endpoint:** `POST /api/quiz/submit` (via WebSocket quiz submission flow)

**Request Body (Pydantic Model — `QuizAnswer`):**

```python
class QuizAnswer(BaseModel):
    questionId:      str                         # ID of the question being answered
    answerIndex:     int                         # index of the selected option (0-based)
    timeTaken:       float                       # seconds taken to answer
    studentId:       str                         # ID of the student
    sessionId:       str                         # ID of the session (MongoDB or Zoom ID)
    timestamp:       Optional[datetime] = None   # auto-set at creation time
    networkStrength: Optional[NetworkStrength] = None  # network quality at answer time
    isCorrect:       Optional[bool] = None       # computed before storing

class NetworkStrength(BaseModel):
    quality:  str                    # "excellent" | "good" | "fair" | "poor" | "critical" | "unknown"
    rttMs:    Optional[float] = None # round-trip time in milliseconds
    jitterMs: Optional[float] = None # jitter in milliseconds
```

**Full document inserted into `quiz_answers` collection:**

```python
db.quiz_answers.insert_one({
    "questionId":      "683a1b2c3d4e5f6a7b8c9d0e",         # from request body
    "answerIndex":     1,                                     # from request body (0-based option index)
    "timeTaken":       5.5,                                   # from request body (seconds)
    "studentId":       "507f1f77bcf86cd799439011",            # from request body
    "sessionId":       "96734210583",                         # from request body (Zoom meeting ID or MongoDB ID)
    "networkStrength": {"quality": "good", "rttMs": 42.5, "jitterMs": 3.2},  # from request body (optional)
    "isCorrect":       True,                                  # computed: answer.answerIndex == question.correctAnswer
    "timestamp":       datetime(2026, 2, 25, 14, 35, 12)     # auto-set in QuizAnswerModel.create()
})
```

**Step-by-step flow:**

```python
# 1. Idempotency check — skip if student already answered this question in this session
existing = await QuizAnswerModel.find_one_by_student_question_session(
    answer.studentId, answer.questionId, answer.sessionId
)
if existing is not None:
    return {"success": True, "isCorrect": existing.get("isCorrect")}

# 2. Get question to check correctness
question = await Question.find_by_id(answer.questionId)
is_correct = question and answer.answerIndex == question.get("correctAnswer")

# 3. Build document and insert  (models/quiz_answer_model.py → QuizAnswerModel.create())
answer_data = answer.model_dump()
answer_data["timestamp"] = datetime.now()
if is_correct is not None:
    answer_data["isCorrect"] = is_correct

result = await database.quiz_answers.insert_one(answer_data)
answer_data["id"] = str(result.inserted_id)

# 4. Mark the question_assignment as answered
await QuestionAssignmentModel.mark_answered(
    session_id=answer.sessionId, student_id=answer.studentId,
    question_id=answer.questionId, is_correct=is_correct,
    answer_id=answer_data["id"], time_taken=answer.timeTaken,
    answer_index=answer.answerIndex
)

# 5. Trigger background preprocessing + KMeans clustering
asyncio.create_task(self._run_preprocessing_and_clustering(answer.sessionId))
```

**Collection:** `quiz_answers`  
**Fields count:** 8 (7 from model + 1 computed `isCorrect`)

---

## 17. Update Session Status to Completed

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.sessions.update_one(...)` | Mark session as completed when instructor ends it manually | `routers/session.py` → `end_session()` |
| 2 | `db.sessions.update_one(...)` | Mark session as completed when Zoom meeting ends (via webhook) | `routers/zoom_webhook.py` → `zoom_events()` |

### 17a. Manual End (Instructor clicks "End Session")

**Endpoint:** `POST /api/sessions/{session_id}/end`

**Full query with all fields:**

```python
db.sessions.update_one(
    # Filter — find session by its ObjectId
    {"_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")},

    # Update operations
    {
        "$set": {
            "status":        "completed",                           # "live" → "completed"
            "actualEndTime": datetime(2026, 2, 25, 15, 0, 0),     # actual time session ended
            "endedAt":       datetime(2026, 2, 25, 15, 0, 0),     # same as actualEndTime
            "endedBy":       "507f1f77bcf86cd799439011"            # instructor's user ID
        }
    }
)
```

**Step-by-step flow:**

```python
# 1. Verify session exists and belongs to this instructor
session = await db.database.sessions.find_one({"_id": ObjectId(session_id)})
if session.get("instructorId") != user["id"]:
    raise HTTPException(status_code=403, detail="You can only end your own sessions")
if session.get("status") == "completed":
    raise HTTPException(status_code=400, detail="Session is already completed")

# 2. Update session status to completed
await db.database.sessions.update_one(
    {"_id": ObjectId(session_id)},
    {
        "$set": {
            "status": "completed",
            "actualEndTime": datetime.utcnow(),
            "endedAt": datetime.utcnow(),
            "endedBy": user["id"]
        }
    }
)

# 3. Stop quiz automation if running
await quiz_scheduler.stop_automation(session_id)

# 4. Broadcast "meeting_ended" event via WebSocket to all connected students
meeting_ended_event = {
    "type": "meeting_ended",
    "sessionId": session_id,
    "status": "completed",
    "message": "Meeting has ended",
    "timestamp": datetime.utcnow().isoformat()
}
await ws_manager.broadcast_to_session(str(zoom_meeting_id), meeting_ended_event)
await ws_manager.broadcast_global(meeting_ended_event)

# 5. Generate session report automatically
```

**Collection:** `sessions`  
**Fields modified:** 4 (`status`, `actualEndTime`, `endedAt`, `endedBy`)

---

### 17b. Zoom Webhook End (Zoom notifies meeting ended)

**Endpoint:** `POST /api/zoom/webhook` (event type: `meeting.ended`)

**Full query with all fields:**

```python
db.sessions.update_one(
    # Filter — find session by its ObjectId (resolved from Zoom meeting ID)
    {"_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")},

    # Update operations
    {
        "$set": {
            "status":        "completed",                           # "live" → "completed"
            "actualEndTime": datetime(2026, 2, 25, 15, 0, 0),     # actual time session ended
            "endedAt":       datetime(2026, 2, 25, 15, 0, 0),     # same as actualEndTime
            "endedBy":       "zoom_webhook",                        # ended by Zoom (not manual)
            "participants":  25                                     # total participant count
        }
    }
)
```

**Step-by-step flow:**

```python
# 1. Extract Zoom meeting ID from webhook payload
zoom_meeting_id = payload.get("object", {}).get("id")

# 2. Find corresponding session in database
session = await db.sessions.find_one({"zoomMeetingId": int(zoom_meeting_id)})

# 3. Only end if session is not already completed
if session.get("status") != "completed":
    # 4. Get participant count from both possible session ID formats
    participant_count = await db.session_participants.count_documents({"sessionId": session_id})
    zoom_participant_count = await db.session_participants.count_documents({"sessionId": str(zoom_meeting_id)})
    total_participants = max(participant_count, zoom_participant_count)

    # 5. Update session status
    await db.sessions.update_one(
        {"_id": session["_id"]},
        {
            "$set": {
                "status": "completed",
                "actualEndTime": datetime.utcnow(),
                "endedAt": datetime.utcnow(),
                "endedBy": "zoom_webhook",
                "participants": total_participants
            }
        }
    )

    # 6. Broadcast "meeting_ended" via WebSocket
    await ws_manager.broadcast_to_session(str(zoom_meeting_id), meeting_ended_event)
    await ws_manager.broadcast_global(meeting_ended_event)

    # 7. Generate session report automatically
```

**Collection:** `sessions`  
**Fields modified:** 5 (`status`, `actualEndTime`, `endedAt`, `endedBy`, `participants`)

---

## 18. Save Clustering Results

| # | Query | Description | Location |
|---|-------|-------------|----------|
| 1 | `db.clusters.insert_one(cluster_data)` | Insert a single cluster record | `models/cluster_model.py` → `ClusterModel.create()` |
| 2 | `db.clusters.delete_many({"sessionId": session_id})` | Delete all existing clusters for a session | `models/cluster_model.py` → `ClusterModel.update_clusters_for_session()` |
| 3 | `db.clusters.insert_one(cluster_data)` (loop) | Insert each new cluster after clearing old ones | `models/cluster_model.py` → `ClusterModel.update_clusters_for_session()` |

**Triggered by:** KMeans clustering runs automatically after every student quiz answer, or manually via `POST /api/clustering/update` or `POST /api/preprocessing/run`

**Pydantic Model — `StudentCluster`:**

```python
class StudentCluster(BaseModel):
    id:              str                                    # cluster identifier
    name:            str                                    # display name (e.g. "Active Learners")
    description:     str                                    # description of the cluster
    studentCount:    int                                    # number of students in this cluster
    engagementLevel: Literal["active", "moderate", "passive"]  # cluster category
    color:           str                                    # UI color code (e.g. "#22c55e")
    prediction:      Literal["stable", "improving", "declining"]  # engagement trend
    students:        List[str]                              # list of student IDs in this cluster
    studentNames:    Optional[Dict[str, str]] = None        # studentId → "firstName lastName"
```

**Full document inserted into `clusters` collection (one per cluster):**

```python
db.clusters.insert_one({
    "id":              "cluster_active_001",                          # cluster identifier
    "name":            "Active Learners",                             # display name
    "description":     "Students with high engagement and accuracy",  # description
    "studentCount":    12,                                            # number of students
    "engagementLevel": "active",                                      # "active" | "moderate" | "passive"
    "color":           "#22c55e",                                     # UI display color
    "prediction":      "stable",                                      # "stable" | "improving" | "declining"
    "students":        ["stu_001", "stu_002", "stu_003", ...],       # list of student IDs
    "studentNames":    {"stu_001": "John Doe", "stu_002": "Jane Smith"},  # optional name map
    "sessionId":       "683a1b2c3d4e5f6a7b8c9d0e"                   # session this clustering belongs to
})
```

**Step-by-step flow (update_clusters_for_session — most common path):**

```python
# 1. Delete ALL existing clusters for this session (clean slate)
db.clusters.delete_many({
    "sessionId": "683a1b2c3d4e5f6a7b8c9d0e"
})

# 2. Insert each new cluster (typically 3: active, moderate, passive)
for cluster in clusters:                        # clusters = List[StudentCluster]
    cluster_data = cluster.model_dump()
    cluster_data["sessionId"] = session_id      # attach session reference
    result = await database.clusters.insert_one(cluster_data)
    cluster_data["id"] = str(result.inserted_id)
```

**Called from:**
- `services/quiz_service.py` → `_run_preprocessing_and_clustering()` (auto-triggered after every answer)
- `services/clustering_service.py` → `get_clusters()` (default clusters) and `update_clusters()` (KMeans results)
- `routers/preprocessing.py` → `run_preprocessing()` (manual trigger)
- `routers/clustering.py` → `update_clusters()` (manual trigger)

**Collection:** `clusters`  
**Fields count:** 10 per cluster document  
**Typical insert count:** 3 documents per session (one per engagement level)

---

## 19. All Delete Queries

All `delete_one` and `delete_many` queries across the entire backend, grouped by collection.  
**Total: 13 delete queries** (5 × `delete_one`, 8 × `delete_many`)

---

### 19a. Delete a Question

**Endpoint:** `DELETE /api/questions/{question_id}`  
**Authorization:** Instructor only — must own the question  
**Location:** `models/question.py` → `Question.delete()` (called from `routers/question.py`)

**Document being deleted (example `questions` document):**

```python
{
    "_id":            ObjectId("683a1b2c3d4e5f6a7b8c9d0e"),
    "question":       "What is the primary purpose of backpropagation?",
    "options":        ["To initialize weights", "To update weights based on error gradients", "To add layers", "To visualize"],
    "correctAnswer":  1,
    "difficulty":     "medium",
    "category":       "Neural Networks",        # or "active"/"moderate"/"passive" for cluster questions
    "questionType":   "generic",                 # "generic" | "cluster"
    "sessionId":      "683a1b2c3d4e5f6a7b8c9d0e",
    "instructorId":   "507f1f77bcf86cd799439011",
    "createdBy":      "507f1f77bcf86cd799439011",
    "createdAt":      datetime(2026, 2, 25, 10, 0, 0)
}
```

**Full query:**

```python
db.questions.delete_one({
    "_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")
})
```

**Step-by-step flow:**

```python
# 1. Find the question first to verify it exists
existing = await Question.find_by_id(question_id)
if not existing:
    raise HTTPException(status_code=404, detail="Question not found")

# 2. Verify the instructor owns the question
if not _question_owned_by(existing, user):
    raise HTTPException(status_code=403, detail="You can only delete your own questions")

# 3. Delete from database  (models/question.py → Question.delete())
result = await database.questions.delete_one({"_id": ObjectId(question_id)})
return result.deleted_count > 0    # True if deleted, False if not found
```

**Collection:** `questions` | **Type:** `delete_one` | **Removes:** 1 document  
**Return value:** `bool` — `True` if deleted, `False` if not found

---

### 19b. Delete a Course

**Endpoint:** `DELETE /api/courses/{course_id}`  
**Authorization:** Instructor only — must own the course  
**Location:** `models/course.py` → `CourseModel.delete()` (called from `routers/course.py`)

**Document being deleted (example `courses` document):**

{
    "_id":                    ObjectId("683a1b2c3d4e5f6a7b8c9d0e"),
    "title":                  "Introduction to Python Programming",
    "description":            "Learn Python from scratch",
    "instructorId":           "507f1f77bcf86cd799439011",
    "instructorName":         "Vimalan Arun",
    "instructorEmail":        "arun@example.com",
    "category":               "Programming",
    "duration":               "8 weeks",
    "courseCode":              "CS101",
    "thumbnail":              None,
    "syllabus":               [],
    "enrolledStudents":       ["stu_001", "stu_002"],
    "enrolledStudentDetails": [{"id": "stu_001", "name": "pragash", "email": "pragash@ex.com", "enrolledAt": "..."}],
    "enrollmentKey":          "ABC12345",
    "enrollmentKeyActive":    True,
    "maxStudents":            50,
    "status":                 "published",         
    "startDate":              datetime(2026, 3, 1),
    "endDate":                datetime(2026, 5, 1),
    "createdAt":              datetime(2026, 2, 20, 10, 0, 0),
    "updatedAt":              datetime(2026, 2, 25, 14, 0, 0)
}

db.courses.delete_one({
    "_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")
})


**Step-by-step flow:**

```python
# 1. Check if course exists and belongs to instructor
course = await CourseModel.find_by_id(course_id)
if not course:
    raise HTTPException(status_code=404, detail="Course not found")
if course["instructorId"] != current_user["id"]:
    raise HTTPException(status_code=403, detail="You can only delete your own courses")

# 2. Delete from database  (models/course.py → CourseModel.delete())
result = await database.courses.delete_one({"_id": ObjectId(course_id)})
return result.deleted_count > 0
```

**Collection:** `courses` | **Type:** `delete_one` | **Removes:** 1 document  
**Return value:** `bool` — `True` if deleted, `False` if not found

---

### 19c. Delete a User

**Endpoint:** Not exposed via API (model method only — available for admin use)  
**Location:** `models/user.py` → `UserModel.delete()`

**Document being deleted (example `users` document):**

```python
{
    "_id":           ObjectId("507f1f77bcf86cd799439011"),
    "firstName":     "John",
    "lastName":      "Doe",
    "email":         "john@example.com",
    "password":      "a665a45920422f9d417e4867efdc...",   # SHA-256 hashed
    "role":          "student",                             # "student" | "instructor" | "admin"
    "status":        1,                                     # 0 = pending, 1 = active
    "emailVerified": True,
    "createdAt":     datetime(2026, 2, 20, 10, 0, 0),
    "updatedAt":     datetime(2026, 2, 25, 14, 0, 0)
}
```

**Full query:**

```python
db.users.delete_one({
    "_id": ObjectId("507f1f77bcf86cd799439011")
})
```

**Code:**

```python
result = await database.users.delete_one({"_id": ObjectId(user_id)})
return result.deleted_count > 0
```

**Collection:** `users` | **Type:** `delete_one` | **Removes:** 1 document  
**Return value:** `bool` — `True` if deleted, `False` if not found

---

### 19d. Delete a Session Report

**Endpoint:** Not exposed via API (model method only)  
**Location:** `models/session_report_model.py` → `SessionReportModel.delete_report()`

**Document being deleted (example `session_reports` document):**

```python
{
    "_id":           ObjectId("683a1b2c3d4e5f6a7b8c9d0e"),
    "sessionId":     "683a1b2c3d4e5f6a7b8c9d0e",
    "reportType":    "master",                               # "master" | "student" | "instructor"
    "instructorId":  "507f1f77bcf86cd799439011",
    "generatedAt":   datetime(2026, 2, 25, 15, 5, 0),
    "generatedBy":   "507f1f77bcf86cd799439011",
    "totalStudents": 25,
    "students":      [{"studentId": "stu_001", "studentName": "Jane", "studentEmail": "jane@ex.com", ...}],
    "quizPerformance": {"totalQuestions": 10, "averageScore": 78.5},
    "engagementData":  {"clusters": [...]},
    "recommendations": ["Increase question frequency for passive students"]
}
```

**Full query:**

```python
db.session_reports.delete_one({
    "_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")
})
```

**Code:**

```python
result = await database.session_reports.delete_one({"_id": ObjectId(report_id)})
return result.deleted_count > 0
```

**Collection:** `session_reports` | **Type:** `delete_one` | **Removes:** 1 document  
**Return value:** `bool` — `True` if deleted, `False` if not found

---

### 19e. Delete Quiz Answers by Question + Session

**Endpoint:** Not exposed directly — called internally when quiz is re-triggered  
**Location:** `models/quiz_answer_model.py` → `QuizAnswerModel.delete_by_question_and_session()`

**Documents being deleted (example `quiz_answers` documents):**

```python
# Each document looks like:
{
    "_id":             ObjectId("..."),
    "questionId":      "683a1b2c3d4e5f6a7b8c9d0e",
    "answerIndex":     1,
    "timeTaken":       5.5,
    "studentId":       "507f1f77bcf86cd799439011",
    "sessionId":       "96734210583",
    "isCorrect":       True,
    "timestamp":       datetime(2026, 2, 25, 14, 35, 12),
    "networkStrength": {"quality": "good", "rttMs": 42.5, "jitterMs": 3.2},
    "clusterAtAnswer": "active"                    # stamped after clustering
}
```

**Full query:**

```python
db.quiz_answers.delete_many({
    "questionId": "683a1b2c3d4e5f6a7b8c9d0e",   # specific question ID
    "sessionId":  "96734210583"                    # specific session ID
})
```

**Code:**

```python
result = await database.quiz_answers.delete_many({
    "questionId": question_id,
    "sessionId": session_id
})
return result.deleted_count    # number of deleted documents
```

**Collection:** `quiz_answers` | **Type:** `delete_many` | **Removes:** All answers for that question in that session  
**Return value:** `int` — count of deleted documents

---

### 19f. Delete All Quiz Answers for a Session

**Endpoint:** Not exposed directly — called when quiz mode is re-activated  
**Location:** `models/quiz_answer_model.py` → `QuizAnswerModel.delete_by_session()`  
**Called from:** `services/quiz_service.py` → `trigger_question()` and `trigger_individual_questions()`

**Full query:**

```python
db.quiz_answers.delete_many({
    "sessionId": "96734210583"   # removes ALL answers for this entire session
})
```

**Step-by-step flow:**

```python
# Called when instructor re-triggers the quiz (fresh start)
# 1. Clear previous answers for this session
await QuizAnswerModel.delete_by_session(session_id)

# 2. Reset question assignments too
await QuestionAssignmentModel.reset_session(session_id)

# Internal code:
result = await database.quiz_answers.delete_many({
    "sessionId": session_id
})
return result.deleted_count
```

**Collection:** `quiz_answers` | **Type:** `delete_many` | **Removes:** All answers for the entire session  
**Return value:** `int` — count of deleted documents

---

### 19g. Delete All Clusters for a Session (before re-insert)

**Endpoint:** Triggered internally after every student answer, or via `POST /api/clustering/update`  
**Location:** `models/cluster_model.py` → `ClusterModel.update_clusters_for_session()`

**Documents being deleted (example `clusters` documents — typically 3 per session):**

```python
# Cluster 1:
{
    "_id":              ObjectId("..."),
    "id":               "cluster_active_001",
    "name":             "Active Learners",
    "description":      "Students with high engagement and accuracy",
    "studentCount":     12,
    "engagementLevel":  "active",           # "active" | "moderate" | "passive"
    "color":            "#22c55e",
    "prediction":       "stable",           # "stable" | "improving" | "declining"
    "students":         ["stu_001", "stu_002", ...],
    "studentNames":     {"stu_001": "John Doe"},
    "sessionId":        "683a1b2c3d4e5f6a7b8c9d0e"
}
# Cluster 2: (moderate)  ...
# Cluster 3: (passive)   ...
```

**Full query:**

```python
db.clusters.delete_many({
    "sessionId": "683a1b2c3d4e5f6a7b8c9d0e"   # removes ALL clusters for this session
})
# immediately followed by insert_one for each new cluster
```

**Step-by-step flow:**

```python
# 1. Delete ALL existing clusters for this session (clean slate)
await database.clusters.delete_many({"sessionId": session_id})

# 2. Insert each new cluster (typically 3: active, moderate, passive)
for cluster in clusters:
    cluster_data = cluster.model_dump()
    cluster_data["sessionId"] = session_id
    result = await database.clusters.insert_one(cluster_data)
```

**Collection:** `clusters` | **Type:** `delete_many` | **Removes:** All cluster documents (typically 3)  
**Note:** Always followed by `insert_one` for fresh clusters — this is a replace pattern

---

### 19h. Delete All Preprocessed Data for a Session (before re-insert)

**Endpoint:** Triggered internally during preprocessing (after every student answer)  
**Location:** `models/preprocessing.py` → `PreprocessingService._store()`

**Documents being deleted (example `preprocessed_engagement` documents):**

```python
# One document per student per session:
{
    "_id":           ObjectId("..."),
    "sessionId":     "683a1b2c3d4e5f6a7b8c9d0e",
    "studentId":     "507f1f77bcf86cd799439011",
    "accuracy":      0.85,                           # quiz accuracy ratio
    "responseTime":  4.2,                             # average response time in seconds
    "questionsAnswered": 8,
    "correctAnswers":    7,
    "processedAt":   datetime(2026, 2, 25, 14, 40, 0)
}
```

**Full query:**

```python
db.preprocessed_engagement.delete_many({
    "sessionId": "683a1b2c3d4e5f6a7b8c9d0e"   # removes ALL preprocessed rows for this session
})
# immediately followed by insert_many with fresh preprocessed data
```

**Step-by-step flow:**

```python
# 1. Remove previous results for this session
await db["preprocessed_engagement"].delete_many({"sessionId": session_id})

# 2. Insert fresh preprocessed data
if docs:
    await db["preprocessed_engagement"].insert_many(docs)
```

**Collection:** `preprocessed_engagement` | **Type:** `delete_many` | **Removes:** All preprocessed engagement rows  
**Note:** Always followed by `insert_many` — this is a replace pattern

---

### 19i. Delete All Question Assignments for a Session (reset)

**Endpoint:** Not exposed directly — called when quiz is re-triggered  
**Location:** `models/question_assignment_model.py` → `QuestionAssignmentModel.reset_session()`  
**Called from:** `services/quiz_service.py` → `trigger_question()` and `trigger_individual_questions()`

**Documents being deleted (example `question_assignments` documents):**

```python
{
    "_id":               ObjectId("..."),
    "sessionId":         "96734210583",
    "studentId":         "507f1f77bcf86cd799439011",
    "questionId":        "683a1b2c3d4e5f6a7b8c9d0e",
    "assignedAt":        datetime(2026, 2, 25, 14, 30, 0),
    "answered":          True,                               # False if not yet answered
    "activationVersion": 1,                                  # quiz activation cycle number
    "answeredAt":        datetime(2026, 2, 25, 14, 30, 15),
    "isCorrect":         True,
    "answerIndex":       1,
    "timeTaken":         5.5,
    "answerId":          "683a1b2c3d4e5f6a7b8c9d0f"
}
```

**Full query:**

```python
db.question_assignments.delete_many({
    "sessionId": "96734210583"   # removes ALL assignments for this session
})
```

**Step-by-step flow:**

```python
# Called when instructor re-triggers the quiz (fresh start)
# 1. Reset all question assignments
await QuestionAssignmentModel.reset_session(session_id)

# 2. Also clear quiz answers
await QuizAnswerModel.delete_by_session(session_id)

# Internal code:
result = await database.question_assignments.delete_many({
    "sessionId": session_id
})
return result.deleted_count
```

**Collection:** `question_assignments` | **Type:** `delete_many` | **Removes:** All assignments for the session  
**Return value:** `int` — count of deleted documents

---

### 19j. Delete All Session Participants (reset)

**Endpoint:** Not exposed directly — model method for session reset  
**Location:** `models/session_participant_model.py` → `SessionParticipantModel.reset_session()`

**Documents being deleted (example `session_participants` documents):**

```python
{
    "_id":          ObjectId("..."),
    "sessionId":    "96734210583",
    "studentId":    "507f1f77bcf86cd799439011",
    "studentName":  "Jane Smith",
    "studentEmail": "jane@example.com",
    "joinedAt":     datetime(2026, 2, 25, 14, 0, 0),
    "status":       "active",                          # "active" | "left"
    "leftAt":       None                                # set when student leaves
}
```

**Full query:**

```python
db.session_participants.delete_many({
    "sessionId": "96734210583"   # removes ALL participant records for this session
})
```

**Code:**

```python
result = await database.session_participants.delete_many({
    "sessionId": session_id
})
return result.deleted_count
```

**Collection:** `session_participants` | **Type:** `delete_many` | **Removes:** All participant records  
**Return value:** `int` — count of deleted documents

---

### 19k. Delete a Push Subscription (unsubscribe)

**Endpoint:** `DELETE /api/push/unsubscribe?endpoint=...`  
**Authorization:** Authenticated student  
**Location:** `routers/push_notification.py` → `unsubscribe_from_push()`

**Document being deleted (example `push_subscriptions` document):**

```python
{
    "_id":       ObjectId("..."),
    "studentId": "507f1f77bcf86cd799439011",
    "endpoint":  "https://fcm.googleapis.com/fcm/send/cR1rHr...",   # browser push endpoint URL
    "keys": {
        "p256dh": "BNcRdreALRFXTkOOUHK1EtK2wtaz5...",              # ECDH public key
        "auth":   "tBHItJI5svbpC7htfPBwWQ=="                        # auth secret
    },
    "createdAt": datetime(2026, 2, 20, 10, 0, 0),
    "updatedAt": datetime(2026, 2, 25, 14, 0, 0)
}
```

**Full query:**

```python
db.push_subscriptions.delete_one({
    "studentId": "507f1f77bcf86cd799439011",              # current user's ID
    "endpoint":  "https://fcm.googleapis.com/fcm/send/..."  # the subscription endpoint URL
})
```

**Step-by-step flow:**

```python
# 1. Get student ID from authenticated user
student_id = user.get("id")

# 2. Delete the specific subscription matching student + endpoint
result = await db.database.push_subscriptions.delete_one({
    "studentId": student_id,
    "endpoint": endpoint
})

# 3. Return 404 if subscription not found
if result.deleted_count == 0:
    raise HTTPException(status_code=404, detail="Subscription not found")
```

**Collection:** `push_subscriptions` | **Type:** `delete_one` | **Removes:** 1 subscription  
**Return value:** HTTP 200 with `{"success": True}` or 404 if not found

---

### 19l. Delete Expired Push Subscription (auto-cleanup)

**Endpoint:** None — triggered automatically during push notification delivery  
**Location:** `services/push_service.py` → `send_to_students()`

**Full query:**

```python
db.push_subscriptions.delete_one({
    "_id": ObjectId("683a1b2c3d4e5f6a7b8c9d0e")   # the expired subscription's ObjectId
})
```

**Step-by-step flow:**

```python
# During push notification delivery to each student:
try:
    webpush(subscription_info=sub_info, data=json.dumps(payload), ...)
except WebPushException as e:
    # HTTP 410 (Gone) means the browser subscription is no longer valid
    if e.response and e.response.status_code == 410:
        await db.database.push_subscriptions.delete_one({"_id": sub["_id"]})
        print(f"Removed expired subscription for student {student_id}")
```

**Collection:** `push_subscriptions` | **Type:** `delete_one` | **Removes:** 1 expired subscription  
**Trigger:** Automatic — when push delivery returns HTTP 410 (subscription expired)

---

### 19m. Clear All Latency Metrics for a Session

**Endpoint:** Not exposed directly — model method for cleanup  
**Location:** `models/latency_metrics.py` → `LatencyMetrics.clear_session_data()`

**Documents being deleted (example `latency_metrics` documents):**

```python
{
    "_id":                 ObjectId("..."),
    "session_id":          "683a1b2c3d4e5f6a7b8c9d0e",
    "student_id":          "507f1f77bcf86cd799439011",
    "student_name":        "Jane Smith",
    "avg_rtt_ms":          42.5,                      # average round-trip time
    "min_rtt_ms":          15.0,
    "max_rtt_ms":          120.0,
    "avg_jitter_ms":       3.2,
    "overall_quality":     "good",                     # "excellent"|"good"|"fair"|"poor"|"critical"
    "stability_score":     92.5,                       # 0–100
    "engagement_adjustment_factor": 1.0,               # 1.0 = no adjustment
    "samples_count":       15,
    "recent_samples":      [{"rtt_ms": 40, "jitter_ms": 2, "quality": "good", "timestamp": "..."}],
    "updated_at":          datetime(2026, 2, 25, 14, 45, 0)
}
```

**Full query:**

```python
db.latency_metrics.delete_many({
    "session_id": "683a1b2c3d4e5f6a7b8c9d0e"   # removes ALL latency data for this session
})
```

**Code:**

```python
collection = await cls.get_collection()
result = await collection.delete_many({"session_id": session_id})
return result.deleted_count
```

**Collection:** `latency_metrics` | **Type:** `delete_many` | **Removes:** All latency records for the session  
**Return value:** `int` — count of deleted documents

---
---

# Summary Tables

## Retrieval Queries

| Collection | find | find_one | count_documents | aggregate |
|------------|------|----------|-----------------|-----------|
| users | 2 | 4 | 0 | 0 |
| sessions | 8 | 14 | 0 | 0 |
| questions | 7 | 2 | 2 | 0 |
| quiz_answers | 5 | 1 | 3 | 0 |
| question_assignments | 4 | 0 | 3 | 1 |
| session_participants | 4 | 1 | 3 | 0 |
| session_reports | 4 | 3 | 0 | 0 |
| courses | 3 | 4 | 0 | 0 |
| course_enrollments | 0 | 0 | 1 | 0 |
| clusters | 2 | 0 | 0 | 0 |
| latency_metrics | 2 | 0 | 0 | 0 |
| push_subscriptions | 2 | 0 | 0 | 0 |
| participation | 0 | 0 | 0 | 0 |
| **Total** | **43** | **29** | **12** | **1** |

## Write / Update / Delete Queries

| # | Operation | Collection | Type | Location |
|---|-----------|------------|------|----------|
| 1 | Insert a New User (Registration) | `users` | `insert_one` | `models/user.py` → `User.create()` |
| 2 | Update User Activation Status | `users` | `update_one` | `routers/auth.py` → `verify_email()` |
| 3 | Insert a Quiz Answer | `quiz_answers` | `insert_one` | `models/quiz_answer_model.py` → `QuizAnswerModel.create()` |
| 4a | Update Session Status (manual end) | `sessions` | `update_one` | `routers/session.py` → `end_session()` |
| 4b | Update Session Status (Zoom webhook) | `sessions` | `update_one` | `routers/zoom_webhook.py` → `zoom_events()` |
| 5a | Save Clustering — single create | `clusters` | `insert_one` | `models/cluster_model.py` → `ClusterModel.create()` |
| 5b | Save Clustering — clear old | `clusters` | `delete_many` | `models/cluster_model.py` → `update_clusters_for_session()` |
| 5c | Save Clustering — insert new | `clusters` | `insert_one` (loop) | `models/cluster_model.py` → `update_clusters_for_session()` |

## All Delete Queries Summary

| # | Operation | Collection | Type | Location |
|---|-----------|------------|------|----------|
| 19a | Delete a Question | `questions` | `delete_one` | `models/question.py` → `Question.delete()` |
| 19b | Delete a Course | `courses` | `delete_one` | `models/course.py` → `CourseModel.delete()` |
| 19c | Delete a User | `users` | `delete_one` | `models/user.py` → `UserModel.delete()` |
| 19d | Delete a Session Report | `session_reports` | `delete_one` | `models/session_report_model.py` → `delete_report()` |
| 19e | Delete Quiz Answers (by question + session) | `quiz_answers` | `delete_many` | `models/quiz_answer_model.py` → `delete_by_question_and_session()` |
| 19f | Delete All Quiz Answers (by session) | `quiz_answers` | `delete_many` | `models/quiz_answer_model.py` → `delete_by_session()` |
| 19g | Delete All Clusters (by session) | `clusters` | `delete_many` | `models/cluster_model.py` → `update_clusters_for_session()` |
| 19h | Delete Preprocessed Data (by session) | `preprocessed_engagement` | `delete_many` | `models/preprocessing.py` → `_store()` |
| 19i | Delete Question Assignments (by session) | `question_assignments` | `delete_many` | `models/question_assignment_model.py` → `reset_session()` |
| 19j | Delete Session Participants (by session) | `session_participants` | `delete_many` | `models/session_participant_model.py` → `reset_session()` |
| 19k | Delete Push Subscription (unsubscribe) | `push_subscriptions` | `delete_one` | `routers/push_notification.py` → `unsubscribe_from_push()` |
| 19l | Delete Expired Push Subscription (auto) | `push_subscriptions` | `delete_one` | `services/push_service.py` → `send_to_students()` |
| 19m | Clear Latency Metrics (by session) | `latency_metrics` | `delete_many` | `models/latency_metrics.py` → `clear_session_data()` |
| | | | **Total: 13 delete queries** | |
