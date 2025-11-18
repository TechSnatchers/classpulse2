# Learning Platform Backend API (Python)

Backend API server for the Learning Platform application, built with FastAPI and MongoDB.

## Prerequisites

1. **Python 3.8 or higher**
2. **MongoDB** - Install MongoDB locally or use MongoDB Atlas (cloud)

### Installing MongoDB

**Windows:**
- Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- Or use MongoDB Atlas (free cloud tier): [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community
```

## Setup

1. **Create a virtual environment (recommended):**
```bash
python -m venv venv
```

2. **Activate the virtual environment:**
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start MongoDB:**
   - If installed locally, start MongoDB service:
   ```bash
   # Windows (as Administrator)
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl start mongod
   # or
   mongod
   ```

5. **Configure MongoDB Atlas:**
   
   **a. Get your MongoDB Atlas connection string:**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   
   **b. Configure your connection:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and replace `<db_password>` with your actual MongoDB Atlas password:
     ```
     PORT=3001
     MONGODB_URL=mongodb+srv://shawmi3030_db_user:YOUR_PASSWORD_HERE@m0.zcjoclr.mongodb.net/?appName=M0
     DATABASE_NAME=learning_platform
     ```
   
   **c. Whitelist your IP address in MongoDB Atlas:**
   - Go to MongoDB Atlas → Network Access
   - Click "Add IP Address"
   - For development, you can use "Allow Access from Anywhere" (0.0.0.0/0)
   - ⚠️ **Note:** For production, use specific IP addresses for security

6. **Seed the database (optional):**
   This will create default users and questions:
   ```bash
   # From the backend directory:
   python src/database/seed.py
   
   # Or run as a module:
   python -m src.database.seed
   ```
   
   Default users:
   - Student: `student@example.com` / `password123`
   - Instructor: `instructor@example.com` / `password123`
   - Admin: `admin@example.com` / `password123`

7. **Start the development server:**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --port 3001
```

The server will run on `http://localhost:3001`

## API Endpoints

### Health Check
- `GET /health` - Check if server is running

### Authentication Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Quiz Endpoints
- `POST /api/quiz/submit` - Submit a quiz answer
- `GET /api/quiz/performance/{question_id}?session_id={session_id}` - Get quiz performance (instructor only)
- `POST /api/quiz/trigger` - Trigger a question (instructor only)

### Clustering Endpoints
- `GET /api/clustering/session/{session_id}` - Get clusters for a session
- `POST /api/clustering/update` - Update clusters based on quiz performance
- `GET /api/clustering/student/{student_id}?session_id={session_id}` - Get student's cluster assignment

## Environment Variables

Create a `.env` file in the backend directory (copy from `.env.example`):

**For MongoDB Atlas:**
```
PORT=3001
MONGODB_URL=mongodb+srv://shawmi3030_db_user:YOUR_PASSWORD@m0.zcjoclr.mongodb.net/?appName=M0
DATABASE_NAME=learning_platform
```

**For Local MongoDB:**
```
PORT=3001
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=learning_platform
```

⚠️ **Important:** Replace `YOUR_PASSWORD` with your actual MongoDB Atlas database user password.

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:3001/docs`
- ReDoc: `http://localhost:3001/redoc`

## Development

The server uses FastAPI with uvicorn for hot reloading. Use the `--reload` flag for development.

## Production

For production, use a production ASGI server like:
```bash
uvicorn main:app --host 0.0.0.0 --port 3001
```

Or use gunicorn with uvicorn workers:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```
