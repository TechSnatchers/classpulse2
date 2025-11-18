# How to Start ngrok

## Step 1: Download ngrok (if not installed)

**Download from:** https://ngrok.com/download

Or using Chocolatey:
```powershell
choco install ngrok
```

## Step 2: Start ngrok

Open a **new terminal** and type:

```powershell
ngrok http 3001
```

That's it! Just those 3 words: `ngrok http 3001`

## Step 3: Copy the URL

You'll see output like this:

```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3001
```

**Copy the HTTPS URL** (the one starting with `https://`)

Example: `https://abc123.ngrok-free.app`

## Step 4: Use in Lambda

Use this URL in Lambda environment variable:
- Key: `BACKEND_API_URL`
- Value: `https://abc123.ngrok-free.app` (your actual ngrok URL)

## Keep It Running

**Important:** Keep the ngrok terminal open! If you close it, the URL will stop working.

You need 3 things running:
1. ✅ Backend: `python main.py` (in one terminal)
2. ✅ ngrok: `ngrok http 3001` (in another terminal)
3. ✅ Lambda function (deployed in AWS)

## Troubleshooting

**"ngrok not found"**
- Make sure ngrok is installed
- Or use full path to ngrok.exe

**"Port 3001 already in use"**
- Make sure your backend is running first
- Or use a different port: `ngrok http 3002` (and update backend port)

