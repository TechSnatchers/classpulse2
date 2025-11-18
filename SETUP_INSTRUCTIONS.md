# Setup Instructions - Registration & Login with MongoDB

## Prerequisites
- Python 3.10+ installed
- Node.js 16+ installed
- MongoDB Atlas account (or local MongoDB)

## Step 1: Start the Backend Server

Open a terminal in the project root:

```powershell
cd backend
python -m pip install -r requirements.txt
python main.py
```

You should see:
```
✅ Connected to MongoDB Atlas: learning_platform
🚀 Server running on http://localhost:3001
```

**Important:** Make sure you see "Connected to MongoDB" - if not, check your MongoDB connection string in `backend/.env`

## Step 2: Start the Frontend Server

Open a NEW terminal in the project root:

```powershell
npm install
npm run dev
```

You should see:
```
VITE ready at http://localhost:5173
```

## Step 3: Test Registration

1. Open browser: `http://localhost:5173`
2. Click "Register" or go to `http://localhost:5173/register`
3. Fill in the form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Password: password123
   - Role: Student
4. Click "Create Account"
5. You should see "Registration successful!"

## Step 4: View Registered Users

1. Login as instructor:
   - Email: `instructor@example.com`
   - Password: `password123`
2. Click "Users" in the sidebar
3. You should see all registered users from MongoDB

## Troubleshooting "Failed to Fetch"

### Issue: Frontend can't connect to backend

**Check 1: Is backend running?**
- Backend must be running on `http://localhost:3001`
- You should see the startup messages in the backend terminal

**Check 2: Check the backend terminal for errors**
- Look for "✅ Connected to MongoDB" message
- If you see MongoDB connection errors, check your `.env` file

**Check 3: Test backend directly**
- Open browser: `http://localhost:3001/health`
- You should see: `{"status":"ok","message":"Server is running"}`
- If this doesn't work, the backend is not running properly

**Check 4: Check browser console**
- Press F12 to open developer tools
- Go to Console tab
- Look for error messages
- Common errors:
  - `net::ERR_CONNECTION_REFUSED` - Backend not running
  - `CORS error` - Backend CORS settings (should be fixed)

**Check 5: Verify ports**
- Frontend should be on: `http://localhost:5173`
- Backend should be on: `http://localhost:3001`

## MongoDB Connection

The backend needs MongoDB to store user data. You have two options:

### Option 1: MongoDB Atlas (Cloud - Recommended)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Update `backend/.env`:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=learning_platform
   ```

### Option 2: Local MongoDB
1. Install MongoDB locally
2. Start MongoDB service
3. Update `backend/.env`:
   ```
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=learning_platform
   ```

## Default Test Accounts

After first run, these accounts are automatically created:

- **Student**: `student@example.com` / `password123`
- **Instructor**: `instructor@example.com` / `password123`
- **Admin**: `admin@example.com` / `password123`

## API Endpoints

Once backend is running:

- Health Check: `GET http://localhost:3001/health`
- Register: `POST http://localhost:3001/api/auth/register`
- Login: `POST http://localhost:3001/api/auth/login`
- Get Users: `GET http://localhost:3001/api/auth/users` (instructor/admin only)

## Still Having Issues?

1. **Restart both servers** (backend and frontend)
2. **Clear browser cache** (Ctrl + F5)
3. **Check MongoDB is connected** - look for the success message in backend terminal
4. **Test backend health endpoint** - `http://localhost:3001/health`
5. **Check backend terminal for errors** - especially MongoDB connection errors

## Success Indicators

✅ Backend terminal shows: "Connected to MongoDB Atlas"
✅ Backend health endpoint works: `http://localhost:3001/health`
✅ Frontend loads without errors
✅ Registration form submits successfully
✅ Can view users in User Management page


