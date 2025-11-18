# Quick Deploy Guide - Zoom Webhook with AWS

## Prerequisites Check

### 1. Install AWS CLI

**Option A: Automatic (PowerShell)**
```powershell
cd aws
.\install-aws-cli.ps1
```

**Option B: Manual**
1. Download: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Run the installer
3. Restart PowerShell

**Option C: Using Chocolatey**
```powershell
choco install awscli
```

### 2. Configure AWS Credentials

```powershell
aws configure
```

You'll need:
- **AWS Access Key ID** - Get from AWS Console → IAM → Users → Security credentials
- **AWS Secret Access Key** - Same location
- **Default region** - e.g., `us-east-1`
- **Default output format** - `json`

### 3. Get AWS Credentials

1. Go to: https://console.aws.amazon.com/iam/
2. Click "Users" → Your user (or create new)
3. Go to "Security credentials" tab
4. Click "Create access key"
5. Choose "Command Line Interface (CLI)"
6. **Save both keys** (you won't see the secret again!)

## Deploy

### Step 1: Update Parameters

Edit `parameters.json` (or create it):
```json
[
  {
    "ParameterKey": "BackendApiUrl",
    "ParameterValue": "http://localhost:3001"
  },
  {
    "ParameterKey": "ZoomWebhookSecretToken",
    "ParameterValue": "YOUR_ZOOM_SECRET_TOKEN"
  }
]
```

### Step 2: Deploy

```powershell
aws cloudformation create-stack --stack-name zoom-webhook-stack --template-body file://cloudformation/zoom-webhook-stack.yaml --parameters file://parameters.json --capabilities CAPABILITY_NAMED_IAM
```

### Step 3: Wait

```powershell
aws cloudformation wait stack-create-complete --stack-name zoom-webhook-stack
```

### Step 4: Get Webhook URL

```powershell
aws cloudformation describe-stacks --stack-name zoom-webhook-stack --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" --output text
```

## Alternative: Use AWS Console (No CLI)

If you don't want to install AWS CLI:

1. Go to: https://console.aws.amazon.com/cloudformation/
2. Click "Create stack" → "With new resources"
3. Choose "Upload a template file"
4. Upload: `aws/cloudformation/zoom-webhook-stack.yaml`
5. Enter parameters:
   - BackendApiUrl: `http://localhost:3001`
   - ZoomWebhookSecretToken: Your Zoom secret
6. Click through and create stack
7. Get webhook URL from "Outputs" tab

