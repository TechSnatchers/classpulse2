# EC2 Deployment Guide - Learning Platform

Complete guide to deploy your Learning Platform (React Frontend + Python Backend) to AWS EC2.

## 📋 Prerequisites

1. **AWS Account** with EC2 access
2. **EC2 Instance** (recommended: t2.medium or larger)
   - OS: Ubuntu 22.04 LTS
   - Storage: At least 20GB
3. **Security Group** with ports open:
   - 22 (SSH)
   - 80 (HTTP)
   - 443 (HTTPS)
   - 3001 (Backend API)
4. **Domain Name** (optional but recommended)
5. **MongoDB Atlas Account** (recommended) or local MongoDB

## 🚀 Quick Deployment (3 Steps)

### Step 1: Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose **Ubuntu Server 22.04 LTS**
4. Select instance type: **t2.medium** (or larger)
5. Configure Security Group:
   ```
   Type              Protocol    Port Range    Source
   SSH               TCP         22            0.0.0.0/0
   HTTP              TCP         80            0.0.0.0/0
   HTTPS             TCP         443           0.0.0.0/0
   Custom TCP        TCP         3001          0.0.0.0/0
   ```
6. Create or select an SSH key pair
7. Launch the instance

### Step 2: Connect to EC2 and Upload Code

**Connect via SSH:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

**Upload your project code:**

**Option A: Using Git (Recommended)**
```bash
cd /var/www
sudo mkdir -p learning-platform
sudo chown -R $USER:$USER learning-platform
cd learning-platform
git clone https://github.com/your-username/your-repo.git .
```

**Option B: Using SCP from your local machine**
```bash
# From your local machine
scp -i your-key.pem -r ./project_fyp-main ubuntu@your-ec2-ip:/home/ubuntu/
```

Then on EC2:
```bash
sudo mv /home/ubuntu/project_fyp-main /var/www/learning-platform
sudo chown -R $USER:$USER /var/www/learning-platform
```

### Step 3: Run Setup and Deployment Scripts

```bash
cd /var/www/learning-platform

# Make scripts executable
chmod +x ec2-setup.sh deploy-to-ec2.sh

# Run initial setup (installs Node.js, Python, Nginx, etc.)
./ec2-setup.sh

# Run deployment script
./deploy-to-ec2.sh
```

The script will ask you:
1. Your domain name (or use EC2 IP)
2. MongoDB configuration (local or Atlas)
3. If you want SSL setup

**That's it!** Your application will be running at `http://your-domain-or-ip`

## 📁 What the Scripts Do

### `ec2-setup.sh`
- Updates system packages
- Installs Node.js 18.x
- Installs Python 3.10+
- Installs Nginx
- Installs PM2
- Installs Git
- Optionally installs MongoDB
- Sets up firewall rules
- Installs Certbot (for SSL)

### `deploy-to-ec2.sh`
- Pulls latest code (if using git)
- Sets up Python virtual environment
- Installs backend dependencies
- Creates backend `.env` file
- Creates systemd service for backend
- Installs frontend dependencies
- Builds frontend for production
- Configures Nginx as reverse proxy
- Optionally sets up SSL with Let's Encrypt

## 🔧 Manual Deployment Steps (Alternative)

If you prefer to deploy manually, follow these steps:

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python
sudo apt install -y python3 python3-pip python3-venv

# Install Nginx
sudo apt install -y nginx

# Install PM2
sudo npm install -g pm2

# Install Git
sudo apt install -y git
```

### 2. Setup Backend

```bash
cd /var/www/learning-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
```

Add to `.env`:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=learning_platform
PORT=3001
FRONTEND_URL=http://your-domain
DOMAIN=your-domain
BASE_URL=http://your-domain
```

**Create systemd service:**
```bash
sudo nano /etc/systemd/system/learning-platform-backend.service
```

Add:
```ini
[Unit]
Description=Learning Platform Backend API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/learning-platform/backend
Environment="PATH=/var/www/learning-platform/backend/venv/bin"
ExecStart=/var/www/learning-platform/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start backend:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable learning-platform-backend
sudo systemctl start learning-platform-backend
sudo systemctl status learning-platform-backend
```

### 3. Setup Frontend

```bash
cd /var/www/learning-platform/frontend

# Install dependencies
npm install

# Create production env
echo "VITE_API_URL=http://your-domain:3001" > .env.production

# Build for production
npm run build

# Copy to nginx directory
sudo mkdir -p /var/www/learning-platform-frontend
sudo cp -r dist/* /var/www/learning-platform-frontend/
sudo chown -R www-data:www-data /var/www/learning-platform-frontend
```

### 4. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/learning-platform
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/learning-platform-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend health and docs
    location ~ ^/(health|docs|redoc) {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/learning-platform /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Setup SSL (Optional but Recommended)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔒 MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your EC2 IP or use `0.0.0.0/0` for development
5. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
6. Add to backend `.env` file

## 🎯 Post-Deployment

### Test Your Deployment

```bash
# Test backend health
curl http://your-domain:3001/health

# Test frontend
curl http://your-domain

# View backend logs
sudo journalctl -u learning-platform-backend -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Service Management

```bash
# Backend service
sudo systemctl status learning-platform-backend
sudo systemctl restart learning-platform-backend
sudo systemctl stop learning-platform-backend
sudo systemctl start learning-platform-backend

# View logs
sudo journalctl -u learning-platform-backend -f

# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
sudo nginx -t  # Test configuration
```

### Update Your Application

```bash
cd /var/www/learning-platform

# Pull latest changes
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart learning-platform-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/learning-platform-frontend/

# Reload nginx
sudo systemctl reload nginx
```

## 🔧 Troubleshooting

### Backend Not Starting

```bash
# Check service status
sudo systemctl status learning-platform-backend

# View detailed logs
sudo journalctl -u learning-platform-backend -n 100

# Check if port 3001 is in use
sudo netstat -tulpn | grep 3001

# Test backend directly
cd /var/www/learning-platform/backend
source venv/bin/activate
python main.py
```

### Frontend Not Loading

```bash
# Check Nginx configuration
sudo nginx -t

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# Check if files exist
ls -la /var/www/learning-platform-frontend/

# Restart Nginx
sudo systemctl restart nginx
```

### MongoDB Connection Issues

```bash
# Test connection from EC2
mongo "mongodb+srv://your-connection-string"

# Or with Python
python3 -c "from pymongo import MongoClient; client = MongoClient('your-connection-string'); print(client.list_database_names())"

# Check if IP is whitelisted in MongoDB Atlas
# Go to: Atlas -> Network Access -> IP Whitelist
```

### Can't Access Application

1. **Check Security Group:** Ensure ports 80, 443, and 3001 are open
2. **Check Firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 3001/tcp
   ```
3. **Check if services are running:**
   ```bash
   sudo systemctl status learning-platform-backend
   sudo systemctl status nginx
   ```

## 🌐 Domain Setup

### Point Domain to EC2

1. Get your EC2 public IP
2. Go to your domain registrar (GoDaddy, Namecheap, etc.)
3. Add an A record:
   ```
   Type: A
   Name: @
   Value: your-ec2-public-ip
   TTL: 3600
   ```
4. Wait for DNS propagation (5-30 minutes)

### Setup SSL with Domain

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 📊 Monitoring & Logs

### View Real-time Logs

```bash
# Backend logs
sudo journalctl -u learning-platform-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# System logs
sudo tail -f /var/log/syslog
```

### Setup Log Rotation

Logs are automatically rotated by systemd and nginx. Check:
```bash
# View log rotation config
cat /etc/logrotate.d/nginx
```

## 🔐 Security Best Practices

1. **Update regularly:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use SSL/HTTPS in production**

3. **Restrict Security Group:**
   - Only allow SSH from your IP
   - Use VPN for sensitive operations

4. **Use strong passwords for MongoDB**

5. **Setup monitoring:**
   ```bash
   # Install monitoring tools
   sudo apt install -y htop iotop
   ```

6. **Regular backups:**
   - Backup MongoDB regularly
   - Create EC2 snapshots

## 🎓 Default Credentials

After deployment, you can login with:
- **Student:** `student@example.com` / `password123`
- **Instructor:** `instructor@example.com` / `password123`
- **Admin:** `admin@example.com` / `password123`

**⚠️ Change these passwords in production!**

## 📞 Support

If you encounter issues:
1. Check the logs (see Monitoring section)
2. Review the Troubleshooting section
3. Ensure all prerequisites are met
4. Check AWS Security Group settings

## 🎉 Success!

Your Learning Platform is now deployed! Access it at:
- **Frontend:** `http://your-domain`
- **Backend API:** `http://your-domain:3001`
- **API Documentation:** `http://your-domain:3001/docs`

