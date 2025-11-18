# Deploy Zoom Webhook - Step by Step

## Step 1: Configure AWS Credentials

```powershell
aws configure
```

Enter:
- **AWS Access Key ID**: [Your access key]
- **AWS Secret Access Key**: [Your secret key]
- **Default region**: `us-east-1` (or your preferred region)
- **Default output format**: `json`

## Step 2: Create Parameters File

Create `parameters.json` in the `aws` folder:

```json
[
  {
    "ParameterKey": "BackendApiUrl",
    "ParameterValue": "http://localhost:3001"
  },
  {
    "ParameterKey": "ZoomWebhookSecretToken",
    "ParameterValue": "YOUR_ZOOM_SECRET_TOKEN_HERE"
  }
]
```

**Important:** Replace `YOUR_ZOOM_SECRET_TOKEN_HERE` with your actual Zoom webhook secret token from Zoom Marketplace.

## Step 3: Deploy Stack

```powershell
aws cloudformation create-stack --stack-name zoom-webhook-stack --template-body file://cloudformation/zoom-webhook-stack.yaml --parameters file://parameters.json --capabilities CAPABILITY_NAMED_IAM
```

## Step 4: Wait for Deployment

```powershell
aws cloudformation wait stack-create-complete --stack-name zoom-webhook-stack
```

This will wait until the stack is fully created (may take 2-3 minutes).

## Step 5: Get Webhook URL

```powershell
aws cloudformation describe-stacks --stack-name zoom-webhook-stack --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" --output text
```

Copy this URL - you'll need it for Zoom configuration.

## Step 6: Configure Zoom

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Your App → Event Subscriptions
3. Add Event Subscription:
   - **Endpoint URL**: Paste the webhook URL from Step 5
   - **Events**: Select:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
4. Save and verify

## Troubleshooting

### "Access Denied"
- Check your AWS credentials: `aws configure list`
- Verify IAM permissions (need CloudFormation, Lambda, API Gateway permissions)

### "Stack already exists"
- Delete existing stack: `aws cloudformation delete-stack --stack-name zoom-webhook-stack`
- Or use a different stack name

### "Template validation failed"
- Check the YAML file path
- Verify you're in the `aws` directory

