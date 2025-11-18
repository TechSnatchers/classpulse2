# Fix 404 Error - API Gateway Not Responding

## Problem
Getting 404 errors when accessing `https://zoomlearningapp.de/` and `/health`

## Possible Causes

### 1. API Gateway Not Deployed to a Stage
Your API Gateway needs to be deployed to a stage (like `prod`, `dev`, or `$default`).

### 2. Routes Not Configured
Your FastAPI routes might not be properly configured in API Gateway.

### 3. Lambda Function Not Connected
The Lambda function might not be connected to API Gateway routes.

## Solution Steps

### Step 1: Check API Gateway Deployment

1. Go to: https://console.aws.amazon.com/apigateway/
2. Click on your API: `zoom_webhook` (ID: `l87183rknh`)
3. Check if there's a **"Stages"** section in the left sidebar
4. Look for deployed stages:
   - If you see stages (like `prod`, `dev`, `$default`) → Good
   - If no stages → You need to deploy

### Step 2: Deploy API Gateway

1. In API Gateway console, click on your API
2. Click **"Actions"** → **"Deploy API"**
3. Select or create a stage:
   - **Deployment stage:** Select `$default` or create `prod`
   - **Deployment description:** "Initial deployment"
4. Click **"Deploy"**

### Step 3: Verify API Gateway URL

After deployment, your API Gateway URL should be:
```
https://l87183rknh.execute-api.eu-north-1.amazonaws.com/$default/
```
or
```
https://l87183rknh.execute-api.eu-north-1.amazonaws.com/prod/
```

### Step 4: Test API Gateway Directly

Test the API Gateway URL directly (not through CloudFront):
```bash
# Test direct API Gateway
curl https://l87183rknh.execute-api.eu-north-1.amazonaws.com/$default/health
curl https://l87183rknh.execute-api.eu-north-1.amazonaws.com/$default/
```

If this works, then CloudFront is the issue.
If this doesn't work, then API Gateway/Lambda needs configuration.

### Step 5: Check Lambda Function

1. Go to: https://console.aws.amazon.com/lambda/
2. Find your Lambda function
3. Check if it's connected to API Gateway
4. Test the Lambda function directly

### Step 6: Check Routes in API Gateway

1. In API Gateway console, check the **"Routes"** or **"Resources"** section
2. Verify you have:
   - `GET /` route
   - `GET /health` route
   - `POST /api/zoom/webhook` route
   - `POST /api/zoom/chatbot` route

If routes are missing, you need to add them.

## Quick Checklist

```
☐ API Gateway deployed to a stage?
☐ Routes configured in API Gateway?
☐ Lambda function connected to routes?
☐ Test API Gateway URL directly
☐ If API Gateway works, check CloudFront
☐ If API Gateway doesn't work, check Lambda
```

## Next Steps

1. **First:** Deploy API Gateway to a stage
2. **Second:** Test API Gateway URL directly
3. **Third:** If API Gateway works, CloudFront should work too
4. **Fourth:** If API Gateway doesn't work, check Lambda function

