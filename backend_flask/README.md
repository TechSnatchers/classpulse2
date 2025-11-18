# Flask Backend - Zoom Live Questions

Send live questions directly to Zoom participants using the Zoom Chat API.

## Features

✅ **Server-to-Server OAuth** - Secure authentication with Zoom  
✅ **Webhook Handling** - Tracks participant join/leave events  
✅ **MongoDB Storage** - Stores participants and questions  
✅ **Direct Messaging** - Sends question links to all meeting participants  
✅ **Complete REST API** - Full CRUD for questions  

---

## Quick Start

### 1. Install Dependencies

```bash
cd backend_flask
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```env
MONGO_URI=mongodb://localhost:27017/zoom_questions
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
BASE_URL=http://localhost:5000
```

### 3. Start MongoDB

```bash
# Make sure MongoDB is running
mongod
```

### 4. Run the Server

```bash
python app.py
```

Server will start on: **http://localhost:5000**

---

## API Endpoints

### Health Check
```bash
GET /health
```

### Zoom Webhook (for Zoom to call)
```bash
POST /api/zoom/webhook
```

### Send Question to Meeting
```bash
POST /api/send-question
Content-Type: application/json

{
  "question_link": "https://example.com/question/abc123",
  "meeting_id": "123456789"
}
```

### Get Meeting Participants
```bash
GET /api/meetings/{meeting_id}/participants
```

### Questions CRUD
```bash
# Create question
POST /api/questions
{
  "title": "Geography Question",
  "question_text": "What is the capital of France?",
  "options": ["London", "Berlin", "Paris", "Madrid"],
  "correct_answer": 2
}

# Get all questions
GET /api/questions

# Get single question
GET /api/questions/{question_id}

# Update question
PUT /api/questions/{question_id}

# Delete question
DELETE /api/questions/{question_id}
```

### Test Zoom Connection
```bash
GET /api/test-zoom
```

---

## Folder Structure

```
backend_flask/
├── app.py                      # Main Flask application
├── database.py                 # MongoDB configuration
├── zoom_chat.py               # Zoom Chat API integration
├── zoom_webhook.py            # Webhook handler
├── routes/
│   ├── __init__.py
│   ├── send_question.py       # Send question endpoint
│   └── questions.py           # Questions CRUD
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## How It Works

### 1. **Participant Tracking**

When participants join a Zoom meeting, Zoom sends webhooks:

```
Zoom Meeting Started
    ↓
Participant Joins
    ↓
Webhook: participant_joined
    ↓
Store in MongoDB:
    - user_id
    - name
    - email
    - meeting_id
```

### 2. **Send Question**

Instructor triggers question send:

```
POST /api/send-question
{
  "question_link": "https://app.com/question/abc123",
  "meeting_id": "123456789"
}
    ↓
Fetch all participants from MongoDB
    ↓
For each participant:
    └─ Send Zoom chat message:
       "📝 New Question! Answer here: https://app.com/question/abc123"
    ↓
Return results
```

### 3. **Message Delivery**

```
Backend → Zoom Chat API → Participant's Zoom Chat
```

Each participant receives a direct message with the question link.

---

## Database Collections

### `participants`
```javascript
{
  "meeting_id": "123456789",
  "user_id": "abc123",
  "name": "John Doe",
  "email": "john@example.com",
  "join_time": ISODate("2024-01-15T10:00:00Z"),
  "status": "joined"
}
```

### `questions`
```javascript
{
  "_id": ObjectId("..."),
  "title": "Geography Question",
  "question_text": "What is the capital of France?",
  "options": ["London", "Berlin", "Paris", "Madrid"],
  "correct_answer": 2,
  "time_limit": 30,
  "created_at": ISODate("2024-01-15T10:00:00Z")
}
```

---

## Zoom Setup

### 1. Create Zoom App

1. Go to: https://marketplace.zoom.us/
2. Click **"Develop"** → **"Build App"**
3. Choose **"Server-to-Server OAuth"**

### 2. Configure App

- Add required scopes:
  - `chat_message:write`
  - `meeting:read:admin`
  - `user:read:admin`

### 3. Get Credentials

Copy these to your `.env` file:
- Account ID
- Client ID
- Client Secret

### 4. Configure Webhook

1. In Zoom app settings, add webhook endpoint
2. URL: `https://your-domain.com/api/zoom/webhook`
3. Subscribe to events:
   - `meeting.participant_joined`
   - `meeting.participant_left`

---

## Testing

### Test Health Check
```bash
curl http://localhost:5000/health
```

### Test Zoom Connection
```bash
curl http://localhost:5000/api/test-zoom
```

### Create a Question
```bash
curl -X POST http://localhost:5000/api/questions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Question",
    "question_text": "What is 2+2?",
    "options": ["3", "4", "5", "6"],
    "correct_answer": 1
  }'
```

### Send Question to Meeting
```bash
curl -X POST http://localhost:5000/api/send-question \
  -H "Content-Type: application/json" \
  -d '{
    "question_link": "https://example.com/question/abc123",
    "meeting_id": "123456789"
  }'
```

---

## Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
sudo service mongodb status

# Start MongoDB
sudo service mongodb start
```

### Zoom API Errors

**401 Unauthorized:**
- Check your Zoom credentials in `.env`
- Verify Account ID, Client ID, and Client Secret

**403 Forbidden:**
- Check app scopes in Zoom Marketplace
- Ensure `chat_message:write` is enabled

**404 User Not Found:**
- Verify participant is in the database
- Check if webhook is receiving events

### No Participants Found
- Make sure Zoom webhook is configured
- Check webhook endpoint is accessible
- Verify participants have joined the meeting

---

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

For production, set:
```env
FLASK_ENV=production
FLASK_DEBUG=False
BASE_URL=https://your-domain.com
```

### HTTPS Required

Zoom webhooks require HTTPS. Use:
- Nginx with SSL certificate
- Cloudflare
- AWS Load Balancer

---

## Features Summary

| Feature | Status |
|---------|--------|
| Server-to-Server OAuth | ✅ |
| Participant tracking | ✅ |
| Send messages to participants | ✅ |
| Questions CRUD | ✅ |
| MongoDB storage | ✅ |
| Webhook handling | ✅ |
| Error handling | ✅ |

---

## API Response Examples

### Success Response
```json
{
  "success": true,
  "message": "Question sent to 5 participants",
  "meeting_id": "123456789",
  "total_participants": 5,
  "success_count": 5,
  "failed_count": 0,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "No participants found for this meeting",
  "meeting_id": "123456789"
}
```

---

## License

MIT

---

**System Ready! Start with: `python app.py`** 🚀

