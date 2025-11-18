# Zoom Webhook Quick Start Guide

## Overview

This integration allows your learning platform to receive real-time events from Zoom meetings (meeting started, participant joined, etc.) through AWS API Gateway and Lambda.

## Architecture

```
Zoom → AWS API Gateway → AWS Lambda → Python Backend → MongoDB
```

## Quick Setup (5 Steps)

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment

Add to your `.env` file:
```
ZOOM_WEBHOOK_SECRET_TOKEN=your_zoom_secret_token_here
```

### Step 3: Deploy AWS Infrastructure

**Option A: Using CloudFormation (Recommended)**
```bash
cd aws
aws cloudformation create-stack \
  --stack-name zoom-webhook-stack \
  --template-body file://cloudformation/zoom-webhook-stack.yaml \
  --parameters \
      ParameterKey=BackendApiUrl,ParameterValue=http://your-backend-url.com \
      ParameterKey=ZoomWebhookSecretToken,ParameterValue=your_secret \
  --capabilities CAPABILITY_NAMED_IAM
```

**Option B: Manual Setup**
1. Create Lambda function with code from `aws/lambda/zoom_webhook_handler.py`
2. Create API Gateway REST API
3. Connect Lambda to API Gateway
4. Deploy API

### Step 4: Get Webhook URL

After deployment, get your webhook URL:
```bash
aws cloudformation describe-stacks \
  --stack-name zoom-webhook-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`WebhookUrl`].OutputValue' \
  --output text
```

You'll get something like:
```
https://abc123.execute-api.us-east-1.amazonaws.com/prod/webhook
```

### Step 5: Configure Zoom

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Your App → Event Subscriptions
3. Add Event Subscription:
   - **Endpoint URL**: Your AWS API Gateway URL from Step 4
   - **Events**: Select:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
4. Save and verify

## Testing

### Test Backend Endpoint
```bash
curl http://localhost:3001/api/zoom/webhook/health
```

### Test with Sample Event
```bash
curl -X POST http://localhost:3001/api/zoom/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "meeting.started",
    "event_ts": 1697461200000,
    "payload": {
      "object": {
        "id": "123456789",
        "topic": "Test Meeting"
      }
    }
  }'
```

## What Gets Stored

Events are automatically stored in MongoDB:

- **zoom_meetings**: Meeting information
- **zoom_participants**: Participant join/leave events  
- **zoom_recordings**: Recording information

## Next Steps

1. Integrate with your session management
2. Add real-time notifications
3. Use participant data for analytics
4. Link meetings to your course sessions

For detailed setup, see `ZOOM_WEBHOOK_SETUP.md`

