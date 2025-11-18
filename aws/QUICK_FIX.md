# Quick Fix - Environment Variable

## The Problem:
- You added `.env` file with `BACKEND_API_URL = http://localhost:3001`
- Lambda doesn't read `.env` files automatically
- `localhost` won't work from AWS Lambda (it's in the cloud, can't reach your PC)

## The Solution:

### 1. Get ngrok URL (if you haven't already)

Open a new terminal:
```powershell
ngrok http 3001
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

### 2. Set Environment Variable in Lambda

**Don't use the `.env` file!** Instead:

1. In Lambda → Click **"Configuration"** tab (left sidebar)
2. Click **"Environment variables"**
3. Click **"Edit"**
4. Click **"Add environment variable"**
5. Enter:
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://abc123.ngrok-free.app` (your ngrok URL)
6. Click **"Save"**

### 3. Deploy Function

1. Go to **"Code"** tab
2. Click **"Deploy"** button (you see "undeployed changes")
3. Wait for deployment

### 4. Verify

Go back to **Configuration → Environment variables** and check:
- ✅ `BACKEND_API_URL` = `https://your-ngrok-url.ngrok-free.app`
- ❌ NOT `http://localhost:3001`

## Summary:

- ❌ `.env` file → Lambda doesn't use it
- ✅ Configuration → Environment variables → This is what Lambda uses
- ❌ `localhost` → Won't work from AWS
- ✅ ngrok URL → This works!

