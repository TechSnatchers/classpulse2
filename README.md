# Learning Platform 🎓

A full-stack adaptive learning platform with real-time engagement features, built with React, FastAPI, and MongoDB. Includes Zoom integration for live sessions with automated attendance tracking and participant monitoring.

## 🌟 Features

- **User Management** - Role-based access (Student, Instructor, Admin)
- **Authentication** - Secure JWT-based authentication
- **Live Sessions** - Integration with Zoom for virtual classes
- **Real-time Questions** - Live Q&A during sessions
- **Quiz System** - Interactive quizzes with performance tracking
- **Clustering** - K-means clustering for student performance analysis
- **Attendance Tracking** - Automated attendance via Zoom webhooks
- **Responsive Design** - Modern UI with Tailwind CSS

## 🏗️ Architecture

```
Frontend (React + Vite)  →  Backend (FastAPI)  →  MongoDB Atlas
                                    ↓
                              Zoom Webhooks
```

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- Python 3.10+
- MongoDB (Atlas or local)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Arunpragash22/learningApp.git
cd learningApp
```

2. **Start Backend**
```bash
cd backend
pip install -r requirements.txt
# Create .env file (see backend/env_template.txt)
python main.py
```

3. **Start Frontend**
```bash
cd frontend
npm install
npm run dev
```

4. **Access Application**
- Frontend: http://localhost:5173
- Backend: http://localhost:3001
- API Docs: http://localhost:3001/docs

### Default Credentials

- **Student:** student@example.com / password123
- **Instructor:** instructor@example.com / password123
- **Admin:** admin@example.com / password123

## 🌐 Deploy to AWS EC2

We provide automated deployment scripts for AWS EC2:

```bash
# On your EC2 instance
./ec2-setup.sh      # Install dependencies (one-time)
./deploy-to-ec2.sh  # Deploy application
```

See [EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📁 Project Structure

```
learningApp/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── utils/        # Utilities
│   └── package.json
├── backend/               # FastAPI backend
│   ├── src/
│   │   ├── routers/      # API routes
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── database/     # Database connection
│   ├── main.py           # Entry point
│   └── requirements.txt
├── backend_flask/        # Flask backend (alternative)
├── backend_realtime/     # Real-time features
├── aws/                  # AWS Lambda/CloudFormation
├── ec2-setup.sh         # EC2 setup script
├── deploy-to-ec2.sh     # Deployment script
└── README.md
```

## 🛠️ Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Lucide Icons

### Backend
- FastAPI
- Python 3.10+
- Motor (async MongoDB)
- Pydantic
- Uvicorn

### Database
- MongoDB Atlas

### Deployment
- AWS EC2
- Nginx
- Systemd

## 📖 Documentation

- [EC2 Deployment Guide](./EC2_DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [Quick EC2 Deploy](./QUICK_EC2_DEPLOY.md) - 5-minute deployment guide
- [Deployment Checklist](./EC2_DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist
- [Setup Instructions](./SETUP_INSTRUCTIONS.md) - Local development setup

## 🔧 Configuration

### Backend Configuration

Create `backend/.env`:

```env
# MongoDB
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=learning_platform

# Server
PORT=3001
FRONTEND_URL=http://localhost:5173

# Zoom API (optional)
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_ACCOUNT_ID=your_account_id
```

### Frontend Configuration

Create `frontend/.env.production`:

```env
VITE_API_URL=http://your-domain:3001
```

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### Quiz
- `POST /api/quiz/submit` - Submit quiz answer
- `GET /api/quiz/performance/{question_id}` - Get performance

### Clustering
- `GET /api/clustering/session/{session_id}` - Get clusters
- `POST /api/clustering/update` - Update clusters

### Zoom
- `POST /api/zoom-webhook` - Zoom webhook handler
- `GET /api/zoom/participants` - Get participants

Full API documentation: http://localhost:3001/docs

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Arunpragash22 - [GitHub](https://github.com/Arunpragash22)

## 🙏 Acknowledgments

- FastAPI for the excellent backend framework
- React team for the frontend library
- MongoDB for the database solution
- Zoom for the video conferencing API

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the troubleshooting section in deployment guides

## 🔒 Security

- Never commit `.env` files
- Use strong passwords for MongoDB
- Enable SSL/HTTPS in production
- Keep dependencies updated

## 🚦 Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

**Built with ❤️ for better learning experiences**

