# Setting BACKEND_API_URL in Lambda

## Location in AWS Console:

**Lambda Function → Configuration → Environment variables**

## Detailed Steps:

1. **Navigate:**
   ```
   Lambda Console
   → Functions
   → zoom_webhook
   → Configuration tab (left sidebar)
   → Environment variables (under Configuration section)
   ```

2. **Add Variable:**
   - Click **"Edit"** button (top right)
   - Click **"Add environment variable"**
   - Enter:
     - **Key:** `BACKEND_API_URL`
     - **Value:** `http://localhost:3001`
   - Click **"Save"**

## Important: Localhost Won't Work from Lambda!

⚠️ **Problem:** Lambda runs in AWS cloud and can't reach `localhost:3001` on your computer.

### Solution Options:

**Option 1: Use ngrok (For Testing)**
```powershell
# Install ngrok
# Download from: https://ngrok.com/download

# Start your backend
cd backend
python main.py

# In another terminal, expose it
ngrok http 3001
```

Then use the ngrok URL in the environment variable:
- **Value:** `https://abc123.ngrok-free.app`

**Option 2: Deploy Backend to Cloud (Production)**
- Deploy your backend to a cloud service (AWS, Heroku, etc.)
- Use that public URL

**Option 3: Test Locally First**
- Skip Lambda for now
- Test webhook directly: `http://localhost:3001/api/zoom/webhook`
- Use ngrok to give Zoom a public URL

## Recommended Setup:

1. **Start backend:** `python main.py` (keep running)
2. **Start ngrok:** `ngrok http 3001` (get public URL)
3. **Set Lambda env var:** Use the ngrok URL
4. **Configure Zoom:** Use API Gateway URL

This way Lambda can reach your backend through ngrok!

