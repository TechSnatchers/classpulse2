# How to Check if Database is Working

## Method 1: Run Test Script
```bash
python test_db.py
```

## Method 2: Check via API Endpoints

### 1. Health Check
```bash
# Using curl
curl http://localhost:3001/health

# Or open in browser
http://localhost:3001/health
```

### 2. Test Login (verifies user data)
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com", "password": "password123"}'
```

### 3. Test Register (creates new user in DB)
```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "password": "Test123",
    "role": "student"
  }'
```

### 4. Interactive API Documentation
Open in browser: http://localhost:3001/docs

This provides an interactive interface to test all endpoints.

## Method 3: Check MongoDB Atlas Dashboard

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Navigate to your cluster
3. Click "Browse Collections"
4. You should see:
   - `users` collection with 3 documents
   - `questions` collection with 3 documents

## Method 4: Check Server Logs

When you start the server with `python main.py`, you should see:
```
🔗 Connecting to MongoDB Atlas...
✅ Connected to MongoDB Atlas: learning_platform
📍 Database: learning_platform
```

If you see these messages, the database is connected!

## Quick Verification Checklist

- [ ] Test script runs successfully (`python test_db.py`)
- [ ] Health endpoint returns OK (`/health`)
- [ ] Can login with seeded users (`/api/auth/login`)
- [ ] Can see data in MongoDB Atlas dashboard
- [ ] Server logs show successful connection

