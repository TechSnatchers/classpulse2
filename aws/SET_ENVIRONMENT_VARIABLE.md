# How to Set Environment Variable in Lambda

## Step-by-Step:

1. **In Lambda Console:**
   - Go to your `zoom_webhook` function
   - Click **"Configuration"** tab (left sidebar)
   - Click **"Environment variables"** (under Configuration)

2. **Add Variable:**
   - Click **"Edit"** button
   - Click **"Add environment variable"**
   - **Key:** `BACKEND_API_URL`
   - **Value:** `http://localhost:3001`
   - Click **"Save"**

## Important Notes:

### For Local Testing:
- Use: `http://localhost:3001` (only works if Lambda can reach your local machine)
- **Better:** Use ngrok to expose localhost:
  1. Install ngrok: https://ngrok.com/download
  2. Run: `ngrok http 3001`
  3. Use the ngrok URL: `https://abc123.ngrok-free.app`

### For Production:
- Use your actual backend URL: `https://your-backend-domain.com`
- Make sure your backend is publicly accessible

## Quick Test:

After setting the variable:
1. Deploy your Lambda function
2. Test it
3. Check CloudWatch logs to see if it's connecting to your backend

