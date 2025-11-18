# Session Debugging Guide

## Common Session Issues and Solutions

### Issue 1: "Cannot GET" Error
**Cause:** Backend server is not running

**Solution:**
1. Open a terminal
2. Navigate to backend folder: `cd backend`
3. Start server: `npm run dev`
4. Verify: Open `http://localhost:3001/health` in browser

### Issue 2: Session ID Not Found
**Cause:** URL parameter is missing or incorrect

**Solution:**
- Check the URL: Should be `/dashboard/sessions/:sessionId`
- Verify sessionId is in the URL: `/dashboard/sessions/1` or `/dashboard/sessions/test-session`
- Check browser console for errors

### Issue 3: Clusters Not Loading
**Cause:** Backend API not responding or sessionId format issue

**Solution:**
1. Check browser console for API errors
2. Verify backend is running: `http://localhost:3001/health`
3. Test cluster endpoint: `http://localhost:3001/api/clustering/session/test-session`
4. Check network tab in browser DevTools

### Issue 4: Quiz Not Submitting
**Cause:** Missing sessionId or backend connection issue

**Solution:**
1. Check if sessionId exists in URL
2. Verify backend is running
3. Check browser console for errors
4. Try submitting answer again

## Testing Session Endpoints

### Test Backend Health
```bash
curl http://localhost:3001/health
```

### Test Get Clusters
```bash
curl http://localhost:3001/api/clustering/session/test-session-123
```

### Test Submit Answer
```bash
curl -X POST http://localhost:3001/api/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "questionId": "1",
    "answerIndex": 1,
    "timeTaken": 10.5,
    "studentId": "student123",
    "sessionId": "test-session-123"
  }'
```

### Test Get Performance
```bash
curl "http://localhost:3001/api/quiz/performance/1?sessionId=test-session-123"
```

## Debug Checklist

- [ ] Backend server is running on port 3001
- [ ] Health endpoint responds: `http://localhost:3001/health`
- [ ] Session ID is present in URL
- [ ] Browser console shows no CORS errors
- [ ] Network tab shows API requests
- [ ] Backend logs show incoming requests

## Quick Fix Commands

```bash
# Start backend
cd backend
npm install  # First time only
npm run dev

# Check if port is in use
netstat -ano | findstr :3001

# Test in browser
# Open: http://localhost:3001/health
```

