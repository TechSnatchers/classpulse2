# Live Session Troubleshooting Guide

## Quick Checks

### 1. Is the backend server running?
```bash
cd backend
npm run dev
```

Check: Open `http://localhost:3001/health` - should show `{"status":"ok"}`

### 2. Is the sessionId in the URL?
- Correct: `/dashboard/sessions/1` or `/dashboard/sessions/test-session`
- Wrong: `/dashboard/sessions` (missing ID)

### 3. Check Browser Console
Open DevTools (F12) and look for:
- Errors in red
- Console logs showing sessionId
- Network tab showing API requests

## Common Issues

### Issue: "Session Not Found" message
**Cause:** sessionId is missing from URL

**Solution:**
1. Navigate to Sessions page: `/dashboard/sessions`
2. Click "Join Live" or "View Details" on a session
3. URL should be: `/dashboard/sessions/[session-id]`

### Issue: Page loads but shows blank/error
**Cause:** Backend not running or API errors

**Solution:**
1. Start backend: `cd backend && npm run dev`
2. Check console for API errors
3. Verify backend health: `http://localhost:3001/health`

### Issue: Clusters not loading
**Cause:** Backend API not responding

**Solution:**
- The app will use default/mock clusters if backend is down
- Check console for warnings: "Using fallback mock data"
- Start backend to get real cluster data

### Issue: Quiz not triggering
**Cause:** Missing sessionId or backend connection

**Solution:**
1. Check console logs for errors
2. Verify sessionId is in URL
3. Check if backend is running
4. For instructors: Make sure you're logged in as instructor/admin

## Debug Steps

1. **Open Browser Console (F12)**
   - Look for "LiveSession Debug Info" logs
   - Check sessionId value
   - Check for errors

2. **Check Network Tab**
   - Look for API requests to `/api/clustering/session/...`
   - Check if requests are successful (200 status)
   - Check response data

3. **Verify Route**
   - URL should match: `/dashboard/sessions/:sessionId`
   - sessionId should be a valid ID (e.g., "1", "test-session")

4. **Test Backend Manually**
   ```bash
   # Test health
   curl http://localhost:3001/health
   
   # Test clusters
   curl http://localhost:3001/api/clustering/session/test-session
   ```

## What Should Work

✅ **Session page loads** - Shows session title and info
✅ **Clusters load** - Shows engagement clusters (or defaults)
✅ **Quiz triggers** - Instructor can trigger questions
✅ **Quiz answers** - Students can submit answers
✅ **Performance shows** - Shows quiz performance after answering
✅ **Clusters update** - Clusters update based on quiz performance

## Still Not Working?

1. Share the browser console errors
2. Share the URL you're trying to access
3. Share backend logs (if running)
4. Check if you're logged in
5. Verify the route in App.tsx matches the URL

