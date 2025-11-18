# AWS Zoom Webhook Integration

This directory contains AWS infrastructure for handling Zoom webhooks.

## Quick Start

### 1. Prerequisites
- AWS CLI installed and configured
- AWS account with appropriate permissions
- Zoom app created in Zoom Marketplace

### 2. Deploy Infrastructure

**Using CloudFormation:**
```bash
cd aws
./deploy.sh
```

**Or manually:**
```bash
aws cloudformation create-stack \
  --stack-name zoom-webhook-stack \
  --template-body file://cloudformation/zoom-webhook-stack.yaml \
  --parameters \
      ParameterKey=BackendApiUrl,ParameterValue=https://your-backend.com \
      ParameterKey=ZoomWebhookSecretToken,ParameterValue=your-secret \
  --capabilities CAPABILITY_NAMED_IAM
```

### 3. Get Webhook URL
```bash
aws cloudformation describe-stacks \
  --stack-name zoom-webhook-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`WebhookUrl`].OutputValue' \
  --output text
```

### 4. Configure Zoom
Use the webhook URL in your Zoom app's Event Subscriptions.

## Files

- `lambda/zoom_webhook_handler.py` - Lambda function code
- `lambda/requirements.txt` - Lambda dependencies
- `cloudformation/zoom-webhook-stack.yaml` - Infrastructure as code
- `deploy.sh` - Deployment script

## Architecture

```
Zoom → API Gateway → Lambda → Python Backend
```

