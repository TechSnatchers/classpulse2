# 🚀 Quick Start Guide - Flask Zoom Backend

## Complete Setup in 5 Minutes

### Step 1: Install Dependencies (1 min)

```bash
cd backend_flask
pip install -r requirements.txt
```

### Step 2: Configure Environment (1 min)

Copy `env.example` to `.env`:

```bash
cp env.example .env
```

Edit `.env` and add your Zoom credentials:
```env
MONGO_URI=mongodb://localhost:27017/zoom_questions
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
BASE_URL=http://localhost:5000
```

### Step 3: Start MongoDB (1 min)

```bash
# Windows
net start MongoDB

# macOS/Linux
sudo service mongodb start

# Or using Docker
docker run -d -p 27017:27017 mongo
```

### Step 4: Run the Server (1 min)

```bash
python app.py
```

You should see:
```
✅ Connected to MongoDB successfully!
✅ Server starting on http://localhost:5000
🎯 Ready to send questions to Zoom participants!
```

### Step 5: Test It (1 min)

```bash
# In a new terminal
python test_flask_backend.py
```

---

## 🎯 Usage

### Send Question to Meeting

```bash
curl -X POST http://localhost:5000/api/send-question \
  -H "Content-Type: application/json" \
  -d '{
    "question_link": "https://example.com/question/abc123",
    "meeting_id": "123456789"
  }'
```

### Create Question

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

### Get All Questions

```bash
curl http://localhost:5000/api/questions
```

### Get Meeting Participants

```bash
curl http://localhost:5000/api/meetings/123456789/participants
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/zoom/webhook` | Zoom webhook handler |
| POST | `/api/send-question` | Send question to participants |
| GET | `/api/meetings/{id}/participants` | Get participants |
| POST | `/api/questions` | Create question |
| GET | `/api/questions` | List questions |
| GET | `/api/test-zoom` | Test Zoom connection |

---

## 🔧 Zoom Setup

### 1. Create Zoom App

1. Go to: https://marketplace.zoom.us/
2. Create **"Server-to-Server OAuth"** app
3. Copy: Account ID, Client ID, Client Secret

### 2. Add Scopes

Required scopes:
- `chat_message:write`
- `meeting:read:admin`
- `user:read:admin`

### 3. Configure Webhook

1. Add webhook endpoint: `https://your-domain.com/api/zoom/webhook`
2. Subscribe to events:
   - `meeting.participant_joined`
   - `meeting.participant_left`

---

## 🧪 Test Commands

```bash
# Health check
curl http://localhost:5000/health

# Test Zoom connection
curl http://localhost:5000/api/test-zoom

# Run full test suite
python test_flask_backend.py
```

---

## 📊 How It Works

```
1. Participants join Zoom meeting
   ↓
2. Zoom sends webhook to /api/zoom/webhook
   ↓
3. Backend stores participant in MongoDB
   ↓
4. Instructor sends question via /api/send-question
   ↓
5. Backend fetches all participants
   ↓
6. Backend sends Zoom chat message to each participant
   ↓
7. Participants receive link in Zoom chat
```

---

## 🐛 Troubleshooting

**Server won't start:**
- Check if MongoDB is running: `mongo --eval "db.adminCommand('ping')"`
- Verify Python version: `python --version` (need 3.7+)

**"Database not connected":**
- Start MongoDB: `sudo service mongodb start`
- Check connection URI in `.env`

**"Failed to send message":**
- Verify Zoom credentials in `.env`
- Check scopes in Zoom Marketplace
- Test connection: `curl http://localhost:5000/api/test-zoom`

**"No participants found":**
- Make sure webhook is configured in Zoom
- Check webhook is receiving events
- Participants must have joined meeting

---

## ✅ Checklist

- [ ] Python 3.7+ installed
- [ ] MongoDB running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with Zoom credentials
- [ ] Server running (`python app.py`)
- [ ] Tests passing (`python test_flask_backend.py`)
- [ ] Zoom webhook configured

---

**Ready! Start sending questions to Zoom meetings! 🎉**

