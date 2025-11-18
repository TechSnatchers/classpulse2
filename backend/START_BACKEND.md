# How to Start Backend Properly

## Quick Start:

```powershell
cd backend
python main.py
```

**Keep this terminal open!** The backend needs to keep running.

## If Port 3001 is Busy:

### Find and Kill Process:

```powershell
# Find process using port 3001
netstat -ano | findstr :3001

# Kill the process (replace PID with actual process ID)
taskkill /F /PID [PID_NUMBER]
```

### Then Start Backend:

```powershell
python main.py
```

## Verify It's Running:

```powershell
Invoke-RestMethod -Uri "http://localhost:3001/health"
```

Should return: `{"status":"ok",...}`

## What to Look For:

When backend starts successfully, you should see:
```
🚀 Server running on http://localhost:3001
✅ Connected to MongoDB Atlas: learning_platform
✅ Backend is ready!
```

## For Zoom Webhooks:

Make sure:
1. ✅ Backend is running (`python main.py`)
2. ✅ ngrok is running (`ngrok http 3001`)
3. ✅ Lambda environment variable set (BACKEND_API_URL = ngrok URL)
4. ✅ Zoom webhook configured

## Check Logs:

When Zoom events come in, you'll see in the backend terminal:
```
📥 Received Zoom event: meeting.started
   Event data: {...}
✅ Meeting stored: [meeting_id]
```

If you don't see these logs, events aren't reaching the backend!

