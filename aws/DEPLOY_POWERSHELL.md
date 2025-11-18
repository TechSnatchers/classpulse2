# Deploy Zoom Webhook to AWS (PowerShell)

## Method 1: Using PowerShell Script (Easiest)

```powershell
cd aws
.\deploy-aws-cli.ps1
```

This script will prompt you for:
- Backend API URL
- Zoom webhook secret token

## Method 2: Using AWS CLI Directly

### Step 1: Create Parameters File

Create `parameters.json`:
```json
[
  {
    "ParameterKey": "BackendApiUrl",
    "ParameterValue": "https://your-backend-url.com"
  },
  {
    "ParameterKey": "ZoomWebhookSecretToken",
    "ParameterValue": "your_zoom_secret_token"
  }
]
```

### Step 2: Deploy Stack

```powershell
aws cloudformation create-stack `
  --stack-name zoom-webhook-stack `
  --template-body file://cloudformation/zoom-webhook-stack.yaml `
  --parameters file://parameters.json `
  --capabilities CAPABILITY_NAMED_IAM
```

### Step 3: Wait for Completion

```powershell
aws cloudformation wait stack-create-complete `
  --stack-name zoom-webhook-stack
```

### Step 4: Get Webhook URL

```powershell
aws cloudformation describe-stacks `
  --stack-name zoom-webhook-stack `
  --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" `
  --output text
```

## Method 3: Single Command (All on One Line)

```powershell
aws cloudformation create-stack --stack-name zoom-webhook-stack --template-body file://cloudformation/zoom-webhook-stack.yaml --parameters ParameterKey=BackendApiUrl,ParameterValue=https://your-backend.com ParameterKey=ZoomWebhookSecretToken,ParameterValue=your_secret --capabilities CAPABILITY_NAMED_IAM
```

**Note:** Replace:
- `https://your-backend.com` with your actual backend URL
- `your_secret` with your Zoom webhook secret token

## Troubleshooting

### "Missing argument in parameter list"
- Use Method 1 (script) or Method 2 (parameters file)
- Don't use backslashes (`\`) in PowerShell - use backticks (`` ` ``) or put everything on one line

### "Template file not found"
- Make sure you're in the `aws` directory
- Check the file path: `cloudformation\zoom-webhook-stack.yaml`

### "Access Denied"
- Check your AWS credentials: `aws configure`
- Verify you have permissions to create CloudFormation stacks, Lambda functions, and API Gateway

