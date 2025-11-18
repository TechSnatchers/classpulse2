# Zoom Webhook Integration with AWS

This guide explains how to set up Zoom webhooks using AWS API Gateway and Lambda to integrate with your learning platform backend.

## Architecture

```
Zoom → API Gateway → Lambda → Python Backend (FastAPI)
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Zoom Developer Account** and app created
4. **Python Backend** running and accessible

## Step 1: Set Up Zoom App

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Sign in and go to "Develop" → "Build App"
3. Create a new app or use existing one
4. Enable "Event Subscriptions" (Webhooks)
5. Note your **Webhook Secret Token** (you'll need this)

## Step 2: Deploy AWS Infrastructure

### Option A: Using CloudFormation (Recommended)

1. Update the CloudFormation template with your backend URL:
   ```bash
   cd aws
   ```

2. Deploy the stack:
   ```bash
   aws cloudformation create-stack \
     --stack-name zoom-webhook-stack \
     --template-body file://cloudformation/zoom-webhook-stack.yaml \
     --parameters \
         ParameterKey=BackendApiUrl,ParameterValue=https://your-backend.com \
         ParameterKey=ZoomWebhookSecretToken,ParameterValue=your-secret-token \
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. Get the webhook URL:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name zoom-webhook-stack \
     --query 'Stacks[0].Outputs[?OutputKey==`WebhookUrl`].OutputValue' \
     --output text
   ```

### Option B: Using AWS Console

1. Create Lambda function:
   - Go to AWS Lambda Console
   - Create function: `zoom-webhook-handler`
   - Runtime: Python 3.11
   - Upload the code from `aws/lambda/zoom_webhook_handler.py`
   - Set environment variable: `BACKEND_API_URL`

2. Create API Gateway:
   - Go to API Gateway Console
   - Create REST API
   - Create resource: `/webhook`
   - Create POST method
   - Integrate with Lambda function
   - Deploy API

3. Note the API Gateway endpoint URL

## Step 3: Configure Zoom Webhook

1. In Zoom Marketplace, go to your app → "Event Subscriptions"
2. Add Event Subscription:
   - **Subscription Name**: Learning Platform Webhooks
   - **Event notification endpoint URL**: Your AWS API Gateway URL
   - **Events to subscribe**:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
3. Save and verify the endpoint (Zoom will send a validation request)

## Step 4: Configure Backend

1. Add environment variable to your `.env` file:
   ```
   ZOOM_WEBHOOK_SECRET_TOKEN=your-zoom-secret-token
   ```

2. The backend already has the webhook endpoint at:
   ```
   POST /api/zoom/webhook
   ```

3. Start your backend server:
   ```bash
   python main.py
   ```

## Step 5: Test the Integration

1. **Test webhook endpoint**:
   ```bash
   curl -X POST http://localhost:3001/api/zoom/webhook/health
   ```

2. **Create a test meeting** in Zoom and trigger events

3. **Check logs**:
   - AWS CloudWatch Logs (for Lambda)
   - Backend server logs
   - MongoDB database (check `zoom_meetings`, `zoom_participants`, `zoom_recordings` collections)

## Supported Events

The system handles these Zoom webhook events:

- **meeting.started**: Meeting begins
- **meeting.ended**: Meeting ends
- **participant.joined**: Participant joins meeting
- **participant.left**: Participant leaves meeting
- **recording.completed**: Recording is ready

## Database Collections

The webhook service creates these MongoDB collections:

- `zoom_meetings`: Meeting information
- `zoom_participants`: Participant join/leave events
- `zoom_recordings`: Recording information

## Security

1. **Webhook Verification**: The backend verifies Zoom webhook signatures
2. **HTTPS**: Use HTTPS for production (API Gateway provides this)
3. **Secret Token**: Store Zoom secret token securely (use AWS Secrets Manager for production)

## Troubleshooting

### Webhook not receiving events
- Check API Gateway logs in CloudWatch
- Verify Lambda function is invoked
- Check backend server logs
- Verify Zoom app webhook configuration

### Signature verification fails
- Ensure `ZOOM_WEBHOOK_SECRET_TOKEN` matches Zoom app secret
- Check request headers are forwarded correctly

### Lambda timeout
- Increase Lambda timeout (default: 30s)
- Check backend API response time

## Cost Estimation

- **API Gateway**: First 1M requests/month free, then $3.50 per million
- **Lambda**: 1M free requests/month, then $0.20 per million
- **CloudWatch Logs**: First 5GB free/month

For typical usage, this should be within AWS Free Tier.

## Next Steps

1. Integrate webhook events with your learning platform features
2. Add real-time notifications for instructors
3. Sync meeting data with your session management
4. Use participant data for engagement analytics

