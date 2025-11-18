# 🎯 Zoom Live Question Triggering System - Complete Guide

## Overview

This system allows instructors to send questions directly into Zoom meeting chats. Students click the link, answer the question, and responses are tracked in real-time with response times calculated.

---

## 🎬 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                  COMPLETE WORKFLOW                          │
└─────────────────────────────────────────────────────────────┘

1. INSTRUCTOR TRIGGERS QUESTION
   ├─ Clicks "Send Question" button on dashboard
   ├─ Backend picks question (random or specific)
   ├─ Generates unique URL with session token
   └─ Sends message to Zoom meeting chat via API

2. ZOOM CHAT MESSAGE APPEARS
   ├─ "📝 NEW QUESTION (Time limit: 30s)"
   ├─ "❓ What is Python?"
   └─ "👉 Click here to answer: https://app.com/question/abc123"

3. STUDENTS CLICK LINK
   ├─ Question page opens in browser
   ├─ Timer starts counting
   └─ Shows question with multiple choice options

4. STUDENT SUBMITS ANSWER
   ├─ Selects an option
   ├─ Clicks submit
   ├─ Response time calculated automatically
   └─ Answer saved to database

5. LIVE DASHBOARD UPDATES
   ├─ Instructor sees responses in real-time
   ├─ Shows: Total responses, correct/incorrect, avg time
   └─ Displays leaderboard by response time
```

---

## 📋 Features

✅ **Instructor Features:**
- Trigger questions with one click
- Pick specific question or random
- Auto-send to Zoom meeting chat
- Live dashboard showing responses
- Response time tracking
- Accuracy statistics
- Complete/close sessions

✅ **Student Features:**
- Click link from Zoom chat
- See question immediately
- Submit answer
- Instant feedback (correct/incorrect)
- View their response time

✅ **System Features:**
- Unique URL per question session
- Prevents duplicate submissions
- Automatic session expiry
- Response time calculation (milliseconds)
- Real-time statistics
- No authentication required for students

---

## 🛠️ Setup Instructions

### Step 1: Configure Zoom App

1. **Go to Zoom Marketplace:**
   - Visit: https://marketplace.zoom.us/
   - Sign in with your Zoom account

2. **Create a Server-to-Server OAuth App:**
   - Click "Develop" → "Build App"
   - Choose "Server-to-Server OAuth"
   - Fill in app information
   - Note down:
     - Client ID
     - Client Secret
     - Account ID

3. **Add Scopes:**
   Required scopes:
   - `meeting:write:admin` - Send messages to meetings
   - `meeting:read:admin` - Read meeting details
   - `chat_message:write` - Send chat messages
   - `chatbot:write` - Chatbot functionality

4. **Activate the App**

### Step 2: Configure Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
# Zoom Configuration
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_ACCOUNT_ID=your_account_id_here
ZOOM_CHATBOT_JID=your_chatbot_jid_here
ZOOM_WEBHOOK_SECRET_TOKEN=your_secret_token_here

# Frontend URL (for generating question links)
FRONTEND_URL=http://localhost:5173

# MongoDB
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=learning_platform
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Start the Server

```bash
python main.py
```

---

## 📡 API Endpoints

### 1. Trigger Question (Instructor Only)

**POST** `/api/live-questions/trigger`

**Headers:**
```
x-user-id: instructor_id
x-user-email: instructor@example.com
```

**Request Body:**
```json
{
  "questionId": "optional_specific_question_id",
  "zoomMeetingId": "123456789",
  "courseId": "optional_course_id",
  "timeLimit": 30,
  "sendToZoom": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Question triggered successfully",
  "session": {
    "id": "session_id",
    "sessionToken": "abc123def456",
    "question": "What is Python?",
    "status": "active",
    "timeLimit": 30
  },
  "questionUrl": "http://localhost:5173/question/abc123def456",
  "zoomMessageSent": true
}
```

---

### 2. Get Question (Public - No Auth)

**GET** `/api/live-questions/session/{token}`

**Example:** `/api/live-questions/session/abc123def456`

**Response:**
```json
{
  "success": true,
  "question": {
    "sessionToken": "abc123def456",
    "sessionId": "session_id",
    "question": "What is Python?",
    "options": [
      "A programming language",
      "A snake",
      "A data structure",
      "A framework"
    ],
    "timeLimit": 30,
    "triggeredAt": "2024-01-15T10:30:00Z",
    "expiresAt": "2024-01-15T10:35:00Z"
  }
}
```

**Note:** Does NOT return the correct answer to prevent cheating.

---

### 3. Submit Answer (Public - No Auth)

**POST** `/api/live-questions/submit/{token}`

**Request Body:**
```json
{
  "selectedAnswer": 0,
  "responseTime": 12.5,
  "studentName": "John Doe",
  "studentEmail": "john@example.com",
  "studentId": "optional_student_id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Answer submitted successfully",
  "isCorrect": true,
  "correctAnswer": 0,
  "responseTime": 12.5,
  "response": {
    "id": "response_id",
    "isCorrect": true,
    "submittedAt": "2024-01-15T10:30:12Z"
  }
}
```

---

### 4. Live Dashboard - Get Active Sessions

**GET** `/api/live-questions/dashboard/active`

**Headers:**
```
x-user-id: instructor_id
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "sessions": [
    {
      "id": "session_id",
      "question": "What is Python?",
      "status": "active",
      "totalResponses": 15,
      "correctResponses": 12,
      "incorrectResponses": 3,
      "triggeredAt": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### 5. Get Session Responses

**GET** `/api/live-questions/dashboard/session/{session_id}/responses`

**Headers:**
```
x-user-id: instructor_id
```

**Response:**
```json
{
  "success": true,
  "session": {
    "id": "session_id",
    "question": "What is Python?",
    "status": "active"
  },
  "statistics": {
    "total": 15,
    "correct": 12,
    "incorrect": 3,
    "accuracy": 80.0,
    "averageResponseTime": 15.2,
    "fastestResponse": 8.1,
    "slowestResponse": 25.6
  },
  "responses": [
    {
      "id": "response_id",
      "studentName": "John Doe",
      "selectedAnswer": 0,
      "isCorrect": true,
      "responseTime": 12.5,
      "submittedAt": "2024-01-15T10:30:12Z"
    }
  ]
}
```

---

### 6. Complete Session

**POST** `/api/live-questions/dashboard/session/{session_id}/complete`

**Headers:**
```
x-user-id: instructor_id
```

**Response:**
```json
{
  "success": true,
  "message": "Session completed successfully"
}
```

---

### 7. Test Zoom Connection

**GET** `/api/live-questions/test-zoom`

**Headers:**
```
x-user-id: instructor_id
```

**Response:**
```json
{
  "success": true,
  "message": "Zoom API connection successful",
  "configured": true
}
```

---

## 💾 Database Collections

### 1. live_question_sessions

```javascript
{
  _id: ObjectId,
  sessionToken: "abc123def456",      // Unique token for URL
  questionId: "question_id",
  question: "What is Python?",
  options: ["Option 1", "Option 2"],
  correctAnswer: 0,
  instructorId: "instructor_id",
  instructorName: "John Doe",
  zoomMeetingId: "123456789",
  courseId: "course_id",
  status: "active",                   // active | completed | expired
  timeLimit: 30,
  triggeredAt: ISODate,
  expiresAt: ISODate,
  responses: ["response_id_1"],       // Array of response IDs
  totalResponses: 15,
  correctResponses: 12,
  incorrectResponses: 3,
  createdAt: ISODate,
  updatedAt: ISODate
}
```

### 2. question_responses

```javascript
{
  _id: ObjectId,
  sessionId: "session_id",
  sessionToken: "abc123def456",
  questionId: "question_id",
  studentId: "optional_student_id",
  studentName: "John Doe",
  studentEmail: "john@example.com",
  zoomUserId: "zoom_user_id",
  selectedAnswer: 0,
  isCorrect: true,
  responseTime: 12.5,                 // Seconds
  submittedAt: ISODate,
  ipAddress: "192.168.1.1",
  createdAt: ISODate
}
```

---

## 🎯 Usage Examples

### Example 1: Trigger Random Question

```javascript
// Frontend JavaScript
const triggerQuestion = async () => {
  const response = await fetch('/api/live-questions/trigger', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-user-id': currentUser.id,
      'x-user-email': currentUser.email
    },
    body: JSON.stringify({
      zoomMeetingId: '123456789',
      timeLimit: 30,
      sendToZoom: true
    })
  });
  
  const data = await response.json();
  console.log('Question URL:', data.questionUrl);
};
```

### Example 2: Student Answers Question

```javascript
// Student clicks link: /question/abc123def456
// Frontend loads question and shows timer

const submitAnswer = async (selectedAnswer, timeElapsed) => {
  const response = await fetch('/api/live-questions/submit/abc123def456', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      selectedAnswer: selectedAnswer,
      responseTime: timeElapsed,
      studentName: 'John Doe',
      studentEmail: 'john@example.com'
    })
  });
  
  const data = await response.json();
  console.log('Correct?', data.isCorrect);
  console.log('Your time:', data.responseTime, 'seconds');
};
```

### Example 3: Instructor Dashboard

```javascript
// Poll for live updates every 2 seconds
const fetchLiveResponses = async (sessionId) => {
  const response = await fetch(
    `/api/live-questions/dashboard/session/${sessionId}/responses`,
    {
      headers: {
        'x-user-id': currentUser.id
      }
    }
  );
  
  const data = await response.json();
  updateDashboard(data.statistics, data.responses);
};

// Poll every 2 seconds
setInterval(() => fetchLiveResponses(sessionId), 2000);
```

---

## 🔧 Frontend Implementation Guide

### Student Question Page (`/question/{token}`)

```jsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function QuestionPage() {
  const { token } = useParams();
  const [question, setQuestion] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [result, setResult] = useState(null);
  
  useEffect(() => {
    // Load question
    fetch(`/api/live-questions/session/${token}`)
      .then(res => res.json())
      .then(data => {
        setQuestion(data.question);
        setStartTime(Date.now());
      });
  }, [token]);
  
  const submitAnswer = async () => {
    const responseTime = (Date.now() - startTime) / 1000;
    
    const response = await fetch(`/api/live-questions/submit/${token}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        selectedAnswer,
        responseTime,
        studentName: 'Student Name'
      })
    });
    
    const data = await response.json();
    setResult(data);
  };
  
  if (!question) return <div>Loading...</div>;
  if (result) return (
    <div>
      <h2>{result.isCorrect ? '✅ Correct!' : '❌ Incorrect'}</h2>
      <p>Response time: {result.responseTime.toFixed(2)}s</p>
    </div>
  );
  
  return (
    <div>
      <h1>{question.question}</h1>
      <p>Time limit: {question.timeLimit}s</p>
      
      {question.options.map((option, index) => (
        <button
          key={index}
          onClick={() => setSelectedAnswer(index)}
          className={selectedAnswer === index ? 'selected' : ''}
        >
          {option}
        </button>
      ))}
      
      <button onClick={submitAnswer} disabled={selectedAnswer === null}>
        Submit Answer
      </button>
    </div>
  );
}
```

### Instructor Dashboard

```jsx
function InstructorDashboard() {
  const [activeSessions, setActiveSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [liveData, setLiveData] = useState(null);
  
  useEffect(() => {
    // Load active sessions
    fetch('/api/live-questions/dashboard/active', {
      headers: { 'x-user-id': currentUser.id }
    })
      .then(res => res.json())
      .then(data => setActiveSessions(data.sessions));
  }, []);
  
  useEffect(() => {
    if (!selectedSession) return;
    
    // Poll for live updates
    const interval = setInterval(() => {
      fetch(`/api/live-questions/dashboard/session/${selectedSession}/responses`, {
        headers: { 'x-user-id': currentUser.id }
      })
        .then(res => res.json())
        .then(data => setLiveData(data));
    }, 2000);
    
    return () => clearInterval(interval);
  }, [selectedSession]);
  
  const triggerQuestion = async () => {
    const response = await fetch('/api/live-questions/trigger', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-user-id': currentUser.id
      },
      body: JSON.stringify({
        zoomMeetingId: '123456789',
        timeLimit: 30,
        sendToZoom: true
      })
    });
    
    const data = await response.json();
    alert(`Question sent! URL: ${data.questionUrl}`);
  };
  
  return (
    <div>
      <button onClick={triggerQuestion}>Send Question to Zoom</button>
      
      {liveData && (
        <div>
          <h2>Live Statistics</h2>
          <p>Total Responses: {liveData.statistics.total}</p>
          <p>Accuracy: {liveData.statistics.accuracy.toFixed(1)}%</p>
          <p>Avg Time: {liveData.statistics.averageResponseTime.toFixed(2)}s</p>
          
          <h3>Recent Responses</h3>
          {liveData.responses.map(r => (
            <div key={r.id}>
              {r.studentName} - {r.isCorrect ? '✅' : '❌'} - {r.responseTime}s
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 🚨 Troubleshooting

### Zoom message not sending

1. **Check Zoom credentials:**
   ```bash
   curl http://localhost:3001/api/live-questions/test-zoom \
     -H "x-user-id: YOUR_ID"
   ```

2. **Verify scopes in Zoom app**

3. **Check logs** for error messages

### Students can't access question

1. **Check session status** (might be expired)
2. **Verify frontend URL** in .env
3. **Check token** is correct

### Duplicate responses

- System automatically prevents duplicates
- Uses student ID, email, or IP address

---

## ✨ Features Summary

| Feature | Status |
|---------|--------|
| Trigger questions via API | ✅ |
| Random question selection | ✅ |
| Unique URL generation | ✅ |
| Send to Zoom chat | ✅ |
| Response time tracking | ✅ |
| Prevent duplicate submissions | ✅ |
| Live instructor dashboard | ✅ |
| Real-time statistics | ✅ |
| Session expiry | ✅ |
| No auth required for students | ✅ |

---

## 📚 Additional Resources

- **Zoom API Docs:** https://marketplace.zoom.us/docs/api-reference/
- **Server-to-Server OAuth:** https://marketplace.zoom.us/docs/guides/build/server-to-server-oauth-app/
- **Chat API:** https://marketplace.zoom.us/docs/api-reference/zoom-api/methods#operation/sendMessage

---

**System is ready! Start triggering live questions in your Zoom meetings! 🚀**

