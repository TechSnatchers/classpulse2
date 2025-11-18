# Start ngrok to Expose Your Backend

## Step 1: Download ngrok

Download from: https://ngrok.com/download

Or using Chocolatey:
```powershell
choco install ngrok
```

## Step 2: Start ngrok

In a **new terminal** (keep backend running):

```powershell
ngrok http 3001
```

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3001
```

## Step 3: Copy the HTTPS URL

Copy the `https://` URL (not the http:// one)

Example: `https://abc123.ngrok-free.app`

## Step 4: Set in Lambda

1. Go to Lambda → Configuration → Environment variables
2. Edit environment variables
3. Set:
   - Key: `BACKEND_API_URL`
   - Value: `https://abc123.ngrok-free.app` (your ngrok URL)
4. Save

## Step 5: Test

1. Get your API Gateway URL from Lambda → Configuration → Triggers
2. Test the webhook endpoint
3. Check backend logs to see if requests are coming through

## Keep Both Running

- **Terminal 1:** Backend (`python main.py`)
- **Terminal 2:** ngrok (`ngrok http 3001`)

Both need to stay running for the webhook to work!

