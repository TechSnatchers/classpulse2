# Fix Environment Variable in Lambda

## ⚠️ Important Notes:

1. **`.env` file doesn't work in Lambda** - Lambda doesn't automatically read `.env` files
2. **`localhost` won't work** - Lambda runs in AWS cloud and can't reach your local machine
3. **You need to use ngrok URL** - Lambda needs a public URL to reach your backend

## ✅ Correct Way to Set Environment Variable:

### Step 1: Get ngrok URL First

1. **Start ngrok** (if not already running):
   ```powershell
   ngrok http 3001
   ```

2. **Copy the HTTPS URL** (looks like: `https://abc123.ngrok-free.app`)

### Step 2: Set in Lambda Configuration

1. In Lambda Console → `zoom_webhook` function
2. Click **"Configuration"** tab (left sidebar)
3. Click **"Environment variables"** (under Configuration)
4. Click **"Edit"** button
5. Click **"Add environment variable"**
6. Enter:
   - **Key:** `BACKEND_API_URL`
   - **Value:** `https://abc123.ngrok-free.app` (your ngrok URL, NOT localhost!)
7. Click **"Save"**

### Step 3: Deploy Your Function

1. Go back to **"Code"** tab
2. Click **"Deploy"** button (or press `Ctrl+Shift+U`)
3. Wait for deployment to complete

## 🔍 Verify It's Set:

1. Go to **Configuration → Environment variables**
2. You should see:
   - `BACKEND_API_URL` = `https://your-ngrok-url.ngrok-free.app`

## ❌ Don't Use:

- ❌ `.env` file (Lambda doesn't read it)
- ❌ `http://localhost:3001` (won't work from AWS)

## ✅ Use:

- ✅ Configuration → Environment variables
- ✅ `https://your-ngrok-url.ngrok-free.app`

