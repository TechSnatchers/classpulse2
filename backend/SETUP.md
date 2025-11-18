# Quick Setup Guide

## Step 1: Install Dependencies

```bash
cd backend
npm install
```

## Step 2: Start the Server

```bash
npm run dev
```

The server will start on `http://localhost:3001`

## Step 3: Test the Server

Open your browser and go to:
- `http://localhost:3001` - API root
- `http://localhost:3001/health` - Health check

## Troubleshooting

### "Cannot GET" Error

1. Make sure the server is running:
   ```bash
   cd backend
   npm run dev
   ```

2. Check if port 3001 is already in use:
   ```bash
   netstat -ano | findstr :3001
   ```

3. Verify the server is responding:
   - Open `http://localhost:3001/health` in your browser
   - You should see: `{"status":"ok","message":"Server is running"}`

### Port Already in Use

Change the port in `backend/src/server.ts`:
```typescript
const PORT = process.env.PORT || 3002; // Change 3001 to 3002
```

### Dependencies Not Installing

1. Delete `node_modules` folder:
   ```bash
   rm -rf node_modules
   ```

2. Delete `package-lock.json`:
   ```bash
   rm package-lock.json
   ```

3. Reinstall:
   ```bash
   npm install
   ```

## API Endpoints

Once the server is running, you can test:

- `GET http://localhost:3001/health` - Health check
- `GET http://localhost:3001/` - API info
- `POST http://localhost:3001/api/quiz/submit` - Submit quiz answer
- `GET http://localhost:3001/api/quiz/performance/:questionId?sessionId=xxx` - Get performance
- `POST http://localhost:3001/api/quiz/trigger` - Trigger question

