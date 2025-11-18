# Testing Zoom Webhook Without AWS

You can test the Zoom webhook integration locally without AWS! Here's how:

## Option 1: Use ngrok (Recommended for Testing)

ngrok creates a public URL that forwards to your local backend.

### Step 1: Install ngrok

**Download from:** https://ngrok.com/download

Or using Chocolatey:
```powershell
choco install ngrok
```

### Step 2: Start Your Backend

```powershell
cd ..\backend
python main.py
```

Keep this running in one terminal.

### Step 3: Expose Backend with ngrok

In a **new terminal**:
```powershell
ngrok http 3001
```

You'll get a URL like: `https://abc123.ngrok-free.app`

### Step 4: Configure Zoom

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Your App → Event Subscriptions
3. Add Event Subscription:
   - **Endpoint URL**: `https://abc123.ngrok-free.app/api/zoom/webhook`
   - **Events**: Select the events you want
4. Save

### Step 5: Test

Create a Zoom meeting and trigger events. Check your backend logs to see webhook events.

## Option 2: Test Webhook Endpoint Directly

You can test the webhook endpoint manually:

```powershell
# Test health endpoint
Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook/health"

# Test with sample event
$body = @{
    event = "meeting.started"
    event_ts = [int64]((Get-Date).ToUniversalTime() - (Get-Date "1970-01-01")).TotalMilliseconds
    payload = @{
        account_id = "test_account"
        object = @{
            id = "123456789"
            uuid = "test-uuid"
            topic = "Test Meeting"
            host_id = "test_host"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:3001/api/zoom/webhook" -Method POST -Body $body -ContentType "application/json"
```

## Option 3: Create AWS Account (For Production)

If you want to use AWS for production later:

1. **Sign up for AWS:**
   - Go to: https://aws.amazon.com/
   - Click "Create an AWS Account"
   - Follow the signup process (requires credit card, but free tier available)

2. **After account is created:**
   - Go to IAM → Users → Add users
   - Create access keys
   - Configure: `aws configure`

## Recommendation

**For now:** Use ngrok (Option 1) to test everything locally
**Later:** Set up AWS account for production deployment

This way you can test the webhook integration immediately without waiting for AWS setup!

