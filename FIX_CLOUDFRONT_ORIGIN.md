# Fix CloudFront Origin - Still Pointing to S3

## Problem
Your domain `zoomlearningapp.de` is still pointing to S3 instead of API Gateway.

## Solution: Verify and Update CloudFront Configuration

### Step 1: Check Current Origin
1. Go to: https://console.aws.amazon.com/cloudfront/
2. Click on: `learning-platform-api-cloudfront`
3. Click **"Origins"** tab
4. Check what origins you have:
   - If you see S3 bucket → Need to update
   - If you see API Gateway → Check behaviors

### Step 2: Verify Behaviors
1. Click **"Behaviors"** tab
2. Check the default behavior (`*` path pattern):
   - **Origin and origin groups:** Should be `api-gateway-origin` (not S3)
   - If it's still S3 → Click "Edit" and change it

### Step 3: Update Behavior (If Needed)
1. Click **"Edit"** on the default behavior
2. **Origin and origin groups:** Select `api-gateway-origin` (or your API Gateway origin name)
3. Make sure these are set:
   - **Viewer protocol policy:** Redirect HTTP to HTTPS
   - **Allowed HTTP methods:** GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
   - **Cache policy:** CachingDisabled
   - **Origin request policy:** AllViewerExceptHostHeader
   - **Response headers policy:** zoom-security-headers
4. Click **"Save changes"**

### Step 4: Deploy
1. Click **"Actions"** → **"Deploy"**
2. Wait 5-15 minutes

### Step 5: Test Again
```bash
curl https://zoomlearningapp.de/health
```

Should return JSON from your FastAPI backend, not S3 error.

## Alternative: Create Separate Behavior for API

If you want to keep S3 for root but route `/api/*` to API Gateway:

1. **Behaviors** tab → **Create behavior**
2. **Path pattern:** `/api/*`
3. **Origin:** `api-gateway-origin`
4. **Cache policy:** CachingDisabled
5. **Origin request policy:** AllViewerExceptHostHeader
6. **Response headers policy:** zoom-security-headers
7. Click **"Create behavior"**
8. Deploy

This way:
- `https://zoomlearningapp.de/` → S3 (index.html)
- `https://zoomlearningapp.de/api/*` → API Gateway (your backend)

