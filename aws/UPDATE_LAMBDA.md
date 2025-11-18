# Update Your Existing Lambda Function

You already have a Lambda function created! Here's how to update it with the Zoom webhook code.

## Step 1: Update Lambda Function Code

1. **In AWS Lambda Console:**
   - Click on your `zoom_webhook` function
   - Go to the "Code" tab
   - Click "Upload from" → ".zip file" or edit inline

2. **Option A: Edit Inline (Quick)**
   - Delete existing code
   - Copy code from `aws/lambda/zoom_webhook_handler.py`
   - Paste into the editor
   - Click "Deploy"

3. **Option B: Upload ZIP (Recommended)**
   - Create a ZIP file with:
     - `zoom_webhook_handler.py`
     - `requirements.txt` (with `requests` package)
   - Upload the ZIP file

## Step 2: Set Environment Variables

In Lambda function → Configuration → Environment variables:

Add:
- **Key**: `BACKEND_API_URL`
- **Value**: `http://localhost:3001` (or your backend URL)

## Step 3: Get API Gateway URL

1. **In Lambda Console:**
   - Go to "Configuration" tab
   - Click "Triggers"
   - Click on the API Gateway trigger
   - Copy the "API endpoint" URL

   It will look like:
   ```
   https://abc123.execute-api.eu-north-1.amazonaws.com/prod/webhook
   ```

## Step 4: Configure Zoom

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Your App → Event Subscriptions
3. Add Event Subscription:
   - **Endpoint URL**: Paste the API Gateway URL from Step 3
   - **Events**: Select:
     - `meeting.started`
     - `meeting.ended`
     - `participant.joined`
     - `participant.left`
     - `recording.completed`
4. Save and verify

## Step 5: Test

1. Create a test Zoom meeting
2. Check Lambda logs: Lambda → Monitor → View CloudWatch logs
3. Check your backend logs

## Quick Commands (If you have AWS CLI configured)

```powershell
# Update function code
aws lambda update-function-code `
  --function-name zoom_webhook `
  --zip-file fileb://function.zip `
  --region eu-north-1

# Update environment variable
aws lambda update-function-configuration `
  --function-name zoom_webhook `
  --environment Variables="{BACKEND_API_URL=http://localhost:3001}" `
  --region eu-north-1

# Get API Gateway URL
aws apigateway get-rest-apis --region eu-north-1
```

