# Update CloudFront to Point to API Gateway

## Current Setup
- **Domain:** `zoomlearningapp.de`
- **CloudFront Distribution:** `learning-platform-api-cloudfront`
- **Current Origin:** S3 (showing sample index.html)
- **API Gateway:** `187183rknh.execute-api.eu-north-1.amazonaws.com`

## Steps to Update CloudFront

### Step 1: Go to CloudFront Console
1. Go to: https://console.aws.amazon.com/cloudfront/
2. Find your distribution: `learning-platform-api-cloudfront`
3. Click on it

### Step 2: Edit Origins
1. Click on the **"Origins"** tab
2. You'll see your current S3 origin
3. Click **"Create origin"** or **"Edit"** the existing origin

### Step 3: Update Origin Settings
**If creating new origin:**
- **Origin domain:** Select or enter: `187183rknh.execute-api.eu-north-1.amazonaws.com`
- **Name:** `api-gateway-origin` (or any name you prefer)
- **Origin path:** (leave blank)
- **Protocol:** HTTPS only
- **HTTP port:** 443
- **HTTPS port:** 443
- **Origin SSL protocols:** TLSv1.2

**If editing existing origin:**
- Change **Origin domain** from S3 bucket to: `187183rknh.execute-api.eu-north-1.amazonaws.com`
- Keep other settings the same

### Step 4: Update Default Cache Behavior
1. Go to **"Behaviors"** tab
2. Select the default behavior (the one with `*` path pattern)
3. Click **"Edit"**
4. Update **Origin and origin groups** to select your API Gateway origin
5. Make sure these settings are correct:
   - **Viewer protocol policy:** Redirect HTTP to HTTPS
   - **Allowed HTTP methods:** GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
   - **Cache policy:** CachingDisabled (for APIs)
   - **Origin request policy:** AllViewerExceptHostHeader
   - **Response headers policy:** zoom-security-headers
6. Click **"Save changes"**

### Step 5: Deploy Changes
1. Click **"Actions"** → **"Deploy"**
2. Wait 5-15 minutes for deployment

### Step 6: Test
After deployment, test:
```bash
curl https://zoomlearningapp.de/health
curl https://zoomlearningapp.de/
```

## Alternative: Keep S3 for Root, Route API to API Gateway

If you want to keep the S3 page for the root URL but route API calls to your backend:

### Create New Behavior for API Paths
1. Go to **"Behaviors"** tab
2. Click **"Create behavior"**
3. **Path pattern:** `/api/*`
4. **Origin:** Select your API Gateway origin
5. **Viewer protocol policy:** Redirect HTTP to HTTPS
6. **Allowed HTTP methods:** GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE
7. **Cache policy:** CachingDisabled
8. **Origin request policy:** AllViewerExceptHostHeader
9. **Response headers policy:** zoom-security-headers
10. Click **"Create behavior"**

This way:
- `https://zoomlearningapp.de/` → S3 (your index.html)
- `https://zoomlearningapp.de/api/*` → API Gateway (your FastAPI backend)

