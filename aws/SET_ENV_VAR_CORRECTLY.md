# ⚠️ Important: .env File Doesn't Work in Lambda!

## The Problem:
You have `.env` file with:
```
BACKEND_API_URL = https://divertive-ricki-goadingly.ngrok-free.dev
```

**But Lambda doesn't read `.env` files!** You must set it as an environment variable.

## ✅ Correct Way to Set It:

### Step 1: Go to Lambda Configuration

1. **AWS Lambda Console**
2. **Your `zoom_webhook` function**
3. **Click "Configuration" tab** (left sidebar)
4. **Click "Environment variables"** (under Configuration)

### Step 2: Add Environment Variable

1. **Click "Edit" button**
2. **Click "Add environment variable"**
3. **Enter:**
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://divertive-ricki-goadingly.ngrok-free.dev`
4. **Click "Save"**

### Step 3: Verify

After saving, you should see:
- **Key:** `BACKEND_API_URL`
- **Value:** `https://divertive-ricki-goadingly.ngrok-free.dev`

## ❌ Don't Use:
- `.env` file in Lambda (Lambda doesn't read it)
- Code editor `.env` file (only for local development)

## ✅ Use:
- Lambda → Configuration → Environment variables

## After Setting:

1. **Deploy Lambda function** (Code tab → Deploy)
2. **Test Lambda** (Test tab)
3. **Check CloudWatch logs** - you should see:
   ```
   Backend URL: https://divertive-ricki-goadingly.ngrok-free.dev
   ```

## Quick Checklist:

- [ ] Lambda → Configuration → Environment variables
- [ ] Key: `BACKEND_API_URL`
- [ ] Value: `https://divertive-ricki-goadingly.ngrok-free.dev`
- [ ] Click Save
- [ ] Deploy Lambda function
- [ ] Test and check CloudWatch logs

