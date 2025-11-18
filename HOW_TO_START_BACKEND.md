# How to Start the Backend Server

## Quick Start

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies (first time only):**
   ```bash
   npm install
   ```

3. **Start the server:**
   ```bash
   npm run dev
   ```

4. **Verify it's running:**
   - Open your browser and go to: `http://localhost:3001/health`
   - You should see: `{"status":"ok","message":"Server is running"}`

## If you get "Cannot GET" error:

This means the backend server is NOT running. Follow these steps:

### Step 1: Check if server is running
Look for a terminal/console window that shows:
```
🚀 Server running on http://localhost:3001
📊 Health check: http://localhost:3001/health
```

### Step 2: Start the server
If you don't see the above message, start the server:
```bash
cd backend
npm run dev
```

### Step 3: Install dependencies if needed
If you get errors about missing modules:
```bash
cd backend
npm install
```

### Step 4: Check the port
The server runs on port 3001. If something else is using that port:
- Change the port in `backend/src/server.ts` (line 7)
- Or stop the application using port 3001

## Windows Users

You can also use the batch file:
```bash
cd backend
start.bat
```

## Testing the API

Once the server is running, test these endpoints:

1. **Health Check:**
   ```
   http://localhost:3001/health
   ```

2. **API Root:**
   ```
   http://localhost:3001/
   ```

3. **Get Clusters:**
   ```
   http://localhost:3001/api/clustering/session/test-session-id
   ```

## Common Issues

### "Cannot find module 'express'"
**Solution:** Run `npm install` in the backend directory

### "Port 3001 already in use"
**Solution:** Change the port in `backend/src/server.ts` or kill the process using port 3001

### "Command not found: npm"
**Solution:** Install Node.js from https://nodejs.org/

## Need Help?

1. Check the console output for error messages
2. Verify Node.js is installed: `node --version`
3. Verify npm is installed: `npm --version`
4. Check that you're in the correct directory (should see `package.json`)

