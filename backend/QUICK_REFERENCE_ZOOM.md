# 🎯 Zoom Live Questions - Quick Reference Card

## 🚀 Quick Start (3 Steps)

```bash
# 1. Start server
python main.py

# 2. Run test (no Zoom needed)
python test_live_questions.py

# 3. Configure Zoom (optional - for production)
# Copy env_template.txt to .env and add Zoom credentials
```

---

## 📡 API Quick Reference

### Trigger Question (Instructor)
```bash
POST /api/live-questions/trigger
Headers: x-user-id, x-user-email
Body: {
  "questionId": "optional",
  "zoomMeetingId": "123456789",
  "timeLimit": 30,
  "sendToZoom": true
}
```

### Get Question (Student - No Auth)
```bash
GET /api/live-questions/session/{token}
```

### Submit Answer (Student - No Auth)
```bash
POST /api/live-questions/submit/{token}
Body: {
  "selectedAnswer": 2,
  "responseTime": 12.5,
  "studentName": "John Doe"
}
```

### Live Dashboard (Instructor)
```bash
GET /api/live-questions/dashboard/active
GET /api/live-questions/dashboard/session/{id}/responses
POST /api/live-questions/dashboard/session/{id}/complete
```

---

## 🗄️ Database Collections

### `live_question_sessions`
- Stores active question sessions
- Unique token for URL access
- Tracks statistics

### `question_responses`
- Stores student answers
- Records response time
- Prevents duplicates

---

## 🎬 Workflow

```
1. Instructor: Click "Send Question"
   ↓
2. Backend: Create session + Generate URL
   ↓
3. Zoom: Message appears in chat
   ↓
4. Student: Click link → Answer → Submit
   ↓
5. Backend: Calculate time + Save response
   ↓
6. Dashboard: Live updates for instructor
```

---

## ⚙️ Environment Variables

```env
# Required for Zoom integration
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_secret
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CHATBOT_JID=your_jid

# Required for URL generation
FRONTEND_URL=http://localhost:5173

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=learning_platform
```

---

## 🧪 Testing Commands

```bash
# Full system test
python test_live_questions.py

# Test specific question
curl -X POST http://localhost:3001/api/live-questions/trigger \
  -H "Content-Type: application/json" \
  -H "x-user-id: instructor_id" \
  -d '{"zoomMeetingId":"123","timeLimit":30}'

# Test Zoom connection
curl http://localhost:3001/api/live-questions/test-zoom \
  -H "x-user-id: instructor_id"
```

---

## 📊 Response Statistics

System automatically tracks:
- Total responses
- Correct/Incorrect count
- Accuracy percentage
- Average response time
- Fastest/Slowest response

---

## 🎯 Key Features

✅ One-click question sending  
✅ Unique URL per session  
✅ Automatic response time tracking  
✅ Duplicate prevention  
✅ Live dashboard  
✅ Session expiry  
✅ No student auth required  

---

## 🔧 Common Commands

```bash
# Start server
python main.py

# Run tests
python test_live_questions.py

# Create question
POST /api/questions/

# Trigger question
POST /api/live-questions/trigger

# View dashboard
GET /api/live-questions/dashboard/active
```

---

## 📱 Frontend Routes Needed

```
/question/{token}  - Student question page
/dashboard         - Instructor dashboard
```

---

## 🔗 Important URLs

- API Docs: http://localhost:3001/docs
- Health: http://localhost:3001/health
- Root: http://localhost:3001

---

## 💡 Tips

1. **No Zoom?** System works without Zoom setup for testing
2. **Testing:** Use test_live_questions.py to verify everything
3. **Live Updates:** Poll dashboard every 2 seconds
4. **Response Time:** Calculated client-side in milliseconds
5. **Security:** Each session has unique token

---

## 📚 Documentation

- **Full Guide:** ZOOM_LIVE_QUESTIONS_GUIDE.md
- **Summary:** ZOOM_SYSTEM_SUMMARY.md
- **This File:** QUICK_REFERENCE_ZOOM.md

---

## 🆘 Troubleshooting

**Zoom message not sending?**
- Check Zoom credentials in .env
- Test with: GET /api/live-questions/test-zoom

**Can't access question?**
- Check session status (might be expired)
- Verify token is correct

**Duplicate submission error?**
- System prevents multiple submissions per student
- This is expected behavior

---

## ✨ Quick Example

```javascript
// Trigger question
const response = await fetch('/api/live-questions/trigger', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-user-id': userId
  },
  body: JSON.stringify({
    zoomMeetingId: '123456789',
    timeLimit: 30
  })
});

const { session, questionUrl } = await response.json();
console.log('Students go to:', questionUrl);
```

---

**System Ready! Start with: `python test_live_questions.py`** 🚀

