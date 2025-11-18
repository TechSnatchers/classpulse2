# Learning Platform - EC2 Deployment Package 🚀

Complete deployment package for deploying your Learning Platform to AWS EC2.

## 📦 What's Included

This deployment package contains everything you need to deploy your full-stack Learning Platform to AWS EC2:

### 📄 Documentation
1. **[EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md)** - Complete deployment guide with detailed instructions
2. **[QUICK_EC2_DEPLOY.md](./QUICK_EC2_DEPLOY.md)** - Quick 5-minute deployment for experienced developers
3. **[EC2_DEPLOYMENT_CHECKLIST.md](./EC2_DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist to track progress

### 🔧 Scripts
1. **`ec2-setup.sh`** - Initial EC2 setup (installs Node.js, Python, Nginx, etc.)
2. **`deploy-to-ec2.sh`** - Main deployment script (deploys backend + frontend)
3. **`update-app.sh`** - Update application after code changes
4. **`monitor-app.sh`** - Health check and monitoring script

## 🎯 Quick Start

Choose your experience level:

### For Beginners
👉 Follow the **[EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md)** - includes detailed explanations

### For Experienced Developers
👉 Follow the **[QUICK_EC2_DEPLOY.md](./QUICK_EC2_DEPLOY.md)** - deploy in 5 minutes

### Using Checklist
👉 Use **[EC2_DEPLOYMENT_CHECKLIST.md](./EC2_DEPLOYMENT_CHECKLIST.md)** - track your progress

## ⚡ Super Quick Deploy (3 Steps)

If you have EC2 already running:

```bash
# 1. Upload code to /var/www/learning-platform
scp -i key.pem -r ./project_fyp-main ubuntu@ec2-ip:/home/ubuntu/

# 2. SSH and move files
ssh -i key.pem ubuntu@ec2-ip
sudo mv /home/ubuntu/project_fyp-main /var/www/learning-platform
cd /var/www/learning-platform

# 3. Run setup and deploy
chmod +x *.sh
./ec2-setup.sh
./deploy-to-ec2.sh
```

That's it! Your app will be running.

## 📋 Prerequisites

Before deployment, ensure you have:

- ✅ AWS account with EC2 access
- ✅ EC2 instance (Ubuntu 22.04 LTS, t2.medium+)
- ✅ SSH key pair
- ✅ Security Group with ports: 22, 80, 443, 3001
- ✅ MongoDB Atlas account (or local MongoDB)
- ✅ Domain name (optional)

## 🏗️ Architecture

After deployment, your stack will look like:

```
┌─────────────────────────────────────────────────┐
│                  Internet                        │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│            AWS EC2 Instance                      │
│                                                   │
│  ┌─────────────────────────────────────────┐   │
│  │         Nginx (Port 80/443)              │   │
│  │  - Serves Frontend (React)               │   │
│  │  - Proxies API to Backend                │   │
│  └──────┬────────────────────┬──────────────┘   │
│         │                    │                   │
│  ┌──────▼──────────┐  ┌──────▼─────────────┐   │
│  │    Frontend      │  │   Backend API      │   │
│  │  (React/Vite)    │  │   (FastAPI)        │   │
│  │  Static Files    │  │   Port 3001        │   │
│  └──────────────────┘  └──────┬─────────────┘   │
│                               │                   │
└───────────────────────────────┼───────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   MongoDB Atlas        │
                    │   (Cloud Database)     │
                    └────────────────────────┘
```

## 📖 Detailed Script Descriptions

### `ec2-setup.sh`
**Purpose:** Initial setup of a fresh EC2 instance

**What it does:**
- Updates Ubuntu packages
- Installs Node.js 18.x
- Installs Python 3.10+
- Installs Nginx web server
- Installs PM2 process manager
- Installs Git
- Optionally installs local MongoDB
- Configures firewall rules
- Installs Certbot for SSL

**When to run:** Once, when first setting up EC2

**Runtime:** 5-10 minutes

**Usage:**
```bash
chmod +x ec2-setup.sh
./ec2-setup.sh
```

---

### `deploy-to-ec2.sh`
**Purpose:** Deploy or redeploy the application

**What it does:**
- Pulls latest code (if git repo)
- Sets up Python virtual environment
- Installs backend dependencies
- Creates backend .env file
- Creates systemd service for backend
- Installs frontend dependencies
- Builds frontend for production
- Configures Nginx
- Optionally sets up SSL

**When to run:** 
- First deployment after ec2-setup.sh
- Major redeployment (not for regular updates)

**Runtime:** 5-10 minutes

**Usage:**
```bash
chmod +x deploy-to-ec2.sh
./deploy-to-ec2.sh
```

**Interactive prompts:**
- Domain name (or use EC2 IP)
- MongoDB choice (local/Atlas)
- MongoDB connection string (if Atlas)
- SSL setup (yes/no)

---

### `update-app.sh`
**Purpose:** Update application after code changes

**What it does:**
- Pulls latest code from git
- Updates backend dependencies
- Restarts backend service
- Updates frontend dependencies
- Rebuilds frontend
- Deploys new frontend files
- Reloads Nginx

**When to run:** After pushing new code changes

**Runtime:** 2-5 minutes

**Usage:**
```bash
./update-app.sh
```

**No prompts** - fully automated

---

### `monitor-app.sh`
**Purpose:** Check application health and status

**What it does:**
- Checks backend service status
- Tests backend API health
- Checks Nginx status
- Checks MongoDB (if local)
- Shows disk, memory, CPU usage
- Shows listening ports
- Shows recent logs

**When to run:** 
- After deployment to verify
- When troubleshooting issues
- Regular health checks

**Runtime:** < 5 seconds

**Usage:**
```bash
./monitor-app.sh
```

## 🔄 Common Workflows

### First-Time Deployment
```bash
# 1. Setup EC2
./ec2-setup.sh

# 2. Deploy application
./deploy-to-ec2.sh

# 3. Verify deployment
./monitor-app.sh
```

### Regular Code Updates
```bash
# Update and redeploy
./update-app.sh

# Verify update
./monitor-app.sh
```

### Troubleshooting
```bash
# Check health
./monitor-app.sh

# View backend logs
sudo journalctl -u learning-platform-backend -f

# Restart services
sudo systemctl restart learning-platform-backend
sudo systemctl restart nginx
```

## 🌐 After Deployment

Your application will be accessible at:

- **Frontend:** `http://your-domain` or `http://ec2-ip`
- **Backend API:** `http://your-domain:3001`
- **API Documentation:** `http://your-domain:3001/docs`
- **API ReDoc:** `http://your-domain:3001/redoc`

### Default Login Credentials
- **Student:** `student@example.com` / `password123`
- **Instructor:** `instructor@example.com` / `password123`
- **Admin:** `admin@example.com` / `password123`

⚠️ **Change these in production!**

## 🔧 Service Management

### Backend Service
```bash
# Status
sudo systemctl status learning-platform-backend

# Start/Stop/Restart
sudo systemctl start learning-platform-backend
sudo systemctl stop learning-platform-backend
sudo systemctl restart learning-platform-backend

# View logs
sudo journalctl -u learning-platform-backend -f

# View last 100 lines
sudo journalctl -u learning-platform-backend -n 100
```

### Nginx Service
```bash
# Status
sudo systemctl status nginx

# Start/Stop/Restart
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx

# Test configuration
sudo nginx -t

# Reload (without downtime)
sudo systemctl reload nginx

# View logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## 🐛 Troubleshooting

### Quick Diagnostics
```bash
# Run health check
./monitor-app.sh

# Check all services
sudo systemctl status learning-platform-backend nginx

# Test backend locally
curl localhost:3001/health

# Test backend remotely
curl http://your-domain:3001/health
```

### Common Issues

**Backend not starting:**
```bash
sudo journalctl -u learning-platform-backend -n 50
cd /var/www/learning-platform/backend
cat .env  # Check configuration
```

**Frontend not loading:**
```bash
sudo nginx -t  # Test config
sudo tail -f /var/log/nginx/error.log
ls -la /var/www/learning-platform-frontend/
```

**Can't connect:**
- Check AWS Security Group
- Check firewall: `sudo ufw status`
- Check DNS: `nslookup your-domain.com`

**MongoDB connection:**
- Verify connection string in `.env`
- Check IP whitelist in MongoDB Atlas
- Test: `mongo "your-connection-string"`

## 📚 Additional Resources

### Documentation
- [EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [MongoDB Atlas](https://docs.atlas.mongodb.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

### Tools
- [AWS Console](https://console.aws.amazon.com/)
- [MongoDB Atlas Console](https://cloud.mongodb.com/)

## 🔐 Security Recommendations

1. **Change default passwords** in the application
2. **Restrict SSH** to your IP in Security Group
3. **Enable SSL/HTTPS** with Certbot
4. **Use strong MongoDB password**
5. **Whitelist specific IPs** in MongoDB Atlas
6. **Keep system updated:** `sudo apt update && sudo apt upgrade`
7. **Setup fail2ban:** `sudo apt install fail2ban`
8. **Regular backups** of database and EC2

## 📞 Support

If you need help:

1. Check the **[EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md)** troubleshooting section
2. Run `./monitor-app.sh` to diagnose issues
3. Check service logs
4. Review AWS Security Group settings

## 📝 File Structure After Deployment

```
/var/www/learning-platform/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env (created by deploy script)
│   ├── venv/ (created by deploy script)
│   └── src/
├── frontend/
│   ├── src/
│   ├── dist/ (created by build)
│   ├── package.json
│   └── vite.config.ts
├── ec2-setup.sh
├── deploy-to-ec2.sh
├── update-app.sh
└── monitor-app.sh

/var/www/learning-platform-frontend/
└── (built frontend files served by Nginx)

/etc/nginx/sites-available/
└── learning-platform (Nginx config)

/etc/systemd/system/
└── learning-platform-backend.service (systemd service)
```

## ✅ Success Indicators

Your deployment is successful when:

- ✅ `./monitor-app.sh` shows all services running
- ✅ `curl localhost:3001/health` returns `{"status":"ok"}`
- ✅ Frontend loads in browser
- ✅ Can login with default credentials
- ✅ No errors in browser console
- ✅ API calls work (check Network tab)

## 🎉 Next Steps

After successful deployment:

1. Test all application features
2. Update default passwords
3. Configure domain and SSL
4. Setup monitoring/alerts
5. Schedule regular backups
6. Document any customizations

---

**Happy Deploying! 🚀**

For questions or issues, refer to the detailed guides or check the troubleshooting sections.

