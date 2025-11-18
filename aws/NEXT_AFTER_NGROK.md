# After ngrok is Running

## ✅ What's Done:
- ngrok authtoken installed
- Ready to start ngrok

## 📋 Next Steps:

### Step 1: Start ngrok

In your terminal, type:
```powershell
ngrok http 3001
```

**Keep this terminal open!** ngrok needs to keep running.

### Step 2: Copy the HTTPS URL

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3001
```

**Copy the HTTPS URL** (the one starting with `https://`)
- Example: `https://abc123.ngrok-free.app`

### Step 3: Set in Lambda

1. Go to AWS Lambda Console
2. Your `zoom_webhook` function
3. **Configuration** → **Environment variables**
4. Click **"Edit"**
5. Add/Update:
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://abc123.ngrok-free.app` (your actual ngrok URL)
6. Click **"Save"**

### Step 4: Deploy Lambda Function

1. Go to **"Code"** tab
2. Click **"Deploy"** button
3. Wait for deployment

### Step 5: Get API Gateway URL

1. **Configuration** → **Triggers**
2. Click on the **API Gateway** trigger
3. **Copy the "API endpoint" URL**
   - Looks like: `https://abc123.execute-api.eu-north-1.amazonaws.com/prod/webhook`

### Step 6: Configure Zoom

1. Go to: https://marketplace.zoom.us/
2. Your App → **Event Subscriptions**
3. Add Event Subscription:
   - **Endpoint URL:** Paste the API Gateway URL from Step 5
   - **Events:** Select:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
4. **Save**

## 🎯 Final Checklist:

- [x] ngrok authtoken installed
- [ ] ngrok running (`ngrok http 3001`)
- [ ] ngrok URL copied
- [ ] Lambda environment variable set (BACKEND_API_URL)
- [ ] Lambda function deployed
- [ ] API Gateway URL copied
- [ ] Zoom webhook configured

## 💡 Remember:

- Keep **3 things running**:
  1. Backend: `python main.py`
  2. ngrok: `ngrok http 3001`
  3. Lambda (deployed in AWS)

- If ngrok URL changes, update Lambda environment variable!

