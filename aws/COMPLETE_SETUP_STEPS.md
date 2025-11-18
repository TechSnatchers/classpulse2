# Complete Setup - Final Steps

## ✅ What You Should Have Now:
- [x] Backend running (`python main.py`)
- [x] ngrok running (`ngrok http 3001`)
- [x] ngrok HTTPS URL copied (e.g., `https://abc123.ngrok-free.app`)

## 📋 Next Steps:

### Step 1: Set Lambda Environment Variable

1. **Go to AWS Lambda Console**
2. **Your `zoom_webhook` function**
3. Click **"Configuration"** tab (left sidebar)
4. Click **"Environment variables"** (under Configuration)
5. Click **"Edit"** button
6. Click **"Add environment variable"** (or edit existing)
7. Enter:
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://abc123.ngrok-free.app` (paste your actual ngrok URL)
8. Click **"Save"**

### Step 2: Deploy Lambda Function

1. Go to **"Code"** tab
2. Click **"Deploy"** button (you should see "undeployed changes")
3. Wait for "Successfully updated" message

### Step 3: Get API Gateway URL

1. Still in Lambda → Click **"Configuration"** tab
2. Click **"Triggers"** (under Configuration)
3. Click on the **API Gateway** trigger
4. **Copy the "API endpoint" URL**
   - Example: `https://abc123.execute-api.eu-north-1.amazonaws.com/prod/webhook`

### Step 4: Configure Zoom Webhook

1. Go to: **https://marketplace.zoom.us/**
2. Sign in → Go to **"Develop"** → **"Build App"** → Your app
3. Click **"Event Subscriptions"** (left sidebar)
4. Click **"Add Event Subscription"** (or edit existing)
5. Fill in:
   - **Subscription Name:** Learning Platform Webhooks
   - **Event notification endpoint URL:** Paste the API Gateway URL from Step 3
6. **Select Events:**
   - ✅ `meeting.started`
   - ✅ `meeting.ended`
   - ✅ `participant.joined`
   - ✅ `participant.left`
   - ✅ `recording.completed`
7. Click **"Save"**
8. Zoom will send a validation request - it should succeed!

### Step 5: Test It!

1. **Create a test Zoom meeting**
2. **Check Lambda logs:**
   - Lambda → Monitor → View CloudWatch logs
3. **Check backend logs:**
   - Look at the terminal running `python main.py`
4. **Check MongoDB:**
   - Events should be stored in `zoom_meetings`, `zoom_participants` collections

## 🎯 Quick Checklist:

- [ ] ngrok URL set in Lambda environment variable
- [ ] Lambda function deployed
- [ ] API Gateway URL copied
- [ ] Zoom webhook configured with API Gateway URL
- [ ] Test meeting created

## 💡 Troubleshooting:

**Lambda can't reach backend:**
- Check ngrok is still running
- Verify environment variable has correct ngrok URL
- Check backend is running on port 3001

**Zoom validation fails:**
- Check API Gateway URL is correct
- Verify Lambda function is deployed
- Check Lambda logs for errors

**No events received:**
- Verify Zoom webhook is active
- Check Lambda logs
- Verify backend is running

