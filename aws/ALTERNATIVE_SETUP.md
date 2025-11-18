# Alternative Setup Methods for Zoom Webhook

If you're having issues with AWS Console, here are alternatives:

## Option 1: Use AWS CLI to Create Credentials

If you have AWS CLI configured with admin access:

```powershell
# Create IAM user for webhook
aws iam create-user --user-name zoom-webhook-deploy

# Create access key
$result = aws iam create-access-key --user-name zoom-webhook-deploy --output json | ConvertFrom-Json
$accessKey = $result.AccessKey.AccessKeyId
$secretKey = $result.AccessKey.SecretAccessKey

Write-Host "Access Key: $accessKey" -ForegroundColor Green
Write-Host "Secret Key: $secretKey" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  Save these credentials - you won't see the secret key again!" -ForegroundColor Yellow

# Attach necessary policies
aws iam attach-user-policy --user-name zoom-webhook-deploy --policy-arn arn:aws:iam::aws:policy/CloudFormationFullAccess
aws iam attach-user-policy --user-name zoom-webhook-deploy --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess
aws iam attach-user-policy --user-name zoom-webhook-deploy --policy-arn arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator
```

Then configure:
```powershell
aws configure
# Use the new access key and secret key
```

## Option 2: Use AWS Console (After Fixing Access)

1. **Fix the security verification:**
   - Reload the page
   - Check email for verification
   - Complete account setup

2. **Create IAM User:**
   - Go to IAM → Users → Add users
   - Enable "Programmatic access"
   - Attach policies:
     - CloudFormationFullAccess
     - AWSLambda_FullAccess
     - AmazonAPIGatewayAdministrator

3. **Get Credentials:**
   - After creating user, go to "Security credentials"
   - Create access key
   - Save both keys

## Option 3: Deploy via AWS Console (No CLI Needed)

If you can access AWS Console:

1. Go to: https://console.aws.amazon.com/cloudformation/
2. Click "Create stack" → "With new resources"
3. Choose "Upload a template file"
4. Upload: `aws/cloudformation/zoom-webhook-stack.yaml`
5. Enter parameters manually
6. Create stack
7. Get webhook URL from "Outputs" tab

## Option 4: Test Without AWS (Local Development)

For local testing, you can skip AWS and test directly:

1. Make sure your backend is running: `python main.py`
2. Use ngrok or similar to expose localhost:
   ```bash
   ngrok http 3001
   ```
3. Use the ngrok URL as your webhook endpoint in Zoom
4. This is for testing only - use AWS for production

## Recommended Next Steps

1. **Try reloading AWS Console page** (most common fix)
2. **Check your email** for AWS verification messages
3. **If still stuck**, use Option 4 (ngrok) for local testing first
4. **Then set up AWS** properly for production

