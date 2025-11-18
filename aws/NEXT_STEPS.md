# Next Steps - Complete Setup

## ✅ What's Done:
- Lambda function code updated (using urllib - no dependencies)
- Backend server should be running on port 3001
- Port 3001 is free

## 📋 Next Steps:

### Step 1: Verify Backend is Running

Open a new terminal and test:
```powershell
Invoke-RestMethod -Uri "http://localhost:3001/health"
```

If it works, you'll see: `{"status":"ok",...}`

If not, start backend:
```powershell
cd backend
python main.py
```
**Keep this terminal open!**

### Step 2: Install and Start ngrok

**Download ngrok:**
- Go to: https://ngrok.com/download
- Download for Windows
- Extract the .exe file

**Or use Chocolatey:**
```powershell
choco install ngrok
```

**Start ngrok (in a NEW terminal):**
```powershell
ngrok http 3001
```

**Copy the HTTPS URL** (looks like: `https://abc123.ngrok-free.app`)

**Keep this terminal open too!**

### Step 3: Set Lambda Environment Variable

1. Go to AWS Lambda Console
2. Your `zoom_webhook` function
3. Configuration → Environment variables
4. Click "Edit"
5. Add:
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://abc123.ngrok-free.app` (your ngrok URL)
6. Click "Save"

### Step 4: Get API Gateway URL

1. In Lambda → Configuration → Triggers
2. Click on the API Gateway trigger
3. **Copy the "API endpoint" URL**
   - Looks like: `https://abc123.execute-api.eu-north-1.amazonaws.com/prod/webhook`

### Step 5: Configure Zoom

1. Go to: https://marketplace.zoom.us/
2. Sign in → Your App
3. Go to "Event Subscriptions"
4. Add Event Subscription:
   - **Endpoint URL:** Paste the API Gateway URL from Step 4
   - **Events:** Select:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
5. Save

### Step 6: Test!

1. Create a test Zoom meeting
2. Check Lambda logs: Lambda → Monitor → View CloudWatch logs
3. Check backend logs (in the terminal running `python main.py`)
4. Check MongoDB for stored events

## 🎯 Quick Checklist:

- [ ] Backend running on port 3001
- [ ] ngrok running and exposing port 3001
- [ ] Lambda environment variable set (BACKEND_API_URL = ngrok URL)
- [ ] API Gateway URL copied
- [ ] Zoom webhook configured with API Gateway URL
- [ ] Test meeting created

## 💡 Tips:

- Keep 3 terminals open:
  1. Backend (`python main.py`)
  2. ngrok (`ngrok http 3001`)
  3. Your main terminal

- If ngrok URL changes, update Lambda environment variable

- For production, deploy backend to cloud and use that URL instead of ngrok

